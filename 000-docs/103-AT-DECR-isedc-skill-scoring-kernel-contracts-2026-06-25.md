# ISEDC Decision Record — Skill-Scoring Kernel Contracts (D1–D5 + C3)

**Doc:** 103-AT-DECR · **Date:** 2026-06-25 · **Class:** 2 (cross-consumer architectural; one-way doors on signed surfaces)
**Council:** ISEDC 7-seat adversarial (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel)
**Acting head:** CTO, by delegated authority
**Epic:** intent-eval-lab#206 · **Build-ready spec:** `102-AT-SPEC-skill-scoring-gap-fill-build-ready-design-2026-06-25.md` (gap-validation + per-item adversarial review)
**Source research:** `100-RR-LAND-…-2026-06-24.md`
**Precedent DRs cited:** DR-085 (kernel one-way-door correction, tenant deferral-G), DR-082 + DR-086 (`skill-refiner-pass/v1` net-new predicate), DR-064 (Evidence-Bundle predicate-compatibility policy), DR-028 (kernel-additive discipline, bd-canonical-writer)

---

## 0. What was adjudicated

Six Class-2 decisions on the skill-scoring gap-fill — each an amendment to a signed or signing-bound kernel instrument:

| #      | Decision                                                                                                                                                                                                                               |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **D1** | Expand the canonical kernel entity set: add `usage_events` (append-only product-metering ledger, distinct from `CostRecord`) + `human_reviews` (open-ended human-trust signal). ONE-WAY DOOR — signed consumers pin the canonical set. |
| **D2** | `tenant_id` on the new entities = optional-not-nullable, following DR-085 D5 / deferral-G.                                                                                                                                             |
| **D3** | New predicate URI(s) for adoption / human-trust evidence bundles (immutable once signed to Rekor; `evals.intentsolutions.io` ONLY, never `labs.*`).                                                                                    |
| **D4** | `RolloutDecision` enum change if the adoption signal feeds rollout decisions.                                                                                                                                                          |
| **D5** | Adoption-weighting mechanism = deterministic time-decay with thresholds; Thompson-sampling bandit REJECTED for the multi-tenant/CI surface.                                                                                            |
| **C3** | (Reaffirm) No rolled aggregate score across heterogeneous dimensions; per-dimension only.                                                                                                                                              |

**Vote tally across the seven seats:**

| #   | CTO      | GC       | CMO      | CFO        | CSO      | CISO     | DevRel   | Ratified verdict                                              |
| --- | -------- | -------- | -------- | ---------- | -------- | -------- | -------- | ------------------------------------------------------------- |
| D1  | nod-cond | nod-cond | nod-cond | **refuse** | nod-cond | nod-cond | nod-cond | **GO with binding conditions**                                |
| D2  | nod      | nod      | nod      | nod        | nod      | nod      | nod      | **GO** (unanimous)                                            |
| D3  | nod-cond | nod-cond | nod-cond | **refuse** | nod-cond | nod-cond | nod-cond | **GO with binding conditions**                                |
| D4  | refuse   | refuse   | refuse   | refuse     | refuse   | refuse   | refuse   | **NO-GO** (unanimous refuse of the change; additive field GO) |
| D5  | nod-cond | nod      | nod      | nod-cond   | nod      | nod      | nod      | **GO with binding conditions**                                |
| C3  | nod      | nod      | nod      | nod        | nod      | nod      | nod      | **REAFFIRMED** (unanimous)                                    |

CFO is the lone refuse on D1 and D3 (premature-cost grounds, not correctness). His minority constraints are bound into the majority record below, per adversarial-integrity protocol.

---

## D1 — Expand canonical kernel entity set: add `usage_events` + `human_reviews`

### Verdict: **GO — with binding conditions**

Six seats nod the shape (additive append-only ledgers, new-row-not-mutation, single terminal `recorded` state); the gap is empirically real and verified (entity files carry no usage/human-review entity, no adoption field on `SkillVersion`). CFO refuses on premature-cost grounds — his constraints are preserved and bound. This is the slate's true one-way door: once a production-Rekor row references the expanded canonical set, removal is impossible without a major kernel break. The fix window — now, before the tag — is the free pass through the door, and the council spends it on the invariants.

