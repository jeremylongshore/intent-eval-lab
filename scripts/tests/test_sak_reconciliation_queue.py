"""Unit tests for the SAK reconciliation queue.

Covers the test matrix the brief asks for:
  - enqueue from BOTH sources (wave-a-residue + wave-b-parked) into the ONE queue
  - each of the four dispositions assignable + queryable
  - merge-gate predicate RED for wave_a_pending, GREEN otherwise
  - wave-B-park predicate for an open-PR file
  - pending vs dispositioned filtering
  - queue state round-trips through JSON + validates against the schema

Offline, fixture-driven, no network. The module under test is loaded by file
path via the `srq` session fixture (scripts use hyphenated filenames).

DISTINCT from test_sak_state_machine.py (the Phase-4 flip lifecycle) and from
scripts/reconciliation-liveness.py (the ≤5-business-day liveness SLA timer) —
this exercises the reconciliation QUEUE data structure + disposition logic.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "specs" / "state-machines" / "schema" / "sak-reconciliation-queue.schema.json"
COMMITTED_QUEUE = REPO_ROOT / "SAK-RECONCILIATION-QUEUE.json"

TARGET_VERSION = "authoring/v1@1.0.0"


# ── Fixtures ──────────────────────────────────────────────────────────────────


def _item(
    srq: ModuleType,
    path: str,
    source: str,
    *,
    open_pr: str | None = None,
    wave_a: bool = False,
    wave_b: bool = False,
    disposition: str | None = None,
) -> object:
    """Build a QueueItem with a fully-specified per-file state record."""
    return srq.QueueItem(
        path=path,
        source=source,
        file_state=srq.FileState(
            open_pr_state=srq.PR_NONE if open_pr is None else open_pr,
            wave_a_pending=wave_a,
            wave_b_parked=wave_b,
            target_version=TARGET_VERSION,
        ),
        disposition=srq.PENDING if disposition is None else disposition,
    )


# ── Vocabulary integrity ──────────────────────────────────────────────────────


def test_four_dispositions_are_the_section_14_17_3_set(srq: ModuleType) -> None:
    assert set(srq.DISPOSITIONS) == {
        "keep-as-is",
        "manual-migrate",
        "deprecate-skill",
        "schema-revision-candidate",
    }
    assert srq.PENDING == "pending"
    assert srq.PENDING not in srq.DISPOSITIONS
    assert (srq.PENDING, *srq.DISPOSITIONS) == srq.ALL_DISPOSITIONS


def test_two_shared_queue_sources(srq: ModuleType) -> None:
    assert set(srq.SOURCES) == {"wave-a-residue", "wave-b-parked"}


# ── Enqueue from both sources into the one shared queue ────────────────────────


def test_enqueue_from_both_sources_shares_one_queue(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "a/SKILL.md", "wave-a-residue"))
    q.enqueue(_item(srq, "b/SKILL.md", "wave-b-parked"))
    assert len(q) == 2
    assert len(q.by_source("wave-a-residue")) == 1
    assert len(q.by_source("wave-b-parked")) == 1
    # Both streams are genuinely in ONE container — total == sum of streams.
    assert len(q) == len(q.by_source("wave-a-residue")) + len(q.by_source("wave-b-parked"))


def test_enqueue_refuses_duplicate_path(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "dup/SKILL.md", "wave-a-residue"))
    with pytest.raises(srq.QueueError):
        q.enqueue(_item(srq, "dup/SKILL.md", "wave-b-parked"))


def test_enqueue_refuses_unknown_source(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    with pytest.raises(srq.QueueError):
        q.enqueue(_item(srq, "x/SKILL.md", "wave-c-bogus"))


def test_enqueue_refuses_unknown_open_pr_state(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    with pytest.raises(srq.QueueError):
        q.enqueue(_item(srq, "x/SKILL.md", "wave-a-residue", open_pr="maybe"))


def test_dequeue_removes_then_raises(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "d/SKILL.md", "wave-a-residue"))
    removed = q.dequeue("d/SKILL.md")
    assert removed.path == "d/SKILL.md"
    assert "d/SKILL.md" not in q
    with pytest.raises(srq.QueueError):
        q.dequeue("d/SKILL.md")


# ── Each of the four dispositions assignable + queryable ───────────────────────


def test_each_disposition_assignable_and_queryable(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    for i, _d in enumerate(srq.DISPOSITIONS):
        q.enqueue(_item(srq, f"d{i}/SKILL.md", "wave-a-residue"))
    for i, d in enumerate(srq.DISPOSITIONS):
        item = q.assign_disposition(f"d{i}/SKILL.md", d, at="2026-07-01", note=f"reason-{d}")
        assert item.disposition == d
        assert item.dispositioned_at == "2026-07-01"
        assert item.note == f"reason-{d}"
    # Every disposition is individually queryable.
    for d in srq.DISPOSITIONS:
        rows = q.by_disposition(d)
        assert len(rows) == 1
        assert rows[0].disposition == d


def test_assign_disposition_refuses_pending_sentinel(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "p/SKILL.md", "wave-a-residue"))
    with pytest.raises(srq.QueueError):
        q.assign_disposition("p/SKILL.md", srq.PENDING)


def test_assign_disposition_refuses_unknown_value(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "p/SKILL.md", "wave-a-residue"))
    with pytest.raises(srq.QueueError):
        q.assign_disposition("p/SKILL.md", "ship-it")


def test_assign_disposition_refuses_unqueued_path(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    with pytest.raises(srq.QueueError):
        q.assign_disposition("ghost/SKILL.md", "keep-as-is")


# ── Merge-gate predicate (the sak-wave-a-precedence rule-2 mechanism) ──────────


def test_merge_gate_red_for_wave_a_pending(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "pend/SKILL.md", "wave-a-residue", wave_a=True))
    assert q.blocks_pr_merge("pend/SKILL.md") is True


def test_merge_gate_green_without_wave_a_pending(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "clear/SKILL.md", "wave-a-residue", wave_a=False))
    assert q.blocks_pr_merge("clear/SKILL.md") is False


def test_merge_gate_green_for_unqueued_path(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    # No wave-A op is pending for a path the queue does not track.
    assert q.blocks_pr_merge("ghost/SKILL.md") is False


def test_blocking_pr_merge_lists_exactly_the_red_set(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "red/SKILL.md", "wave-a-residue", wave_a=True))
    q.enqueue(_item(srq, "green/SKILL.md", "wave-a-residue", wave_a=False))
    assert [it.path for it in q.blocking_pr_merge()] == ["red/SKILL.md"]


def test_clear_wave_a_pending_flips_gate_green(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "land/SKILL.md", "wave-a-residue", wave_a=True))
    assert q.blocks_pr_merge("land/SKILL.md") is True
    q.clear_wave_a_pending("land/SKILL.md")
    assert q.blocks_pr_merge("land/SKILL.md") is False
    assert q.blocking_pr_merge() == []


# ── Wave-B-park predicate (the rule-3 mechanism) ──────────────────────────────


def test_wave_b_park_eligible_for_open_pr(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "open/SKILL.md", "wave-b-parked", open_pr=srq.PR_OPEN, wave_b=True))
    assert q.is_wave_b_park_eligible("open/SKILL.md") is True


def test_wave_b_not_park_eligible_without_open_pr(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "none/SKILL.md", "wave-b-parked", open_pr=srq.PR_NONE))
    assert q.is_wave_b_park_eligible("none/SKILL.md") is False
    # An un-queued path is treated as having no open PR.
    assert q.is_wave_b_park_eligible("ghost/SKILL.md") is False


def test_refresh_open_pr_state_sets_and_clears_park(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "p1/SKILL.md", "wave-b-parked", open_pr=srq.PR_NONE))  # will open
    q.enqueue(_item(srq, "p2/SKILL.md", "wave-b-parked", open_pr=srq.PR_OPEN, wave_b=True))  # will close
    src = srq.GitHubPrStateSource({"p1/SKILL.md": srq.PR_OPEN, "p2/SKILL.md": srq.PR_NONE})
    changed = q.refresh_open_pr_state(src)
    assert set(changed) == {"p1/SKILL.md", "p2/SKILL.md"}
    # Newly-open → parked.
    assert q.get("p1/SKILL.md").file_state.wave_b_parked is True
    assert q.is_wave_b_park_eligible("p1/SKILL.md") is True
    # Newly-closed → un-parked (the pull_request:closed re-enqueue path).
    assert q.get("p2/SKILL.md").file_state.wave_b_parked is False
    assert q.is_wave_b_park_eligible("p2/SKILL.md") is False


def test_refresh_does_not_touch_wave_a_pending(srq: ModuleType) -> None:
    # The merge-gate flag is cleared only by wave A LANDING, never by a PR-state
    # refresh — the two orderings are independent.
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "keep/SKILL.md", "wave-a-residue", open_pr=srq.PR_OPEN, wave_a=True))
    q.refresh_open_pr_state(srq.GitHubPrStateSource({"keep/SKILL.md": srq.PR_NONE}))
    assert q.get("keep/SKILL.md").file_state.wave_a_pending is True


# ── pending vs dispositioned filtering ────────────────────────────────────────


def test_pending_vs_dispositioned_filtering(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "still/SKILL.md", "wave-a-residue"))
    q.enqueue(_item(srq, "done/SKILL.md", "wave-b-parked"))
    q.assign_disposition("done/SKILL.md", "keep-as-is")
    assert [it.path for it in q.pending_disposition()] == ["still/SKILL.md"]
    assert [it.path for it in q.dispositioned()] == ["done/SKILL.md"]
    # The two partitions are complementary and exhaustive.
    assert len(q.pending_disposition()) + len(q.dispositioned()) == len(q)


def test_parked_query(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "parked/SKILL.md", "wave-b-parked", open_pr=srq.PR_OPEN, wave_b=True))
    q.enqueue(_item(srq, "live/SKILL.md", "wave-a-residue"))
    assert [it.path for it in q.parked()] == ["parked/SKILL.md"]


# ── JSON round-trip + schema validation ───────────────────────────────────────


def test_json_round_trip_is_lossless(srq: ModuleType) -> None:
    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "r1/SKILL.md", "wave-a-residue", wave_a=True))
    q.enqueue(_item(srq, "r2/SKILL.md", "wave-b-parked", open_pr=srq.PR_OPEN, wave_b=True))
    q.assign_disposition("r1/SKILL.md", "schema-revision-candidate", at="2026-07-02")

    # Serialize → JSON text → parse → from_state, the full committed-file path.
    state = q.to_state(as_of="2026-07-02")
    reparsed = srq.ReconciliationQueue.from_state(json.loads(json.dumps(state)))

    assert len(reparsed) == 2
    assert reparsed.get("r1/SKILL.md").disposition == "schema-revision-candidate"
    # The load-bearing flags survive serialization: the gate + the park.
    assert reparsed.blocks_pr_merge("r1/SKILL.md") is True
    assert reparsed.is_wave_b_park_eligible("r2/SKILL.md") is True
    assert reparsed.get("r1/SKILL.md").file_state.target_version == TARGET_VERSION


def test_from_state_rejects_wrong_version(srq: ModuleType) -> None:
    with pytest.raises(srq.QueueError):
        srq.ReconciliationQueue.from_state({"state_version": "bogus/v9", "items": []})


def test_round_trip_state_validates_against_schema(srq: ModuleType) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    q = srq.ReconciliationQueue()
    q.enqueue(_item(srq, "v1/SKILL.md", "wave-a-residue", wave_a=True))
    q.enqueue(_item(srq, "v2/SKILL.md", "wave-b-parked", open_pr=srq.PR_OPEN, wave_b=True))
    q.assign_disposition("v2/SKILL.md", "deprecate-skill", at="2026-07-03")
    state = q.to_state(as_of="2026-07-03")

    # A generated queue round-trips through the schema with zero errors.
    errors = sorted(jsonschema.Draft7Validator(schema).iter_errors(state), key=lambda e: list(e.path))
    assert errors == [], [e.message for e in errors]


def test_committed_seed_queue_validates(srq: ModuleType) -> None:
    """The committed SAK-RECONCILIATION-QUEUE.json satisfies the schema AND
    parses through the in-code vocabulary guards."""
    errors = srq.validate_queue_file(str(COMMITTED_QUEUE), str(SCHEMA_PATH))
    assert errors == [], errors
    # And it loads through the runtime guards without raising.
    q = srq.ReconciliationQueue.from_state(json.loads(COMMITTED_QUEUE.read_text(encoding="utf-8")))
    assert len(q) >= 1


# ── A bad queue file is REJECTED by the schema (negative case) ─────────────────


def test_schema_rejects_bad_disposition(srq: ModuleType) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    bad = {
        "state_version": "sak-reconciliation-queue/v1",
        "items": [
            {
                "path": "bad/SKILL.md",
                "source": "wave-a-residue",
                "file_state": {
                    "open_pr_state": "none",
                    "wave_a_pending": False,
                    "wave_b_parked": False,
                    "target_version": "authoring/v1@1.0.0",
                },
                "disposition": "ship-it-anyway",
            }
        ],
    }
    errors = list(jsonschema.Draft7Validator(schema).iter_errors(bad))
    assert errors, "schema must reject an out-of-enum disposition"


# ── The self-test entry point is green (CI parity) ────────────────────────────


def test_module_self_test_passes(srq: ModuleType) -> None:
    assert srq.cmd_self_test() == 0
