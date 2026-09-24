#!/usr/bin/env python3
"""SAK Wave-B durability protocol — per-file branch + atomic commit + 3-retry.

The DURABILITY half of the Wave-B (Refiner / eval-loop) wave of the Phase-4 SAK
corpus migration. Wave B refines one SKILL.md file at a time; this protocol
makes each file's refinement DURABLE and RECOVERABLE so a failure parks the file
(re-enqueueable) rather than silently dropping it. It is the "side-branch +
atomic + 3-retry + parked-queue" mechanism of F-MK-004.

Normative authority (all in 000-docs/):
  - plan 033 v7 § 14.17.1 — per-file branch + atomic commit:
      * branch name `refiner/wave-b/<file-hash>`
      * a single commit per ACCEPTED edit (Refiner-run-ID + cost + score-delta)
      * a FAILED attempt produces NO commit (rolled back at the working tree)
      * a SUCCESSFUL attempt produces one commit + a PR auto-merged after
        validate-plugins.yml passes
  - plan 033 v7 § 14.17.2 — 3-retry + parked queue:
      * attempt 1: standard Refiner config (Sonnet + default eval set)
      * attempt 2 (if 1 fails): retry with an adjusted prompt (clarifies the
        failure mode)
      * attempt 3 (if 2 fails): retry with Opus
      * 3 failures: the file is PARKED for manual review (ESCALATION) — never
        silently dropped.
  - plan 048 v8 Delta 1 — "Wave B never on open-PR files": a file with an open
    PR is PARKED before any attempt, and re-enqueued when the PR merges/closes.
  - plan 048 v8 § 14.17 — "parked ≠ failed": a parked item is re-enqueued, not
    lost. The reconciliation queue (scripts/sak-reconciliation-queue.py) owns the
    parked set; this protocol ROUTES into it, it does not build a second queue.

What this module models vs. what it does NOT do:
  - MODELS the durability-protocol DECISIONS as state: the deterministic branch
    name, the per-file attempt lifecycle (the atomic-commit state), the 3-retry
    ladder + escalation, and the routing of parked files into the reconciliation
    queue's parked set.
  - DOES NOT perform git/GitHub side effects: the actual branch/commit/PR
    operations are downstream and isolated behind a single STUB SEAM
    (RefinerAttemptSource), exactly as the sibling scripts isolate the GitHub
    open-PR state (GitHubPrStateSource) and the governance sign-off
    (load_signoff_from_state). This module decides; it does not execute.

ATOMIC-COMMIT INVARIANT (the load-bearing durability guarantee): a Wave-B result
for a file is EITHER fully committed (exactly one commit on the per-file branch)
OR not at all (no commit, working tree rolled back) — never a partial state. The
lifecycle below makes "in flight" a distinct, non-terminal state, and every
terminal state asserts the invariant (COMMITTED ⇒ 1 commit; every other terminal
⇒ 0 commits). assert_atomic() enforces it in code.

PARKED-QUEUE INTEGRATION: when a file cannot complete — it has an open PR (Delta
1: never on open-PR files) OR it has exhausted the 3-retry ladder (§ 14.17.2) —
it is routed to the reconciliation queue's `wave-b-parked` set via that module's
own FileState / QueueItem / is_wave_b_park_eligible. There is exactly ONE parked
queue; this protocol reuses it.

The module is import-safe and offline. The CLI exposes:
    --self-test            deterministic offline self-test (CI gate)
    --validate <file>      jsonschema-validate a durability-state JSON vs. schema
    --show                 print the lifecycle + retry ladder + a state, if any

Stdlib only (jsonschema is an optional import behind --validate). Exit 0 = ok;
1 = self-test / validation failure; 2 = usage / parse error.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from dataclasses import dataclass, field
from types import ModuleType

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_STATE = os.path.join(REPO_ROOT, "SAK-WAVE-B-DURABILITY.json")
SCHEMA_PATH = os.path.join(REPO_ROOT, "specs", "state-machines", "schema", "sak-wave-b-durability.schema.json")
RECONCILIATION_QUEUE_PATH = os.path.join(REPO_ROOT, "scripts", "sak-reconciliation-queue.py")

STATE_VERSION = "sak-wave-b-durability/v1"

#: The per-file branch prefix (plan 033 § 14.17.1). The full branch name is
#: f"{BRANCH_PREFIX}{file_hash(path)}".
BRANCH_PREFIX = "refiner/wave-b/"

#: The maximum number of Refiner attempts before escalation (plan 033 § 14.17.2:
#: attempt 1 Sonnet, attempt 2 adjusted-prompt, attempt 3 Opus, then park).
MAX_ATTEMPTS = 3

#: The reconciliation-queue source a parked Wave-B file lands under. Mirrors
#: sak-reconciliation-queue's SOURCES — kept as a named constant so the two
#: stay in lock-step (validated against the imported module in the self-test).
PARKED_SOURCE = "wave-b-parked"


# ── The lifecycle (plan 033 § 14.17.1 + § 14.17.2) ───────────────────────────

#: A file enters PENDING, optionally goes PARKED-OPEN-PR (never attempted), else
#: walks the attempt ladder via IN-FLIGHT; an accepted edit -> COMMITTED, a
#: rejected/failed edit rolls the working tree back to PENDING for the next
#: attempt; 3 failures -> ESCALATED-PARKED (routed to the reconciliation queue).
PENDING = "PENDING"
IN_FLIGHT = "IN-FLIGHT"
COMMITTED = "COMMITTED"
PARKED_OPEN_PR = "PARKED-OPEN-PR"
ESCALATED_PARKED = "ESCALATED-PARKED"

STATES: tuple[str, ...] = (PENDING, IN_FLIGHT, COMMITTED, PARKED_OPEN_PR, ESCALATED_PARKED)

#: Terminal states (no further attempt is made).
TERMINAL_STATES: frozenset[str] = frozenset({COMMITTED, PARKED_OPEN_PR, ESCALATED_PARKED})

#: The two terminal states that route the file into the reconciliation queue's
#: parked set ("parked ≠ failed" — both are re-enqueueable).
PARKED_STATES: frozenset[str] = frozenset({PARKED_OPEN_PR, ESCALATED_PARKED})

#: The per-attempt Refiner config (plan 033 § 14.17.2). Index = attempt number-1.
ATTEMPT_CONFIGS: tuple[str, ...] = (
    "sonnet-default",  # attempt 1: standard config (Sonnet + default eval set)
    "sonnet-adjusted-prompt",  # attempt 2: retry with adjusted prompt
    "opus",  # attempt 3: retry with Opus
)


# ── Deterministic branch derivation (plan 033 § 14.17.1) ─────────────────────


def file_hash(path: str) -> str:
    """Deterministic short hash of a file PATH (not content) for the branch name.

    The branch name must be derivable from the path alone so the dispatcher can
    address a file's branch without reading its content (and so two runs over the
    same path produce the same branch — recoverability). Uses a sha256 over the
    UTF-8 path, truncated to 12 hex chars (collision-safe at corpus scale ~3.5k
    files: 12 hex = 48 bits). Stable + offline.
    """
    return hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]


def branch_name(path: str) -> str:
    """The per-file Wave-B branch name `refiner/wave-b/<file-hash>` (§ 14.17.1)."""
    return f"{BRANCH_PREFIX}{file_hash(path)}"


# ── Result / state types ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class AtomicViolation(Exception):
    """Raised when a durability state violates the atomic-commit invariant
    (a COMMITTED file without exactly one commit, or a non-COMMITTED file with
    a commit). A bug-catcher: the lifecycle should make this unreachable."""

    message: str

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.message


class DurabilityError(Exception):
    """Raised on an illegal durability mutation (bad transition, unknown
    state, duplicate/missing path)."""


@dataclass
class FileDurability:
    """The per-file Wave-B durability record.

    Fields:
      - path            : the SKILL.md path being refined.
      - branch          : the deterministic `refiner/wave-b/<hash>` branch.
      - state           : one of STATES.
      - attempts        : how many Refiner attempts have been made (0..MAX_ATTEMPTS).
      - committed       : True iff exactly one commit landed on the branch
                          (the atomic-commit success flag — COMMITTED ⇔ True).
      - escalation_reason: set when the file parks (open-PR or 3-retry exhaustion).
      - refiner_run_id / cost / score_delta: recorded on a COMMITTED edit
                          (the § 14.17.1 commit-message contents).
    """

    path: str
    branch: str = ""
    state: str = PENDING
    attempts: int = 0
    committed: bool = False
    escalation_reason: str | None = None
    refiner_run_id: str | None = None
    cost: float | None = None
    score_delta: float | None = None
    last_failure_mode: str | None = None

    def __post_init__(self) -> None:
        if not self.branch:
            self.branch = branch_name(self.path)

    # ── invariant ───────────────────────────────────────────────────────────

    def commit_count(self) -> int:
        """The number of commits on the per-file branch implied by this state.

        Atomic by construction: a COMMITTED file has exactly ONE commit; every
        other state has ZERO (a failed attempt is rolled back at the working
        tree, never committed; a parked file was never attempted-to-completion).
        """
        return 1 if self.state == COMMITTED else 0

    def assert_atomic(self) -> None:
        """Enforce the atomic-commit invariant; raise AtomicViolation if broken.

        COMMITTED  ⇔ committed is True ⇔ commit_count() == 1
        otherwise  ⇔ committed is False ⇔ commit_count() == 0
        No partial state is representable.
        """
        if self.state == COMMITTED:
            if not self.committed or self.commit_count() != 1:
                raise AtomicViolation(
                    f"{self.path!r}: COMMITTED must have committed=True and exactly 1 commit "
                    f"(committed={self.committed}, commits={self.commit_count()})"
                )
        else:
            if self.committed or self.commit_count() != 0:
                raise AtomicViolation(
                    f"{self.path!r}: non-COMMITTED state {self.state!r} must have committed=False and 0 commits "
                    f"(committed={self.committed}, commits={self.commit_count()})"
                )

    @property
    def is_terminal(self) -> bool:
        return self.state in TERMINAL_STATES

    @property
    def is_parked(self) -> bool:
        return self.state in PARKED_STATES

    @property
    def retries_remaining(self) -> int:
        return max(0, MAX_ATTEMPTS - self.attempts)

    def next_attempt_config(self) -> str | None:
        """The Refiner config for the NEXT attempt, or None if the ladder is
        exhausted (attempts == MAX_ATTEMPTS)."""
        if self.attempts >= MAX_ATTEMPTS:
            return None
        return ATTEMPT_CONFIGS[self.attempts]

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "branch": self.branch,
            "state": self.state,
            "attempts": self.attempts,
            "committed": self.committed,
            "escalation_reason": self.escalation_reason,
            "refiner_run_id": self.refiner_run_id,
            "cost": self.cost,
            "score_delta": self.score_delta,
            "last_failure_mode": self.last_failure_mode,
        }

    @classmethod
    def from_dict(cls, raw: dict) -> FileDurability:
        path = raw["path"]
        fd = cls(
            path=path,
            branch=raw.get("branch") or branch_name(path),
            state=raw.get("state", PENDING),
            attempts=int(raw.get("attempts", 0)),
            committed=bool(raw.get("committed", False)),
            escalation_reason=raw.get("escalation_reason"),
            refiner_run_id=raw.get("refiner_run_id"),
            cost=raw.get("cost"),
            score_delta=raw.get("score_delta"),
            last_failure_mode=raw.get("last_failure_mode"),
        )
        if fd.state not in STATES:
            raise DurabilityError(f"unknown state {fd.state!r} for {path!r} (must be one of {STATES})")
        if fd.branch != branch_name(path):
            raise DurabilityError(
                f"branch {fd.branch!r} for {path!r} does not match the deterministic {branch_name(path)!r}"
            )
        fd.assert_atomic()
        return fd


# ── The Refiner-attempt stub seam ────────────────────────────────────────────


@dataclass(frozen=True)
class AttemptOutcome:
    """The outcome of one Refiner attempt (what the real Refiner returns)."""

    accepted: bool
    refiner_run_id: str | None = None
    cost: float | None = None
    score_delta: float | None = None
    failure_mode: str | None = None


class RefinerAttemptSource:
    """STUB SEAM — the source of a Refiner attempt's outcome.

    The real Wave-B dispatcher would (a) check out the per-file branch, (b) run
    the Refiner with the attempt's config, and (c) on acceptance commit + open a
    PR, or on rejection roll the working tree back. A real adapter shells out to
    git + the Refiner here. Until then this offline stub is seeded from a
    hand-supplied {path: [AttemptOutcome, ...]} map so the durability protocol's
    DECISION logic is testable without git or a live Refiner. This single class
    is the ONE place a live Refiner/git source replaces.
    """

    def __init__(self, outcomes: dict[str, list[AttemptOutcome]] | None = None) -> None:
        self._outcomes: dict[str, list[AttemptOutcome]] = {k: list(v) for k, v in (outcomes or {}).items()}

    def run_attempt(self, path: str, config: str, attempt_no: int) -> AttemptOutcome:
        """Return the outcome of attempt `attempt_no` (1-indexed) for `path`.

        Unknown paths / exhausted scripted outcomes default to a rejection (the
        conservative default — a missing outcome must never be read as success).
        """
        seq = self._outcomes.get(path)
        if not seq or attempt_no > len(seq):
            return AttemptOutcome(accepted=False, failure_mode="no-outcome-scripted")
        return seq[attempt_no - 1]


# ── The durability protocol ──────────────────────────────────────────────────


@dataclass
class WaveBDurability:
    """The Wave-B durability protocol over a set of per-file records.

    Holds at most one record per path (keyed on `path`), preserving insert
    order. Owns the branch model, the atomic-commit lifecycle, the 3-retry
    ladder + escalation, and the routing of parked files into the
    reconciliation queue's parked set. The reconciliation-queue module is the
    SINGLE parked queue; this protocol composes with it (it does not duplicate
    it).
    """

    files: list[FileDurability] = field(default_factory=list)

    # ── lookups ──────────────────────────────────────────────────────────────

    def _index_of(self, path: str) -> int:
        for i, fd in enumerate(self.files):
            if fd.path == path:
                return i
        return -1

    def get(self, path: str) -> FileDurability | None:
        idx = self._index_of(path)
        return self.files[idx] if idx >= 0 else None

    def __contains__(self, path: object) -> bool:
        return isinstance(path, str) and self._index_of(path) >= 0

    def __len__(self) -> int:
        return len(self.files)

    # ── registration ──────────────────────────────────────────────────────────

    def register(self, path: str) -> FileDurability:
        """Track a new file for Wave-B refinement. Refuses a duplicate path
        (one record per path). The file starts PENDING with 0 attempts on its
        deterministic branch."""
        if path in self:
            raise DurabilityError(f"path already tracked: {path!r} (one record per path)")
        fd = FileDurability(path=path)
        fd.assert_atomic()
        self.files.append(fd)
        return fd

    # ── the open-PR park (plan 048 v8 Delta 1: never on open-PR files) ─────────

    def park_open_pr(self, path: str, *, reason: str | None = None) -> FileDurability:
        """Park a file BEFORE any attempt because it has an open PR (Delta 1).

        Legal only from PENDING (an in-flight or terminal file is not re-parked
        here). The file moves to PARKED-OPEN-PR; no attempt is made and no commit
        is produced (atomic invariant preserved). Re-enqueued by the
        reconciliation queue when the PR merges/closes. Parked ≠ failed.
        """
        fd = self._require(path)
        if fd.state != PENDING:
            raise DurabilityError(
                f"open-PR park is legal only from PENDING (got {fd.state!r} for {path!r}); "
                "a file already in-flight or terminal is not re-parked here"
            )
        fd.state = PARKED_OPEN_PR
        fd.escalation_reason = reason or "open-PR: Wave B never runs on a file with an open PR (plan 048 Delta 1)"
        fd.assert_atomic()
        return fd

    # ── one Refiner attempt (the 3-retry ladder, § 14.17.2) ───────────────────

    def attempt(self, path: str, source: RefinerAttemptSource) -> FileDurability:
        """Run the next Refiner attempt for `path` and apply the outcome.

        Walks the § 14.17.2 ladder:
          - acceptance  -> COMMITTED (one atomic commit; records run-id/cost/delta).
          - rejection   -> increment the attempt counter; roll back to PENDING
                           for the next attempt; on the 3rd rejection ESCALATE
                           (-> ESCALATED-PARKED, routed to the reconciliation
                           queue's parked set).

        Refuses an attempt on a terminal file (committed or parked). The
        atomic-commit invariant holds at every step: a rejected attempt never
        commits; only an accepted attempt commits, exactly once.
        """
        fd = self._require(path)
        if fd.is_terminal:
            raise DurabilityError(
                f"no attempt on a terminal file: {path!r} is {fd.state!r} "
                f"({'committed' if fd.state == COMMITTED else 'parked'})"
            )
        if fd.attempts >= MAX_ATTEMPTS:  # pragma: no cover - defensive; escalation fires at the 3rd failure
            raise DurabilityError(f"retry ladder exhausted for {path!r} but state is {fd.state!r}, not escalated")

        config = ATTEMPT_CONFIGS[fd.attempts]
        attempt_no = fd.attempts + 1
        fd.state = IN_FLIGHT
        outcome = source.run_attempt(path, config, attempt_no)
        fd.attempts = attempt_no

        if outcome.accepted:
            # Atomic success: exactly one commit lands; record the § 14.17.1
            # commit-message contents.
            fd.state = COMMITTED
            fd.committed = True
            fd.refiner_run_id = outcome.refiner_run_id
            fd.cost = outcome.cost
            fd.score_delta = outcome.score_delta
            fd.last_failure_mode = None
            fd.assert_atomic()
            return fd

        # Rejection: NO commit (rolled back at the working tree). Record the
        # failure mode (informs the next attempt's adjusted prompt).
        fd.committed = False
        fd.last_failure_mode = outcome.failure_mode
        if fd.attempts >= MAX_ATTEMPTS:
            # 3rd failure -> ESCALATE (never silently dropped).
            fd.state = ESCALATED_PARKED
            fd.escalation_reason = (
                f"3-retry ladder exhausted ({MAX_ATTEMPTS} failed attempts); "
                f"last failure mode: {outcome.failure_mode or 'unknown'} (plan 033 § 14.17.2)"
            )
        else:
            # Roll back to PENDING for the next attempt (working tree clean).
            fd.state = PENDING
        fd.assert_atomic()
        return fd

    def run_to_completion(self, path: str, source: RefinerAttemptSource) -> FileDurability:
        """Drive a file through the full ladder until it reaches a terminal state
        (COMMITTED or ESCALATED-PARKED). A convenience over repeated attempt()."""
        fd = self._require(path)
        while not fd.is_terminal:
            self.attempt(path, source)
        return fd

    def _require(self, path: str) -> FileDurability:
        fd = self.get(path)
        if fd is None:
            raise DurabilityError(f"path not tracked: {path!r}")
        return fd

    # ── queries ────────────────────────────────────────────────────────────────

    def committed(self) -> list[FileDurability]:
        return [fd for fd in self.files if fd.state == COMMITTED]

    def parked(self) -> list[FileDurability]:
        """Every parked file (open-PR + escalated) — the reconciliation-queue
        routing set. Parked ≠ failed: all are re-enqueueable."""
        return [fd for fd in self.files if fd.is_parked]

    def escalated(self) -> list[FileDurability]:
        return [fd for fd in self.files if fd.state == ESCALATED_PARKED]

    def open_pr_parked(self) -> list[FileDurability]:
        return [fd for fd in self.files if fd.state == PARKED_OPEN_PR]

    def in_progress(self) -> list[FileDurability]:
        return [fd for fd in self.files if fd.state in (PENDING, IN_FLIGHT)]

    def assert_all_atomic(self) -> None:
        for fd in self.files:
            fd.assert_atomic()

    # ── parked-queue integration (the ONE reconciliation queue) ───────────────

    def to_reconciliation_items(self, srq: ModuleType, *, target_version: str) -> list[object]:
        """Build reconciliation-queue items for every parked file, REUSING the
        reconciliation-queue module's FileState / QueueItem (do not re-implement).

        Each parked file becomes a `wave-b-parked` QueueItem whose FileState has
        wave_b_parked=True (the rule-3 park flag), so the queue's
        is_wave_b_park_eligible / parked() see it. open-PR-parked files set
        open_pr_state=open (the queue can clear them on PR close); escalated
        files set open_pr_state=none (no PR — they wait for manual review).
        The escalation_reason becomes the item note. This is the single bridge
        from durability → the one parked queue.
        """
        items: list[object] = []
        for fd in self.parked():
            open_pr = srq.PR_OPEN if fd.state == PARKED_OPEN_PR else srq.PR_NONE
            file_state = srq.FileState(
                open_pr_state=open_pr,
                wave_a_pending=False,  # wave A always precedes wave B for a file (Delta 1.1 invariant)
                wave_b_parked=True,
                target_version=target_version,
            )
            items.append(
                srq.QueueItem(
                    path=fd.path,
                    source=PARKED_SOURCE,
                    file_state=file_state,
                    disposition=srq.PENDING,
                    note=fd.escalation_reason,
                )
            )
        return items

    def route_parked_to_queue(self, srq: ModuleType, queue: object, *, target_version: str) -> list[str]:
        """Enqueue every parked file into the GIVEN reconciliation queue (the ONE
        shared queue), skipping any path already present. Returns the paths newly
        routed. Re-enqueueable: parked ≠ failed.
        """
        routed: list[str] = []
        for item in self.to_reconciliation_items(srq, target_version=target_version):
            if item.path in queue:  # type: ignore[operator]  # queue.__contains__ takes str
                continue
            queue.enqueue(item)  # type: ignore[attr-defined]
            routed.append(item.path)  # type: ignore[attr-defined]
        return routed

    # ── JSON round-trip ────────────────────────────────────────────────────────

    def to_state(self, *, as_of: str | None = None) -> dict:
        """Serialize to the committed SAK-WAVE-B-DURABILITY.json shape."""
        state: dict = {"state_version": STATE_VERSION}
        if as_of is not None:
            state["as_of"] = as_of
        state["files"] = [fd.to_dict() for fd in self.files]
        return state

    @classmethod
    def from_state(cls, state: dict) -> WaveBDurability:
        """Parse from the committed JSON shape. Validates the state version, the
        per-file state vocabulary, the deterministic branch name, and the
        atomic-commit invariant of every record (mirrors the schema in code, so
        an out-of-band edit is caught even without jsonschema installed)."""
        version = state.get("state_version")
        if version != STATE_VERSION:
            raise DurabilityError(f"state_version must be {STATE_VERSION!r} (got {version!r})")
        d = cls()
        for raw in state.get("files", []):
            fd = FileDurability.from_dict(raw)
            if fd.path in d:
                raise DurabilityError(f"duplicate path in state: {fd.path!r}")
            d.files.append(fd)
        return d


# ── reconciliation-queue module loader (reuse, never reimplement) ────────────


def load_reconciliation_queue_module(path: str = RECONCILIATION_QUEUE_PATH) -> ModuleType:
    """Load scripts/sak-reconciliation-queue.py by file path (hyphenated
    filename; not importable by name). This is the ONE parked queue — we reuse
    its FileState / QueueItem / predicates, never re-implement them."""
    spec = importlib.util.spec_from_file_location("sak_reconciliation_queue", path)
    if spec is None or spec.loader is None:  # pragma: no cover - import guard
        raise RuntimeError(f"cannot load reconciliation-queue module at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("sak_reconciliation_queue", module)
    spec.loader.exec_module(module)
    return module


# ── Schema validation ────────────────────────────────────────────────────────


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def validate_state_file(state_path: str, schema_path: str = SCHEMA_PATH) -> list[str]:
    """Validate a durability-state JSON against the sak-wave-b-durability schema.
    Returns a list of human-readable error strings (empty == valid)."""
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


def _print_lifecycle() -> None:
    print("SAK Wave-B durability — lifecycle (plan 033 § 14.17.1 + § 14.17.2):")
    print(f"  branch model     : {BRANCH_PREFIX}<sha256(path)[:12]>  (deterministic, path-derived)")
    print(f"  states           : {' -> '.join(STATES)}")
    print(f"  terminal         : {', '.join(sorted(TERMINAL_STATES))}")
    print(f"  parked (re-enqueueable): {', '.join(sorted(PARKED_STATES))}")
    print("  3-retry ladder   :")
    for i, cfg in enumerate(ATTEMPT_CONFIGS, start=1):
        print(f"    attempt {i}: {cfg}")
    print(f"    {MAX_ATTEMPTS} failures -> ESCALATED-PARKED (routed to the reconciliation queue; parked ≠ failed)")
    print("  atomic-commit invariant: COMMITTED ⇔ exactly 1 commit; every other state ⇔ 0 commits.")


def _render_state(d: WaveBDurability) -> str:
    lines = [
        "SAK Wave-B durability state",
        f"  files: {len(d)}  "
        f"(committed: {len(d.committed())}, escalated-parked: {len(d.escalated())}, "
        f"open-PR-parked: {len(d.open_pr_parked())}, in-progress: {len(d.in_progress())})",
    ]
    if not d.files:
        lines.append("  (no files tracked)")
        return "\n".join(lines)
    for fd in d.files:
        extra = f"  reason={fd.escalation_reason}" if fd.escalation_reason else ""
        lines.append(
            f"    {fd.path}  branch={fd.branch}  state={fd.state}  "
            f"attempts={fd.attempts}/{MAX_ATTEMPTS}  committed={fd.committed}{extra}"
        )
    return "\n".join(lines)


def cmd_show(state_path: str) -> int:
    _print_lifecycle()
    if not os.path.exists(state_path):
        print(f"\n(no durability state file at {state_path} — showing lifecycle only)")
        return 0
    try:
        state = _load_json(state_path)
        d = WaveBDurability.from_state(state)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"failed to read durability state: {exc}", file=sys.stderr)
        return 2
    except (DurabilityError, AtomicViolation) as exc:
        print(f"invalid durability state: {exc}", file=sys.stderr)
        return 1
    print()
    print(_render_state(d))
    return 0


def cmd_validate(state_path: str, schema_path: str) -> int:
    if not os.path.exists(state_path):
        print(f"durability state not found: {state_path}", file=sys.stderr)
        return 2
    errors = validate_state_file(state_path, schema_path)
    if errors:
        print(f"sak-wave-b-durability --validate: FAIL — {state_path} does not satisfy {schema_path}:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"sak-wave-b-durability --validate: OK — {state_path} satisfies {schema_path}")
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

    def always_accept(path: str) -> RefinerAttemptSource:
        return RefinerAttemptSource(
            {path: [AttemptOutcome(accepted=True, refiner_run_id="run-1", cost=0.12, score_delta=0.4)]}
        )

    def always_reject(path: str, n: int = MAX_ATTEMPTS) -> RefinerAttemptSource:
        return RefinerAttemptSource({path: [AttemptOutcome(accepted=False, failure_mode=f"f{i}") for i in range(n)]})

    # 1. Branch-name determinism: same path -> same branch; different -> different.
    check("branch is deterministic for a path", branch_name("a/SKILL.md") == branch_name("a/SKILL.md"))
    check("different paths -> different branches", branch_name("a/SKILL.md") != branch_name("b/SKILL.md"))
    check("branch carries the refiner/wave-b/ prefix", branch_name("a/SKILL.md").startswith(BRANCH_PREFIX))
    check(
        "file_hash is 12 hex chars",
        len(file_hash("a/SKILL.md")) == 12 and all(c in "0123456789abcdef" for c in file_hash("a/SKILL.md")),
    )

    # 2. Register starts a clean PENDING record on the deterministic branch.
    d = WaveBDurability()
    fd = d.register("a/SKILL.md")
    check(
        "register -> PENDING, 0 attempts, not committed",
        fd.state == PENDING and fd.attempts == 0 and fd.committed is False,
    )
    check("register sets the deterministic branch", fd.branch == branch_name("a/SKILL.md"))
    check("first attempt config is sonnet-default", fd.next_attempt_config() == "sonnet-default")

    # 3. Duplicate register refused.
    try:
        d.register("a/SKILL.md")
        check("duplicate register refused", False)
    except DurabilityError:
        check("duplicate register refused", True)

    # 4. Happy path: attempt 1 accepted -> COMMITTED, atomic (exactly 1 commit).
    d1 = WaveBDurability()
    d1.register("ok/SKILL.md")
    fd = d1.attempt("ok/SKILL.md", always_accept("ok/SKILL.md"))
    check("accepted attempt -> COMMITTED", fd.state == COMMITTED)
    check(
        "COMMITTED records run-id/cost/score-delta",
        fd.refiner_run_id == "run-1" and fd.cost == 0.12 and fd.score_delta == 0.4,
    )
    check("COMMITTED is atomic: exactly 1 commit", fd.commit_count() == 1 and fd.committed is True)
    fd.assert_atomic()
    check("COMMITTED is terminal", fd.is_terminal and not fd.is_parked)

    # 5. Atomic invariant: a tampered partial state is rejected.
    bad = FileDurability(path="x/SKILL.md", state=COMMITTED, committed=False)
    try:
        bad.assert_atomic()
        check("partial COMMITTED (no commit) rejected by atomic invariant", False)
    except AtomicViolation:
        check("partial COMMITTED (no commit) rejected by atomic invariant", True)
    bad2 = FileDurability(path="y/SKILL.md", state=PENDING, committed=True)
    try:
        bad2.assert_atomic()
        check("PENDING-with-commit rejected by atomic invariant", False)
    except AtomicViolation:
        check("PENDING-with-commit rejected by atomic invariant", True)

    # 6. Retry counter increments; the ladder walks sonnet -> adjusted -> opus.
    d2 = WaveBDurability()
    d2.register("retry/SKILL.md")
    src = always_reject("retry/SKILL.md")
    fd = d2.get("retry/SKILL.md")
    configs_seen = []
    for expected_after, _ in enumerate(ATTEMPT_CONFIGS, start=1):
        configs_seen.append(fd.next_attempt_config())
        d2.attempt("retry/SKILL.md", src)
        if expected_after < MAX_ATTEMPTS:
            check(
                f"attempt {expected_after} rejected -> back to PENDING, counter={expected_after}",
                fd.state == PENDING and fd.attempts == expected_after,
            )
    check("ladder configs are sonnet-default -> sonnet-adjusted-prompt -> opus", configs_seen == list(ATTEMPT_CONFIGS))

    # 7. 3rd failure ESCALATES (never silently dropped) with a reason.
    check("3rd failure -> ESCALATED-PARKED", fd.state == ESCALATED_PARKED)
    check("escalation records a reason", fd.escalation_reason is not None and "3-retry" in fd.escalation_reason)
    check("escalated file is parked + terminal", fd.is_parked and fd.is_terminal)
    check("escalated file made exactly MAX_ATTEMPTS attempts", fd.attempts == MAX_ATTEMPTS)
    check("escalated file has NO commit (atomic)", fd.commit_count() == 0 and fd.committed is False)
    fd.assert_atomic()

    # 8. A reject-then-accept sequence commits on the later attempt (atomic).
    d3 = WaveBDurability()
    d3.register("late/SKILL.md")
    late_src = RefinerAttemptSource(
        {
            "late/SKILL.md": [
                AttemptOutcome(accepted=False, failure_mode="f1"),
                AttemptOutcome(accepted=True, refiner_run_id="run-2", cost=0.2, score_delta=0.3),
            ]
        }
    )
    d3.attempt("late/SKILL.md", late_src)  # reject
    fd = d3.get("late/SKILL.md")
    check(
        "after one rejection: PENDING, attempts=1, no commit",
        fd.state == PENDING and fd.attempts == 1 and fd.commit_count() == 0,
    )
    d3.attempt("late/SKILL.md", late_src)  # accept
    check(
        "second attempt accepted -> COMMITTED with 1 commit",
        fd.state == COMMITTED and fd.commit_count() == 1 and fd.refiner_run_id == "run-2",
    )

    # 9. No attempt on a terminal file.
    try:
        d3.attempt("late/SKILL.md", late_src)
        check("attempt on a COMMITTED file refused", False)
    except DurabilityError:
        check("attempt on a COMMITTED file refused", True)

    # 10. run_to_completion drives the full ladder in one call.
    d4 = WaveBDurability()
    d4.register("auto/SKILL.md")
    fd = d4.run_to_completion("auto/SKILL.md", always_reject("auto/SKILL.md"))
    check("run_to_completion lands a terminal state", fd.is_terminal and fd.state == ESCALATED_PARKED)

    # 11. Open-PR park: parked BEFORE any attempt, no commit, re-enqueueable.
    d5 = WaveBDurability()
    d5.register("openpr/SKILL.md")
    fd = d5.park_open_pr("openpr/SKILL.md")
    check("open-PR file parked from PENDING (never attempted)", fd.state == PARKED_OPEN_PR and fd.attempts == 0)
    check("open-PR parked file has NO commit (atomic)", fd.commit_count() == 0)
    check("open-PR parked file is parked + terminal", fd.is_parked and fd.is_terminal)
    fd.assert_atomic()
    # open-PR park is illegal once in-flight/terminal.
    try:
        d5.park_open_pr("openpr/SKILL.md")
        check("re-park of a parked file refused", False)
    except DurabilityError:
        check("re-park of a parked file refused", True)

    # 12. Parked-queue integration: route parked files into the ONE reconciliation queue.
    srq = load_reconciliation_queue_module()
    check("reuses reconciliation-queue PARKED source (lock-step)", PARKED_SOURCE in srq.SOURCES)
    dq = WaveBDurability()
    dq.register("p-open/SKILL.md")
    dq.park_open_pr("p-open/SKILL.md")
    dq.register("p-esc/SKILL.md")
    dq.run_to_completion("p-esc/SKILL.md", always_reject("p-esc/SKILL.md"))
    dq.register("p-ok/SKILL.md")
    dq.attempt("p-ok/SKILL.md", always_accept("p-ok/SKILL.md"))  # committed, NOT parked
    check(
        "parked() lists exactly the two parked files (not the committed one)",
        {fd.path for fd in dq.parked()} == {"p-open/SKILL.md", "p-esc/SKILL.md"},
    )

    queue = srq.ReconciliationQueue()
    routed = dq.route_parked_to_queue(srq, queue, target_version=TV)
    check("routed exactly the two parked files into the queue", set(routed) == {"p-open/SKILL.md", "p-esc/SKILL.md"})
    check("queue items use the wave-b-parked source", all(it.source == "wave-b-parked" for it in queue.items))
    check(
        "reconciliation queue's own park predicate sees the open-PR file",
        queue.is_wave_b_park_eligible("p-open/SKILL.md") is True,
    )
    check(
        "reconciliation queue's parked() sees BOTH routed files (wave_b_parked set)",
        {it.path for it in queue.parked()} == {"p-open/SKILL.md", "p-esc/SKILL.md"},
    )
    check("parked ≠ failed: routed items carry an escalation/park note", all(it.note for it in queue.items))
    # Re-routing is idempotent (no duplicate-path enqueue).
    routed_again = dq.route_parked_to_queue(srq, queue, target_version=TV)
    check(
        "re-routing is idempotent (parked item re-enqueueable, not duplicated)", routed_again == [] and len(queue) == 2
    )

    # 13. The escalated file, once its PR/manual review lands, is recoverable — the
    #     reconciliation queue can clear + re-enqueue it (parked != failed). Prove the
    #     queue's clear path works on a routed open-PR item.
    queue.refresh_open_pr_state(srq.GitHubPrStateSource({"p-open/SKILL.md": srq.PR_NONE}))
    check(
        "routed open-PR item is un-parked when its PR closes (re-enqueue path)",
        queue.get("p-open/SKILL.md").file_state.wave_b_parked is False,
    )

    # 14. JSON round-trip is lossless + re-applies the atomic + branch guards.
    dj = WaveBDurability()
    dj.register("r-ok/SKILL.md")
    dj.attempt("r-ok/SKILL.md", always_accept("r-ok/SKILL.md"))
    dj.register("r-esc/SKILL.md")
    dj.run_to_completion("r-esc/SKILL.md", always_reject("r-esc/SKILL.md"))
    dj.register("r-open/SKILL.md")
    dj.park_open_pr("r-open/SKILL.md")
    state = dj.to_state(as_of="2026-07-02")
    round_tripped = WaveBDurability.from_state(json.loads(json.dumps(state)))
    check("round-trip preserves file count", len(round_tripped) == 3)
    check(
        "round-trip preserves COMMITTED + its atomic commit",
        round_tripped.get("r-ok/SKILL.md").state == COMMITTED
        and round_tripped.get("r-ok/SKILL.md").commit_count() == 1,
    )
    check(
        "round-trip preserves ESCALATED-PARKED + reason",
        round_tripped.get("r-esc/SKILL.md").state == ESCALATED_PARKED
        and round_tripped.get("r-esc/SKILL.md").escalation_reason is not None,
    )
    check(
        "round-trip preserves the deterministic branch",
        round_tripped.get("r-open/SKILL.md").branch == branch_name("r-open/SKILL.md"),
    )
    round_tripped.assert_all_atomic()

    # 15. from_state rejects a wrong version, an unknown state, a bad branch, a partial commit.
    try:
        WaveBDurability.from_state({"state_version": "bogus/v9", "files": []})
        check("from_state rejects wrong version", False)
    except DurabilityError:
        check("from_state rejects wrong version", True)
    try:
        WaveBDurability.from_state(
            {"state_version": STATE_VERSION, "files": [{"path": "z/SKILL.md", "state": "GHOST"}]}
        )
        check("from_state rejects an unknown state", False)
    except DurabilityError:
        check("from_state rejects an unknown state", True)
    try:
        WaveBDurability.from_state(
            {
                "state_version": STATE_VERSION,
                "files": [{"path": "z/SKILL.md", "branch": "refiner/wave-b/deadbeef", "state": PENDING}],
            }
        )
        check("from_state rejects a non-deterministic branch", False)
    except DurabilityError:
        check("from_state rejects a non-deterministic branch", True)
    try:
        WaveBDurability.from_state(
            {"state_version": STATE_VERSION, "files": [{"path": "z/SKILL.md", "state": COMMITTED, "committed": False}]}
        )
        check("from_state rejects a partial (non-atomic) commit", False)
    except (DurabilityError, AtomicViolation):
        check("from_state rejects a partial (non-atomic) commit", True)

    # 16. The committed seed state (if present) validates against the schema + parses.
    if os.path.exists(DEFAULT_STATE) and os.path.exists(SCHEMA_PATH):
        errs = validate_state_file(DEFAULT_STATE, SCHEMA_PATH)
        check("committed SAK-WAVE-B-DURABILITY.json validates against the schema", errs == [])
        WaveBDurability.from_state(_load_json(DEFAULT_STATE))
        check("committed durability state parses through the in-code guards", True)

    # 17. A generated state validates against the schema (schema parity with the model).
    if os.path.exists(SCHEMA_PATH):
        try:
            import jsonschema

            schema = _load_json(SCHEMA_PATH)
            errs = sorted(jsonschema.Draft7Validator(schema).iter_errors(state), key=lambda e: list(e.path))
            check("a generated durability state validates against the schema", errs == [])
        except ImportError:  # pragma: no cover - environment guard
            check("jsonschema available for schema-parity check", False)

    print()
    if failures:
        print(f"self-test: {failures} FAILURE(S).")
        return 1
    print(
        "self-test: deterministic branch model, atomic-commit lifecycle, 3-retry-with-escalation, "
        "open-PR park, parked-queue integration (reuses the ONE reconciliation queue), and JSON round-trip all sound."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="SAK Wave-B durability protocol — per-file branch + atomic commit + 3-retry-with-escalation + parked-queue integration."
    )
    parser.add_argument("--self-test", action="store_true", help="run the deterministic offline self-test (CI gate)")
    parser.add_argument(
        "--validate", action="store_true", help="jsonschema-validate a durability-state JSON against the schema"
    )
    parser.add_argument(
        "--show", action="store_true", help="print the lifecycle + retry ladder (+ a state file, if present)"
    )
    parser.add_argument("--state", default=DEFAULT_STATE, help="path to SAK-WAVE-B-DURABILITY.json")
    parser.add_argument("--schema", default=SCHEMA_PATH, help="path to the sak-wave-b-durability schema")
    args = parser.parse_args(argv)

    if args.self_test:
        return cmd_self_test()
    if args.validate:
        return cmd_validate(args.state, args.schema)
    if args.show:
        return cmd_show(args.state)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
