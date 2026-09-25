#!/usr/bin/env python3
"""Fail-closed, changed-lines scrub for public surfaces.

The scanner is intentionally deterministic and secretless. It never contacts a
service, reads a credential, or prints matched content. Git diff modes scan only
added lines, so old public history is not silently re-litigated while new
exposure is blocked. ``--path`` and ``--all`` are available for audits and
fixture-driven checks.

Exit codes:
  0  no findings
  1  a configured detector found a finding
  2  usage, Git, file, or policy configuration error (fail closed)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = REPO_ROOT / "scripts" / "public-surface-policy.json"


class PolicyError(ValueError):
    """The scrub policy is invalid and cannot safely be applied."""


@dataclass(frozen=True)
class Detector:
    detector_id: str
    kind: str
    scope: str
    value: str
    pattern: re.Pattern[str] | None = None


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    detector_id: str


@dataclass(frozen=True)
class Policy:
    public_roots: tuple[str, ...]
    ignored_prefixes: tuple[str, ...]
    detectors: tuple[Detector, ...]


def _normalise_path(path: str) -> str:
    value = path.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def _prefix_matches(path: str, prefix: str) -> bool:
    clean = prefix.rstrip("/")
    return path == clean or path.startswith(f"{clean}/")


def _as_string_list(raw: Any, key: str) -> tuple[str, ...]:
    if not isinstance(raw, list) or not all(isinstance(item, str) and item for item in raw):
        raise PolicyError(f"{key} must be a non-empty string list")
    return tuple(_normalise_path(item) for item in raw)


def load_policy(path: Path = DEFAULT_POLICY) -> Policy:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PolicyError(f"cannot read policy {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise PolicyError("policy root must be an object")

    public_roots = _as_string_list(raw.get("public_roots"), "public_roots")
    ignored_prefixes = _as_string_list(raw.get("ignored_prefixes"), "ignored_prefixes")
    raw_detectors = raw.get("detectors")
    if not isinstance(raw_detectors, list) or not raw_detectors:
        raise PolicyError("detectors must be a non-empty list")

    detectors: list[Detector] = []
    for index, item in enumerate(raw_detectors):
        if not isinstance(item, dict):
            raise PolicyError(f"detector {index} must be an object")
        detector_id = item.get("id")
        kind = item.get("kind")
        scope = item.get("scope")
        if not all(isinstance(value, str) and value for value in (detector_id, kind, scope)):
            raise PolicyError(f"detector {index} requires id, kind, and scope")
        if kind not in {"literal", "regex"}:
            raise PolicyError(f"detector {detector_id}: unsupported kind {kind!r}")
        if scope not in {"public", "all"}:
            raise PolicyError(f"detector {detector_id}: unsupported scope {scope!r}")
        value_key = "value" if kind == "literal" else "pattern"
        value = item.get(value_key)
        if not isinstance(value, str) or not value:
            raise PolicyError(f"detector {detector_id}: {value_key} must be a non-empty string")
        compiled: re.Pattern[str] | None = None
        if kind == "regex":
            try:
                compiled = re.compile(value)
            except re.error as exc:
                raise PolicyError(f"detector {detector_id}: invalid regex: {exc}") from exc
        detectors.append(Detector(detector_id, kind, scope, value, compiled))
    return Policy(public_roots, ignored_prefixes, tuple(detectors))


def _is_ignored(path: str, policy: Policy) -> bool:
    return any(_prefix_matches(path, prefix) for prefix in policy.ignored_prefixes)


def _is_public(path: str, policy: Policy) -> bool:
    return any(_prefix_matches(path, prefix) for prefix in policy.public_roots)


def scan_lines(path: str, lines: list[tuple[int, str]], policy: Policy) -> list[Finding]:
    """Scan ``(line_number, text)`` pairs without retaining matched content."""

    normalised = _normalise_path(path)
    if _is_ignored(normalised, policy):
        return []
    public = _is_public(normalised, policy)
    findings: list[Finding] = []
    for line_number, text in lines:
        for detector in policy.detectors:
            if detector.scope == "public" and not public:
                continue
            matched = (
                detector.value.casefold() in text.casefold()
                if detector.kind == "literal"
                else detector.pattern is not None and detector.pattern.search(text) is not None
            )
            if matched:
                findings.append(Finding(normalised, line_number, detector.detector_id))
    return findings


def _read_text_lines(repo_root: Path, relative_path: str) -> list[tuple[int, str]]:
    path = repo_root / relative_path
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise PolicyError(f"cannot read {relative_path}: {exc}") from exc
    if b"\0" in data:
        return []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PolicyError(f"non-UTF-8 public file {relative_path}: {exc}") from exc
    return list(enumerate(text.splitlines(), start=1))


def scan_paths(repo_root: Path, paths: list[str], policy: Policy) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        relative = _normalise_path(path)
        if relative.startswith("/") or relative == ".." or relative.startswith("../"):
            raise PolicyError(f"path is outside the repository: {path}")
        findings.extend(scan_lines(relative, _read_text_lines(repo_root, relative), policy))
    return findings


def _git_diff(repo_root: Path, args: list[str]) -> str:
    command = ["git", "diff", "--no-ext-diff", "--unified=0", "--diff-filter=ACMR", *args]
    try:
        completed = subprocess.run(command, cwd=repo_root, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PolicyError(f"git diff failed: {exc}") from exc
    return completed.stdout


def changed_lines(repo_root: Path, diff_args: list[str]) -> list[tuple[str, list[tuple[int, str]]]]:
    """Return added lines grouped by destination path from a zero-context diff."""

    result: list[tuple[str, list[tuple[int, str]]]] = []
    current_path: str | None = None
    current_line = 0
    grouped: dict[str, list[tuple[int, str]]] = {}
    for raw_line in _git_diff(repo_root, diff_args).splitlines():
        if raw_line.startswith("+++ b/"):
            current_path = _normalise_path(raw_line[6:])
            current_line = 0
            grouped.setdefault(current_path, [])
            continue
        if raw_line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", raw_line)
            if match:
                current_line = int(match.group(1))
            continue
        if current_path is None:
            continue
        if raw_line.startswith("+"):
            grouped[current_path].append((current_line, raw_line[1:]))
            current_line += 1
        elif not raw_line.startswith("-"):
            current_line += 1
    result.extend(grouped.items())
    return result


def _tracked_paths(repo_root: Path) -> list[str]:
    try:
        completed = subprocess.run(
            ["git", "ls-files", "-z"], cwd=repo_root, check=True, capture_output=True
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PolicyError(f"git ls-files failed: {exc}") from exc
    return [_normalise_path(item) for item in completed.stdout.decode("utf-8").split("\0") if item]


def scan_diff(repo_root: Path, diff_args: list[str], policy: Policy) -> list[Finding]:
    findings: list[Finding] = []
    for path, lines in changed_lines(repo_root, diff_args):
        findings.extend(scan_lines(path, lines, policy))
    return findings


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--staged", action="store_true", help="scan added lines staged in the index")
    source.add_argument("--diff-range", metavar="BASE...HEAD", help="scan added lines in a Git diff range")
    source.add_argument("--all", action="store_true", help="scan every tracked file")
    source.add_argument("--path", action="append", help="scan a repository-relative file (repeatable)")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY, help="policy JSON path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        policy = load_policy(args.policy)
        if args.staged:
            findings = scan_diff(REPO_ROOT, ["--cached"], policy)
        elif args.diff_range:
            findings = scan_diff(REPO_ROOT, [args.diff_range], policy)
        elif args.all:
            findings = scan_paths(REPO_ROOT, _tracked_paths(REPO_ROOT), policy)
        elif args.path:
            findings = scan_paths(REPO_ROOT, args.path, policy)
        else:  # pragma: no cover - argparse's mutually-exclusive group prevents this
            raise PolicyError("a scan source is required")
    except PolicyError as exc:
        print(f"public-surface-scan: configuration or input error: {exc}", file=sys.stderr)
        return 2

    if not findings:
        print("public-surface-scan: PASS (no configured findings in added/public content)")
        return 0
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.detector_id}")
    print(f"public-surface-scan: FAIL ({len(findings)} finding(s)); matched content is intentionally withheld")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
