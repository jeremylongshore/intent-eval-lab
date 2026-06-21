---
title: SAK Phase-4 decomposition → implementation map — 4a / 4b / 4b.5 / 4c against what now exists
category: AT-SPEC
status: NORMATIVE
date: 2026-06-21
authority: plan 033 v7 § 14.4 REVISED; plan 048 v8 Delta 1 / 1.1 / 3 + § 14.31
bead: bd_000-projects-a010
epic: bd_000-projects-3kye (SAK)
---

# SAK Phase-4 decomposition → implementation map

**Status: NORMATIVE.** This doc is the formal decomposition of SAK Phase-4 into its four
named sub-phases — **4a** (Wave A deterministic) / **4b** (Wave B eval-loop) / **4b.5**
(shadow-mode dual-validator) / **4c** (advisory→blocking flip) — per plan 033 v7 § 14.4
REVISED, amended by plan 048 v8 Deltas 1 / 1.1 / 3 + § 14.31.

It is **not** a restatement of the plan. The value-add is the second column: the Phase-4
**mechanism was built this sprint** (the state machine, the rollback command, the
reconciliation queue, the Wave-B durability protocol all landed 2026-06-20 as docs
092–095), so this is a **decomposition → implementation map** — each sub-phase stated with
(1) its plan definition + preconditions and (2) the concrete artifact(s) that now implement
it, with (3) an honest gap list where the supporting machinery exists but the **execution
driver** does not.

**Honesty discipline (read before the table).** A sub-phase is **BUILT** only when its
own deliverable exists as a runnable, CI-wired artifact in this repo. Where only the
**supporting machinery** (the state/queue/durability/rollback decision logic) exists and the
**execution driver** (the batch remediator, the dual-validator shadow runner, the CCP-side CI
flip flag) does not, the sub-phase is **PARTIAL** and the unbuilt driver is named as an
**OPEN** gap. No sub-phase is claimed BUILT on the strength of its scaffolding alone.

## Source-of-truth pointers

| Layer                           | Where                                                                                                |
| ------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Authoritative 4a/4b/4b.5/4c def | plan 033 v7 § 14.4 REVISED (`033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md`)              |
| Flip-gate + concurrency deltas  | plan 048 v8 Delta 1 / 1.1 / 3 + § 14.31 (`048-PP-PLAN-skill-refiner-sak-amendment-v8-2026-06-10.md`) |
| Phase-4 flip state machine      | 092-AT-SPEC + `scripts/sak-state-machine.py` + `specs/state-machines/schema/sak-state.schema.json`   |
| Phase-4c rollback               | 093-AT-SPEC + `scripts/sak-kernel-gate-revert.py`                                                    |
| Reconciliation queue            | 094-AT-SPEC + `scripts/sak-reconciliation-queue.py` + its schema                                     |
| Wave-B durability               | 095-AT-SPEC + `scripts/sak-wave-b-durability.py` + its schema                                        |

## Status summary

| Sub-phase                           | Status      | Implementing artifact(s)                                                                                                                                                                                   |
| ----------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **4a** Wave A deterministic batch   | **PARTIAL** | Residue + merge-gate machinery BUILT (`sak-reconciliation-queue.py`, 094); the `batch-remediate` executor itself is SPEC-ONLY.                                                                             |
| **4b** Wave B eval-loop             | **PARTIAL** | Durability + parked-queue routing BUILT (`sak-wave-b-durability.py`, 095); the Refiner eval-loop driver (`@j-rig/refiner`) is external + unbuilt.                                                          |
| **4b.5** Shadow-mode dual-validator | **PARTIAL** | The `SHADOW-MODE` / `HOLDING` states + transitions BUILT (`sak-state-machine.py`, 092); the dual-validator runner + deviation meter is SPEC-ONLY.                                                          |
| **4c** Advisory→blocking flip       | **BUILT**\* | Flip-gate enforcement + rollback command BUILT (`sak-state-machine.py` + `sak-kernel-gate-revert.py`, 092/093). \*The CCP-side `validate-plugins.yml` mode-flag flip that the gate authorizes is external. |

\* 4c is the one sub-phase whose **own deliverable** — the gated flip decision and its
rollback — is the decision logic, and that logic is built, CI-wired, and hash-pinned here.
The actuator it authorizes (flipping a CI mode flag in the CCP repo) is downstream-external by
design — this repo owns the **decision**, not the CCP CI surface.

---

## 4a — Wave A deterministic batch

