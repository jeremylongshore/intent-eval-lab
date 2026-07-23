#!/usr/bin/env python3
"""Watcher liveness — so the spec-drift watcher cannot fail silent-green (Gregg).

The byte-hash watcher separates "drift" from "fetch_error" and, by design, does
NOT fail the run on fetch errors alone (upstream may be briefly unavailable).
Three guards close silent-green modes:

  1. fetch_error_streak — a persisted per-surface consecutive-error counter. A
     single transient error is tolerated; >= THRESHOLD (default 3) consecutive
     errors FAILS the run loud (the surface is effectively unmonitored).

  2. baseline_stale_streak — consecutive successful captures where the source
     is in ``drift`` status (byte hash moved) without a baseline advance
     (``seeded`` / ``refreshed`` / ``ok``). Byte-hash on a *single* run stays
     non-alerting (c875cf1); *persistence* of that drift is the signal to
     fire (IEP #15 / 1jn0.1.5). Resets when the baseline advances or the
     surface is clean again.

  3. dead-man heartbeat — a persisted last-successful-run timestamp. If no run
     has recorded in > MAX_GAP_HOURS (default 26 — one daily cron + slack), the
     cron itself is dead; the next run (or a separate scheduled probe) alerts.

State persists in a committed file (`specs/snapshots/.state.json`) — the same
pattern as the `.sha` baselines (the workflow never writes anywhere else, and a
committed file survives cache eviction). Stdlib only; no network.

Exit 0 = healthy; exit 1 = a guard tripped (CI step fires ntfy + fails);
exit 2 = usage / parse error.

Usage:
  watcher-liveness.py --record-run DRIFT.json [--now ISO]   # update streaks + timestamp; fail if a streak >= threshold
  watcher-liveness.py --heartbeat-check [--now ISO]         # fail if the last recorded run is too old
  watcher-liveness.py --show                                # print current state
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STATE = os.path.join(REPO_ROOT, "specs", "snapshots", ".state.json")

ERROR_STATUSES = {"fetch_error", "no_baseline"}
# Successful observations (hash compared). "drift" is successful but baseline-stale.
OK_STATUSES = {"ok", "drift", "seeded", "refreshed"}
# Baseline advanced or surface is clean — clear baseline_stale_streak.
BASELINE_CURRENT_STATUSES = {"ok", "seeded", "refreshed"}
# Hash moved, baseline did not — accumulate baseline_stale_streak.
BASELINE_STALE_STATUSES = {"drift"}


def _now(args_now: str | None) -> datetime:
    if args_now:
        return datetime.fromisoformat(args_now.replace("Z", "+00:00")).astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _load_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return {
        "state_version": "watcher-liveness/v1",
        "last_run_utc": None,
        "max_gap_hours": 26,
        "streak_threshold": 3,
        "surfaces": {},
    }


def _save_state(path: str, state: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)
        fh.write("\n")


def _default_surface_rec() -> dict:
    return {
        "fetch_error_streak": 0,
        "baseline_stale_streak": 0,
        "last_ok_utc": None,
    }


def cmd_record_run(state_path: str, drift_path: str, now_iso: str | None) -> int:
    state = _load_state(state_path)
    threshold = int(state.get("streak_threshold", 3))
    with open(drift_path, encoding="utf-8") as fh:
        drift = json.load(fh)

    surfaces = state.setdefault("surfaces", {})
    for row in drift.get("sources", []):
        name, status = row.get("source"), row.get("status")
        if not name:
            continue
        rec = surfaces.setdefault(name, _default_surface_rec())
        # Backfill key for states written before baseline_stale_streak existed.
        rec.setdefault("baseline_stale_streak", 0)
        rec.setdefault("fetch_error_streak", 0)

        if status in ERROR_STATUSES:
            rec["fetch_error_streak"] = int(rec.get("fetch_error_streak", 0)) + 1
            # Do not touch baseline_stale_streak on fetch errors — we did not
            # observe the baseline relationship this run.
        elif status in OK_STATUSES:
            rec["fetch_error_streak"] = 0
            rec["last_ok_utc"] = drift.get("checked_at")
            if status in BASELINE_STALE_STATUSES:
                rec["baseline_stale_streak"] = int(rec.get("baseline_stale_streak", 0)) + 1
            elif status in BASELINE_CURRENT_STATUSES:
                rec["baseline_stale_streak"] = 0

    state["last_run_utc"] = (now_iso or _now(None).strftime("%Y-%m-%dT%H:%M:%SZ"))
    _save_state(state_path, state)

    fetch_exceeded = [
        f"{name} (fetch_error_streak={rec['fetch_error_streak']})"
        for name, rec in surfaces.items()
        if int(rec.get("fetch_error_streak", 0)) >= threshold
    ]
    stale_exceeded = [
        f"{name} (baseline_stale_streak={rec['baseline_stale_streak']})"
        for name, rec in surfaces.items()
        if int(rec.get("baseline_stale_streak", 0)) >= threshold
    ]

    tripped = False
    if fetch_exceeded:
        tripped = True
        print(f"watcher-liveness: FETCH-ERROR STREAK >= {threshold} on:")
        for e in fetch_exceeded:
            print(f"  - {e}")
        print("These surfaces are effectively unmonitored. Investigate the upstream URL / extractor.")
    if stale_exceeded:
        tripped = True
        print(f"watcher-liveness: BASELINE-STALE STREAK >= {threshold} on:")
        for e in stale_exceeded:
            print(f"  - {e}")
        print(
            "These surfaces have drifted for N consecutive successful captures "
            "without a baseline advance. Open/merge the promotion PR or run "
            "spec-drift-check.sh --refresh after human review."
        )
    if tripped:
        return 1
    print(
        f"watcher-liveness: recorded run; all {len(surfaces)} surfaces under "
        f"the streak threshold ({threshold}) for fetch-error and baseline-stale."
    )
    return 0


def cmd_heartbeat_check(state_path: str, now_iso: str | None) -> int:
    state = _load_state(state_path)
    last = state.get("last_run_utc")
    max_gap = float(state.get("max_gap_hours", 26))
    if not last:
        print("watcher-liveness: heartbeat bootstrap — no prior run recorded yet (OK).")
        return 0
    now = _now(now_iso)
    gap_hours = (now - _parse_iso(last)).total_seconds() / 3600.0
    if gap_hours > max_gap:
        print(
            f"watcher-liveness: DEAD-MAN HEARTBEAT TRIPPED — last run {last} "
            f"was {gap_hours:.1f}h ago (> {max_gap}h). The drift cron is not firing."
        )
        return 1
    print(f"watcher-liveness: heartbeat OK — last run {gap_hours:.1f}h ago (<= {max_gap}h).")
    return 0


def cmd_show(state_path: str) -> int:
    print(json.dumps(_load_state(state_path), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Spec-drift watcher liveness guards.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--record-run", metavar="DRIFT.json", help="update streaks + timestamp from a drift JSON report")
    group.add_argument("--heartbeat-check", action="store_true", help="fail if the last recorded run is too old")
    group.add_argument("--show", action="store_true", help="print current state")
    parser.add_argument("--state", default=DEFAULT_STATE, help="state file path")
    parser.add_argument("--now", default=None, help="override 'now' (ISO 8601) for deterministic tests")
    args = parser.parse_args()

    if args.record_run:
        return cmd_record_run(args.state, args.record_run, args.now)
    if args.heartbeat_check:
        return cmd_heartbeat_check(args.state, args.now)
    if args.show:
        return cmd_show(args.state)
    return 2


if __name__ == "__main__":
    sys.exit(main())
