# Prompt + Context Evaluation — SPEC v0.1.0-draft

> **Status: SKELETON (draft, non-normative).** Section headers + scope only. This module
> codifies a methodology for evaluating **intent-bearing artifacts beyond skills** — prompts
> and context templates — reusing the platform's existing eval substrate (MatcherMap,
> JudgeDecision, EvidenceBundle). It exists ahead of any code per intent-eval-lab's chartered
> role (Blueprint A § 2.1). Normative content does **not** land until the gates in
> [`043-DR-RFC-intent-eval-target-generalization-2026-06-06.md`](../../../000-docs/043-DR-RFC-intent-eval-target-generalization-2026-06-06.md)
> clear (Class-1 ISEDC for the entity change + predicate reservation; bandwidth gate per
> DR-010 § 13.5).
>
> **Anchors:** landscape [`042-RR-LAND`](../../../000-docs/042-RR-LAND-prompt-and-context-eval-landscape-2026-06-06.md);
> recommendation [`043-DR-RFC`](../../../000-docs/043-DR-RFC-intent-eval-target-generalization-2026-06-06.md);
> Blueprint B § 2.1–2.5; glossary § 4 (Intentional Mapping vocabulary).

## 1. Scope

- **In scope:** evaluating a `prompt` and a `context-template` as eval targets — the
  expected-behavior families, the matcher classes, and the failure-shape namespace that make
  such evaluation conformance-shaped (pass/fail) rather than merely score-shaped.
- **Out of scope:** the kernel `EvalTarget` union itself (proposed in 043-DR-RFC, gated); how
  prompts/context templates are _constructed_ (templating + structured-output libraries — see
  042 § 5.2–5.3; these are authoring tools, not eval surface); skill evaluation (covered by
  the existing j-rig 7-layer harness).
- **Anchoring discipline (specs/methodology/README.md):** every normative requirement, when
  authored, will cite the canonical upstream source it codifies (RAGAS, RULER, OWASP LLM Top
  10, the Anthropic context-engineering post, etc. — see 042 § 8). This skeleton anchors but
  does not yet enumerate normative MUSTs.

## 2. Target types

> _Placeholder — to be authored once 043-DR-RFC's `EvalTarget` proposal clears Class-1 ISEDC._

- **2.1 `prompt`** — a frozen, content-addressed instruction artifact (the prompt-engineering
  unit). Mirrors `SkillSnapshot` shape (glossary § 2.9): SHA-pinned body + variables + config.
- **2.2 `context-template`** — a frozen artifact describing how context is assembled
  (Write/Select/Compress/Isolate per 042 § 2): retrieval policy, memory policy, compression
  policy, isolation boundaries.
- **2.3 Relationship to `skill`** — a `skill` is the composite (prompt + context scaffolding);
  `prompt` and `context-template` are the decomposed primitives. Skill is intent-type #1.

## 3. Matcher families

> _Placeholder — these become MatcherMap classes (Blueprint B § 2.3); namespace admission is
> gated per 043-DR-RFC § 4.3 + § 7._

- **3.1 MM-P\*** (prompt-eval): instruction-adherence, output-schema conformance,
  reference-free quality (LLM-as-judge / G-Eval, 042 § 3.1), injection-resistance
  (OWASP LLM Top 10, 042 § 3.1).
- **3.2 MM-C\*** (context-eval): faithfulness-to-context, context-precision, context-recall
  (RAGAS, 042 § 4.2), needle-retrieval (NIAH/RULER, 042 § 4.2), context-rot-resistance
  (Chroma, 042 § 4.2).
- **3.3 Reuse, not reinvention** — each family is an _expected-behavior declaration_, the exact
  thing MatcherMap already models. No new judge engine; the existing JudgeDecision +
  EvidenceBundle layers carry the verdicts and evidence unchanged (043-DR-RFC § 3).

## 4. Failure-shape namespace

> _Placeholder — extends the Intentional Mapping vocabulary (glossary § 4). MM-1..MM-6 are
> immutable; MM-P\*/MM-C\* admission routes through the MM-7+ criteria (DR-004 S1Q3) or an
> ISEDC namespace decision (043-DR-RFC § 4.3). To be enumerated post-gate._

## 5. Conformance vs eval

Per specs/methodology/README.md: a conformance claim is binary (pass/fail against normative
requirements); an eval result is relative (ranking, A/B). This module will ship both shapes in
separate artifacts — a conformance test suite (binary) and research evals (quantitative) — and
will not conflate them.

## 6. Predicate surface (proposed, not reserved, not declared)

When this module reaches normative status, signed evidence would carry
`evals.intentsolutions.io/prompt-eval/v1` and `…/context-eval/v1`. **Proposed only** — not
reserved (Class-1 ISEDC), not declared, not emitted (043-DR-RFC § 6). Host is
`evals.intentsolutions.io` exclusively; never `labs.` (CISO binding, glossary § 8).

## 7. Conformance test suite

> _Placeholder — `conformance-test-suite/` to be populated when normative requirements land.
> Per specs/README.md: "a claim of conformance without a test pass is not a claim."_

## 8. Case studies

> _Placeholder — `case-studies/` holds vendor-neutral instantiations only; partner-named
> instantiations require written consent (DR-004 S1Q2; lab CLAUDE.md brand-name policy)._

---

_v0.1.0-draft skeleton. Non-normative. 2026-06-06._