### Definition + preconditions (plan 033 § 14.4a)

Run `batch-remediate.py` against the ~3,543-file CCP SKILL.md corpus + 53 global skills:
deterministic frontmatter normalization to the kernel-schema-valid IS-marketplace tier
(`compatible-with` → `compatibility`; `allowed-tools` → YAML list; infer
`version`/`author`/`tags`/`license` from git metadata where unambiguous; emit per-file diff +
remediation log). **Exit gate:** ≥ 80% of corpus passes the kernel schema in advisory mode
after Wave A (not 99.5% — that is the 4c flip gate). **Rollback:** `git revert` the
batch-remediate commit(s); no Evidence-Bundle implications (gate still advisory).
**Reconciliation:** files Wave A leaves with WARN-level open issues land in a residue queue
for Wave B. Per plan 048 v8 Delta 1, Wave A for a file runs **before** any in-flight
contributor PR merges (wave-A-wins; the PR rebases onto post-Wave-A state).

### What implements it

- **Residue + concurrency machinery — BUILT.** `scripts/sak-reconciliation-queue.py`
  (094-AT-SPEC) is the single queue holding Wave A residue (`source: wave-a-residue`). It
  carries the per-file state record `{open_pr_state, wave_a_pending, wave_b_parked,
target_version}` and the **merge-gate predicate** `blocks_pr_merge(path)` — RED iff
  `wave_a_pending == True` — which is the `sak-wave-a-precedence` "Wave A precedes in-flight-PR
  merge" rule (plan 048 Delta 1 rule 2 / Delta 1.1). Schema:
  `specs/state-machines/schema/sak-reconciliation-queue.schema.json`. CI: `ci.yml` "Validate
  specs and docs" runs `--self-test` + `--validate`; 28-case pytest suite. Both script + schema
  hash-pinned in `.harness-hash`.
- **Pinned target version — BUILT (as data).** The `target_version` field on each queue item
  carries the `LATEST_PHASE_4_VERSION` pin (plan 048 Delta 1) so authors never chase a moving
  schema.

### OPEN gaps

- **The `batch-remediate` executor itself is SPEC-ONLY.** No `batch-remediate.py` exists in
  this repo (`find . -name '*batch-remediate*'` → none). The deterministic frontmatter
  normalizer is a CCP-repo migration tool (it operates on the CCP corpus, not lab artifacts);
  the lab side built the **queue + merge-gate the executor feeds**, not the executor. The 80%
  advisory-pass exit gate is therefore **not yet measurable** — there is no run.
- **The Wave-A `git revert` rollback path** is described in 092-AT-SPEC's state machine
  (`ADVISORY-W-A --wave-a-failure→ ROLLED-BACK`, rollback class 1) as a **modeled transition**,
  but the actual `git revert` of a real batch commit is a CCP-repo operation, not a lab script.

---

## 4b — Wave B eval-loop

### Definition + preconditions (plan 033 § 14.4b)

The Skill Refiner Phase-B eval-loop processes the ~20% Wave A did not handle + the Wave A
residue. The Refiner proposes edits under the strict-improvement gate (AC-7); accepted edits
land as a per-file PR. **Exit gate:** ≥ 99% of the full corpus passes the kernel schema in
advisory mode (≈30–40 residue files expected; 100% not required). **Rollback:** each Refiner
edit is its own commit on a per-file branch; rollback = `git revert` of specific commits;
if the Refiner produces bad edits at high rate, STOP + reconcile per § 14.4.rollback.
**Cost ceiling** (§ 14.4.cost): STOP at budget regardless of completion. Per plan 048 v8
Delta 1, Wave B **never** runs on a file with an open PR (parked, re-enqueued on PR close).

### What implements it

- **Durability protocol — BUILT.** `scripts/sak-wave-b-durability.py` (095-AT-SPEC) is the
  "side-branch + atomic + 3-retry + parked-queue" mechanism (F-MK-004): per-file branch
  `refiner/wave-b/<sha256(path)[:12]>` (path-derived for recoverability); the atomic-commit
  invariant (`COMMITTED ⇔ exactly one commit`, every other state ⇔ zero, no partial state,
  enforced by `assert_atomic()` + `from_state()` on load); the 3-retry ladder
  (`sonnet-default` → `sonnet-adjusted-prompt` → `opus`, **escalating** on the 3rd failure to
  `ESCALATED-PARKED` rather than silently dropping); and the open-PR park
  (`PARKED-OPEN-PR`, before any attempt). Schema:
  `specs/state-machines/schema/sak-wave-b-durability.schema.json`. CI `--self-test` +
  `--validate`; 31-case pytest suite; script + schema hash-pinned.