### Binding conditions (all mandatory before the entities ship in a kernel minor; first production signature is the freeze)

**B1.1 — Two separate additive minors, two triplets.** The entities land as SEPARATE kernel minors, each its own triplet (JSON Schema + Zod + Pydantic + state machine), never one combined PR. They have different reproducibility properties: `usage_events` is replayable from counts; `human_reviews` is non-reproducible. New files only; ZERO edits to the existing entity files; append-one-line to the index. (CTO B(b), GC B(b).) _Minority carve-out (CTO standing dissent): if bandwidth forces a single combined PR over this objection, `human_reviews` MUST retain its own parallel statement schema and permanent-staging clause — its non-reproducibility cannot be laundered by co-shipping with the replayable `usage_events`._

**B1.2 — Anti-gaming cross-field invariants are load-bearing, machine-enforced, NOT prose.** (CTO B(c), CISO (1)+(2), DevRel BINDING-1.)

- `usage_events`: every metered (non-`api_call`) row binds non-nullable `source_entity_type`/`source_entity_id` PLUS a verified marker the runtime sets ONLY after the source session clears its quality gate — enforced as Zod `.superRefine` / Pydantic `model_validator` / JSON-Schema `if-then`. **The spec's "ZERO hand-validators needed" claim is DELETED.**
- `human_reviews`: requires `session_trace_id` non-null OR `judge_decision_id` non-null (pin to something verified); service-account-authored rows are excluded from human-signal counts or tagged distinctly.

**B1.3 — Parallel statement schema for `human_reviews`.** It ships a parallel additive `HumanReviewStatementSchema` binding only `subject[0].digest.sha256 === input_hash` (no `gate_id` invariant). It does NOT ride the `GateResultV1`-pinned `EvidenceStatementSchema` (`.strict()` + `z.literal(GATE_RESULT_V1_URI)`). `usage_events` rides INSIDE the `extensions` field of an EvidenceStatement and does NOT become one — a metering row masquerading as a gate-result statement is lineage-laundering and is refused. (CTO B(d), CISO (4), CSO.)

**B1.4 — `meter` enum closed-vs-open is locked BEFORE first signature.** A post-signature `meter` rename is a `/v2` burn on a never-signed shape. The metering owner locks closed-vs-open before any production-Rekor row references `usage_events`. Closed pricing enum is recommended (safest for billing). Drop `dashboard_render` from the `meter`/`source_entity_type` enums — it is a predicate body, not a lifecycle entity. (CSO B(a), spec §5 risk 1.)

**B1.5 — The amendment record is coherent in the SAME PR.** The `index.ts` entity-count header, Blueprint B's entity-count prose, the canonical glossary, and the umbrella CLAUDE.md "14 entities" line are ALL corrected in the same diff that exports the new entities, WITH a recorded supersession note. The kernel CHANGELOG carries the explicit "one-way door: signed consumers now depend on the expanded canonical set" notice and a per-entity entry. **No entity exports until the count assertions are corrected in the same diff.** (GC B, CMO dissent, CFO note.)

**B1.6 — Honest non-fabricating emit path ships in the entity PR.** A lone developer who ran a skill once must be able to record a valid `usage_event` + `human_review` WITHOUT hand-authoring a `tenant_id`, a synthetic gated session, or a predicate envelope. A golden-path `j-rig ingest-skill` / `review` example ships in the same PR (not a follow-on). The runtime sets the verified marker; the dev never types it. (DevRel BINDING-1 — a one-way canonical lock-in whose only honest emit path is forge-a-fake-parent is disqualified.)

### Resolve the entity-count framing

The spec's "14→16" framing is contested. CMO and CTO note the re-export surface already carries more than the headline count (e.g. `EvidenceBundlePayload` / `SkillVersion` via DR-028). **Ruling:** the council does NOT ratify a specific integer. The one-way door is "what gets a signed schema + state machine + predicate + index re-export," not a headcount. B1.5 binds: whatever the verified live count is, every canonical record asserts the SAME corrected number in the landing PR. A self-contradicting count across canonical records is itself a defective instrument and is refused.

