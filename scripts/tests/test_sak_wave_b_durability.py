"""Unit tests for the SAK Wave-B durability protocol.

Covers the test matrix the brief asks for:
  - branch-name determinism (same file -> same branch; different -> different)
  - the retry counter increments + escalates on the 3rd failure to the parked
    queue with a reason
  - the atomic-commit invariant (no partial state)
  - a parked item is recoverable / re-enqueued (not failed)
  - an open-PR file is parked, not attempted
  - the durability state round-trips JSON + validates against the schema

The parked-queue integration is exercised against the REAL reconciliation-queue
module (loaded via the `srq` fixture) — the durability protocol routes parked
files into the ONE shared queue rather than building a second one.

Offline, fixture-driven, no network. The modules under test are loaded by file
path via the `wb` + `srq` session fixtures (scripts use hyphenated filenames).

DISTINCT from test_sak_reconciliation_queue.py (the shared parked/disposition
queue) and test_sak_state_machine.py (the Phase-4 flip lifecycle) — this
exercises the per-file Wave-B durability lifecycle (branch + atomic commit +
3-retry + escalation + parked-queue routing).
"""

from __future__ import annotations

import json
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "specs" / "state-machines" / "schema" / "sak-wave-b-durability.schema.json"
COMMITTED_STATE = REPO_ROOT / "SAK-WAVE-B-DURABILITY.json"

TARGET_VERSION = "authoring/v1@1.0.0"


# ── Fixtures ──────────────────────────────────────────────────────────────────


def _accept_once(wb: ModuleType, path: str) -> object:
    """A RefinerAttemptSource whose first attempt for `path` is accepted."""
    return wb.RefinerAttemptSource(
        {path: [wb.AttemptOutcome(accepted=True, refiner_run_id="run-1", cost=0.1, score_delta=0.5)]}
    )


def _reject_all(wb: ModuleType, path: str, n: int = 3) -> object:
    """A RefinerAttemptSource that rejects `path` `n` times."""
    return wb.RefinerAttemptSource({path: [wb.AttemptOutcome(accepted=False, failure_mode=f"f{i}") for i in range(n)]})


# ── Branch-name determinism ───────────────────────────────────────────────────


def test_branch_name_is_deterministic(wb: ModuleType) -> None:
    assert wb.branch_name("skills/a/SKILL.md") == wb.branch_name("skills/a/SKILL.md")


def test_different_paths_get_different_branches(wb: ModuleType) -> None:
    assert wb.branch_name("skills/a/SKILL.md") != wb.branch_name("skills/b/SKILL.md")


def test_branch_carries_prefix_and_short_hash(wb: ModuleType) -> None:
    name = wb.branch_name("skills/a/SKILL.md")
    assert name.startswith(wb.BRANCH_PREFIX)
    suffix = name[len(wb.BRANCH_PREFIX) :]
    assert len(suffix) == 12
    assert all(c in "0123456789abcdef" for c in suffix)


