#!/usr/bin/env python3
"""Anthropic leading-indicator watcher — the bitter-lesson trigger (plan 033 § 14.11).

The spec-drift watcher (scripts/spec-drift-check.sh + scripts/fetch-capture.py)
answers "did an upstream contract page change?" THIS watcher answers a different,
strategic question: "has Anthropic shipped something that signals the Spec
Authority Kernel (SAK) should stop investing and cut over to upstream?" The 12
indicators (§ 14.11.1) range Low → CRITICAL; the disposition matrix (§ 14.11.2)
counts firings by severity into a verdict (CONTINUE | NOTE | RETRO | PAUSE | STOP).

It mirrors the deterministic-detection + typed-fetch-failure posture of the
spec-drift machinery exactly:

  * Only a clean fetch feeds disposition. A fetch failure (network, 404, rate
    limit, shape-broken page) is classified, alerted, and recorded — but it is
    NEVER a hit. A bad fetch can never masquerade as an Anthropic signal
    (Armstrong's typed-isolated-failure discipline, 052-AT-SPEC).
  * Detection is deterministic. Structured sources (GitHub releases atom, RSS
    feed entry ids, JSON/TS schema presence) are parsed exactly and diff against
    last_known_snapshot; a change there escalates IMMEDIATELY.
  * The 2 prose sources (indicators #1, #6 — Anthropic blog + skills overview)
    are the only flake risk. Per § 14.11.3 (<5% flake budget) a prose change
    HOLDS for a 7-day disposition window before it counts as an escalating hit;
    inside the window it is PENDING, not firing.

Stdlib only. Network ONLY in live mode; --self-test is fully offline with
fixtures (a new-hit case, a no-change case, a fetch-failure case).

Exit 0 = no new escalating hit (or self-test passed);
exit 1 = at least one new escalating hit (or self-test failure);
exit 2 = usage / config error.

Usage:
  leading-indicator-watch.py                       # poll all 12 indicators
  leading-indicator-watch.py --state STATE.json    # persisted window state
  leading-indicator-watch.py --report REPORT.json  # write a JSON report (CI)
  leading-indicator-watch.py --self-test           # offline fixtures
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_REGISTRY = os.path.join(REPO_ROOT, "specs", "leading-indicators.v1.json")
DEFAULT_STATE = os.path.join(REPO_ROOT, "specs", "snapshots", ".leading-indicator-state.json")

# Typed fetch-failure taxonomy — same vocabulary as fetch-capture.py (052-AT-SPEC).
# Only FETCH_OK ever feeds disposition; everything else is alert-only, never a hit.
FETCH_OK = "FETCH_OK"
UNREACHABLE = "UNREACHABLE"
MOVED = "MOVED"
RATELIMITED = "RATELIMITED"
SHAPE_CHANGED = "SHAPE_CHANGED"
FETCH_STATUSES = (FETCH_OK, UNREACHABLE, MOVED, RATELIMITED, SHAPE_CHANGED)

# Prose sources (indicators 1, 6) hold a change for this window before escalating.
PROSE_DISPOSITION_DAYS = 7
PROSE_KIND = "prose"
STRUCTURED_KINDS = ("github-release", "rss", "json-schema")

SEVERITIES = ("Low", "Medium", "High", "CRITICAL")

TIMEOUT_SECONDS = 30
USER_AGENT = "intent-eval-lab-leading-indicator-watch/1.0"

# Per source_kind, the exact deterministic extraction. A structured source parses
# to a stable token; a shape mismatch is SHAPE_CHANGED (not a hit). Prose hashes
# the whole body (the 7-day window absorbs cosmetic churn before it escalates).
_RELEASE_ID = re.compile(r"<id>(tag:github\.com,[^<]+)</id>")
_RSS_ID = re.compile(r"<id>([^<]+)</id>")
_SHAPE_HINTS = {
    "github-release": _RELEASE_ID,
    "rss": _RSS_ID,
    # A markdown/TS spec body must carry at least one heading or an interface decl.
    "json-schema": re.compile(r"(?m)^#{1,3} |export (interface|type)|\"\$schema\""),
    "prose": re.compile(r"(?m)^#{1,3} |<id>"),
}


def _classify(http_code, body, error, kind):
    """Map a raw fetch to one typed status (first rule wins; conservative)."""
    if error is not None:
        if http_code == 429:
            return RATELIMITED
        if http_code == 404:
            return MOVED
        return UNREACHABLE
    if http_code == 429:
        return RATELIMITED
    if http_code == 404:
        return MOVED
    if http_code is None or http_code >= 400:
        return UNREACHABLE
    text = (body or b"").decode("utf-8", errors="replace")
    hint = _SHAPE_HINTS.get(kind)
    if hint is not None and not hint.search(text):
        return SHAPE_CHANGED
    return FETCH_OK


def _extract_snapshot(body, kind):
    """Deterministic snapshot token from a FETCH_OK body. Structured sources
    extract their stable id; prose hashes the whole body."""
    import hashlib

    text = (body or b"").decode("utf-8", errors="replace")
    if kind in ("github-release", "rss"):
        pat = _SHAPE_HINTS[kind]
        m = pat.search(text)
        return m.group(1) if m else None
    # json-schema + prose: stable content hash (json-schema is a presence/identity
    # signal; prose is whole-body, with the 7-day window guarding against churn).
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def http_fetch(url):
    """Return (http_code, body, error). Stdlib only."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as resp:
            return resp.status, resp.read(), None
    except urllib.error.HTTPError as exc:
        return exc.code, None, str(exc)
    except Exception as exc:  # URLError, timeout, ConnectionError, ...
        return None, None, str(exc)


