#!/usr/bin/env python3
"""Verify every vendor-meta.json records the bytes actually on disk.

WHY THIS EXISTS
---------------
`vendor-meta.json` is the provenance record for a deep capture: per file, the
source URL, the upstream commit where applicable, and the sha256 + byte count of
the exact bytes vendored. Every downstream argument about what upstream said, and
every re-vendor decision, rests on that record being true.

Nothing checked it. Each extractor's `--check` proves the projection is a faithful
derivation of the FILES, and `--self-test` proves the anchors parse — neither reads
`sha256` or `bytes` at all. So a hand re-vendor that copied a new page in but
recorded the wrong hash (or forgot to update it) passed every gate in the repo
while the provenance quietly described a file that no longer existed.

That is not a hypothetical shape: three reference docs were re-vendored BY HAND
during the freshness work, each one editing sha256 and bytes in a text editor.
A silent provenance lie is worse than a stale capture, because the stale capture
is at least honestly labelled.

WHAT IT CHECKS, for every specs/_vendor/upstream/<contract>/vendor-meta.json:

  1. every declared file exists;
  2. its sha256 matches the bytes on disk;
  3. its `bytes` matches the real size;
  4. every file in the directory is DECLARED (an undeclared file is an
     unprovenanced input the extractor could silently start parsing);
  5. the required top-level keys are present.

Stdlib only. Offline. Read-only.

Exit 0 = every capture's provenance is true; 1 = a mismatch; 2 = usage/parse error.

Usage:
  check-vendor-meta-integrity.py [--vendor-root DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_VENDOR_ROOT = os.path.join(REPO_ROOT, "specs", "_vendor", "upstream")

# Files that live beside a capture but are documentation ABOUT it, not inputs to it.
NOT_CAPTURE_INPUTS = {"vendor-meta.json", "projection.json", "projection.v1.json", "PROVENANCE.md"}

REQUIRED_META_KEYS = ("contract", "spec_version", "files")

REGISTRY = os.path.join(REPO_ROOT, "specs", "upstream-surface-registry.v1.json")

# Roles that carry SPEC AUTHORITY — a page or schema the extractor treats as
# normative. Every one of these must correspond to a registered, monitored
# surface, because an unregistered spec input is a document we parse and depend
# on but never re-fetch, never diff, and never notice changing.
#
# This is not hypothetical: claude-code-mcp.md is vendored with role
# claude-code-doc and parsed by extract-mcp-projection.py, yet no surface in the
# registry points at code.claude.com/docs/en/mcp.md. It has been an
# unmonitored normative input the whole time.
#
# `sample-*` roles are deliberately exempt. Samples are commit-pinned
# real-world artifacts that CORROBORATE the doc; they are supposed to be frozen,
# and monitoring them for drift would be meaningless.
_SPEC_BEARING_ROLES = {"reference-doc", "supporting-doc", "machine-schema", "claude-code-doc"}


def _registered_surfaces() -> set[str] | None:
    """Names of every monitored surface, or None if the registry is unreadable.

    None (rather than an empty set) so a missing registry degrades to skipping
    this check instead of declaring every vendored input unregistered.
    """
    try:
        with open(REGISTRY, encoding="utf-8") as fh:
            reg = json.load(fh)
    except (OSError, ValueError):
        return None
    names = {s["name"] for s in reg.get("surfaces", []) if s.get("monitored") and s.get("name")}
    return names or None


def check_registered_surfaces(capture_dir: str, advisories: list[str], registered: set[str]) -> None:
    """Every spec-bearing vendored input must name a monitored surface.

    Matched on the vendor-meta `surface` field rather than by comparing URLs.
    The vendored record already declares which surface each file came from, so
    that declaration is the link to verify; re-deriving it from URL strings
    would introduce a second, weaker matcher that disagrees with the first the
    moment a URL is written two ways.
    """
    name = os.path.basename(capture_dir)
    try:
        with open(os.path.join(capture_dir, "vendor-meta.json"), encoding="utf-8") as fh:
            meta = json.load(fh)
    except (OSError, ValueError):
        return  # already reported by check_capture
    for entry in meta.get("files", []):
        role = entry.get("role")
        if role not in _SPEC_BEARING_ROLES:
            continue
        surface = entry.get("surface")
        origin = entry.get("source_url") or entry.get("source_url_canonical") or "(no source_url recorded)"
        if not surface:
            advisories.append(
                f"{name}/{entry.get('file')}: parsed as '{role}' from {origin}, but declares NO surface. "
                f"An extractor treats this document as normative while nothing re-fetches it, diffs it, or "
                f"notices it change. Register it in specs/upstream-surface-registry.v1.json (and the watcher "
                f"SOURCES) and set `surface` here — or change the role if it is corroborating sample data."
            )
        elif surface not in registered:
            advisories.append(
                f"{name}/{entry.get('file')}: declares surface '{surface}', which is not a monitored surface "
                f"in the registry. Either the surface was renamed or removed, or this input is unmonitored."
            )


def _sha256(path: str) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with open(path, "rb") as fh:
        while chunk := fh.read(1 << 20):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def check_capture(capture_dir: str, problems: list[str]) -> int:
    """Verify one capture directory. Returns the number of files checked."""
    name = os.path.basename(capture_dir)
    meta_path = os.path.join(capture_dir, "vendor-meta.json")
    try:
        with open(meta_path, encoding="utf-8") as fh:
            meta = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        problems.append(f"{name}: cannot read vendor-meta.json: {exc}")
        return 0

    for key in REQUIRED_META_KEYS:
        if key not in meta:
            problems.append(f"{name}: vendor-meta.json is missing required key '{key}'")

    declared: set[str] = set()
    checked = 0
    for entry in meta.get("files", []):
        filename = entry.get("file")
        if not filename:
            problems.append(f"{name}: a files[] entry has no 'file' key")
            continue
        declared.add(filename)
        path = os.path.join(capture_dir, filename)
        if not os.path.isfile(path):
            problems.append(f"{name}/{filename}: declared in vendor-meta.json but MISSING on disk")
            continue

        actual_sha, actual_bytes = _sha256(path)
        checked += 1
        recorded_sha = entry.get("sha256")
        if recorded_sha and recorded_sha != actual_sha:
            problems.append(
                f"{name}/{filename}: sha256 MISMATCH — vendor-meta records {recorded_sha[:16]}…, "
                f"file is {actual_sha[:16]}…. The provenance record describes bytes that are not there."
            )
        elif not recorded_sha:
            problems.append(f"{name}/{filename}: no sha256 recorded — the capture has no verifiable provenance")
        recorded_bytes = entry.get("bytes")
        if isinstance(recorded_bytes, int) and recorded_bytes != actual_bytes:
            problems.append(
                f"{name}/{filename}: bytes MISMATCH — vendor-meta records {recorded_bytes}, file is {actual_bytes}"
            )

    # An UNDECLARED file in a capture dir is an input with no provenance at all.
    # The extractors select inputs by vendor-meta `role`, so such a file is inert
    # today — and one vendor-meta edit away from being parsed as authority.
    on_disk = {
        f
        for f in os.listdir(capture_dir)
        if os.path.isfile(os.path.join(capture_dir, f)) and f not in NOT_CAPTURE_INPUTS
    }
    for orphan in sorted(on_disk - declared):
        problems.append(
            f"{name}/{orphan}: present in the capture directory but NOT declared in vendor-meta.json — "
            "an input with no provenance record"
        )
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify vendored capture provenance against the bytes on disk.")
    parser.add_argument("--vendor-root", default=DEFAULT_VENDOR_ROOT, help="root holding <contract>/ capture dirs")
    parser.add_argument(
        "--enforce-surfaces",
        action="store_true",
        help="fail when a spec-bearing vendored input is not a registered surface (advisory by default)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.vendor_root):
        print(f"ERROR: vendor root not found: {args.vendor_root}", file=sys.stderr)
        return 2

    captures = sorted(
        os.path.join(args.vendor_root, d)
        for d in os.listdir(args.vendor_root)
        if os.path.isfile(os.path.join(args.vendor_root, d, "vendor-meta.json"))
    )
    if not captures:
        # An empty sweep reporting success is the same failure class this repo
        # keeps finding: a gate that checked nothing must not look like a pass.
        print(f"ERROR: no captures found under {args.vendor_root} — this gate verified NOTHING.", file=sys.stderr)
        return 2

    problems: list[str] = []
    total = sum(check_capture(c, problems) for c in captures)

    # Kept SEPARATE from `problems` on purpose. Provenance mismatches are
    # integrity failures and fail the build. "This normative input is not a
    # registered surface" is a real finding but a PRE-EXISTING one — two inputs
    # are unregistered today — and turning a new check into a merge-blocking
    # error in the change that introduces it breaks CI for everyone and teaches
    # people to route around the gate. It reports loudly and exits 0 until
    # --enforce-surfaces is passed, which is how it will be turned on once the
    # two are registered.
    advisories: list[str] = []
    registered = _registered_surfaces()
    if registered is None:
        print("WARNING: surface registry unreadable — skipping the registered-surface check.", file=sys.stderr)
    else:
        for capture in captures:
            check_registered_surfaces(capture, advisories, registered)

    if advisories:
        print(f"vendor-meta integrity: {len(advisories)} UNREGISTERED SPEC INPUT(S) [advisory]:")
        for advisory in advisories:
            print(f"  ! {advisory}")
        print()

    if problems:
        print(f"vendor-meta integrity: {len(problems)} PROBLEM(S):")
        for problem in problems:
            print(f"  - {problem}")
        print(
            "\nFix: re-derive the record from the bytes, never the other way round. "
            "After replacing a vendored file, recompute sha256 + bytes and re-run the extractor's --write."
        )
        return 1

    if advisories and args.enforce_surfaces:
        print("Failing because --enforce-surfaces was requested.")
        return 1

    print(
        f"vendor-meta integrity: OK — {len(captures)} capture(s), {total} vendored file(s); "
        "every sha256 and byte count matches the bytes on disk, and every file is declared."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
