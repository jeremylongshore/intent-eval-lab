# Shape Reconciliation Addendum — j-rig vs Kernel Schema Comparison

**Filing**: 017-RR-LAND-shape-reconciliation-addendum-2026-05-21.md
**Date**: 2026-05-21
**Author**: Jeremy Longshore (CTO + beads work; executed by Claude per CEO-mode directive)
**Bead**: `bd_000-projects-g5jt` (iel-shape-reconciliation-addendum, P0)
**Cluster**: iep-P1-kernel-adoption (`bd_000-projects-6hd6`) — IEP Convergence Debt Plan (2026-05-20, enhanced 2026-05-21)
**Supersedes**: nothing. **Addendum to**: `016-RR-LAND-kernel-shadow-inventory-2026-05-20.md` § 4.2 + § 6.
**Scope**: read-only analysis. No source modified.

---

## 1. Why this addendum exists

The 2026-05-20 inventory (016-RR-LAND) classified j-rig's `EvalSpecSchema`, `EvidenceBundleSchema`, `GateResultPredicateSchema`, and `GateResultEnum` as "DUPLICATES kernel" based on a **name match**. Architecture review on 2026-05-21 flagged this as Class-2 risk: a name match between two TypeScript types in different repos is not the same as a shape match. **Mechanical name-based codemod risks breaking j-rig's eval framework if the underlying shapes diverge.**

The plan (IEP Convergence Debt Plan, enhanced 2026-05-21) makes this addendum an **explicit gate**: no j-rig codemod PR (`iaj-E02b`) opens until field-by-field shape comparison lands. This document is that comparison.

The four target items:

1. `EvalSpec` / `EvalSpecSchema` — already classified in 016 § 2 as "name-collision pending shape proof" (j-rig's eval-spec is YAML eval-contract format; kernel's EvalSpec is canonical research-eval per Blueprint B § 2.1). This addendum confirms the collision and recommends the rename.
2. `EvidenceBundle` / `EvidenceBundleSchema` — § 3 below.
3. `GateResultPredicate` / `GateResultV1` — § 4 below. **Unification-relevant boundary per DR-010 Q3.**
4. `GateResult` / `GateDecision` enum — § 5 below.

---

## 2. EvalSpec — confirmed NAME COLLISION; rename retained-local

**Kernel** (`intent-eval-core/src/entities/EvalSpec.ts`):

Per Blueprint B § 2.1 the canonical `EvalSpec` is the platform-wide research-eval contract. Required fields include `id: UUIDv7`, `version: SemVer`, `name: KebabSlug`, `matchers: MatcherMap FKs`, `assertions: AssertionExpression[]`, `scoring: ScoringConfig`, `composition: CompositionDag`, `expected_artifacts: Sha256[]`, `runtime_limits: RuntimeLimits`, `provider_constraints: string[]`, `created_at`, `created_by`, `content_hash`.

**j-rig** (`j-rig-binary-eval/packages/core/src/schemas/eval-spec.ts:31-52`):

```typescript
export const EvalSpecSchema = z.object({
  spec_version: z.literal("1.0"),
  skill_name: z.string(),
  description: z.string(),
  criteria: z.array(CriterionSchema),
  test_cases: z.array(TestCaseSchema),
  models: z.array(ModelTargetSchema),
  siblings: z.array(SiblingSkillSchema).optional(),
  tags: z.array(z.string()).optional(),
});
export type EvalSpec = z.infer<typeof EvalSpecSchema>;
```

This is the j-rig YAML eval-contract format for the 7-layer skill-eval framework. It captures **a specific skill's eval contract** — completely different from kernel's `EvalSpec`, which captures **a canonical platform-wide eval specification**.

**Shape overlap**: only `description: string`. Zero structural overlap on any other field.

**Classification**: NAME COLLISION. Not a duplicate. Codemodding j-rig to import kernel's `EvalSpec` would break j-rig's eval framework (j-rig's `Criterion`, `TestCase`, `ModelTarget`, `SiblingSkill` don't exist in kernel; kernel's `matchers`, `assertions`, `scoring`, `composition` don't exist in j-rig).

