#!/usr/bin/env python3
"""Drift gate: the kernel's exported TransitionMaps must equal Blueprint B.

Blueprint B (000-docs/012-AT-ARCH-platform-runtime-blueprint.md) is the NORMATIVE
source for the 13-entity runtime state machines per the IEP source-of-truth
hierarchy. The kernel @intentsolutions/core ships those machines as
`<entity>Transitions: TransitionMap<S>` const exports. There was no machine-
checkable artifact proving the two are single-sourced — a developer could edit a
kernel map without touching the Blueprint and ship an out-of-spec runtime that
no static gate catches (Kleppmann finding #5, 000-docs/023-AA-AACR-thinker-panel-
review-2026-05-25.md § 2.1).

This gate closes that hole. It asserts:

    kernel src/entities/*.ts exported TransitionMaps
        == specs/state-machines/transition-table.v1.json `kernel_state_map`

REDS (exit 1) on ANY drift: missing/extra map, missing/extra from-state, or a
mismatched to-state set. The lab artifact is the single source the kernel is
checked against; Blueprint B is the human-normative source the artifact is
extracted from (extraction note in the JSON).

ZERO RUNTIME DEPS. Stdlib only. Offline-by-default: compares against a vendored
kernel snapshot (specs/state-machines/kernel-transition-snapshot.v1.json) that is
committed to the lab and refreshable from the live kernel via --refresh. This
mirrors the specs/_vendor/ + specs/snapshots/.sha hermetic-CI pattern already in
this repo.

Modes
  (default)            compare kernel snapshot vs artifact kernel_state_map; REDS on drift
  --refresh            re-fetch the kernel maps (local sibling checkout first,
                       then GitHub raw URL) and rewrite the snapshot, then compare
  --rebuild-kernel-view  recompute the artifact's kernel_state_map (the event-erased
                       from->[to] projection) from its `entities[].transitions`,
                       then write it back. Use after editing the 4-tuples.
  --source local|raw   force the --refresh source (default: try local then raw)

Exit codes: 0 = single-sourced (no drift); 1 = drift; 2 = usage/parse/fetch error.

Usage:
  python3 scripts/check-statemachine-drift.py
  python3 scripts/check-statemachine-drift.py --refresh
  python3 scripts/check-statemachine-drift.py --rebuild-kernel-view
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACT = os.path.join(REPO_ROOT, "specs", "state-machines", "transition-table.v1.json")
SNAPSHOT = os.path.join(REPO_ROOT, "specs", "state-machines", "kernel-transition-snapshot.v1.json")

# The kernel const exports that constitute the canonical 13-entity machines.
# (name -> source file). Kept explicit so an accidentally-renamed or dropped
# kernel map surfaces as drift rather than being silently skipped.
KERNEL_MAPS: dict[str, str] = {
    "evalSpecTransitions": "EvalSpec.ts",
    "evalRunTransitions": "EvalRun.ts",
    "matcherMapTransitions": "MatcherMap.ts",
    "evidenceBundleTransitions": "EvidenceBundle.ts",
    "judgeDecisionTransitions": "JudgeDecision.ts",
    "runtimeReceiptTransitions": "RuntimeReceipt.ts",
    "regressionPackTransitions": "RegressionPack.ts",
    "rolloutGateTransitions": "RolloutGate.ts",
    "skillSnapshotTransitions": "SkillSnapshot.ts",
    "sessionTraceTransitions": "SessionTrace.ts",
    "toolInvocationTransitions": "ToolInvocation.ts",
    "costRecordTransitions": "CostRecord.ts",
    "failureTaxonomyTransitions": "FailureTaxonomy.ts",
}

# Where to find the kernel src at --refresh time. The sibling-checkout location
# is tried first; KERNEL_SRC_DIR overrides (e.g. a worktree or the canonical
# intent-eval-platform/intent-eval-core path). CI uses --source raw (no checkout).
_LOCAL_CANDIDATES = [
    os.environ.get("KERNEL_SRC_DIR", ""),
    os.path.normpath(os.path.join(REPO_ROOT, "..", "intent-eval-core", "src", "entities")),
    os.path.normpath(
        os.path.join(REPO_ROOT, "..", "intent-eval-platform", "intent-eval-core", "src", "entities")
    ),
]
RAW_BASE = "https://raw.githubusercontent.com/jeremylongshore/intent-eval-core/main/src/entities"


def _local_kernel_dir() -> str | None:
    """First existing local kernel src/entities dir, or None."""
    for cand in _LOCAL_CANDIDATES:
        if cand and os.path.isdir(cand):
            return cand
    return None

# Matches:  export const <name>: TransitionMap<...> = { ... } as const;
# (anchored to the const name; non-greedy body up to the closing `}` + `as const`)
_MAP_RE_TMPL = (
    r"export\s+const\s+{name}\s*:\s*TransitionMap<[^>]+>\s*=\s*\{{(?P<body>.*?)\}}\s*as\s+const"
)
# Within a body, one row:  <state>: [ 'a', 'b' ],   (value may span lines)
_ROW_RE = re.compile(r"(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*\[(?P<vals>[^\]]*)\]")
_STR_RE = re.compile(r"['\"]([^'\"]+)['\"]")


def _die(msg: str, code: int = 2) -> None:
    print(f"::error::{msg}", file=sys.stderr)
    sys.exit(code)


def _load_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        _die(f"missing file: {path}")
    except (json.JSONDecodeError, OSError) as exc:
        _die(f"cannot parse {path}: {exc}")
    return {}  # unreachable


def parse_kernel_ts(text: str, const_name: str) -> dict[str, list[str]]:
    """Extract one `<const_name>` TransitionMap from kernel TS source text.

    The kernel maps are flat `as const` literals — `state: [ 'to', ... ]` rows.
    A strict regex is sufficient and keeps this gate zero-dep. Comments after a
    value (e.g. `// reversible`) are tolerated because we only read inside [].
    """
    m = re.search(_MAP_RE_TMPL.format(name=re.escape(const_name)), text, re.DOTALL)
    if not m:
        raise ValueError(f"could not find `{const_name}` TransitionMap in kernel source")
    body = m.group("body")
    out: dict[str, list[str]] = {}
    for row in _ROW_RE.finditer(body):
        key = row.group("key")
        vals = [s.group(1) for s in _STR_RE.finditer(row.group("vals"))]
        out[key] = vals
    if not out:
        raise ValueError(f"`{const_name}` parsed to an empty map (regex drift?)")
    return out


def _fetch_kernel_source(filename: str, source: str) -> str:
    """Return the TS source for one kernel entity file. source: local|raw|auto."""
    if source in ("local", "auto"):
        local_dir = _local_kernel_dir()
        if local_dir:
            local = os.path.join(local_dir, filename)
            if os.path.isfile(local):
                with open(local, encoding="utf-8") as fh:
                    return fh.read()
            if source == "local":
                _die(f"--source local: kernel file not found at {local}")
        elif source == "local":
            _die(
                "--source local: no kernel src/entities dir found "
                f"(set KERNEL_SRC_DIR; tried {[c for c in _LOCAL_CANDIDATES if c]})"
            )
    # raw / auto-fallback
    url = f"{RAW_BASE}/{filename}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "iel-statemachine-drift-gate"})
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (https only, fixed host)
            return resp.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        _die(f"cannot fetch kernel source {url}: {exc}")
    return ""  # unreachable


def refresh_snapshot(source: str) -> dict[str, dict[str, list[str]]]:
    """Re-read every kernel map from `source` and write the vendored snapshot."""
    maps: dict[str, dict[str, list[str]]] = {}
    for const_name, filename in KERNEL_MAPS.items():
        text = _fetch_kernel_source(filename, source)
        try:
            maps[const_name] = parse_kernel_ts(text, const_name)
        except ValueError as exc:
            _die(f"{filename}: {exc}")
    snapshot = {
        "_note": (
            "VENDORED kernel transition maps. Generated by "
            "scripts/check-statemachine-drift.py --refresh from "
            "@intentsolutions/core src/entities/*.ts. Do NOT hand-edit; "
            "re-run --refresh. Keeps the drift gate hermetic + offline "
            "(specs/_vendor pattern)."
        ),
        "kernel_package": "@intentsolutions/core",
        "kernel_ref": "main",
        "maps": maps,
    }
    with open(SNAPSHOT, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2, sort_keys=False)
        fh.write("\n")
    print(f"refreshed kernel snapshot ({source}): {SNAPSHOT}")
    return maps


def rebuild_kernel_view() -> None:
    """Recompute artifact.kernel_state_map from artifact.entities[].transitions."""
    art = _load_json(ARTIFACT)
    view: dict[str, dict[str, list[str]]] = {}
    for ent in art.get("entities", []):
        const = ent["kernel_const"]
        adj: dict[str, list[str]] = {}
        for tr in ent.get("transitions", []):
            frm = tr.get("from", "")
            to = tr.get("to", "")
            adj.setdefault(frm, [])
            if to and to not in adj[frm]:
                adj[frm].append(to)
        # Ensure every reachable to-state exists as a (possibly terminal) key.
        for tos in list(adj.values()):
            for st in tos:
                adj.setdefault(st, [])
        # Stable, sorted to-lists for deterministic diffing.
        view[const] = {k: sorted(adj[k]) for k in adj}
    # preserve the _comment key if present
    existing = art.get("kernel_state_map", {})
    if "_comment" in existing:
        view = {"_comment": existing["_comment"], **view}
    art["kernel_state_map"] = view
    with open(ARTIFACT, "w", encoding="utf-8") as fh:
        json.dump(art, fh, indent=2, sort_keys=False)
        fh.write("\n")
    print(f"rebuilt kernel_state_map in {ARTIFACT}")


def _norm(m: dict) -> dict[str, list[str]]:
    """Normalize a from->[to] map: drop _comment, sort to-lists."""
    return {k: sorted(v) for k, v in m.items() if not k.startswith("_")}


def compare(kernel_maps: dict[str, dict[str, list[str]]]) -> int:
    art = _load_json(ARTIFACT)
    expected_all = art.get("kernel_state_map", {})
    if not isinstance(expected_all, dict) or len([k for k in expected_all if not k.startswith("_")]) == 0:
        _die("artifact kernel_state_map missing/empty — run --rebuild-kernel-view")

    expected_names = {k for k in expected_all if not k.startswith("_")}
    actual_names = set(kernel_maps)

    problems: list[str] = []

    missing = sorted(expected_names - actual_names)
    extra = sorted(actual_names - expected_names)
    for name in missing:
        problems.append(
            f"map `{name}` is in the Blueprint-B artifact but MISSING from the kernel "
            f"(kernel dropped/renamed a state machine without updating Blueprint B + the artifact)"
        )
    for name in extra:
        problems.append(
            f"map `{name}` is exported by the kernel but ABSENT from the Blueprint-B artifact "
            f"(kernel added a state machine without updating Blueprint B + the artifact)"
        )

    for name in sorted(expected_names & actual_names):
        exp = _norm(expected_all[name])
        act = _norm(kernel_maps[name])

        exp_states = set(exp)
        act_states = set(act)
        for st in sorted(exp_states - act_states):
            problems.append(f"{name}: from-state `{st}` in artifact but not in kernel")
        for st in sorted(act_states - exp_states):
            problems.append(f"{name}: from-state `{st}` in kernel but not in artifact")
        for st in sorted(exp_states & act_states):
            if exp[st] != act[st]:
                problems.append(
                    f"{name}: from-state `{st}` to-states drift — "
                    f"artifact={exp[st]} kernel={act[st]}"
                )

    if problems:
        print("::group::State-machine drift detected (kernel != Blueprint-B artifact)")
        for p in problems:
            print(f"::error::{p}")
        print("::endgroup::")
        print(
            "\n::error::State-machine drift: the kernel @intentsolutions/core transition "
            "maps no longer match specs/state-machines/transition-table.v1.json "
            "(extracted from Blueprint B § 3.1 + § 2). Single-source the change: edit "
            "Blueprint B, regenerate the artifact (--rebuild-kernel-view), and "
            "--refresh the kernel snapshot in the SAME PR. See "
            "000-docs/076-AT-SPEC-state-machine-single-source-and-drift-gate-2026-06-13.md.",
            file=sys.stderr,
        )
        return 1

    n = len(expected_names)
    print(f"OK: all {n} kernel transition maps are single-sourced with Blueprint B "
          f"(specs/state-machines/transition-table.v1.json).")
    return 0


def main(argv: list[str]) -> int:
    args = set(argv[1:])
    source = "auto"
    if "--source" in argv:
        i = argv.index("--source")
        if i + 1 < len(argv):
            source = argv[i + 1]
        if source not in ("local", "raw", "auto"):
            _die("--source must be local|raw|auto")

    if "--rebuild-kernel-view" in args:
        rebuild_kernel_view()
        return 0

    if "--refresh" in args:
        kernel_maps = refresh_snapshot(source)
        return compare(kernel_maps)

    # default: compare against the vendored snapshot (offline, hermetic)
    snap = _load_json(SNAPSHOT)
    kernel_maps = snap.get("maps")
    if not isinstance(kernel_maps, dict) or not kernel_maps:
        _die(f"snapshot {SNAPSHOT} has no `maps` — run --refresh first")
    return compare(kernel_maps)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