- **Parked-queue routing — BUILT.** Both terminal park states route into the **single**
  reconciliation queue (094) by **reusing** its `FileState` / `QueueItem` /
  `is_wave_b_park_eligible` structures (`to_reconciliation_items` + `route_parked_to_queue`,
  idempotent) — "parked ≠ failed." The wave-B-park predicate `is_wave_b_park_eligible(path)`
  (an open-PR file is skipped, never run concurrently) is the plan 048 Delta 1 rule-3 mechanism.

### OPEN gaps

- **The Refiner eval-loop driver is external + unbuilt here.** The durability protocol models
  durability **decisions**, not side effects — git/GitHub operations are isolated behind the
  `RefinerAttemptSource` stub seam ("this module decides; it does not execute"). The actual
  eval-loop that proposes edits under AC-7 is `@j-rig/refiner` / `@j-rig/refiner-core` in the
  j-rig monorepo (the Skill Refiner product), which is the wider in-flight buildout — **not** an
  artifact in this repo. The 99%-advisory-pass exit gate is **not yet measurable** (no run).
- **The per-file cost meter (§ 14.4.cost)** — `$50/file mean, $200/file hard cap, $35K total`,
  `audit/wave-b-cost-ledger.jsonl`, the `iaj-refiner-cost-instrument` bead — is **SPEC-ONLY**:
  it instruments `@j-rig/refiner-core` OTel spans, not a lab script. No ledger file exists.

---

## 4b.5 — Shadow-mode dual-validator

### Definition + preconditions (plan 033 § 14.4b.5)

Before the advisory→blocking flip, the CCP CI `validate-plugins.yml` runs in **DUAL MODE** for
≥ 7 calendar days: the existing CCP validator (current authority) + the kernel-schema validator
(proposed authority). Diff their verdicts per file; report the **deviation rate**. **Exit
gate:** EITHER (a) deviation rate < 0.5% of corpus (acceptable noise; flip safe), OR (b)
deviation rate ≥ 0.5% AND **each** deviation carries a named disposition
(schema-revision-candidate? validator-bug? file-author-fix?). Shadow mode ends on **disposition
completeness**, not a calendar. **Rationale:** the kernel-vs-CCP validator divergence is the
most likely source of 4c surprises; shadow mode surfaces them before they break authors at flip
time.

### What implements it

- **The `SHADOW-MODE` lifecycle — BUILT (as state).** `scripts/sak-state-machine.py`
  (092-AT-SPEC) models `SHADOW-MODE` as a real state with two outbound edges:
  `dispositions-resolved → READY-TO-FLIP` (gated on `open_p0_count == 0`) and
  `deviations-open-p0 → HOLDING` (the audit branch — open-P0 deviations route to audit, and
  `HOLDING` can **never** flip directly to `BLOCKING`; its only exit is `audit-cleared →
SHADOW-MODE`). This encodes the § 14.4b.5 discipline that an unresolved deviation cannot reach
  the flip.

### OPEN gaps

- **The dual-validator runner + deviation meter is SPEC-ONLY.** No lab script runs the CCP
  validator and the kernel-schema validator side by side over the corpus and computes a
  per-file deviation rate (`find scripts -iname '*shadow*' -o -iname '*dual*'` → none). The
  state machine knows _that_ shadow mode happens and _what its exits mean_; it does not _run_
  the comparison. That runner is a CCP-CI-repo artifact (`validate-plugins.yml` dual mode),
  unbuilt.
- **The ≥ 7-calendar-day window + the < 0.5% deviation measurement** are therefore not yet
  measurable here — there is no deviation source feeding the state machine's `open_p0_count`.
  The state machine reads that count from `SAK-STATE.json`; the producer that would populate it
  from a real shadow run does not exist.

---

## 4c — Advisory→blocking flip

### Definition + preconditions (plan 033 § 14.4c + plan 048 v8 Delta 3)

`validate-plugins.yml` flips `mode: advisory` → `mode: blocking` for SKILL.md; PR-blocking
starts. The four exit preconditions are **not equal in override-ability** (plan 048 v8
Delta 3):

