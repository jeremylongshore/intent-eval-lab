#!/usr/bin/env python3
"""Stale-reconciliation detector — ADVISORY liveness view over the lineage backlog.

Normative spec: 000-docs/090-AT-SPEC-prose-schema-reconciliation-liveness-escalation-2026-06-20.md
(F-LL-005). This is the OPTIONAL, advisory detector from § 5 of that spec — it
makes the ≤ 5-business-day reconciliation SLA *observable* between scheduled
spec-drift runs by reading the lineage outstanding-trigger count directly.

POSTURE (deliberate — see 090-AT-SPEC § 5):
  - READ-ONLY. Reads the DERIVED projection specs/lineage/coverage-map.json
    (054-AT-SPEC) and prints a verdict. Never edits the lineage log, the
    coverage map, or any kernel/schema file.
  - ADVISORY. NOT wired into ci.yml's required "Validate specs and docs" job
    and NOT a branch-protection gate. The SLA's BLOCKING obligation (day > 5)
    lives in the existing reconciliation gate, not here. Wiring a business-day
    timer as a required check would fail CI on a calendar boundary unrelated to
    a PR's diff — the time-coupled footgun the repo's required-check posture
    avoids. Promotion to a gate is a future, separately-governed step.
  - SELF-CONTAINED. Ships an offline deterministic --self-test (the repo-wide
    convention) so it is not dead code under the escape-scan even though it is
    unwired.

It answers, on demand, "what's my standing reconciliation backlog, and is any of
it past SLA?" — run manually: `python3 scripts/reconciliation-liveness.py`.

Per the 090-AT-SPEC § 3 SLA bands (business days outstanding since a divergence's
`since` timestamp; business day = a UTC weekday Mon–Fri):
  OK         <= 3 business days
  ESCALATE   == 4 business days   (day-4 escalation to GC / governance triple)
  RETRO-DUE  >= 5 business days   (day-5 ISEDC Class-2 retrospective is due)

Stdlib only. Offline. Exit 0 = no reconciliation past SLA (or no backlog);
1 = at least one divergence is RETRO-DUE (>= 5 business days); 2 = usage / parse
error. The nonzero exit is INFORMATIONAL for a human runner — this script is not
a CI gate, so the code is not consumed by branch protection.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_COVERAGE = os.path.join(REPO_ROOT, "specs", "lineage", "coverage-map.json")

# 090-AT-SPEC § 3 SLA bands, in business days outstanding.
BAND_ESCALATE = 4  # day-4 escalation
BAND_RETRO_DUE = 5  # day-5 ISEDC Class-2 retrospective due / day > 5 block


def parse_iso(ts: str) -> datetime:
    """Parse a UTC ISO timestamp (YYYY-MM-DDTHH:MM:SSZ) to an aware datetime."""
    cleaned = ts.strip()
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"
    dt = datetime.fromisoformat(cleaned)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def business_days_between(start: datetime, now: datetime) -> int:
    """Count UTC weekdays (Mon–Fri) strictly after `start`'s date through `now`'s date.

    Deterministic, calendar-only (no holiday calendar — 090-AT-SPEC § 3 is
    deliberately conservative). Days are counted on date boundaries: the start
    date itself is day 0; each subsequent weekday increments the count. A
    `now` earlier than `start` yields 0 (clamped — a future `since` is not
    outstanding).
    """
    start_d = start.date()
    now_d = now.date()
    if now_d <= start_d:
        return 0
    count = 0
    cur = start_d
    while cur < now_d:
        cur = cur.fromordinal(cur.toordinal() + 1)
        if cur.weekday() < 5:  # Mon=0 .. Fri=4
            count += 1
    return count


def classify(business_days: int) -> str:
    if business_days >= BAND_RETRO_DUE:
        return "RETRO-DUE"
    if business_days == BAND_ESCALATE:
        return "ESCALATE"
    return "OK"


def assess(coverage: dict, now: datetime) -> dict:
    """Build the advisory report from a parsed coverage-map projection.

    Reads the 054-AT-SPEC projection contract: per surface,
    `convergence_triggers_outstanding` (count) and `divergences_outstanding[]`
    (each carrying a `since` timestamp + `subject` + `convergence_trigger`).
    """
    surfaces = coverage.get("surfaces", {})
    rows = []
    total_outstanding = 0
    retro_due = 0
    for surface_name, surface in sorted(surfaces.items()):
        count = int(surface.get("convergence_triggers_outstanding", 0))
        total_outstanding += count
        for div in surface.get("divergences_outstanding", []):
            since_raw = div.get("since")
            if not since_raw:
                # A divergence with no since-timestamp cannot be SLA-timed;
                # surface it as UNKNOWN rather than silently dropping it.
                rows.append(
                    {
                        "surface": surface_name,
                        "subject": div.get("subject", "?"),
                        "since": None,
                        "business_days": None,
                        "band": "UNKNOWN",
                    }
                )
                continue
            bdays = business_days_between(parse_iso(since_raw), now)
            band = classify(bdays)
            if band == "RETRO-DUE":
                retro_due += 1
            rows.append(
                {
                    "surface": surface_name,
                    "subject": div.get("subject", "?"),
                    "since": since_raw,
                    "business_days": bdays,
                    "band": band,
                }
            )
    return {
        "total_convergence_triggers_outstanding": total_outstanding,
        "retro_due_count": retro_due,
        "rows": rows,
    }


def render(report: dict) -> str:
    lines = [
        "Prose↔schema reconciliation liveness (ADVISORY — 090-AT-SPEC § 5)",
        f"  standing backlog (convergence_triggers_outstanding): {report['total_convergence_triggers_outstanding']}",
        f"  past SLA (>= 5 business days, RETRO-DUE): {report['retro_due_count']}",
    ]
    if not report["rows"]:
        lines.append("  no outstanding divergences — backlog clear.")
        return "\n".join(lines)
    lines.append("  outstanding divergences:")
    for r in report["rows"]:
        bd = "?" if r["business_days"] is None else str(r["business_days"])
        lines.append(f"    [{r['band']:<9}] {r['surface']}/{r['subject']}  since={r['since']}  business_days={bd}")
    return "\n".join(lines)


def cmd_assess(coverage_path: str, now: datetime, as_json: bool) -> int:
    if not os.path.exists(coverage_path):
        print(f"coverage map not found: {coverage_path}", file=sys.stderr)
        return 2
    try:
        with open(coverage_path, encoding="utf-8") as fh:
            coverage = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"failed to read coverage map: {exc}", file=sys.stderr)
        return 2
    report = assess(coverage, now)
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render(report))
    return 1 if report["retro_due_count"] > 0 else 0


def cmd_self_test() -> int:
    """Offline deterministic check — proves the business-day math + SLA banding."""
    failures: list[str] = []

    def check(name: str, got: object, want: object) -> None:
        if got != want:
            failures.append(f"{name}: got {got!r} want {want!r}")

    # Business-day counting (anchored on known weekdays; 2026-06-15 is a Monday).
    mon = parse_iso("2026-06-15T00:00:00Z")  # Monday
    # Mon -> same day = 0 business days outstanding.
    check("same-day", business_days_between(mon, parse_iso("2026-06-15T23:59:59Z")), 0)
    # Mon -> Tue = 1.
    check("mon->tue", business_days_between(mon, parse_iso("2026-06-16T00:00:00Z")), 1)
    # Mon -> Fri = 4 (Tue,Wed,Thu,Fri).
    check("mon->fri", business_days_between(mon, parse_iso("2026-06-19T00:00:00Z")), 4)
    # Mon -> next Mon = 5 (weekend skipped: Tue..Fri + Mon).
    check("mon->nextmon", business_days_between(mon, parse_iso("2026-06-22T00:00:00Z")), 5)
    # Weekend does not advance: Fri -> Sun = 0 business days after Fri.
    fri = parse_iso("2026-06-19T00:00:00Z")
    check("fri->sun", business_days_between(fri, parse_iso("2026-06-21T12:00:00Z")), 0)
    # A future `since` clamps to 0.
    check("future-since", business_days_between(parse_iso("2026-06-22T00:00:00Z"), mon), 0)

    # SLA banding.
    check("band-3", classify(3), "OK")
    check("band-4", classify(4), "ESCALATE")
    check("band-5", classify(5), "RETRO-DUE")
    check("band-6", classify(6), "RETRO-DUE")

    # assess() against a synthetic coverage map mirroring the 054-AT-SPEC shape.
    now = parse_iso("2026-06-22T00:00:00Z")  # Monday, +5 business days from 06-15
    fixture = {
        "surfaces": {
            "agentskills-spec": {
                "convergence_triggers_outstanding": 2,
                "divergences_outstanding": [
                    {"subject": "skill-frontmatter/version", "since": "2026-06-15T00:00:00Z"},
                    {"subject": "skill-frontmatter/author", "since": "2026-06-19T00:00:00Z"},
                ],
            },
            "claude-docs": {
                "convergence_triggers_outstanding": 0,
                "divergences_outstanding": [],
            },
        }
    }
    rep = assess(fixture, now)
    check("total-outstanding", rep["total_convergence_triggers_outstanding"], 2)
    # version (06-15 -> 06-22 = 5 business days) is RETRO-DUE; author (06-19 -> 06-22 = 0) is OK.
    check("retro-due-count", rep["retro_due_count"], 1)
    bands = sorted(r["band"] for r in rep["rows"])
    check("bands", bands, ["OK", "RETRO-DUE"])

    # cmd_assess return code: backlog with a RETRO-DUE row exits 1.
    # (clean backlog exits 0.)
    clean = {"surfaces": {"x": {"convergence_triggers_outstanding": 0, "divergences_outstanding": []}}}
    check("clean-retro-due", assess(clean, now)["retro_due_count"], 0)

    # Missing-since divergence surfaces as UNKNOWN, not dropped.
    nodate = {
        "surfaces": {
            "y": {
                "convergence_triggers_outstanding": 1,
                "divergences_outstanding": [{"subject": "z", "since": None}],
            }
        }
    }
    rep2 = assess(nodate, now)
    check("unknown-band", [r["band"] for r in rep2["rows"]], ["UNKNOWN"])

    if failures:
        print("SELF-TEST FAILED:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("reconciliation-liveness self-test: OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ADVISORY stale-reconciliation detector over the lineage backlog (090-AT-SPEC § 5)."
    )
    parser.add_argument("--self-test", action="store_true", help="offline deterministic check")
    parser.add_argument("--coverage", default=DEFAULT_COVERAGE, help="path to coverage-map.json")
    parser.add_argument("--json", action="store_true", help="emit the report as JSON")
    parser.add_argument("--now", default=None, help="UTC ISO timestamp to evaluate against (default: now)")
    args = parser.parse_args()

    if args.self_test:
        return cmd_self_test()

    now = parse_iso(args.now) if args.now else datetime.now(UTC)
    return cmd_assess(args.coverage, now, args.json)


if __name__ == "__main__":
    sys.exit(main())