### Preserved minority dissent — CFO (refuse), verbatim-sharp

> "This is the single most expensive decision on the table and it is being asked at the wrong altitude. The test is not 'is the gap real' (it is) but 'does an UNBUILT consumer create an IMMUTABLE liability NOW.' It does not. The entire downstream — j-rig adoption signal, CLI intake verbs, dashboard surface — does not exist. We would be minting two permanent canonical entities, baking them into a signed set consumers depend on forever, to feed code we have not written. The kernel-additive path makes this FEEL cheap; it is not. A canonical entity is a forever-maintenance, forever-migration, forever-Pydantic-codegen obligation across the whole ecosystem."

**CFO's bound alternative (does not block the GO, but is recorded as the dissent's constructive form):** build `slice_utility` (Item 3, pure refiner-core, zero kernel risk) and the CLI intake verbs writing to LOCAL `@j-rig/db` SQLite fact tables FIRST, with NO kernel entity; let usage/review rows accumulate as repo-local SQLite for one real soak window; promote to canonical entity ONLY when a built, in-use consumer demonstrably needs the cross-repo signed contract.
**CMO bound dissent (accepts entity, refuses name):** `usage_events` reads as a billing table wearing a kernel badge — "the moment a reader sees it in our canonical EVAL contract, the story flips from 'we measure whether skills earn their keep' to 'we built telemetry to bill you.'" If the council ratifies the name as-drawn, the rename to a signal-named entity is a forward debt that MUST be paid before the predicate signs to production (a one-way door named for the metering substrate cannot be renamed once a signed consumer depends on it).

**Acting-head ruling on the dissents:** GO stands. CFO's premature-cost objection is real but is answered by the freeze discipline (B1.4 + first-signature freeze) rather than by deferral — the council does not pay the cost twice (build-local-then-rebuild-canonical) when the additive-then-freeze path lets the canonical shape land now and stay malleable until the first production signature. CMO's naming concern is escalated to a binding open item: **the metering owner and CMO jointly settle the entity name before B1.4's enum lock**; if the name carries billing semantics, CMO's rename-before-production-sign debt (above) is binding. None of this blocks bottom-up build start, because no production signature occurs before the entities, invariants, and name are settled.

---

## D2 — `tenant_id` optional-not-nullable on the new entities

### Verdict: **GO (unanimous, zero conditions beyond citing the precedent)**

All seven seats nod. This is the cleanest decision on the docket: it makes the record CONSISTENT rather than divergent. Verified — `EvalSpec` / `EvalRun` / `SkillSnapshot` / `SkillVersion` all carry `readonly tenant_id?: Uuidv7` (optional, omitted from `required`, tested in `deferral-specs.test.ts`). The spec's original Item-1 draft claim that "no other entity carries a tenant axis" is factually wrong and is STRUCK; the four existing fields ARE the precedent this follows. A required-tenant divergence would have been the trap — it ossifies a multi-tenancy assumption into the signed surface before the tenancy model is settled, and is a silent amendment of a ratified deferral.

### Binding conditions

**B2.1 — Byte-identical to the precedent.** `readonly tenant_id?: Uuidv7`, omitted from `required`, with a DocComment citing **DR-085 D5 / deferral-G (bd_000-projects-k0fj)** by ID. Add the new entities to `deferral-specs.test.ts` so the reservation is a TESTED invariant, not prose. (CTO, GC, CSO.)

**B2.2 — Absent tenant is a first-class state end-to-end, never a pooled fallback.** A present `tenant_id` is an attested tenant claim; an absent one is single-tenant/global and MUST NOT fall into a shared multi-tenant aggregate. The D4/D5 rollup computes per-tenant first and EXCLUDES unkeyed rows from cross-tenant aggregates rather than averaging them in as noise — otherwise optional-tenant becomes a covert cross-tenant forgery/laundering vector. A fixture must round-trip a tenant-less `usage_event` + `human_review` through emit → verify → render → rollup with no warning. (CISO B, DevRel BINDING-2.)

