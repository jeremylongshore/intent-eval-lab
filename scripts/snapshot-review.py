#!/usr/bin/env python3
"""Build an offline, commit-bound review of a captured snapshot promotion.

Reuses the existing deterministic extractors, never executes code from the
compared Git trees, fetches upstream, edits a kernel schema, or approves a merge.
Recommendations cover extracted facts only; unprojected prose needs review.
"""

from __future__ import annotations

import argparse
import contextlib
import difflib
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REGISTRY = "specs/upstream-surface-registry.v1.json"
EXTRACTORS = {
    "agentskills-spec": ("spec-projection-diff.py", "extract_projection"),
    "claude-hooks": ("extract-hook-config-projection.py", "extract_reference_doc"),
    "plugins-reference": ("extract-plugin-manifest-projection.py", "extract_reference_doc"),
    "sub-agents": ("extract-agent-definition-projection.py", "extract_reference_doc"),
    "plugin-marketplaces": ("extract-marketplace-catalog-projection.py", "extract_reference_doc"),
}


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def resolve(root: Path, ref: str) -> str:
    return git(root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()


def read(root: Path, commit: str, path: str) -> bytes:
    size = int(git(root, "cat-file", "-s", f"{commit}:{path}"))
    if size > 8 * 1024 * 1024:
        raise ValueError(f"Snapshot review input exceeds 8 MiB: {path}")
    return git(root, "show", f"{commit}:{path}")


def surfaces(root: Path, commit: str) -> dict[str, dict[str, Any]]:
    registry = json.loads(read(root, commit, REGISTRY))
    result = {}
    for surface in registry["surfaces"]:
        name = surface["name"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in result:
            raise ValueError("Invalid or duplicate surface name")
        result[name] = surface
    return result


def snapshot(root: Path, commit: str, name: str) -> dict[str, Any] | None:
    prefix = f"specs/_vendor/{name}/"
    paths = git(root, "ls-tree", "-r", "--name-only", commit, "--", prefix).decode().splitlines()
    candidates = [p for p in paths if re.fullmatch(re.escape(prefix) + r"snapshot\.[a-z]+", p)]
    if not candidates and not paths:
        return None
    if len(candidates) != 1:
        raise ValueError(f"Expected one captured snapshot for {name}")
    data = read(root, commit, candidates[0])
    meta = json.loads(read(root, commit, prefix + "vendor-meta.json"))
    digest = hashlib.sha256(data).hexdigest()
    if meta.get("surface_id") != name or meta.get("sha256") != digest or meta.get("bytes") != len(data):
        raise ValueError(f"Snapshot metadata does not bind captured bytes: {name}")
    record_path = meta.get("source_raw_record", "")
    if not re.fullmatch(r"archive/raw/" + re.escape(name) + r"/[A-Za-z0-9_-]+\.meta\.json", record_path):
        raise ValueError(f"Invalid capture provenance path: {name}")
    record = json.loads(read(root, commit, record_path))
    if (
        record.get("status") != "FETCH_OK"
        or record.get("surface_id") != name
        or record.get("sha256") != digest
        or record.get("bytes") != len(data)
    ):
        raise ValueError(f"Snapshot lacks matching FETCH_OK provenance: {name}")
    return {"path": candidates[0], "sha256": digest, "bytes": len(data), "data": data, "raw_record": record_path}


def project(name: str, data: bytes) -> dict[str, Any]:
    filename, function = EXTRACTORS[name]
    spec = importlib.util.spec_from_file_location(
        "review_" + name.replace("-", "_"), Path(__file__).with_name(filename)
    )
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load reviewed extractor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="snapshot-review-") as directory:
        path = Path(directory) / "snapshot.md"
        path.write_bytes(data)
        # Extractors report anchor failures and exit 2. Preserve that as an
        # explicit unknown recommendation, not a clean or prose-only verdict.
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            try:
                result = getattr(module, function)(str(path))
            except SystemExit as exc:
                raise ValueError("Extractor could not establish its required anchors") from exc
    result.pop("captured_from", None)
    return result


def differences(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    if json.dumps(before, sort_keys=True, allow_nan=False) == json.dumps(after, sort_keys=True, allow_nan=False):
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(before.keys() | after.keys()):
            pointer = path + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in before:
                value = after[key]
                impact = "review-required"
                if isinstance(value, dict) and type(value.get("required")) is bool:
                    impact = "potential-breaking" if value["required"] else "additive"
                result.append({"path": pointer, "change": "added", "after": value, "impact": impact})
            elif key not in after:
                result.append(
                    {"path": pointer, "change": "removed", "before": before[key], "impact": "potential-breaking"}
                )
            else:
                result.extend(differences(before[key], after[key], pointer))
        return result
    impact = "review-required"
    if path.endswith("/required") and type(before) is bool and type(after) is bool:
        impact = "potential-breaking" if after else "additive"
    elif (
        path.endswith("/enum")
        and isinstance(before, list)
        and isinstance(after, list)
        and all(isinstance(v, str) for v in before + after)
    ):
        if set(before) == set(after):
            return []
        impact = "potential-breaking" if set(before) - set(after) else "additive"
    return [{"path": path, "change": "modified", "before": before, "after": after, "impact": impact}]


def recommendation(changes: list[dict[str, Any]]) -> str:
    if any(c["impact"] == "potential-breaking" for c in changes):
        return "potential-breaking"
    if any(c["impact"] == "review-required" for c in changes):
        return "review-required"
    return "additive" if changes else "unchanged-projection"


def build_report(root: Path, base: str, head: str) -> dict[str, Any]:
    base, head = resolve(root, base), resolve(root, head)
    old_registry, new_registry = surfaces(root, base), surfaces(root, head)
    rows = []
    for name in sorted(old_registry.keys() | new_registry.keys()):
        before, after = snapshot(root, base, name), snapshot(root, head, name)
        if before is None and after is None:
            continue
        if before and after and before["sha256"] == after["sha256"]:
            continue
        row: dict[str, Any] = {
            "surface": name,
            "contract": (new_registry.get(name) or old_registry[name])["contract"],
            "before": {k: v for k, v in (before or {}).items() if k != "data"},
            "after": {k: v for k, v in (after or {}).items() if k != "data"},
            "recommendation": "review-required",
            "projection_changes": [],
        }
        if before is None or after is None:
            row["reason"] = "Capture added or removed; no two-sided semantic comparison is available."
        elif name not in EXTRACTORS:
            row["reason"] = "Byte-only coverage; schema impact cannot be inferred from a byte change."
        else:
            try:
                changes = differences(project(name, before["data"]), project(name, after["data"]))
                row.update(recommendation=recommendation(changes), projection_changes=changes)
                row["reason"] = (
                    "Recommendation covers extracted facts only. Review all unprojected prose before disposition."
                )
            except (ValueError, KeyError, IndexError, TypeError) as exc:
                row["reason"] = (
                    f"Extractor unavailable for this comparison ({type(exc).__name__}); human classification required."
                )
        old_text = (before or {}).get("data", b"").decode("utf-8", errors="replace")
        new_text = (after or {}).get("data", b"").decode("utf-8", errors="replace")
        diff = list(
            difflib.unified_diff(
                old_text.splitlines(), new_text.splitlines(), fromfile=base[:12], tofile=head[:12], n=2
            )
        )
        row["diff_lines"] = len(diff)
        row["diff_excerpt"] = "\n".join(line[:300] for line in diff[:16])[:2200]
        row["diff_excerpt_truncated"] = len(diff) > 16 or any(len(line) > 300 for line in diff[:16])
        rows.append(row)
    return {
        "schema": "snapshot-review/v1",
        "base_commit": base,
        "head_commit": head,
        "human_merge_required": True,
        "surfaces": rows,
    }


def render(report: dict[str, Any], repository: str, run_url: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Invalid GitHub repository")
    if not re.fullmatch(r"https://github\.com/" + re.escape(repository) + r"/actions/runs/[0-9]+", run_url):
        raise ValueError("Invalid source workflow URL")
    compare = f"https://github.com/{repository}/compare/{report['base_commit']}..{report['head_commit']}"
    lines = [
        "Automated snapshot review (`snapshot-review/v1`).",
        "",
        "**Human merge required.** A kernel maintainer reviews every snapshot advance; potential breaking changes also need governance-triple review.",
        "No recommendation edits a schema, changes `$schemaVersion`, authorizes a merge, or clears deterministic drift.",
        "A snapshot may advance separately from a schema only after the reviewer confirms textual or compatible additive impact.",
        "An unchanged projection is not proof of prose-only change: extractors cover only part of each source.",
        "",
        f"[Full commit comparison]({compare}) · [Current watcher run]({run_url})",
        f"Base: `{report['base_commit']}` · promotion: `{report['head_commit']}`.",
        "",
        "The watcher also carries append-only capture/lineage records, currency evidence and its liveness dashboard.",
        "Review the exact commits above; later watcher runs may update this bot branch. Do not push to it by hand.",
    ]
    if not report["surfaces"]:
        lines += [
            "",
            "No captured snapshot bytes differ between these commits; inspect the full diff for bookkeeping or registry changes.",
        ]
    for row in report["surfaces"]:
        lines += ["", f"### {row['surface']}: {row['recommendation']}", "", row["reason"]]
        for label in ("before", "after"):
            value = row[label]
            commit = report["base_commit" if label == "before" else "head_commit"]
            link = f"[snapshot](https://github.com/{repository}/blob/{commit}/{value['path']})" if value else "absent"
            lines.append(f"- {label}: {link}, `{value.get('sha256', 'absent')}` ({value.get('bytes', 0)} bytes)")
        lines += [
            "",
            f"Projection changes: {len(row['projection_changes'])}. Full structured findings are in the run's `snapshot-review` artifact.",
        ]
        excerpt = row["diff_excerpt"]
        fence = "`" * max(3, 1 + max((len(m[0]) for m in re.finditer(r"`+", excerpt)), default=0))
        lines += ["", fence + "diff", excerpt, fence]
        if row["diff_excerpt_truncated"]:
            lines.append(
                f"Excerpt truncated; full diff has {row['diff_lines']} lines. Use the commit-bound comparison above."
            )
    lines += ["", "Refs bead bd_000-projects-218d.", "", "- Jeremy Longshore", "intentsolutions.io", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--run-url", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = build_report(args.repo_root, args.base, args.head)
        body = render(report, args.repository, args.run_url)
        if len(body.encode()) > 60_000:
            raise ValueError("Review body exceeds GitHub budget; do not publish a partial review")
        args.out_dir.mkdir(parents=True, exist_ok=False)
        (args.out_dir / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        (args.out_dir / "pr-body.md").write_text(body)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"snapshot-review: refused ({type(exc).__name__}): {exc}", file=sys.stderr)
        return 2
    print(f"snapshot-review: {len(report['surfaces'])} changed captured surfaces; human review required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
