#!/usr/bin/env python3
"""Tier-bridge conformance runner — proves the SPEC.md § 6 verdict-combination algebra by example.

This runner is the executable half of the conformance suite mandated by
`specs/tier-bridge/v0.1.0-draft/SPEC.md` § 10. It:

  1. re-implements the § 6 (R5–R9) verdict-combination algebra and the § 5 fail-fast / § 9
     reachability invariants as a single pure function `combine(t1, t2, t3)`, and
  2. loads every fixture under `fixtures/` (one reachable `(t1, t2, t3)` triple per file) and
     asserts the runner's computed final verdict equals the fixture's declared `expected_final`,
  3. asserts every UNREACHABLE triple declared in `fixtures/unreachable/` is rejected by the
     algebra (raises), never silently combined (SPEC § 6 R9 / conformance README).

A green run is what makes a tier-bridge conformance claim a claim (SPEC § 10; specs/README
"A claim of conformance without a test pass is not a claim").

Authority: the algebra here MUST match SPEC.md § 6 exactly. If the spec changes, this runner and
the fixtures change in lock-step; the spec wins on any disagreement.

Stdlib only. Offline. Deterministic.

Usage:
    python3 run.py            # run the suite, exit 0 on all-pass, 1 on any failure
    python3 run.py --list     # list discovered fixtures + computed verdicts, exit 0
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(HERE, "fixtures")
UNREACHABLE_DIR = os.path.join(FIXTURES_DIR, "unreachable")

# --- Verdict vocabularies (SPEC § 6 R5) -------------------------------------------------------
T1 = {"PASS", "FAIL"}
T2 = {"GREEN", "YELLOW", "RED"}
T3 = {"GREEN", "RED", "SKIPPED"}
FINAL = {"PASS", "FAIL", "VERIFIED"}


class UnreachableTriple(Exception):
    """Raised when `(t1, t2, t3)` is one the spec says a conformant impl MUST NOT produce.

    Per SPEC § 6 R9, the fail-fast rules (§ 5) make `(FAIL, _, GREEN)`, `(FAIL, _, RED)`,
    `(_, RED, GREEN)`, `(_, RED, RED)` unreachable — a behavioral tier never runs after a
    fail-fast skip, so a non-SKIPPED `t3` alongside a fail-fast static verdict is a contradiction,
    not a row to combine.
    """


def combine(t1: str, t2: str, t3: str) -> str:
    """Pure implementation of the SPEC § 6 verdict-combination algebra.

    Returns the final verdict ∈ {PASS, FAIL, VERIFIED}. Raises ValueError for an out-of-vocabulary
    input and UnreachableTriple for a triple the spec forbids a conformant impl from producing.
    """
    if t1 not in T1:
        raise ValueError(f"t1 must be one of {sorted(T1)}, got {t1!r}")
    if t2 not in T2:
        raise ValueError(f"t2 must be one of {sorted(T2)}, got {t2!r}")
    if t3 not in T3:
        raise ValueError(f"t3 must be one of {sorted(T3)}, got {t3!r}")

    # Reachability guard (SPEC § 5 fail-fast + § 6 R9): after a fail-fast static verdict the
    # behavioral tier MUST be SKIPPED. A FAIL t1 (R3) or RED t2 (R2) with a non-SKIPPED t3 is the
    # forbidden set of triples; reject rather than silently combine.
    fail_fast = (t1 == "FAIL") or (t2 == "RED")
    if fail_fast and t3 != "SKIPPED":
        raise UnreachableTriple(
            f"({t1}, {t2}, {t3}) is unreachable: a fail-fast static verdict forces t3=SKIPPED "
            f"(SPEC § 5 R2/R3 + § 6 R9)"
        )

    # R7 — FAIL on any blocking tier failure (checked first; subsumes both fail-fast skips and a
    # behavioral RED on a run where Tier 3 actually executed).
    if t1 == "FAIL" or t2 == "RED" or t3 == "RED":
        return "FAIL"

    # From here: t1 == PASS, t2 ∈ {GREEN, YELLOW}, t3 ∈ {GREEN, SKIPPED}.
    # R6 — VERIFIED iff the behavioral tier actually ran and passed.
    if t3 == "GREEN":
        return "VERIFIED"

    # R8 — PASS otherwise (static-only promotion; t3 SKIPPED, incl. unavailable per § 9 R15/R16).
    return "PASS"


def _load_fixtures(dirpath: str, recurse_skip: str | None = None) -> list[dict]:
    out: list[dict] = []
    for name in sorted(os.listdir(dirpath)):
        full = os.path.join(dirpath, name)
        if recurse_skip and os.path.abspath(full) == os.path.abspath(recurse_skip):
            continue
        if not name.endswith(".json"):
            continue
        with open(full, encoding="utf-8") as fh:
            data = json.load(fh)
        data["_path"] = os.path.relpath(full, HERE)
        out.append(data)
    return out


def _run_reachable(fixtures: list[dict]) -> list[str]:
    failures: list[str] = []
    for fx in fixtures:
        fid = fx.get("fixture_id", "<no id>")
        t = fx["input"]
        expected = fx["expected_final"]
        try:
            got = combine(t["t1"], t["t2"], t["t3"])
        except (ValueError, UnreachableTriple) as exc:
            failures.append(f"{fid} ({fx['_path']}): runner raised on a reachable fixture: {exc}")
            continue
        if got != expected:
            failures.append(
                f"{fid} ({fx['_path']}): ({t['t1']}, {t['t2']}, {t['t3']}) -> "
                f"got {got!r}, expected {expected!r}"
            )
    return failures


def _run_unreachable(fixtures: list[dict]) -> list[str]:
    failures: list[str] = []
    for fx in fixtures:
        fid = fx.get("fixture_id", "<no id>")
        t = fx["input"]
        try:
            got = combine(t["t1"], t["t2"], t["t3"])
        except UnreachableTriple:
            continue  # correct: the algebra rejected a forbidden triple
        failures.append(
            f"{fid} ({fx['_path']}): unreachable triple ({t['t1']}, {t['t2']}, {t['t3']}) was "
            f"NOT rejected — runner combined it to {got!r} (SPEC § 6 R9 says it MUST be rejected)"
        )
    return failures


def main(argv: list[str]) -> int:
    reachable = _load_fixtures(FIXTURES_DIR, recurse_skip=UNREACHABLE_DIR)
    unreachable = _load_fixtures(UNREACHABLE_DIR) if os.path.isdir(UNREACHABLE_DIR) else []

    if "--list" in argv:
        print(f"reachable fixtures: {len(reachable)}")
        for fx in reachable:
            t = fx["input"]
            try:
                got = combine(t["t1"], t["t2"], t["t3"])
            except (ValueError, UnreachableTriple) as exc:
                got = f"<raised: {exc}>"
            print(
                f"  {fx.get('fixture_id', '?'):>10}  "
                f"({t['t1']:>4}, {t['t2']:>6}, {t['t3']:>7}) -> {got}"
            )
        print(f"unreachable fixtures (must be rejected): {len(unreachable)}")
        for fx in unreachable:
            t = fx["input"]
            print(f"  {fx.get('fixture_id', '?'):>10}  ({t['t1']:>4}, {t['t2']:>6}, {t['t3']:>7})")
        return 0

    if not reachable:
        print("FAIL: no reachable fixtures discovered", file=sys.stderr)
        return 1

    failures = _run_reachable(reachable) + _run_unreachable(unreachable)

    total = len(reachable) + len(unreachable)
    if failures:
        print(f"FAIL: {len(failures)} of {total} fixtures did not match the SPEC § 6 algebra:")
        for line in failures:
            print(f"  - {line}")
        return 1

    print(
        f"PASS: {len(reachable)} reachable + {len(unreachable)} unreachable fixtures "
        f"all match SPEC § 6 algebra ({total} total)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
