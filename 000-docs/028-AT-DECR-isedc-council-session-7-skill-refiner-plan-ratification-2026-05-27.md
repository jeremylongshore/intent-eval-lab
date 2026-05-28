# ISEDC Session 7 — Decision Record

**Date:** 2026-05-27
**Topic:** Skill Refiner plan 027 v4.1 ratification — Plan Audit findings + 13-thinker tension arbitrations + 7-seat ISEDC adjudication
**Subject artifact:** `intent-eval-platform/intent-eval-lab/000-docs/027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` (v4.1, commit `22fc55e`, PR #77)
**Acting head of board:** Claude (acting CTO designated by Jeremy Longshore via CTO-mode delegation, this session)
**Council size:** 7 ISEDC seats (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel) + 13 thinker-canon prior input
**Decisions logged:** 10 (4 tension arbitrations + 6 P0 ratifications)
**Status:** RATIFIED-WITH-DELTAS (plan 027 v5 to be authored in Step 5 remediation; STATUS.md → RATIFIED after v5 lands)
**References:** Plan Audit at `intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/`; ISEDC session JSONL at `~/.claude/skills/exec-decision-council/sessions/2026-05-27-skill-refiner-plan-ratification/`

## 1. Mission of the Decision Record

Ratify the Skill Refiner buildout plan (027 v4.1) before any first `bd claim` per § 13 Step 7 hard gate. Adjudicate 4 cross-seat tensions left unresolved by the 7-seat Plan Audit panel, ratify 6 convergent P0 remediations as binding, and produce the binding Decision Record that authorizes plan v5 amendment.

## 2. Why a council, not a single review

Plan 027 was authored by a single agent (Claude) over multiple iterations and validated through internal reviewers + a 7-seat thinker-canon panel + 6 additional thinker-canon arbitrations. Three load-bearing decisions remained genuinely contested:

- The SkillVersion entity shape ships as a one-way door in signed `@intentsolutions/core@0.3.0` Rekor entries
- The Phase D "deferred indefinitely" framing carries implicit-obligation legal surface
- The brand framing ("Skill Refiner is a product" vs "mechanism is swappable, eval is product") affects developer mental model + the 3-product agent-rig narrative

Single-reviewer reasoning is insufficient for these asymmetric-cost decisions; the ISEDC pattern is the response. Hickey F-RH-003 / Lamport F-LL-07 explicitly flagged the methodologically-recursive risk of a single-author plan being self-audited.

## 3. Synthesis lenses applied

1. The arena (5 surfaces): APIs · CLIs · MCP servers · agents · SKILL.md
2. Both sides: client-side eval + server-side eval
3. Transformation pipeline: API → CLI → MCP → SKILL.md → agent
4. Composable partial attestation: every component a valid entry; silence ≠ failure

## 4. The 10 questions adjudicated

| # | Question | Why this is immutable/costly |
|---|---|---|
| T1 | SkillVersion / SkillSnapshot resolution (merge / discriminator / orthogonal-no-FK / state-machine) | Schema name ships in signed Rekor entries + npm `@intentsolutions/core@0.3.0`; consumer-cited names are one-way doors |
| T2 | Phase D "creator sub-product" resolution (anti-goal vs quarterly trigger) | Anti-goal removes implicit-obligation legal surface; quarterly trigger creates recurring bandwidth tax |
| T3 | Process discipline weight (collapse to bd-as-writer + projections vs 7 parallel disciplines) | CI cost + contributor friction + supply-chain attestation pattern alignment |
| T4 | Mechanism-vs-product brand framing | Affects 45k+ NPM following mental model + 3-product agent-rig narrative + IS positioning vs SkillsBench paper |
| P0-1 | Acceptance gate "strict on all dims" → formal partial-order predicate | Predicate ships in signed `skill-refiner-pass/v1` URI |
| P0-2 | Append-only event log + Rekor consistency model + `version_kind` + `pending_production` state | Cross-field invariant `rekor_log_index iff signing_mode='production'` is CISO binding |
| P0-3 | Null-hypothesis Phase A.0 baseline (naive-Opus-in-context vs Refiner) | Saves weeks of Phase B if null-hypothesis holds; transparency win regardless |
| P0-4 | Hard-gate enforcement (`bd claim` pre-check honoring Plan Audit STATUS) | Honor-system gates create plausible-deniability + multi-system-of-record liability |
| P0-5 | AC-7 swap interface operationalization (`RefinerStrategy` + 2 reference impls) | AC-7 claim is unsubstantiated until interface exists; misrepresentation exposure if external audit checks |
| P0-6 | EvalSet versioning/lineage/refresh moved from Phase F to Phase A | First Refiner pass runs against an un-versioned eval set under current plan; load-bearing per SkillsBench finding |

## 5. Council composition

| Seat | Value system | Bias | Typical adversaries |
|---|---|---|---|
| CTO | Technical durability · schema integrity · immutability awareness · future-proofing | Deliberation > commit · empirical evidence > authorship claims | CMO, CSO on speed-of-filing |
| GC | IP protection · partner-consent compliance · audit-trail discipline | Written consent before reference; paper trail sacrosanct | CMO, CSO |
| CMO | Positioning · narrative coherence · tagline alignment · first-mover authorship | Visible > silent · ambitious > conservative | GC, CFO, CSO |
| CFO | Sole-prop bandwidth · customer-signal gating · opportunity cost | Defer until customer evidence justifies | CMO, CSO |
| CSO | OTel SIG-GenAI / in-toto / SLSA / AgentSkills.io realpolitik | Community-temperature precedes RFC; first-impression permanent | CMO |
| CISO | Supply-chain attestation integrity · signing infra · threat model · Rekor discipline | Reserve schema slots for signing fields NOW; scoped subdomains | CMO, CTO |
| VP DevRel | Developer-audience signal · OSS contribution dynamics · friction-to-adopt | "Saturday-developer test"; informal > formal | GC, CMO |

Plus 13 thinker-canon arbitrations as evidence: Hickey, Beck, Karpathy, Huyen, Lamport, Cunningham, Kleppmann (original Plan Audit panel) + Fowler, Gregg, Torvalds, Pike, Thompson, Armstrong (tension-arbitration extension).

## 6. Per-question record

### T1 — SkillVersion / SkillSnapshot resolution

**Vote tally (20 voices total):**

| Path | Thinker panel (13) | ISEDC (7) | Total | Weight |
|---|---|---|---|---|
| DISCRIMINATOR (separate entities + `version_kind` discriminator field; richest signing surface) | Kleppmann · Fowler · Gregg | GC · CSO · CISO | **6** | Plurality + strongest argument |
| MERGE (one entity + `kind` discriminator) | Hickey-implied · Torvalds · Thompson | CTO · CFO | 5 | Second |
| ORTHOGONAL no-FK (two entities, no relationship) | Pike · internal-architect | — | 2 | Minority |
| STATE-MACHINE separate | Lamport · Armstrong | — | 2 | Minority |
| Defer (mechanism not their seat) | — | CMO · VP DevRel | 2 abstentions w/ constraints | — |

**Primary tension:** MERGE camp (CTO + CFO + 3 thinkers) prioritizes simplicity-and-shipping-speed. DISCRIMINATOR camp (GC + CSO + CISO + 3 thinkers) prioritizes irreversibility-of-signed-kernel + signing-surface fidelity. CTO offered "orthogonal-no-FK as fallback if signing surface needs it" — implicit concession to CISO objection.

**Verbatim load-bearing positions:**
- **CISO:** "`version_kind` becomes a signable claim in the predicate payload. Merge loses lineage provenance under signed Rekor entries."
- **GC:** "Merging entities AFTER public npm publish (`@intentsolutions/core@0.3.0`) is a one-way door — consumers cite v0.3.0 by name. Discriminator + state machine has the richest audit surface."
- **CMO:** "Veto any outcome where `SkillSnapshot` becomes the named-in-spec artifact. `SkillVersion` must remain the citable term."
- **CTO:** "MERGE — one `SkillVersion` entity with `kind` discriminator. Accept Pike's orthogonal-no-FK only if two concrete cross-field invariants cannot be expressed by the merged type."
- **VP DevRel:** "CLI noun stability is the binding constraint — the type the developer imports must equal the noun in CLI output."

**DECISION (acting head of board):** **DISCRIMINATOR + separate entities with `version_kind` field on SkillVersion.** Specifically:
- SkillVersion ships as a NEW entity in `@intentsolutions/core@0.3.0` schema (14th canonical)
- SkillSnapshot stays as the existing entity (unchanged)
- SkillVersion carries `version_kind: 'edit' | 'revert' | 'restore'` field (load-bearing signable claim)
- SkillVersion carries `parent_version_id` referencing prior SkillVersion (NOT FK to SkillSnapshot; lineage internal)
- SkillVersion carries `source_snapshot_hash` reference to the SkillSnapshot at the moment of refinement (read-only reference; not a relational FK)
- The names "SkillVersion" + "SkillSnapshot" both ship as named-in-spec artifacts (honors CMO veto)

**Rationale:** the DISCRIMINATOR path wins on both headcount (6 vs 5) AND argument strength. The signing-surface concern (CISO) + irreversibility concern (GC) are concrete and load-bearing; the MERGE camp's simplicity argument is aesthetic. The CTO's offered fallback (orthogonal-no-FK) is fold-in to the discriminator path via the `source_snapshot_hash` being a reference, not a FK — preserves the schema-integrity orthogonality without losing the discriminator signal.

**Dissent acknowledged (verbatim):**
- CTO: "Reject Kleppmann 'discriminator + separate' as cluttered union trap. Reject Lamport/Armstrong state-machine path as over-engineered for v0.3.0 ship."
- CFO: "Cheapest to ship + cheapest to carry. Rejected state-machine as over-investment for v0.3.0."
- Thompson: "MERGE — one entity. Splitting later is cheap; un-splitting two Rekor-signed entities is not."

**Binding minority constraints (folded into decision):**
- (CTO) State-machine formalism deferred to a follow-up doc (NOT in v0.3.0 ship). Phase C ships entity + discriminator + `parent_version_id` only.
- (CFO) Scope bound: discriminator adds < 1 week to Phase C vs MERGE baseline. Implementation must respect this.
- (CMO) Both entity names ship as named artifacts in Blueprint B § 7 + glossary.
- (Lamport/Armstrong) State-machine spec authored as a SECOND DR in v0.4.0 — not now.

### T2 — Phase D "creator sub-product" resolution

**Vote tally:**

| Path | Thinker panel (13) | ISEDC (7) | Total |
|---|---|---|---|
| **ANTI-GOAL** in Blueprint A § 3 (with re-opening reserved for future ISEDC) | Cunningham · Fowler · Torvalds · Pike · Thompson · Armstrong | CTO (compromise) · GC · CMO · CFO · CSO · CISO | **12 STRONG MAJORITY** |
| Quarterly + on-frontier-release re-evaluation triggers | Karpathy · Gregg | — | 2 |
| Defer (out of seat) | — | VP DevRel (supports anti-goal) | — |

**Primary tension:** Karpathy + Gregg want capability-signal triggers preserved for bitter-lesson hedging. Everyone else wants the cleaner anti-goal posture.

**Verbatim load-bearing positions:**
- **GC:** "Anti-goal is the more legally-defensible posture — explicit non-commitment in Blueprint A removes future 'you promised Phase D' claims from any partner contract."
- **CMO:** "Anti-claim ('we don't build skill generators because the math doesn't work — here's SkillsBench') is differentiating brand gold. Anti-goal IS the marketing move."
- **CFO:** "Quarterly trigger costs 4–8 days/year recurring forever; anti-goal is zero cost and reversible by future ISEDC. Highest-ROI bandwidth call in the session."
- **CSO:** "Anti-goal is cleaner standards-body positioning. Quarterly leaves IS in uncategorizable middle for agentskills.io WG."
- **Karpathy (dissent):** "Quarterly + on-release re-measurement keeps the option open at low cost."

**DECISION:** **ANTI-GOAL.** Phase D is removed from plan 027 v5 and Blueprint A § 3 is amended to add:

> **§ 3.X Anti-goal — IS does not build a creator product for SKILL.md generation.** SkillsBench (arXiv 2602.12670) demonstrates that self-generated skills underperform the no-skill baseline ("no benefit on average") while human-curated skills deliver +16.2pp. IS's role is to refine human-curated skills via evals-gated edits, not to displace human curation. Re-opening this anti-goal requires a future ISEDC session triggered by externally-published evidence that frontier models can self-generate skills above the curated baseline.

**Dissent acknowledged (verbatim):**
- Karpathy: "Phase D 'deferred indefinitely' has only two re-open triggers (external work / partner asks), both demand-signals. The upstream capability-signal (frontier model release) is silent."
- Gregg: "Convert Karpathy's 'quarterly cadence' and Cunningham's 'anti-goal' into a falsifiable trigger metric: self-gen lift > +8pp on the kernel-pinned eval set on any frontier release, OR internal acceptance rate parity."

**Binding minority constraints:**
- (Karpathy + Gregg) Gregg's falsifiable trigger metric (`self-gen lift > +8pp on kernel-pinned eval set on any frontier release`) is the re-opening trigger condition. ISEDC reconvenes if this metric is observed.
- (CISO) Anti-goal review revisited at every Blueprint A amendment cycle.

### T3 — Process discipline weight

**Vote tally:**

| Path | Total |
|---|---|
| **COLLAPSE: bd-as-linearizable-writer + GH/Plane as read-only projections** | **All 13 thinkers + all 7 ISEDC seats = 20/20 CONSENSUS** |
| Keep as 7 parallel disciplines | 0 |

**Primary tension:** none. Universal consensus across all 20 voices.

**Verbatim load-bearing positions:**
- **VP DevRel:** "7 process disciplines mean a contributor PR gets bounced 7 ways. Murder."
- **CFO:** "7 disciplines × maintenance burden = unsustainable for a sole-prop."
- **CSO:** "Single-writer attestation surface is CORRECT supply-chain pattern. In-toto + sigstore world is moving toward single-writer + verifiable-projection patterns. Tri-link with 3 writers is OPPOSITE of standards-aligned."
- **CISO:** "Multiple writers = multiple compromise paths."
- **GC:** "Eliminates legal-discovery ambiguity (which copy is canonical for litigation?)."

**DECISION:** **COLLAPSE to bd-as-writer + GH/Plane as projections.** Specifically:
- AC-12 in plan 027 v5 is rewritten as: "tri-link discipline = bd is the canonical writer of bead↔doc↔GH-issue cross-refs; GH issue bodies + doc front-matter are GENERATED PROJECTIONS via `bd-sync`; humans editing GH or doc bodies directly is a CI-detected anomaly that re-projects from bd."
- `validate-trilink.sh` is simplified: Check 1 (bead has Doc + GitHub fields) stays; Checks 2 + 3 become advisory-only (the projections are generated, so checking them is checking the generator).
- The 7 parallel disciplines collapse to ONE: "bd is source; everything else is projection."
- `~/bin/bd-sync` is extended to be the GENERATOR (push bd cross-refs to GH body + doc front-matter) instead of mirroring.

**Binding minority constraints:** none (consensus).

**Implementation deltas:**
- Plan 027 § 3.5 (PR-1 through PR-5) collapses to one PR-1
- Plan § 5.5 verifier discussion simplifies
- `~/bin/bd-sync` extension is a new bead under RC-IEL or new dedicated bead

### T4 — Mechanism-vs-product brand framing

**Vote tally:**

| Path | Thinker panel (13) | ISEDC (7) | Total |
|---|---|---|---|
| Mechanism-swappable, EVAL IS THE PRODUCT (collapse to single-product framing) | Fowler · Gregg · Pike · Thompson · Armstrong · CSO (mild) | — | 6 |
| **Skill Refiner stays as a NAMED PRODUCT in the 3-product stack; AC-7 documents the swap interface as internal engineering hedge** | Torvalds (action-level) · Karpathy (dissented in own arbitration but didn't pick) | CMO · CFO · VP DevRel | **3 + strong-argument** |
| Defer | — | CTO · GC · CISO | 3 abstentions |

**Primary tension:** CMO/CFO/VP DevRel preserve the 3-product agent-rig stack brand; thinker majority + CSO push for "eval is the product / mechanism swappable" framing.

**Verbatim load-bearing positions:**
- **CMO:** "The 3-product agent-rig stack framing is the entire brand story (Test → Improve → Ship). Collapsing to 'eval-guided improvement mechanism' commoditizes positioning and surrenders authorship. Push BACK on the consensus."
- **VP DevRel:** "CLI command IS the mental model. `j-rig refine` is the verb that gets tweeted. `@j-rig/refiner` is the npm package developers search/fork. Named product, AC-7 lives as internal engineering hedge."
- **CFO:** "Already rebranded twice in v4 history; third rebrand inside a month is brand-instability signal. Pushed back on CMO if they push too hard for full reframe; accept 'AC-7 documents the technical reality, brand stays.'"
- **Pike (dissent):** "IS sells THE EVAL DISCIPLINE, not the refiner. 'Show me your eval set and I'll tell you what you sell.' The refiner is implementation detail."
- **Armstrong:** "The eval set + refiner are concurrent — eval runs on a frozen kernel while refiner proposes against it. IS sells THE GUARANTEE that the eval set is decoupled from the refiner mechanism. Mechanism is swappable per AC-7; the eval set guarantee is the product."

**DECISION:** **Skill Refiner stays as a NAMED product in the 3-product agent-rig stack** (Test → Improve → Ship). AC-7 is operationalized via the `RefinerStrategy` interface (per P0-RATIFY-5) as the engineering hedge. The "eval is the product" framing is preserved AS the internal architectural truth (documented in Blueprint A) but does NOT override the consumer-facing 3-product brand.

**Rationale:** CMO + CFO + VP DevRel form a 3-seat business-axis consensus. The thinker-majority argument is architecturally correct (the eval IS the durable artifact) but the BRAND is a separate concern from the architecture. Brand-instability cost (3rd rebrand in one month per CFO) + developer-mental-model preservation (per VP DevRel) + 45k+ NPM following alignment (per CMO) outweigh the elegance of the thinker-consensus reframe. **Both can be true:** the architecture treats mechanism as swappable; the brand treats Skill Refiner as a named product. AC-7 is the bridge.

**Dissent acknowledged (verbatim):**
- Pike: "Demote Skill Refiner to a feature of J-Rig (the eval discipline IS the product). Three-product stack collapses to two."
- Fowler: "The `skill-refiner-pass/v1` predicate contract is the durable artifact; Refiner is one reference implementation."
- Thompson: "The eval set is the product. Promote Huyen's F-CH-001 (eval-set lineage) from Phase F to Phase A.0 alongside the bitter-lesson baseline."

**Binding minority constraints:**
- (Pike + Thompson + Fowler) AC-7 swap interface (`RefinerStrategy`) MUST be operationalized in Phase A per P0-RATIFY-5. Without it, the "named product" framing is misrepresentation.
- (Thompson) EvalSet lineage IS moved from Phase F to Phase A per P0-RATIFY-6.
- (Pike) The phrase "Skill Refiner is one reference implementation of the eval-guided improvement loop" lands as canonical positioning language in Blueprint A.
- (CSO) Standards-body lead-with-eval positioning preserved separately from consumer-facing 3-product brand.

### P0-RATIFY-1 — Acceptance gate "strict on all dims" → formal partial-order predicate

**Vote:** 20/20 RATIFY YES. Universal consensus across thinker panel + ISEDC.

**DECISION:** **RATIFIED with these implementation deltas:**
- Plan AC-3 amended: `accept()` predicate = "Pareto-dominant on the kernel-pinned `behavioral` dimension AND non-regressing on all other named dimensions, with statistical-significance threshold T at α=0.05"
- Dimension set is PINNED in `@intentsolutions/core@0.3.0` SkillVersion schema (per CISO determinism binding)
- Tie-breaking rule for Pareto-incomparable cases: "if neither version Pareto-dominates the other, the candidate is REJECTED and added to the rejected-edit buffer with reason `pareto-incomparable`" (per Kleppmann F-MK-6 + CSO normative-spec)
- Significance threshold + tie-breaking SHIP IN `skill-refiner-pass/v1` predicate JSON Schema, NORMATIVELY (per CSO binding)

### P0-RATIFY-2 — Append-only event log + Rekor consistency model

**Vote:** 20/20 RATIFY YES.

**DECISION:** **RATIFIED with these implementation deltas:**
- AC-2 amended to specify: "local event log is append-only at the FILESYSTEM level (no rename, no truncate); Rekor entries are append-only at the TRANSPARENCY-LOG level; the two consistency models are independent."
- `version_kind: 'edit' | 'revert' | 'restore'` field added to SkillVersion schema (folded into T1 decision)
- `pending_production` intermediate state added — SkillVersion can be `pending_production` while Rekor is being written; cross-field invariant relaxed to `rekor_log_index non-null iff signing_mode='production' AND status='active'`
- Outbox + reconciler pattern: every `pending_production` row carries `retry_after` timestamp + `max_retries: 5` (CISO binding); after max retries, `signing_failed` status surfaces to human
- Rekor unavailability does NOT block local SkillVersion creation; downgrades to `signing_mode='staging'` with explicit `signing_downgrade_reason` field

### P0-RATIFY-3 — Null-hypothesis Phase A.0 baseline

**Vote:** 20/20 RATIFY YES.

**DECISION:** **RATIFIED. Phase A.0 ships before Phase A.** Specifically:
- Phase A.0 deliverable: comparison of naive-Opus-in-context-with-eval-set vs the proposed Refiner mechanism on the Phase B demo skill (`/validate-skillmd` per Step 0 § 7.1 resolution)
- Decision rule: if naive baseline achieves > 70% of projected Refiner lift, DESCOPE Phase B mechanism (per Karpathy F-AK-001 sample finding)
- Per VP DevRel binding: result is PUBLISHED as a blog post regardless of outcome (transparency wins community trust even if mechanism loses)
- Per CMO binding: pre-brief comms for both outcomes; result is NOT a surprise

### P0-RATIFY-4 — Hard-gate enforcement

**Vote:** 20/20 RATIFY YES.

**DECISION:** **RATIFIED with VP DevRel external-contributor delta.**
- `bd claim` pre-check honoring Plan Audit STATUS file IS IMPLEMENTED
- Internal `bd claim` calls are HARD-GATED (block until STATUS = RATIFIED) per CISO threat-model binding
- External-contributor PRs (PRs from non-IS GitHub users) see the gate as a CI WARNING + a `contributor-acknowledgment` requirement, not a hard block (per VP DevRel binding)
- The enforcement script lives in `intent-eval-lab/scripts/bd-claim-precheck.sh` (parallel to `validate-trilink.sh`)

### P0-RATIFY-5 — AC-7 swap interface operationalization

**Vote:** 20/20 RATIFY YES.

**DECISION:** **RATIFIED with implementation deltas:**
- `RefinerStrategy` interface defined in `@j-rig/refiner-core/strategies/` (one TypeScript interface)
- Phase A ships TWO reference implementations:
  - `NaiveInContextStrategy` (also serves as the Phase A.0 null-hypothesis baseline per P0-RATIFY-3)
  - `SkillOptStyleStrategy` (the original v4.1 propose() mechanism, refactored as a strategy impl)
- Per CISO signed-manifest binding: `refiner_strategy_id` field added to SkillVersion schema; signed in predicate payload
- Per VP DevRel community-extension binding: `RefinerStrategy` interface documented in `j-rig-binary-eval/000-docs/` with conformance-test suite for community contributors

### P0-RATIFY-6 — EvalSet versioning moved from Phase F to Phase A

**Vote:** 20/20 RATIFY YES with scope deltas.

**DECISION:** **RATIFIED.** Phase A surface for EvalSet:
- `EvalSet` value type extended with `eval_set_version` (semver) + `lineage_parent` (hash of prior eval set) + `refresh_due_at` (rfc3339 timestamp; 90 days default)
- `j-rig refine bootstrap` CLI subcommand produces an EvalSet with all three fields populated
- Per CFO scope discipline: refresh-cadence enforcement + deprecation policy stay in Phase F (Phase A ships the schema; Phase F operationalizes the cadence)
- Per VP DevRel `--quick` mode binding: `j-rig refine bootstrap --quick` produces a lightweight eval set with version + lineage but skips refresh-due-at + comprehensive coverage analysis (for casual contributors)
- Per Thompson trust binding: eval sets are SIGNED with the same sigstore identity as SkillVersion (closes the Trusting-Trust loop — IS signs both the skill AND the eval used to grade it)

## 7. Council memos verbatim (cross-question themes)

(Excerpts from the seat memo sections — preserved per ISEDC adversarial-integrity protocol.)

**CTO:** "Cross-question theme is 'prose-as-substitute-for-schema.' Most costly to recover from = T1 (only genuine one-way door). Recommended 60% of session time on T1; ratify T2/T3/P0-1..6 in a single block; T4 brand call deferred to CMO with binding engineering constraint."

**GC:** "The unifying defect is too many implicit obligations + undefined predicates + honor-system gates + multi-system-of-record fact-stores — each creates discovery or misrepresentation exposure."

**CMO:** "Anti-goal IS the marketing move. Surprise alignment with GC + thinker majority on T2. But T4 brand reframe surrenders authorship — collapsing to 'eval discipline' loses positioning we've earned with 45k+ NPM following."

**CFO:** "Highest-ROI bandwidth call in the session is T2 anti-goal (zero recurring cost vs 4-8 days/year). Hard line drawn at +4 weeks for any single remediation."

**CSO:** "Standards-body realpolitik: anti-goal positioning + bd-as-writer + Pareto-dominant predicate all align IS with where in-toto + SLSA + Sigstore are moving. After Phase A ships, file draft in-toto predicate type proposal for `eval-set/v1`, but ONLY after community-temperature reconnaissance."

**CISO:** "Highest-priority P0 is P0-RATIFY-2 (consistency model + outbox + retry). Without it, the cross-field invariant cannot be reliably enforced. Explicit refusal to compromise: defer `signing_mode='production'` capability to v0.4.0 rather than ship enforcement-light v0.3.0."

**VP DevRel:** "Single biggest contribution-friction reduction in the plan is T3 (collapse tri-link). Single most-tweetable artifact is P0-RATIFY-3 publication (regardless of outcome). Brand preservation (T4) is the developer-mental-model concern that engineering consensus underweights."

## 8. Cross-cutting themes

### Most-costly-to-recover-from tally
- T1 (SkillVersion shape): 4 seats (CTO + GC + CISO + CSO) — ONE-WAY DOOR via npm + Rekor
- P0-RATIFY-2 (consistency model): 2 seats (CISO + CSO) — cross-field invariant un-enforceable without it
- T4 (brand framing): 2 seats (CMO + VP DevRel) — third rebrand in one month signals instability

→ T1 + P0-RATIFY-2 deliberated slowest; received most word-count in this Decision Record.

### Adversarial integrity check
- CMO carried lone minority on T4 (3-seat business-axis minority vs 6-seat thinker majority). Minority bound rather than dismissed.
- CISO carried strong-dissent on P0-RATIFY-2 (refused compromise with CFO scoping). Hard line preserved.
- Karpathy + Gregg carried minority on T2 (2 of 14 voices for quarterly trigger). Falsifiable trigger metric folded in as re-opening condition.

No consensus theater detected. Three real tensions surfaced + resolved with binding constraints preserved.

### How the 4 synthesis lenses landed
- **Arena (5 surfaces):** T3 collapse to bd-as-writer + T4 brand preservation jointly preserve the existing claude-code-plugins → npm-distribution surface
- **Both-sides eval (client + server):** P0-RATIFY-1 + P0-RATIFY-2 + P0-RATIFY-6 jointly establish server-side eval-set governance + client-side `RefinerStrategy` swap
- **Transformation pipeline:** SkillVersion entity (T1 DISCRIMINATOR) + EvalSet versioning (P0-RATIFY-6) + RefinerStrategy interface (P0-RATIFY-5) form one composable pipeline (skill → version → strategy → score → predicate)
- **Composable partial attestation:** P0-RATIFY-2's `pending_production` state + P0-RATIFY-4's contributor-acknowledgment + T3's bd-as-writer all honor "silence ≠ failure"

## 9. Implementation directives

| # | Directive | Owner | Target |
|---|---|---|---|
| 1 | Author plan 027 v5 with all amendments above | acting CTO (Claude) | Next session, after this DR is filed |
| 2 | Amend Blueprint A § 3 to add Phase D anti-goal language (T2) | acting CTO | Same PR as plan v5 |
| 3 | Author or fold into existing bead: SkillVersion entity schema with `version_kind` + `parent_version_id` + `source_snapshot_hash` (T1) | RC-IEC + IEC-N1 | Phase C blocker; bd update |
| 4 | Author or fold into existing bead: `RefinerStrategy` interface + NaiveInContext + SkillOptStyle reference impls (P0-RATIFY-5) | new bead under RC-IAJ | Phase A blocker |
| 5 | Author bead: Phase A.0 null-hypothesis baseline (P0-RATIFY-3) | new bead under RC-IAJ | Pre-Phase-A; gates Phase A |
| 6 | Author bead: `bd-sync` extension as cross-ref GENERATOR (T3) | new bead under RC-IEL or TL-EPIC | Replaces validate-trilink Checks 2+3 |
| 7 | Author bead: `bd-claim-precheck.sh` enforcement script (P0-RATIFY-4) | new bead under RC-IEL | Honors hard gate per § 13 Step 7 |
| 8 | Author bead: Outbox + reconciler for sigstore Rekor unavailability (P0-RATIFY-2) | new bead under RC-IAH | Phase C blocker |
| 9 | Update STATUS.md → RATIFIED-WITH-DELTAS | acting CTO | Immediately after this DR is filed |
| 10 | Hard gate per § 13 Step 7 remains ACTIVE — no `bd claim` until plan v5 + new beads are filed | enforcement | Until plan v5 ships |

## 10. Reusable pattern reference

This session used the `exec-decision-council` skill v1.0.0 at `~/.claude/skills/exec-decision-council/SKILL.md`. Session artifacts (JSONL + per-seat positions + this Decision Record) at `~/.claude/skills/exec-decision-council/sessions/2026-05-27-skill-refiner-plan-ratification/`. Per-seat positions verbatim are in that directory's `inputs/seat-*.md` files (not duplicated here for brevity; this DR cites verbatim quotes inline).

## 11. Acting head of board declaration

I, Claude (acting CTO, designated by Jeremy Longshore via CTO-mode delegation in this session), having read all 7 ISEDC seat positions + 13 thinker-canon arbitrations + the Plan Audit synthesis, hereby ratify the 10 decisions above as binding on plan 027 v5 + downstream remediation work.

Minority dissents are preserved verbatim in this Decision Record. Binding minority constraints (the strongest version of each minority position) are folded into the decisions as named bindings.

Plan Audit STATUS file (`intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/STATUS.md`) is updated to `RATIFIED-WITH-DELTAS` immediately following this DR's filing. STATUS will move to `RATIFIED` after plan 027 v5 lands with all amendments.

The hard gate per plan § 13 Step 7 (no `bd claim` until ratification) is PARTIALLY LIFTED — `bd claim` is permitted against the new beads created by this Decision Record's implementation directives (items 3-8), but remains in effect for any prior-existing Skill Refiner bead until plan v5 is filed.

Filed: 2026-05-27.

— Jeremy Longshore
intentsolutions.io
