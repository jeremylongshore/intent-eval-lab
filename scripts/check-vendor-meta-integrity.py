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

    if problems:
        print(f"vendor-meta integrity: {len(problems)} PROBLEM(S):")
        for problem in problems:
            print(f"  - {problem}")
        print(
            "\nFix: re-derive the record from the bytes, never the other way round. "
            "After replacing a vendored file, recompute sha256 + bytes and re-run the extractor's --write."
        )
        return 1

    print(
        f"vendor-meta integrity: OK — {len(captures)} capture(s), {total} vendored file(s); "
        "every sha256 and byte count matches the bytes on disk, and every file is declared."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
