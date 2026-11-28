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
    pre.update(json.loads((REPO_ROOT / "scripts/tests/fixtures/sak-community-notice-valid.json").read_text()))
    pre["flip_evidence"] = json.loads((REPO_ROOT / "scripts/tests/fixtures/sak-flip-evidence.json").read_text())
    pre.update(pre_overrides)
    if isinstance(pre.get("flip_evidence"), dict):
        for approval in pre["flip_evidence"]["approvals"].values():
            approval["manifest_sha256"] = ssm.flip_manifest_sha256(pre)
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
    decision = ssm.evaluate(_state_machine(ssm, "READY-TO-FLIP"), ssm.FLIP_EVENT, at="2026-07-01")
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


def test_subfloor_coverage_requires_reviewed_calendar_disposition(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP", coverage_corpus_pass_pct=99.4)
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, allow_calendar_ceiling=True, at="2026-07-01").rejected
    _quarantine(ssm, sm)
    decision = ssm.evaluate(sm, ssm.FLIP_EVENT, allow_calendar_ceiling=True, at="2026-07-01")
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


def test_flip_without_community_notice_is_refused_even_with_calendar_ceiling(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP", community_notice=None)
    decision = ssm.evaluate(sm, ssm.FLIP_EVENT, allow_calendar_ceiling=True, at="2026-07-01")
    assert decision.rejected
    assert any("community_notice" in reason for reason in decision.reasons)


def _review_notice(ssm: ModuleType, sm: dict) -> None:
    notice = sm["preconditions"]["community_notice"]
    notice["vp_devrel_review"]["manifest_sha256"] = ssm.notice_manifest_sha256(notice)
    sm["preconditions"]["flip_evidence"]["notice_manifest_sha256"] = ssm.notice_manifest_sha256(notice)
    _approve_flip(ssm, sm)


@pytest.mark.parametrize("ceiling", [False, True])
@pytest.mark.parametrize(
    "at,allowed",
    [
        (None, False),
        ("invalid", False),
        ("2026-06-15T00:00:00", False),
        ("2026-06-14T23:59:59Z", False),
        ("2026-06-15T00:00:00Z", True),
        ("2026-06-14T19:00:00-05:00", True),
    ],
)
def test_notice_window_is_fourteen_full_days(ssm: ModuleType, at: str | None, allowed: bool, ceiling: bool) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    if ceiling:
        sm["preconditions"]["coverage_corpus_pass_pct"] = 99.4
        _quarantine(ssm, sm)
    decision = ssm.evaluate(sm, ssm.FLIP_EVENT, at=at, allow_calendar_ceiling=ceiling)
    assert decision.allowed is allowed


@pytest.mark.parametrize("surface", ["kernel_changelog", "marketplace_changelog", "pinned_issue", "fix_it_guide"])
def test_every_publication_surface_is_required(ssm: ModuleType, surface: str) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    del sm["preconditions"]["community_notice"]["artifacts"][surface]
    _review_notice(ssm, sm)
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01", allow_calendar_ceiling=True).rejected


@pytest.mark.parametrize(
    "path,value",
    [
        (("not_before",), "2026-06-14T23:59:59Z"),
        (("not_before",), "2026-08-01T00:00:00Z"),
        (("artifacts", "fix_it_guide", "published_at"), "2026-06-02T00:00:00Z"),
        (("artifacts", "pinned_issue", "pinned_at"), "2026-05-31T00:00:00Z"),
        (("artifacts", "pinned_issue", "pinned_at"), "2026-06-30T00:00:00Z"),
        (("artifacts", "kernel_changelog", "published_at"), "9999-12-31T00:00:00Z"),
        (("vp_devrel_review", "signed_at"), "2026-05-31T23:59:59Z"),
        (("vp_devrel_review", "signed_at"), "2026-07-02T00:00:00Z"),
        (("notifications", 0, "sent_at"), "2026-05-31T23:59:59Z"),
        (("notifications", 0, "sent_at"), "2026-07-02T00:00:00Z"),
        (("notifications", 0, "sent_at"), "2026-06-02T00:00:00Z"),
        (("artifacts", "kernel_changelog", "url"), "file:///not-public"),
        (("artifacts", "kernel_changelog", "url"), "https:///missing-host"),
        (("artifacts", "kernel_changelog", "url"), "https://user:fixture@example.org/receipt"),
        (("artifacts", "kernel_changelog", "published_at"), "2026-06-01"),
        (("artifacts", "kernel_changelog", "published_at"), "2026-06-01T00:00:00"),
        (("change_sha256",), "d" * 64),
        (("deviation_report", "sha256"), "d" * 64),
        (("notifications",), []),
        (("affected_authors",), ["fixture-author", "missed-author"]),
    ],
)
def test_notice_evidence_cannot_be_overridden_by_calendar_ceiling(ssm: ModuleType, path: tuple, value: object) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    node = sm["preconditions"]["community_notice"]
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    _review_notice(ssm, sm)
    decision = ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01", allow_calendar_ceiling=True)
    assert decision.rejected
    assert any("community_notice" in reason and "049-AT-DECR" in reason for reason in decision.reasons)


def test_notice_review_does_not_survive_a_changed_artifact(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    sm["preconditions"]["community_notice"]["artifacts"]["fix_it_guide"]["sha256"] = "e" * 64
    decision = ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01")
    assert decision.rejected
    assert any("manifest_sha256" in reason for reason in decision.reasons)


def test_notice_delivery_inventory_is_exact_and_allows_reviewed_empty_scope(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    notice = sm["preconditions"]["community_notice"]
    notice["notifications"].append(copy.deepcopy(notice["notifications"][0]))
    _review_notice(ssm, sm)
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01").rejected
    notice["notifications"] = []
    notice["affected_authors"] = []
    _review_notice(ssm, sm)
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01").allowed


def test_emit_uses_transition_time_and_preserves_state_when_notice_is_early(ssm: ModuleType) -> None:
    state = {"state_machine": _state_machine(ssm, "READY-TO-FLIP")}
    before = copy.deepcopy(state)
    with pytest.raises(ssm.TransitionError, match="public notice window"):
        ssm.emit(state, ssm.FLIP_EVENT, at="2026-06-14T23:59:59Z")
    assert state == before
    emitted = ssm.emit(state, ssm.FLIP_EVENT, at="2026-06-15T00:00:00Z")
    assert emitted["state_machine"]["current_state"] == "BLOCKING"
    assert emitted["state_machine"]["transition_history"][-1][
        "community_notice_manifest_sha256"
    ] == ssm.notice_manifest_sha256(state["state_machine"]["preconditions"]["community_notice"])
    assert state == before


def test_emitted_notice_receipt_is_schema_valid(ssm: ModuleType, tmp_path: Path) -> None:
    state = json.loads((REPO_ROOT / "SAK-STATE.json").read_text())
    state["state_machine"] = _state_machine(ssm, "READY-TO-FLIP")
    emitted = ssm.emit(state, ssm.FLIP_EVENT, at="2026-07-01T00:00:00Z")
    path = tmp_path / "state.json"
    path.write_text(json.dumps(emitted))
    assert ssm.validate_state_file(str(path)) == []
    emitted["state_machine"]["transition_history"][-1]["community_notice_manifest_sha256"] = "invalid"
    path.write_text(json.dumps(emitted))
    assert ssm.validate_state_file(str(path))


def _approve_flip(ssm: ModuleType, sm: dict) -> None:
    pre = sm["preconditions"]
    for approval in pre["flip_evidence"]["approvals"].values():
        approval["manifest_sha256"] = ssm.flip_manifest_sha256(pre)


def _quarantine(ssm: ModuleType, sm: dict) -> None:
    artifact = {"url": "https://example.org/quarantine", "sha256": "e" * 64, "published_at": "2026-06-01T01:00:00Z"}
    sm["preconditions"]["flip_evidence"]["coverage_disposition"] = {
        "decision": "flip-with-quarantine",
        "reviewed_at": "2026-06-01T00:30:00Z",
        "decision_record": artifact,
        "quarantine_report": artifact,
        "corpus_size": 10000,
        "passed_files": 9940,
        "quarantined_files": [f"synthetic/{i}.md" for i in range(20)],
        "quarantine_mode": "advisory-only",
    }
    _approve_flip(ssm, sm)


@pytest.mark.parametrize(
    "field", ["flip_evidence", "coverage_corpus_pass_pct", "shadow_days_complete", "shadow_deviation_pct"]
)
def test_missing_flip_inputs_fail_closed(ssm: ModuleType, field: str) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    del sm["preconditions"][field]
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01", allow_calendar_ceiling=True).rejected


@pytest.mark.parametrize("value", ["true", 1, [], {}, None])
def test_governance_truthiness_is_not_approval(ssm: ModuleType, value: object) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    sm["preconditions"]["governance_signoff"]["cto"] = value
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01").rejected


@pytest.mark.parametrize("value", ["0", False, -1, float("nan"), float("inf"), {}, []])
def test_bad_p0_types_rejected_without_exception(ssm: ModuleType, value: object) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    sm["preconditions"]["open_p0_count"] = value
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01").rejected


@pytest.mark.parametrize(
    "path,value",
    [
        (("advisory", "started_at"), "2026-05-02T00:00:01Z"),
        (("advisory", "continuous"), False),
        (("deterministic_folds", "total"), 0),
        (("deterministic_folds", "agreed"), 9999),
        (("rollback", "tested"), False),
        (("rollback", "implemented"), False),
        (("rollback", "strategy"), "mutate-original"),
        (("rollback", "tested_at"), "2026-07-02T00:00:00Z"),
        (("security_checks_day_zero",), False),
        (("valid_until",), "2026-06-30T23:59:59Z"),
        (("measured_at",), "2026-07-02T00:00:00Z"),
        (("change_sha256",), "a" * 64),
        (("deviation_report_sha256",), "a" * 64),
        (("notice_manifest_sha256",), "a" * 64),
        (("artifacts", "agreement", "url"), "https:///missing-host"),
        (("artifacts", "shadow_log", "published_at"), "2026-07-02T00:00:00Z"),
        (("approvals", "cto", "signed_at"), "2026-05-31T00:00:00Z"),
        (("approvals", "ciso", "approved"), False),
    ],
)
def test_ratified_gate_failures_cannot_be_waived(ssm: ModuleType, path: tuple, value: object) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP", coverage_corpus_pass_pct=99.4)
    _quarantine(ssm, sm)
    node = sm["preconditions"]["flip_evidence"]
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    _approve_flip(ssm, sm)
    result = ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01", allow_calendar_ceiling=True)
    assert result.rejected


def test_exact_thirty_day_soak_boundary(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    sm["preconditions"]["flip_evidence"]["advisory"]["started_at"] = "2026-05-02T00:00:00Z"
    _approve_flip(ssm, sm)
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01").allowed


def test_changed_inputs_invalidate_every_governance_review(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    sm["preconditions"]["coverage_corpus_pass_pct"] = 99.8
    result = ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01")
    assert result.rejected
    assert sum("approval does not bind" in r for r in result.reasons) == 3


@pytest.mark.parametrize(
    "path,value",
    [
        (("corpus_size",), 0),
        (("passed_files",), 10001),
        (("passed_files",), 9941),
        (("quarantined_files",), []),
        (("quarantined_files",), ["same.md", "same.md"]),
        (("quarantined_files",), [f"synthetic/{i}.md" for i in range(50)]),
        (("quarantine_mode",), "blocking"),
        (("decision",), "extend"),
        (("reviewed_at",), "2026-05-30T00:00:00Z"),
        (("decision_record", "published_at"), "2026-07-02T00:00:00Z"),
    ],
)
def test_coverage_disposition_cannot_hide_unsafe_or_inconsistent_scope(
    ssm: ModuleType, path: tuple, value: object
) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP", coverage_corpus_pass_pct=99.4)
    _quarantine(ssm, sm)
    node = sm["preconditions"]["flip_evidence"]["coverage_disposition"]
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    _approve_flip(ssm, sm)
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01", allow_calendar_ceiling=True).rejected


def test_coverage_exception_does_not_accept_inadequate_retained_corpus(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP", coverage_corpus_pass_pct=98.0)
    _quarantine(ssm, sm)
    sm["preconditions"]["flip_evidence"]["coverage_disposition"]["passed_files"] = 9800
    _approve_flip(ssm, sm)
    result = ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01", allow_calendar_ceiling=True)
    assert any("retained corpus" in reason for reason in result.reasons)


@pytest.mark.parametrize("value", [None, [], "invalid", False])
def test_direct_flip_calls_refuse_malformed_state(ssm: ModuleType, value: object) -> None:
    assert ssm.can_flip(value, at="2026-07-01").rejected
    assert ssm.evaluate(value, ssm.FLIP_EVENT, at="2026-07-01").rejected


@pytest.mark.parametrize("value", [None, [], "invalid", False])
def test_direct_flip_calls_refuse_malformed_preconditions(ssm: ModuleType, value: object) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP")
    sm["preconditions"] = value
    assert ssm.can_flip(sm, at="2026-07-01").rejected


def test_calendar_flag_must_be_boolean(ssm: ModuleType) -> None:
    assert ssm.can_flip(_state_machine(ssm, "READY-TO-FLIP"), at="2026-07-01", allow_calendar_ceiling="false").rejected


def test_flip_transition_records_bound_evidence_digest(ssm: ModuleType) -> None:
    state = {"state_machine": _state_machine(ssm, "READY-TO-FLIP")}
    result = ssm.emit(state, ssm.FLIP_EVENT, at="2026-07-01")
    assert result["state_machine"]["transition_history"][-1][
        "flip_evidence_manifest_sha256"
    ] == ssm.flip_manifest_sha256(state["state_machine"]["preconditions"])


def test_unbounded_counts_are_refused_without_arithmetic_overflow(ssm: ModuleType) -> None:
    sm = _state_machine(ssm, "READY-TO-FLIP", coverage_corpus_pass_pct=99.4)
    _quarantine(ssm, sm)
    sm["preconditions"]["flip_evidence"]["coverage_disposition"]["passed_files"] = 10**1000
    assert ssm.evaluate(sm, ssm.FLIP_EVENT, at="2026-07-01", allow_calendar_ceiling=True).rejected
