# Lamport Findings — Skill Refiner Plan 027 (snoopy-fluttering-comet v4.1)

**Seat:** Leslie Lamport (channeled)
**Primary axes:** GAPS, RISK
**Date:** 2026-05-27
**Plan version audited:** v4.1 (post-internal-review)

> _"If you're thinking without writing, you only think you're thinking."_ > _"A specification is not a description of what the system does, but a definition of what it means to be correct."_ > _"State machines are obvious, and properties are obvious. The bug is always in the assumption you didn't write down."_

The plan is rich in prose, ASCII diagrams, dependency tables, and ratification choreography. It is poor in _invariants stated precisely enough to falsify._ The central load-bearing nouns — "refined," "accepted," "SkillVersion," "append-only event log," "strict improvement" — are deployed as primitive terms across 50+ occurrences without ever being given a formal predicate definition. The plan will not type-check against itself, and downstream consumers of `skill-refiner-pass/v1` will have no formal anchor for what they are consuming. The three most embarrassing-if-overlooked findings are F-LL-01, F-LL-02, F-LL-03 below.

---

## F-LL-01 — "Refined" / "accept" used as primitive throughout; no formal predicate

**Severity:** P0 BLOCKER
**Axis:** GAPS

**Lamport position invoked:**

> _"A specification is not a description of WHAT but a definition of CORRECT. Every primitive term in a specification must either be a defined term in the specification language or be defined by the specification before it is used."_

**The defect.** The plan calls itself "Skill **Refiner**." It mints a predicate URI `skill-refiner-pass/v1`. It builds an `accept()` function as the "durable contribution per AC-7." And yet nowhere in the plan — nor in the canonical glossary (brief-pack doc 06, which I grepped for `refine|refined|SkillVersion`: zero matches) — is "refined" given a definition. The closest the plan gets is § 4 Phase A:

> _"Implement `apply()` + `accept()` — pure transformation + strict-improvement gate"_ (§ 4 Phase A build order, item 2)

and AC-7:

> _"The acceptance gate is the durable contribution; the refiner mechanism is swappable"_ (§ 3 AC-7).

