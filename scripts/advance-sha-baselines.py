#!/usr/bin/env python3
"""Advance the byte-hash baselines (specs/snapshots/.sha/) from a drift report.

spec-drift-check.sh compares each source's fetched hash with its committed
baseline in specs/snapshots/.sha/<source>.sha and reports `drift` when they
differ. Until 2026-10 nothing in the watcher ever wrote those files: the
promotion PR advanced the captured snapshots but not these hashes, so every
source that had changed since the baselines were seeded (2026-06-11) reported
`drift` on every run, and watcher-liveness's baseline_stale_streak could never
reset.

The watcher now runs this on the promotion branch before its archive commit.
It writes the hash the drift check actually OBSERVED (the report's `current`
field, never a re-fetch) for each `drift` row, so the baseline on main moves
only when a human merges the promotion PR. A row with any other status is left
alone: `fetch_error` observed nothing, and `ok` already matches.

Exit 0 = wrote zero or more baselines; exit 2 = unreadable or malformed report.
Stdlib only; no network.

Usage:
  advance-sha-baselines.py --report DRIFT.json [--sha-dir DIR]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SHA_DIR = os.path.join(REPO_ROOT, "specs", "snapshots", ".sha")
_HASH = re.compile(r"^[0-9a-f]{64}$")
_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def advance(report_path: str, sha_dir: str) -> list[str]:
    """Write observed hashes for drifted sources; return the names advanced."""
    with open(report_path, encoding="utf-8") as fh:
        report = json.load(fh)
    rows = report.get("sources")
    if not isinstance(rows, list):
        raise ValueError("report has no 'sources' list")
    advanced: list[str] = []
    for row in rows:
        if not isinstance(row, dict) or row.get("status") != "drift":
            continue
        name, current = row.get("source"), row.get("current")
        if not (isinstance(name, str) and _NAME.match(name)):
            raise ValueError(f"drift row has an invalid source name: {name!r}")
        if not (isinstance(current, str) and _HASH.match(current)):
            raise ValueError(f"drift row {name!r} has no 64-hex 'current' hash")
        os.makedirs(sha_dir, exist_ok=True)
        with open(os.path.join(sha_dir, f"{name}.sha"), "w", encoding="utf-8") as fh:
            fh.write(current + "\n")
        advanced.append(name)
    return advanced


def main() -> int:
    parser = argparse.ArgumentParser(description="Advance .sha baselines from a drift report.")
    parser.add_argument("--report", required=True, help="drift JSON written by spec-drift-check.sh --both")
    parser.add_argument("--sha-dir", default=DEFAULT_SHA_DIR, help="baseline directory")
    args = parser.parse_args()
    try:
        advanced = advance(args.report, args.sha_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"advance-sha-baselines: cannot advance — {exc}", file=sys.stderr)
        return 2
    if advanced:
        print(f"advance-sha-baselines: advanced {len(advanced)} baseline(s): {', '.join(sorted(advanced))}")
    else:
        print("advance-sha-baselines: no drifted sources; baselines unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
