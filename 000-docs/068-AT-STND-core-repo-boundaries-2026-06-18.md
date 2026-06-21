---
title: Core Repo Boundaries — what each IEP repo owns, what crosses the Evidence Bundle seam, per-repo anti-goals
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: Blueprint A § 2.1 (5-repo taxonomy, DR-010 Q1=A)
inherits_from:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — the constitution)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — kernel + Evidence Bundle contracts)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E13
bead: bd_000-projects-or1s
filing_standard: Document Filing Standard v4.3
related_docs:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — § 2.1 taxonomy this doc derives from)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — § 7 Evidence Bundle predicate contracts)
  - 013-AT-SPEC-repo-blueprint-template.md (Blueprint C — per-repo blueprint scope-boundaries section)
  - 014-DR-GLOS-canonical-glossary.md (terminology source of truth)
  - 069-DR-STND-state-labeling-standard-2026-06-18.md (scope-element labels)
related_drs:
  - 010-AT-DECR (DR-010 — Q1=A single converged platform; Q3 unification thesis BINDING)
  - 018-AT-DECR (DR-018 — kernel as wire-format authority; @j-rig/* v2.0.0)
---

> **State label: NORMATIVE.** Binds the repo-boundary contract for all five IEP repos.
> Derives from Blueprint A § 2.1; on any conflict, Blueprint A wins per its § 0.

# Core Repo Boundaries

**Beads:** `bd_000-projects-or1s` (iel-E13a) under epic `bd_000-projects-7gs` (iel-E13).
Paired with the kernel-side ownership work (iec-E11).

## 0. What this standard is

Blueprint A (`011-AT-ARCH`) § 2.1 names the five repositories of the Intent Eval
Platform and assigns each a one-line role. This standard is the **operational
expansion** of that taxonomy: for each repo it fixes (a) what the repo **owns**, (b)
what it **must not own**, and (c) the precise contract that **crosses the Evidence
Bundle seam** between repos. It exists so that a contributor opening any repo can tell,
without re-deriving the architecture, whether a proposed change belongs there or
belongs in a sibling repo.

This document **derives from and does not override** Blueprint A. Where this document
and Blueprint A § 2.1 disagree, Blueprint A wins (Blueprint A § 0). Where this document
and Blueprint B § 7 disagree on the Evidence Bundle contract, Blueprint B wins. The
13-entity domain model and the `gate-result/v1` predicate body are owned by Blueprint B;
this standard cites them and never re-specifies them.

Terms used here — Evidence Bundle, predicate URI, kernel, Rollout Gate, harness, gate —
are defined in the Canonical Glossary (`014-DR-GLOS`). This standard does not redefine them.

## 1. Scope-element labels

Per the State-Labeling Standard (`069-DR-STND`) § 1, the per-capability labels used in
this document are a closed set, distinct from document-lifecycle labels:

| Label          | Meaning for a repo responsibility / capability                              |
| -------------- | --------------------------------------------------------------------------- |
| `CURRENT`      | Owned and shipping today in the named repo.                                 |
| `PLANNED`      | Committed for a named repo but not yet built; the boundary is reserved now. |
| `EXPERIMENTAL` | Present but behind a `v0.x` / staging gate; the boundary may still move.    |
| `DEFERRED`     | Recognized as belonging to a repo but explicitly not yet scheduled.         |
| `REJECTED`     | Explicitly disclaimed — the repo MUST NOT take this on (an anti-goal).      |

A capability's label is orthogonal to its document's lifecycle label. A `NORMATIVE`
document (this one) can mark a capability `PLANNED`.

## 2. The Evidence Bundle seam — the one coupling

There is exactly **one** architectural coupling between the five repos, and it is the
**Evidence Bundle schema** (Blueprint A § 2.1: "The coupling lives at the schema layer;
everything else is per-repo."). No monorepo, no shared build system, no shared CI.

What crosses the seam is **Evidence Bundle rows** — in-toto Statement v1 documents
carrying a predicate URI (`gate-result/v1` et al.), DSSE-wrapped, defined canonically by
the kernel schema (Blueprint B § 7.0). The seam's authority chain, per DR-018 Option
α-minus and Blueprint B § 7.0:

- **The kernel (`intent-eval-core`) owns the wire format.** The canonical JSON Schema
  for every predicate body lives at `@intentsolutions/core/schemas/v1/<predicate>.schema.json`.
  On any disagreement between a consumer's local shape and the kernel schema, the kernel
  schema wins.
- **Producers emit; consumers read; neither re-specifies.** A gate emitter (audit-harness)
  or a behavioral-eval harness (j-rig) produces rows against the kernel contract. The
  Rollout Gate logic consumes them. None of them owns the schema — the kernel does.
- **Row independence holds across the seam** (Blueprint B § 7.1): a row is independently
  verifiable; bundles are unioned, not joined.

Anything that is _not_ an Evidence Bundle row does **not** cross the seam. Internal types,
helper utilities, CLI surfaces, dashboards, and test fixtures stay inside their repo. A
change that requires two repos to agree on something other than the Evidence Bundle
schema is a design smell — resolve it at the schema layer or keep it inside one repo.

## 3. Per-repo boundary contracts

The five repos and their bead prefixes are fixed by Blueprint A § 2.1. The role lines
below quote that section; the OWNS / MUST-NOT-OWN / CROSSES-THE-SEAM rows are this
standard's operational expansion.

### 3.1 `intent-eval-core` (kernel) — prefix `iec-`

Role (Blueprint A § 2.1): _Canonical contracts kernel — types, schemas, lifecycle state
machines, replay semantics, evidence semantics, failure taxonomy, UUID/event standards.
**No execution, no judges, no deployment logic.** Pure types._

|                               |                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OWNS** (`CURRENT`)          | The 13-entity domain model (Blueprint B § 2); JSON Schemas + codegen'd Zod/Pydantic bindings; the `gate-result/v1` predicate body schema; lifecycle state machines; replay-fidelity (RF-N) declarations; UUIDv7 + OTel-attribute naming authority; the cross-field invariants for Evidence Bundle rows. `PLANNED`: `EvidenceBundlePayload` + `evidence-bundle-payload/v1` (kernel v0.2.0, iec-E12). |
| **MUST NOT OWN** (`REJECTED`) | Any execution of an evaluation, any judge logic, any deployment/Action code, any provider adapter, any CLI that _runs_ a gate. The kernel is imported by everything and depends on no ecosystem repo.                                                                                                                                                                                               |
| **CROSSES THE SEAM**          | The kernel _defines_ the seam. It exports the schemas every other repo validates against. It emits no rows itself.                                                                                                                                                                                                                                                                                  |

### 3.2 `intent-eval-lab` (methodology) — prefix `iel-`

Role (Blueprint A § 2.1): _Methodology + specification authoring — Blueprints A/B/C live
here, canonical glossary lives here, normative SPEC.md modules live here under `specs/`.
Sandbox for experiments. Public Decision Record archive._

|                               |                                                                                                                                                                                                                                                                                                                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **OWNS** (`CURRENT`)          | Blueprints A/B/C; the Canonical Glossary; Decision Records; the predicate-type registry (`specs/PREDICATE-TYPES.md`, Blueprint B § 7.2); normative SPEC.md prose; standards-track RFCs; this boundary standard. `PLANNED`/`EXPERIMENTAL`: per-class spec modules under `specs/` (mcp-plugin-observability, prompt-evaluation, etc.). |
| **MUST NOT OWN** (`REJECTED`) | Normative machine-readable schema content for any predicate body — that is the kernel's (Blueprint B § 7.0; lab `specs/.../schema/` holds only `$ref` redirect stubs, enforced by `schema-drift.yml`). The lab also does not ship executable platform code; it is the only repo that depends on no other ecosystem repo.             |
| **CROSSES THE SEAM**          | The lab feeds **normative specifications** into the kernel as JSON Schema additions (Blueprint A § 2.2). It emits no Evidence Bundle rows in production; its own test surface MAY emit rows for self-application (Blueprint C § "self-application," iel-E05).                                                                        |

### 3.3 `audit-harness` — prefix `iah-`

Role (Blueprint A § 2.1): _Deterministic gates — escape-scan, CRAP, architecture,
harness-hash, bias-count, gherkin-lint. Already polyglot (Node CLI + shell + Python).
Emits Evidence Bundle gate-result rows._

|                               |                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OWNS** (`CURRENT`)          | The deterministic gate implementations; the polyglot CLI dispatcher; hash-pinning (`.harness-hash`); the gate logic that decides PASS/FAIL/ADVISORY for each deterministic check. `PLANNED`: the `emit-evidence` subcommand (iah-E04) — the second prospective Evidence Bundle emitter named in DR-018 § 6.4 binding precondition #1. `DEFERRED`: production-Rekor signing (iah-E06, gated on DNSSEC + CAA + compatibility policy). |
| **MUST NOT OWN** (`REJECTED`) | The Evidence Bundle schema (kernel owns it); behavioral / LLM-as-judge evaluation (j-rig owns it); ship/no-ship promotion decisions (the Rollout Gate owns those). audit-harness produces deterministic gate-result rows; it does not decide rollouts.                                                                                                                                                                              |
| **CROSSES THE SEAM**          | **Emits** `gate-result/v1` rows against the kernel schema. Each row's subject `name` matches its predicate `gate_id` per Blueprint B § 7.3.                                                                                                                                                                                                                                                                                         |

### 3.4 `j-rig-skill-binary-eval` — prefix `iaj-`

Role (Blueprint A § 2.1): _Behavioral evaluation harness + Rollout Gate decision logic +
provider adapters + regression packs. TS pnpm monorepo. Emits + consumes Evidence Bundle
rows. The decision engine lives here._
(GH-canonical name `j-rig-skill-binary-eval`; local FS dir `j-rig-binary-eval`.)

|                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **OWNS** (`CURRENT`)          | Behavioral / binary skill evaluation; provider adapters; regression packs; the **Rollout Gate decision logic** as the workspace package `@j-rig/rollout-gate`; the eval-verdict / runtime-receipt emission. `CURRENT` per DR-018: re-exports kernel `GateResultV1` (j-rig `@2.0.0+`); retains a behavioral secondary cross-field check for one major version cycle. `PLANNED`: `@j-rig/refiner-core` + `@j-rig/refiner` (Skill Refiner, DR-028). |
| **MUST NOT OWN** (`REJECTED`) | The canonical predicate-body schema (kernel owns it; j-rig re-exports, never re-specifies — DR-018 Q2). The GitHub Action _shell_ (that is intent-rollout-gate). Deterministic static gates (those are audit-harness).                                                                                                                                                                                                                           |
| **CROSSES THE SEAM**          | **Emits** Evidence Bundle rows (`eval-verdict/v1`, `runtime-receipt/v1`, and conformant `gate-result/v1`) and **consumes** rows to drive the Rollout Gate decision. The decision logic is the seam's primary _consumer_.                                                                                                                                                                                                                         |

### 3.5 `intent-rollout-gate` — prefix `iar-`

Role (Blueprint A § 2.1): _**Thin GitHub Action shell** that delegates all decision logic
to `@j-rig/rollout-gate`._

|                                     |                                                                                                                                                                                                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OWNS** (`CURRENT`/`EXPERIMENTAL`) | The Action surface only: `action.yml` + `dist/index.js` + the npm-publishable Action variant. The shell parses inputs, calls `@j-rig/rollout-gate`, and surfaces the verdict as Action outputs / exit codes. The M5.1 TS runtime is `EXPERIMENTAL` (`v0.x`).                      |
| **MUST NOT OWN** (`REJECTED`)       | **Any decision logic.** All ship/no-ship reasoning lives in `@j-rig/rollout-gate`. If a behavior change requires editing decision logic, the change belongs in j-rig, not here. This anti-goal is the repo's entire reason to exist as a separate thin shell (Blueprint A § 2.1). |
| **CROSSES THE SEAM**                | **Consumes** an Evidence Bundle + a `tests/TESTING.md`-shaped policy via `@j-rig/rollout-gate` and surfaces the decision. It does not emit rows of its own; the decision it surfaces was computed by j-rig logic against kernel-defined rows.                                     |

## 4. Boundary decision procedure

When a contributor is unsure which repo a change belongs in, apply this in order:

1. **Is it a type, schema, invariant, or naming authority?** → `intent-eval-core`.
2. **Is it methodology, a spec, a glossary entry, a Decision Record, or the predicate
   registry?** → `intent-eval-lab`.
3. **Is it a deterministic, reproducible check (no LLM judgment)?** → `audit-harness`.
4. **Is it behavioral evaluation, a provider adapter, a regression pack, or
   ship/no-ship decision logic?** → `j-rig-skill-binary-eval`.
5. **Is it the GitHub Action input/output surface only, with no decision logic?** →
   `intent-rollout-gate`.

If a change seems to fit two repos, it almost always means a type or schema needs to move
to the kernel (step 1) so both repos depend on it rather than duplicating it. Duplicated
types across repos are a Blueprint A principle-10 ("schema is canon") violation and a CI
drift failure, not a design choice.

## 5. Anti-goals summary (the `REJECTED` rows, consolidated)

| Repo                      | Must NOT own                                                                     |
| ------------------------- | -------------------------------------------------------------------------------- |
| `intent-eval-core`        | Execution, judges, deployment/Action code, provider adapters, gate-running CLIs. |
| `intent-eval-lab`         | Normative machine-readable predicate schemas; executable platform code.          |
| `audit-harness`           | The Evidence Bundle schema; behavioral/LLM-as-judge eval; rollout decisions.     |
| `j-rig-skill-binary-eval` | The canonical predicate schema; the Action shell; deterministic static gates.    |
| `intent-rollout-gate`     | Any decision logic whatsoever.                                                   |

These anti-goals are binding under Blueprint A § 2.1 and the "schema is canon" principle
(Blueprint A § 1.2 principle 10). A pull request that crosses one of these lines is out of
compliance and routes through governance (Blueprint A § 2.3), not a silent merge.

## 6. Relationship to per-repo blueprints

Blueprint C (`013-AT-SPEC`) requires each repo to author its own per-repo blueprint with
an explicit scope-boundaries section (in / out / deferred / anti-goals). This standard is
the **cross-repo** view that each per-repo blueprint's scope section MUST be consistent
with. If a per-repo blueprint's anti-goals contradict the `REJECTED` rows in § 5, the
contradiction is a defect resolved in favor of this standard (which derives directly from
Blueprint A).

## 7. Cross-references

- 5-repo taxonomy this standard expands: Blueprint A (`011-AT-ARCH`) § 2.1, § 2.2.
- Evidence Bundle predicate contracts: Blueprint B (`012-AT-ARCH`) § 7.
- Schema authority (kernel wins): Blueprint B § 7.0; DR-018 (`018-AT-DECR`) § 6.4.
- Predicate-type registry: `specs/PREDICATE-TYPES.md` (Blueprint B § 7.2).
- Scope-element labels: `069-DR-STND-state-labeling-standard-2026-06-18.md` § 1.
- Per-repo blueprint scope-boundaries template: Blueprint C (`013-AT-SPEC`).
