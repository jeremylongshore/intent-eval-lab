#!/usr/bin/env python3
"""SAK reconciliation queue — Wave A residue + Wave B parked, shared queue.

The reconciliation queue is the SINGLE queue shared between two streams of
files that the Phase-4 corpus migration could not cleanly land:

  - wave-a-residue : a file with WARN-level open issues after the mechanical
                     `batch-remediate` (wave A) ran (plan 033 v7 § 14.17.3).
  - wave-b-parked  : a file the Refiner (wave B) could not migrate after the
                     § 14.17.2 3-retry ladder (Sonnet -> reprompt -> Opus).

Two normative authorities are composed here:

  1. plan 033 v7 § 14.17.3 (the ORIGINAL monthly-review disposition queue):
     every item is dispositioned at SAK AAR cadence (§ 14.13.2) into one of
     FOUR dispositions:
       keep-as-is                file stays valid at a lower tier; coverage-mapped
       manual-migrate            engineer manually edits; lands in next batch
       deprecate-skill           skill marked for removal next CCP minor
       schema-revision-candidate routed to the § 14.A.3 queue; schema may revise

  2. plan 048 v8 Delta 1.1 (which EXTENDS — does not replace — § 14.17.3 with a
     REAL-TIME ENFORCEMENT capability). The monthly-review disposition function
     above is UNCHANGED and runs ALONGSIDE the real-time enforcement. Each
     tracked file carries a per-file state record:

         { open_pr_state: open|none,
           wave_a_pending: bool,
           wave_b_parked:  bool,
           target_version: LATEST_PHASE_4_VERSION }

     over which two PURE PREDICATES decide the migration's two legal write
     orderings:

       - merge-gate (rule-2 mechanism): a file with wave_a_pending == True
         blocks its own PR merge. This is the `sak-wave-a-precedence` required
         CI check; it is RED for any file with a queued, un-landed wave-A op.
         (Wave-B Refiner PRs are exempt-by-construction: wave A always precedes
         wave B for a given file, so a wave-B-eligible file never has
         wave_a_pending set — the gate keys on that flag, so the invariant holds
         without a carve-out.)

       - wave-B-park (rule-3 mechanism): the wave-B dispatcher SKIPS any file
         with open_pr_state == open, sets wave_b_parked = True, and emits no
         Refiner op. The pull_request:closed webhook (merged OR closed) clears
         the park flag and re-enqueues the file. Parked != failed.

This module models the QUEUE DATA STRUCTURE + the DECISION LOGIC only. The
actual GitHub/CI wiring is downstream; the GitHub open-PR state source is
isolated behind a single STUB SEAM (GitHubPrStateSource) a real
`gh pr list --search` adapter would replace.

DISTINCT FROM scripts/reconciliation-liveness.py — that is the ADVISORY
≤5-business-day liveness SLA TIMER (090-AT-SPEC § 5 / plan 033 § 14.16.2). THIS
is the reconciliation QUEUE data structure + the four-disposition + real-time
enforcement logic (plan 033 § 14.17.3 + plan 048 v8 Delta 1.1). Different
artifact.

The module is import-safe and offline. The CLI exposes:
    --self-test            deterministic offline self-test (CI gate)
    --validate <file>      jsonschema-validate a queue JSON against the schema
    --show                 print the queue contents + per-query summary

No network, no writes (the queue is hand-maintained / generated upstream; this
module reads + reasons, it never mutates a committed file).

Stdlib only (jsonschema is an optional import behind --validate). Exit 0 = ok;
1 = self-test / validation failure; 2 = usage / parse error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUEUE = os.path.join(REPO_ROOT, "SAK-RECONCILIATION-QUEUE.json")
SCHEMA_PATH = os.path.join(REPO_ROOT, "specs", "state-machines", "schema", "sak-reconciliation-queue.schema.json")

STATE_VERSION = "sak-reconciliation-queue/v1"

# ── The shared-queue vocabulary ──────────────────────────────────────────────

#: The two streams that share the ONE reconciliation queue (plan 033 § 14.17.3).
SOURCES: tuple[str, ...] = ("wave-a-residue", "wave-b-parked")

#: The four monthly-review dispositions (plan 033 § 14.17.3), plus the
#: not-yet-dispositioned sentinel. `pending` is the default for a fresh item.
PENDING = "pending"
DISPOSITIONS: tuple[str, ...] = (
    "keep-as-is",
    "manual-migrate",
    "deprecate-skill",
    "schema-revision-candidate",
)
#: Every value `disposition` may hold (the four + the pending sentinel).
ALL_DISPOSITIONS: tuple[str, ...] = (PENDING, *DISPOSITIONS)

#: The per-file open-PR state (plan 048 v8 Delta 1.1).
PR_OPEN = "open"
PR_NONE = "none"
OPEN_PR_STATES: tuple[str, ...] = (PR_OPEN, PR_NONE)


# ── Result / state types ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class FileState:
    """The per-file real-time state record (plan 048 v8 Delta 1.1)."""

    open_pr_state: str = PR_NONE
    wave_a_pending: bool = False
    wave_b_parked: bool = False
    target_version: str = ""

    def to_dict(self) -> dict:
        return {
            "open_pr_state": self.open_pr_state,
            "wave_a_pending": self.wave_a_pending,
            "wave_b_parked": self.wave_b_parked,
            "target_version": self.target_version,
        }

    @classmethod
    def from_dict(cls, raw: dict) -> FileState:
        return cls(
            open_pr_state=raw.get("open_pr_state", PR_NONE),
            wave_a_pending=bool(raw.get("wave_a_pending", False)),
            wave_b_parked=bool(raw.get("wave_b_parked", False)),
            target_version=str(raw.get("target_version", "")),
        )


@dataclass
class QueueItem:
    """One reconciliation-queue item — a tracked SKILL.md path with its source,
    per-file real-time state record, and monthly-review disposition."""

    path: str
    source: str
    file_state: FileState
    disposition: str = PENDING
    enqueued_at: str | None = None
    dispositioned_at: str | None = None
    note: str | None = None

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "source": self.source,
            "file_state": self.file_state.to_dict(),
            "disposition": self.disposition,
            "enqueued_at": self.enqueued_at,
            "dispositioned_at": self.dispositioned_at,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, raw: dict) -> QueueItem:
        return cls(
            path=raw["path"],
            source=raw["source"],
            file_state=FileState.from_dict(raw.get("file_state") or {}),
            disposition=raw.get("disposition", PENDING),
            enqueued_at=raw.get("enqueued_at"),
            dispositioned_at=raw.get("dispositioned_at"),
            note=raw.get("note"),
        )


class QueueError(Exception):
    """Raised on an illegal queue mutation (bad source/disposition, dup path,
    missing path)."""


# ── The GitHub-state stub seam ───────────────────────────────────────────────


class GitHubPrStateSource:
    """STUB SEAM — the source of a file's open-PR state.

    Plan 048 v8 Delta 1.1 specifies that `open_pr_state` is refreshed from
    `gh pr list --search "<path>"` on every queue tick (and on the GitHub
    `pull_request` opened/closed webhook). A real adapter would shell out to
    `gh` (or read a webhook payload) here. Until then this offline stub is
    seeded from a hand-supplied {path: "open"|"none"} map so the queue's
    decision logic is testable without a network or a live repo. This single
    class is the ONE place a live GitHub source replaces.
    """

    def __init__(self, open_paths: dict[str, str] | None = None) -> None:
        self._states = dict(open_paths or {})

    def open_pr_state(self, path: str) -> str:
        """Return PR_OPEN / PR_NONE for `path`. Unknown paths default to none."""
        return self._states.get(path, PR_NONE)


# ── The reconciliation queue ─────────────────────────────────────────────────


@dataclass
class ReconciliationQueue:
    """The single shared reconciliation queue (plan 033 § 14.17.3 + plan 048 v8
    Delta 1.1). Holds at most one item per path (keyed on `path`), preserving
    enqueue order. All mutations validate the source / disposition vocabulary
    and refuse duplicate / missing paths."""

    items: list[QueueItem] = field(default_factory=list)

    # ── lookups ──────────────────────────────────────────────────────────────

    def _index_of(self, path: str) -> int:
        for i, it in enumerate(self.items):
            if it.path == path:
                return i
        return -1

    def get(self, path: str) -> QueueItem | None:
        idx = self._index_of(path)
        return self.items[idx] if idx >= 0 else None

    def __contains__(self, path: object) -> bool:
        return isinstance(path, str) and self._index_of(path) >= 0

    def __len__(self) -> int:
        return len(self.items)

    # ── enqueue / dequeue ──────────────────────────────────────────────────────

    def enqueue(self, item: QueueItem) -> QueueItem:
        """Add an item. Refuses an unknown source, an unknown disposition, or a
        duplicate path (the queue holds at most one item per path)."""
        if item.source not in SOURCES:
            raise QueueError(f"unknown source {item.source!r} (must be one of {SOURCES})")
        if item.disposition not in ALL_DISPOSITIONS:
            raise QueueError(f"unknown disposition {item.disposition!r} (must be one of {ALL_DISPOSITIONS})")
        if item.file_state.open_pr_state not in OPEN_PR_STATES:
            raise QueueError(
                f"unknown open_pr_state {item.file_state.open_pr_state!r} (must be one of {OPEN_PR_STATES})"
            )
        if item.path in self:
            raise QueueError(f"path already queued: {item.path!r} (one item per path)")
        self.items.append(item)
        return item

    def dequeue(self, path: str) -> QueueItem:
        """Remove + return the item for `path`. Raises if `path` is not queued.

        Used when a file's reconciliation is fully resolved (the manual edit
        landed, the skill was deprecated, the schema was revised) and it should
        no longer appear in the standing backlog.
        """
        idx = self._index_of(path)
        if idx < 0:
            raise QueueError(f"path not queued: {path!r}")
        return self.items.pop(idx)

    # ── disposition assignment (the § 14.17.3 monthly-review function) ─────────

    def assign_disposition(
        self, path: str, disposition: str, *, at: str | None = None, note: str | None = None
    ) -> QueueItem:
        """Assign one of the four real dispositions to a queued item. Refuses an
        unknown disposition and refuses re-setting an item to `pending` (the
        review moves an item OFF pending, never back onto it). Raises if `path`
        is not queued."""
        if disposition not in DISPOSITIONS:
            raise QueueError(
                f"disposition must be one of {DISPOSITIONS} (got {disposition!r}); "
                "use a real disposition, not the pending sentinel"
            )
        idx = self._index_of(path)
        if idx < 0:
            raise QueueError(f"path not queued: {path!r}")
        item = self.items[idx]
        item.disposition = disposition
        if at is not None:
            item.dispositioned_at = at
        if note is not None:
            item.note = note
        return item

    # ── the real-time enforcement predicates (plan 048 v8 Delta 1.1) ───────────

    def blocks_pr_merge(self, path: str) -> bool:
        """The `sak-wave-a-precedence` merge-gate predicate (rule-2 mechanism).

        A file with a queued, un-landed wave-A op (wave_a_pending == True) BLOCKS
        its own PR merge. Pure over the queue state. An un-queued path never
        blocks (no wave-A op is pending for it). This is the predicate the
        required CI check reads — RED iff this returns True.
        """
        item = self.get(path)
        return bool(item and item.file_state.wave_a_pending)

    def is_wave_b_park_eligible(self, path: str) -> bool:
        """The wave-B-park predicate (rule-3 mechanism).

        The wave-B (Refiner) dispatcher must SKIP — park — any file with an open
        PR (open_pr_state == open). Pure over the queue state. An un-queued path
        is treated as having no open PR (not park-eligible).
        """
        item = self.get(path)
        return bool(item and item.file_state.open_pr_state == PR_OPEN)

    def refresh_open_pr_state(self, source: GitHubPrStateSource) -> list[str]:
        """Re-read every item's open_pr_state from the (stubbed) GitHub source —
        the per-tick / per-webhook refresh of plan 048 v8 Delta 1.1.

        Composes the rule-3 park lifecycle:
          - a file whose PR is now OPEN gets wave_b_parked set True;
          - a file whose PR is now NONE has its park flag cleared (the
            pull_request:closed clear-and-re-enqueue path: parked != failed).

        Returns the list of paths whose open_pr_state changed (for logging /
        re-enqueue scheduling). wave_a_pending is NOT touched here — only wave A
        landing clears that flag (see clear_wave_a_pending).
        """
        changed: list[str] = []
        for it in self.items:
            new_state = source.open_pr_state(it.path)
            if new_state != it.file_state.open_pr_state:
                changed.append(it.path)
            if new_state == PR_OPEN:
                it.file_state = FileState(
                    open_pr_state=PR_OPEN,
                    wave_a_pending=it.file_state.wave_a_pending,
                    wave_b_parked=True,
                    target_version=it.file_state.target_version,
                )
            else:  # PR_NONE — the PR merged or closed; clear the park flag.
                it.file_state = FileState(
                    open_pr_state=PR_NONE,
                    wave_a_pending=it.file_state.wave_a_pending,
                    wave_b_parked=False,
                    target_version=it.file_state.target_version,
                )
        return changed

    def clear_wave_a_pending(self, path: str) -> QueueItem:
        """Clear the wave_a_pending flag for `path` — i.e. wave A LANDED for the
        file, so the `sak-wave-a-precedence` gate goes GREEN and the file's PR
        may merge. Raises if `path` is not queued."""
        idx = self._index_of(path)
        if idx < 0:
            raise QueueError(f"path not queued: {path!r}")
        item = self.items[idx]
        item.file_state = FileState(
            open_pr_state=item.file_state.open_pr_state,
            wave_a_pending=False,
            wave_b_parked=item.file_state.wave_b_parked,
            target_version=item.file_state.target_version,
        )
        return item

    # ── queries (the brief's "what's parked / pending / blocks merge") ─────────

    def parked(self) -> list[QueueItem]:
        """Items the wave-B dispatcher parked (wave_b_parked == True)."""
        return [it for it in self.items if it.file_state.wave_b_parked]

    def pending_disposition(self) -> list[QueueItem]:
        """Items not yet dispositioned (disposition == pending)."""
        return [it for it in self.items if it.disposition == PENDING]

    def dispositioned(self) -> list[QueueItem]:
        """Items that have a real (non-pending) disposition assigned."""
        return [it for it in self.items if it.disposition != PENDING]

    def blocking_pr_merge(self) -> list[QueueItem]:
        """Items whose wave-A op is un-landed and therefore block their PR
        merge (the `sak-wave-a-precedence` RED set)."""
        return [it for it in self.items if it.file_state.wave_a_pending]

    def by_source(self, source: str) -> list[QueueItem]:
        if source not in SOURCES:
            raise QueueError(f"unknown source {source!r} (must be one of {SOURCES})")
        return [it for it in self.items if it.source == source]

    def by_disposition(self, disposition: str) -> list[QueueItem]:
        if disposition not in ALL_DISPOSITIONS:
            raise QueueError(f"unknown disposition {disposition!r}")
        return [it for it in self.items if it.disposition == disposition]

    # ── JSON round-trip ────────────────────────────────────────────────────────

    def to_state(self, *, as_of: str | None = None) -> dict:
        """Serialize to the committed SAK-RECONCILIATION-QUEUE.json shape."""
        state: dict = {"state_version": STATE_VERSION}
        if as_of is not None:
            state["as_of"] = as_of
        state["items"] = [it.to_dict() for it in self.items]
        return state

    @classmethod
    def from_state(cls, state: dict) -> ReconciliationQueue:
        """Parse a queue from the committed JSON shape. Validates the state
        version + the source/disposition vocabulary of every item (mirrors the
        schema's enum constraints in code, so an out-of-band edit is caught even
        without jsonschema installed)."""
        version = state.get("state_version")
        if version != STATE_VERSION:
            raise QueueError(f"state_version must be {STATE_VERSION!r} (got {version!r})")
        q = cls()
        for raw in state.get("items", []):
            item = QueueItem.from_dict(raw)
            # Re-use enqueue() so the same vocabulary + dup-path guards apply.
            q.enqueue(item)
        return q


# ── Schema validation ────────────────────────────────────────────────────────


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def validate_queue_file(queue_path: str, schema_path: str = SCHEMA_PATH) -> list[str]:
    """Validate a queue JSON against the sak-reconciliation-queue schema.
    Returns a list of human-readable error strings (empty == valid)."""
    try:
        import jsonschema
    except ImportError:  # pragma: no cover - environment guard
        return ["jsonschema not installed (pip install jsonschema)"]

    schema = _load_json(schema_path)
    doc = _load_json(queue_path)
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    out = []
    for err in errors:
        loc = "/".join(str(p) for p in err.path) or "<root>"
        out.append(f"{loc}: {err.message}")
    return out


# ── CLI ──────────────────────────────────────────────────────────────────────


def _render_queue(q: ReconciliationQueue) -> str:
    lines = [
        "SAK reconciliation queue (plan 033 § 14.17.3 + plan 048 v8 Delta 1.1)",
        f"  items: {len(q)}  "
        f"(wave-a-residue: {len(q.by_source('wave-a-residue'))}, "
        f"wave-b-parked: {len(q.by_source('wave-b-parked'))})",
        f"  pending disposition: {len(q.pending_disposition())}  dispositioned: {len(q.dispositioned())}",
        f"  parked (wave_b_parked): {len(q.parked())}  "
        f"blocking PR merge (wave_a_pending): {len(q.blocking_pr_merge())}",
    ]
    if not q.items:
        lines.append("  (queue empty)")
        return "\n".join(lines)
    lines.append("  items:")
    for it in q.items:
        fs = it.file_state
        flags = []
        if fs.wave_a_pending:
            flags.append("WAVE-A-PENDING(blocks-merge)")
        if fs.wave_b_parked:
            flags.append("PARKED")
        flag_s = ("  " + " ".join(flags)) if flags else ""
        lines.append(f"    [{it.source:<14}] {it.path}  pr={fs.open_pr_state}  disposition={it.disposition}{flag_s}")
    return "\n".join(lines)


def cmd_show(queue_path: str) -> int:
    if not os.path.exists(queue_path):
        print(f"reconciliation queue not found: {queue_path}", file=sys.stderr)
        return 2
    try:
        state = _load_json(queue_path)
        q = ReconciliationQueue.from_state(state)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"failed to read queue: {exc}", file=sys.stderr)
        return 2
    except QueueError as exc:
        print(f"invalid queue: {exc}", file=sys.stderr)
        return 1
    print(_render_queue(q))
    return 0


def cmd_validate(queue_path: str, schema_path: str) -> int:
    if not os.path.exists(queue_path):
        print(f"reconciliation queue not found: {queue_path}", file=sys.stderr)
        return 2
    errors = validate_queue_file(queue_path, schema_path)
    if errors:
        print(f"sak-reconciliation-queue --validate: FAIL — {queue_path} does not satisfy {schema_path}:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"sak-reconciliation-queue --validate: OK — {queue_path} satisfies {schema_path}")
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

    TV = "authoring/v1@1.0.0"  # a LATEST_PHASE_4_VERSION pin.

    def item(
        path: str,
        source: str,
        *,
        open_pr: str = PR_NONE,
        wave_a: bool = False,
        wave_b: bool = False,
        disposition: str = PENDING,
    ) -> QueueItem:
        return QueueItem(
            path=path,
            source=source,
            file_state=FileState(
                open_pr_state=open_pr,
                wave_a_pending=wave_a,
                wave_b_parked=wave_b,
                target_version=TV,
            ),
            disposition=disposition,
        )

    # 1. Vocabulary integrity: the four dispositions + pending sentinel.
    check(
        "four dispositions are exactly the § 14.17.3 set",
        set(DISPOSITIONS) == {"keep-as-is", "manual-migrate", "deprecate-skill", "schema-revision-candidate"},
    )
    check("pending is not one of the four real dispositions", PENDING not in DISPOSITIONS)
    check("ALL_DISPOSITIONS = pending + the four", (PENDING, *DISPOSITIONS) == ALL_DISPOSITIONS)
    check("two shared-queue sources", set(SOURCES) == {"wave-a-residue", "wave-b-parked"})

    # 2. Enqueue from BOTH sources into the ONE queue.
    q = ReconciliationQueue()
    q.enqueue(item("a/SKILL.md", "wave-a-residue"))
    q.enqueue(item("b/SKILL.md", "wave-b-parked"))
    check("both sources share ONE queue", len(q) == 2)
    check(
        "by_source splits the shared queue",
        len(q.by_source("wave-a-residue")) == 1 and len(q.by_source("wave-b-parked")) == 1,
    )

    # 3. Duplicate path refused (one item per path).
    try:
        q.enqueue(item("a/SKILL.md", "wave-b-parked"))
        check("duplicate path refused", False)
    except QueueError:
        check("duplicate path refused", True)

    # 4. Unknown source / disposition / open_pr_state refused on enqueue.
    for bad in (
        QueueItem("x", "wave-c-bogus", FileState(target_version=TV)),
        QueueItem("y", "wave-a-residue", FileState(target_version=TV), disposition="ship-it"),
        QueueItem("z", "wave-a-residue", FileState(open_pr_state="maybe", target_version=TV)),
    ):
        try:
            ReconciliationQueue().enqueue(bad)
            check(f"bad item refused: {bad.path}", False)
        except QueueError:
            check(f"bad item refused: {bad.path}", True)

    # 5. Each of the four dispositions is assignable + queryable.
    q2 = ReconciliationQueue()
    for i, _d in enumerate(DISPOSITIONS):
        q2.enqueue(item(f"d{i}/SKILL.md", "wave-a-residue"))
    for i, d in enumerate(DISPOSITIONS):
        q2.assign_disposition(f"d{i}/SKILL.md", d, at="2026-07-01", note=f"reason-{d}")
    assigned = {it.path: it.disposition for it in q2.items}
    check("all four dispositions assignable", set(assigned.values()) == set(DISPOSITIONS))
    check("by_disposition queries each", all(len(q2.by_disposition(d)) == 1 for d in DISPOSITIONS))
    check(
        "assign stamps dispositioned_at + note",
        q2.get("d0/SKILL.md").dispositioned_at == "2026-07-01" and q2.get("d0/SKILL.md").note is not None,
    )

    # 6. assign_disposition refuses the pending sentinel + unknown values.
    try:
        q2.assign_disposition("d0/SKILL.md", PENDING)
        check("assign refuses pending sentinel", False)
    except QueueError:
        check("assign refuses pending sentinel", True)
    try:
        q2.assign_disposition("nope/SKILL.md", "keep-as-is")
        check("assign refuses unqueued path", False)
    except QueueError:
        check("assign refuses unqueued path", True)

    # 7. Merge-gate predicate: RED for wave_a_pending, GREEN otherwise.
    qg = ReconciliationQueue()
    qg.enqueue(item("pend/SKILL.md", "wave-a-residue", wave_a=True))
    qg.enqueue(item("clear/SKILL.md", "wave-a-residue", wave_a=False))
    check("merge-gate RED for wave_a_pending", qg.blocks_pr_merge("pend/SKILL.md") is True)
    check("merge-gate GREEN without wave_a_pending", qg.blocks_pr_merge("clear/SKILL.md") is False)
    check("merge-gate GREEN for un-queued path", qg.blocks_pr_merge("ghost/SKILL.md") is False)
    check(
        "blocking_pr_merge query lists exactly the RED set",
        [it.path for it in qg.blocking_pr_merge()] == ["pend/SKILL.md"],
    )

    # 8. clear_wave_a_pending flips the gate GREEN (wave A landed).
    qg.clear_wave_a_pending("pend/SKILL.md")
    check("clearing wave_a_pending flips the gate GREEN", qg.blocks_pr_merge("pend/SKILL.md") is False)
    check("blocking set empty after wave A lands", qg.blocking_pr_merge() == [])

    # 9. Wave-B-park predicate: park-eligible iff open_pr_state == open.
    qp = ReconciliationQueue()
    qp.enqueue(item("open/SKILL.md", "wave-b-parked", open_pr=PR_OPEN, wave_b=True))
    qp.enqueue(item("none/SKILL.md", "wave-b-parked", open_pr=PR_NONE))
    check("park-eligible for open PR", qp.is_wave_b_park_eligible("open/SKILL.md") is True)
    check("not park-eligible for no PR", qp.is_wave_b_park_eligible("none/SKILL.md") is False)
    check("not park-eligible for un-queued path", qp.is_wave_b_park_eligible("ghost") is False)

    # 10. refresh_open_pr_state composes the park lifecycle (set + clear).
    qr = ReconciliationQueue()
    qr.enqueue(item("p1/SKILL.md", "wave-b-parked", open_pr=PR_NONE))  # will open
    qr.enqueue(item("p2/SKILL.md", "wave-b-parked", open_pr=PR_OPEN, wave_b=True))  # will close
    src = GitHubPrStateSource({"p1/SKILL.md": PR_OPEN, "p2/SKILL.md": PR_NONE})
    changed = qr.refresh_open_pr_state(src)
    check("refresh reports both changed paths", set(changed) == {"p1/SKILL.md", "p2/SKILL.md"})
    check(
        "newly-open file is parked",
        qr.get("p1/SKILL.md").file_state.wave_b_parked is True and qr.is_wave_b_park_eligible("p1/SKILL.md") is True,
    )
    check(
        "newly-closed file is un-parked (re-enqueue path; parked != failed)",
        qr.get("p2/SKILL.md").file_state.wave_b_parked is False and qr.is_wave_b_park_eligible("p2/SKILL.md") is False,
    )

    # 11. refresh does NOT touch wave_a_pending (only wave A landing clears it).
    qa = ReconciliationQueue()
    qa.enqueue(item("keepA/SKILL.md", "wave-a-residue", open_pr=PR_OPEN, wave_a=True))
    qa.refresh_open_pr_state(GitHubPrStateSource({"keepA/SKILL.md": PR_NONE}))
    check("refresh leaves wave_a_pending intact", qa.get("keepA/SKILL.md").file_state.wave_a_pending is True)

    # 12. parked() / pending_disposition() / dispositioned() queries.
    qq = ReconciliationQueue()
    qq.enqueue(item("k1/SKILL.md", "wave-b-parked", open_pr=PR_OPEN, wave_b=True))
    qq.enqueue(item("k2/SKILL.md", "wave-a-residue"))
    qq.assign_disposition("k2/SKILL.md", "keep-as-is")
    check("parked() lists the parked item", [it.path for it in qq.parked()] == ["k1/SKILL.md"])
    check(
        "pending_disposition() lists the un-dispositioned item",
        [it.path for it in qq.pending_disposition()] == ["k1/SKILL.md"],
    )
    check("dispositioned() lists the dispositioned item", [it.path for it in qq.dispositioned()] == ["k2/SKILL.md"])

    # 13. dequeue removes an item; second dequeue raises.
    qq.dequeue("k1/SKILL.md")
    check("dequeue removes the item", "k1/SKILL.md" not in qq)
    try:
        qq.dequeue("k1/SKILL.md")
        check("dequeue of un-queued path raises", False)
    except QueueError:
        check("dequeue of un-queued path raises", True)

    # 14. JSON round-trip is lossless + re-applies the vocabulary guards.
    qj = ReconciliationQueue()
    qj.enqueue(item("r1/SKILL.md", "wave-a-residue", wave_a=True))
    qj.enqueue(item("r2/SKILL.md", "wave-b-parked", open_pr=PR_OPEN, wave_b=True))
    qj.assign_disposition("r1/SKILL.md", "schema-revision-candidate", at="2026-07-02")
    state = qj.to_state(as_of="2026-07-02")
    round_tripped = ReconciliationQueue.from_state(json.loads(json.dumps(state)))
    check("round-trip preserves item count", len(round_tripped) == 2)
    check(
        "round-trip preserves disposition", round_tripped.get("r1/SKILL.md").disposition == "schema-revision-candidate"
    )
    check(
        "round-trip preserves wave_a_pending (gate survives serialization)",
        round_tripped.blocks_pr_merge("r1/SKILL.md") is True,
    )
    check("round-trip preserves park flag", round_tripped.is_wave_b_park_eligible("r2/SKILL.md") is True)

    # 15. from_state rejects a wrong state_version.
    try:
        ReconciliationQueue.from_state({"state_version": "bogus/v9", "items": []})
        check("from_state rejects wrong version", False)
    except QueueError:
        check("from_state rejects wrong version", True)

    # 16. The committed seed queue (if present) validates against the schema.
    if os.path.exists(DEFAULT_QUEUE) and os.path.exists(SCHEMA_PATH):
        errs = validate_queue_file(DEFAULT_QUEUE, SCHEMA_PATH)
        check("committed SAK-RECONCILIATION-QUEUE.json validates against the schema", errs == [])
        # And it parses cleanly through the in-code vocabulary guards.
        ReconciliationQueue.from_state(_load_json(DEFAULT_QUEUE))
        check("committed queue parses through the in-code guards", True)

    print()
    if failures:
        print(f"self-test: {failures} FAILURE(S).")
        return 1
    print(
        "self-test: shared-queue enqueue/dequeue, four dispositions, merge-gate "
        "(wave_a_pending) + wave-B-park (open-PR) predicates, refresh lifecycle, "
        "queries, and JSON round-trip all sound."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="SAK reconciliation queue — Wave A residue + Wave B parked, "
        "4 dispositions + real-time enforcement predicates."
    )
    parser.add_argument("--self-test", action="store_true", help="run the deterministic offline self-test (CI gate)")
    parser.add_argument("--validate", action="store_true", help="jsonschema-validate a queue JSON against the schema")
    parser.add_argument("--show", action="store_true", help="print the queue contents + per-query summary")
    parser.add_argument("--queue", default=DEFAULT_QUEUE, help="path to SAK-RECONCILIATION-QUEUE.json")
    parser.add_argument("--schema", default=SCHEMA_PATH, help="path to the sak-reconciliation-queue schema")
    args = parser.parse_args(argv)

    if args.self_test:
        return cmd_self_test()
    if args.validate:
        return cmd_validate(args.queue, args.schema)
    if args.show:
        return cmd_show(args.queue)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
