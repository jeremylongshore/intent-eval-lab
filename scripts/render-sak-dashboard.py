#!/usr/bin/env python3
"""SAK-DASHBOARD.md machine renderer (033 § 14.13.1; closes audit F-WC-005 / C4).

Renders the Spec Authority Kernel dashboard from COMMITTED state ONLY — no
network, no new state of its own. Mirrors the detector-health.py rendering
pattern exactly: derive a machine document (carrying a sha256 fingerprint of
every source consumed) plus a compact markdown rendering, then a --check mode
that re-derives at the COMMITTED generated_at and fails on a stale committed
output so CI catches a hand-edited or drifted dashboard.

The SAK dashboard is a DERIVED VIEW. Never hand-edit SAK-DASHBOARD.md. To change
what it says, edit the inputs and regenerate:

  SAK-STATE.json                         hand-maintained slow-moving facts the
                                         renderer cannot derive in-repo: phase
                                         status, the Phase-4 advisory->blocking
                                         state machine, the FTE-week cost ledger
                                         (029-DR-BAND is prose), and the SAK
                                         bead-subtree counts (the canonical bead
                                         store is the gitignored umbrella
                                         ~/000-projects/.beads/, unreadable from
                                         this repo / CI)
  specs/leading-indicators.v1.json       the 12 Anthropic leading indicators +
                                         severities + disposition matrix
                                         (063-AT-SPEC). A "firing" is a
                                         non-null last_known_snapshot diff; the
                                         live watcher state is CACHED not
                                         committed (leading-indicator-watch.yml),
                                         so the committed registry is the only
                                         in-repo truth: at-seed = 0 firing
  specs/lineage/coverage-map.json        the derived coverage-map projection
                                         (054-AT-SPEC): per-surface adopt /
                                         diverge / convergence-trigger state ->
                                         coverage-map-state section

Outputs (both GENERATED; deterministic given the inputs):
  SAK-DASHBOARD.md   root-level rendering (033 § 14.13.1 — root for visibility)
  specs/sak-dashboard.json   machine document, fingerprinting every source

--check fails when a committed output is stale vs its sources: it re-derives at
the COMMITTED generated_at, so mere passage of time never trips it — the same
pattern as detector-health.py --check and lineage-log.py project-coverage
--check. --self-test is offline + fixture-driven.

Stdlib only. Exit 0 = ok; 1 = check or self-test failure; 2 = usage error.

Usage:
  render-sak-dashboard.py                # regenerate both outputs
  render-sak-dashboard.py --check        # fail if a committed output is stale
  render-sak-dashboard.py --self-test    # offline deterministic fixtures
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import UTC, datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STATE = os.path.join(REPO_ROOT, "SAK-STATE.json")
DEFAULT_INDICATORS = os.path.join(REPO_ROOT, "specs", "leading-indicators.v1.json")
DEFAULT_COVERAGE = os.path.join(REPO_ROOT, "specs", "lineage", "coverage-map.json")
DEFAULT_JSON_OUT = os.path.join(REPO_ROOT, "specs", "sak-dashboard.json")
DEFAULT_MD_OUT = os.path.join(REPO_ROOT, "SAK-DASHBOARD.md")

SPEC_DOC = "000-docs/033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md"
GENERATED_HEADER = (
    "GENERATED-DO-NOT-EDIT — SAK dashboard derived from committed state "
    "(SAK-STATE.json + leading-indicators registry + lineage coverage map). "
    f"Regenerate: python3 scripts/render-sak-dashboard.py. Normative spec: {SPEC_DOC} § 14.13.1"
)


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _label(path: str, root: str) -> str:
    """Repo-relative label for a source path (committed JSON must never carry
    absolute paths); paths outside root (test fixtures) keep their own name."""
    abspath, absroot = os.path.abspath(path), os.path.abspath(root)
    if abspath.startswith(absroot + os.sep):
        return os.path.relpath(abspath, absroot)
    return path


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ── Derivation (pure given inputs) ───────────────────────────────────────────


def _derive_indicators(indicators_doc: dict) -> dict:
    """Firing count by severity + disposition verdict. A leading indicator is
    'firing' iff its committed last_known_snapshot is non-null (the watcher live
    state is cached, never committed, so the committed registry is the in-repo
    truth — at-seed every snapshot is null = 0 firing)."""
    rows = []
    firing_by_severity = {"Low": 0, "Medium": 0, "High": 0, "CRITICAL": 0}
    for ind in sorted(indicators_doc.get("indicators", []), key=lambda i: i["id"]):
        firing = ind.get("last_known_snapshot") is not None
        severity = ind.get("severity", "Low")
        if firing:
            firing_by_severity[severity] = firing_by_severity.get(severity, 0) + 1
        rows.append(
            {
                "id": ind["id"],
                "indicator": ind.get("indicator", ""),
                "severity": severity,
                "firing": firing,
            }
        )
    monitored = len(rows)
    firing_total = sum(firing_by_severity.values())

    # Disposition matrix (most-severe-wins), per specs/leading-indicators.v1.json
    # disposition_matrix + 033 § 14.11.2. Low-severity firings (0-2) fold into
    # the CONTINUE bucket, so only CRITICAL / High / Medium counts gate a verdict.
    crit = firing_by_severity["CRITICAL"]
    high = firing_by_severity["High"]
    med = firing_by_severity["Medium"]
    if crit >= 2:
        verdict, action = "STOP", "STOP SAK; archive as historical contribution; cut over to upstream"
    elif crit == 1:
        verdict, action = "PAUSE", "PAUSE all SAK phases; ISEDC Class-1 re-charter to evaluate upstream cutover"
    elif high >= 1 or med >= 2:
        verdict, action = "RETRO", "ISEDC Class-2 retrospective; consider pausing Phase >= 3"
    elif med == 1:
        verdict, action = "NOTE", "Note in next AAR; no plan change"
    else:
        verdict, action = "CONTINUE", "Continue per plan"

    return {
        "monitored": monitored,
        "firing_total": firing_total,
        "firing_by_severity": firing_by_severity,
        "verdict": verdict,
        "action": action,
        "rows": rows,
    }


def _derive_coverage(coverage_doc: dict) -> dict:
    """Coverage-map state from the derived projection (054-AT-SPEC)."""
    surfaces = coverage_doc.get("surfaces", {}) or {}
    total = len(surfaces)
    adopted = sum(1 for s in surfaces.values() if s.get("adopted"))
    divergences_outstanding = sum(len(s.get("divergences_outstanding", [])) for s in surfaces.values())
    convergence_fired = sum(len(s.get("convergence_fired", [])) for s in surfaces.values())
    convergence_triggers_outstanding = sum(int(s.get("convergence_triggers_outstanding", 0)) for s in surfaces.values())
    rows = []
    for name in sorted(surfaces):
        s = surfaces[name]
        rows.append(
            {
                "surface": name,
                "contract": s.get("contract"),
                "adopted": bool(s.get("adopted")),
                "divergences_outstanding": len(s.get("divergences_outstanding", [])),
                "convergence_triggers_outstanding": int(s.get("convergence_triggers_outstanding", 0)),
            }
        )
    return {
        "surfaces_total": total,
        "surfaces_adopted": adopted,
        "divergences_outstanding": divergences_outstanding,
        "convergence_fired": convergence_fired,
        "convergence_triggers_outstanding": convergence_triggers_outstanding,
        "rows": rows,
    }


def derive(
    state_path: str,
    indicators_path: str,
    coverage_path: str,
    generated_at: str,
    label_root: str,
) -> dict:
    state = _load_json(state_path)
    indicators_doc = _load_json(indicators_path)
    coverage_doc = _load_json(coverage_path)

    inputs = {
        _label(state_path, label_root): _sha256_file(state_path),
        _label(indicators_path, label_root): _sha256_file(indicators_path),
        _label(coverage_path, label_root): _sha256_file(coverage_path),
    }

    return {
        "_generated": GENERATED_HEADER,
        "dashboard_version": "sak-dashboard/v1",
        "generated_at": generated_at,
        "as_of": state.get("as_of"),
        "phases": list(state.get("phases", [])),
        "state_machine": dict(state.get("state_machine", {})),
        "leading_indicators": _derive_indicators(indicators_doc),
        "cost_ledger": dict(state.get("cost_ledger", {})),
        "bead_state": dict(state.get("bead_state", {})),
        "coverage_map": _derive_coverage(coverage_doc),
        "inputs": inputs,
    }


# ── Rendering ────────────────────────────────────────────────────────────────


def render_json(doc: dict) -> str:
    return json.dumps(doc, indent=2, sort_keys=True) + "\n"


def render_markdown(doc: dict) -> str:
    lines = [f"<!-- {GENERATED_HEADER} -->", "", f"# SAK Dashboard — generated {doc['generated_at']}", ""]
    lines.append(f"State as of {doc.get('as_of') or '(unspecified)'}. This file is DERIVED — never hand-edit it.")
    lines.append("")

    # Phase status.
    lines.append("## Phase status")
    lines.append("")
    if doc["phases"]:
        for p in doc["phases"]:
            lines.append(f"- **{p.get('phase', '?')}**: {p.get('status', '?')} — {p.get('detail', '')}")
    else:
        lines.append("- (no phases recorded in SAK-STATE.json)")
    lines.append("")

    # State machine.
    sm = doc["state_machine"]
    lines.append("## State machine")
    lines.append("")
    if sm:
        states = sm.get("states", [])
        lines.append(f"- Machine: {sm.get('machine', '?')}")
        lines.append(f"- Current state: **{sm.get('current_state', '?')}** (entered {sm.get('entered_at', '?')})")
        if states:
            lines.append(f"- States: {' -> '.join(states)}")
        lines.append(f"- Next gate: {sm.get('next_gate', '?')}")
    else:
        lines.append("- (no state machine recorded)")
    lines.append("")

    # Leading indicators.
    li = doc["leading_indicators"]
    sev = li["firing_by_severity"]
    lines.append("## Leading indicators")
    lines.append("")
    lines.append(
        f"- {li['monitored']} monitored | {li['firing_total']} firing "
        f"(CRITICAL {sev['CRITICAL']}, High {sev['High']}, Medium {sev['Medium']}, Low {sev['Low']})"
    )
    lines.append(f"- Disposition: **{li['verdict']}** — {li['action']}")
    lines.append("")
    lines.append("| # | Indicator | Severity | Firing |")
    lines.append("|---|---|---|---|")
    for row in li["rows"]:
        firing = "**FIRING**" if row["firing"] else "—"
        lines.append(f"| {row['id']} | {row['indicator']} | {row['severity']} | {firing} |")
    lines.append("")

    # Cost ledger.
    cl = doc["cost_ledger"]
    lines.append("## Cost ledger")
    lines.append("")
    if cl:
        unit = cl.get("unit", "FTE-week")
        lines.append(
            f"- Total budget: {cl.get('total_budget_fte_weeks', '?')} {unit} ({cl.get('total_calendar_floor', '?')})"
        )
        lines.append("")
        lines.append("| Phase | Budget (FTE-days) | Spent (FTE-days) | Gated on |")
        lines.append("|---|---|---|---|")
        for p in cl.get("phases", []):
            budget = p.get("budget_fte_days", "?")
            spent = p.get("spent_fte_days", "?")
            try:
                pct = f" ({round(100.0 * float(spent) / float(budget), 1)}%)" if float(budget) else ""
            except (TypeError, ValueError, ZeroDivisionError):
                pct = ""
            lines.append(f"| {p.get('phase', '?')} | {budget} | {spent}{pct} | {p.get('gated_on', '?')} |")
    else:
        lines.append("- (no cost ledger recorded)")
    lines.append("")

    # Bead state.
    bs = doc["bead_state"]
    lines.append("## Bead state")
    lines.append("")
    lines.append(f"SAK / Skill-Refiner bead subtree (epic `9k5h`); captured {bs.get('captured_at', '?')}.")
    lines.append("")
    if bs.get("groups"):
        lines.append("| Label group | Open | In progress | Deferred | Closed |")
        lines.append("|---|---|---|---|---|")
        for g in bs["groups"]:
            lines.append(
                f"| `{g.get('label', '?')}` | {g.get('open', 0)} | {g.get('in_progress', 0)} | "
                f"{g.get('deferred', 0)} | {g.get('closed', 0)} |"
            )
    else:
        lines.append("- (no bead-state groups recorded)")
    lines.append("")

    # Coverage map.
    cm = doc["coverage_map"]
    lines.append("## Coverage map state")
    lines.append("")
    lines.append(
        f"- {cm['surfaces_adopted']}/{cm['surfaces_total']} upstream surfaces adopted | "
        f"{cm['divergences_outstanding']} divergences outstanding | "
        f"{cm['convergence_triggers_outstanding']} convergence triggers outstanding | "
        f"{cm['convergence_fired']} convergence triggers fired"
    )
    lines.append("")
    lines.append("| Surface | Contract | Adopted | Divergences outstanding | Convergence triggers outstanding |")
    lines.append("|---|---|---|---|---|")
    for row in cm["rows"]:
        lines.append(
            f"| {row['surface']} | {row['contract']} | {'yes' if row['adopted'] else 'NO'} | "
            f"{row['divergences_outstanding']} | {row['convergence_triggers_outstanding']} |"
        )
    return "\n".join(lines) + "\n"


# ── Commands ─────────────────────────────────────────────────────────────────


def _derive_from_args(args: argparse.Namespace, generated_at: str) -> dict:
    return derive(args.state, args.indicators, args.coverage_map, generated_at, args.label_root)


def cmd_generate(args: argparse.Namespace) -> int:
    if args.now:
        generated_at = _parse_iso(args.now).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        generated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    doc = _derive_from_args(args, generated_at)
    for out_path, content in ((args.json_out, render_json(doc)), (args.md_out, render_markdown(doc))):
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(content)
    li = doc["leading_indicators"]
    print(
        f"render-sak-dashboard: wrote {args.json_out} + {args.md_out} — "
        f"disposition {li['verdict']} ({li['firing_total']}/{li['monitored']} indicators firing)."
    )
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    if not os.path.exists(args.json_out):
        print(f"render-sak-dashboard --check: FAIL — committed output missing: {args.json_out}")
        return 1
    try:
        with open(args.json_out, encoding="utf-8") as fh:
            committed_json = fh.read()
        generated_at = json.loads(committed_json)["generated_at"]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"render-sak-dashboard --check: FAIL — committed JSON unreadable ({exc})")
        return 1

    doc = _derive_from_args(args, generated_at)
    stale = []
    if committed_json != render_json(doc):
        stale.append(args.json_out)
    if not os.path.exists(args.md_out):
        stale.append(f"{args.md_out} (missing)")
    else:
        with open(args.md_out, encoding="utf-8") as fh:
            if fh.read() != render_markdown(doc):
                stale.append(args.md_out)
    if stale:
        print(
            "render-sak-dashboard --check: STALE — committed output(s) do not match a fresh "
            f"derivation from the current sources (re-derived at the committed generated_at {generated_at}):"
        )
        for path in stale:
            print(f"  - {path}")
        print(
            "The SAK dashboard is a DERIVED view — never hand-edit it. "
            "Regenerate: python3 scripts/render-sak-dashboard.py"
        )
        return 1
    print(
        f"render-sak-dashboard --check: OK — committed dashboard is fresh (disposition {doc['leading_indicators']['verdict']})."
    )
    return 0


# ── Deterministic offline self-test ──────────────────────────────────────────

FIXTURE_NOW = "2026-06-20T12:00:00Z"


def _write_fixture(
    tmp: str,
    *,
    firing_ids: dict[int, str] | None = None,
) -> argparse.Namespace:
    """Build a self-contained fixture. firing_ids maps indicator id -> a
    non-null snapshot value (anything truthy = firing)."""
    firing_ids = firing_ids or {}
    indicators = {
        "registry_version": "leading-indicators/v1",
        "disposition_matrix": [],
        "indicators": [
            {"id": 1, "indicator": "ind-high", "severity": "High", "last_known_snapshot": firing_ids.get(1)},
            {"id": 2, "indicator": "ind-med", "severity": "Medium", "last_known_snapshot": firing_ids.get(2)},
            {"id": 3, "indicator": "ind-crit", "severity": "CRITICAL", "last_known_snapshot": firing_ids.get(3)},
            {"id": 4, "indicator": "ind-med-2", "severity": "Medium", "last_known_snapshot": firing_ids.get(4)},
            {"id": 5, "indicator": "ind-crit-2", "severity": "CRITICAL", "last_known_snapshot": firing_ids.get(5)},
        ],
    }
    state = {
        "state_version": "sak-state/v1",
        "as_of": "2026-06-20",
        "phases": [{"phase": "Phase 0", "status": "COMPLETE", "detail": "wedge landed"}],
        "state_machine": {
            "machine": "SAK advisory -> blocking flip",
            "current_state": "ADVISORY",
            "entered_at": "2026-06-09",
            "next_gate": "soak",
            "states": ["ADVISORY", "BLOCKING"],
        },
        "cost_ledger": {
            "unit": "FTE-week",
            "total_budget_fte_weeks": 8.8,
            "total_calendar_floor": "~3 months",
            "phases": [{"phase": "Phase A", "budget_fte_days": 10.0, "spent_fte_days": 2.0, "gated_on": "bandwidth"}],
        },
        "bead_state": {
            "captured_at": "2026-06-20",
            "groups": [{"label": "sak", "open": 23, "in_progress": 0, "deferred": 1, "closed": 0}],
        },
    }
    coverage = {
        "projection_version": "lineage-coverage/v1",
        "surfaces": {
            "surface-a": {
                "contract": "skill-frontmatter",
                "adopted": {"at": "2026-06-09T00:00:00Z", "event_id": 1},
                "divergences_outstanding": [{"subject": "x"}, {"subject": "y"}],
                "convergence_triggers_outstanding": 2,
                "convergence_fired": [],
            },
            "surface-b": {
                "contract": "mcp-config",
                "adopted": {"at": "2026-06-11T00:00:00Z", "event_id": 2},
                "divergences_outstanding": [],
                "convergence_triggers_outstanding": 0,
                "convergence_fired": [{"subject": "z"}],
            },
        },
    }
    paths = {
        "state": os.path.join(tmp, "SAK-STATE.json"),
        "indicators": os.path.join(tmp, "leading-indicators.v1.json"),
        "coverage_map": os.path.join(tmp, "coverage-map.json"),
        "json_out": os.path.join(tmp, "out", "sak-dashboard.json"),
        "md_out": os.path.join(tmp, "out", "SAK-DASHBOARD.md"),
    }
    for path, payload in (
        (paths["state"], state),
        (paths["indicators"], indicators),
        (paths["coverage_map"], coverage),
    ):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
            fh.write("\n")
    return argparse.Namespace(now=FIXTURE_NOW, label_root=tmp, **paths)


def cmd_self_test() -> int:
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        if condition:
            print(f"self-test ok: {label}")
        else:
            print(f"self-test FAIL: {label}")
            failures += 1

    def quiet_derive(ns: argparse.Namespace) -> dict:
        return _derive_from_args(ns, _parse_iso(ns.now).strftime("%Y-%m-%dT%H:%M:%SZ"))

    with tempfile.TemporaryDirectory() as tmp:
        # 1. No firing -> CONTINUE; every source fingerprinted (fixture-relative).
        os.makedirs(os.path.join(tmp, "continue"))
        ns = _write_fixture(os.path.join(tmp, "continue"))
        doc = quiet_derive(ns)
        check("no firing -> CONTINUE", doc["leading_indicators"]["verdict"] == "CONTINUE")
        check("no firing -> 0 firing total", doc["leading_indicators"]["firing_total"] == 0)
        check(
            "every source fingerprinted (3 inputs, fixture-relative)",
            len(doc["inputs"]) == 3
            and all(len(v) == 64 for v in doc["inputs"].values())
            and all(not k.startswith("/") for k in doc["inputs"]),
        )

        # 2. One Medium firing -> NOTE.
        os.makedirs(os.path.join(tmp, "note"))
        ns_note = _write_fixture(os.path.join(tmp, "note"), firing_ids={2: "snap"})
        doc = quiet_derive(ns_note)
        check("1 Medium firing -> NOTE", doc["leading_indicators"]["verdict"] == "NOTE")

        # 3. One High firing -> RETRO.
        os.makedirs(os.path.join(tmp, "retro-high"))
        ns_rh = _write_fixture(os.path.join(tmp, "retro-high"), firing_ids={1: "snap"})
        doc = quiet_derive(ns_rh)
        check("1 High firing -> RETRO", doc["leading_indicators"]["verdict"] == "RETRO")

        # 4. Two Medium firings -> RETRO.
        os.makedirs(os.path.join(tmp, "retro-med"))
        ns_rm = _write_fixture(os.path.join(tmp, "retro-med"), firing_ids={2: "s", 4: "s"})
        doc = quiet_derive(ns_rm)
        check("2 Medium firings -> RETRO", doc["leading_indicators"]["verdict"] == "RETRO")

        # 5. One CRITICAL firing -> PAUSE (most-severe-wins over coincident lows).
        os.makedirs(os.path.join(tmp, "pause"))
        ns_p = _write_fixture(os.path.join(tmp, "pause"), firing_ids={3: "s", 2: "s"})
        doc = quiet_derive(ns_p)
        check("1 CRITICAL firing -> PAUSE", doc["leading_indicators"]["verdict"] == "PAUSE")

        # 6. Two CRITICAL firings -> STOP.
        os.makedirs(os.path.join(tmp, "stop"))
        ns_s = _write_fixture(os.path.join(tmp, "stop"), firing_ids={3: "s", 5: "s"})
        doc = quiet_derive(ns_s)
        check("2 CRITICAL firings -> STOP", doc["leading_indicators"]["verdict"] == "STOP")
        check(
            "2 CRITICAL -> firing_by_severity CRITICAL == 2",
            doc["leading_indicators"]["firing_by_severity"]["CRITICAL"] == 2,
        )

        # 7. Coverage-map derivation: 2 adopted, 2 divergences, 1 fired, 2 triggers outstanding.
        doc = quiet_derive(ns)
        cm = doc["coverage_map"]
        check(
            "coverage map derived from projection",
            cm["surfaces_total"] == 2
            and cm["surfaces_adopted"] == 2
            and cm["divergences_outstanding"] == 2
            and cm["convergence_fired"] == 1
            and cm["convergence_triggers_outstanding"] == 2,
        )

        # 8. Cost ledger percent rendering present in markdown.
        md = render_markdown(doc)
        check("cost ledger renders percent of budget", "(20.0%)" in md)
        check(
            "markdown has all six sections",
            all(
                h in md
                for h in (
                    "## Phase status",
                    "## State machine",
                    "## Leading indicators",
                    "## Cost ledger",
                    "## Bead state",
                    "## Coverage map state",
                )
            ),
        )

        # 9. Determinism: two generations from the same inputs are byte-identical.
        check("generate exits 0", cmd_generate(ns) == 0)
        with open(ns.json_out, encoding="utf-8") as fh:
            first_json = fh.read()
        with open(ns.md_out, encoding="utf-8") as fh:
            first_md = fh.read()
        check("regenerate exits 0", cmd_generate(ns) == 0)
        with open(ns.json_out, encoding="utf-8") as fh:
            same_json = fh.read() == first_json
        with open(ns.md_out, encoding="utf-8") as fh:
            same_md = fh.read() == first_md
        check("deterministic given inputs (json + md byte-identical)", same_json and same_md)

        # 10. Freshness gate: fresh passes; hand-edit fails; source change fails;
        #     regenerate restores; missing json fails.
        check("--check passes right after generate", cmd_check(ns) == 0)
        with open(ns.md_out, "a", encoding="utf-8") as fh:
            fh.write("\nhand edit\n")
        check("--check FAILS on a hand-edited markdown", cmd_check(ns) == 1)
        check("regenerate restores freshness", cmd_generate(ns) == 0 and cmd_check(ns) == 0)
        state_doc = _load_json(ns.state)
        state_doc["state_machine"]["current_state"] = "BLOCKING-CANARY"
        with open(ns.state, "w", encoding="utf-8") as fh:
            json.dump(state_doc, fh, indent=2)
        check("--check FAILS when a source changed under the committed output", cmd_check(ns) == 1)
        check("regenerate after source change restores freshness", cmd_generate(ns) == 0 and cmd_check(ns) == 0)
        os.remove(ns.json_out)
        check("--check FAILS when the committed JSON is missing", cmd_check(ns) == 1)

    # 11. The committed real outputs must themselves be fresh (mirrors
    #     detector-health self-test step 10); guarded so fixtures-only envs skip.
    if os.path.exists(DEFAULT_JSON_OUT):
        ns_real = argparse.Namespace(
            state=DEFAULT_STATE,
            indicators=DEFAULT_INDICATORS,
            coverage_map=DEFAULT_COVERAGE,
            json_out=DEFAULT_JSON_OUT,
            md_out=DEFAULT_MD_OUT,
            label_root=REPO_ROOT,
            now=None,
        )
        check("committed dashboard is fresh", cmd_check(ns_real) == 0)

    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the SAK dashboard renderer is not sound.")
        return 1
    print("\nself-test: disposition matrix, coverage derivation, determinism, and freshness failure modes all sound.")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="SAK-DASHBOARD.md machine renderer (033 § 14.13.1).")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if a committed output is stale vs sources")
    mode.add_argument("--self-test", action="store_true", help="offline deterministic fixtures")
    parser.add_argument("--state", default=DEFAULT_STATE)
    parser.add_argument("--indicators", default=DEFAULT_INDICATORS)
    parser.add_argument("--coverage-map", default=DEFAULT_COVERAGE)
    parser.add_argument("--json-out", default=DEFAULT_JSON_OUT)
    parser.add_argument("--md-out", default=DEFAULT_MD_OUT)
    parser.add_argument("--now", default=None, help="override 'now' (UTC ISO) for deterministic generation")
    parser.add_argument(
        "--label-root",
        default=REPO_ROOT,
        help="root for relative path labels in the inputs fingerprint map (default: repo root)",
    )
    args = parser.parse_args()

    if args.self_test:
        return cmd_self_test()
    if args.check:
        return cmd_check(args)
    return cmd_generate(args)


if __name__ == "__main__":
    sys.exit(main())
