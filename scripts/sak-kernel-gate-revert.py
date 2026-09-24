#!/usr/bin/env python3
"""SAK Phase-4c rollback protocol — ``kernel-gate-revert`` command.

The rollback half of the SAK advisory->blocking flip lifecycle (plan 033 v7
§ 14.4.rollback class 3 + plan 048 v8 § 14.4c). This command reverts a SAK gate
from a gated/BLOCKING state back toward advisory by driving the Phase-4 state
machine (``scripts/sak-state-machine.py``) to ``ROLLED-BACK`` via its existing
``evaluate()`` / ``emit()`` engine and the governance-sign-off seam
(``load_signoff_from_state``). It does NOT reimplement any state/transition
logic — the state machine remains the single source of the legal-transition
graph and the hard gates.

Normative authority (all in 000-docs/):
  - plan 033 v7 § 14.4.rollback class 3 — the post-flip-regression rollback:
    governance triple authorizes a single ``kernel-gate-revert <reason>`` command
    that (a) flips the validator back to advisory mode, (b) records a Decision
    Record (``AT-DECR-phase-4c-rollback-NNN``), (c) emits a kernel-side Evidence
    Bundle row marking the BLOCKING-window attestations
    ``signing_mode: rolled-back-superseded``, and (d) opens an ISEDC Class-2
    retrospective session within 7 calendar days.
  - plan 048 v8 § 14.4c / Delta 3 — the governance-triple (CTO + CISO + VP-DevRel)
    sign-off rule for the advisory->blocking flip; the same triple authorizes its
    rollback.
  - doc 092-AT-SPEC — documents the state machine this command drives.

What this command owns vs. what it does not:
  - OWNS (a) the state transition to ``ROLLED-BACK`` (the in-repo "flip back to
    advisory" half), the governance-triple gate, the revert reason/target record,
    and (d) stamping the 7-day ISEDC Class-2 ``retrospective_due_at`` deadline.
  - DOES NOT own (c) the kernel-side Evidence Bundle ``rolled-back-superseded``
    superseding-envelope event — that is owned by the kernel-side emitter per
    § 14.4.rollback / F-MK-005 (Rekor is append-only; rollback supersedes, never
    mutates). This command records the *intent* (the affected window + a flag)
    in the transition record so the kernel emitter can act on it, but it never
    touches Rekor.

GOVERNANCE SIGN-OFF SOURCE IS STUBBED (same seam vyng stubbed): the three
booleans are read via the state machine's ``load_signoff_from_state()`` from
``SAK-STATE.json``'s ``state_machine.preconditions.governance_signoff``. A real
governance-signoff source (an ISEDC AT-DECR ledger, a signing service) would
replace that single function. The optional ``--signoff cto,ciso,vp_devrel`` CLI
flag is an OFFLINE override used by ``--self-test``/``--dry-run`` and operators
who carry the sign-off out of band; absent it, the seam is the sole source.

The module is import-safe and offline. The CLI exposes:
    --self-test                 deterministic offline self-test (CI gate)
    --dry-run                   evaluate a revert without writing (prints the plan)
    --revert                    perform the revert; writes the new state to --out
    --check-retrospective       surface whether a stamped retrospective is overdue

No network. Writes only when ``--revert`` is given with an explicit ``--out``.
"""

from __future__ import annotations

import argparse
import copy
import datetime as _dt
import importlib.util
import json
import os
import sys
from dataclasses import dataclass, field
from types import ModuleType

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STATE = os.path.join(REPO_ROOT, "SAK-STATE.json")
STATE_MACHINE_PATH = os.path.join(REPO_ROOT, "scripts", "sak-state-machine.py")

#: The ISEDC Class-2 retrospective must be opened within this many calendar days
#: of the revert (plan 033 § 14.4.rollback class 3 (d)).
RETROSPECTIVE_WINDOW_DAYS = 7

#: The event that drives BLOCKING -> ROLLED-BACK in the state machine. The
#: state machine owns this name; we reference it rather than re-declare it.
REGRESSION_EVENT = "regression-detected"

#: The three governance seats whose sign-off authorizes a revert (plan 048 § 14.4c).
GOVERNANCE_SEATS: tuple[str, ...] = ("cto", "ciso", "vp_devrel")


