---
title: SAK CI-Gate 90-Day Re-Eval Cadence — quarterly review of the 4 SAK gates (FP/FN measurement + flake budget + maintenance-burden ledger)
date: 2026-06-20
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: 033-PP-PLAN § 14.13.3 (closes audit finding F-WC-001)
inherits_from:
  - 033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md (§ 14.13 — SAK dashboard + AAR cadence; § 14.13.3 — 90-day CI gate re-eval cadence)
  - 046-AT-STND-sak-governance-owners.md (seat-bound owner map)
related_docs:
  - 045-RR-LAND-single-source-of-truth-and-continuous-spec-compliance-2026-06-09.md (the SSoT declaration + continuity machinery + § 6 changelog-observance gate)
  - 053-AT-SPEC-drift-classification-eval-set-2026-06-12.md (the drift-classification recall-floor write gate)
  - 063-AT-SPEC-leading-indicator-watcher-2026-06-12.md (prior-art flake-budget pattern; § "Flake budget <5% FP")
  - 071-AA-AACR-iep-testing-cicd-audit-matrix-2026-06-18.md (audit matrix flagging required-vs-advisory state of these gates)
  - 069-DR-STND-state-labeling-standard-2026-06-18.md (lifecycle-label vocabulary)
related_drs:
  - 044-AT-DECR-isedc-council-session-8-sak-charter-2026-06-09.md (SAK charter ratification)
  - 081-AT-DECR-isedc-sak-class-1-charter-ratification-2026-06-17.md (charter ratification — CSO continuity-spine-as-standing-cost rider)
epic: bd_000-projects-9k5h (Make the kernel the single source of truth and keep it continuously spec-compliant with upstream)
bead: bd_000-projects-39qj
filing_standard: Document Filing Standard v4.3
---

> **State label: NORMATIVE.** This specification binds a recurring quarterly review of
> the four SAK CI gates. It is the canonical, standalone reference for the 90-day
> re-eval cadence introduced in plan 033 § 14.13.3. Amendments route per Blueprint A
> § 2.3 (DR-010 three-class governance routing); the named owner is the CTO seat per
> 046-AT-STND. Closes audit finding **F-WC-001**.

# SAK CI-Gate 90-Day Re-Eval Cadence

**Beads:** `bd_000-projects-39qj` under epic `bd_000-projects-9k5h` (the SSoT epic).

## 1. Why this exists (the F-WC-001 finding)

The Spec Authority Kernel (SAK) keeps the kernel `@intentsolutions/core`
`schemas/authoring/v1/*` continuously adherent to upstream. Four CI gates enforce that
adherence on every PR. Like every standing detector, those gates can rot in two
directions at once:

- **They go quiet (false negatives).** A gate that no longer catches the drift it was
  built to catch is worse than no gate — it manufactures false confidence. The
  catastrophic asymmetric failure the SSoT declaration names (045-RR-LAND) is a stale
  schema fanning out fleet-wide under green dashboards. A blind gate is one path to it.
- **They go noisy (false positives + flakes).** A gate that reds on non-drift trains
  contributors to ignore red, which re-creates the false-negative failure by a
  different route. It also burns developer-hours on flake triage — a maintenance tax
  that, unmeasured, silently grows until someone deletes the gate in frustration.

Audit finding **F-WC-001** ("CI gate re-eval cadence") observed that the four gates
shipped with no scheduled review of either failure mode. Plan 033 § 14.13.3 specified
a 90-day cadence to close it. This document is that specification, made standalone and
binding. It is deliberately the **doc-is-the-deliverable** closure: the review
procedure, the FP/FN measurement protocol, the flake budget, and the maintenance-burden
ledger are defined here; the first quarterly run executes against this spec.

The CSO charter rider (081-AT-DECR) frames the stakes precisely: a SSoT without a
_live, maintained_ drift-detector is a liability, not an asset. "Landed once" is not
"live-maintained." This cadence is the instrument that converts the gates from
landed-once into live-maintained.

## 2. The four SAK gates under review

The bead title and the current CI topology are authoritative for the gate set. (Plan
033 § 14.13.3's original enumeration named `is-extension-rationale` and
`leading-indicator-watch`; those evolved — `is-extension-rationale` is now a _check
inside_ `coverage-map-gates` rather than a standalone PR gate, and
`leading-indicator-watch` is a daily continuity _monitor_, not a per-PR quality gate.
This spec reviews the four load-bearing per-PR gates that actually block merges.)

