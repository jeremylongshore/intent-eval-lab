# Kernel Shadow Inventory — Local Re-Definitions of Canonical Types Across 5 Repos

**Filing**: 016-RR-LAND-kernel-shadow-inventory-2026-05-20.md
**Date**: 2026-05-20
**Author**: Jeremy Longshore (CTO + beads work; executed by Claude)
**Bead**: `bd_000-projects-x6dd` (iep-kernel-shadow-inventory, P0)
**Cluster**: iep-P1-kernel-adoption (`bd_000-projects-6hd6`) — IEP Convergence Debt Plan (2026-05-20)
**GitHub**: jeremylongshore/intent-eval-lab#58
**Plane**: LAB-91
**Scope**: read-only audit. No source code modified.

---

## 1. Purpose

Inventory every local re-definition of any canonical kernel type across the 5 Intent Eval Platform repositories. The kernel (`@intentsolutions/core@0.1.0`) is published with sigstore provenance and is the canonical source for the 13-entity domain model + `gate-result/v1` predicate spec per Blueprint B § 2 and § 7. Consumer-side migration to the kernel is gated on knowing **exactly** what currently shadows kernel exports.

This document is the unblocker for the four parallel consumer migrations in Priority 1: `iah-E02*`, `iaj-E02*`, `iel-link-schemas-to-kernel`, and `iar-consumer-migration`.

---

## 2. Scope orientation — what the plan got wrong

The 2026-05-20 IEP Convergence Debt plan named "11 canonical types" to inventory:

> EvidenceBundle, EvalSpec, EvalRun, EvalCase, SessionTrace, Provider, JudgeAdapter, ScoringConfig, MatcherInputPattern, AssertionExpression, GateResultV1

**3 of those 11 names do not exist in the kernel surface as defined in `intent-eval-core/src/entities/index.ts`:**

| Plan-listed name | Status in kernel                                                                                                                                                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `EvalCase`       | **Not a kernel export.** Closest analogue: cases live as fields inside `EvalSpec`. No standalone entity.                                                                                                                                         |
| `Provider`       | **Not a kernel export.** "Provider" appears only in code comments (e.g., `CostRecord.ts` says "Provider identifier (e.g., anthropic, openai)") and toolspecs (`ToolInvocation.ts` describes "provider:vendor:model" format). Not an entity type. |
| `JudgeAdapter`   | **Not a kernel export.** Closest analogue: `JudgeDecision` entity. No "adapter" abstraction.                                                                                                                                                     |

