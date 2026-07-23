#!/usr/bin/env python3
"""Run every field-level projection checker against the CAPTURED upstream pages.

THE GAP THIS CLOSES
-------------------
Five deep-capture extractors have run green on every PR since 2026-06-12 under
steps titled "…projection freshness". They are not freshness checks. Each
re-extracts its projection from `specs/_vendor/upstream/<contract>/` — a
hand-vendored tree `fetch-capture.py` cannot write (`upstream` is not a surface
id) — and compares it against the committed projection derived from those same
bytes. Both operands are frozen, so the result is green by construction no matter
what upstream does. The extractors' own comments say the design intended
otherwise: "CI never refetches: the capture is a one-time build-time fetch;
ongoing freshness is the watcher's job." The watcher never got them wired.

This is that wiring. It reads the coverage map in
`specs/upstream-surface-registry.v1.json` and, for each surface declaring
`semantic_coverage.status == "field-level"`, runs the declared checker with
`--surface <name>` so the parsed reference doc is repointed at
`specs/_vendor/<surface>/snapshot<ext>` — the tier-2 tree the capture stage
advances, and only ever on a FETCH_OK classification.

REGISTRY-DRIVEN ENFORCEMENT
---------------------------
`semantic_coverage.enforcement` decides whether a drifted surface fails this
driver (`failing`) or is merely reported (`report-only`). That is not laxity: a
surface whose findings are still awaiting a human disposition would otherwise
make this lane permanently red, and we have direct evidence that permanently-red
lanes get ignored — byte-drift alerting was gated off for exactly that reason.
Flipping a surface to `failing` is a one-line registry edit made once its
findings are dispositioned, which keeps the flip visible in review.

An INOPERABLE checker (exit 2) is red whenever its surface is enforced, and is
always shouted about. A gate that could not run is not a gate that passed —
collapsing that into "clean" is the whole failure class this file exists to end.

Byte-hash-only surfaces are printed too, with their stated reason. A coverage
report that silently omits what it does not cover is how "no extractor" gets
mistaken for "not covered by design".

Stdlib only. Offline (the checkers take paths, never URLs).

Exit 0 = every enforced surface clean; 1 = an enforced surface drifted;
2 = an enforced surface could not be checked, or the registry is unusable.

Usage:
  projection-freshness.py                 # run the coverage map, honour enforcement
  projection-freshness.py --strict        # treat report-only surfaces as failing too
  projection-freshness.py --surface NAME  # run one surface only
  projection-freshness.py --list          # print the coverage map, run nothing
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import captured_source  # noqa: E402

REPO_ROOT = captured_source.REPO_ROOT

CLEAN, DRIFT, INOPERABLE = 0, 1, 2

_VERDICT = {CLEAN: "CLEAN", DRIFT: "DRIFT", INOPERABLE: "INOPERABLE"}


def field_level_surfaces(registry: dict) -> list[dict]:
    return [
        s
        for s in registry.get("surfaces", [])
        if (s.get("semantic_coverage") or {}).get("status") == "field-level"
    ]


def byte_only_surfaces(registry: dict) -> list[dict]:
    return [
        s
        for s in registry.get("surfaces", [])
        if (s.get("semantic_coverage") or {}).get("status") == "byte-hash-only"
    ]


def run_checker(surface: dict) -> tuple[int, str]:
    """Run one surface's declared checker. Returns (exit code, captured output)."""
    cov = surface["semantic_coverage"]
    argv = [sys.executable, *cov["checker"], "--surface", surface["name"]]
    try:
        proc = subprocess.run(argv, cwd=REPO_ROOT, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.SubprocessError) as exc:
        return INOPERABLE, f"could not execute {' '.join(cov['checker'])}: {exc}"
    output = (proc.stdout + proc.stderr).rstrip()
    # Anything outside {0,1,2} is an unknown failure mode — treat it as inoperable
    # rather than guessing, so it cannot be silently read as clean.
    code = proc.returncode if proc.returncode in _VERDICT else INOPERABLE
    return code, output