But "strict improvement" is never given a predicate. The TypeScript fragment in § 4 Phase A declares `accept(scoreV1, scoreV2): boolean` as the whole signature; no contract follows. Multi-dimensional scores (AC-3) make "strict improvement" _ambiguous by construction_ — strict on which dimensions? All? Pareto-dominance? Lexicographic by ordered priority? A weighted sum (and if so, who owns the weights, and how does the weight choice avoid Goodhart per AC-3's own warning)? The plan asserts the gate exists; it does not state what the gate _means_. AC-3 says scores are "never collapsed to a scalar," which makes the `boolean` return type of `accept()` _type-unsound_ given the input domain.

**Why this is P0.** The predicate `skill-refiner-pass/v1` will be _signed into Rekor_ (Blueprint B § 7.2: "predicate URIs are effectively immutable once signed and pushed to a transparency log"). Whatever definition of "refined" the first signed row pins, the platform is bound to _forever_. Shipping a predicate whose semantic is "the function `accept()` returned true" — where `accept` is undefined — anchors un-falsifiable evidence in a permanent transparency log. This is the failure mode DR-010 Q3 was written to prevent: the URI grammar is locked but the body semantic is not.

**Citation from plan:** § 4 Phase A (lines 349-353, TypeScript fragment with `declare function accept(scoreV1: ScoreRecord, scoreV2: ScoreRecord): boolean;`); § 3 AC-3 (multi-dim, "never collapsed to a scalar"); § 3 AC-7 ("acceptance gate is the durable contribution").

**What the plan must add before any code is claimed.** A § 3.X (or new doc 028) section titled "The Acceptance Predicate" that:

1. Defines `Accept(s_old, s_new): Bool` as a _named predicate_ with type signature and prose definition.
2. States the precise rule (strict Pareto-dominance? lexicographic? weighted with explicit weights as part of `EvalSetHash`?). Picking one is a Class-1 architectural decision per Blueprint A § 2.3 routing — file an ISEDC session if it is non-obvious.
3. States the inverse — `Reject(s_old, s_new)` — and proves they partition the score-pair space (no ties, or ties resolved deterministically).
4. Pins the definition into the `skill-refiner-pass/v1` predicate body schema as a required `acceptance_rule_uri` field so consumers can verify _which_ rule produced the row.

---

## F-LL-02 — AC-2 "append-only event log" claimed as primitive; no consistency property stated

**Severity:** P0 BLOCKER
**Axis:** RISK

**Lamport position invoked:**

> _"State machines are obvious; properties are obvious; the bug is in the assumption you didn't write down. Especially temporal assumptions — what does 'eventually' mean, what does 'consistent' mean, who is the observer."_

**The defect.** AC-2 says:

> _"Append-only event log; never in-place SKILL.md mutation. Each accepted edit produces a content-addressed `SkillVersion` value; 'current best' is a separate mutable pointer."_ (§ 3 AC-2)

§ 4 Phase A operationalizes this:

> _"Append-only event log at `.j-rig/refiner/log.jsonl` (each line is a value-record)"_ > _"Single mutable pointer file: `.j-rig/refiner/pointers/<skill>/best` (just a hash)"_ > _"Content-addressed store at `.j-rig/refiner/store/<hash>"`_

This is a **three-component distributed-storage system** — log, store, pointer — running on a local filesystem and (per § 4.5 ecosystem fold) eventually emitting through `audit-harness emit-evidence` to _sigstore staging_ (Phase B), to _production Rekor_ (Phase C). And not one consistency property is stated.

Specifically the plan does not say:

1. **Is the log linearizable?** Two `accept()` calls from two concurrent Claude Code sessions on the same skill — what is the ordering rule? Filesystem `append(2)` is _not_ a total-order primitive across processes without an explicit lock.
2. **Is the `best` pointer atomic w.r.t. the log?** A reader of `best` followed by a read of `log.jsonl` may observe a hash in `best` that has not yet appeared as a record in `log.jsonl` (writer crashed between the two writes), or a record in `log.jsonl` that is not the current `best` (pointer advance is lazy). Neither failure mode is specified, neither is recoverable without a defined invariant.
3. **What is the relationship between the local append-only log and the eventually-signed Rekor entries?** Rekor is the _only_ truly append-only durable substrate in the stack (Blueprint B § 6 lifecycle: `signed → archived_to_rekor`, "permanent by design — one-way door"). The local log is a _staging area_ for Rekor. The plan calls both "append-only" as if they were equivalent. They are not. A local `.jsonl` file can be `rm`'d; a Rekor entry cannot. Conflating the two collapses a fundamental safety property.
4. **What does "accepted edit" mean across the boundary of a `git rebase`, `git filter-branch`, or `rm -rf .j-rig/`?** The plan asserts the log is append-only but lives inside the project filesystem with no protection from the user's own git operations. A SkillVersion that was "accepted" and signed to staging — and is then orphaned because the engineer rebased the branch out of existence — is now a Rekor row pointing to a SkillDocHash that no longer reconstructs. This is an _un-falsifiable_ attestation and violates Blueprint B § 4.4 "audit-grade deterministic, not approximately reproducible."

**Why this is P0.** Once any row hits Rekor (Phase C exit criterion), the inconsistency between the local log and the public log becomes permanent and visible to external auditors. CAP-style failure modes that look like edge cases pre-Phase-C become _attestation defects baked into a public transparency log_ post-Phase-C.

**Citation from plan:** § 3 AC-2; § 4 Phase A (lines 356-358); § 4 Phase C exit criteria; cross-ref Blueprint B § 4.4 + § 6 (one-way-door property).

**What the plan must add.** A § 4 Phase A "Consistency Model" subsection stating:

1. The total-order rule for `log.jsonl` (single-writer per skill? file lock? content-addressed ordering by accept timestamp + tiebreak?).
2. The atomicity guarantee for the (log-append, pointer-advance) pair (write-pointer-then-log? log-then-pointer? a transaction-marker record?).
3. The relationship to Rekor: which records are "candidates" (local only) vs "committed" (staging-signed) vs "anchored" (production-Rekor). These are state-machine states; they must be named.
4. The recovery rule for orphaned-by-git SkillVersions: at minimum a refusal-to-sign predicate (`emit-evidence` must verify the SkillDocHash is reachable from `HEAD` before signing). Filed as a precondition bead, not buried in a § 8 risk row.

---

## F-LL-03 — SkillVersion cross-field invariant named but not stated as proof obligation on consumers

**Severity:** P1 CRITICAL
**Axis:** GAPS

**Lamport position invoked:**

> _"State machines are obvious; properties are obvious; the bug is in the assumption you didn't write down."_
> Stating an invariant the producer maintains is not enough — the contract must say what the consumer is entitled to _rely on_, in what conditions the reliance holds, and what recourse exists when it fails.

**The defect.** § 4 Phase C names a cross-field invariant on the SkillVersion entity:

> _"Cross-field invariants per CISO binding (filed as `bd_000-projects-1is2`): `rekor_log_index` non-null iff `signing_mode='production'`"_ (§ 4 Phase C, line 451)

This is a one-sentence drive-by. It is named as a CISO binding but not specified as a TLA+/Z-style invariant: no quantifier, no scope, no consumer-side relying-party contract. As written, four things are unclear:

1. **Producer-side or consumer-side?** Is the kernel Zod validator the only enforcer (producer-side, "you cannot construct an invalid SkillVersion")? Or are consumers like `intent-rollout-gate` (M5 runtime, § 4 Phase C "intent-rollout-gate changes") entitled to _skip verification_ on the assumption the invariant holds? Or are consumers obligated to _re-verify_ the invariant on every row they read? The plan does not say. These are different threat models with different attack surfaces.
2. **What does "non-null" mean for an `int64`?** The schema (§ 4 Phase C schema fragment) declares `"rekor_log_index": "int64 | null"`. JSON-Schema lacks first-class int64; the kernel will encode this as `number` with a range constraint, and JS numbers above 2^53 are unsafe. A Rekor log index _can_ exceed 2^53 (Rekor production has been online since 2021 and the index is monotonic). The "non-null" half of the invariant has a silent precision bug; the plan does not state whether `rekor_log_index` is a JSON `number`, a JSON `string`-encoded int64, or a typed `bigint` (TypeScript only). This is exactly the class of "obvious property with un-written assumption" the Lamport canon flags.
3. **"iff" is bidirectional — does the plan mean it?** If `signing_mode='staging'` AND `rekor_log_index` is populated (e.g. with the staging Rekor's index from `rekor.sigstage.dev`), is that a valid SkillVersion or an invalid one? The current iff says invalid. But § 4 Phase B exit criteria asks for evidence "attached to the demo" pre-Phase-C, which strongly implies staging-signed bundles will populate _some_ index field. Either the invariant is wrong (should be `production-rekor-anchored ⇒ rekor_log_index non-null`, one-way implication) or Phase B is forbidden from populating `rekor_log_index` — neither is stated.
4. **What is the recourse on violation?** If a consumer reads a SkillVersion row where the invariant is violated, does the consumer (a) reject the row and emit `bundle.emission.refused` per Blueprint B § 6, (b) treat the row as unsigned and process it anyway, or (c) escalate to a human? The plan is silent. Since `skill-refiner-pass/v1` is bound to be signed into Rekor permanently (§ 4 Phase C exit criterion), the violation case is _itself a permanent record_ — a consumer needs a documented response or it will improvise one, and the improvisations will diverge across the 5 IEP repos.

**Why this is P1 (not P0).** Unlike F-LL-01 and F-LL-02, the producer side has at least a named bead (`bd_000-projects-1is2`) and a hook into the kernel Zod validator. But the consumer side is undefined, and `intent-rollout-gate` will start consuming these rows in Phase C — at which point the un-specified relying-party contract becomes an inter-repo runtime hazard.

**Citation from plan:** § 4 Phase C schema fragment (lines 432-445); § 4 Phase C "intent-rollout-gate changes" (line 458); cross-ref Blueprint B § 6 (`bundle.emission.refused` precedent).

**What the plan must add.** In doc 028 (the normative predicate spec), an explicit "Invariants" section that:

1. States each cross-field invariant in formal form: `∀ v ∈ SkillVersion: v.signing_mode = 'production' ⇔ v.rekor_log_index ≠ null` (or whatever the chosen direction actually is — see point 3).
2. States the producer obligation: kernel Zod validator rejects construction; `j-rig emit-refiner-pass` rejects emission.
3. States the consumer obligation: every consumer of a `skill-refiner-pass/v1` row MUST re-verify the invariant before relying on `rekor_log_index`. Rows that violate the invariant MUST be rejected with `bundle.emission.refused` per Blueprint B § 6 precedent.
4. Pins the `rekor_log_index` encoding (recommendation: JSON `string` of decimal int64) and adds a kernel test that round-trips an index > 2^53.

---

## F-LL-04 — Phase exit criteria are descriptive, not liveness/safety properties

**Severity:** P2 MAJOR
**Axis:** GAPS

**Lamport position invoked:**

> _"Temporal logic — what does 'Phase A ships' actually mean? Liveness is 'something good eventually happens'; safety is 'something bad never happens.' Confuse them and your spec is wrong."_

**The defect.** § 9 Verification lists eight aggregate exit criteria. Each is a _descriptive snapshot_ ("npm view returns 0.1.0+", "ISEDC Session 7 DR filed"), not a _temporal property_. The plan never distinguishes safety from liveness, never says what "Phase A has shipped" _means_ in the sense of an observable, persistent, falsifiable post-condition.

Concrete missing properties:

1. **Safety on the predicate URI namespace.** No `gate-result/v1` row ever appears under `labs.intentsolutions.io` (CISO binding from DR-004). The plan asserts this in § 13.5 of the umbrella CLAUDE.md but does not state it as a _Phase B exit safety property_ the build must verify. A `grep` over staged-but-not-yet-signed bundles before each release is the obvious check. Not specified.
2. **Liveness on the acceptance gate.** Every `EditProposal` is _eventually_ labeled `accepted` or `rejected` — never indefinitely pending. Without this, a stalled refiner run leaks resources and pollutes the rejected-edits buffer in undefined ways.
3. **Safety on the strict-improvement gate.** If a SkillVersion `v_new` was accepted relative to `v_old` under `EvalSet E1`, and `E1` is later updated to `E1'`, the prior acceptance decision is _historically valid against E1_ and remains so forever. This is the property that makes `skill-refiner-pass/v1` rows historically auditable rather than retroactively-invalidatable. Not stated.

**Why this is P2 (not P0/P1).** The plan can ship without these — they are debt, not blockers. But shipping without them means each future ISEDC session that touches the eval-set governance will re-discover that the historical-validity property was never written down, and will be re-litigated from scratch.

**Citation from plan:** § 9 Verification (eight criteria); § 3 AC-2; AC-6 eval-set bootstrap.

---

## F-LL-05 — SkillVersion entity lacks state-machine transition spec

**Severity:** P2 MAJOR
**Axis:** GAPS

**Lamport position invoked:**

> _"State machines are obvious."_ — they should be, but only after you've drawn them.

**The defect.** Blueprint B § 6 (lifecycle states) gives every existing entity a state machine: `EvidenceBundle: building → signing → signed → archived_to_rekor`; `RolloutGate: evaluated`. § 4 Phase C declares SkillVersion as "the 14th canonical entity" with full schema fields, and § 5.5 D5 includes an ER diagram — but no state machine.

What states does a SkillVersion occupy? Reading the plan implicitly:

- `proposed` (an `EditProposal` exists, `accept()` not yet called)
- `accepted` (passed the gate; lives in local log only)
- `signed_staging` (Phase B emit, sigstore staging)
- `signed_production` (Phase C emit, production Rekor)
- `shadow` / `canary` / `promoted` (§ 4 Phase F promotion ladder — but these are explicitly NOT-in-scope per § 11)
- `superseded_by` (the markdown report § 10 banding — `SUPERSEDED-BY-NNN`)

The plan uses each of these terms but never states the transition graph. Which transitions are legal? Can a SkillVersion go from `signed_staging` to `signed_production` (re-sign with stronger evidence)? Can it go _backward_ — `signed_staging` → `proposed` if the eval-set is invalidated? Per Blueprint B § 6 precedent, _transitions out of `signed` are forbidden_ (one-way door), but this rule is never restated for SkillVersion. A reader of the plan must reverse-engineer the state machine from prose scattered across § 3 AC-2, § 4 Phase A/B/C, § 4 Phase F, and § 6.5 D5.

**Citation from plan:** § 4 Phase C schema fragment; § 5.5 D5 (ER diagram, no states shown); § 4 Phase F (promotion ladder, deferred); cross-ref Blueprint B § 6.

**What the plan must add.** A state-machine diagram in doc 028 with explicit nodes + transition arrows, and the one-way-door rule restated: `transitions out of signed_* are forbidden; corrections produce a new SkillVersion that references the prior via parent_version_id`. This mirrors the EvidenceBundle pattern in Blueprint B § 6.

---

## F-LL-06 — OTel attribute namespace pinning is named in `9pi3` but plan does not state the falsifiable property

**Severity:** P2 MAJOR
**Axis:** GAPS

**Lamport position invoked:**

> _"If you're thinking without writing, you only think you're thinking."_

**The defect.** § 4.5 ecosystem-fold matrix names `9pi3` (OTel semconv pin, P0) as blocking Phase C kernel ship. § 8 risks names "agentskills.io spec changes between plan ratification and Phase A code" but not OTel attribute drift. Neither row states the _invariant_ a pinned semconv is supposed to maintain.

The unwritten assumption is: every OTel span emitted by `@j-rig/refiner` carries the same attribute keys (`agent.rollout.gate.*`, `agent.evidence_bundle.*` per the CLAUDE.md "OpenTelemetry RFC draft" entry) _across all Refiner versions that ship under skill-refiner-pass/v1_. If the attribute namespace drifts mid-Phase-C, all rows signed before the drift become un-correlatable to rows signed after — an audit failure mode that does not surface until someone queries the OTel store six months later.

The falsifiable property is: _for any two `skill-refiner-pass/v1` rows R1 and R2 signed under the same kernel major version, R1.otel_attribute_keys = R2.otel_attribute_keys_. This is a _cross-row invariant_ (Lamport: "the bug is in the assumption you didn't write down" — and cross-row invariants are the assumptions plans omit most often).

**Citation from plan:** § 4.5 ecosystem-fold matrix (`9pi3` row); § 8 risks table.

**What the plan must add.** A § 4.5 sub-row stating: "OTel attribute keys are pinned per kernel major version. Adding a key is non-breaking; removing or renaming a key requires a kernel major bump. The pinning is enforced by an `audit-harness` gate `otel-attribute-namespace-check` (file a bead under `RC-IAH`)."

---

## F-LL-07 — "Plan written by one author might miss things" risk is hand-waved by the panel ratification it is being judged by

**Severity:** P3 MINOR
**Axis:** RISK MITIGATION

**Lamport position invoked:**

> A specification that names its own auditor as the mitigation for its own gaps is a specification that has assumed away the very thing the auditor exists to check.

**The defect.** § 8 risks table:

> _"this plan is itself a risk — written by one author (Claude), might miss things | § 12 Plan Audit phase: 7-seat thinker-canon panel reviews plan BEFORE any code; § 13 Step 5 codifies this as mandatory before first `bd claim`"_

This is the plan citing the audit _I am writing right now_ as its own mitigation. The mitigation works if and only if the audit fires findings the plan does not already anticipate. If the audit is itself defective (e.g., the panel agrees with the author's blind spots), the mitigation circular-reasons. The plan should state an _external_ falsifier in addition to the internal one — e.g., "a Phase B demo on `/validate-skillmd` that produces a score regression on a real eval set is a stop-the-line signal that the design is wrong, regardless of what the Plan Audit said."

**Citation from plan:** § 8 risks table (last-but-one row).

**What the plan must add.** A § 10 stopping criterion: "If the Phase B end-to-end demo produces a score regression OR fails to demonstrate strict improvement under the rule from F-LL-01, the design is falsified empirically — re-draft Phases A-C regardless of Plan Audit status."

---

## Summary

Seven findings filed against plan 027 v4.1. Three are P0 BLOCKER (F-LL-01, F-LL-02) or P1 CRITICAL (F-LL-03) and represent the canon-level failures: a primitive term used 50+ times without a formal predicate definition, an append-only event log claimed without a consistency property, and a cross-field invariant named without a relying-party contract. The remaining four (F-LL-04 through F-LL-07) are structural debt that the plan can ship over but will pay interest on.

The plan is _richly architected_ and _poorly specified_. The architecture choices are mostly defensible. The specification is largely missing. Architecture without specification is a building without load calculations — it may stand, but no one can prove it will.

VERDICT: AMEND