**B2.3 — Any future mandatory-tenant need is its own DR.** If metering genuinely requires a mandatory tenant for billing correctness, that is a documented divergence requiring its own ISEDC nod — never a unilateral required-field ship. On the CFO local-table alternative, the tenant/`repo_slug` column lands in the first `CREATE TABLE` (the only place retrofit cost is bounded). (GC, CFO, CSO, CISO.)

### Dissent

None. Unanimous nod.

---

## D3 — New predicate URI(s) for adoption / human-trust evidence bundles

### Verdict: **GO — with binding conditions**

Six seats nod minting the URIs as the correct mechanism (precedent: `skill-refiner-pass/v1`, net-new, DR-082/DR-086). CFO refuses on premature-signing grounds — bound below. A predicate URI signed to Rekor is the most irreversible artifact the platform mints: the transparency log is append-only, so a wrong host, a wrong anchor, or an impossible promotion assumption becomes a permanent, publicly-visible scar the instant it is signed. The council conditions hard and freezes the shape before the first signature.

### Binding conditions

**B3.1 — Host is `evals.intentsolutions.io` ONLY, never `labs.*`, with DNSSEC + CAA live BEFORE first signature.** No-override CISO binding (2026-05-10) + umbrella CLAUDE.md §5 operational rule + iah-E06 pre-flight precedent. Replicate the existing `not.toContain('labs.intentsolutions.io')` test pattern for each new URI. `labs.*` may host methodology prose but NEVER a predicate identifier, OTel attribute namespace, or attestation predicate. (Every seat; CSO + CISO hardest.)

**B3.2 — `human-review/v1` is `sigstore_staging` PERMANENTLY, and that permanence is BOUND IN THIS DR — not a hand-edited constant.** A human's open-ended TEXT assessment is NON-REPRODUCIBLE and can never meet `rekor_production`'s reproduce-the-hash bar (`SigningMode` is the closed 3-enum `sigstore_staging | rekor_production | unsigned_experimental`; production carries a reproduce-the-hash test). Staging is permanent BY DESIGN, not a TODO. A future agent MUST NOT be able to silently flip `signing_mode` to production. (CTO (2), GC (3), CSO B(b), CISO (2), CMO, DevRel BINDING-3.) **DevRel binding overlay:** the permanent-staging status is developer-facing brand surface, not a CISO footnote — the authorizing text states staging-is-permanent-by-design AND names a DIFFERENT real trust criterion for `human-review/v1` (verified reviewer identity + pinned session), so an OSS adopter does not read "unsigned == half-finished == abandoned." The doc-072 boundary (`j-rig review` curated thumb is NOT this signed predicate and never a trust root) is loud in dev-facing docs.

**B3.3 — Anchor against the REAL constants.** The edit target is the `PREDICATE_URIS` const in `src/predicates/gate-result-v1.ts` (verified), NOT `index.ts` as the source design stated. `JudgeDecision`'s real predicate is `eval-verdict/v1`, NOT the implied `judge-decision/v1` — re-anchor the "human agrees/overrides the machine verdict" workflow and the `judge_decision_id` FK against the real constant. A predicate record citing a non-existent sibling URI is a defective instrument before it is ever signed. (CTO (3), GC (2), CSO, CISO (3).)

**B3.4 — Each new predicate ships its own subject-digest invariant + a one-line threat note + a CHANGELOG entry.** The `subject[0].digest.sha256 === input_hash` pin IS the forgery cost; a predicate without it has forgery cost zero. Every new signed predicate is new attack surface and gets a one-line threat note (who can forge a passing row, what stops them). Each URI gets its own kernel-authoring CHANGELOG entry — the changelog-observance gate depends on it. (CTO (4), CISO (3)+(4).)

**B3.5 — No URI registered before its accept-rule is machine-enforced; freeze precedes any external mention.** Minting a URI before its accept-rule is enforced is a forgery-cost-zero predicate. Community-temperature precedes any blog/gist/OTel/external reference to these URIs; freeze the shape, then sign, then speak. (GC, CSO overall.)

### Preserved minority dissent — CFO (refuse), verbatim-sharp