- **(a) coverage ≥ 99.5% corpus pass** — the ONLY precondition the 30-day calendar ceiling can
  disposition: at day 30, a flip below the floor is permitted **only** with the remaining
  < 0.5% of files **quarantined** (advisory-only, never blocking).
- **(b) shadow window ≥ 7 days at deviation < 0.5%** (§ 14.4b.5) — advisory relative to (c)/(d).
- **(c) zero open P0** in the schema-revision-candidates queue (§ 14.A.3) — **HARD gate**, never
  overridden by the calendar ceiling.
- **(d) governance triple sign-off** (CTO + CISO + VP DevRel, § 14.12) — **HARD gate**, never
  overridden by the calendar ceiling.

If (c) or (d) is unmet at day 30, the flip is **BLOCKED** and **auto-escalates to an ISEDC
convening** — a human DECISION, never an automatic flip. **Lifecycle states** (plan 048 v8
§ 14.31): `DRAFT` / `SHIPPED-INTERNAL` / `PUBLISHED`; § 14.27 read-only-immutability binds only
at and after `PUBLISHED`, so structural decomposition (§ 14.18) happens **before** publication —
no contradiction.

### What implements it

- **The flip-gate enforcement — BUILT.** `scripts/sak-state-machine.py` (092-AT-SPEC) gates the
  `READY-TO-FLIP --governance-triple-signs→ BLOCKING` transition exactly to Delta 3: (c)
  zero-open-P0 and (d) governance triple are enforced as **absolute** hard gates; (a) coverage is
  the **only** precondition the calendar ceiling can disposition (a sub-floor flip is permitted
  only when the caller passes `allow_calendar_ceiling=True`, which quarantines the long tail);
  (b) the shadow window is surfaced as a rejection reason when clearly unmet. The governance
  sign-off is read through the `load_signoff_from_state` seam (the single function a real ISEDC
  AT-DECR ledger / signing service replaces). CI `--self-test` + `--validate`; 35-case pytest
  suite; script + schema hash-pinned.
