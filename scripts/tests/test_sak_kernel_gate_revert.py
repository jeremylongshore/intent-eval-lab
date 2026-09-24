"""Unit tests for the SAK Phase-4c rollback protocol — kernel-gate-revert.

Covers the test matrix the brief asks for:
  - revert with the full governance triple succeeds and reaches ROLLED-BACK with
    retrospective_due_at set (= revert_at + 7 calendar days)
  - revert with ANY missing sign-off is REJECTED with the right reason (each of
    the three missing seats tested independently)
  - revert from an illegal source state is rejected
  - retrospective-overdue detection (OVERDUE / PENDING / NONE; boundary day)
  - the emitted ROLLED-BACK state (incl. the rollback block) validates against
    sak-state.schema.json

Offline, fixture-driven, no network. Both modules are loaded by file path via
the `gate_revert` + `ssm` session fixtures in conftest.py (scripts use
hyphenated filenames).
"""

from __future__ import annotations

import json
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

FULL_SIGNOFF = {"cto": True, "ciso": True, "vp_devrel": True}


# ── Fixtures ──────────────────────────────────────────────────────────────────


def _state(ssm: ModuleType, current: str, signoff: dict | None = None) -> dict:
    """A full SAK-STATE-shaped dict at `current` with the given (partial) triple
    sign-off applied into preconditions.governance_signoff. Default sign-off is
    all-false (the seam's default), so callers opt INTO authorization."""
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


# ── Revert with full triple sign-off succeeds -> ROLLED-BACK + retrospective ──


def test_revert_with_full_triple_reaches_rolled_back(gate_revert: ModuleType, ssm: ModuleType) -> None:
    state = _state(ssm, "BLOCKING", FULL_SIGNOFF)
    new = gate_revert.perform_revert(
        ssm,
        state,
        at="2026-08-01",
        reason="BLOCKING broke real PRs at high rate",
        reverted_gate="validate-plugins.yml",
        reverted_version="authoring/v1",
        decision_record_ref="AT-DECR-phase-4c-rollback-001",
    )
    assert new["state_machine"]["current_state"] == "ROLLED-BACK"
    rb = new["state_machine"]["rollback"]
    assert rb["from_state"] == "BLOCKING"
    assert rb["to_state"] == "ROLLED-BACK"
    assert rb["reason"] == "BLOCKING broke real PRs at high rate"
    assert rb["reverted_gate"] == "validate-plugins.yml"
    assert rb["reverted_version"] == "authoring/v1"
    assert rb["decision_record_ref"] == "AT-DECR-phase-4c-rollback-001"
    assert rb["governance_signoff"] == FULL_SIGNOFF


def test_retrospective_due_at_is_revert_plus_seven_calendar_days(gate_revert: ModuleType, ssm: ModuleType) -> None:
    new = gate_revert.perform_revert(
        ssm, _state(ssm, "BLOCKING", FULL_SIGNOFF), at="2026-08-01", reason="r", reverted_gate="g"
    )
    rb = new["state_machine"]["rollback"]
    assert rb["retrospective_due_at"] == "2026-08-08"
    assert rb["retrospective_window_days"] == gate_revert.RETROSPECTIVE_WINDOW_DAYS == 7
    assert rb["retrospective_class"] == "ISEDC-Class-2"


def test_revert_appends_exactly_one_history_entry_well_formed(gate_revert: ModuleType, ssm: ModuleType) -> None:
    new = gate_revert.perform_revert(
        ssm, _state(ssm, "BLOCKING", FULL_SIGNOFF), at="2026-08-01", reason="r", reverted_gate="g"
    )
    history = new["state_machine"]["transition_history"]
    assert len(history) == 1
    rec = history[0]
    assert rec["from"] == "BLOCKING"
    assert rec["to"] == "ROLLED-BACK"
    assert rec["event"] == gate_revert.REGRESSION_EVENT
    assert rec["at"] == "2026-08-01"
    assert rec["reason"] == "r"


def test_revert_is_non_mutating(gate_revert: ModuleType, ssm: ModuleType) -> None:
    src = _state(ssm, "BLOCKING", FULL_SIGNOFF)
    snapshot = json.dumps(src, sort_keys=True)
    _ = gate_revert.perform_revert(ssm, src, at="2026-08-01", reason="r", reverted_gate="g")
    assert json.dumps(src, sort_keys=True) == snapshot


def test_evaluate_revert_allowed_with_full_triple(gate_revert: ModuleType, ssm: ModuleType) -> None:
    decision = gate_revert.evaluate_revert(ssm, _state(ssm, "BLOCKING", FULL_SIGNOFF)["state_machine"])
    assert decision.allowed is True
    assert decision.to_state == "ROLLED-BACK"
    assert decision.missing_signoff == ()


# ── Revert with a missing sign-off is REJECTED with the right reason ──────────