| #   | Gate                                  | Repo + CI workflow                                     | Implementation                                                                                                            | What it catches                                                                                                                                               | Determinism                                                                                                        |
| --- | ------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| G1  | `coverage-map-completeness`           | `intent-eval-core` · `coverage-map-gates.yml`          | `scripts/check-coverage-map-completeness.ts` (+ `check-is-extension-rationale.ts`, `check-coverage-map-prose-anchors.ts`) | Every kernel `authoring/v1` field has a coverage-map row classifying it `anthropic-spec-derived` vs `is-only-extension`; IS-only extensions carry a rationale | Fully deterministic (AST/JSON walk; no LLM)                                                                        |
| G2  | `prose-anchor-validity`               | `intent-eval-core` · `prose-anchor-validity.yml`       | `scripts/check-prose-anchors.ts` + `parse-spec-headings.ts`                                                               | Every `anthropic-spec-derived` coverage-map entry cites a 6767-h section heading that actually exists in the master spec (no dangling anchors)                | Fully deterministic (pinned markdown parse; no LLM)                                                                |
| G3  | `drift-classification` (recall floor) | `intent-eval-lab` · `ci.yml` "Validate specs and docs" | `scripts/drift-eval-runner.py` against `evals/drift-classification/v1/`                                                   | The (future) LLM drift classifier clears a **recall floor of 1.0 on material cases** on the frozen human-labeled eval set before it earns any write authority | Deterministic _scorer_ over a frozen set; the thing it gates (an LLM) is not — see 053-AT-SPEC + 055-AT-SPEC walls |
| G4  | `changelog-observance`                | `intent-eval-core` · `changelog-observance.yml`        | `scripts/check-changelog-observance.ts`                                                                                   | A schema change without a matching CHANGELOG + lineage record fails; the kernel CHANGELOG is canonical and CCP `SCHEMA_CHANGELOG` cites it                    | Fully deterministic (diff vs CHANGELOG presence)                                                                   |

**Owner seat.** Per 046-AT-STND, the **CTO** seat owns kernel schema versioning and
breaking-change discipline; G1/G2/G4 are kernel-side and route to the CTO. G3's
write-gate semantics are a CISO concern per the autonomy-ceiling charter (081-AT-DECR
Q5 — the LLM never earns its hop without clearing the recall floor), so G3's quarterly
review is **CTO-led, CISO co-signed**. No gate change lands without its named seat.

## 3. The 90-day cadence

- **Period.** One review every 90 calendar days (≈ quarterly), per gate, all four in a
  single review pass. Anchor date: the date this spec lands (2026-06-20). First review
  due on or before **2026-09-18** (T+90d).
- **Deliverable per quarter.** One after-action-style report filed as
  `intent-eval-lab/000-docs/NNN-RR-LAND-sak-ci-gate-quarterly-<date>.md` (the
  `NNN-RR-LAND` filing per Document Filing Standard v4.3; lifecycle label `INFORMATIVE`
  — it is a measurement record, not a binding spec). The report carries the four
  measurement tables of § 4–§ 6 plus a one-line per-gate disposition (KEEP / RE-TUNE /
  ESCALATE).
- **Skip rule.** A quarter may be skipped _only_ if zero of the four gates fired a
  non-trivial result in the period AND the maintenance-burden ledger (§ 6) recorded
  zero developer-hours. A skip is itself recorded as a one-paragraph note in the index
  and a `[sak-ci-gate-quarterly] SKIPPED <date>` line in the ledger — silence is never
  the record. (Bandwidth is the gate per DR-010 § 13.5; the cadence is a standing
  safety cost per the CSO rider, so a skip is a deliberate, logged decision, not a
  default.)
- **Low-frequency reminder.** This spec is the closeable deliverable; a literal 90-day
  cron is optional. The recommended reminder mechanism is a **tracked checklist bead**
  re-opened each quarter (one bead per quarterly run, parented to the SSoT epic
  `bd_000-projects-9k5h`), surfaced by `bd ready` when its due-date lands. If a
  cron stub is later wired, it lives as a `schedule:`-triggered job that opens the
  deduped `[sak-ci-gate-quarterly]` reminder issue — it never mutates a gate, only
  reminds. See § 8.

## 4. FP/FN measurement protocol

The two failure modes (§ 1) are measured separately because they have different oracles
and different costs.

### 4.1 False-positive rate (gate reds on non-drift)

A **false positive** is a gate firing RED on a PR that did not actually introduce the
drift the gate exists to catch (a flake, an over-broad match, a parser brittleness, a
stale fixture). FP is directly observable from CI history — every RED that was resolved
by "re-run / revert an unrelated change / fix the gate, not the schema" is an FP.