**Reconciliation**: j-rig renames its local type to free up the canonical `EvalSpec` name.

**Recommended rename**: `JrigSkillEval` / `JrigSkillEvalSchema` (or, less verbose, `SkillEvalContract` / `SkillEvalContractSchema`). The "Jrig" prefix is the safer choice — it makes the j-rig-local-ness explicit at every import site and prevents future name re-collision if kernel grows a `SkillEval` concept.

**Cost**: pure rename. No semantic change. Walk every import of `EvalSpec` / `EvalSpecSchema` from `@j-rig/core` schemas and rename. ~6 files per 016 § 4.2 grep.

**Bead**: new sub-bead under `iaj-E02b` (or its own bead): `iaj-eval-spec-rename` (P1, task).

---

## 3. EvidenceBundle — DIVERGENT ABSTRACTION LAYERS

### 3.1 Field-by-field comparison

**Kernel `EvidenceBundle`** (`intent-eval-core/src/entities/EvidenceBundle.ts:62-113`):

| Field | Type | Semantics |
|---|---|---|
| `id` | `Uuidv7` | PK. The bundle's database-row identity. |
| `eval_run_id` | `Uuidv7` | FK → EvalRun.id. |
| `created_at` | `Rfc3339` | When the bundle row was created. |
| `predicate_uri_set` | `readonly (KnownPredicateUri \| (string & {}))[]` | Which predicate URIs appear in the bundle's rows. |
| `row_count` | `number` | How many rows are in the bundle. |
| `subject_set` | `readonly InTotoSubject[]` | Deduplicated subjects across rows. |
| `storage_key` | `StorageKey` | sha256-content-addressed object-storage key for the **payload** (the actual rows). The bundle row carries only the pointer. |
| `signing_mode` | `'sigstore_staging' \| 'rekor_production' \| 'unsigned_experimental'` | Signing posture. |
| `rekor_log_indices` | `readonly number[]` | Rekor transparency-log indices when applicable. |
| `verification_status` | `'verified' \| 'unverified' \| 'failed'` | Most-recent verification result. |
| `verification_last_checked_at` | `Rfc3339` | When verification was last checked. |

**Abstraction layer**: this is the **bundle index row** — metadata about a content-addressed storage object plus signing/verification state. The actual rows live behind `storage_key`. The kernel models the bundle-as-database-row.

**j-rig `EvidenceBundleSchema`** (`j-rig-binary-eval/packages/core/src/schemas/evidence-bundle.ts:139-145`):

| Field | Type | Semantics |
|---|---|---|
| `bundle_format` | `z.literal("json-array")` | Container format tag. |
| `rows` | `z.array(EvidenceStatementSchema)` | The actual in-toto Statements. |

**Abstraction layer**: this is the **bundle payload** — the literal JSON array of in-toto Statement rows. j-rig models the bundle-as-payload.

### 3.2 Classification: DIVERGENT (different abstraction layers)

These are two different concepts sharing a name. The kernel's `EvidenceBundle` is the database-row-with-metadata; j-rig's `EvidenceBundleSchema` is the wire format of the rows themselves. They are not even on the same side of the producer/consumer line:

- Kernel's `EvidenceBundle` is what a **consumer** (intent-rollout-gate, lab UI, archival service) reads when it wants to find + verify a bundle.
- j-rig's `EvidenceBundleSchema` is what a **producer** (j-rig CLI's `emit-evidence`) writes to disk and what a **consumer** parses to extract individual rows.

The two concepts are complementary, not duplicative. Both legitimately exist; both deserve names. The current name overlap is a coincidence of vocabulary, not a real duplication.

### 3.3 Reconciliation options

Three legitimate paths. The user/ISEDC picks one:

**Option α** — Kernel adds a distinct payload type; j-rig re-exports it.
- Kernel introduces `EvidenceBundlePayload` (or similar) as the canonical wire format. j-rig deletes its local `EvidenceBundleSchema` and re-exports `EvidenceBundlePayloadSchema` from kernel.
- Pro: full unification at both the database-row AND wire-format layers. DR-010 Q3 unification thesis maximally satisfied.
- Con: requires a kernel change (new Class-1 contract surface). Subsequent minor version of `@intentsolutions/core`. Coordinated migration.

**Option β** — j-rig renames; kernel keeps current `EvidenceBundle`; no re-export.
- j-rig renames `EvidenceBundleSchema` → `EvidenceBundlePayloadSchema` (or `EvidenceRowBundleSchema`, `StatementsContainerSchema`, etc.). Local to j-rig.
- Pro: minimal change. No kernel modification. Resolves name collision.
- Con: leaves two parallel concepts with no shared codepath. Future drift risk if kernel later grows a payload type.

**Option γ** — Kernel absorbs j-rig's wire format; j-rig deletes.
- Kernel adopts j-rig's `EvidenceBundleSchema` as a sibling type under a different name; j-rig codemod-imports from kernel.
- Same as Option α effectively. Worth listing only to make explicit that "kernel grows the new type" is the path forward — kernel never shrinks.

**Recommendation**: **Option α**. The unification thesis (DR-010 Q3 BINDING) is the platform's load-bearing architectural principle. The wire format of evidence rows is the most consumer-facing surface in the platform — keeping it canonical is exactly what the kernel exists for. Cost is one new contract type in a minor kernel version; cleanliness payoff is permanent.

**If Option α is chosen**, the new kernel contract should also fold in j-rig's `EvidenceStatementSchema` (the row shape) and the cross-field invariants enforced in j-rig's `superRefine` (subject[0].name === predicate.gate_id; subject[0].digest.sha256 === predicate.input_hash without prefix). These invariants are normative per Blueprint B § 7.3 line 792 and currently exist only in j-rig.

**Class assessment**: this is a Class-2 ISEDC matter. Kernel surface growth that ripples across consumers + touches the unification-relevant boundary.

---

## 4. GateResultPredicate vs GateResultV1 — NORMATIVE DIVERGENCE

This is the consequential finding. The j-rig `GateResultPredicate` mirrors the **v0.1.0-draft** lab spec; the kernel's `GateResultV1` reflects the **NORMATIVE Blueprint B § 7.4** spec landed 2026-05-15 (via PRs 56, 63, 64). j-rig has not been updated since the normative lock.

### 4.1 Required-field comparison

| Kernel `GateResultV1Required` field | j-rig `GateResultPredicateSchema` field | Status |
|---|---|---|
| `gate_id: string` | `gate_id: z.string()` | ✅ Match (same regex enforced in both). |
| `gate_name: string` | — | ❌ **Missing in j-rig.** Required in kernel per § 7.4 line 803. |
| `gate_version: string` (SemVer) | — | ❌ **Missing in j-rig.** Required in kernel per § 7.4 line 804. |
| `gate_decision: GateDecision` (`'pass'\|'fail'\|'advisory'\|'error'`) | `result: GateResultEnum` (`"PASS"\|"FAIL"\|"ADVISORY"\|"NOT_APPLICABLE"`) | ⚠️ **Divergent.** Field name differs (`gate_decision` vs `result`); enum case differs (lowercase vs uppercase); fourth value differs (kernel has `'error'`, j-rig has `"NOT_APPLICABLE"`). See § 5 for enum reconciliation. |
| `gate_reasons: readonly string[]` | — | ❌ **Missing in j-rig.** Required in kernel per § 7.4 line 806. Empty array permitted for unconditional pass; required ≥1 entry for fail/advisory/error per kernel doc. |
| `coverage: Coverage` (`dimensions_evaluated[] + dimensions_skipped[]`) | — | ❌ **Missing in j-rig.** Required in kernel per § 7.4 line 807. NOT_APPLICABLE encoding flows through `coverage.dimensions_skipped`, not through the decision enum. |
| `policy_ref: string` (`sha256:<hex>:<repo-relative-path>`) | — | ❌ **Missing in j-rig.** Required in kernel per § 7.4 line 808. Defends against mid-flight policy mutation. |
| `policy_hash: Sha256Prefixed` | `policy_hash: z.string().regex(SHA256_PREFIXED_REGEX)` | ✅ Match. |
| `input_hash: Sha256Prefixed` | `input_hash: z.string().regex(SHA256_PREFIXED_REGEX)` | ✅ Match. |
| `evaluated_at: Rfc3339` | `timestamp: z.string().datetime()` | ⚠️ **Field name differs.** Same semantic; kernel renamed for clarity. |
| `runner: string` | `runner: z.string().regex(RUNNER_REGEX)` | ✅ Match. |
| `commit_sha: string` | `commit_sha: z.string().regex(COMMIT_SHA_REGEX)` | ✅ Match. |