@pytest.mark.parametrize(
    "missing_seat,pretty",
    [("cto", "CTO"), ("ciso", "CISO"), ("vp_devrel", "VP-DevRel")],
)
def test_revert_rejected_when_one_seat_missing(
    gate_revert: ModuleType, ssm: ModuleType, missing_seat: str, pretty: str
) -> None:
    partial = {s: True for s in gate_revert.GOVERNANCE_SEATS if s != missing_seat}
    decision = gate_revert.evaluate_revert(ssm, _state(ssm, "BLOCKING", partial)["state_machine"])
    assert decision.rejected is True
    assert missing_seat in decision.missing_signoff
    assert decision.to_state is None
    assert any("governance-triple sign-off incomplete" in r for r in decision.reasons)
    assert any(pretty in r for r in decision.reasons)


def test_revert_rejected_with_no_signoff_names_all_three(gate_revert: ModuleType, ssm: ModuleType) -> None:
    decision = gate_revert.evaluate_revert(ssm, _state(ssm, "BLOCKING")["state_machine"])
    assert decision.rejected is True
    assert set(decision.missing_signoff) == set(gate_revert.GOVERNANCE_SEATS)


def test_perform_revert_raises_on_incomplete_signoff(gate_revert: ModuleType, ssm: ModuleType) -> None:
    state = _state(ssm, "BLOCKING", {"cto": True, "ciso": True})  # vp_devrel absent
    with pytest.raises(gate_revert.RevertError) as exc:
        gate_revert.perform_revert(ssm, state, at="2026-08-01", reason="r", reverted_gate="g")
    assert "vp_devrel" in exc.value.decision.missing_signoff


def test_perform_revert_refuses_empty_reason(gate_revert: ModuleType, ssm: ModuleType) -> None:
    with pytest.raises(gate_revert.RevertError):
        gate_revert.perform_revert(
            ssm, _state(ssm, "BLOCKING", FULL_SIGNOFF), at="2026-08-01", reason="  ", reverted_gate="g"
        )


# ── Revert from an illegal source state is rejected ───────────────────────────


@pytest.mark.parametrize("illegal_source", ["ADVISORY", "SHADOW-MODE", "READY-TO-FLIP", "HOLDING", "ROLLED-BACK"])
def test_revert_from_illegal_source_state_rejected(
    gate_revert: ModuleType, ssm: ModuleType, illegal_source: str
) -> None:
    # Even with the full triple, states with no `regression-detected` rollback
    # edge cannot be reverted; the engine's legal-transition check rejects them.
    decision = gate_revert.evaluate_revert(ssm, _state(ssm, illegal_source, FULL_SIGNOFF)["state_machine"])
    assert decision.rejected is True
    assert any("illegal transition" in r for r in decision.reasons)


def test_perform_revert_raises_from_illegal_source_state(gate_revert: ModuleType, ssm: ModuleType) -> None:
    with pytest.raises(gate_revert.RevertError):
        gate_revert.perform_revert(
            ssm, _state(ssm, "ADVISORY", FULL_SIGNOFF), at="2026-08-01", reason="r", reverted_gate="g"
        )


def test_perform_revert_raises_when_no_state_machine(gate_revert: ModuleType, ssm: ModuleType) -> None:
    with pytest.raises(gate_revert.RevertError):
        gate_revert.perform_revert(ssm, {}, at="2026-08-01", reason="r", reverted_gate="g")


# ── Sign-off seam + override resolution ───────────────────────────────────────


def test_governance_gate_reads_the_state_machine_seam(gate_revert: ModuleType, ssm: ModuleType) -> None:
    # No override: authorization comes purely from preconditions.governance_signoff.
    allowed = gate_revert.evaluate_revert(ssm, _state(ssm, "BLOCKING", FULL_SIGNOFF)["state_machine"])
    rejected = gate_revert.evaluate_revert(ssm, _state(ssm, "BLOCKING")["state_machine"])
    assert allowed.allowed is True
    assert rejected.rejected is True


def test_signoff_override_authorizes_a_seam_unauthorized_state(gate_revert: ModuleType, ssm: ModuleType) -> None:
    # Seam says all-false, but an out-of-band override carries the triple.
    decision = gate_revert.evaluate_revert(ssm, _state(ssm, "BLOCKING")["state_machine"], signoff_override=FULL_SIGNOFF)
    assert decision.allowed is True


# ── Retrospective-overdue detection ───────────────────────────────────────────


def _reverted_state(gate_revert: ModuleType, ssm: ModuleType, at: str = "2026-08-01") -> dict:
    return gate_revert.perform_revert(ssm, _state(ssm, "BLOCKING", FULL_SIGNOFF), at=at, reason="r", reverted_gate="g")


def test_retrospective_overdue_when_past_deadline(gate_revert: ModuleType, ssm: ModuleType) -> None:
    new = _reverted_state(gate_revert, ssm)  # due 2026-08-08
    status = gate_revert.check_retrospective(new, as_of="2026-09-01")
    assert status.overdue is True
    assert status.verdict == "OVERDUE"
    assert status.due_at == "2026-08-08"


def test_retrospective_pending_before_deadline(gate_revert: ModuleType, ssm: ModuleType) -> None:
    new = _reverted_state(gate_revert, ssm)
    status = gate_revert.check_retrospective(new, as_of="2026-08-05")
    assert status.overdue is False
    assert status.verdict == "PENDING"
    assert status.days_remaining == 3