> "A signed predicate URI is the most immutable artifact we produce — once a row is signed to the production Rekor log it is unbounded, permanent liability. Signing fields are INERT until the trust root exists; do not gold-plate them early. There is no consumer signing adoption/human-trust bundles to production Rekor today, and the spec itself concedes `human-review/v1` can NEVER meet `rekor_production`'s bar — so the cheapest version of this decision is to NOT sign yet. The URI namespace stays reserved (`evals` only; `labs.*` forbidden); defer registration to the same future council cycle that promotes the canonical entity, gated on a built, verified emitter."

**Acting-head ruling:** GO stands. CFO's refusal collapses to a sequencing rule that the build order already honors — D3's URIs are registered but NOT signed to production until a built, verified emitter exists, and `human-review/v1` is permanently staging by B3.2. Registration-without-production-signature carries near-zero irreversible cost (it is reservable; the freeze is the first production signature, per CSO). CFO's "name a built, in-use consumer at the moment of any production signature; no speculative production-minting" is bound as a non-waivable gate on the first signature, satisfying the dissent without deferring the contract.

---

## D4 — `RolloutDecision` enum change for the adoption signal

### Verdict: **NO-GO on the enum change. GO on the additive `LaunchReport.adoptionVerdict?` field instead.**

**Unanimous — all seven seats refuse the enum mutation.** This is the one place on the slate where a Class-2 additive nod was asked to silently mutate a closed, consumer-pinned union — the PR #57 pattern. `RolloutDecision` is exhaustively switched by signed/pinned consumers; adding a member (`deprecate_review`) breaks exhaustiveness across `decideRollout`, `rollout-gate`, and every external `@j-rig/core` consumer at once — a breaking ripple disguised as a one-line edit. Worse from the integrity seat: adoption is the LEAST-trustworthy input (forgeable metering, D1) and `RolloutDecision` is the MOST trust-bearing output; wiring a forgeable signal into a fail-closed gate's own enum inverts defense-in-depth. The verified enum (`'ship' | 'warn' | 'block' | 'obsolete_review'`) is j-rig-LOCAL (`@j-rig/core` `.d.ts`), not a kernel `@intentsolutions/core` signed schema, AND already carries `obsolete_review`, which covers the "model caught up" case — weakening the case for ANY enum edit further.

### Binding conditions

**B4.1 — `RolloutDecision` union is NOT mutated in this work.** No member added or removed. Exhaustiveness stays intact. (Every seat.)

**B4.2 — Adoption nuance ships as an additive, opt-in `LaunchReport.adoptionVerdict?: AdoptionVerdict` field.** Consumers opt in for the 4-quadrant nuance; everyone else's pinned exhaustive switch is untouched. (Every seat; this is the spec's Item-4 fix, ratified.)

**B4.3 — Adoption is advisory-and-deprecate-only, NEVER promotes; the deterministic `accept()` gates stay the shipping authority.** Adoption can never override the deterministic gate. (CTO, CISO, DevRel, CFO.)

**B4.4 — Any future `RolloutDecision` extension is a SEPARATE Class-2 ISEDC DR** with an exhaustiveness-impact analysis enumerating every switch over the union (`decideRollout` + `rollout-gate` + external `@j-rig/core` consumers), a major version bump of `@j-rig/core`, a documented codemod, and a forgery-cost analysis of the adoption signal feeding it — never a rider on a gap-fill. (CTO standing dissent, GC, CSO, CISO, DevRel.)

### Note on framing (CTO + CISO correction, bound)

The spec's "ripples across signed consumers" is real but mis-located: this is `@j-rig/core`'s `.d.ts` surface, not the kernel's signed schema. The refusal stands on consumer-exhaustiveness + premature-semantics grounds (adoption thresholds are still uncalibrated, D5), NOT on a kernel-signature claim. Recording the correct reason matters so a future reader does not over- or under-scope a later enum DR.

### Dissent

None against the refuse. The unanimity is itself the record: the additive-opt-in path gives consumers the full nuance with zero exhaustiveness breakage.

---

## D5 — Deterministic time-decay adoption weighting; bandit REJECTED

### Verdict: **GO — with binding conditions. Thompson-sampling bandit REJECTED unconditionally for this surface.**

