Verified. The load-bearing facts hold: 14 entities (no usage/human-review), `tenant_id` is optional-not-nullable on EvalSpec/EvalRun/SkillSnapshot/SkillVersion (DR-085 D5 / deferral-G), JudgeDecision's real predicate is `eval-verdict/v1`, c3-scan.ts exists, and the significance functions are real. Here is the deliverable.

---

# IEP Skill-Scoring Gap-Fill — Build-Ready Design Spec + Go/No-Go

**Epic:** intent-eval-lab#206 · **Source research:** `100-RR-LAND-...-2026-06-24.md` · **Status:** synthesized from gap-validation + per-item adversarial review

---

## 1. Executive go/no-go

**Verdict: GO — build it, but build a 3-item gap, not the 6-item slate as drawn, and only after one ISEDC nod.**

### Is the gap real

Yes, and it is the strongest kind: **a known, documented, un-built gap with the remedy already named in the research itself.** Verified against all three subsystems:

- **Kernel** (`intent-eval-core`): exactly 14 entities, zero `usage_events`, zero `human_reviews`, no adoption/popularity field anywhere in `SkillVersion`. The v1 schema dir has no usage/feedback schema.
- **j-rig**: `optimizer/experiment.ts` and `governance/baseline.ts` operate _exclusively_ on eval-set verdicts. `RefinerStrategy` consumes eval-score-driven `ScoredRollout`, never an adoption signal. This is the precise inversion of the meta_skill feedback→reward loop.
- **dashboard**: no usage/human-review intake. Every "annotation" is a visibility-tier publish-gate, not a human-trust review.

### Is it redundant with the validate-skillmd rubric? — NO. This is the question that could have killed the project; it doesn't

**The scoring layer is ORTHOGONAL, not redundant.** The distinction is load-bearing:

- **validate-skillmd grades the WRITING.** Every input is the SKILL.md's bytes-on-disk plus the filesystem. It runs _without LLM calls_, never runs the skill, never sees a model, a user, or time pass. It answers one question: "is this file well-authored?"
- **The proposed layer grades the BEHAVIOR, the PROVENANCE, and the REAL-WORLD PICKUP** — things invisible to static text analysis.

Of the 8 proposed scores, **exactly one ("Quality") touches the rubric, and the research doc explicitly delegates it BACK to the rubric unchanged** — a deliberate hand-off, not a parallel reimplementation. The remaining 7: 4 delegate to already-built IEP surfaces (j-rig, kernel, dashboard), and 3 (Adoption, Human-trust, Usefulness-slice) have no home anywhere. They cannot duplicate a rubric that has no concept of usage, humans, or slices. **One honest near-adjacency:** the proposed slice-utility shares the word "utility" with the rubric's `score_utility` pillar but not the referent — the rubric scores whether the _author documented_ use cases; the proposed layer scores the _realized value of each block_. Adjacent vocabulary, zero measurement overlap. **Verdict: adopt the 3 gap-scores, leave Quality with the rubric.**

### Is the gap analysis itself sound? — Mostly, with two corrections fed into the design

1. **It missed a genuine 3rd gap: a skill-to-skill DEPENDENCY/RELATIONSHIP GRAPH** (meta_skill `ms graph` — PageRank keystones, betweenness bottlenecks, cycle detection). No IEP entity models any edge between skills. This is arguably the _most shippable_ finding the report skipped: meta_skill's graph delegates to `bv`, the **same beads-graph engine IEP already runs on its own bead workspace** — IEP owns the engine but never points it at the skill catalog. "You already have `bv`, apply it to skills" was the strongest available finding and went unsurfaced. **It is NOT in epic #206's six items; flag it as a follow-on bead, do not bolt it in here.**
2. **Slice-utility (gap b) is softer than co-billed.** Its only existing implementation is a hardcoded const that the report itself says "DON'T COPY." That makes it "a feature nobody has built well," not "a thing meta_skill has that IEP lacks." It's still worth building (the _computed_ form is genuinely new) but it should be sequenced behind the two hard gaps, not as a co-equal.

### Bottom line

The 6 work items are each individually **NOT confirmed build-ready as drawn** — every one failed adversarial review on at least one hard rule. The gaps are real; the designs need the verifier's fixes applied before a line is written. **5 of 6 items have a kernel/governance dependency that warrants a single Class-2 ISEDC nod** (15th-entity expansion + tenant-axis precedent + new predicate URIs + a `RolloutDecision` enum change all ripple across signed consumers). Get that nod once, covering all of it, then build bottom-up.