- **The rollback command — BUILT.** `scripts/sak-kernel-gate-revert.py` (093-AT-SPEC) is
  `kernel-gate-revert`: it drives the state machine `BLOCKING --regression-detected→ ROLLED-BACK`
  (reusing the engine's `emit()`, never re-declaring the edge), refuses the revert unless the
  **same** governance triple signs (rejection names the missing seats), stamps the
  `retrospective_due_at = reverted_at + 7 calendar days` ISEDC Class-2 deadline (rollback class 3
  (d)), and surfaces overdue retrospectives via `--check-retrospective`. The
  `rolled-back-superseded` Rekor superseding event stays owned by the kernel-side emitter
  (F-MK-005 — Rekor is append-only); this command records only the **intent**
  (`rollback.affected_window` + `rollback.superseding_signing_mode`), never touching Rekor. CI
  `--self-test` + `--check-retrospective`; 35-case pytest suite.

### OPEN gaps

- **The CCP-side actuator is external by design.** The `validate-plugins.yml`
  `mode: advisory → mode: blocking` config flip that this gate **authorizes** is a CCP-repo CI
  change, not a lab artifact. This repo owns the **gated decision + its rollback**, not the CCP
  CI surface that the decision actuates. (This is the correct boundary, not a missing piece — but
  it is named here so the map is not read as "4c flips the CCP gate from this repo." It does not;
  it decides _whether_ the flip is allowed.)
- **The governance sign-off source is STUBBED behind one seam.** Until a live
  governance-signoff source exists (an ISEDC AT-DECR ledger / signing service), the three
  booleans default to all-false from `SAK-STATE.json`. Replacing `load_signoff_from_state` is the
  only change a real source needs — but that source is not yet wired.

---

## End-to-end flow (4a → 4b → 4b.5 → 4c) with the rollback off-ramp

The legal-transition graph below is the one the **state machine enforces** (092-AT-SPEC); the
sub-phase labels map each segment to its decomposition. `[BUILT]` = decision logic exists +
CI-wired here; `[PARTIAL]` = supporting machinery built, execution driver SPEC-ONLY.

```text
   4a Wave A deterministic                4b Wave B eval-loop
   [PARTIAL: queue+merge-gate BUILT,      [PARTIAL: durability+park BUILT,
    batch-remediate SPEC-ONLY]            @j-rig/refiner driver external]
            │                                       │
            ▼                                       ▼
  ┌──────────────────┐  wave-a-merged   ┌──────────────────┐  wave-b-done   ┌──────────────────┐
  │     ADVISORY     │ ───────────────▶ │   ADVISORY-W-A   │ ─────────────▶ │  ADVISORY-W-AB   │
  │  (default state) │                  │  (wave A merged) │                │ (both waves done)│
  └──────────────────┘                  └────────┬─────────┘                └────────┬─────────┘
                                          wave-a-failure                       enable-shadow
                                         (rollback class 1)                          │
                                                 │                                   ▼
                                                 │              4b.5 shadow-mode dual-validator
                                                 │              [PARTIAL: SHADOW/HOLDING states
                                                 │               BUILT, dual-validator runner
                                                 │               SPEC-ONLY]
                                                 │                                   │
                                                 │                  ┌────────────────┴───────────────┐
                                                 │                  ▼                                │
                                                 │        ┌──────────────────┐  deviations-open-p0   │
                                                 │        │   SHADOW-MODE    │ ────────────────────┐ │
                                                 │        │ (dual-validator) │                     │ │
                                                 │        └────────┬─────────┘ ◀───────────┐       │ │
                                                 │       dispositions-resolved │ audit-     │       ▼ │
                                                 │        (open_p0_count == 0)  │ cleared    │  ┌─────────┐
                                                 │                 ▼            │            │  │ HOLDING │
                                                 │        ┌──────────────────┐  │            └──│ (audit) │
                                                 │        │  READY-TO-FLIP   │  │   HOLDING never  └─────────┘
                                                 │        └────────┬─────────┘  │   flips direct ─────┘
                                                 │   governance-triple-signs    │   to BLOCKING
                                                 │   [HARD: (c) zero-open-P0    │
                                                 │    + (d) triple sign-off;    │  4c advisory→blocking flip
                                                 │    (a) coverage calendar-    │  [BUILT: flip-gate + rollback
                                                 │    dispositionable]          │   decision logic here; CCP
                                                 │                 ▼            │   mode-flag actuator external]
                                                 │        ┌──────────────────┐  │
                                                 │        │     BLOCKING     │  │
                                                 │        │  (flip complete) │  │
                                                 │        └────────┬─────────┘  │
                                                 │       regression-detected    │
                                                 │       (rollback class 3:     │
                                                 │        kernel-gate-revert,    │
                                                 │        governance triple,     │
                                                 │        +7d ISEDC Class-2)     │
                                                 ▼                 ▼            │
                                          ┌──────────────────────────┐         │
                                          │       ROLLED-BACK        │ ────────┘
                                          │  (back-to-shadow re-try) │  back-to-shadow
                                          └──────────────────────────┘
```

**Rollback off-ramp (the three classes, plan 033 § 14.4.rollback):** class 1
(`ADVISORY-W-A --wave-a-failure→ ROLLED-BACK`, Wave A `git revert`); class 2
(`ADVISORY-W-AB --wave-b-failure→ ROLLED-BACK`, per-file Refiner-commit revert); class 3
(`BLOCKING --regression-detected→ ROLLED-BACK`, the governance-gated `kernel-gate-revert`
command with the 7-day ISEDC Class-2 retrospective stamp). Every `ROLLED-BACK` returns to
`SHADOW-MODE` via `back-to-shadow` for a re-attempt. `ROLLED-BACK` is the single off-ramp; it is
reachable from each of the three gated states and never bypasses shadow on the way back to a
flip.

## Honest bottom line

- **BUILT here (decision logic, CI-wired, hash-pinned):** the Phase-4 flip state machine (092),
  the `kernel-gate-revert` rollback command (093), the shared reconciliation queue +
  merge-gate / wave-B-park predicates (094), and the Wave-B durability protocol + parked-queue
  routing (095). The 4c **gate** — the hard-vs-dispositionable precondition discipline and its
  rollback — is fully realized.
- **NOT built here (execution drivers — SPEC-ONLY / external):** the Wave-A `batch-remediate`
  deterministic executor (4a); the `@j-rig/refiner` eval-loop driver + its cost meter (4b); the
  dual-validator shadow runner + deviation meter (4b.5); the CCP `validate-plugins.yml` mode-flag
  actuator (4c). These are CCP-repo / j-rig-monorepo artifacts; the lab built the **machinery the
  drivers feed**, and the **decision logic that gates the flip**, not the drivers themselves.

The Phase-4 _control plane_ exists and is enforced; the Phase-4 _data plane_ (the actual corpus
migration runs) is the remaining work, and it lives outside this repo.

— Jeremy Longshore
intentsolutions.io