- **Procedure.** For the period, pull every RED run of each gate (`gh run list
--workflow <gate>.yml --status failure` for the kernel gates; the
  `Validate specs and docs` job history for G3). Classify each RED as TRUE-POSITIVE
  (the PR really introduced the drift) or FALSE-POSITIVE (it did not). The denominator
  is total runs of the gate in the period.
- **Targets.** FP rate **target < 2%**; **> 5% triggers RE-TUNE** of that gate. (Same
  budget the leading-indicator watcher already runs to — 063-AT-SPEC § "Flake budget";
  the deterministic gates G1/G2/G4 should sit near zero, so any non-trivial FP rate on
  them is a parser/fixture bug to fix, not a tolerance to accept.)

### 4.2 False-negative rate (gate stays green on real drift)

A **false negative** is real drift that the gate did NOT catch. This has **no perfect
oracle** — by definition the gate didn't flag it, so it isn't in CI history. The
review approximates it with a manual sample.

- **Procedure.** Sample **20 merged PRs per quarter** that touched any
  `schemas/authoring/v1/*` file, the coverage map, the 6767-h prose, or the kernel
  CHANGELOG (the surfaces the four gates guard). For each, a human reviewer answers:
  "did this PR introduce a drift the relevant gate _should_ have caught but stayed
  green on?" Any YES is a confirmed false negative — the highest-severity finding,
  because a blind gate is the SSoT failure mode (§ 1).
- **Targets.** FN target is **zero confirmed false negatives**; any confirmed FN is an
  immediate ESCALATE (§ 7) regardless of rate, because the cost is asymmetric (a missed
  material drift is unrecoverable; an FP costs one human review — 053-AT-SPEC). The
  20-PR sample size is the same discipline as the drift-classification eval's
  manual-sample posture; if a quarter has fewer than 20 qualifying PRs, sample all of
  them and note the reduced denominator.

### 4.3 Gate utility (TP-catch ratio)

To distinguish a _useful_ gate from a _dormant_ one, also record the **gate-utility
ratio**: true-positive catches ÷ total runs. A gate with near-zero utility over
several quarters is a candidate for the port-not-delete inventory (033 § 14.14) — it
either guards a surface that no longer drifts, or it should be folded into a sibling
gate. Low utility is a _discussion_ trigger (note it in the report), never an automatic
removal.

### 4.4 The per-quarter FP/FN table (report template)

| Gate                           | Total runs | TRUE-POS | FALSE-POS | FP rate | FP target | FN sample size | Confirmed FN | Utility (TP/runs) | Disposition               |
| ------------------------------ | ---------- | -------- | --------- | ------- | --------- | -------------- | ------------ | ----------------- | ------------------------- |
| G1 `coverage-map-completeness` |            |          |           |         | < 2%      |                | 0 expected   |                   | KEEP / RE-TUNE / ESCALATE |
| G2 `prose-anchor-validity`     |            |          |           |         | < 2%      |                | 0 expected   |                   | KEEP / RE-TUNE / ESCALATE |
| G3 `drift-classification`      |            |          |           |         | < 2%      |                | 0 expected   |                   | KEEP / RE-TUNE / ESCALATE |
| G4 `changelog-observance`      |            |          |           |         | < 2%      |                | 0 expected   |                   | KEEP / RE-TUNE / ESCALATE |

## 5. Flake budget

A **flake** is a non-deterministic RED — same input, different verdict (a network blip
in a fetch, a non-pinned tool version, an ordering dependency). Flakes are a subset of
false positives but tracked separately because the _fix_ differs: an FP is a logic/scope
bug; a flake is a determinism bug.

- **Budget.** Each gate has a flake budget of **< 1 flake per quarter**. Three of the
  four gates (G1/G2/G4) are fully deterministic — they read committed files and run
  pinned tooling, so their flake budget is effectively **zero**; any flake on them is a
  determinism regression (an unpinned dependency, a non-deterministic walk order) to
  fix at the root, not absorb. G3's scorer is deterministic over a frozen set; its only
  flake surface is the manifest-integrity fetch, which is local. A flake budget
  _exceeded_ is a RE-TUNE for that gate in the same quarter, not deferred.
- **Determinism guardrails already in place** (the reason the budget is near-zero):
  - G1/G2/G4 pin their tooling (the `intent-eval-core` workflows use a pinned Node +
    pinned dependency tree); G2's markdown parse is pinned (053/045 discipline — a
    pinned parser, renumbering a 6767-h section requires a same-commit coverage-map PR).
  - G3 verifies manifest integrity _before_ scoring (a score against a drifted set is
    rejected, not flaked — 053-AT-SPEC § "recall-floor write-gate contract").
  - The gate definitions are hash-pinned via `.harness-hash` (063-AT-SPEC § CI) where
    applicable — a silent edit to a gate workflow blocks the PR, so flakes can't be
    introduced by an unreviewed workflow edit.