---

## 2. Per-item build-ready design (verifier's fixes applied)

### Item 1 — `usage_events` (kernel, 15th entity) — **CONDITIONAL GO, 5 fixes mandatory**

**Entity shape:** Append-only product-metering ledger. One immutable row per billable/quota-relevant action. Distinct from `CostRecord` (which is provider-spend in money+tokens; UsageEvent is product-meter counts in business units). The `cost_record_ref` nullable back-reference is the seam proving they're separate tables. Single terminal state `recorded`; corrections are new rows, never mutation.

**Apply these fixes before building:**

- **FIX (tenant_id) — non-negotiable:** Change `tenant_id` from `REQUIRED, non-nullable` to **optional-not-nullable** (`tenant_id?: Uuidv7`, omitted from `required`). The design's claim that "no other entity carries a tenant axis" is **factually wrong** — EvalSpec, EvalRun, SkillSnapshot, and SkillVersion all carry it as optional per **DR-085 D5 / deferral-G (bd_000-projects-k0fj)**, verified in `deferral-specs.test.ts`. A required tenant violates the binding ruling. Cite the four existing fields as the precedent this **follows**, not breaks.
- **FIX (anti-gaming, Rule 3):** Add a REQUIRED cross-field invariant binding every metered (non-`api_call`) row to a verified/quality-gated source — non-nullable `source_entity_type`/`source_entity_id` for metered rows, plus a verified marker the runtime sets only after the source session clears its quality gate. **This MANDATES a `model_validator` / `.superRefine` / JSON-Schema `if-then`** — so **delete the "ZERO hand-validators needed" claim** (it was only true because the design omitted the rule). Sibling CostRecord/SessionTrace already carry hand-written validators for exactly this.
- **FIX (C3, Rule 2):** Add a normative consumer contract forbidding `SUM(quantity)` across distinct `meter` _or_ distinct `unit` values into one scalar. Rollups are per-`(meter,unit)` vectors only. Add a fixture/test asserting heterogeneous-meter rollup is out of contract.
- **FIX (compute-not-constant, Rule 1):** Add a HARD-RULE prose block: "`quantity` is a count of a verified action, never an assigned utility." No utility/weight is ever stored on the row. Any derived value lives in a downstream component that computes it from the ledger at read time.
- **FIX (factual):** Remove `dashboard_render` from the `meter` and `source_entity_type` enums — `dashboard-render` is a **predicate body**, not a lifecycle entity. Metering off a predicate-render conflates the entity and predicate layers.
- **FIX (Evidence Bundle):** A UsageEvent rides _inside the `extensions` field_ of an EvidenceStatement; it does **not become** an EvidenceStatement (those are pinned to `GateResultV1`). Drop the bare "content-addressable via sha256" claim unless you reference a canonical-JSON digest contract the kernel actually provides.

**Open question to resolve with the metering owner before locking the signed surface:** is `meter` a strictly-closed pricing enum (recommended, safest for billing) or the open kernel-registered pattern? Closed enum is a one-way door for renames/removals.

---

### Item 2 — `human_reviews` (kernel, sibling 15th entity) — **CONDITIONAL GO, 4 fixes mandatory**

**Entity shape:** A single human's open-ended assessment of an EvalRun — the human counterpart to JudgeDecision. Langfuse "scores" fold into **three orthogonal nullable channels** (this is the C3-clean choice — keep it): `score_text: string|null` (open-ended TEXT, intentionally not enum/number), `thumbs: boolean|null`, `annotation: string|null`. At-least-one-signal cross-field refinement. Single terminal state `recorded`; revisions are new rows via `supersedes_id`. FK spine: `eval_run_id` (required), `session_trace_id`/`judge_decision_id`/`supersedes_id` (nullable), `reviewer_identity: ActorIdentity`, `input_hash: Sha256`. `tenant_id?` reserved per deferral-G (this one is correct in the design).

**Apply these fixes before building:**