These are plan-recollection errors (the plan was drafted from memory rather than from the kernel's `src/entities/index.ts`). They do not represent gaps in the kernel — they represent names the plan invented. **The inventory below uses the ACTUAL kernel surface, not the plan-listed names.**

### The actual kernel canonical surface

Per `intent-eval-core/src/entities/index.ts` (verified 2026-05-20), the kernel re-exports 13 canonical entities:

1. `EvalSpec`
2. `EvalRun`
3. `MatcherMap` (with embedded `MatcherInputPattern` sub-type)
4. `EvidenceBundle`
5. `JudgeDecision`
6. `RuntimeReceipt`
7. `RegressionPack`
8. `RolloutGate`
9. `SkillSnapshot`
10. `SessionTrace`
11. `ToolInvocation`
12. `CostRecord`
13. `FailureTaxonomy`

Plus from `src/predicates/`:

1. `GateResultV1` (the `gate-result/v1` predicate type — NORMATIVE per Blueprint B § 7)

Plus sub-types inside the entity files (kernel-exported, but not standalone entities):

- `ScoringConfig` (inside `EvalSpec.ts`)
- `AssertionExpression` (inside `EvalSpec.ts`, declared as `unknown`)
- `MatcherInputPattern` (inside `MatcherMap.ts`)

Note on j-rig's parallel sub-types: j-rig defines its own local sub-types (`ModelTarget`, `SiblingSkill`, `GateResultEnum`, etc.) that are NOT kernel exports and are NOT part of the kernel canonical surface. They are j-rig-local concepts that share namespace adjacency with the kernel but live entirely under `@j-rig/core`. Their classification is documented in § 4.2 (j-rig-specific types retained locally) and § 6 (open question on `GateResultEnum` vs kernel `GateResultV1`).

The kernel publishes JSON Schemas for the 13 entities + `gate-result.schema.json` at `intent-eval-core/schemas/v1/*.schema.json`. Verified file listing matches the entity list.

---

## 3. Kernel adoption baseline — zero across all 4 consumers

Grep verification across all 4 consumer repos' `package.json` and per-workspace `packages/*/package.json` files:

| Repo                | `@intentsolutions/core` in deps? |
| ------------------- | -------------------------------- |
| audit-harness       | NO                               |
| j-rig-binary-eval   | NO                               |
| intent-rollout-gate | NO                               |
| intent-eval-lab     | NO                               |

**Conclusion**: kernel adoption is at 0% across the platform. Priority 1's `iah-E02a`, `iaj-E02a`, and `iar-consumer-migration` will each be the **first** consumption of the kernel in their respective repos.

---

## 4. Per-repo inventory — local re-definitions of kernel canonical types

### 4.1 audit-harness — clean

**Production-code type definitions of kernel-canonical types**: NONE.

`audit-harness/bin/audit-harness.js` (the CLI dispatcher) references the strings `EvidenceBundle` and `gate-result` in usage text / command names, but defines no types. Audit-harness has no TypeScript surface and no schema files in production code paths.

**Retention site (acceptable; needs allowlist on the kernel-shadow-check CI gate)**:

| Path                                                               | Reason for retention                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `audit-harness/tests/fixtures/gate-result.schema.json` (109 lines) | Test fixture used by audit-harness's own test suite to validate that its `emit-evidence` output conforms to a known-good predicate shape. Acceptable retention: tests need a stable on-disk copy that's not re-pinned every kernel release. Future allowlist entry on `audit-harness kernel-shadow-check` should permit this path with a comment-reference to this inventory and a periodic sync expectation. |

**Migration cost**: `iah-E02a` (add dep), `iah-E02b` (no codemod needed — no local types), `iah-E02c` (no deletions needed), `iah-E02d` (regression suite green — minimal risk).

**Recommendation**: `iah-E02b` and `iah-E02c` can be closed quickly with a one-line evidence note ("no local types to migrate; audit-harness has no production TS surface for kernel entities"). `iah-E02a` still adds the dep so that `audit-harness/bin/audit-harness.js`'s future `kernel-shadow-check` subcommand (per `iah-kernel-shadow-check` / `bd_000-projects-873c`) can import the kernel's Zod validators.

---

### 4.2 j-rig-binary-eval — substantial drift (the real migration work)

**Production-code type definitions of kernel-canonical types**: 4 confirmed kernel-canonical duplications + several adjacent sub-types.

All in `j-rig-binary-eval/packages/core/src/schemas/`:

| Local definition                                                                                                                                   | Kernel canonical                                                                              | Status                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `packages/core/src/schemas/eval-spec.ts:31` — `export const EvalSpecSchema = z.object({...})`                                                      | `intent-eval-core/src/validators/v1/eval-spec.ts` — `EvalSpecSchema`                          | **DUPLICATES kernel**                                                                                                                                                                     |
| `packages/core/src/schemas/eval-spec.ts:52` — `export type EvalSpec = z.infer<typeof EvalSpecSchema>`                                              | `intent-eval-core/src/entities/EvalSpec.ts` — `EvalSpec` interface                            | **DUPLICATES kernel**                                                                                                                                                                     |
| `packages/core/src/schemas/evidence-bundle.ts:22-23` — `GateResultEnum` + `GateResult` type (`"PASS" \| "FAIL" \| "ADVISORY" \| "NOT_APPLICABLE"`) | Kernel's `GateResultV1` predicate value space                                                 | **OVERLAPS kernel.** Probably a value-space subset of kernel's predicate result enum. Needs reconciliation: either re-export kernel's, or define j-rig's as a transformation of kernel's. |
| `packages/core/src/schemas/evidence-bundle.ts:54-83` — `GateResultPredicateSchema` + `GateResultPredicate` type                                    | `intent-eval-core/src/predicates/gate-result-v1.ts` — `GateResultV1`                          | **DUPLICATES kernel.** This is the most consequential duplication — the predicate is NORMATIVE per Blueprint B § 7 and the kernel is the single source of truth.                          |
| `packages/core/src/schemas/evidence-bundle.ts:139-145` — `EvidenceBundleSchema` + `EvidenceBundle` type                                            | `intent-eval-core/src/entities/EvidenceBundle.ts` — `EvidenceBundle` + `EvidenceBundleSchema` | **DUPLICATES kernel**                                                                                                                                                                     |

**j-rig-specific types in the same files (not in kernel; retain locally)**:

| Local definition                                                                           | Why it's j-rig-local                                                                                |
| ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `eval-spec.ts:8-9` — `ModelTarget` ("haiku"\|"sonnet"\|"opus")                             | Provider-specific enum; not a kernel concern                                                        |
| `eval-spec.ts:14-23` — `SiblingSkill` (Schema + type)                                      | j-rig regression-pack concept; not a kernel entity                                                  |
| `evidence-bundle.ts:25-26` — `AdvisorySeverity` ("info"\|"warn"\|"error")                  | Application-layer concern; not in kernel                                                            |
| `evidence-bundle.ts:29-30` — `PipelineSide` ("client"\|"server"\|"ci"\|"sandbox"\|"local") | Runtime-classification enum; not in kernel                                                          |
| `evidence-bundle.ts:86-96` — `Subject` (Schema + type)                                     | in-toto envelope subject; kernel may absorb later, but currently j-rig-local                        |
| `evidence-bundle.ts:105-132` — `EvidenceStatement` (Schema + type)                         | Composition of Subject + Predicate; could be folded if kernel grows this, but currently j-rig-local |
| `eval-contract.ts:12-60` — `EvalContractSchema` + `EvalContract` type                      | j-rig's adoption surface for eval contracts; distinct from kernel's `EvalSpec`                      |

**Migration target file list for `iaj-E02b` (codemod)**:

```text
j-rig-binary-eval/packages/core/src/schemas/eval-spec.ts        (lines 31, 52)
j-rig-binary-eval/packages/core/src/schemas/evidence-bundle.ts  (lines 22-23, 54-83, 139-145)
```

**Migration target file list for `iaj-E02c` (delete duplicated)**:

After codemod, the duplicated exports at lines 31+52 (eval-spec.ts) and 54-83+139-145 (evidence-bundle.ts) can be deleted in favor of re-exports from `@intentsolutions/core`. The lines 22-23 (`GateResult` enum) need reconciliation discussion — see § 6 below.

**Downstream consumers of the j-rig local types** (must update import paths after codemod):

Files known to import from `packages/core/src/schemas/`:

```text
j-rig-binary-eval/packages/core/src/index.ts                    (workspace re-exports)
j-rig-binary-eval/packages/core/src/evidence/writer.ts          (uses EvidenceBundleSchema)
j-rig-binary-eval/packages/core/src/evidence/reader.ts          (uses EvidenceBundleSchema)
j-rig-binary-eval/packages/core/src/evidence/index.ts           (re-exports)
j-rig-binary-eval/packages/cli/src/commands/emit-evidence.ts    (uses EvidenceBundleSchema)
j-rig-binary-eval/packages/db/src/schema.ts                     (uses EvalSpec)
```

Full grep would expand this list — codemod (`iaj-E02b`) must walk every TS file in `packages/*/src/` and update imports.

**Migration cost**: high. j-rig is the substantive Priority 1 work.

---

### 4.3 intent-rollout-gate — no implementation yet (zero shadow)

**Production-code type definitions of kernel-canonical types**: NONE.

Repository contents (full file listing, non-node_modules, non-git):

```text
intent-rollout-gate/action.yml
intent-rollout-gate/.github/workflows/ci.yml
intent-rollout-gate/.claude/settings.json
intent-rollout-gate/.beads/* (local bead db)
```

No `package.json`, no `src/`, no TS, no schema files. The Action is the no-op composite stub per `action.yml`. Plan finding confirmed: intent-rollout-gate has zero implementation. The plan was correct that this is where M5 MVP work lands.

**Migration cost**: trivial. `iar-consumer-migration` (`bd_000-projects-cab3`) is essentially "when iar-E03 + iar-E04 land, the action imports the kernel via the j-rig package; no kernel adoption work specifically in this repo." Under Option-A architecture, kernel consumption flows in through `@j-rig/rollout-gate` — intent-rollout-gate is the thin shell.

---

### 4.4 intent-eval-lab — schema content under `specs/` (Priority 5 surface)

**Production-code type definitions of kernel-canonical types**: NONE in TS/JS source (lab has no TypeScript surface).

**Schema content (Priority 5 target):**

| Path                                                                                | Lines | Status                                                                                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` | 109   | **DUPLICATES kernel** — this is the JSON Schema version of what `@intentsolutions/core/schemas/v1/gate-result.schema.json` publishes. Priority 5 (`iel-link-schemas-to-kernel`) target.                                                                                                                |
| `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/README.md`               | TBD   | Documentation of the predicate; references SPEC.md.                                                                                                                                                                                                                                                    |
| `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/SPEC.md`                        | 333   | Contains the predicate contract text. Lines 94-278 describe the `gate-result/v1` predicate with URI `https://evals.intentsolutions.io/gate-result/v1`. **NORMATIVE per Blueprint B § 7.** Per Priority 5 work, this gets a kernel-canonical declaration; the schema file gets replaced with a pointer. |

**Plan correction**: the plan referenced `intent-eval-lab/specs/evidence-bundle/schema/gate-result.schema.json` (top-level `schema/` under `evidence-bundle/`). **This path does not exist.** The actual schema lives in the `v0.1.0-draft/schema/` subdirectory. Priority 5 work must target the actual path.

**Blueprint B § 7 reference** (lab's normative declaration of the predicate spec): `intent-eval-lab/000-docs/012-AT-ARCH-platform-runtime-blueprint.md` line 33 says:

> The JSON Schema at `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` lands as a normative reference alongside this document, not duplicated inside it.

After Priority 5: this sentence updates to declare `@intentsolutions/core/schemas/v1/gate-result.schema.json` as the canonical source, with the lab schema file becoming a pointer stub.

**Migration cost**: medium. Three new beads under `iep-P5` (`iel-link-schemas-blueprint-b`, `iel-link-schemas-glossary`, `iel-link-schemas-drift-ci`) cover the work. Plus the existing `iel-link-schemas-to-kernel` for the actual schema file replacement.

---

## 5. Migration target master list (file path → bead)

| File                                                                                                                          | Action                                                                                                                                 | Bead                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `audit-harness/package.json`                                                                                                  | Add `@intentsolutions/core` dep                                                                                                        | `iah-E02a` (`bd_000-projects-urxx`)                                                            |
| `audit-harness/bin/audit-harness.js`                                                                                          | Future `kernel-shadow-check` subcommand                                                                                                | `iah-kernel-shadow-check` (`bd_000-projects-873c`) — NEW                                       |
| `audit-harness/tests/fixtures/gate-result.schema.json`                                                                        | Retain; add to allowlist                                                                                                               | `iah-kernel-shadow-check` allowlist (post-implementation)                                      |
| `j-rig-binary-eval/packages/core/package.json` (and per-package package.json files)                                           | Add `@intentsolutions/core` dep                                                                                                        | `iaj-E02a` (`bd_000-projects-fzjx`)                                                            |
| `j-rig-binary-eval/packages/core/src/schemas/eval-spec.ts` lines 31, 52                                                       | Replace with re-export from kernel                                                                                                     | `iaj-E02b` (`bd_000-projects-qklh`)                                                            |
| `j-rig-binary-eval/packages/core/src/schemas/evidence-bundle.ts` lines 54-83, 139-145                                         | Replace with re-export from kernel                                                                                                     | `iaj-E02b`                                                                                     |
| `j-rig-binary-eval/packages/core/src/schemas/evidence-bundle.ts` lines 22-23 (`GateResult` enum)                              | RECONCILIATION DISCUSSION — see § 6                                                                                                    | `iaj-E02b` + open question                                                                     |
| j-rig consumers of the above (`evidence/writer.ts`, `reader.ts`, `index.ts`, `cli/commands/emit-evidence.ts`, `db/schema.ts`) | Update import paths                                                                                                                    | `iaj-E02b`                                                                                     |
| `j-rig-binary-eval/packages/core/src/schemas/eval-spec.ts` (after codemod)                                                    | Delete duplicated `EvalSpecSchema` + `EvalSpec` (keep `ModelTarget` + `SiblingSkill`)                                                  | `iaj-E02c` (`bd_000-projects-m1mn`)                                                            |
| `j-rig-binary-eval/packages/core/src/schemas/evidence-bundle.ts` (after codemod)                                              | Delete duplicated `EvidenceBundle*` + `GateResultPredicate*` (keep `AdvisorySeverity`, `PipelineSide`, `Subject`, `EvidenceStatement`) | `iaj-E02c`                                                                                     |
| j-rig regression suite                                                                                                        | Re-run; verify green                                                                                                                   | `iaj-E02d` (`bd_000-projects-5018`)                                                            |
| `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json`                                           | Replace content with pointer stub                                                                                                      | `iel-link-schemas-to-kernel` (`bd_000-projects-i4jh`)                                          |
| `intent-eval-lab/000-docs/012-AT-ARCH-platform-runtime-blueprint.md` § 7                                                      | Add kernel-canonical declaration sentence                                                                                              | `iel-link-schemas-blueprint-b` (`bd_000-projects-v1ao`) — NEW                                  |
| `intent-eval-lab/000-docs/014-DR-GLOS-canonical-glossary.md`                                                                  | Add kernel pointers per term                                                                                                           | `iel-link-schemas-glossary` (`bd_000-projects-7vvz`) — NEW                                     |
| `intent-eval-lab/.github/workflows/schema-drift.yml`                                                                          | NEW — CI drift-check gate                                                                                                              | `iel-link-schemas-drift-ci` (`bd_000-projects-1zr1`) — NEW                                     |
| intent-rollout-gate                                                                                                           | No direct kernel-adoption work; flows in via `@j-rig/rollout-gate` per Option-A                                                        | `iar-consumer-migration` (`bd_000-projects-cab3`) — wait on `iaj-E02` + `iaj-E03` + `iaj-E09b` |

---

## 6. Open question — `GateResult` vs `GateResultV1`

j-rig's `evidence-bundle.ts:22-23` defines:

````typescript
export const GateResultEnum = z.enum(["PASS", "FAIL", "ADVISORY", "NOT_APPLICABLE"]);
export type GateResult = z.infer<typeof GateResultEnum>;
```text

Kernel's `intent-eval-core/src/predicates/gate-result-v1.ts` defines `GateResultV1` as the full predicate object (the in-toto attestation predicate, including subject, decision, gate findings, scoring, evidence pointers, etc.). The j-rig enum is a **value-space subset** — the four possible decision values.

Two possible reconciliations, both legitimate:

- **Option α**: kernel adds a `GateDecision` enum (or similar) as the decision-value-only sub-type, and j-rig re-exports it. Pro: prevents drift on the enum values. Con: bloats kernel surface with a sub-type that may only matter at the predicate-evaluation boundary.

- **Option β**: j-rig retains `GateResultEnum` locally as an enum aligned to kernel's predicate. Kernel's JSON Schema for `gate-result/v1` already constrains the decision-value enum to the same 4 strings. j-rig's local enum is a typing convenience; the source of truth remains kernel's schema. Pro: lighter kernel surface, no churn. Con: drift risk if kernel adds a 5th value (e.g., "DEFERRED") and j-rig doesn't track it.

**Recommendation**: take this to the kernel-side bead `iec-E02` cluster + a quick ISEDC seat review (it's enum-shape, not architecture-level, so probably an engineering decision rather than full council convene). For Priority 1 migration purposes, **defer this reconciliation** — j-rig retains `GateResultEnum` locally with a TODO comment referencing this inventory § 6, and the `iaj-E02b` codemod focuses on the larger duplications (`EvalSpec`, `EvidenceBundle`, `GateResultPredicate`).

---

## 7. Acceptable retention sites (allowlist seeds for `kernel-shadow-check`)

When `iah-kernel-shadow-check` (`bd_000-projects-873c`) ships, it will need an allowlist format. Seed entries this inventory recommends:

| Path                                                                                            | Reason                                                                                                      | Renewal cadence                          |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `audit-harness/tests/fixtures/gate-result.schema.json`                                          | Test fixture for emit-evidence regression suite                                                             | Re-pin on each kernel major version bump |
| `j-rig-binary-eval/packages/core/src/schemas/evidence-bundle.ts` lines 22-23 (`GateResultEnum`) | Pending § 6 reconciliation                                                                                  | Remove allowlist after § 6 resolved      |
| `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json`             | Will be replaced with pointer stub by `iel-link-schemas-to-kernel`; retention is transient until that lands | Remove allowlist when stub lands         |
| Anywhere a test fixture lives under `*/tests/fixtures/`                                         | Test data; not production code                                                                              | Per-test review                          |

The allowlist format itself is `iah-kernel-shadow-check`'s implementation detail (probably YAML or JSON with `path`, `reason`, `decision_record_ref`, `expires_at`, `owner` fields).

---

## 8. Findings + recommendations for next-session execution

### 8.1 Substantive scope of Priority 1

- **audit-harness migration: trivial.** No production-code re-definitions. Three sub-beads (`iah-E02a/b/c/d`) can compress to a single "add dep + close E02b/c with no-op evidence + run tests" PR.
- **j-rig migration: substantive.** Four kernel duplications across two files + 6+ downstream consumer files needing import updates. The largest piece of Priority 1 work.
- **intent-rollout-gate migration: deferred-by-architecture.** Under Option-A, kernel flows in through `@j-rig/rollout-gate`. `iar-consumer-migration` (`bd_000-projects-cab3`) waits on `iaj-E02` closure (kernel adoption in j-rig) AND `iaj-E03`/`iaj-E09b` (the `@j-rig/rollout-gate` workspace + publish).
- **intent-eval-lab schema repoint: medium.** One schema file replacement + Blueprint B § 7 update + glossary pointers + drift-check CI. Three of the four sub-beads are new (created this session).

### 8.2 Recommended execution order for next sessions

1. **Session N+1 (`feat/iep-convergence-p1-audit-harness` in audit-harness)** — close `iah-E02a/b/c/d` with one PR. Low risk, fast win. Demonstrates `kernel-shadow-check` clean exit on audit-harness's source tree. ~half-day.

2. **Session N+2 (`feat/iep-convergence-p1-j-rig` in j-rig-binary-eval)** — the substantive migration. Walk codemod through `eval-spec.ts` + `evidence-bundle.ts` + downstream consumers. Defer the § 6 `GateResult` enum reconciliation. Land `iaj-E02a/b/c/d` and the migration AAR in one PR. ~1-2 days.

3. **Session N+3 (`feat/iep-convergence-p5-schema-repoint` in intent-eval-lab)** — execute Priority 5 in parallel with Priority 1 migrations: `iel-link-schemas-to-kernel` replaces the schema file with a stub; `iel-link-schemas-blueprint-b` adds the kernel-canonical declaration; `iel-link-schemas-glossary` adds pointers; `iel-link-schemas-drift-ci` lands the CI gate. ~1 day.

4. **Session N+4** — Priority 2 (j-rig hardening: `iep-P2`) and Priority 3 (audit-harness hardening: `iep-P3`) can run in parallel after Priority 1 j-rig closure. Sigstore work + license drift + `.harness-hash` self-pin.

5. **Session N+5+** — Priority 4 (`iep-P4` rollout-gate M5 MVP). Depends on `iaj-E03` (`@j-rig/rollout-gate` package) being publishable. May want to bundle iar-E02 DR-002 closure first (existing iar-E02a/b/c/d sub-beads).

### 8.3 Blockers to clear before Priority 1 migration code lands

- **None for audit-harness.** Can start immediately.
- **None for j-rig.** The kernel publishes `EvalSpec`, `EvidenceBundle`, `gate-result/v1` already (v0.1.0 sigstore-attested on npm).
- **None for lab.** Same.
- For intent-rollout-gate kernel consumption: blocked on `iaj-E03` + `iaj-E09b` per the architecture lock.

### 8.4 Architectural confirmations (no contradictions found)

- Kernel exports 13 entities + GateResultV1 + sub-types per Blueprint B § 2 + § 7. ✓
- Unification thesis (DR-010 Q3) — every validator emits Evidence Bundle. **Not yet verified in practice**; Priority 1 closure is what verifies it. ✓
- Thin-shell architecture for intent-rollout-gate (Option-A from 2026-05-20 decision) — confirmed against bd state (`iar-E04` ≤200 LOC rule) and umbrella `CLAUDE.md`. ✓
- Plan-recollection errors flagged (`EvalCase`, `Provider`, `JudgeAdapter` not in kernel) — orientation finding, not a blocker. ✓

**No architecture contradictions surfaced during inventory walk.** Proceeding to bead-structure closure per user's hard constraint.

---

## 9. Source-of-truth verification trail

For audit reproducibility, the inventory was constructed by:

1. Listing `intent-eval-core/src/entities/` (14 entity files + `index.ts`) and reading `index.ts` re-exports (verified 13 of 14 are re-exported; one file is a test).
2. Listing `intent-eval-core/schemas/v1/` (15 JSON Schema files including `_common.schema.json` + `index.json`).
3. Listing `intent-eval-core/src/predicates/` (gate-result-v1.ts + test + index.ts).
4. `find` + `grep` across each consumer repo's `*.ts`, `*.js`, `*.mjs`, `*.cjs`, `*.json`, excluding `node_modules`, `dist`, `coverage`, `.git`.
5. `grep -E '"@intentsolutions/core"'` across each consumer's `package.json` and `packages/*/package.json`.
6. Spot-check of identified files (`packages/core/src/schemas/eval-spec.ts`, `evidence-bundle.ts`, `eval-contract.ts`) to confirm declaration sites and line numbers.
7. Cross-reference against bd state: `bd_000-projects-46x` (iah-E02), `bd_000-projects-7wj` (iaj-E02), `bd_000-projects-i4jh` (iel-link-schemas-to-kernel), `bd_000-projects-cab3` (iar-consumer-migration), `bd_000-projects-x6dd` (this inventory bead), plus 5 umbrellas (`iep-P1..P5`).

All findings in this document are derived from the verified file tree at commit `da1185a` on `intent-eval-lab` main (and equivalent HEADs on the other 4 sub-repos). No claims rely on memory or external recall.

---

## 10. Closure

This inventory satisfies the acceptance criteria for `bd_000-projects-x6dd` (iep-kernel-shadow-inventory):

- [x] Inventory doc filed at `intent-eval-lab/000-docs/016-RR-LAND-kernel-shadow-inventory-2026-05-20.md`
- [x] Per-repo per-type breakdown complete (§ 4)
- [x] Migration target list with file paths derived (§ 5)

**Recommend closing `bd_000-projects-x6dd` with this document as evidence** once the user reviews. Closure unblocks the four parallel Priority 1 migrations (`iah-E02*`, `iaj-E02*`, `iel-link-schemas-to-kernel`, `iar-consumer-migration`).

— Jeremy Longshore
intentsolutions.io
````
