---
date: 2026-06-06
authors:
  - Jeremy Longshore (Intent Solutions)
status: PROPOSAL / RFC (NON-NORMATIVE)
governance: >
  The deep build this RFC proposes is a Class-1 ISEDC change (canonical-domain entity
  amendment, Blueprint B § 2.2) and is bandwidth-gated per DR-010 § 13.5. This document
  PROPOSES; it does not amend any normative doc, mutate any entity, or commit any build.
filing_standard: Document Filing Standard v4.3
companion:
  - 042-RR-LAND-prompt-and-context-eval-landscape-2026-06-06.md (the cited landscape this recommendation rests on)
binds_against:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — § 2.1 repo roles, § 3 anti-goals)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — § 2.1 EvalSpec, § 2.2 EvalRun, § 2.3 MatcherMap)
  - 014-DR-GLOS-canonical-glossary.md (canonical glossary — § 4 MM vocabulary, § 6 predicate URIs)
  - 027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md (AC-7, AC-13 RefinerStrategy)
  - 028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md (DR-028)
epic: iel-prompt-context-eval
---

# RFC — Generalizing the Eval Unit from "Skill" to "Intent-Bearing Artifact"

> **STATUS: NON-NORMATIVE PROPOSAL.** This RFC recommends a direction and names the gate it
> must pass. It changes nothing on its own. The recommended deep build (a kernel `EvalTarget`
> union + an `EvalRun.eval_target` field) is a **Class-1 ISEDC** trigger — it amends the
> canonical-domain model in Blueprint B § 2.2 (DR-010 § 7 Q6: "canonical-domain schema
> surface"). Realization is also **bandwidth-gated** per DR-010 § 13.5. Nothing here is
> implemented; this is intent-eval-lab doing exactly its chartered job: authoring methodology
> ahead of code (Blueprint A § 2.1).

---

## 1. The question

> _Intent Solutions' niche is agent-native evaluation, and the platform is literally named
> the **Intent Eval Platform** — yet it evaluates exactly one kind of unit, a `SKILL.md`. The
> industry has moved from prompt engineering to context engineering. Where does prompt + context
> evaluation fit, and should the platform name a more general unit-under-test?_

This RFC answers: **yes, eventually — and the move is a renaming at the contract layer, not a
new engine.** The evidence substrate, the judge layer, and the matcher layer are already
target-agnostic. Only two fields hardcode "skill." The recommendation is the **Intent reframe**:
`EvalTarget = skill | prompt | context-template | agent`, where _skill is intent-type #1_ and
prompt/context-template are #2/#3.

---

## 2. Mapping the ecosystem's eval surfaces onto the landscape

### 2.1 A SKILL.md is already a packaged prompt + context artifact

Per the landscape doc § 2, the 2025 industry consensus is that prompt engineering is a
_subset_ of context engineering [042 § 2]. A Claude Code Skill bundles **both**: an
instruction prompt (the SKILL.md body) **and** the context scaffolding it injects (tool
descriptions, bundled reference files, frontmatter triggers). The platform is therefore
already evaluating _one point_ in the prompt→context space. It has not generalized the _name_.

### 2.2 j-rig's 7 layers already cover much of the behavioral "topline"

| j-rig layer (`j-rig-binary-eval` CLAUDE.md)                       | Landscape analogue (042)              | Already target-agnostic?                          |
| ----------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------- |
| L1 Spec (YAML eval contracts, criteria)                           | EvalSpec / assertion gates (§ 3.1)    | **No** — `eval-spec.ts` hardcodes `skill_name`    |
| L2 Execution (trigger/functional/regression/adversarial/baseline) | red-team + golden datasets (§ 3.1)    | mechanism-agnostic; inputs are skill-shaped today |
| L3 Observation (outputs, cost, latency)                           | tracing (§ 3.2)                       | yes                                               |
| L4 Judgment (deterministic first, LLM-judge second)               | LLM-as-judge / G-Eval (§ 3.1)         | **yes** — judges score outputs, not "skills"      |
| L5 Optimization (failure clustering, one-change)                  | DSPy-class optimization (§ 5)         | yes (see § 5 here)                                |
| L6 Evidence (persistence, launch reports)                         | Evidence Bundle / attestation (§ 3.3) | **yes** — bundles reference runs, not skills      |
| L7 CLI/CI/API (PR gate)                                           | promptfoo/Braintrust gates (§ 3.2)    | yes                                               |

Five of seven layers are already agnostic to _what_ is under test. The skill-specificity lives
in L1 (the spec) and the kernel FK — exactly where the reframe applies.

---

## 3. The gap, named precisely

Two — and only two — load-bearing places hardcode "skill" as the unit-under-test:

1. **Kernel `EvalRun` (Blueprint B § 2.2).** `EvalRun` carries
   `readonly skill_snapshot_id: Uuidv7;  // FK → SkillSnapshot.id`
   (`intent-eval-core/src/entities/EvalRun.ts:88-89`). The unit-under-test is _typed as a
   SkillSnapshot FK_. There is no `Prompt` or `ContextTemplate` entity in the 13-entity model
   (glossary § 2), so there is nothing else an `EvalRun` _could_ point at.

2. **j-rig `EvalSpec`.** The behavioral harness's spec hardcodes the unit by name:
   `skill_name: z.string()…describe("Name of the skill being evaluated")`
   (`j-rig-binary-eval/packages/core/src/schemas/eval-spec.ts:33-37`), and even the model axis
   is a closed `ModelTarget = z.enum(["haiku","sonnet","opus"])` (ibid. line 8).

**What is already target-agnostic (the good news):**

- **`MatcherMap` (Blueprint B § 2.3)** declares "for inputs that look like X, expected behavior
  is Y" — it never mentions skills. Input-pattern → expected-behavior is artifact-neutral.
- **`JudgeDecision` (Blueprint B § 2.5; `JudgeDecision.ts`)** references `matcher_map_id` and
  `eval_run_id` — it judges a matching event, not "a skill."
- **`EvidenceBundle` (Blueprint B § 2.4)** references `eval_run_id` and is the platform's
  lingua franca; it is intrinsically agnostic to what produced the run.
- **`EvalSpec` (kernel, `EvalSpec.ts`)** targets snapshots by **content hash**
  (`expected_artifacts: readonly Sha256[]`), not by a skill-typed field — so the kernel
  EvalSpec is _already closer to target-agnostic than j-rig's_.

So the eval **engine** is agnostic; only the **declared subject** is skill-typed. The reframe
touches `EvalRun` + the j-rig `EvalSpec` and adds entity types — it does **not** touch the
judge, matcher, or evidence layers.

---

## 4. Recommendation — the Intent reframe

### 4.1 The union

```text
EvalTarget = SkillSnapshot          (intent-type #1 — exists today)
           | PromptSnapshot         (intent-type #2 — proposed)
           | ContextTemplateSnapshot (intent-type #3 — proposed)
           | AgentSnapshot          (intent-type #4 — proposed, lowest priority)
```

All four are **intent-bearing artifacts**: a frozen, content-addressed thing that encodes an
intent and can be evaluated for whether it realizes that intent. `SkillSnapshot` already has
the right shape (SHA-pinned source + deps + config, glossary § 2.9); the new members mirror it.

### 4.2 The single field change at the contract layer

- `EvalRun.skill_snapshot_id: Uuidv7` → `EvalRun.eval_target: EvalTargetRef`, where
  `EvalTargetRef = { kind: 'skill' | 'prompt' | 'context-template' | 'agent'; snapshot_id: Uuidv7 }`.
- j-rig `EvalSpec.skill_name` → a discriminated `target` object (kind + name).
- **`MatcherMap`, `JudgeDecision`, `EvidenceBundle`, `RuntimeReceipt`, `SessionTrace`,
  `CostRecord` stay as-is.** They are already target-agnostic (§ 3).

This is why the move is a _renaming exercise_, not a new engine: one FK becomes a tagged
reference; one new entity-family is added; everything downstream of the run is untouched.

### 4.3 New metrics map onto MatcherMap, not onto a new subsystem

The landscape's prompt/context metrics (RAGAS faithfulness/context-precision/context-recall;
RULER long-context; lost-in-the-middle; context-rot — 042 § 4.2) are **expected-behavior
declarations** — exactly what `MatcherMap` already models. They become new MatcherMap _classes_
in proposed namespaces:

- **MM-P\*** — prompt-eval matcher classes (e.g., instruction-adherence, output-schema
  conformance, injection-resistance).
- **MM-C\*** — context-eval matcher classes (e.g., faithfulness-to-context, context-precision,
  needle-retrieval, context-rot-resistance).

> **Governance note on MM-P\*/MM-C\*.** The MM-1..MM-6 identifiers are immutable and MM-7+
> admission is gated by the `CONTRIBUTING-failure-shape.md` path (DR-004 S1Q3; glossary § 4).
> Introducing MM-P\*/MM-C\* namespaces is therefore itself a governance act — either an
> extension of the Intentional Mapping vocabulary via the MM-7+ admission criteria, or a new
> sibling namespace decided by ISEDC. This RFC **proposes the naming**; it does not admit it.

### 4.4 Realization order

1. **Now (this RFC + the spec skeleton):** lab methodology only. Author
   `specs/prompt-evaluation/v0.1.0-draft/SPEC.md` (skeleton; B3) describing target types,
   matcher families, and the failure-shape namespace. No code.
2. **Later (gated):** the kernel `EvalTarget` union + `EvalRun.eval_target` migration in
   `intent-eval-core`, then the j-rig `EvalSpec` upgrade. Class-1 ISEDC + bandwidth gate (§ 7).