Seven seats reject the bandit; CTO and CFO attach conditions on the decay mechanism. The bandit is a category error here, not a phase-2 option. Thompson sampling is non-deterministic by construction (PRNG draws from posteriors) — the same evidence produces different gate outcomes on replay, which breaks the `gate-result/v1` audit-reproducibility contract, breaks `accept()`'s replayability, and breaks the launch report as a stable signable artifact. You cannot sign a non-deterministic verdict. Worse, a bandit's exploration term would BY CONSTRUCTION occasionally route a fail-closed CI gate to the INFERIOR skill version to reduce posterior variance — intentionally shipping a worse skill sometimes, indefensible in a fail-closed gate. Deterministic time-decay-with-thresholds is closed-form, replayable, signable, and composes with the existing `accept.ts` z-test and `decideRollout` machinery.

### Binding conditions

**B5.1 — Inject `now`; the host artifact must be replayable (precondition, non-waivable).** `buildLaunchReport` currently calls `new Date().toISOString()` directly (verified) — inject `now`, mirroring `kernel-version.ts`. Rejecting the bandit for non-determinism while the artifact it lands in reads the wall clock is incoherent. Bound by CTO as non-waivable regardless of how the threshold debate resolves. (CTO (1), GC, CSO, CISO, DevRel.)

**B5.2 — Thresholds are calibrated/derived, NOT bare literals.** A bare `halfLifeDays`/`minVolume`/floor is the "fake constant" the epic's own Rule 1 forbids — a load-bearing literal in a signed verdict that nothing justifies. Require the verdict to clear a significance margin given decayed evidence weight (mirror `accept.ts`), OR ship per-ecosystem-overridable floors WITH a documented calibration procedure + a back-test step before they become load-bearing. (CTO (2), CFO, CSO, CISO, CMO.)

**B5.3 — Per-tenant decayed rates computed FIRST, then bounded-weight aggregate.** Cap each tenant's contribution or quorum per-tenant verdicts; a tenant below its own `minVolume` is excluded, never averaged in as noise. Segregate `source:"ci"` (gate-anchored, trustworthy) from `source:"plugin"` (unverified); weight unverified at/near zero on the deprecate axis. (CTO (3), CISO, spec Item-4 fixes.)

**B5.4 — The verdict is EXPLAINABLE to the affected maintainer.** The launch report shows decayed evidence weight, per-tenant breakdown, and which threshold was cleared, so a maintainer whose skill drew `deprecate_review`/`obsolete_review` can see exactly why and contest it. A black-box deterministic score is only marginally better DX than a black-box bandit. (DevRel BINDING-5.)

**B5.5 — Bandit is permitted ONLY in Refiner strategy-selection, off any signed surface.** A contextual bandit choosing which `RefinerStrategy` to try next inside `@intentsolutions/refiner` under a fixed token budget is a genuine exploration problem and is admissible there — physically barred from any surface that produces a signable verdict. (All seats; surgical separation.)

### Preserved minority condition — CFO (nod-with-condition)

> "Deterministic-decay is only 'cheap' if we don't gold-plate the thresholds prematurely. Do NOT build the decay/threshold weighting as a load-bearing rollout input until the local fact tables have accumulated a real soak window of event data to back-test against. Ship the mechanism with conservative, explicitly-provisional, per-ecosystem-overridable defaults and a documented calibration procedure — never bare literals presented as tuned."

**Acting-head ruling:** Bound. B5.2 already requires calibration-or-overridable-floors-with-back-test; CFO's "explicitly-provisional until a soak window back-tests them" is the operational form of that condition and is binding — thresholds are marked provisional and are not load-bearing on a production verdict until back-tested.

---

## C3 — No rolled aggregate score across heterogeneous dimensions (REAFFIRM)

### Verdict: **REAFFIRMED (unanimous, structural enforcement bound)**

All seven seats reaffirm. A rolled headline score across heterogeneous dimensions is the ultimate ossification trap and a forgery-cost-zero assertion: once a "usefulness %" is signed into a bundle, every downstream consumer treats it as canonical and the heterogeneous dimensions it crushed together can never be decomposed back out — anyone can pick the weights that produce the "pass" they want and the signed row carries no evidence of the weighting. It is also developer-hostile: a high-adoption/low-quality skill and a low-adoption/high-quality skill read identically, destroying the signal a maintainer could act on.