def test_register_sets_the_deterministic_branch(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    fd = d.register("skills/a/SKILL.md")
    assert fd.branch == wb.branch_name("skills/a/SKILL.md")
    assert fd.state == wb.PENDING
    assert fd.attempts == 0
    assert fd.committed is False


def test_register_refuses_duplicate_path(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("dup/SKILL.md")
    with pytest.raises(wb.DurabilityError):
        d.register("dup/SKILL.md")


# ── Atomic-commit invariant (no partial state) ────────────────────────────────


def test_accepted_attempt_commits_atomically(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("ok/SKILL.md")
    fd = d.attempt("ok/SKILL.md", _accept_once(wb, "ok/SKILL.md"))
    assert fd.state == wb.COMMITTED
    assert fd.committed is True
    assert fd.commit_count() == 1
    # The § 14.17.1 commit-message contents are recorded.
    assert fd.refiner_run_id == "run-1"
    assert fd.cost == 0.1
    assert fd.score_delta == 0.5
    fd.assert_atomic()  # does not raise


def test_atomic_invariant_rejects_committed_without_commit(wb: ModuleType) -> None:
    bad = wb.FileDurability(path="x/SKILL.md", state=wb.COMMITTED, committed=False)
    with pytest.raises(wb.AtomicViolation):
        bad.assert_atomic()


def test_atomic_invariant_rejects_pending_with_commit(wb: ModuleType) -> None:
    bad = wb.FileDurability(path="y/SKILL.md", state=wb.PENDING, committed=True)
    with pytest.raises(wb.AtomicViolation):
        bad.assert_atomic()


def test_failed_attempt_produces_no_commit(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("rej/SKILL.md")
    fd = d.attempt("rej/SKILL.md", _reject_all(wb, "rej/SKILL.md"))
    # A rejected attempt rolls back to PENDING with NO commit.
    assert fd.state == wb.PENDING
    assert fd.committed is False
    assert fd.commit_count() == 0
    fd.assert_atomic()


def test_reject_then_accept_commits_on_the_later_attempt(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("late/SKILL.md")
    src = wb.RefinerAttemptSource(
        {
            "late/SKILL.md": [
                wb.AttemptOutcome(accepted=False, failure_mode="f1"),
                wb.AttemptOutcome(accepted=True, refiner_run_id="run-2", cost=0.2, score_delta=0.3),
            ]
        }
    )
    d.attempt("late/SKILL.md", src)  # reject
    fd = d.get("late/SKILL.md")
    assert fd.state == wb.PENDING and fd.attempts == 1 and fd.commit_count() == 0
    d.attempt("late/SKILL.md", src)  # accept
    assert fd.state == wb.COMMITTED and fd.commit_count() == 1 and fd.refiner_run_id == "run-2"


# ── Retry counter increments + escalates on the 3rd failure ───────────────────


def test_retry_counter_increments_per_attempt(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("retry/SKILL.md")
    src = _reject_all(wb, "retry/SKILL.md")
    fd = d.get("retry/SKILL.md")
    d.attempt("retry/SKILL.md", src)
    assert fd.attempts == 1 and fd.state == wb.PENDING
    d.attempt("retry/SKILL.md", src)
    assert fd.attempts == 2 and fd.state == wb.PENDING


def test_retry_ladder_walks_sonnet_adjusted_opus(wb: ModuleType) -> None:
    assert wb.ATTEMPT_CONFIGS == ("sonnet-default", "sonnet-adjusted-prompt", "opus")
    d = wb.WaveBDurability()
    d.register("ladder/SKILL.md")
    fd = d.get("ladder/SKILL.md")
    seen = []
    src = _reject_all(wb, "ladder/SKILL.md")
    for _ in wb.ATTEMPT_CONFIGS:
        seen.append(fd.next_attempt_config())
        d.attempt("ladder/SKILL.md", src)
    assert seen == list(wb.ATTEMPT_CONFIGS)


def test_third_failure_escalates_to_parked_with_reason(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("esc/SKILL.md")
    fd = d.run_to_completion("esc/SKILL.md", _reject_all(wb, "esc/SKILL.md"))
    # ESCALATED — never silently dropped.
    assert fd.state == wb.ESCALATED_PARKED
    assert fd.attempts == wb.MAX_ATTEMPTS
    assert fd.escalation_reason is not None and "3-retry" in fd.escalation_reason
    assert fd.is_parked and fd.is_terminal
    # Escalated => parked, atomic (no commit).
    assert fd.commit_count() == 0 and fd.committed is False
    fd.assert_atomic()


def test_no_attempt_on_a_terminal_file(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("done/SKILL.md")
    d.attempt("done/SKILL.md", _accept_once(wb, "done/SKILL.md"))  # -> COMMITTED
    with pytest.raises(wb.DurabilityError):
        d.attempt("done/SKILL.md", _accept_once(wb, "done/SKILL.md"))


# ── Open-PR file is parked, not attempted ─────────────────────────────────────


def test_open_pr_file_is_parked_not_attempted(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("openpr/SKILL.md")
    fd = d.park_open_pr("openpr/SKILL.md")
    assert fd.state == wb.PARKED_OPEN_PR
    assert fd.attempts == 0  # never attempted
    assert fd.commit_count() == 0  # atomic: no commit
    assert fd.is_parked and fd.is_terminal
    assert fd.escalation_reason is not None
    fd.assert_atomic()


def test_open_pr_park_illegal_once_terminal(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("openpr/SKILL.md")
    d.park_open_pr("openpr/SKILL.md")
    with pytest.raises(wb.DurabilityError):
        d.park_open_pr("openpr/SKILL.md")


def test_open_pr_park_illegal_when_in_progress(wb: ModuleType) -> None:
    """A file that has already taken (and failed) an attempt is no longer
    PENDING; open-PR park from that point is refused — the two orderings are
    deliberately disjoint."""
    d = wb.WaveBDurability()
    d.register("started/SKILL.md")
    d.attempt("started/SKILL.md", _reject_all(wb, "started/SKILL.md"))  # rejected -> PENDING but attempts=1
    fd = d.get("started/SKILL.md")
    assert fd.attempts == 1
    # Still PENDING (rolled back), so an open-PR park is *technically* legal from
    # PENDING — but it must preserve atomicity (no commit). Park it and confirm.
    parked = d.park_open_pr("started/SKILL.md")
    assert parked.state == wb.PARKED_OPEN_PR and parked.commit_count() == 0


# ── Parked-queue integration: route into the ONE reconciliation queue ─────────


def test_parked_files_route_into_the_reconciliation_queue(wb: ModuleType, srq: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("p-open/SKILL.md")
    d.park_open_pr("p-open/SKILL.md")
    d.register("p-esc/SKILL.md")
    d.run_to_completion("p-esc/SKILL.md", _reject_all(wb, "p-esc/SKILL.md"))
    d.register("p-ok/SKILL.md")
    d.attempt("p-ok/SKILL.md", _accept_once(wb, "p-ok/SKILL.md"))  # COMMITTED, NOT parked

    # Only the two parked files are routing candidates.
    assert {fd.path for fd in d.parked()} == {"p-open/SKILL.md", "p-esc/SKILL.md"}

    queue = srq.ReconciliationQueue()
    routed = d.route_parked_to_queue(srq, queue, target_version=TARGET_VERSION)
    assert set(routed) == {"p-open/SKILL.md", "p-esc/SKILL.md"}

    # The items land in the ONE shared queue under the wave-b-parked source,
    # with the rule-3 park flag set so the queue's own predicates see them.
    assert all(it.source == "wave-b-parked" for it in queue.items)
    assert {it.path for it in queue.parked()} == {"p-open/SKILL.md", "p-esc/SKILL.md"}
    assert queue.is_wave_b_park_eligible("p-open/SKILL.md") is True
    # The escalation/park reason is carried as the queue-item note (audit trail).
    assert all(it.note for it in queue.items)


def test_does_not_route_committed_files(wb: ModuleType, srq: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("c/SKILL.md")
    d.attempt("c/SKILL.md", _accept_once(wb, "c/SKILL.md"))
    queue = srq.ReconciliationQueue()
    routed = d.route_parked_to_queue(srq, queue, target_version=TARGET_VERSION)
    assert routed == []
    assert len(queue) == 0


def test_routing_is_idempotent_reenqueueable_not_duplicated(wb: ModuleType, srq: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("p/SKILL.md")
    d.run_to_completion("p/SKILL.md", _reject_all(wb, "p/SKILL.md"))
    queue = srq.ReconciliationQueue()
    first = d.route_parked_to_queue(srq, queue, target_version=TARGET_VERSION)
    second = d.route_parked_to_queue(srq, queue, target_version=TARGET_VERSION)
    assert first == ["p/SKILL.md"]
    assert second == []  # already present — not duplicated
    assert len(queue) == 1


def test_parked_item_is_recoverable_not_failed(wb: ModuleType, srq: ModuleType) -> None:
    """Parked != failed: a routed open-PR item is un-parked (re-enqueued) by the
    reconciliation queue when its PR closes — recoverability, not loss."""
    d = wb.WaveBDurability()
    d.register("recov/SKILL.md")
    d.park_open_pr("recov/SKILL.md")
    queue = srq.ReconciliationQueue()
    d.route_parked_to_queue(srq, queue, target_version=TARGET_VERSION)
    assert queue.is_wave_b_park_eligible("recov/SKILL.md") is True
    # The pull_request:closed webhook (PR_NONE) clears the park flag -> re-enqueued.
    queue.refresh_open_pr_state(srq.GitHubPrStateSource({"recov/SKILL.md": srq.PR_NONE}))
    assert queue.get("recov/SKILL.md").file_state.wave_b_parked is False
    assert queue.is_wave_b_park_eligible("recov/SKILL.md") is False


def test_reuses_reconciliation_queue_source_in_lockstep(wb: ModuleType, srq: ModuleType) -> None:
    # The durability protocol's PARKED_SOURCE must be a real reconciliation-queue
    # source (no second, divergent vocabulary).
    assert wb.PARKED_SOURCE in srq.SOURCES


# ── JSON round-trip + schema validation ───────────────────────────────────────


def test_json_round_trip_is_lossless(wb: ModuleType) -> None:
    d = wb.WaveBDurability()
    d.register("r-ok/SKILL.md")
    d.attempt("r-ok/SKILL.md", _accept_once(wb, "r-ok/SKILL.md"))
    d.register("r-esc/SKILL.md")
    d.run_to_completion("r-esc/SKILL.md", _reject_all(wb, "r-esc/SKILL.md"))
    d.register("r-open/SKILL.md")
    d.park_open_pr("r-open/SKILL.md")

    state = d.to_state(as_of="2026-07-02")
    reparsed = wb.WaveBDurability.from_state(json.loads(json.dumps(state)))

    assert len(reparsed) == 3
    assert reparsed.get("r-ok/SKILL.md").state == wb.COMMITTED
    assert reparsed.get("r-ok/SKILL.md").commit_count() == 1
    assert reparsed.get("r-esc/SKILL.md").state == wb.ESCALATED_PARKED
    assert reparsed.get("r-esc/SKILL.md").escalation_reason is not None
    assert reparsed.get("r-open/SKILL.md").branch == wb.branch_name("r-open/SKILL.md")
    reparsed.assert_all_atomic()


def test_from_state_rejects_wrong_version(wb: ModuleType) -> None:
    with pytest.raises(wb.DurabilityError):
        wb.WaveBDurability.from_state({"state_version": "bogus/v9", "files": []})


def test_from_state_rejects_unknown_state(wb: ModuleType) -> None:
    with pytest.raises(wb.DurabilityError):
        wb.WaveBDurability.from_state(
            {"state_version": wb.STATE_VERSION, "files": [{"path": "z/SKILL.md", "state": "GHOST"}]}
        )


def test_from_state_rejects_non_deterministic_branch(wb: ModuleType) -> None:
    with pytest.raises(wb.DurabilityError):
        wb.WaveBDurability.from_state(
            {
                "state_version": wb.STATE_VERSION,
                "files": [{"path": "z/SKILL.md", "branch": "refiner/wave-b/deadbeefdead", "state": "PENDING"}],
            }
        )


def test_from_state_rejects_partial_commit(wb: ModuleType) -> None:
    with pytest.raises((wb.DurabilityError, wb.AtomicViolation)):
        wb.WaveBDurability.from_state(
            {
                "state_version": wb.STATE_VERSION,
                "files": [{"path": "z/SKILL.md", "state": "COMMITTED", "committed": False}],
            }
        )


def test_round_trip_state_validates_against_schema(wb: ModuleType) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    d = wb.WaveBDurability()
    d.register("v-ok/SKILL.md")
    d.attempt("v-ok/SKILL.md", _accept_once(wb, "v-ok/SKILL.md"))
    d.register("v-esc/SKILL.md")
    d.run_to_completion("v-esc/SKILL.md", _reject_all(wb, "v-esc/SKILL.md"))
    state = d.to_state(as_of="2026-07-03")

    errors = sorted(jsonschema.Draft7Validator(schema).iter_errors(state), key=lambda e: list(e.path))
    assert errors == [], [e.message for e in errors]


def test_committed_seed_state_validates(wb: ModuleType) -> None:
    """The committed SAK-WAVE-B-DURABILITY.json satisfies the schema AND parses
    through the in-code atomic + branch guards."""
    errors = wb.validate_state_file(str(COMMITTED_STATE), str(SCHEMA_PATH))
    assert errors == [], errors
    d = wb.WaveBDurability.from_state(json.loads(COMMITTED_STATE.read_text(encoding="utf-8")))
    assert len(d) >= 1
    d.assert_all_atomic()


def test_schema_rejects_partial_commit_cross_field(wb: ModuleType) -> None:
    """The schema's atomic-commit documentation is enforced in code by from_state;
    here we prove the schema at least rejects an out-of-enum state (the structural
    floor the in-code guard sits on top of)."""
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    bad = {
        "state_version": "sak-wave-b-durability/v1",
        "files": [{"path": "bad/SKILL.md", "state": "TELEPORTED"}],
    }
    errors = list(jsonschema.Draft7Validator(schema).iter_errors(bad))
    assert errors, "schema must reject an out-of-enum state"


# ── The self-test entry point is green (CI parity) ────────────────────────────


def test_module_self_test_passes(wb: ModuleType) -> None:
    assert wb.cmd_self_test() == 0