- **Flake-budget table (report template).**

| Gate                           | Flakes observed | Flake budget      | Root cause (if any) | Determinism fix landed? |
| ------------------------------ | --------------- | ----------------- | ------------------- | ----------------------- |
| G1 `coverage-map-completeness` |                 | 0 (deterministic) |                     |                         |
| G2 `prose-anchor-validity`     |                 | 0 (deterministic) |                     |                         |
| G3 `drift-classification`      |                 | < 1               |                     |                         |
| G4 `changelog-observance`      |                 | 0 (deterministic) |                     |                         |

## 6. Maintenance-burden ledger

The maintenance tax is the slowest, most invisible killer of a standing gate. The
ledger makes it visible.

- **Unit.** Developer-hours spent in the period on each gate, bucketed by reason:
  FLAKE-TRIAGE (chasing a non-deterministic red), FP-FIX (correcting an over-broad
  match / stale fixture), FN-FIX (closing a discovered blind spot), and UPSTREAM-ADAPT
  (changing the gate because upstream moved — _expected_, healthy maintenance, not a
  defect).
- **Target.** **< 4 developer-hours per quarter across all four gates combined** (plan
  033 § 14.13.3). Exceeding it is a RE-TUNE discussion (which gate ate the budget, and
  is the fix a one-time determinism repair or recurring upstream churn?). UPSTREAM-ADAPT
  hours that exceed the budget are _not_ a defect — they signal the kernel is tracking
  a fast-moving upstream surface and may warrant a leading-indicator check (063-AT-SPEC),
  not a gate weakening.
- **Append-only.** The ledger is append-only across quarters so the _trend_ is legible
  — a gate whose maintenance cost climbs three quarters running is on a path to
  deletion-by-frustration; the trend catches it before someone rips it out. A skipped
  quarter records a zero-hours line (§ 3 skip rule). This append-only discipline mirrors
  the lineage-log posture the charter (081-AT-DECR, GC theme) requires for every
  SAK paper-trail artifact.
- **Ledger table (carried forward each quarter, append-only).**

| Quarter (end date)   | Gate              | FLAKE-TRIAGE hrs | FP-FIX hrs | FN-FIX hrs | UPSTREAM-ADAPT hrs | Gate subtotal    | Notes     |
| -------------------- | ----------------- | ---------------- | ---------- | ---------- | ------------------ | ---------------- | --------- |
| 2026-Q3 (2026-09-18) | G1                |                  |            |            |                    |                  | first run |
| 2026-Q3 (2026-09-18) | G2                |                  |            |            |                    |                  | first run |
| 2026-Q3 (2026-09-18) | G3                |                  |            |            |                    |                  | first run |
| 2026-Q3 (2026-09-18) | G4                |                  |            |            |                    |                  | first run |
|                      | **quarter total** |                  |            |            |                    | **(target < 4)** |           |

## 7. Dispositions (what a review can decide)

Each gate gets exactly one disposition per quarter:

- **KEEP** — within all budgets (FP < 2%, flakes within budget, FN = 0, maintenance
  share proportionate). No action; record the numbers.
- **RE-TUNE** — FP > 5%, or flake budget exceeded, or maintenance hours over budget
  attributable to that gate. Action: a tracked fix bead under the SSoT epic, fix lands
  before next quarter, the report names the specific change. RE-TUNE never weakens _what
  drift the gate catches_ — it tightens determinism / scope, never recall.
- **ESCALATE** — any confirmed false negative (a real drift the gate missed), or a
  utility-near-zero gate proposed for fold-in/removal. Routes to the named owner seat
  (§ 2): CTO for G1/G2/G4, CTO + CISO for G3. A gate _removal_ or recall-weakening is a
  Decision Record per Blueprint A § 2.3, never a unilateral review-time call, and a
  removal additionally consults the port-not-delete inventory (033 § 14.14).

**Asymmetry rule (binding).** A false negative always outranks any false-positive or
maintenance-cost concern. The cadence may never trade away recall to reduce noise: an
FP costs one human review; a missed material drift is unrecoverable (053-AT-SPEC).
RE-TUNE reduces noise _without_ reducing the drift surface caught; only an ESCALATE +
Decision Record may touch recall, and only upward.