### Binding conditions

**B6.1 — Enforcement is STRUCTURAL, not regex.** The `c3-scan.ts` detector only catches the literal `pass` token — it is NOT the defense. The defense is structural absence: `SkillCard` has no `rolledScore` field by construction; no renderer takes more than one dimension's rows (no `renderRolledScore`); `usage_events` forbids `SUM` across distinct `(meter,unit)`; the adoption 2×2 is AND-combined never averaged; `slice_utility` is a per-block vector with no skill-level aggregate. Each surface is backed by a consuming-surface test asserting no cross-dimension scalar is emitted. (Every seat.)

**B6.2 — The C3 guard lives IN j-rig, not borrowed from the dashboard.** Port `c3-scan` into a shared `pnpm run check` lane, or make `report --usage/--reviews` structurally incapable of a cross-dimension aggregate — j-rig emits rows the dashboard never sees, and enforcement travels with the code it governs. (CTO, CFO, CSO, CISO, DevRel.)

**B6.3 — `human_reviews.score_text` is normatively NON-COMPARABLE free text** consumers MUST NOT parse into a scalar or aggregate, OR a separate structured `numeric_score` channel is added so numbers stop hiding in a string. The three orthogonal human-review channels stay orthogonal. (Every seat.)

**B6.4 — Renderers do NO arithmetic.** Any adoption rate/% is a field the kernel entity computes and emits INSIDE the verified bundle; a renderer-side division (`verifiedUsageCount / anything`) is a hand-derived unverified value and is C3 violated at the last mile. Rendering a raw verified count is fine; dividing it is not. No-data and no-trust states render LOUD (`badge--no-data` == `badge--fail` weight). (CTO, CSO, CISO, DevRel, CMO.)

### Dissent

None. CMO's only push is additive: C3 should be elevated to a NAMED, quotable public principle (first-mover positioning against single-score leaderboards) — recorded as a marketing follow-on, not a constraint on the build. DevRel + GC + CFO + CSO pre-register a STRUCTURAL refusal of any future "single skill score %" for marketing/case-study legibility: it must be made structurally impossible to add later (B6.1), not merely discouraged.

---

## Decision summary

| #      | Verdict                                                                                                                                      |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **D1** | GO with binding conditions B1.1–B1.6 (one-way door; first production signature is the freeze; CFO refuse + CMO naming dissent preserved)     |
| **D2** | GO (unanimous); conditions B2.1–B2.3                                                                                                         |
| **D3** | GO with binding conditions B3.1–B3.5 (CFO refuse preserved as a no-production-sign-before-built-emitter gate)                                |
| **D4** | NO-GO on the enum change (unanimous refuse); GO on the additive `adoptionVerdict?` field; conditions B4.1–B4.4                               |
| **D5** | GO with binding conditions B5.1–B5.5; bandit REJECTED unconditionally for the signed surface (admissible only in Refiner strategy-selection) |
| **C3** | REAFFIRMED (unanimous); conditions B6.1–B6.4                                                                                                 |

---

## (1) The single nod — does the bottom-up build proceed

**YES.** The bottom-up build proceeds. One Class-2 ISEDC nod covers the slate, exactly as the spec's Gate-0 requested — the canonical-entity expansion, the tenant-axis precedent confirmation, the two new predicate URIs, and the launch-report artifact semantics. The two genuine refuses do NOT block the build: D4's enum mutation is replaced by an additive opt-in field that ships in the same work, and CFO's D1/D3 refuses collapse to a sequencing discipline (no production signature before a built, verified emitter) that the build order already honors.

Build in the ratified order: **(0) this nod lands + `bd-claim-precheck` STATUS gate satisfied for refiner-labeled beads → (1) `usage_events` + `human_reviews` kernel triplets, separate minors, all B1 invariants → (2) `cli_verbs` intake + CASS gate + tenant column in first `CREATE TABLE` → (3) `adoption_signal` decay/threshold weighting → (4) `slice_utility` (parallel, pure refiner-core) → (5) `dashboard_surface` last, fixture resolver first, production resolver only after (1) lands.** Close beads bottom-up via `bd-sync close`, one logical cluster per GH issue, adversarially verify every "close-now."

