#!/usr/bin/env python3
"""SAK Phase-4 advisory->blocking flip state machine — emit + validation.

This is the formal state machine governing the SAK advisory->blocking flip
(Skill-Refiner / authoring-kernel adoption). It is DISTINCT from the 13-entity
runtime state machine at specs/state-machines/transition-table.v1.json
(Blueprint B). This one is the SAK Phase-4 *flip lifecycle*.

Normative authority (all in 000-docs/):
  - plan 033 v7 § 14.4.shadow  — the lifecycle diagram (states + edges)
  - plan 033 v7 § 14.4c        — the advisory->blocking flip exit gate
  - plan 048 v8 Delta 3        — REVISES § 14.4c: which preconditions the 30-day
                                 calendar ceiling can disposition. (a) coverage
                                 is dispositionable (quarantine the long tail);
                                 (c) zero-open-P0 and (d) governance-triple
                                 sign-off are HARD gates the ceiling never
                                 overrides.
  - plan 033 v7 § 14.4.rollback — rollback protocol + ROLLED-BACK semantics
  - plan 048 v8 Delta 4 / § 14.31 — authoring/v1 lifecycle-states

The machine (plan 033 § 14.4.shadow), formalized:

    ADVISORY --wave-a-merged--> ADVISORY-W-A --wave-b-done--> ADVISORY-W-AB
        --enable-shadow--> SHADOW-MODE
            --dispositions-resolved--> READY-TO-FLIP  (only if no open P0)
            --deviations-open-p0--> HOLDING
        HOLDING --audit-cleared--> SHADOW-MODE
        READY-TO-FLIP --governance-triple-signs--> BLOCKING   (HARD-gated)
        BLOCKING --regression-detected--> ROLLED-BACK
        ROLLED-BACK --back-to-shadow--> SHADOW-MODE

Plus the rollback-protocol edges off the wave states (§ 14.4.rollback):
        ADVISORY-W-A  --wave-a-failure--> ROLLED-BACK
        ADVISORY-W-AB --wave-b-failure--> ROLLED-BACK

ROLLED-BACK is reachable from the gated states (ADVISORY-W-A, ADVISORY-W-AB,
BLOCKING) per the prompt brief + § 14.4.rollback.

Design choices made where the plan is under-specified (documented in the PR):
  - HOLDING is the canonical diagram's audit branch off SHADOW-MODE; it is NOT
    in the prompt's 5-state subset but IS in § 14.4.shadow, so it is modeled.
    Its only exit is back to SHADOW-MODE (audit cleared) — it can never flip
    directly to BLOCKING.
  - The only HARD-gated transition is READY-TO-FLIP -> BLOCKING. Its three hard
    preconditions are (c) open_p0_count == 0 and (d) the full CTO+CISO+VP-DevRel
    triple sign-off; precondition (a) coverage is checked but is
    calendar-dispositionable (a flip with coverage < 99.5% is allowed only when
    the caller passes allow_calendar_ceiling=True, which quarantines the long
    tail — see can_flip()).
  - SHADOW-MODE -> READY-TO-FLIP additionally requires no open P0 (the diagram
    routes open-P0 deviations to HOLDING, not READY-TO-FLIP).
  - GOVERNANCE SIGN-OFF SOURCE IS STUBBED: until a live governance-signoff
    service exists, the three booleans are read from the preconditions block in
    SAK-STATE.json (hand-maintained). load_signoff_from_state() is the single
    seam a real source would replace.

The module is import-safe and offline. The CLI exposes:
    --self-test            deterministic offline self-test (CI gate)
    --validate <file>      jsonschema-validate a SAK-STATE.json against the schema
    --show                 print the legal-transition table

No network, no writes unless --emit is used with an explicit output path.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from dataclasses import dataclass, field

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STATE = os.path.join(REPO_ROOT, "SAK-STATE.json")
SCHEMA_PATH = os.path.join(REPO_ROOT, "specs", "state-machines", "schema", "sak-state.schema.json")

# ── The lifecycle ────────────────────────────────────────────────────────────

#: The eight states (plan 033 § 14.4.shadow), forward order.
STATES: tuple[str, ...] = (
    "ADVISORY",
    "ADVISORY-W-A",
    "ADVISORY-W-AB",
    "SHADOW-MODE",
    "HOLDING",
    "READY-TO-FLIP",
    "BLOCKING",
    "ROLLED-BACK",
)

#: States from which a rollback (-> ROLLED-BACK) is reachable.
GATED_STATES: frozenset[str] = frozenset({"ADVISORY-W-A", "ADVISORY-W-AB", "BLOCKING"})

#: The hard-gated flip transition (the one event whose preconditions the
#: calendar ceiling can NEVER override — plan 048 Delta 3).
FLIP_EVENT = "governance-triple-signs"

# ── Coverage / shadow floors (plan 033 § 14.4c + § 14.4b.5) ──────────────────

COVERAGE_FLOOR_PCT = 99.5
SHADOW_MIN_DAYS = 7
SHADOW_MAX_DEVIATION_PCT = 0.5


#: Legal transitions: (from_state, event) -> to_state.
#: Every value here is a state in STATES; this is the single source of the graph.
LEGAL_TRANSITIONS: dict[tuple[str, str], str] = {
    ("ADVISORY", "wave-a-merged"): "ADVISORY-W-A",
    ("ADVISORY-W-A", "wave-b-done"): "ADVISORY-W-AB",
    ("ADVISORY-W-A", "wave-a-failure"): "ROLLED-BACK",
    ("ADVISORY-W-AB", "enable-shadow"): "SHADOW-MODE",
    ("ADVISORY-W-AB", "wave-b-failure"): "ROLLED-BACK",
    ("SHADOW-MODE", "dispositions-resolved"): "READY-TO-FLIP",
    ("SHADOW-MODE", "deviations-open-p0"): "HOLDING",
    ("HOLDING", "audit-cleared"): "SHADOW-MODE",
    ("READY-TO-FLIP", FLIP_EVENT): "BLOCKING",
    ("BLOCKING", "regression-detected"): "ROLLED-BACK",
    ("ROLLED-BACK", "back-to-shadow"): "SHADOW-MODE",
}


# ── Result types ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class TransitionDecision:
    """The outcome of evaluating a requested transition."""

    allowed: bool
    from_state: str
    event: str
    to_state: str | None
    reasons: tuple[str, ...] = field(default_factory=tuple)

    @property
    def rejected(self) -> bool:
        return not self.allowed


class TransitionError(Exception):
    """Raised by emit() when a transition is rejected."""

    def __init__(self, decision: TransitionDecision):
        self.decision = decision
        super().__init__("; ".join(decision.reasons) or "transition rejected")


# ── Precondition evaluation ──────────────────────────────────────────────────


def _coerce_preconditions(state_machine: dict) -> dict:
    """Pull the preconditions block out of a state_machine dict, defaulting
    to an empty (all-unknown) block. Never mutates the input."""
    pre = state_machine.get("preconditions") or {}
    return dict(pre)


def load_signoff_from_state(state_machine: dict) -> dict:
    """STUB SEAM — read the governance triple sign-off from SAK-STATE.json.

    A real governance-signoff source (an ISEDC AT-DECR ledger, a signing
    service) would replace this single function. Until then the three booleans
    are hand-maintained in SAK-STATE.json's
    state_machine.preconditions.governance_signoff. Missing block => all false.
    """
    pre = _coerce_preconditions(state_machine)
    signoff = pre.get("governance_signoff") or {}
    return {
        "cto": bool(signoff.get("cto", False)),
        "ciso": bool(signoff.get("ciso", False)),
        "vp_devrel": bool(signoff.get("vp_devrel", False)),
        "decision_record_ref": signoff.get("decision_record_ref"),
    }


def _governance_complete(signoff: dict) -> bool:
    return bool(signoff.get("cto") and signoff.get("ciso") and signoff.get("vp_devrel"))


def can_flip(
    state_machine: dict,
    *,
    allow_calendar_ceiling: bool = False,
) -> TransitionDecision:
    """Evaluate the advisory->blocking flip (READY-TO-FLIP -> BLOCKING).

    Hard gates (plan 048 Delta 3 — the calendar ceiling NEVER overrides these):
      (c) open_p0_count == 0
      (d) full CTO + CISO + VP-DevRel triple sign-off
    Calendar-dispositionable gate:
      (a) coverage >= 99.5%  — UNLESS allow_calendar_ceiling=True, in which case
          a flip below the floor is permitted (the long tail is quarantined).
    Advisory gate (recorded but never blocks the flip on its own here):
      (b) shadow window >= 7d at deviation < 0.5% — surfaced as a reason if unmet.
    """
    from_state = "READY-TO-FLIP"
    to_state = "BLOCKING"
    pre = _coerce_preconditions(state_machine)
    reasons: list[str] = []

    if state_machine.get("current_state") != from_state:
        reasons.append(f"flip requires current_state == {from_state!r}, got {state_machine.get('current_state')!r}")

    # (c) zero open P0 — HARD.
    open_p0 = pre.get("open_p0_count")
    if open_p0 is None:
        reasons.append("precondition (c) unmet: open_p0_count is unknown (must be explicitly 0)")
    elif open_p0 != 0:
        reasons.append(f"precondition (c) unmet: {open_p0} open P0 issue(s) in schema-revision-candidates queue")

    # (d) governance triple — HARD.
    signoff = load_signoff_from_state(state_machine)
    if not _governance_complete(signoff):
        missing = [r for r in ("cto", "ciso", "vp_devrel") if not signoff.get(r)]
        reasons.append(
            "precondition (d) unmet: governance triple sign-off incomplete (missing: " + ", ".join(missing) + ")"
        )

    # (a) coverage — calendar-dispositionable.
    coverage = pre.get("coverage_corpus_pass_pct")
    if coverage is None:
        if not allow_calendar_ceiling:
            reasons.append("precondition (a) unmet: coverage_corpus_pass_pct is unknown")
    elif coverage < COVERAGE_FLOOR_PCT and not allow_calendar_ceiling:
        reasons.append(
            f"precondition (a) unmet: coverage {coverage}% < {COVERAGE_FLOOR_PCT}% "
            "(flip below floor requires the 30-day calendar ceiling; pass allow_calendar_ceiling=True to quarantine the long tail)"
        )

    # (b) shadow window — advisory; only surfaces as a reason if clearly unmet.
    days = pre.get("shadow_days_complete")
    deviation = pre.get("shadow_deviation_pct")
    if days is not None and days < SHADOW_MIN_DAYS:
        reasons.append(f"precondition (b) unmet: shadow window {days}d < {SHADOW_MIN_DAYS}d")
    if deviation is not None and deviation >= SHADOW_MAX_DEVIATION_PCT:
        reasons.append(f"precondition (b) unmet: shadow deviation {deviation}% >= {SHADOW_MAX_DEVIATION_PCT}%")

    return TransitionDecision(
        allowed=not reasons,
        from_state=from_state,
        event=FLIP_EVENT,
        to_state=to_state if not reasons else None,
        reasons=tuple(reasons),
    )


def _can_enter_ready_to_flip(state_machine: dict) -> list[str]:
    """SHADOW-MODE -> READY-TO-FLIP guard: no open P0 (open-P0 deviations route
    to HOLDING per the § 14.4.shadow diagram, not to READY-TO-FLIP)."""
    pre = _coerce_preconditions(state_machine)
    open_p0 = pre.get("open_p0_count")
    if open_p0 is None:
        return ["dispositions-resolved requires open_p0_count == 0 (unknown); route open-P0 deviations to HOLDING"]
    if open_p0 != 0:
        return [
            f"dispositions-resolved blocked: {open_p0} open P0 issue(s) — route to HOLDING (deviations-open-p0), not READY-TO-FLIP"
        ]
    return []


# ── Core evaluation ──────────────────────────────────────────────────────────


def evaluate(
    state_machine: dict,
    event: str,
    *,
    allow_calendar_ceiling: bool = False,
) -> TransitionDecision:
    """Evaluate whether `event` is a legal, precondition-satisfied transition
    out of state_machine['current_state']. Pure — never mutates input."""
    from_state = state_machine.get("current_state")

    if from_state not in STATES:
        return TransitionDecision(
            allowed=False,
            from_state=str(from_state),
            event=event,
            to_state=None,
            reasons=(f"unknown current_state {from_state!r} (not in the lifecycle)",),
        )

    key = (from_state, event)
    if key not in LEGAL_TRANSITIONS:
        legal_events = sorted(e for (s, e) in LEGAL_TRANSITIONS if s == from_state)
        return TransitionDecision(
            allowed=False,
            from_state=from_state,
            event=event,
            to_state=None,
            reasons=(
                f"illegal transition: event {event!r} is not legal from state {from_state!r} "
                f"(legal events from here: {legal_events or 'none — terminal-ish state'})",
            ),
        )

    to_state = LEGAL_TRANSITIONS[key]

    # Precondition gates layered on top of the legal-edge check.
    if event == FLIP_EVENT:
        decision = can_flip(state_machine, allow_calendar_ceiling=allow_calendar_ceiling)
        # can_flip already encodes from_state == READY-TO-FLIP + the gates.
        return decision

    if (from_state, event) == ("SHADOW-MODE", "dispositions-resolved"):
        reasons = _can_enter_ready_to_flip(state_machine)
        if reasons:
            return TransitionDecision(
                allowed=False, from_state=from_state, event=event, to_state=None, reasons=tuple(reasons)
            )

    return TransitionDecision(allowed=True, from_state=from_state, event=event, to_state=to_state)


def emit(
    state: dict,
    event: str,
    *,
    at: str,
    reason: str | None = None,
    decision_record_ref: str | None = None,
    allow_calendar_ceiling: bool = False,
) -> dict:
    """Apply a transition and return a NEW state dict (deep-copied; input is
    never mutated). Raises TransitionError if the transition is rejected.

    The returned state has:
      - state_machine.current_state set to the new state
      - state_machine.entered_at set to `at`
      - a transition record appended to state_machine.transition_history
    """
    if "state_machine" not in state or not isinstance(state["state_machine"], dict):
        raise TransitionError(
            TransitionDecision(
                allowed=False,
                from_state="<missing>",
                event=event,
                to_state=None,
                reasons=("state has no 'state_machine' object",),
            )
        )

    sm = state["state_machine"]
    decision = evaluate(sm, event, allow_calendar_ceiling=allow_calendar_ceiling)
    if decision.rejected:
        raise TransitionError(decision)

    new_state = copy.deepcopy(state)
    new_sm = new_state["state_machine"]
    record = {
        "from": decision.from_state,
        "to": decision.to_state,
        "event": event,
        "at": at,
        "reason": reason,
        "decision_record_ref": decision_record_ref,
    }
    new_sm["current_state"] = decision.to_state
    new_sm["entered_at"] = at
    history = new_sm.get("transition_history")
    if not isinstance(history, list):
        history = []
    history.append(record)
    new_sm["transition_history"] = history
    return new_state


# ── Schema validation ────────────────────────────────────────────────────────


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def validate_state_file(state_path: str, schema_path: str = SCHEMA_PATH) -> list[str]:
    """Validate a SAK-STATE.json against the sak-state schema. Returns a list of
    human-readable error strings (empty == valid)."""
    try:
        import jsonschema
    except ImportError:  # pragma: no cover - environment guard
        return ["jsonschema not installed (pip install jsonschema)"]

    schema = _load_json(schema_path)
    doc = _load_json(state_path)
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    out = []
    for err in errors:
        loc = "/".join(str(p) for p in err.path) or "<root>"
        out.append(f"{loc}: {err.message}")
    return out


# ── CLI ──────────────────────────────────────────────────────────────────────


def _print_table() -> None:
    print("SAK Phase-4 flip — legal transitions (from --event--> to):")
    for (frm, ev), to in LEGAL_TRANSITIONS.items():
        gate = "  [HARD-GATED]" if ev == FLIP_EVENT else ""
        print(f"  {frm:>14}  --{ev}-->  {to}{gate}")


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_state_file(args.state, args.schema)
    if errors:
        print(f"sak-state-machine --validate: FAIL — {args.state} does not satisfy {args.schema}:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"sak-state-machine --validate: OK — {args.state} satisfies {args.schema}")
    return 0


def cmd_self_test() -> int:  # noqa: C901 - linear self-test, readability over decomposition
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        if condition:
            print(f"self-test ok: {label}")
        else:
            print(f"self-test FAIL: {label}")
            failures += 1

    # ── Fixtures (no I/O; pure dicts) ─────────────────────────────────────────
    def sm(state: str, **pre_overrides: object) -> dict:
        """Build a minimal state_machine dict at `state` with full sign-off +
        clean preconditions, then apply overrides into preconditions."""
        pre = {
            "coverage_corpus_pass_pct": 99.9,
            "shadow_days_complete": 10,
            "shadow_deviation_pct": 0.1,
            "open_p0_count": 0,
            "governance_signoff": {"cto": True, "ciso": True, "vp_devrel": True, "decision_record_ref": "044-AT-DECR"},
        }
        pre.update(pre_overrides)
        return {
            "machine": "SAK advisory -> blocking flip (Phase 4)",
            "current_state": state,
            "states": list(STATES),
            "preconditions": pre,
        }

    # 1. Graph integrity: every transition value is a known state.
    check("every transition target is a known state", all(to in STATES for to in LEGAL_TRANSITIONS.values()))
    check("every transition source is a known state", all(frm in STATES for (frm, _ev) in LEGAL_TRANSITIONS))

    # 2. The prompt's named lifecycle edges all exist.
    named_path = [
        ("ADVISORY", "wave-a-merged", "ADVISORY-W-A"),
        ("ADVISORY-W-A", "wave-b-done", "ADVISORY-W-AB"),
        ("ADVISORY-W-AB", "enable-shadow", "SHADOW-MODE"),
        ("SHADOW-MODE", "dispositions-resolved", "READY-TO-FLIP"),
        ("READY-TO-FLIP", FLIP_EVENT, "BLOCKING"),
    ]
    check(
        "the canonical forward path edges all exist",
        all(LEGAL_TRANSITIONS.get((f, e)) == t for f, e, t in named_path),
    )

    # 3. Legal transition passes.
    d = evaluate(sm("ADVISORY"), "wave-a-merged")
    check(
        "legal transition ADVISORY --wave-a-merged--> ADVISORY-W-A passes", d.allowed and d.to_state == "ADVISORY-W-A"
    )

    # 4. Illegal transition rejected (event not legal from this state).
    d = evaluate(sm("ADVISORY"), "governance-triple-signs")
    check("illegal transition rejected (flip from ADVISORY)", d.rejected and "illegal transition" in d.reasons[0])

    # 5. Illegal transition rejected (unknown event).
    d = evaluate(sm("SHADOW-MODE"), "teleport")
    check("unknown event rejected from SHADOW-MODE", d.rejected)

    # 6. Flip with all preconditions met passes.
    d = evaluate(sm("READY-TO-FLIP"), FLIP_EVENT)
    check("flip passes with coverage+zero-P0+full-signoff", d.allowed and d.to_state == "BLOCKING")

    # 7. Flip with an OPEN P0 rejected (HARD gate (c)).
    d = evaluate(sm("READY-TO-FLIP", open_p0_count=1), FLIP_EVENT)
    check("flip rejected with 1 open P0 (hard gate c)", d.rejected and any("(c)" in r for r in d.reasons))

    # 8. Open-P0 flip rejected EVEN WITH calendar ceiling (ceiling never overrides c).
    d = evaluate(sm("READY-TO-FLIP", open_p0_count=2), FLIP_EVENT, allow_calendar_ceiling=True)
    check("calendar ceiling does NOT override open-P0 hard gate", d.rejected and any("(c)" in r for r in d.reasons))

    # 9. Flip with incomplete governance sign-off rejected (HARD gate (d)).
    s = sm("READY-TO-FLIP")
    s["preconditions"]["governance_signoff"]["vp_devrel"] = False
    d = evaluate(s, FLIP_EVENT)
    check(
        "flip rejected with missing VP-DevRel sign-off (hard gate d)", d.rejected and any("(d)" in r for r in d.reasons)
    )

    # 10. Sub-floor coverage rejected without ceiling; permitted with ceiling.
    d_no = evaluate(sm("READY-TO-FLIP", coverage_corpus_pass_pct=98.0), FLIP_EVENT)
    d_yes = evaluate(sm("READY-TO-FLIP", coverage_corpus_pass_pct=98.0), FLIP_EVENT, allow_calendar_ceiling=True)
    check("coverage < 99.5% rejected without calendar ceiling", d_no.rejected and any("(a)" in r for r in d_no.reasons))
    check("coverage < 99.5% permitted WITH calendar ceiling (quarantine long tail)", d_yes.allowed)

    # 11. SHADOW-MODE -> READY-TO-FLIP requires zero open P0; open-P0 routes to HOLDING.
    d = evaluate(sm("SHADOW-MODE", open_p0_count=1), "dispositions-resolved")
    check("dispositions-resolved blocked with open P0", d.rejected)
    d = evaluate(sm("SHADOW-MODE", open_p0_count=1), "deviations-open-p0")
    check("deviations-open-p0 routes SHADOW-MODE -> HOLDING with open P0", d.allowed and d.to_state == "HOLDING")

    # 12. Rollback reachable from each gated state.
    for frm, ev in (
        ("ADVISORY-W-A", "wave-a-failure"),
        ("ADVISORY-W-AB", "wave-b-failure"),
        ("BLOCKING", "regression-detected"),
    ):
        d = evaluate(sm(frm), ev)
        check(f"ROLLED-BACK reachable from {frm} via {ev}", d.allowed and d.to_state == "ROLLED-BACK")
    rollback_sources = {f for (f, _e), t in LEGAL_TRANSITIONS.items() if t == "ROLLED-BACK"}
    check("every gated state can reach ROLLED-BACK", rollback_sources == set(GATED_STATES))

    # 13. ROLLED-BACK returns to SHADOW-MODE (diagram: "back to SHADOW").
    d = evaluate(sm("ROLLED-BACK"), "back-to-shadow")
    check("ROLLED-BACK --back-to-shadow--> SHADOW-MODE", d.allowed and d.to_state == "SHADOW-MODE")

    # 14. emit() is non-mutating and appends history.
    before = sm("ADVISORY")
    snapshot = json.dumps(before, sort_keys=True)
    new = emit({"state_machine": before}, "wave-a-merged", at="2026-07-01")
    check("emit does not mutate the input state_machine", json.dumps(before, sort_keys=True) == snapshot)
    check("emit advances current_state", new["state_machine"]["current_state"] == "ADVISORY-W-A")
    check("emit sets entered_at", new["state_machine"]["entered_at"] == "2026-07-01")
    check("emit appends exactly one history record", len(new["state_machine"]["transition_history"]) == 1)
    check(
        "emit history record is well-formed",
        new["state_machine"]["transition_history"][0]
        == {
            "from": "ADVISORY",
            "to": "ADVISORY-W-A",
            "event": "wave-a-merged",
            "at": "2026-07-01",
            "reason": None,
            "decision_record_ref": None,
        },
    )

    # 15. emit() raises on a rejected transition.
    try:
        emit({"state_machine": sm("READY-TO-FLIP", open_p0_count=3)}, FLIP_EVENT, at="2026-07-01")
        check("emit raises TransitionError on rejected flip", False)
    except TransitionError as exc:
        check("emit raises TransitionError on rejected flip", any("(c)" in r for r in exc.decision.reasons))

    # 16. Full happy-path walk ADVISORY -> BLOCKING via emit() chains cleanly.
    state = {"state_machine": sm("ADVISORY")}
    chain = [
        ("wave-a-merged", "ADVISORY-W-A"),
        ("wave-b-done", "ADVISORY-W-AB"),
        ("enable-shadow", "SHADOW-MODE"),
        ("dispositions-resolved", "READY-TO-FLIP"),
        (FLIP_EVENT, "BLOCKING"),
    ]
    walk_ok = True
    for ev, expect in chain:
        try:
            state = emit(state, ev, at="2026-07-01")
            walk_ok = walk_ok and state["state_machine"]["current_state"] == expect
        except TransitionError:
            walk_ok = False
    check("full ADVISORY->BLOCKING happy-path walk via emit()", walk_ok)
    check("happy-path walk recorded 5 history entries", len(state["state_machine"]["transition_history"]) == 5)

    # 17. Schema validation: the committed SAK-STATE.json is schema-valid.
    if os.path.exists(DEFAULT_STATE) and os.path.exists(SCHEMA_PATH):
        errs = validate_state_file(DEFAULT_STATE, SCHEMA_PATH)
        check("committed SAK-STATE.json validates against the schema", errs == [])

    print()
    if failures:
        print(f"self-test: {failures} FAILURE(S).")
        return 1
    print(
        "self-test: legal/illegal transitions, hard-gate preconditions, rollback, emit immutability, and schema validation all sound."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SAK Phase-4 advisory->blocking flip state machine.")
    parser.add_argument("--self-test", action="store_true", help="run the deterministic offline self-test (CI gate)")
    parser.add_argument(
        "--validate", action="store_true", help="jsonschema-validate a SAK-STATE.json against the schema"
    )
    parser.add_argument("--show", action="store_true", help="print the legal-transition table")
    parser.add_argument("--state", default=DEFAULT_STATE, help="path to SAK-STATE.json (for --validate)")
    parser.add_argument("--schema", default=SCHEMA_PATH, help="path to the sak-state schema (for --validate)")
    args = parser.parse_args(argv)

    if args.self_test:
        return cmd_self_test()
    if args.validate:
        return cmd_validate(args)
    if args.show:
        _print_table()
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