### 4.2 Optional-field comparison

| Kernel `GateResultV1Optional` field | j-rig field | Status |
|---|---|---|
| `metadata?: Record<string, unknown>` | `metadata: z.record(...).optional()` | ✅ Match. |
| `failure_mode?: string` | `failure_mode: z.string().optional()` | ✅ Match. |
| `advisory_severity?: AdvisorySeverity` | `advisory_severity: AdvisorySeverityEnum.optional()` | ✅ Match (same 3-value enum: `'info'|'warn'|'error'`). |
| `cost_record_ref?: Uuidv7` | — | ❌ **Missing in j-rig.** Kernel addition. |
| `replay_fidelity_level?: ReplayFidelityLevel` | — | ❌ **Missing in j-rig.** Kernel addition (forward-ref to iel-E11 RF-0..RF-4). |

### 4.3 Cross-field invariants

Both schemas enforce the same cross-field invariants (subject[0].name === predicate.gate_id; subject[0].digest.sha256 === predicate.input_hash without prefix). j-rig enforces these in `EvidenceStatementSchema.superRefine`; kernel documents them in prose at `gate-result-v1.ts:158-160` + Blueprint B § 7.3 line 792. **No divergence on invariants.** Both implementations would accept/reject the same rows for these checks.

### 4.4 Classification: NORMATIVE DIVERGENCE

This is not a duplication; it is a **stale implementation**. j-rig's schema implements the v0.1.0-draft spec from before the normative lock. The kernel implements the normative spec as adopted via Blueprint B § 7.4.

Per DR-010 Q3 (unification thesis BINDING), every validator MUST emit Evidence Bundle conformant to kernel's `gate-result/v1` contract. j-rig's current output is **non-conformant**:

- j-rig emits `result` instead of `gate_decision`.
- j-rig emits `timestamp` instead of `evaluated_at`.
- j-rig does not emit `gate_name`, `gate_version`, `gate_reasons`, `coverage`, or `policy_ref`.
- j-rig's decision enum uses uppercase + has `NOT_APPLICABLE` instead of kernel's `'error'`.

Any consumer that follows the kernel's normative schema (and that's the binding requirement — see kernel's `gate-result-v1.ts:1-18` docstring: "Adding a field or loosening a constraint here MUST go through Class-1 ISEDC convening") will reject every row j-rig currently produces.

### 4.5 Reconciliation: j-rig upgrades to kernel's normative shape (BREAKING CHANGE)

The unification thesis admits only one direction: kernel wins. j-rig migrates.

**Required j-rig schema changes**:

1. Rename `result` field → `gate_decision`.
2. Rename `timestamp` field → `evaluated_at`.
3. Change `result` enum values from uppercase to lowercase per kernel: `'pass' | 'fail' | 'advisory' | 'error'`.
4. Remove `NOT_APPLICABLE` value from enum; encode NOT_APPLICABLE via `coverage.dimensions_skipped` instead per Blueprint B § 7.4 line 832.
5. Add required fields: `gate_name`, `gate_version`, `gate_reasons`, `coverage`, `policy_ref`.
6. Add optional fields: `cost_record_ref`, `replay_fidelity_level`.
7. Either re-export kernel's `GateResultV1` shape directly (preferred) OR define a local Zod schema that exactly mirrors kernel's TS type — re-export is preferred to eliminate drift surface.