def default_fetcher(indicator):
    """(http_code, body, error) for one indicator. Swapped out in --self-test."""
    return http_fetch(indicator["source_url"])


def load_registry(path):
    with open(path, encoding="utf-8") as fh:
        registry = json.load(fh)
    indicators = registry.get("indicators", [])
    if len(indicators) != 12:
        print(f"ERROR: expected 12 indicators, found {len(indicators)}", file=sys.stderr)
        sys.exit(2)
    return registry, indicators


def load_state(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def evaluate_indicator(indicator, state, http_code, body, error, now):
    """Classify the fetch, diff against the baseline, and decide whether this
    indicator FIRES (an escalating hit), is PENDING (prose inside its 7-day
    window), is UNCHANGED, or had a non-FETCH_OK fetch (alert-only, never a hit).

    Returns a dict row + the new per-indicator state to persist.
    """
    iid = str(indicator["id"])
    kind = indicator["source_kind"]
    severity = indicator["severity"]
    prior = state.get(iid, {})
    # Baseline precedence: persisted state (live evolution) then the seed in the
    # registry's last_known_snapshot (null at seed).
    baseline = prior.get("snapshot", indicator.get("last_known_snapshot"))

    status = _classify(http_code, body, error, kind)
    row = {
        "id": indicator["id"],
        "indicator": indicator["indicator"],
        "severity": severity,
        "source_kind": kind,
        "fetch_status": status,
        "disposition": None,
        "fires": False,
    }
    new_state = dict(prior)

    if status != FETCH_OK:
        # A bad fetch is a typed, isolated failure. NEVER a hit. The last-known
        # snapshot + any pending window are preserved untouched.
        row["disposition"] = "bad-fetch (alert-only, never a hit)"
        return row, new_state

    snapshot = _extract_snapshot(body, kind)
    new_state["last_fetch_at"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    changed = baseline is not None and snapshot != baseline
    first_seed = baseline is None

    if first_seed:
        # First clean fetch seeds the baseline; seeding is never a hit.
        new_state["snapshot"] = snapshot
        row["disposition"] = "seeded baseline (no prior snapshot)"
        new_state.pop("pending_since", None)
        return row, new_state

    if not changed:
        # No change vs baseline (incl. a prose page that reverted mid-window).
        # Advance baseline to the observed value (a no-op when equal) and clear
        # any pending state.
        new_state["snapshot"] = snapshot
        row["disposition"] = "unchanged"
        new_state.pop("pending_since", None)
        return row, new_state

    # A change was detected against a real baseline.
    if kind in STRUCTURED_KINDS:
        # Structured sources escalate IMMEDIATELY (<5% flake budget: structured
        # parsing only escalates immediately, per § 14.11.3). Advance the
        # baseline so the same release/entry id doesn't re-fire next run.
        new_state["snapshot"] = snapshot
        row["fires"] = True
        row["disposition"] = "FIRING (structured-source change, immediate escalation)"
        new_state.pop("pending_since", None)
        return row, new_state

    # Prose source (#1, #6): hold for a 7-day disposition window before firing.
    # CRITICAL: while PENDING we deliberately DO NOT advance the baseline snapshot
    # — keeping the OLD baseline is what makes the change keep being detected on
    # each daily run until the window elapses. Advancing it here would erase the
    # very change we're holding, and the watcher would silently forget it.
    pending_since_raw = prior.get("pending_since")
    if pending_since_raw is None:
        new_state["snapshot"] = baseline  # hold old baseline (see note above)
        new_state["pending_since"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        new_state["pending_snapshot"] = snapshot
        row["disposition"] = (
            f"PENDING (prose change; holds {PROSE_DISPOSITION_DAYS}d before escalation)"
        )
        return row, new_state

    pending_since = datetime.strptime(pending_since_raw, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )
    if now - pending_since >= timedelta(days=PROSE_DISPOSITION_DAYS):
        # Window elapsed and the change is still present → fire, and NOW adopt the
        # observed snapshot as the new baseline so it doesn't re-fire.
        new_state["snapshot"] = snapshot
        row["fires"] = True
        row["disposition"] = (
            f"FIRING (prose change persisted {PROSE_DISPOSITION_DAYS}+d past window)"
        )
        new_state.pop("pending_since", None)
        new_state.pop("pending_snapshot", None)
        return row, new_state

    # Still inside the window — keep the OLD baseline + the original pending_since.
    new_state["snapshot"] = baseline
    new_state["pending_since"] = pending_since_raw
    new_state["pending_snapshot"] = snapshot
    days_held = (now - pending_since).days
    row["disposition"] = (
        f"PENDING ({days_held}/{PROSE_DISPOSITION_DAYS}d into prose disposition window)"
    )
    return row, new_state


def disposition_verdict(firing_rows, matrix):
    """Count firings by severity → the disposition-matrix verdict (§ 14.11.2)."""
    counts = {s: 0 for s in SEVERITIES}
    for r in firing_rows:
        counts[r["severity"]] += 1
    crit = counts["CRITICAL"]
    high = counts["High"]
    med = counts["Medium"]
    low = counts["Low"]

    if crit >= 2:
        verdict, action = "STOP", "STOP SAK; archive as historical contribution; cut over to upstream"
    elif crit == 1:
        verdict, action = (
            "PAUSE",
            "PAUSE all SAK phases; ISEDC Class-1 re-charter to evaluate upstream cutover",
        )
    elif high >= 1 or med >= 2:
        verdict, action = "RETRO", "ISEDC Class-2 retrospective; consider pausing Phase >= 3"
    elif med == 1:
        verdict, action = "NOTE", "Note in next AAR; no plan change"
    else:
        # 0 firings, or only Low-severity firings (0-2 Low).
        verdict, action = "CONTINUE", "Continue per plan"
    return {
        "verdict": verdict,
        "action": action,
        "counts": counts,
        "firing": len(firing_rows),
    }


def run_watch(indicators, state, matrix, fetcher=default_fetcher, now=None):
    """Poll every indicator; return (exit_code, report_dict, new_state)."""
    now = now or datetime.now(timezone.utc)
    rows = []
    new_state = dict(state)
    bad_fetches = []
    firing_rows = []
    pending_rows = []

    for indicator in indicators:
        http_code, body, error = fetcher(indicator)
        row, ind_state = evaluate_indicator(indicator, state, http_code, body, error, now)
        new_state[str(indicator["id"])] = ind_state
        rows.append(row)
        if row["fetch_status"] != FETCH_OK:
            bad_fetches.append(row)
        if row["fires"]:
            firing_rows.append(row)
        elif row["disposition"] and row["disposition"].startswith("PENDING"):
            pending_rows.append(row)

    verdict = disposition_verdict(firing_rows, matrix)
    report = {
        "evaluated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "indicators": rows,
        "bad_fetches": [r["id"] for r in bad_fetches],
        "pending": [r["id"] for r in pending_rows],
        "firing": [r["id"] for r in firing_rows],
        "verdict": verdict,
    }
    # Exit 1 iff at least one indicator newly FIRED. Bad fetches alone never
    # fail the gate (upstream temporarily unavailable; alert, don't false-positive).
    exit_code = 1 if firing_rows else 0
    return exit_code, report, new_state


def print_report(report):
    print(f"Leading-indicator watch — {report['evaluated_at']}")
    for r in report["indicators"]:
        mark = "FIRE" if r["fires"] else ("BAD " if r["fetch_status"] != FETCH_OK else "  · ")
        print(f"  [{mark}] #{r['id']:<2} ({r['severity']:<8}) {r['indicator']}")
        print(f"         {r['disposition']}")
    v = report["verdict"]
    print("")
    print(
        f"Firing: {v['firing']} "
        f"(CRITICAL={v['counts']['CRITICAL']} High={v['counts']['High']} "
        f"Medium={v['counts']['Medium']} Low={v['counts']['Low']})"
    )
    if report["bad_fetches"]:
        print(f"Bad fetches (alert-only, never a hit): {report['bad_fetches']}")
    if report["pending"]:
        print(f"Prose pending (inside 7d window): {report['pending']}")
    print(f"VERDICT: {v['verdict']} — {v['action']}")


# ── Offline deterministic self-test ─────────────────────────────────────────


def cmd_self_test():
    failures = 0

    def check(label, condition):
        nonlocal failures
        if condition:
            print(f"self-test ok: {label}")
        else:
            print(f"self-test FAIL: {label}")
            failures += 1

    registry, indicators = load_registry(DEFAULT_REGISTRY)
    matrix = registry.get("disposition_matrix", [])
    now = datetime(2026, 6, 12, 9, 0, 0, tzinfo=timezone.utc)

    # Classification fixtures — every status reachable, exactly one each.
    good_release = b"<feed><entry><id>tag:github.com,2008:Repository/1/v2.0.0</id></entry></feed>"
    check("classify github-release FETCH_OK", _classify(200, good_release, None, "github-release") == FETCH_OK)
    check("classify 429 -> RATELIMITED", _classify(429, None, "HTTP 429", "rss") == RATELIMITED)
    check("classify 404 -> MOVED", _classify(404, None, "HTTP 404", "rss") == MOVED)
    check("classify 500 -> UNREACHABLE", _classify(500, None, "HTTP 500", "rss") == UNREACHABLE)
    check("classify timeout -> UNREACHABLE", _classify(None, None, "timed out", "prose") == UNREACHABLE)
    check(
        "classify shape-broken release -> SHAPE_CHANGED",
        _classify(200, b"<html>not a feed</html>", None, "github-release") == SHAPE_CHANGED,
    )

    # Scripted fetcher: id -> sequence of (http_code, body, error) across runs.
    scripts = {}

    def fake_fetcher(indicator):
        return scripts[indicator["id"]].pop(0)

    # CASE 1 — no change: a structured source returns the same release id twice.
    # First run seeds; second run is UNCHANGED → no fire.
    rel_a = b"<feed><entry><id>tag:github.com,2008:Repository/1/v1.0.0</id></entry></feed>"
    for ind in indicators:
        # All structured sources see rel_a both runs; prose sees a stable body.
        body = rel_a if ind["source_kind"] in ("github-release", "rss") else b"# Stable heading\n\nbody"
        scripts[ind["id"]] = [(200, body, None), (200, body, None)]
    rc_seed, rep_seed, st1 = run_watch(indicators, {}, matrix, fetcher=fake_fetcher, now=now)
    check("seed run: exit 0 (seeding is never a hit)", rc_seed == 0)
    check("seed run: 0 firing", len(rep_seed["firing"]) == 0)
    rc_same, rep_same, st2 = run_watch(indicators, st1, matrix, fetcher=fake_fetcher, now=now)
    check("no-change run: exit 0", rc_same == 0)
    check("no-change run: 0 firing", len(rep_same["firing"]) == 0)
    check("no-change run: verdict CONTINUE", rep_same["verdict"]["verdict"] == "CONTINUE")

    # CASE 2 — new hit: a CRITICAL structured source (indicator 5) changes its
    # release id on the second run → fires immediately → PAUSE verdict.
    scripts = {}
    crit5 = next(i for i in indicators if i["id"] == 5)
    rel_b = b"<feed><entry><id>tag:github.com,2008:Repository/1/v2.0.0</id></entry></feed>"
    for ind in indicators:
        body0 = rel_a if ind["source_kind"] in ("github-release", "rss") else b"# Stable\n\nx"
        scripts[ind["id"]] = [(200, body0, None)]
    # seed
    _, _, st_seed = run_watch(indicators, {}, matrix, fetcher=lambda i: scripts[i["id"]].pop(0), now=now)
    scripts2 = {}
    for ind in indicators:
        if ind["id"] == 5:
            scripts2[ind["id"]] = [(200, rel_b, None)]  # CRITICAL source changed
        else:
            body0 = rel_a if ind["source_kind"] in ("github-release", "rss") else b"# Stable\n\nx"
            scripts2[ind["id"]] = [(200, body0, None)]
    rc_hit, rep_hit, _ = run_watch(
        indicators, st_seed, matrix, fetcher=lambda i: scripts2[i["id"]].pop(0), now=now
    )
    check("new-hit run: exit 1 (a CRITICAL indicator fired)", rc_hit == 1)
    check("new-hit run: indicator 5 in firing list", 5 in rep_hit["firing"])
    check("new-hit run: verdict PAUSE (1 CRITICAL)", rep_hit["verdict"]["verdict"] == "PAUSE")
    check("new-hit severity: CRITICAL count == 1", rep_hit["verdict"]["counts"]["CRITICAL"] == 1)

    # CASE 3 — fetch failure: an UNREACHABLE source is alert-only, never a hit,
    # and the last-known snapshot is preserved.
    scripts3 = {}
    for ind in indicators:
        if ind["id"] == 5:
            scripts3[ind["id"]] = [(None, None, "connection refused")]  # bad fetch on the CRITICAL one
        else:
            body0 = rel_a if ind["source_kind"] in ("github-release", "rss") else b"# Stable\n\nx"
            scripts3[ind["id"]] = [(200, body0, None)]
    rc_bad, rep_bad, st_bad = run_watch(
        indicators, st_seed, matrix, fetcher=lambda i: scripts3[i["id"]].pop(0), now=now
    )
    check("bad-fetch run: exit 0 (a bad fetch is never a hit)", rc_bad == 0)
    check("bad-fetch run: 5 in bad_fetches", 5 in rep_bad["bad_fetches"])
    check("bad-fetch run: 5 NOT in firing", 5 not in rep_bad["firing"])
    check(
        "bad-fetch run: last-known snapshot for 5 preserved",
        st_bad["5"].get("snapshot") == st_seed["5"].get("snapshot"),
    )

    # CASE 4 — prose 7-day window: a prose source (#6, Medium) changes; inside the
    # window it is PENDING not firing; past the window it fires.
    prose6 = next(i for i in indicators if i["id"] == 6)
    check("indicator 6 is prose", prose6["source_kind"] == PROSE_KIND)
    seed_state_6 = {"6": {"snapshot": "BASELINEHASH"}}
    changed_body = b"# New onboarding doc\n\nNow cites field validation."

    def only6(_ind, body):
        return (200, body, None)

    # day 0: prose change → PENDING (not firing)
    rc_p0, rep_p0, st_p0 = run_watch(
        [prose6], seed_state_6, matrix,
        fetcher=lambda i: only6(i, changed_body), now=now,
    )
    check("prose day0: exit 0 (inside window, not firing)", rc_p0 == 0)
    check("prose day0: indicator 6 PENDING", 6 in rep_p0["pending"])
    check("prose day0: pending_since recorded", "pending_since" in st_p0["6"])

    # day 8: same prose change still present → window elapsed → FIRES
    now8 = now + timedelta(days=8)
    rc_p8, rep_p8, _ = run_watch(
        [prose6], st_p0, matrix,
        fetcher=lambda i: only6(i, changed_body), now=now8,
    )
    check("prose day8: exit 1 (window elapsed → fires)", rc_p8 == 1)
    check("prose day8: indicator 6 FIRES", 6 in rep_p8["firing"])
    check("prose day8: verdict NOTE (1 Medium)", rep_p8["verdict"]["verdict"] == "NOTE")

    # CASE 5 — disposition matrix unit checks (severity → verdict).
    def fr(sev):
        return {"severity": sev}

    check("matrix 0 firing -> CONTINUE", disposition_verdict([], matrix)["verdict"] == "CONTINUE")
    check("matrix 2 Low -> CONTINUE", disposition_verdict([fr("Low"), fr("Low")], matrix)["verdict"] == "CONTINUE")
    check("matrix 1 Medium -> NOTE", disposition_verdict([fr("Medium")], matrix)["verdict"] == "NOTE")
    check("matrix 2 Medium -> RETRO", disposition_verdict([fr("Medium"), fr("Medium")], matrix)["verdict"] == "RETRO")
    check("matrix 1 High -> RETRO", disposition_verdict([fr("High")], matrix)["verdict"] == "RETRO")
    check("matrix 1 CRITICAL -> PAUSE", disposition_verdict([fr("CRITICAL")], matrix)["verdict"] == "PAUSE")
    check("matrix 2 CRITICAL -> STOP", disposition_verdict([fr("CRITICAL"), fr("CRITICAL")], matrix)["verdict"] == "STOP")

    # Registry sanity: severities valid; prose sources are exactly #1 and #6.
    prose_ids = sorted(i["id"] for i in indicators if i["source_kind"] == PROSE_KIND)
    check("registry: prose sources are exactly {1, 6}", prose_ids == [1, 6])
    check("registry: all severities valid", all(i["severity"] in SEVERITIES for i in indicators))
    check("registry: ids are 1..12", sorted(i["id"] for i in indicators) == list(range(1, 13)))

    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the leading-indicator watcher is not sound.")
        return 1
    print("\nself-test: all cases passed (new-hit, no-change, fetch-failure, prose-window, matrix).")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Anthropic leading-indicator watcher.")
    parser.add_argument("--self-test", action="store_true", help="offline fixtures-driven check")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY, help="indicator registry path")
    parser.add_argument("--state", default=DEFAULT_STATE, help="persisted window state path")
    parser.add_argument("--report", default=None, help="write a JSON report here (CI)")
    args = parser.parse_args()

    if args.self_test:
        return cmd_self_test()

    registry, indicators = load_registry(args.registry)
    matrix = registry.get("disposition_matrix", [])
    state = load_state(args.state)
    exit_code, report, new_state = run_watch(indicators, state, matrix)
    print_report(report)

    os.makedirs(os.path.dirname(args.state), exist_ok=True)
    with open(args.state, "w", encoding="utf-8") as fh:
        json.dump(new_state, fh, indent=2)
        fh.write("\n")
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
            fh.write("\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