def cmd_list(registry: dict) -> int:
    print("Semantic coverage map (specs/upstream-surface-registry.v1.json):\n")
    for surface in field_level_surfaces(registry):
        cov = surface["semantic_coverage"]
        print(f"  field-level     {surface['name']:26} [{cov['enforcement']:11}] {' '.join(cov['checker'])}")
    for surface in byte_only_surfaces(registry):
        print(f"  byte-hash-only  {surface['name']:26} {surface['semantic_coverage']['reason']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the field-level projection checkers against captured pages.")
    parser.add_argument("--strict", action="store_true", help="treat report-only surfaces as failing")
    parser.add_argument("--surface", default=None, help="run a single surface instead of the whole map")
    parser.add_argument("--list", action="store_true", help="print the coverage map and exit")
    args = parser.parse_args()

    try:
        registry = captured_source.load_registry()
    except captured_source.InoperableError as exc:
        print(f"projection-freshness: INOPERABLE — {exc}", file=sys.stderr)
        return INOPERABLE

    if args.list:
        return cmd_list(registry)

    surfaces = field_level_surfaces(registry)

    # An empty or shrunken map must be INOPERABLE, never a clean board.
    #
    # Without this the loop body simply never runs, `worst` stays CLEAN, and the
    # driver prints "CLEAN (exit 0) over 0 field-level surface(s)" — flatly
    # contradicting this module's own rule that a gate which could not run is not
    # a gate that passed. "The map got smaller" and "the map is clean" were the
    # same green, which is the failure this whole file exists to end, one level up.
    floor = (registry.get("semantic_coverage_floor") or {}).get("field_level")
    if not surfaces:
        print(
            "projection-freshness: INOPERABLE — the registry declares ZERO field-level surfaces, so this "
            "gate compared nothing. An empty map is not a clean map.",
            file=sys.stderr,
        )
        return INOPERABLE
    if isinstance(floor, int) and not isinstance(floor, bool) and len(surfaces) < floor:
        print(
            f"projection-freshness: INOPERABLE — {len(surfaces)} field-level surface(s) is below the "
            f"registry's declared floor of {floor}. Semantic coverage shrank without the floor being "
            "lowered in the same change, so this run checked less than it is supposed to.",
            file=sys.stderr,
        )
        return INOPERABLE

    if args.surface:
        surfaces = [s for s in surfaces if s["name"] == args.surface]
        if not surfaces:
            print(
                f"projection-freshness: INOPERABLE — '{args.surface}' is not a field-level surface. "
                "Run --list to see the coverage map.",
                file=sys.stderr,
            )
            return INOPERABLE

    worst = CLEAN
    summary: list[str] = []

    for surface in surfaces:
        name = surface["name"]
        enforcement = surface["semantic_coverage"]["enforcement"]
        enforced = args.strict or enforcement == "failing"
        code, output = run_checker(surface)

        print(f"\n─── {name} ({surface['contract']}) [{enforcement}{'; --strict' if args.strict else ''}]")
        print(output or "(no output)")
        if code == INOPERABLE:
            # Always shout: an inoperable checker is a blind spot whether or not
            # this particular surface is currently enforced.
            print(f"::error::projection-freshness: {name} checker could not run (exit 2) — this surface was NOT checked.")

        summary.append(f"  {_VERDICT[code]:11} {name:26} {'enforced' if enforced else 'report-only'}")
        if enforced:
            worst = max(worst, code)

    print("\n─── Summary")
    for line in summary:
        print(line)
    for surface in byte_only_surfaces(registry):
        print(f"  UNCOVERED   {surface['name']:26} byte-hash-only: {surface['semantic_coverage']['reason'][:96]}")

    print(f"\nprojection-freshness: {_VERDICT[worst]} (exit {worst}) over {len(surfaces)} field-level surface(s).")
    if worst == DRIFT:
        print(
            "A human reconciles: read the captured page, decide per finding whether it is a real "
            "upstream spec change or a stale extractor anchor, then fold it into the kernel one "
            "surface per reviewable PR. Never bulk-refresh."
        )
    return worst


if __name__ == "__main__":
    sys.exit(main())
