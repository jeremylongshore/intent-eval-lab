# Tier-Bridge Spec — v0.1.0-draft

> **Status: NORMATIVE DRAFT.** This specification is the single source of truth for how a
> skill's **static tiers** (standard / marketplace grading + the static production gate) and
> its **behavioral tier** (the `j-rig` execution-based eval) compose into one promotion
> decision. Both tools reference THIS document for the composition rules; neither tool
> redefines them. Where a tool's own docs and this spec disagree about composition, this spec
> wins.
>
> **Scope of authority.** This bridge governs only the _relationship between_ the tiers — the
> ordering, the fail-fast boundary, the verdict-combination algebra, and the Evidence Bundle
> each tier emits. It does **not** define the grading rubric (that is the validator's), the
> static-gate check set (that is the validator's Tier 2), or the behavioral layer set (that is
> `taxonomy` / `j-rig`'s). Those are referenced, not restated.
>
> **Authority precedence.** Where this spec touches the Evidence Bundle envelope, the
> `gate-result/v1` predicate, signing, or the kernel domain model, the canonical
> [`../../evidence-bundle/v0.1.0-draft/SPEC.md`](../../evidence-bundle/v0.1.0-draft/SPEC.md)
> and the kernel `@intentsolutions/core` schema win on conflict (Blueprint B § 7.0). Where it
> touches ecosystem taxonomy or repo roles, [Blueprint A](../../../000-docs/011-AT-ARCH-ecosystem-master-blueprint.md)
> § 2.1 wins. Where it touches platform terminology, the
> [canonical glossary](../../../000-docs/014-DR-GLOS-canonical-glossary.md) wins.

## 1. Purpose

A skill is promoted to production (or to a marketplace listing) only after passing a series of
quality checks. Those checks fall into two families with fundamentally different cost,
determinism, and failure semantics:

- **Static checks** read the artifact without executing it. They are fast (seconds), free,
  and deterministic: the same SKILL.md byte-for-byte always produces the same verdict. They
  answer _"is this artifact well-formed, complete, and free of obvious production hazards?"_
- **Behavioral checks** execute the skill against a model matrix and judge the resulting
  behavior. They are slow (minutes), cost real API spend, and are probabilistic: the same
  SKILL.md can produce different verdicts across runs because model sampling is stochastic.
  They answer _"does this skill actually behave correctly when invoked?"_

Two tools cover these families:

- The **static validator** (`validate-skillmd`) runs the static checks. Its **Tier 1** grades
  the artifact against the Intent Solutions rubric (standard or marketplace), and its **Tier
  2** is a static production gate (allowed-tools accuracy, auth protocol, dead code, tool
  safety, orchestration bounds). Both are static (glossary: a deterministic validator returns
  PASS/FAIL mechanically).
- The **behavioral harness** (`j-rig`) runs the execution-based eval. This is the validator's
  **Tier 3** — opt-in, slow, costed.

Without a bridge, the two tools have overlapping but unstated relationships: which runs first,
what a static failure means for whether the behavioral eval should even run, and how two
heterogeneous verdicts (one deterministic, one probabilistic) combine into a single
ship / no-ship answer. This spec defines that bridge so a promotion decision is reproducible
and the two tools' outputs are composable — not two disconnected reports a human must
reconcile by hand.

## 2. Scope

### 2.1 In scope (v0.1.0-draft)

| Concern                                                                        | Where |
| ------------------------------------------------------------------------------ | ----- |
| The three tiers + the static/behavioral split                                  | § 4   |
| Tier ordering + the fail-fast boundary                                         | § 5   |
| The verdict-combination algebra (how tier verdicts compose into one decision)  | § 6   |
| The Evidence Bundle each tier emits + how a bundle carries multi-tier evidence | § 7   |
| Determinism + reproducibility obligations per tier                             | § 8   |
| The unavailable-behavioral-tier rule (Tier 3 absent ≠ failure)                 | § 9   |
| Conformance fixtures (the composition decision table proven by example)        | § 10  |

### 2.2 Out of scope (v0.1.0-draft)

- **The grading rubric.** The 100-point rubric, the 8-field marketplace required-field set,
  and the standard-vs-marketplace tier boundary are the validator's concern. This spec
  references the rubric's _verdict_ (a Tier 1 PASS/FAIL/grade) but does not define how the
  grade is computed.
- **The Tier 2 static-check set.** The five static production checks are the validator's. This
  spec references their _aggregate verdict_ (GREEN / YELLOW / RED) but does not enumerate or
  redefine the checks.
- **The behavioral layer set.** The behavioral tier's internal layers (trigger quality,
  functional quality, regression, baseline value, model variance, rollout safety, cost /
  latency) are the harness's concern — and are distinct from the 7-layer _testing taxonomy_
  (see § 4.4 disambiguation). This spec references the behavioral tier's _aggregate verdict_
  (GREEN / RED / SKIPPED), not its layers.
- **Predicate body schemas.** The `gate-result/v1` body and any behavioral-eval predicate
  body are kernel concerns (Blueprint B § 7.0). This spec references which predicate each tier
  emits under; it does not define the bodies.
- **Non-skill eval targets.** Prompts and context templates as eval targets are covered by the
  [`prompt-evaluation`](../../prompt-evaluation/v0.1.0-draft/SPEC.md) module. This bridge
  governs the skill artifact only.

## 3. Conformance keywords

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY** are used per
[RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) /
[RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174).

A **promotion run** is a single evaluation of one skill artifact that produces one final
promotion verdict. A promotion run is the unit this spec governs.

## 4. The three tiers

### 4.1 Tier 1 — standard / marketplace grading (STATIC)

Tier 1 grades the SKILL.md against the rubric. Its output is one of:

- a **grade** (numeric, against the rubric), and
- a **gate verdict** for the requested mode: `PASS` (meets the required-field floor for the
  mode) or `FAIL` (a required field is missing at the requested tier).

Tier 1 is **static**: it reads frontmatter + body and returns a mechanical verdict (glossary,
"a deterministic validator … that returns PASS or FAIL mechanically"). The same bytes always
grade the same. Tier 1 is **always run** in a promotion run.

### 4.2 Tier 2 — static production gate (STATIC)

Tier 2 is the static production gate: a fixed set of binary production-hazard checks
(allowed-tools accuracy, auth protocol, dead code, tool safety, orchestration bounds). Its
aggregate verdict is one of:

- `GREEN` — all checks pass.
- `YELLOW` — only warnings; no blocking failure.
- `RED` — at least one blocking failure.

Tier 2 is **static** and **always run** alongside Tier 1. Tier 2 is the production-hazard floor
that Tier 1's _quality_ grade does not cover: a skill can grade well on the rubric and still
ship a production hazard (e.g., an undeclared tool), which Tier 2 catches.

### 4.3 Tier 3 — behavioral eval (BEHAVIORAL, opt-in)

Tier 3 is the execution-based behavioral eval run by `j-rig` (glossary: `j-rig` = "behavioral
evaluation, TypeScript, emits + consumes Evidence Bundle rows"). It executes the skill against
a model matrix and judges the resulting behavior. Its aggregate verdict is one of:

- `GREEN` — the behavioral eval passed across the evaluated model matrix.
- `RED` — the behavioral eval surfaced a blocking failure (which layer / which model is in the
  evidence, not in this aggregate).
- `SKIPPED` — the behavioral harness was not available or not requested (§ 9).

Tier 3 is **behavioral**: it is slow, costs API spend, and is **probabilistic** (model
sampling is stochastic). Tier 3 is **opt-in** — it runs only when the promotion run explicitly
requests it (the validator's `--thorough`). A default promotion run is Tier 1 + Tier 2 only.

### 4.4 Disambiguation — two different "7-layer" things

The behavioral tier's _internal_ structure is a set of behavioral-eval layers (trigger,
functional, regression, baseline, model-variance, rollout-safety, cost). This is **NOT** the
same as the **7-layer testing taxonomy** (git-hooks → static → unit → integration → system →
E2E → acceptance) specified in
[`../../taxonomy/v0.1.0-draft/SPEC.md`](../../taxonomy/v0.1.0-draft/SPEC.md). The testing
taxonomy classifies _a repository's testing system_; the behavioral-eval layers classify _one
skill's runtime behavior_. They coincide only nominally (both happen to enumerate seven
things). A conformant promotion run MUST NOT conflate them: the behavioral tier's verdict is
about the skill's behavior, not about the repo's test coverage across the taxonomy.

## 5. Tier ordering + the fail-fast boundary

### R1 — Static tiers run before the behavioral tier

A promotion run MUST run Tier 1 and Tier 2 (the static tiers) before Tier 3 (the behavioral
tier). Rationale: the static tiers are free and deterministic; spending minutes and API budget
on a behavioral eval of an artifact that fails a static production-hazard check is wasteful and
can be unsafe (e.g., executing a skill with an undeclared tool).

### R2 — A RED static production gate fails fast

If Tier 2's verdict is `RED`, the promotion run MUST NOT run Tier 3, and the final verdict is
`FAIL` (§ 6 R7). The behavioral tier does not run against a skill with a known production
hazard. A `YELLOW` Tier 2 (warnings only) does NOT block Tier 3.

### R3 — A FAIL Tier 1 fails fast

If Tier 1's gate verdict is `FAIL` (a required field is missing at the requested mode), the
promotion run MUST NOT run Tier 3, and the final verdict is `FAIL`. An artifact that does not
meet the structural floor for its requested mode is not eligible for behavioral promotion.

### R4 — Ordering within the static tiers is unconstrained

Tier 1 and Tier 2 are both static, deterministic, and independent; a promotion run MAY run
them in either order or concurrently. Only the static→behavioral boundary (R1) is ordered.

## 6. Verdict-combination algebra

A promotion run produces exactly one **final verdict** ∈ { `PASS`, `FAIL`, `VERIFIED` } from
the three tier verdicts. The combination is total and deterministic:

### R5 — Inputs

The algebra consumes:

- `t1` ∈ { `PASS`, `FAIL` } — Tier 1 gate verdict.
- `t2` ∈ { `GREEN`, `YELLOW`, `RED` } — Tier 2 aggregate.
- `t3` ∈ { `GREEN`, `RED`, `SKIPPED` } — Tier 3 aggregate (`SKIPPED` when not run, including
  fail-fast skip per § 5 or opt-out per § 9).

### R6 — `VERIFIED` requires the behavioral tier to have actually run and passed

The final verdict is `VERIFIED` **iff** `t1 = PASS` AND `t2 ∈ { GREEN, YELLOW }` AND
`t3 = GREEN`. `VERIFIED` is strictly stronger than `PASS`: it asserts the behavioral eval ran
and the skill behaved correctly. A promotion run MUST NOT report `VERIFIED` when `t3 =
SKIPPED` — absence of a behavioral failure is not evidence of behavioral correctness (§ 9 R12).

### R7 — `FAIL` on any blocking tier failure

The final verdict is `FAIL` **iff** `t1 = FAIL` OR `t2 = RED` OR `t3 = RED`. Any one blocking
tier failure fails the promotion run. (Per § 5, a fail-fast `t1 = FAIL` or `t2 = RED` forces
`t3 = SKIPPED`; the `t3 = RED` disjunct only applies on a run where Tier 3 actually executed.)

### R8 — `PASS` otherwise

The final verdict is `PASS` in every remaining case — i.e. `t1 = PASS` AND `t2 ∈ { GREEN,
YELLOW }` AND `t3 = SKIPPED`. `PASS` is the default-promotion-run outcome (Tier 1 + Tier 2
green, behavioral eval not requested). It means _"clears the static bar; behavioral eval not
performed."_

### R9 — The decision table is total

Every `(t1, t2, t3)` triple maps to exactly one final verdict. The table:

| `t1`   | `t2`              | `t3`      | Final      | Why                                  |
| ------ | ----------------- | --------- | ---------- | ------------------------------------ |
| `FAIL` | _any_             | `SKIPPED` | `FAIL`     | R3 fail-fast; structural floor unmet |
| `PASS` | `RED`             | `SKIPPED` | `FAIL`     | R2 fail-fast; production hazard      |
| `PASS` | `GREEN`\|`YELLOW` | `RED`     | `FAIL`     | R7; behavioral failure               |
| `PASS` | `GREEN`\|`YELLOW` | `GREEN`   | `VERIFIED` | R6; behavioral eval passed           |
| `PASS` | `GREEN`\|`YELLOW` | `SKIPPED` | `PASS`     | R8; static-only promotion            |

(The fail-fast rules § 5 make the `(FAIL, _, GREEN)`, `(FAIL, _, RED)`, `(_, RED, GREEN)`,
`(_, RED, RED)` rows unreachable — a behavioral tier never runs after a fail-fast skip. A
conformant implementation MUST NOT produce those triples.)

## 7. Evidence each tier emits

### R10 — Every tier verdict is Evidence-Bundle-emittable

Per the unification thesis (DR-010 § 7 Q2: "every validator emits Evidence Bundle"), each
tier's verdict MUST be expressible as a `gate-result/v1` row inside an Evidence Bundle, per the
canonical [`evidence-bundle`](../../evidence-bundle/v0.1.0-draft/SPEC.md) envelope and the
kernel schema. Specifically:

- Tier 1 and Tier 2 are **static** gates: their rows carry deterministic `gate_decision`
  values, an `input_hash` over the graded artifact, and `dimensions_evaluated` naming the
  rubric / static-check surface. These are `audit-harness`-class rows (glossary: `audit-harness`
  "emits `gate-result/v1` rows").
- Tier 3 is **behavioral**: its row is the `j-rig` behavioral-eval verdict. The behavioral
  predicate body (which layer, which model, confidence) is a kernel concern reserved for the
  behavioral-eval predicate; this bridge requires only that the _aggregate_ tier verdict be
  carried as a `gate_result`-shaped row so the three tiers compose in one bundle.

### R11 — A multi-tier promotion run produces one bundle with one row per tier run

A promotion run that executes N tiers (N ∈ {2, 3}) MUST emit an Evidence Bundle whose `row_count`
equals the number of tier verdicts produced and whose `subject_set` names each tier's gate.
The final verdict (§ 6) is a _derived_ combination over those rows — it MUST be reproducible by
re-applying the § 6 algebra to the bundle's rows, so a downstream RolloutGate (glossary) can
re-derive the promotion decision from the bundle alone without re-running any tier.

## 8. Determinism + reproducibility obligations

### R12 — Static tiers are byte-deterministic

Tier 1 and Tier 2 MUST be deterministic functions of the graded artifact bytes + the pinned
rubric/policy version: the same SKILL.md + the same validator version always yields the same
Tier 1 and Tier 2 verdicts. The `gate-result/v1` row's `input_hash` MUST be a hash over the
graded artifact so a verdict is reproducibly attributable to exact bytes.

### R13 — The behavioral tier is probabilistic and MUST record its non-determinism inputs

Tier 3 is probabilistic (model sampling). A behavioral-tier row MUST record the inputs that
make its verdict reproducible-in-principle: the model matrix evaluated, and the eval-spec /
seed identity (so a re-run with the same inputs is comparable). A behavioral-tier verdict MUST
NOT be presented as byte-deterministic; conflating a probabilistic verdict with a deterministic
one (R12) is non-conformant.

### R14 — The combination algebra is deterministic

§ 6's algebra is a pure function of `(t1, t2, t3)`. Given the three tier verdicts, the final
verdict MUST be reproducible regardless of the (probabilistic) process that produced `t3`.
Non-determinism is confined to _producing_ `t3`; it MUST NOT leak into _combining_ the tiers.

## 9. The unavailable-behavioral-tier rule

### R15 — Tier 3 absence is `SKIPPED`, never `FAIL`

When the behavioral harness is unavailable (not installed, not on PATH) or the promotion run
did not request it, Tier 3's verdict is `SKIPPED`, NOT `FAIL`. A promotion run MUST NOT fail
solely because the behavioral tier did not run. Only Tier 1 + Tier 2 are mandatory; the
behavioral tier is opt-in (§ 4.3). This mirrors the validator's own rule: "Tier 3 absence does
not mean a skill fails — only Tier 1+2 are mandatory."

### R16 — A `SKIPPED` behavioral tier caps the final verdict at `PASS`

Per R6, `VERIFIED` is unreachable when `t3 = SKIPPED`. A static-only promotion run tops out at
`PASS`. `VERIFIED` is reserved for runs where the behavioral eval actually executed and passed
— it is the signal that a downstream consumer can trust the skill's _behavior_, not merely its
_shape_.

## 10. Conformance fixtures

A conformant tier-bridge implementation MUST reproduce the § 6 R9 decision table exactly. The
reference fixture set under
[`conformance-test-suite/`](./conformance-test-suite/) (to be authored alongside the first
implementation) enumerates each reachable triple and its expected final verdict, plus the
fail-fast invariants:

1. `(FAIL, *, *)` → final `FAIL` AND `t3 = SKIPPED` (R3).
2. `(PASS, RED, *)` → final `FAIL` AND `t3 = SKIPPED` (R2).
3. `(PASS, GREEN, GREEN)` → final `VERIFIED` (R6).
4. `(PASS, YELLOW, GREEN)` → final `VERIFIED` (R6; YELLOW does not block).
5. `(PASS, GREEN, RED)` → final `FAIL` (R7).
6. `(PASS, GREEN, SKIPPED)` → final `PASS` (R8).
7. `(PASS, GREEN, SKIPPED-because-unavailable)` → final `PASS`, never `FAIL` (R15) and never
   `VERIFIED` (R16).

A claim of conformance without a fixture pass is not a claim (specs/README § "Test suites").

## 11. Anchors

- **Static/behavioral judge distinction:** canonical glossary
  [§ JudgeDecision / § harness](../../../000-docs/014-DR-GLOS-canonical-glossary.md) — a judge
  is either a deterministic validator (static gate, mechanical PASS/FAIL) or an LLM-as-judge
  (probabilistic). `audit-harness` = static + `gate-result/v1`; `j-rig` = behavioral.
- **Unification thesis (every validator emits Evidence Bundle):**
  [DR-010 § 7 Q2](../../../000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md).
- **Repo roles (which tool is which):** [Blueprint A § 2.1](../../../000-docs/011-AT-ARCH-ecosystem-master-blueprint.md).
- **Evidence Bundle envelope + `gate-result/v1`:**
  [`../../evidence-bundle/v0.1.0-draft/SPEC.md`](../../evidence-bundle/v0.1.0-draft/SPEC.md) +
  [Blueprint B § 7](../../../000-docs/012-AT-ARCH-platform-runtime-blueprint.md).
- **The 7-layer testing taxonomy (distinct from the behavioral-eval layers — § 4.4):**
  [`../../taxonomy/v0.1.0-draft/SPEC.md`](../../taxonomy/v0.1.0-draft/SPEC.md).
- **RolloutGate consumes a bundle + policy → ship/no-ship:** canonical glossary § RolloutGate.

## 12. RFC

Composition-algebra challenges, additional fail-fast cases, and counter-proposals welcome via
GitHub issues on [`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab).

## License

Apache 2.0 — see [LICENSE](../../../LICENSE) at repo root.