## 8. Optional low-frequency reminder (implementation note, non-binding)

This spec is self-sufficient as the deliverable. Two reminder mechanisms are sanctioned;
either or both may be wired later without amending this spec:

1. **Tracked checklist bead (recommended).** Re-open a quarterly checklist bead
   parented to `bd_000-projects-9k5h` with a due-date 90 days out; `bd ready` surfaces
   it when due. Each quarter's run closes its bead with the filed report as evidence and
   opens the next. Lowest-tech, zero-CI, no rot surface.
2. **Cron stub (optional).** A `schedule:`-triggered GitHub Action that opens a deduped
   `[sak-ci-gate-quarterly]` reminder issue on the SSoT epic's repo. It MUST be
   reminder-only: it opens an issue, never reads or mutates a gate definition, never
   reds a PR. If wired, it follows the same dedup + ntfy posture as
   `leading-indicator-watch.yml` (063-AT-SPEC § "Side effects") but with _no_ gate-state
   side effects whatsoever. A cron stub is explicitly out of scope for closing this
   bead — the doc + checklist-bead reminder is the closeable surface.

## 9. Relationship to adjacent cadences

This 90-day CI-gate review is distinct from, and complementary to, two other cadences in
the SAK machinery — do not conflate them:

- **The AAR cadence (033 § 14.13.2)** fires on _phase milestones_ (Phase 1 ships,
  Phase 2 cutover, Phase 4 waves, Phase 4c flip) plus a quarterly roll-up. That measures
  _delivery_. This spec measures _gate health_. They can share a quarter's calendar slot
  but answer different questions.
- **The leading-indicator watcher (063-AT-SPEC, daily)** asks "has upstream shipped
  something that signals the whole SAK should cut over?" — a _strategic_ stop signal.
  This spec asks "are the four gates we run still doing their job well?" — a _tactical_
  health check. A leading indicator firing may make a gate's UPSTREAM-ADAPT burden
  spike here; that's expected coupling, not duplication.

## 10. Definition of done (this spec)

This document is the closeable deliverable for `bd_000-projects-39qj`. It is done when:

1. The four gates, their CI locations, and their owner seats are enumerated (§ 2) —
   **done**, ground-truthed against live CI (`coverage-map-gates.yml`,
   `prose-anchor-validity.yml`, `changelog-observance.yml` in `intent-eval-core`;
   `drift-eval-runner.py` in `intent-eval-lab` `ci.yml`).
2. The FP/FN measurement procedure with targets and oracles is specified (§ 4) — **done**.
3. A flake budget with per-gate determinism guardrails is specified (§ 5) — **done**.
4. A maintenance-burden ledger (append-only, bucketed, < 4 hr/quarter target) is
   specified (§ 6) — **done**.
5. The disposition set, the asymmetry rule, and the escalation routing are specified
   (§ 7) — **done**.
6. The reminder mechanism is named (§ 8) and the doc is filed + indexed per
   Document Filing Standard v4.3 — **done on merge**.

The first quarterly run (2026-Q3, due ≤ 2026-09-18) executes against this spec and files
the first `NNN-RR-LAND-sak-ci-gate-quarterly-<date>.md` report.

## Cross-references

- **Plan source:** `033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md` § 14.13.3
  (the 90-day cadence directive; closes F-WC-001).
- **Owner map:** `046-AT-STND-sak-governance-owners.md` (CTO owns kernel gates;
  CISO co-signs the G3 recall-floor write gate).
- **SSoT + continuity machinery:** `045-RR-LAND-single-source-of-truth-and-continuous-spec-compliance-2026-06-09.md`
  (§ 6 changelog-observance gate; the drift-watch + FF#2 spine this cadence keeps healthy).
- **G3 contract:** `053-AT-SPEC-drift-classification-eval-set-2026-06-12.md`
  (recall-floor write gate) + `055-AT-SPEC-llm-classifier-deterministic-walls-2026-06-12.md`
  (the walls bracketing the classifier).
- **Flake-budget prior art:** `063-AT-SPEC-leading-indicator-watcher-2026-06-12.md`
  § "Flake budget (<5% false positives)".
- **Required-vs-advisory audit:** `071-AA-AACR-iep-testing-cicd-audit-matrix-2026-06-18.md`
  (flags G1/G2/G4 as non-required PR checks in `intent-eval-core` — a finding this
  cadence's reviews should track toward making them required).
- **Charter stakes:** `081-AT-DECR-isedc-sak-class-1-charter-ratification-2026-06-17.md`
  (CSO continuity-spine-as-standing-cost rider; GC append-only-paper-trail theme).