---

## 5. Where the Python prompt-code tools fit (DSPy et al.)

### 5.1 The Skill Refiner is already a DSPy-class optimizer

Per the landscape § 5, DSPy/TextGrad/GEPA represent "prompt engineering as compilation":
declare a metric, let an optimizer search the prompt space. **Intent Solutions already ships a
member of this school** — the **Skill Refiner** (plan 027 v5; DR-028) is a compile-against-a-metric
optimizer specialized to `SKILL.md`, accepting only on the strict-improvement-on-Pareto-dominant
predicate (DR-028 P0-RATIFY-1). The difference from generic DSPy: the Refiner's value is the
**acceptance gate**, not the search.

### 5.2 DSPy/TextGrad/GEPA are pluggable RefinerStrategy backends — a seam, not a dependency

DR-028 ratified **AC-7** (mechanism swappable, gate durable) and **AC-13** (the
`RefinerStrategy` interface, with reference impls `NaiveInContext` + `SkillOptStyle`). That
interface is exactly the seam where a DSPy-class optimizer plugs in:

```text
RefinerStrategy  ← NaiveInContext        (ratified reference impl)
                 ← SkillOptStyle          (ratified reference impl)
                 ← DSPyStrategy           (FUTURE — wraps DSPy/GEPA behind the same gate)
                 ← TextGradStrategy       (FUTURE)
```

The acceptance gate (strict-improvement predicate) is durable across whichever backend
proposes the edit. So **DSPy is named here as an integration seam (`DSPyStrategy`), not a
dependency to add now.** Adding it today would violate the bandwidth gate and the
no-premature-productization rule (lab CLAUDE.md § 4).

### 5.3 Construction libraries stay out of the eval kernel

Templating (LangChain `PromptTemplate`, Jinja2) and structured-output libraries (Instructor,
Outlines, Guidance, BAML — 042 § 5.2–5.3) are how an `EvalTarget` of kind `prompt` or
`context-template` would be **constructed**, not **evaluated**. They belong on the _authoring_
side, never inside the eval kernel — mirroring the orchestrator-of-tools principle by which
`audit-harness scan` shells out to `gitleaks`/RAGAS rather than reimplementing them. The kernel
stays a contracts kernel (intent-eval-core CLAUDE.md anti-goals: NOT a runtime, NOT a judge).

---

## 6. Predicate names — PROPOSED, not reserved, not declared

Two predicate names are _proposed_ for the eventual signed-evidence surface of the new target
types:

- `evals.intentsolutions.io/prompt-eval/v1`
- `evals.intentsolutions.io/context-eval/v1`

**Constraints honored:**

- **Host is `evals.intentsolutions.io` only.** Never `labs.intentsolutions.io` (CISO binding,
  glossary § 8; DR-004 Q1 + DR-010 § 10). `labs.` may host methodology/blog content but never a
  predicate URI.
- **Proposed ≠ reserved ≠ declared.** Per DR-010 § 7 Q6, "new predicate URI subtype
  reservation" is itself a **Class-1 ISEDC** act. This RFC therefore _proposes_ the names; it
  does **not** reserve them and does **not** declare a normative SPEC or emit any
  `predicateType` anywhere. No code, schema, or attestation carries these strings (verifiable
  by grep — see the plan's verification gate). They sit in the same "recognized but not yet
  reserved" status the glossary already uses for `harness-experiment/v1` / `cache-decision/v1`
  (glossary § 6 "Deferred predicate types").

---

## 7. Governance + realization gating

| Step                                                            | Gate                                                                       | Authority                 |
| --------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------- |
| This RFC + spec skeleton + glossary proposed-terms entry        | None (lab methodology authoring) — additive, non-normative                 | Blueprint A § 2.1         |
| Reserving `prompt-eval/v1` / `context-eval/v1`                  | **Class-1 ISEDC** (new predicate URI subtype reservation)                  | DR-010 § 7 Q6             |
| Adding `EvalTarget` union + `EvalRun.eval_target` to the kernel | **Class-1 ISEDC** (canonical-domain entity amendment, Blueprint B § 2.2)   | DR-010 § 7 Q6             |
| Admitting MM-P\*/MM-C\* matcher namespaces                      | MM-7+ admission path or ISEDC namespace decision                           | DR-004 S1Q3; glossary § 4 |
| Actually building any of the above                              | **Bandwidth gate** (Phase B is bandwidth-gated, not customer-signal-gated) | DR-010 § 13.5             |

**Anti-goals honored (Blueprint A § 3):** no new repo; no entity mutation; no code; no new
sub-platform initiation (glossary § 8 "No new platform initiation in next 6 months"). This is
methodology authoring in the repo chartered for it.

---

## 8. Alternatives considered (not chosen)

1. **Tier-2 standalone "prompt eval" project.** Spin prompt/context eval out as an independent
   research project (like `semantic-flux`). _Rejected as the primary path_ because the platform's
   whole thesis is unification via Evidence Bundle (DR-010 Q3); a standalone would _re-implement_
   the agnostic substrate it already owns. Recorded as an alternative, not chosen.
2. **j-rig-only extension** (add `target_kind` to j-rig's `EvalSpec`, skip the kernel). _Rejected
   as the primary path_ because it would let the behavioral harness diverge from the canonical
   domain model — the exact drift DR-018 reconciled. The kernel is the source of truth; the
   target type belongs there.
3. **Do nothing / keep skill-only.** Viable indefinitely — skill eval is a real, shippable
   wedge. The reframe is an _option to hold_, not an urgent build. This RFC's recommendation is
   "author the methodology now, hold the build behind the gate," not "build now."

---

## 9. Open questions for a future ISEDC session

1. Is `EvalTarget` a discriminated union over snapshot entities, or a single polymorphic
   `IntentArtifactSnapshot` with a `kind` field? (Mirrors the DR-028 T1 SkillVersion-vs-Snapshot
   discriminator debate.)
2. Does `agent` belong in v1 of the union, or is it deferred (agents compose many
   prompts/contexts and may warrant their own model)?
3. Do MM-P\*/MM-C\* enter via the MM-7+ path, or as a parallel namespace with its own
   admission criteria?
4. Sequencing against the Skill Refiner: does `DSPyStrategy` (§ 5.2) land before or after the
   `EvalTarget` union? (They are independent; either order works.)

---

_Proposal / RFC, non-normative. Author: Jeremy Longshore (Intent Solutions). 2026-06-06._
_Comments via GitHub issues on `jeremylongshore/intent-eval-lab`._
