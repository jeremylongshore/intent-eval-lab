"""Unit tests for the SAK Phase-4 advisory->blocking flip state machine.

Covers the test matrix the brief asks for:
  - legal-transition-passes
  - illegal-transition-rejected
  - precondition-not-met-flip-rejected (open P0; missing sign-off; sub-floor coverage)
  - rollback-from-each-gated-state
  - schema-validation of a valid + an invalid SAK-STATE.json

Offline, fixture-driven, no network. The module under test is loaded by file
path via the `ssm` session fixture (scripts use hyphenated filenames).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


# ── Fixtures ──────────────────────────────────────────────────────────────────


def _state_machine(ssm: ModuleType, state: str, **pre_overrides: object) -> dict:
    """A state_machine dict at `state` with a clean, flip-ready preconditions
    block (full triple sign-off, zero P0, coverage above floor) before
    overrides are applied into preconditions."""
    pre: dict = {
        "coverage_corpus_pass_pct": 99.9,
        "shadow_days_complete": 10,
        "shadow_deviation_pct": 0.1,
        "open_p0_count": 0,
        "governance_signoff": {
            "cto": True,
            "ciso": True,
            "vp_devrel": True,
            "decision_record_ref": "044-AT-DECR",
        },
    }
    pre.update(pre_overrides)
    return {
        "machine": "SAK advisory -> blocking flip (Phase 4)",
        "current_state": state,
        "states": list(ssm.STATES),
        "preconditions": pre,
    }


# ── Graph integrity ───────────────────────────────────────────────────────────


def test_every_transition_target_and_source_is_a_known_state(ssm: ModuleType) -> None:
    assert all(to in ssm.STATES for to in ssm.LEGAL_TRANSITIONS.values())
    assert all(frm in ssm.STATES for (frm, _ev) in ssm.LEGAL_TRANSITIONS)


def test_canonical_forward_path_edges_exist(ssm: ModuleType) -> None:
    path = [
        ("ADVISORY", "wave-a-merged", "ADVISORY-W-A"),
        ("ADVISORY-W-A", "wave-b-done", "ADVISORY-W-AB"),
        ("ADVISORY-W-AB", "enable-shadow", "SHADOW-MODE"),
        ("SHADOW-MODE", "dispositions-resolved", "READY-TO-FLIP"),
        ("READY-TO-FLIP", ssm.FLIP_EVENT, "BLOCKING"),
    ]
    for frm, ev, to in path:
        assert ssm.LEGAL_TRANSITIONS[(frm, ev)] == to


# ── Legal transition passes ───────────────────────────────────────────────────


@pytest.mark.parametrize(
    "from_state,event,to_state",
    [
        ("ADVISORY", "wave-a-merged", "ADVISORY-W-A"),
        ("ADVISORY-W-A", "wave-b-done", "ADVISORY-W-AB"),
        ("ADVISORY-W-AB", "enable-shadow", "SHADOW-MODE"),
        ("SHADOW-MODE", "deviations-open-p0", "HOLDING"),
        ("HOLDING", "audit-cleared", "SHADOW-MODE"),
        ("ROLLED-BACK", "back-to-shadow", "SHADOW-MODE"),
    ],
)
def test_legal_transition_passes(ssm: ModuleType, from_state: str, event: str, to_state: str) -> None:
    # Use an open P0 so deviations-open-p0 (SHADOW-MODE -> HOLDING) is well-posed;
    # harmless for the other edges.
    sm = _state_machine(ssm, from_state, open_p0_count=1 if from_state == "SHADOW-MODE" else 0)
    decision = ssm.evaluate(sm, event)
    assert decision.allowed is True
    assert decision.to_state == to_state
    assert decision.rejected is False


def test_dispositions_resolved_passes_with_zero_p0(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "SHADOW-MODE", open_p0_count=0)
    decision = ssm.evaluate(sm, "dispositions-resolved")
    assert decision.allowed is True
    assert decision.to_state == "READY-TO-FLIP"


def test_flip_passes_with_all_preconditions_met(ssm: ModuleType) -> None:
    decision = ssm.evaluate(_state_machine(ssm, "READY-TO-FLIP"), ssm.FLIP_EVENT)
    assert decision.allowed is True
    assert decision.to_state == "BLOCKING"


# ── Illegal transition rejected ───────────────────────────────────────────────


def test_illegal_event_from_state_rejected(ssm: ModuleType) -> None:
    # The flip event is illegal from ADVISORY (it's only legal from READY-TO-FLIP).
    decision = ssm.evaluate(_state_machine(ssm, "ADVISORY"), ssm.FLIP_EVENT)
    assert decision.rejected is True
    assert any("illegal transition" in r for r in decision.reasons)


def test_unknown_event_rejected(ssm: ModuleType) -> None:
    decision = ssm.evaluate(_state_machine(ssm, "SHADOW-MODE"), "teleport")
    assert decision.rejected is True


def test_unknown_current_state_rejected(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "ADVISORY")
    sm["current_state"] = "NOT-A-STATE"
    decision = ssm.evaluate(sm, "wave-a-merged")
    assert decision.rejected is True
    assert any("unknown current_state" in r for r in decision.reasons)


# ── Precondition-not-met flip rejected ────────────────────────────────────────


def test_flip_rejected_with_open_p0(ssm: ModuleType) -> None:
    decision = ssm.evaluate(_state_machine(ssm, "READY-TO-FLIP", open_p0_count=1), ssm.FLIP_EVENT)
    assert decision.rejected is True
    assert any("(c)" in r for r in decision.reasons)


def test_calendar_ceiling_does_not_override_open_p0(ssm: ModuleType) -> None:
    # The 30-day calendar ceiling can ONLY disposition coverage (a), never the
    # zero-open-P0 hard gate (c) — plan 048 Delta 3.
    decision = ssm.evaluate(
        _state_machine(ssm, "READY-TO-FLIP", open_p0_count=3),
        ssm.FLIP_EVENT,
        allow_calendar_ceiling=True,
    )
    assert decision.rejected is True
    assert any("(c)" in r for r in decision.reasons)


@pytest.mark.parametrize("missing_seat", ["cto", "ciso", "vp_devrel"])
def test_flip_rejected_with_incomplete_governance_signoff(ssm: ModuleType, missing_seat: str) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    sm["preconditions"]["governance_signoff"][missing_seat] = False
    decision = ssm.evaluate(sm, ssm.FLIP_EVENT)
    assert decision.rejected is True
    assert any("(d)" in r for r in decision.reasons)


def test_calendar_ceiling_does_not_override_missing_signoff(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    sm["preconditions"]["governance_signoff"]["ciso"] = False
    decision = ssm.evaluate(sm, ssm.FLIP_EVENT, allow_calendar_ceiling=True)
    assert decision.rejected is True
    assert any("(d)" in r for r in decision.reasons)


def test_subfloor_coverage_rejected_without_ceiling(ssm: ModuleType) -> None:
    decision = ssm.evaluate(_state_machine(ssm, "READY-TO-FLIP", coverage_corpus_pass_pct=98.0), ssm.FLIP_EVENT)
    assert decision.rejected is True
    assert any("(a)" in r for r in decision.reasons)


def test_subfloor_coverage_permitted_with_calendar_ceiling(ssm: ModuleType) -> None:
    decision = ssm.evaluate(
        _state_machine(ssm, "READY-TO-FLIP", coverage_corpus_pass_pct=98.0),
        ssm.FLIP_EVENT,
        allow_calendar_ceiling=True,
    )
    assert decision.allowed is True
    assert decision.to_state == "BLOCKING"


def test_dispositions_resolved_blocked_with_open_p0(ssm: ModuleType) -> None:
    # Open-P0 deviations must route to HOLDING, not READY-TO-FLIP.
    decision = ssm.evaluate(_state_machine(ssm, "SHADOW-MODE", open_p0_count=1), "dispositions-resolved")
    assert decision.rejected is True


# ── Rollback from each gated state ────────────────────────────────────────────


@pytest.mark.parametrize(
    "from_state,event",
    [
        ("ADVISORY-W-A", "wave-a-failure"),
        ("ADVISORY-W-AB", "wave-b-failure"),
        ("BLOCKING", "regression-detected"),
    ],
)
def test_rollback_reachable_from_each_gated_state(ssm: ModuleType, from_state: str, event: str) -> None:
    decision = ssm.evaluate(_state_machine(ssm, from_state), event)
    assert decision.allowed is True
    assert decision.to_state == "ROLLED-BACK"


def test_gated_states_set_matches_rollback_sources(ssm: ModuleType) -> None:
    rollback_sources = {frm for (frm, _ev), to in ssm.LEGAL_TRANSITIONS.items() if to == "ROLLED-BACK"}
    assert rollback_sources == set(ssm.GATED_STATES)


def test_rollback_returns_to_shadow(ssm: ModuleType) -> None:
    decision = ssm.evaluate(_state_machine(ssm, "ROLLED-BACK"), "back-to-shadow")
    assert decision.allowed is True
    assert decision.to_state == "SHADOW-MODE"


# ── emit() behavior ───────────────────────────────────────────────────────────


def test_emit_is_non_mutating_and_appends_history(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "ADVISORY")
    state = {"state_machine": sm}
    before = json.dumps(state, sort_keys=True)
    new = ssm.emit(state, "wave-a-merged", at="2026-07-01")
    # input untouched
    assert json.dumps(state, sort_keys=True) == before
    # output advanced
    assert new["state_machine"]["current_state"] == "ADVISORY-W-A"
    assert new["state_machine"]["entered_at"] == "2026-07-01"
    assert new["state_machine"]["transition_history"] == [
        {
            "from": "ADVISORY",
            "to": "ADVISORY-W-A",
            "event": "wave-a-merged",
            "at": "2026-07-01",
            "reason": None,
            "decision_record_ref": None,
        }
    ]


def test_emit_records_reason_and_decision_record(ssm: ModuleType) -> None:
    state = {"state_machine": _state_machine(ssm, "BLOCKING")}
    new = ssm.emit(
        state,
        "regression-detected",
        at="2026-08-01",
        reason="BLOCKING broke real PRs at high rate",
        decision_record_ref="AT-DECR-phase-4c-rollback-001",
    )
    rec = new["state_machine"]["transition_history"][-1]
    assert rec["to"] == "ROLLED-BACK"
    assert rec["reason"] == "BLOCKING broke real PRs at high rate"
    assert rec["decision_record_ref"] == "AT-DECR-phase-4c-rollback-001"


def test_emit_raises_on_rejected_transition(ssm: ModuleType) -> None:
    state = {"state_machine": _state_machine(ssm, "READY-TO-FLIP", open_p0_count=2)}
    with pytest.raises(ssm.TransitionError) as exc:
        ssm.emit(state, ssm.FLIP_EVENT, at="2026-07-01")
    assert any("(c)" in r for r in exc.value.decision.reasons)


def test_emit_raises_when_no_state_machine_present(ssm: ModuleType) -> None:
    with pytest.raises(ssm.TransitionError):
        ssm.emit({}, "wave-a-merged", at="2026-07-01")


def test_full_happy_path_walk(ssm: ModuleType) -> None:
    state = {"state_machine": _state_machine(ssm, "ADVISORY")}
    chain = [
        ("wave-a-merged", "ADVISORY-W-A"),
        ("wave-b-done", "ADVISORY-W-AB"),
        ("enable-shadow", "SHADOW-MODE"),
        ("dispositions-resolved", "READY-TO-FLIP"),
        (ssm.FLIP_EVENT, "BLOCKING"),
    ]
    for event, expected in chain:
        state = ssm.emit(state, event, at="2026-07-01")
        assert state["state_machine"]["current_state"] == expected
    assert len(state["state_machine"]["transition_history"]) == 5


# ── Schema validation of a valid + an invalid SAK-STATE.json ──────────────────


def test_committed_sak_state_json_is_schema_valid(ssm: ModuleType) -> None:
    errors = ssm.validate_state_file(str(REPO_ROOT / "SAK-STATE.json"), ssm.SCHEMA_PATH)
    assert errors == []


def test_invalid_sak_state_json_is_rejected(ssm: ModuleType, tmp_path: Path) -> None:
    # Start from the real committed file, then break it: an off-canon state.
    with open(REPO_ROOT / "SAK-STATE.json", encoding="utf-8") as fh:
        doc = json.load(fh)
    bad = copy.deepcopy(doc)
    bad["state_machine"]["current_state"] = "NOT-A-REAL-STATE"
    bad_path = tmp_path / "bad-SAK-STATE.json"
    bad_path.write_text(json.dumps(bad), encoding="utf-8")
    errors = ssm.validate_state_file(str(bad_path), ssm.SCHEMA_PATH)
    assert errors != []
    assert any("current_state" in e for e in errors)


def test_invalid_state_machine_missing_required_field_rejected(ssm: ModuleType, tmp_path: Path) -> None:
    bad = {
        "state_version": "sak-state/v1",
        "state_machine": {
            # missing required "machine" and "states"
            "current_state": "ADVISORY",
        },
    }
    bad_path = tmp_path / "missing-required.json"
    bad_path.write_text(json.dumps(bad), encoding="utf-8")
    errors = ssm.validate_state_file(str(bad_path), ssm.SCHEMA_PATH)
    assert errors != []