- **FIX (anti-gaming, Rule 3) — the gate is too weak:** "at-least-one-signal" is trivially gamed (a lone `thumbs=true` counts as a full review). **Require `session_trace_id` non-null OR `judge_decision_id` non-null** — a review must pin to something verified. Add a normative note that usage/utility counters consume HumanReview rows **only** when the referenced session passed its quality gate, and that **service-account-authored reviews are excluded from human-signal counts** (or tagged distinctly).
- **FIX (C3 value-layer, Rule 2):** `score_text` is free text the design's own examples show carrying "4/5", "strong", and prose — three dimensions hiding in one string. Pick one: either add an OPTIONAL structured `numeric_score: number|null` fourth channel so numbers stop hiding in text, **OR** make it normative that `score_text` is NON-COMPARABLE free text consumers MUST NOT parse into a scalar or aggregate.
- **FIX (factual) — corrects the central analogy:** JudgeDecision's predicate URI is **`eval-verdict/v1`**, NOT the implied `judge-decision/v1` (verified in `JudgeDecision.ts:7`). Re-anchor the "human agrees/overrides the machine verdict" workflow and the `judge_decision_id` FK against the real constant.
- **FIX (Evidence Bundle) — drop the overstated headline:** The real `EvidenceStatementSchema` is hard-pinned via `predicateType: z.literal(GATE_RESULT_V1_URI)` under `.strict()` — a `human-review/v1` row **cannot ride the existing payload schema**. Ship a **parallel additive `HumanReviewStatementSchema`** binding only `subject[0].digest.sha256 === input_hash` (no `gate_id` invariant). Scope this explicitly in the PR; it is net-new contract surface, not a flagged risk. The `KnownPredicateUri` edit target is the `PREDICATE_URIS` const in `src/predicates/gate-result-v1.ts` (verified), **not** `index.ts` as the design states.
- **Note:** `signing_mode: sigstore_staging` must be authorized by a DR (human review is non-reproducible, so it can never meet `rekor_production`'s reproduce-the-hash bar) — don't register it as a hand-edited constant; bind it in the DR.

---

### Item 3 — `slice_utility` (refiner-core, COMPUTED per-block) — **GO with fixes, lowest kernel risk**

**Algorithm: Leave-One-Block-Out (LOBO) causal attribution.** A block's utility is the **measured counterfactual drop in behavioral score when the block is ablated**, judged at the _same α=0.05 z-test bar_ the acceptance gate already uses. This is the deliberate inverse of meta_skill's const table (Policy=0.95 by fiat): here a block's _type_ is never its utility; its utility is the demonstrated effect of its presence.

Per anchorable block B (reusing existing machinery only):

1. `sliceIntoBlocks(doc)` → uniquely-anchorable spans (valid `DeleteOp` targets per `requireUnique`).
2. Build `DeleteOp{target: B.anchor}`, wrap in synthetic `EditProposal`, `applyEdit(doc, proposal)` → ablated variant.
3. Score variant against the SAME frozen eval set via injected `BlockScorer` seam (stubbable, keeps module pure).
4. `delta = baseline.behavioral.value − ablated.behavioral.value` (signed, computed). Classify via the real `isSignificantRegression`/`isSignificantImprovement` (verified in `accept.ts:116,133`): regression → `load-bearing`, improvement → `harmful` (cut candidate), neither → `inert`.

Two modes: **full-LOBO** (K+1 scorer calls) and **weakest-first/capped** (the meta_skill static-type bias is admissible **only as ablation ORDER** under `maxAblations`, never as the output score).

**Apply these fixes before building:**

- **FIX (anti-gaming, Rule 3):** Make eval-set quality a precondition. Refuse-or-flag (`evalSetQuality: 'ungated'`) when the set is `harvested`/`hybrid` without an explicit verified flag, and when `isRefreshDue(evalSet)` is true. Reuse the already-exported `isRefreshDue` + `evaluateEvalSet` — no new machinery. Synthetic/golden sets are admissible by construction.
- **FIX (correctness):** Schema-check the ablated variant **before scoring it** via the already-exported `kernelSkillFrontmatterValidator`. If ablation makes the doc schema-invalid (e.g. removing a required frontmatter field), classify as `schema-required` (utility:null), never score it. This is the correct meaning of "pair with decide.ts."
- **FIX (statistical power):** Carry `baselineN`/`ablatedN` on every `BlockUtility`. Split the non-significant bucket into `inert` (adequate n) vs `inconclusive` (underpowered). A low-power null must NOT read as a computed zero.
- **FIX (interface drift):** The prose promises `delta`, `utilityRank`, `skipped` but the type omits them. Add `utilityRank: number|null` and report-level `skipped: readonly string[]`; keep signed `utility`. One normative shape.
- **FIX (C3 structural):** No report-level aggregate field exists (good — keep it). Add a phantom/documented no-reduce marker and a consuming-surface test asserting no skill-level "usefulness %" is emitted.
- **HOLD THE LINE (Rule 4):** Do **NOT** make `BlockUtility` a kernel entity or emit a signed bundle row from this module in this PR. Keep it pure refiner-core; emission is deferred downstream. Any kernel routing is a separate gated bead with its own DR.

---

### Item 4 — `adoption_signal` (j-rig weighting) — **GO with fixes; this is where the bandit decision lives (see §3)**

**Mechanism: deterministic time-decayed adoption score with explicit thresholds — NOT a bandit.** (Full justification in §3.)

**Wiring:** New pure module `packages/refiner-core/src/adoption.ts` (no I/O, no `Date.now()`, caller injects `now` — mirrors `kernel-version.ts`). New `usage_events` fact table in `@j-rig/db`. The core join is the **2×2 of baseline-value-flag × decayed adoption, AND-combined never averaged:**

| bare model matches? | users keep it? | verdict                                       |
| ------------------- | -------------- | --------------------------------------------- |
| skill adds value    | high adoption  | `keep`                                        |
| skill adds value    | low adoption   | `watch` (discoverability problem)             |
| bare model matches  | high adoption  | `deprecate_review` (model caught up but used) |
| bare model matches  | low adoption   | `obsolete_review` (both axes agree)           |

Adoption is **advisory and only ever DEPRECATES, never PROMOTES**; the deterministic accept() gates stay authoritative for shipping.

**Apply these fixes before building:**

- **FIX (Rule 4 — enum):** Do **NOT** add `deprecate_review` to the `RolloutDecision` union in this PR. Put the 4-quadrant nuance in a **separate additive `LaunchReport.adoptionVerdict?: AdoptionVerdict`** field consumers opt into, leaving `RolloutDecision` untouched and exhaustiveness intact. (Enum extension, if ever wanted, is a separate ISEDC DR.)
- **FIX (Rule 5 — multi-tenant):** Compute **per-tenant decayed rates first, then aggregate with bounded per-tenant weight** (cap each tenant's contribution, or aggregate per-tenant verdicts with a quorum). Expose `perTenant: ReadonlyMap<...>`. A tenant below its own `minVolume` is excluded, not averaged in as noise. This makes the fairness claim real instead of asserted.
- **FIX (Rule 3 — ingestion gate):** Only count toward `acceptanceRate` events whose emitting session passed the deterministic gate. **Segregate `source:"ci"` (gate-anchored, trustworthy) from `source:"plugin"` (unverified)**; weight unverified at/near zero on the deprecate axis. Close the auto-accept Goodhart path at ingestion, not just the human backstop.
- **FIX (Rule 1 — thresholds):** Make thresholds calibrated/derived, not bare literals. Require the verdict to clear a significance margin given the decayed evidence weight (mirror `accept.ts`), or ship the floor as an empirically-tuned, per-ecosystem-overridable value **with a documented calibration procedure**. Add a back-test step before thresholds are load-bearing.
- **FIX (determinism):** `buildLaunchReport` already calls `new Date().toISOString()` directly (verified) — inject `now` into it (matching `kernel-version.ts`) so the artifact the adoption signal lands in is actually replayable. Otherwise the determinism argument used to reject the bandit is undercut by the very function being extended.

---

### Item 5 — `cli_verbs` (`j-rig ingest-skill` + `j-rig review`) — **GO with fixes; CASS gate is the core**

**Interface:** Two Commander verbs on the j-rig program, local-first SQLite writes via `@j-rig/db`.

- `j-rig ingest-skill <skill-dir> --session-id <id> [CASS flags] [--signal <s>] [--json]` — captures one usage/adoption event, gated by a CASS session-quality score.
- `j-rig review <skill-dir> --verdict up|down [--rationale <text>] [--reviewer <id>]` — captures a comment-grade human thumb + open-ended TEXT rationale.

**The CASS anti-gaming gate (load-bearing, ported from meta_skill `quality.rs`):** start 0.0; `tests_passed +0.25`, `clear_resolution +0.25`, `code_changes +0.15`, `user_confirmed +0.15`, `backtracking −0.10`, `abandoned −0.20`; **PASS ≥ 0.30.** A failing row is **persisted (`cass_passed=0`) but excluded from every adoption rollup** (`WHERE cass_passed=1`). Persist-but-exclude beats drop-on-ingest — it makes "load in a loop to inflate" _visible_ in the data. No `--force-count` path exists.

**Governance boundary (must not blur):** `j-rig review` is a **curated-signal** thumb (`governance_class="curated-signal"` on the row), explicitly **NOT** a signed in-toto `human-review/v1` predicate and **never a trust root** (doc 072 R6). Any future signed adjudication is a separate verb gated by the closed HR-1..HR-5 trigger set.

**Apply these fixes before building:**

- **FIX (Rule 5 — tenant, and there's no migration tooling):** Add a non-null `tenant_id`/`repo_slug` column to **both** tables **in the initial `CREATE TABLE`** (it cannot be retrofitted cleanly — `database.ts` is CREATE-TABLE-IF-NOT-EXISTS only, no ALTER path). Make every rollup tenant-scoped. Add a minimal migration shim as a pre-req bead so the inevitable future column additions aren't blocked.
- **FIX (Rule 2 — C3 in j-rig, not borrowed from dashboard):** Don't surface usage/reviews through `report` until a C3 guard exists _in j-rig_. Either port the dashboard `c3-scan.ts` detector into a shared check run in `pnpm run check`, or make `report --usage/--reviews` structurally incapable of a cross-dimension aggregate (one labeled count per dimension×predicate, + a test). `reward` stays per-event; any aggregate is scoped to ONE homogeneous signal type.
- **Scope v1:** record tenant-keyed `signal`/`reward`; **NO bandit/recommendation loop** until the multi-tenant-fit question is resolved. Resolve the open question to "recording is sufficient for v1, tenant-partitioned."
- **OTel stays off:** the OTel name set is closed/normative (doc 067); minting `usage.*`/`review.*` events is refused-on-sight until 067 is amended. Ship local-SQLite-only.

---

### Item 6 — `dashboard_surface` (C3-safe per-skill render) — **GO — the only item that PASSED review clean**

**Interface:** New read-only surface `site/skills/`, a sibling module to `src/results/`, rendering **per skill, per dimension, side-by-side, never rolled.** Consumes the SAME verify-before-render seam (`RenderInput` / `BundleResolver`) — no second ingest path. Three independent panels (Adoption / Human-trust / Quality), each self-contained with its own provenance, predicate URI, and the 4-timestamp surface (never collapsed). `SkillCard` has **no `rolledScore` field by construction** — that structural absence, not the regex, is the real C3 defense. Renderer signatures: `renderAdoptionPanel` / `renderHumanTrustPanel` / `renderQualityPanel` — **none takes more than one dimension's rows; there is deliberately no `renderRolledScore`.** no-data and no-trust render LOUD (reuse `noDataPanel`, `badge--no-data` == `badge--fail` weight).

**This item is CONFIRMED. Apply these hardenings (not violations):**

- **HARDEN (Rule 1 — no renderer arithmetic):** Any adoption rate/% shown must be a field the kernel `usage_events` entity computes and emits _inside the verified bundle_. The renderer must NOT divide `verifiedUsageCount` by anything — a renderer-side ratio is a hand-derived, unverified value. Add "no arithmetic in the renderer" to the structural guarantees. Rendering the raw verified count is fine.
- **HARDEN (Rule 3):** Add a resolver-invariant test asserting a row whose bundle was not verified-session-gated (or carries a raw-load count) is rejected/absent at the resolver — mirror how `bundle-resolver.ts` returns null for unverified bytes. Make the "NEVER raw loads" rule a tested invariant, not prose.
- **HARDEN (Rule 4):** Assert the resolver imports `usage_events`/`human_reviews` validators FROM `@intentsolutions/core` and never defines a local type (kernel anti-goal "Schema duplication forbidden").
- **CLARIFY:** Bead .6 ships ZERO kernel artifacts — it is pure consumer. EB-compatibility is the obligation of sibling beads .1/.2. The production resolver cannot wire until .1/.2 land; ship now fed by the in-memory fixture resolver with honest loud no-data state. **Don't mark .6 "done" implying live data.**

---

## 3. The bandit-vs-decay decision

**Recommendation: deterministic time-decayed adoption score with explicit thresholds. The Thompson-sampling bandit is rejected — not as a phase-2 option, as a category error for this surface.** Unconditional.

**Why decay/threshold wins:**

1. **Wrong question.** A bandit answers "which arm should _I_ pull _next_ to maximize _my_ reward?" — online action-selection under uncertainty. j-rig's adoption signal answers "across N tenants and M CI runs, is this skill still earning its keep vs. the bare model?" — that's **estimation + a monotone decision**, not exploration/exploitation. There is no arm to pull.
2. **Determinism is a hard contract; Thompson sampling is non-deterministic by definition.** It draws from posteriors via a PRNG. The same evidence would produce different gate outcomes on replay — that **breaks the Evidence Bundle / `gate-result/v1` audit-reproducibility contract, breaks `accept()`'s replayability, and breaks the launch-report as a stable artifact.** You cannot sign a non-deterministic verdict. The repo's whole posture (`kernel-version.ts` injects time rather than calling `Date.now()`) treats reproducibility as sacred.
3. **A bandit's exploration term would, by construction, occasionally route a CI rollout gate to the _inferior_ skill version to reduce posterior variance** — i.e. intentionally ship a worse skill sometimes. In a fail-closed gate that is indefensible.
4. **The data shape is wrong for it.** j-rig has batched, federated, sparse, per-tenant aggregate counts over time — not one sequential reward stream. A decay kernel handles recency-weighting (skills rot as base models improve) in closed form; a bandit posterior conflates "low evidence" with "explore me more," which is backwards — low-evidence skills should be _held_, not promoted.
5. **Multi-tenant fairness/privacy.** A per-tenant posterior either leaks one tenant's behavior into another's gate or needs N posteriors with no aggregation story. Decayed counts aggregate cleanly with per-tenant weighting from already-anonymized rollups.
6. **It composes with what exists.** `isObsoleteCandidate` (a threshold), `decideRollout` (a deterministic tree), the `accept.ts` z-test machinery, and the exact decay/supersession precedent in `kernel-version.ts` are all already there. The bandit would be a foreign PRNG-seeded stateful posterior store fitting none of these seams.

**Where the bandit IS legitimate — and why it isn't this surface:** if/when the **Skill Refiner** needs to choose _which RefinerStrategy to try next_ per skill under a fixed token budget (NaiveInContext vs SkillOptStyle vs future), that is a genuine single-stream exploration/exploitation problem and a **contextual bandit is a candidate there — inside `@intentsolutions/refiner`, never in the rollout/adoption gate.** Keep the two concerns surgically separate. (The `cli_verbs` design correctly records `signal`/`reward` for _later_ use without building a bandit — that's the right v1 posture.)

---

## 4. Hard-rule adherence (post-fix)

| Rule                       | Status after fixes                               | Where it bites                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| -------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Compute-not-constant**   | ✅ enforced                                      | Slice-utility is computed-from-eval-signal by construction (the whole point). Adoption thresholds must be calibrated/derived, not bare literals (Item 4 fix). UsageEvent `quantity` is a counted action, never an assigned utility (prose HARD RULE). Dashboard renderer does NO arithmetic (Item 6 harden).                                                                                                                                                                                                |
| **C3 — no rolled score**   | ✅ enforced structurally                         | Dashboard: no `rolledScore` field, no multi-dimension renderer. Slice-utility: per-block vector, no aggregate. UsageEvent: no cross-`(meter,unit)` SUM. HumanReview: 3 orthogonal channels, `score_text` non-comparable. CLI: C3 guard ported into j-rig, `report` emits per-dimension counts only. Adoption: 2×2 AND-combined, never averaged. **Note: the literal `c3-scan.ts` regex only catches "pass" — every surface is defended by absence-of-rolling-code-path + a structural test, not the regex alone.** |
| **Anti-gaming**            | ✅ enforced (was the most-violated rule pre-fix) | CASS gate ≥0.30 (CLI). UsageEvent requires a verified gated source (cross-field invariant). HumanReview must pin to a verified session; service-account reviews excluded. Adoption counts only gate-anchored `source:"ci"` events. Slice-utility refuses ungated/stale eval sets. Dashboard rejects unverified rows at the resolver.                                                                                                                                                                        |
| **Kernel-additive**        | ✅ enforced                                      | New files only, zero edits to the 14 entity files; append-one-line to indices. `tenant_id` optional-not-nullable per DR-085 D5 (Item 1 fix corrects a required-tenant violation). HumanReview ships a parallel additive `HumanReviewStatement`, not a mutation of the gate-pinned `EvidenceStatement`. Adoption does NOT mutate `RolloutDecision` (additive field instead). Slice-utility stays out of the kernel entirely. No schema duplication (dashboard imports kernel validators).                    |
| **Evidence-Bundle compat** | ✅ with corrected claims                         | UsageEvent rides in `extensions`, doesn't _become_ an EvidenceStatement; sha256 content-addressability claim dropped unless a canonical-JSON contract is referenced. HumanReview gets a real parallel statement type. Slice-utility defers emission downstream (vacuous-by-deferral). Dashboard's EB obligation is its siblings' (.1/.2), each shipping a kernel triplet.                                                                                                                                   |

---

## 5. Open risks + sequencing

### Genuine unknowns (not yet resolved by design)

1. **The `meter` enum closed-vs-open call** (UsageEvent) — a pricing decision, one-way door once signed. Needs the metering owner before merge.
2. **`tenant_id` mandatory-vs-reserved** — RESOLVED to _reserved_ by DR-085 D5. If metering genuinely needs a mandatory tenant, that's a documented divergence requiring its own ISEDC nod, not a unilateral ship.
3. **Adoption threshold calibration** — `halfLifeDays`/`minVolume`/floors need empirical tuning from real event distributions, possibly tied to model-release cadence (skills rot fastest right after a frontier bump). Ship conservative defaults + a back-test; don't let bare literals become load-bearing.
4. **Block interaction effects** (slice-utility) — LOBO is a first-order approximation; two blocks that only matter together each look inert when ablated singly. True Shapley is 2^K — out of scope. Document LOBO as first-order, pairwise as a wave-2 opt-in flag.
5. **The missed 3rd gap** — the skill-to-skill dependency graph (`bv` applied to the skill catalog) is the highest-leverage un-scoped finding. File it as a follow-on bead under #206; it is genuinely new, most-shippable, and not in the current six.
6. **`human-review/v1` permanent-staging** — non-reproducible predicates can never meet `rekor_production`'s reproduce-the-hash bar; the authorizing DR must state staging-is-permanent (or define a different promotion criterion).

### Build order (bottom-up — dependencies first, fail-closed)

**Gate 0 — ISEDC nod (do this once, covering all of it):** 15th-entity expansion + the tenant-axis precedent confirmation + the two new predicate URIs + the launch-report artifact semantics. Cite DR-085 D5 + the `skill-refiner-pass/v1` (DR-082) net-new-predicate precedent. This is one Class-2 review, not five. **Nothing below ships until this lands** and the refiner-labeled `bd-claim-precheck` STATUS gate is satisfied for the gated beads.

1. **Item 1 `usage_events`** + **Item 2 `human_reviews`** (kernel triplets, parallel) — these are the foundation; everything else reads them. Apply all fixes; run `codegen:validators` → `codegen:pydantic` → `check` (mandatory order). Each lands as the additive feature of the next kernel minor.
2. **Item 5 `cli_verbs`** — the intake surface that _writes_ usage/review rows, with the CASS gate + tenant column in the initial CREATE TABLE. Depends on the entity shapes from (1).
3. **Item 4 `adoption_signal`** — the j-rig weighting (decay/threshold) that _consumes_ the usage rows into launch-report verdicts. Depends on (1) and the ingestion source-segregation from (5).
4. **Item 3 `slice_utility`** — independent of the kernel work (pure refiner-core), can run in parallel with 1–4 once the eval-set quality preconditions are wired. Sequence it _behind_ the two hard gaps since it's the softer gap.
5. **Item 6 `dashboard_surface`** — the render surface, **last**. Ship the seam + fixture resolver early for the honest no-data state, but the production resolver wires only after (1)'s entities land. Don't mark done implying live data.

**Discipline reminders:** close beads bottom-up via `bd-sync close` (never raw `bd close` — the mirror drifts), one logical cluster per GH issue (not one per task bead), and adversarially verify each "close-now" — only a minority survive scrutiny. The dashboard item (6) is the only one confirmed clean as-drawn; the other five are GO **only with the verifier's fixes applied**, not as originally designed.

**Files verified in support of this spec:** `intent-eval-core/src/entities/{JudgeDecision.ts:7 (eval-verdict/v1), deferral-specs.test.ts (DR-085 D5 tenant reservation), index.ts (14 entities)}`, `intent-eval-core/src/predicates/{index.ts, gate-result-v1.ts (PREDICATE_URIS)}`, `intent-eval-dashboard/src/results/c3-scan.ts`, `j-rig-binary-eval/packages/refiner-core/src/accept.ts:{116,133}`.