# ── State-machine engine loader (reuse, never reimplement) ───────────────────


def load_state_machine_module(path: str = STATE_MACHINE_PATH) -> ModuleType:
    """Load ``scripts/sak-state-machine.py`` by file path.

    The scripts directory uses hyphenated filenames, so the module is not
    importable by name; load it by path the same way ``scripts/tests/conftest.py``
    does. This is the engine: we drive its ``evaluate``/``emit`` and reuse its
    ``load_signoff_from_state`` seam.
    """
    spec = importlib.util.spec_from_file_location("sak_state_machine", path)
    if spec is None or spec.loader is None:  # pragma: no cover - import guard
        raise RuntimeError(f"cannot load state machine module at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("sak_state_machine", module)
    spec.loader.exec_module(module)
    return module


# ── Result type ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class RevertDecision:
    """The outcome of evaluating a requested revert."""

    allowed: bool
    from_state: str
    to_state: str | None
    reasons: tuple[str, ...] = field(default_factory=tuple)
    missing_signoff: tuple[str, ...] = field(default_factory=tuple)

    @property
    def rejected(self) -> bool:
        return not self.allowed


class RevertError(Exception):
    """Raised by ``perform_revert`` when a revert is rejected."""

    def __init__(self, decision: RevertDecision):
        self.decision = decision
        super().__init__("; ".join(decision.reasons) or "revert rejected")


# ── Governance gate ──────────────────────────────────────────────────────────


def resolve_signoff(
    ssm: ModuleType,
    state_machine: dict,
    *,
    override: dict | None = None,
) -> dict:
    """Resolve the governance triple sign-off.

    Default source is the state machine's ``load_signoff_from_state`` seam (the
    same seam the flip uses). ``override`` — an offline/out-of-band sign-off map
    like ``{"cto": True, "ciso": True, "vp_devrel": True}`` — wins when provided
    (used by ``--signoff`` / ``--self-test``). Replacing ``load_signoff_from_state``
    with a live governance-signoff source is the only change a real source needs.
    """
    signoff = ssm.load_signoff_from_state(state_machine)
    if override:
        merged = dict(signoff)
        for seat in GOVERNANCE_SEATS:
            if seat in override:
                merged[seat] = bool(override[seat])
        return merged
    return signoff


def missing_governance_seats(signoff: dict) -> tuple[str, ...]:
    """The governance seats whose sign-off is absent (in canonical order)."""
    return tuple(seat for seat in GOVERNANCE_SEATS if not signoff.get(seat))


# ── Core evaluation ──────────────────────────────────────────────────────────


def evaluate_revert(
    ssm: ModuleType,
    state_machine: dict,
    *,
    signoff_override: dict | None = None,
) -> RevertDecision:
    """Evaluate whether a revert (-> ``ROLLED-BACK``) is allowed.

    Two independent gates, both required:
      1. The governance triple (CTO + CISO + VP-DevRel) must ALL be present —
         refuse with the missing seats named otherwise (plan 048 § 14.4c).
      2. The state machine must allow the rollback edge out of the current state
         (legal-transition check, delegated to ``ssm.evaluate`` — the engine,
         not a reimplementation). Reverting from an illegal source state (e.g.
         ``ADVISORY``, which has no rollback edge) is rejected with the engine's
         own reason.

    Pure — never mutates input.
    """
    from_state = state_machine.get("current_state")
    reasons: list[str] = []

    # Gate 1 — governance triple (refuse if ANY seat absent).
    signoff = resolve_signoff(ssm, state_machine, override=signoff_override)
    missing = missing_governance_seats(signoff)
    if missing:
        pretty = {"cto": "CTO", "ciso": "CISO", "vp_devrel": "VP-DevRel"}
        named = ", ".join(pretty[m] for m in missing)
        reasons.append(
            f"governance-triple sign-off incomplete: revert refused (missing: {named}). "
            "All three of CTO + CISO + VP-DevRel must sign off to authorize a kernel-gate-revert "
            "(plan 048 § 14.4c)."
        )

    # Gate 2 — the state machine must permit the rollback edge from here.
    sm_decision = ssm.evaluate(state_machine, REGRESSION_EVENT)
    to_state = sm_decision.to_state if sm_decision.allowed else None
    if not sm_decision.allowed:
        # Surface the engine's own reason verbatim so an illegal source state
        # (no rollback edge) is rejected with a clear, engine-authored message.
        reasons.extend(sm_decision.reasons)
    elif sm_decision.to_state != "ROLLED-BACK":  # pragma: no cover - defensive
        reasons.append(
            f"unexpected rollback target {sm_decision.to_state!r} (expected ROLLED-BACK) from state {from_state!r}"
        )

    return RevertDecision(
        allowed=not reasons,
        from_state=str(from_state),
        to_state=to_state if not reasons else None,
        reasons=tuple(reasons),
        missing_signoff=missing,
    )


def _retrospective_due_at(at: str) -> str:
    """``at`` (an ISO date ``YYYY-MM-DD``) + the 7-day window, as an ISO date.

    The deadline is calendar-day based per plan 033 § 14.4.rollback class 3 (d)
    ("within 7 calendar days"). ``at`` is parsed as a date; a date-time ``at``
    is truncated to its date for the deadline (the window is calendar-day, not
    second-precise).
    """
    date_part = at.split("T", 1)[0]
    base = _dt.date.fromisoformat(date_part)
    due = base + _dt.timedelta(days=RETROSPECTIVE_WINDOW_DAYS)
    return due.isoformat()


def perform_revert(
    ssm: ModuleType,
    state: dict,
    *,
    at: str,
    reason: str,
    reverted_gate: str,
    reverted_version: str | None = None,
    decision_record_ref: str | None = None,
    signoff_override: dict | None = None,
    affected_window: dict | None = None,
) -> dict:
    """Drive the gate to ``ROLLED-BACK`` and return a NEW state dict.

    Reuses the state machine's ``emit()`` (deep-copies; input never mutated;
    history appended) for the transition, then stamps the Phase-4c rollback
    metadata onto the new state:

      - ``state_machine.rollback`` — the revert record: ``reason``,
        ``reverted_gate``, ``reverted_version``, ``reverted_at`` and the
        ``retrospective_due_at`` = ``at`` + 7 calendar days (the ISEDC Class-2
        deadline, plan 033 § 14.4.rollback class 3 (d)).
      - ``affected_window`` (optional) is recorded for the kernel-side emitter to
        mark BLOCKING-window attestations ``rolled-back-superseded`` (this
        command records the intent; it never touches Rekor — that envelope event
        is owned by the kernel emitter per § 14.4.rollback / F-MK-005).

    Raises ``RevertError`` if the governance gate or the legal-transition check
    rejects the revert.
    """
    if "state_machine" not in state or not isinstance(state["state_machine"], dict):
        raise RevertError(
            RevertDecision(
                allowed=False,
                from_state="<missing>",
                to_state=None,
                reasons=("state has no 'state_machine' object",),
            )
        )
    if not reason or not reason.strip():
        raise RevertError(
            RevertDecision(
                allowed=False,
                from_state=str(state["state_machine"].get("current_state")),
                to_state=None,
                reasons=("a revert reason is required (plan 033 § 14.4.rollback records the reason)",),
            )
        )

    sm = state["state_machine"]
    decision = evaluate_revert(ssm, sm, signoff_override=signoff_override)
    if decision.rejected:
        raise RevertError(decision)

    # Drive the transition through the engine (non-mutating; appends history).
    new_state = ssm.emit(
        state,
        REGRESSION_EVENT,
        at=at,
        reason=reason,
        decision_record_ref=decision_record_ref,
    )

    new_sm = new_state["state_machine"]
    signoff = resolve_signoff(ssm, sm, override=signoff_override)
    rollback_record: dict = {
        "reverted_at": at,
        "reason": reason,
        "reverted_gate": reverted_gate,
        "reverted_version": reverted_version,
        "from_state": decision.from_state,
        "to_state": new_sm["current_state"],
        "decision_record_ref": decision_record_ref,
        "governance_signoff": {seat: bool(signoff.get(seat)) for seat in GOVERNANCE_SEATS},
        "retrospective_due_at": _retrospective_due_at(at),
        "retrospective_window_days": RETROSPECTIVE_WINDOW_DAYS,
        "retrospective_class": "ISEDC-Class-2",
    }
    if affected_window is not None:
        # Recorded intent only — the kernel-side emitter acts on this to mark
        # the BLOCKING-window attestations rolled-back-superseded. NOT a Rekor write.
        rollback_record["affected_window"] = copy.deepcopy(affected_window)
        rollback_record["superseding_signing_mode"] = "rolled-back-superseded"
    new_sm["rollback"] = rollback_record
    return new_state


# ── Retrospective-overdue surfacing ──────────────────────────────────────────


@dataclass(frozen=True)
class RetrospectiveStatus:
    """Whether a stamped ISEDC Class-2 retrospective is overdue."""

    present: bool
    due_at: str | None
    as_of: str | None
    overdue: bool
    days_remaining: int | None

    @property
    def verdict(self) -> str:
        if not self.present:
            return "NONE"
        return "OVERDUE" if self.overdue else "PENDING"


def check_retrospective(state: dict, *, as_of: str | None = None) -> RetrospectiveStatus:
    """Surface whether a stamped ``retrospective_due_at`` is past.

    Symmetric to how the detector-health / lineage-liveness scripts surface
    overdue items: read-only, deterministic, no network. ``as_of`` defaults to
    today's date (UTC) when not pinned.
    """
    rollback = (state.get("state_machine") or {}).get("rollback") or {}
    due_at = rollback.get("retrospective_due_at")
    if not due_at:
        return RetrospectiveStatus(present=False, due_at=None, as_of=as_of, overdue=False, days_remaining=None)

    today = as_of or _dt.datetime.now(_dt.UTC).date().isoformat()
    due = _dt.date.fromisoformat(due_at.split("T", 1)[0])
    now = _dt.date.fromisoformat(today.split("T", 1)[0])
    days_remaining = (due - now).days
    return RetrospectiveStatus(
        present=True,
        due_at=due_at,
        as_of=today,
        overdue=now > due,
        days_remaining=days_remaining,
    )


# ── I/O helpers ──────────────────────────────────────────────────────────────


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _parse_signoff_flag(value: str | None) -> dict | None:
    """Parse ``--signoff cto,ciso,vp_devrel`` into an override map.

    Only the listed seats are set True; unlisted seats are left to the seam
    (so ``--signoff cto`` proves a single-seat carry, with ciso/vp_devrel still
    sourced from SAK-STATE.json). ``--signoff none`` => empty override (all from
    seam). An unknown seat name is an error.
    """
    if value is None:
        return None
    raw = [s.strip().lower() for s in value.split(",") if s.strip()]
    if raw == ["none"] or raw == []:
        return {}
    override: dict = {}
    for seat in raw:
        if seat not in GOVERNANCE_SEATS:
            raise ValueError(f"unknown governance seat {seat!r} (expected one of {', '.join(GOVERNANCE_SEATS)})")
        override[seat] = True
    return override


# ── CLI ──────────────────────────────────────────────────────────────────────


def cmd_dry_run(ssm: ModuleType, args: argparse.Namespace) -> int:
    state = _load_json(args.state)
    sm = state.get("state_machine") or {}
    override = _parse_signoff_flag(args.signoff)
    decision = evaluate_revert(ssm, sm, signoff_override=override)
    print(f"kernel-gate-revert --dry-run against {args.state}")
    print(f"  current_state : {sm.get('current_state')!r}")
    if decision.allowed:
        due = _retrospective_due_at(args.at)
        print(f"  decision      : ALLOWED -> {decision.to_state}")
        print(f"  reverted_gate : {args.gate}")
        print(f"  reason        : {args.reason}")
        print(f"  retrospective : ISEDC Class-2 due by {due} (revert_at {args.at} + {RETROSPECTIVE_WINDOW_DAYS}d)")
        return 0
    print("  decision      : REJECTED")
    for r in decision.reasons:
        print(f"    - {r}")
    return 1


def cmd_revert(ssm: ModuleType, args: argparse.Namespace) -> int:
    state = _load_json(args.state)
    override = _parse_signoff_flag(args.signoff)
    try:
        new_state = perform_revert(
            ssm,
            state,
            at=args.at,
            reason=args.reason,
            reverted_gate=args.gate,
            reverted_version=args.version,
            decision_record_ref=args.decision_record_ref,
            signoff_override=override,
        )
    except RevertError as exc:
        print("kernel-gate-revert: REJECTED")
        for r in exc.decision.reasons:
            print(f"  - {r}")
        return 1

    rb = new_state["state_machine"]["rollback"]
    out = args.out
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(new_state, fh, indent=2)
            fh.write("\n")
        print(f"kernel-gate-revert: OK — {rb['from_state']} -> {rb['to_state']}; new state written to {out}")
    else:
        print(f"kernel-gate-revert: OK — {rb['from_state']} -> {rb['to_state']} (no --out; state not written)")
    print(f"  reason        : {rb['reason']}")
    print(f"  reverted_gate : {rb['reverted_gate']}")
    print(f"  retrospective : ISEDC Class-2 due by {rb['retrospective_due_at']}")
    return 0


def cmd_check_retrospective(args: argparse.Namespace) -> int:
    state = _load_json(args.state)
    status = check_retrospective(state, as_of=args.as_of)
    if not status.present:
        print(f"retrospective: NONE — no rollback recorded in {args.state} (no retrospective deadline to track)")
        return 0
    if status.overdue:
        print(
            f"retrospective: OVERDUE — ISEDC Class-2 retrospective was due {status.due_at} "
            f"(as of {status.as_of}, {-status.days_remaining}d past). Open it now (plan 033 § 14.4.rollback class 3 (d))."
        )
        return 1
    print(
        f"retrospective: PENDING — ISEDC Class-2 retrospective due {status.due_at} "
        f"({status.days_remaining}d remaining as of {status.as_of})."
    )
    return 0


def cmd_self_test(ssm: ModuleType) -> int:  # noqa: C901 - linear self-test, readability over decomposition
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        if condition:
            print(f"self-test ok: {label}")
        else:
            print(f"self-test FAIL: {label}")
            failures += 1

    full = {"cto": True, "ciso": True, "vp_devrel": True}

    def state(current: str, signoff: dict | None = None) -> dict:
        pre: dict = {
            "coverage_corpus_pass_pct": 99.9,
            "shadow_days_complete": 10,
            "shadow_deviation_pct": 0.1,
            "open_p0_count": 0,
            "governance_signoff": {
                "cto": False,
                "ciso": False,
                "vp_devrel": False,
                "decision_record_ref": None,
            },
        }
        if signoff:
            pre["governance_signoff"].update(signoff)
        return {
            "state_version": "sak-state/v1",
            "state_machine": {
                "machine": "SAK advisory -> blocking flip (Phase 4)",
                "current_state": current,
                "states": list(ssm.STATES),
                "preconditions": pre,
            },
        }

    # 1. Revert with full triple sign-off from BLOCKING succeeds -> ROLLED-BACK.
    d = evaluate_revert(ssm, state("BLOCKING", full)["state_machine"])
    check(
        "revert from BLOCKING with full triple sign-off is ALLOWED -> ROLLED-BACK",
        d.allowed and d.to_state == "ROLLED-BACK",
    )

    # 2. perform_revert reaches ROLLED-BACK and stamps retrospective_due_at = +7d.
    new = perform_revert(
        ssm,
        state("BLOCKING", full),
        at="2026-08-01",
        reason="BLOCKING broke real PRs at high rate",
        reverted_gate="validate-plugins.yml",
        reverted_version="authoring/v1",
        decision_record_ref="AT-DECR-phase-4c-rollback-001",
    )
    rb = new["state_machine"]["rollback"]
    check("perform_revert reaches ROLLED-BACK", new["state_machine"]["current_state"] == "ROLLED-BACK")
    check("retrospective_due_at is revert_at + 7 calendar days", rb["retrospective_due_at"] == "2026-08-08")
    check("retrospective is tagged ISEDC Class-2", rb["retrospective_class"] == "ISEDC-Class-2")
    check("rollback record carries the reverted gate", rb["reverted_gate"] == "validate-plugins.yml")
    check("rollback record carries the reason", rb["reason"] == "BLOCKING broke real PRs at high rate")
    check("transition_history appended exactly one entry", len(new["state_machine"]["transition_history"]) == 1)

    # 3. Each missing seat is rejected with that seat named.
    for seat, pretty in (("cto", "CTO"), ("ciso", "CISO"), ("vp_devrel", "VP-DevRel")):
        partial = {s: True for s in GOVERNANCE_SEATS if s != seat}
        d = evaluate_revert(ssm, state("BLOCKING", partial)["state_machine"])
        check(
            f"revert REJECTED when {pretty} sign-off absent (and {pretty} is named)",
            d.rejected and seat in d.missing_signoff and any(pretty in r for r in d.reasons),
        )

    # 4. No sign-off at all is rejected with all three named.
    d = evaluate_revert(ssm, state("BLOCKING")["state_machine"])
    check(
        "revert REJECTED with zero sign-off (all three missing)",
        d.rejected and set(d.missing_signoff) == set(GOVERNANCE_SEATS),
    )

    # 5. Sign-off seam is honoured: SAK-STATE-style governance_signoff drives it.
    d_seam = evaluate_revert(ssm, state("BLOCKING", full)["state_machine"], signoff_override=None)
    check("governance gate reads the load_signoff_from_state seam", d_seam.allowed)

    # 6. Revert from an ILLEGAL source state (ADVISORY — no rollback edge) rejected,
    #    even WITH full sign-off, via the engine's own legal-transition check.
    d = evaluate_revert(ssm, state("ADVISORY", full)["state_machine"])
    check(
        "revert from ADVISORY rejected (no rollback edge) even with full sign-off",
        d.rejected and any("illegal transition" in r for r in d.reasons),
    )

    # 7. perform_revert raises RevertError on a missing-seat revert.
    try:
        perform_revert(
            ssm, state("BLOCKING", {"cto": True, "ciso": True}), at="2026-08-01", reason="x", reverted_gate="g"
        )
        check("perform_revert raises RevertError on incomplete sign-off", False)
    except RevertError as exc:
        check("perform_revert raises RevertError on incomplete sign-off", "vp_devrel" in exc.decision.missing_signoff)

    # 8. perform_revert refuses an empty reason.
    try:
        perform_revert(ssm, state("BLOCKING", full), at="2026-08-01", reason="   ", reverted_gate="g")
        check("perform_revert refuses an empty reason", False)
    except RevertError:
        check("perform_revert refuses an empty reason", True)

    # 9. perform_revert is non-mutating on its input.
    src = state("BLOCKING", full)
    snapshot = json.dumps(src, sort_keys=True)
    _ = perform_revert(ssm, src, at="2026-08-01", reason="r", reverted_gate="g")
    check("perform_revert does not mutate its input state", json.dumps(src, sort_keys=True) == snapshot)

    # 10. affected_window intent is recorded for the kernel emitter (no Rekor write here).
    new_w = perform_revert(
        ssm,
        state("BLOCKING", full),
        at="2026-08-01",
        reason="r",
        reverted_gate="g",
        affected_window={"from": "2026-07-20", "to": "2026-08-01"},
    )
    rbw = new_w["state_machine"]["rollback"]
    check(
        "affected_window recorded for the kernel emitter",
        rbw.get("affected_window") == {"from": "2026-07-20", "to": "2026-08-01"},
    )
    check(
        "superseding signing_mode intent is rolled-back-superseded",
        rbw.get("superseding_signing_mode") == "rolled-back-superseded",
    )

    # 11. The full emitted ROLLED-BACK state — INCLUDING the rollback block —
    #     validates against the sak-state schema (the schema's stateMachine.rollback
    #     def accepts the Phase-4c rollback record).
    if os.path.exists(ssm.SCHEMA_PATH):
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump(new, fh)
            tmp = fh.name
        errs = ssm.validate_state_file(tmp, ssm.SCHEMA_PATH)
        os.unlink(tmp)
        check("full emitted ROLLED-BACK state (incl. rollback block) validates against sak-state schema", errs == [])

    # 12. Rollback transition_history entry is schema-shaped (from/to/event/at present).
    rec = new["state_machine"]["transition_history"][-1]
    check(
        "rollback history record is well-formed",
        rec["from"] == "BLOCKING"
        and rec["to"] == "ROLLED-BACK"
        and rec["event"] == REGRESSION_EVENT
        and rec["at"] == "2026-08-01",
    )

    # 13. Retrospective-overdue surfacing: past due => OVERDUE; future => PENDING; none => NONE.
    overdue = check_retrospective(new, as_of="2026-09-01")
    check(
        "retrospective surfaced OVERDUE when as_of is past the deadline",
        overdue.overdue and overdue.verdict == "OVERDUE",
    )
    pending = check_retrospective(new, as_of="2026-08-05")
    check(
        "retrospective surfaced PENDING before the deadline",
        (not pending.overdue) and pending.verdict == "PENDING" and pending.days_remaining == 3,
    )
    on_deadline = check_retrospective(new, as_of="2026-08-08")
    check("retrospective NOT overdue exactly on the deadline day", not on_deadline.overdue)
    none_status = check_retrospective(state("BLOCKING", full))
    check("retrospective verdict NONE when no rollback recorded", none_status.verdict == "NONE")

    # 14. _retrospective_due_at handles a date-time `at` (truncates to calendar date).
    check(
        "retrospective deadline from a date-time at truncates to calendar +7d",
        _retrospective_due_at("2026-08-01T12:34:56Z") == "2026-08-08",
    )

    # 15. --signoff flag parsing.
    check(
        "--signoff cto,ciso,vp_devrel parses to a full override",
        _parse_signoff_flag("cto,ciso,vp_devrel") == {s: True for s in GOVERNANCE_SEATS},
    )
    check("--signoff none parses to an empty override (seam-only)", _parse_signoff_flag("none") == {})
    try:
        _parse_signoff_flag("president")
        check("--signoff rejects an unknown seat", False)
    except ValueError:
        check("--signoff rejects an unknown seat", True)

    print()
    if failures:
        print(f"self-test: {failures} FAILURE(S).")
        return 1
    print(
        "self-test: governance-triple gate, ROLLED-BACK emit reuse, 7-day ISEDC Class-2 retrospective "
        "stamping + overdue surfacing, illegal-source rejection, and schema-validity all sound."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="SAK Phase-4c rollback protocol — kernel-gate-revert (governance-triple-gated -> ROLLED-BACK)."
    )
    parser.add_argument("--self-test", action="store_true", help="run the deterministic offline self-test (CI gate)")
    parser.add_argument("--dry-run", action="store_true", help="evaluate a revert without writing; print the plan")
    parser.add_argument("--revert", action="store_true", help="perform the revert (writes the new state to --out)")
    parser.add_argument(
        "--check-retrospective",
        action="store_true",
        help="surface whether a stamped ISEDC Class-2 retrospective is overdue (exit 1 if overdue)",
    )
    parser.add_argument("--state", default=DEFAULT_STATE, help="path to SAK-STATE.json")
    parser.add_argument("--out", default=None, help="path to write the new state to (for --revert)")
    parser.add_argument("--at", default=None, help="ISO date/datetime the revert fires (for --revert / --dry-run)")
    parser.add_argument("--reason", default=None, help="the revert reason (required for --revert)")
    parser.add_argument("--gate", default="validate-plugins.yml", help="the gate being reverted (recorded)")
    parser.add_argument("--version", default=None, help="the gate/schema version being reverted (recorded)")
    parser.add_argument("--decision-record-ref", default=None, help="AT-DECR-phase-4c-rollback-NNN pointer (recorded)")
    parser.add_argument(
        "--signoff",
        default=None,
        help="offline sign-off override, e.g. 'cto,ciso,vp_devrel' or 'none' (default: read the SAK-STATE.json seam)",
    )
    parser.add_argument(
        "--as-of", default=None, help="ISO date to evaluate --check-retrospective against (default: today)"
    )
    parser.add_argument("--state-machine", default=STATE_MACHINE_PATH, help="path to scripts/sak-state-machine.py")
    args = parser.parse_args(argv)

    if args.self_test:
        return cmd_self_test(load_state_machine_module(args.state_machine))
    if args.check_retrospective:
        return cmd_check_retrospective(args)

    if args.dry_run or args.revert:
        if not args.at:
            parser.error("--at is required for --dry-run / --revert")
        if args.revert and not args.reason:
            parser.error("--reason is required for --revert")
        if args.dry_run and not args.reason:
            args.reason = "(dry-run: no reason supplied)"
        ssm = load_state_machine_module(args.state_machine)
        if args.dry_run:
            return cmd_dry_run(ssm, args)
        return cmd_revert(ssm, args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