The skill-to-skill dependency graph (`bv` applied to the skill catalog) is filed as a follow-on bead under #206 — out of scope for this slate, not bolted in.

## (2) The binding constraints the build MUST honor

1. **First production-Rekor signature is the freeze, not this council nod.** Lock the `meter` enum closed-vs-open AND the entity name (D1 B1.4) before any `usage_events` row signs to production. Registration-without-production-signature is reversible; the signature is forever.
2. **`human-review/v1` is permanently `sigstore_staging`, bound in this DR** — never a hand-edited, silently-flippable constant. It carries a different real trust criterion (verified reviewer identity + pinned session) and that permanence is loud in dev-facing docs (D3 B3.2).
3. **Every new predicate URI is `evals.intentsolutions.io` only, never `labs.*`, with DNSSEC + CAA live before first signature** (D3 B3.1). Anchor against the REAL constants — `PREDICATE_URIS` in `gate-result-v1.ts`, `eval-verdict/v1` for JudgeDecision (D3 B3.3).
4. **`RolloutDecision` is NOT mutated** (D4 B4.1). Adoption rides an additive opt-in `LaunchReport.adoptionVerdict?` field; advisory-and-deprecate-only, never promotes; the deterministic `accept()` gate stays the shipping authority (D4 B4.3).
5. **Anti-gaming invariants are machine-enforced, not prose** — `usage_events` binds to a verified gated source via `.superRefine`/`model_validator`; `human_reviews` pins to a verified session and excludes service-account rows; the "zero hand-validators" claim is deleted (D1 B1.2). The CASS gate (≥0.30, persist-but-exclude) is load-bearing at the CLI.
6. **Determinism is non-waivable.** Inject `now` into `buildLaunchReport`; thresholds are calibrated/derived/provisional-until-back-tested, never bare literals; the bandit is barred from any signable surface (D5 B5.1–B5.2, B5.5).
7. **C3 is enforced structurally + per-surface test, not by the `c3-scan` regex; renderers do no arithmetic; the guard lives IN j-rig** (C3 B6.1–B6.4). No skill-level rolled "usefulness %" is representable anywhere.
8. **`tenant_id` is optional-not-nullable byte-identical to DR-085 D5, tested in `deferral-specs.test.ts`; absent tenant is a first-class state, never pooled into a cross-tenant aggregate** (D2 B2.1–B2.2).
9. **The amendment record is coherent in the landing PR** — every canonical entity-count assertion (`index.ts` header, Blueprint B prose, glossary, CLAUDE.md) corrected in the same diff, with a recorded supersession note and a CHANGELOG one-way-door notice (D1 B1.5).
10. **An honest, non-fabricating emit path ships in the entity PR** — a lone developer records a valid usage/review row without forging a tenant, session, or predicate envelope (D1 B1.6). DevRel's D1 nod reverts to REFUSE if forge-a-fake-parent is the only honest path.

---

## Filing + provenance

- **Acting head:** CTO, by delegated authority. Verbatim seat positions preserved per adversarial-integrity protocol; the lone-refuse (CFO, D1+D3) and the naming dissent (CMO, D1) and the standing dissents (CTO combined-PR/enum, CSO/CISO D4, DevRel D3-brand) are bound into the majority record, not suppressed.
- **One-way-door items (immutable once signed):** D1 (canonical set), D3 (predicate URIs). Treat the first production-Rekor signature as the freeze; everything in this DR is a condition on keeping the malleable phase malleable until then.
- **Reversible items:** D2 (precedent-following), D4-additive-field, D5 (pure refiner-core), C3 (structural reaffirm).
- **Cross-refs:** epic intent-eval-lab#206; precedents DR-085, DR-082/DR-086, DR-064, DR-028; build-ready spec `102-AT-SPEC-skill-scoring-gap-fill-build-ready-design-2026-06-25.md`; source research `100-RR-LAND-…-2026-06-24.md`.

- Jeremy Longshore
  intentsolutions.io