**Consumer impact within j-rig**:

Per 016 § 4.2, the following j-rig files consume `GateResultPredicate` / `EvidenceBundle*` types:

- `packages/core/src/index.ts`
- `packages/core/src/evidence/writer.ts`
- `packages/core/src/evidence/reader.ts`
- `packages/core/src/evidence/index.ts`
- `packages/cli/src/commands/emit-evidence.ts`
- `packages/db/src/schema.ts`

Each must be updated to:
- Emit the new field set (`gate_name`, `gate_version`, `gate_reasons`, `coverage`, `policy_ref` — sites that produce rows must now construct these fields).
- Read using the new field names (`gate_decision` not `result`; `evaluated_at` not `timestamp`).
- Map the `NOT_APPLICABLE` decision pattern through `coverage.dimensions_skipped` per the kernel doctrine.

This is **substantively more than a codemod** — the producing sites must now know how to populate `gate_name`, `gate_version`, `gate_reasons`, `coverage`, `policy_ref`. Some of these values are knowable mechanically (`gate_version` from package.json; `gate_name` from a per-gate constant); others are semantic (`gate_reasons` requires the gate logic to produce structured reason strings).

**Class assessment**: Class-2 ISEDC matter. This is a breaking schema change to a producer of attestations + downstream API breakage for any j-rig consumer reading `result` / `timestamp` fields.

**Migration sequencing recommendation**:

1. ISEDC ratifies the j-rig schema upgrade (Class-2 review — likely fast since it's a unification-thesis enforcement, not a contested design choice).
2. j-rig adds the kernel as a dep (`iaj-E02a`, already filed).
3. j-rig schema upgrade lands as a single coherent PR: rename + add fields + delete local duplicate + re-export from kernel + update all 6 downstream consumers + tests.
4. j-rig bumps major version (per its own SemVer policy — `result`→`gate_decision` is a breaking change for any j-rig consumer).
5. Release notes call out the schema upgrade explicitly with a migration table for j-rig's external consumers.

**Bead structure**:

- `iaj-E02a` (add dep) — already filed, unchanged.
- `iaj-E02b` (codemod schema imports) — **scope upgrade**: from "re-export name-matched types" to "upgrade j-rig to kernel's normative schema; rename `result` → `gate_decision`; rename `timestamp` → `evaluated_at`; add 5 required fields; populate them at all producer sites." This is the actual unification work.
- `iaj-E02c` (delete duplicated) — unchanged in concept; deletes happen as part of the codemod PR.
- `iaj-E02d` (regression suite green) — gains scope: must verify the new wire format round-trips and that producer sites populate the new fields. Negative tests should verify rejection of v0.1.0-draft-shaped rows.
- New bead: `iaj-schema-upgrade-aar` (P1) — AAR doc + j-rig release notes capturing the breaking change.

---

## 5. GateResult enum — DIVERGENT (case + fourth value)

### 5.1 Comparison

**Kernel `GateDecision`** (`intent-eval-core/src/predicates/gate-result-v1.ts:35`):

```typescript
export type GateDecision = 'pass' | 'fail' | 'advisory' | 'error';
```

**j-rig `GateResult`** (`j-rig-binary-eval/packages/core/src/schemas/evidence-bundle.ts:22-23`):

```typescript
export const GateResultEnum = z.enum(["PASS", "FAIL", "ADVISORY", "NOT_APPLICABLE"]);
export type GateResult = z.infer<typeof GateResultEnum>;
```

### 5.2 Classification: DIVERGENT (case + semantics)

Two differences:

1. **Case.** Kernel is lowercase; j-rig is uppercase. Pure stylistic; carries no semantic weight on its own.
2. **Fourth value.** Kernel has `'error'` (gate ran into infrastructure failure — verdict on the gate, not the input). j-rig has `"NOT_APPLICABLE"` (gate determined input is out of scope).

The fourth-value divergence is the structural one. Per Blueprint B § 7.4 line 832, NOT_APPLICABLE is **not encoded as a decision-enum value** — it's encoded as `gate_decision: 'pass'` + `coverage.dimensions_skipped[]` populated + `gate_reasons` documenting the skip. And `'error'` is a distinct verdict-on-the-gate case that j-rig currently has no representation for.

### 5.3 Reconciliation (forced by § 4)

j-rig migrates the enum to kernel's shape:

- `"PASS"` → `'pass'`
- `"FAIL"` → `'fail'`
- `"ADVISORY"` → `'advisory'`
- `"NOT_APPLICABLE"` → eliminate; map to `'pass'` + populated `coverage.dimensions_skipped` + `gate_reasons` per kernel doctrine.
- New value: `'error'` for gate-infrastructure failures.

This is the same migration as § 4. The enum is a sub-concern of the predicate-body upgrade and lands in the same PR.

**Class assessment**: this is enum-level, not standalone — it rides on § 4's Class-2 review.

---

## 6. Re-classification of 016 § 4.2 — corrected

The inventory § 4.2 table classified four j-rig items as "DUPLICATES kernel." Corrected classification per this addendum:

| Local definition | Original (016) | Corrected (017) |
|---|---|---|
| `eval-spec.ts:31` — `EvalSpecSchema` | DUPLICATES kernel | **NAME COLLISION** — rename j-rig local |
| `eval-spec.ts:52` — `EvalSpec` type | DUPLICATES kernel | **NAME COLLISION** — rename j-rig local |
| `evidence-bundle.ts:22-23` — `GateResultEnum` + `GateResult` | OVERLAPS kernel | **DIVERGENT (subset of § 4 migration)** — kernel wins; rides on § 4 PR |
| `evidence-bundle.ts:54-83` — `GateResultPredicateSchema` + `GateResultPredicate` | DUPLICATES kernel | **NORMATIVE DIVERGENCE** — j-rig upgrades to kernel's normative shape (breaking change for j-rig) |
| `evidence-bundle.ts:139-145` — `EvidenceBundleSchema` + `EvidenceBundle` | DUPLICATES kernel | **DIVERGENT ABSTRACTION LAYERS** — kernel grows a payload type (Option α); j-rig re-exports |

The corrected classifications materially change the migration scope:

- **3 of 5 items** require ISEDC Class-2 review or rideshare: § 3 (EvidenceBundle), § 4 (predicate body), § 5 (enum). § 4 and § 5 ride together; § 3 is independent.
- **1 of 5 items** is a kernel-side change (Option α from § 3) before j-rig can re-export.
- **1 of 5 items** is a pure rename (§ 2 EvalSpec) — proceed without ISEDC; just engineering.

The inventory § 4.2 migration-cost estimate of "1-2 days" was based on a name-based codemod. With normative divergence, the realistic estimate is closer to a week of focused work — the producer sites in j-rig must learn to populate the new fields (`gate_name`, `gate_version`, `gate_reasons`, `coverage`, `policy_ref`), and the j-rig release becomes a breaking version bump.

---

## 7. ISEDC convening recommendation

This addendum's findings cross the Class-2 threshold per the standing ISEDC discipline (umbrella `CLAUDE.md` § ISEDC). Convening is recommended for two questions:

1. **j-rig predicate-body upgrade** (§ 4 + § 5). The unification thesis (DR-010 Q3 BINDING) makes the direction non-negotiable, but ISEDC review is appropriate because:
   - It's a breaking change for j-rig's external consumers.
   - It revalidates the unification thesis against the practical cost (the council can affirm "yes, this is what unification means in practice").
   - It locks the migration sequencing + release-note + version-bump policy on the record.
2. **Kernel EvidenceBundle wire-format growth** (§ 3, Option α). Kernel adds `EvidenceBundlePayload` + `EvidenceStatement` types. New kernel contract surface. Bumps `@intentsolutions/core` minor version.

Both questions are appropriate for a single ISEDC session ("j-rig kernel-adoption normative reconciliation"). The CTO, CISO, CMO, and GC seats carry the live concerns:

- **CTO**: schema authority + unification thesis enforcement
- **CISO**: signed attestation surface — j-rig's existing emit-evidence flow has been producing rows that will be rejected by spec-compliant verifiers. CISO needs to weigh whether existing j-rig attestations need re-emission or whether they can stay in `sigstore_staging` until j-rig upgrades.
- **CMO**: external communication around the breaking change in j-rig (release notes, migration guide; tied to OSS positioning).
- **GC**: PREDICATE-TYPES.md registry update + DR filing if a new minor of kernel ships with the payload type.

The remaining 3 seats (CFO, CSO, VP DevRel) carry standing positions but no live concerns specific to this decision. Their seats should still be represented per adversarial-integrity protocol.

**Proposed bead**: `iep-isedc-session-5-jrig-reconciliation` (P0, feature), filed under `iep-P1-kernel-adoption` umbrella. Convening artifact filed as `intent-eval-lab/000-docs/018-AT-DECR-isedc-council-session-5-jrig-reconciliation-2026-05-XX.md` per Doc Filing Standard v4.3.

---

## 8. Decisions deferred / not in scope of this addendum

- **iah-E02 path** (audit-harness kernel adoption). Out of scope here; separate question. Architectural-question note already on parent bead (`bd_000-projects-46x`) via bd-sync per the 2026-05-21 enhanced plan.
- **Lab schema repoint** (`iel-link-schemas-to-kernel`, P5 priority). Independent track. Can proceed in parallel without waiting on this addendum or ISEDC.
- **j-rig version-bump policy** for the breaking change. Goes into ISEDC alongside § 4 — the council records the version-bump policy.
- **Existing j-rig attestations** (if any have been signed against the v0.1.0-draft schema). Need CISO call on whether they need re-emission. ISEDC § 4 includes this.
- **Kernel minor-version bump** for Option α (§ 3). ISEDC ratifies the new payload contract; kernel team owns the implementation under existing `iec-*` cluster discipline.

---

## 9. Acceptance for `bd_000-projects-g5jt`

- [x] Field-by-field comparison tables for EvidenceBundle (§ 3.1), GateResultPredicate (§ 4.1 + § 4.2), GateResult enum (§ 5.1)
- [x] Explicit divergence-vs-re-export decision per item (§ 6 corrected classifications)
- [x] EvalSpec name-collision rename recommendation (§ 2)
- [x] ISEDC convening recommendation with question scoping (§ 7)
- [x] Cross-refs to 016 inventory + Blueprint B § 7 + DR-010 Q3

**Recommend closing `bd_000-projects-g5jt` once this document lands on lab main.** Closure unblocks Class-2 ISEDC convening (`iep-isedc-session-5-jrig-reconciliation`), which in turn unblocks the upgraded `iaj-E02b` migration scope.

---

## 10. Source-of-truth verification trail

This addendum was constructed by:

1. Reading kernel canonical files: `intent-eval-core/src/entities/EvidenceBundle.ts` (113 lines), `intent-eval-core/src/predicates/gate-result-v1.ts` (294 lines), `intent-eval-core/src/entities/index.ts` (27 lines).
2. Reading j-rig canonical files: `j-rig-binary-eval/packages/core/src/schemas/evidence-bundle.ts` (146 lines), `j-rig-binary-eval/packages/core/src/schemas/eval-spec.ts` (verified lines 31, 52).
3. Reading Blueprint B § 7.1–§ 7.5 (normative predicate spec, lines 730–849).
4. Cross-checking against DR-010 Q3 (unification thesis BINDING) per `intent-eval-lab/000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md`.
5. Cross-checking against 016 § 4.2 + § 6 (the items this addendum re-classifies).

All findings derive from the verified file tree at lab `main` (commit referenced in 016 § 9). No claim relies on memory.

— Jeremy Longshore
intentsolutions.io