def test_retrospective_not_overdue_exactly_on_deadline(gate_revert: ModuleType, ssm: ModuleType) -> None:
    new = _reverted_state(gate_revert, ssm)
    status = gate_revert.check_retrospective(new, as_of="2026-08-08")
    assert status.overdue is False
    assert status.days_remaining == 0


def test_retrospective_overdue_one_day_after_deadline(gate_revert: ModuleType, ssm: ModuleType) -> None:
    new = _reverted_state(gate_revert, ssm)
    status = gate_revert.check_retrospective(new, as_of="2026-08-09")
    assert status.overdue is True
    assert status.days_remaining == -1


def test_retrospective_none_when_no_rollback_recorded(gate_revert: ModuleType, ssm: ModuleType) -> None:
    status = gate_revert.check_retrospective(_state(ssm, "BLOCKING", FULL_SIGNOFF))
    assert status.present is False
    assert status.verdict == "NONE"
    assert status.overdue is False


# ── affected_window intent (kernel-emitter handoff, no Rekor write here) ──────


def test_affected_window_recorded_as_intent(gate_revert: ModuleType, ssm: ModuleType) -> None:
    new = gate_revert.perform_revert(
        ssm,
        _state(ssm, "BLOCKING", FULL_SIGNOFF),
        at="2026-08-01",
        reason="r",
        reverted_gate="g",
        affected_window={"from": "2026-07-20", "to": "2026-08-01"},
    )
    rb = new["state_machine"]["rollback"]
    assert rb["affected_window"] == {"from": "2026-07-20", "to": "2026-08-01"}
    assert rb["superseding_signing_mode"] == "rolled-back-superseded"


def test_affected_window_absent_when_not_supplied(gate_revert: ModuleType, ssm: ModuleType) -> None:
    new = _reverted_state(gate_revert, ssm)
    rb = new["state_machine"]["rollback"]
    assert "affected_window" not in rb
    assert "superseding_signing_mode" not in rb


# ── Schema validity of the emitted ROLLED-BACK state ──────────────────────────


def test_emitted_rolled_back_state_validates_against_schema(
    gate_revert: ModuleType, ssm: ModuleType, tmp_path: Path
) -> None:
    new = gate_revert.perform_revert(
        ssm,
        _state(ssm, "BLOCKING", FULL_SIGNOFF),
        at="2026-08-01",
        reason="BLOCKING broke real PRs at high rate",
        reverted_gate="validate-plugins.yml",
        reverted_version="authoring/v1",
        decision_record_ref="AT-DECR-phase-4c-rollback-001",
    )
    out = tmp_path / "rolled-back-SAK-STATE.json"
    out.write_text(json.dumps(new), encoding="utf-8")
    errors = ssm.validate_state_file(str(out), ssm.SCHEMA_PATH)
    assert errors == []


def test_emitted_state_with_affected_window_validates(gate_revert: ModuleType, ssm: ModuleType, tmp_path: Path) -> None:
    new = gate_revert.perform_revert(
        ssm,
        _state(ssm, "BLOCKING", FULL_SIGNOFF),
        at="2026-08-01",
        reason="r",
        reverted_gate="g",
        affected_window={"from": "2026-07-20", "to": "2026-08-01"},
    )
    out = tmp_path / "rolled-back-window.json"
    out.write_text(json.dumps(new), encoding="utf-8")
    errors = ssm.validate_state_file(str(out), ssm.SCHEMA_PATH)
    assert errors == []


# ── --signoff CLI flag parsing ────────────────────────────────────────────────


def test_parse_signoff_full(gate_revert: ModuleType) -> None:
    assert gate_revert._parse_signoff_flag("cto,ciso,vp_devrel") == {s: True for s in gate_revert.GOVERNANCE_SEATS}


def test_parse_signoff_none_and_empty(gate_revert: ModuleType) -> None:
    assert gate_revert._parse_signoff_flag("none") == {}
    assert gate_revert._parse_signoff_flag(None) is None


def test_parse_signoff_unknown_seat_raises(gate_revert: ModuleType) -> None:
    with pytest.raises(ValueError):
        gate_revert._parse_signoff_flag("president")


# ── CLI smoke (offline, exit codes) ───────────────────────────────────────────


def test_cli_self_test_exits_zero(gate_revert: ModuleType) -> None:
    assert gate_revert.main(["--self-test"]) == 0


def test_cli_dry_run_against_committed_state_is_rejected(gate_revert: ModuleType) -> None:
    # The committed SAK-STATE.json is in ADVISORY with no sign-off; a dry-run
    # revert must be rejected (exit 1) — proves the gate fires on real state.
    rc = gate_revert.main(["--dry-run", "--at", "2026-08-01", "--reason", "x"])
    assert rc == 1


def test_cli_check_retrospective_on_committed_state_is_none(gate_revert: ModuleType) -> None:
    # The committed SAK-STATE.json has no rollback block => NONE => exit 0.
    rc = gate_revert.main(["--check-retrospective"])
    assert rc == 0
