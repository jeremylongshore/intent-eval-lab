---
date: 2026-06-06
authors:
  - Jeremy Longshore (Intent Solutions)
status: RESEARCH (non-normative)
filing_standard: Document Filing Standard v4.3
relates_to:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — anti-goals, repo taxonomy)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — § 2.1 EvalSpec, § 2.2 EvalRun, 13-entity model)
  - 014-DR-GLOS-canonical-glossary.md (canonical glossary)
  - 027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md (Skill Refiner plan — AC-7, AC-13 RefinerStrategy)
companion:
  - 043-DR-RFC-intent-eval-target-generalization-2026-06-06.md (the positioning recommendation this landscape feeds)
epic: iel-prompt-context-eval
verification: every external claim carries a live source URL in § 8; verification status (verified / partial / flagged) is recorded per source.
---

# Prompt + Context Engineering Evaluation — Landscape (2024–2026)

> **Scope.** This is a research/landscape recon doc. It surveys how the industry evaluates
> **prompts** and **context** (as distinct from how the Intent Eval Platform evaluates a
> `SkillSnapshot`), and it inventories the "Python tools to work with prompts" category
> (DSPy and its cousins). It is **non-normative**: it asserts no platform commitment. The
> recommendation that follows from it — generalizing the platform's unit-under-test from
> "skill" to **intent-bearing artifact** — lives in the companion RFC
> [`043-DR-RFC-intent-eval-target-generalization-2026-06-06.md`](043-DR-RFC-intent-eval-target-generalization-2026-06-06.md).
>
> **Citation discipline.** Every external claim carries a live source URL collected in
> § 8 with a verification status. Where a widely-repeated claim could not be traced to a
> primary source (e.g., a numeric "production-ready" threshold, a paywalled analyst
> pronouncement, a colloquial term-of-art), it is **flagged** in § 8.3 rather than asserted
> as fact.

---

## 0. How to read this document

§ 1 states the paradox that motivates the survey. § 2 establishes the industry thesis shift
(prompt engineering as a _subset_ of context engineering) from primary sources. § 3 surveys
**prompt-engineering evaluation** — methodologies and tools, ending in a topline-vs-commodity
table. § 4 surveys **context-engineering evaluation** — definitions, metrics, tools, maturity.
§ 5 surveys the **prompt-as-code / optimization** category (DSPy et al.) plus the adjacent
templating and structured-output libraries. § 6 synthesizes what is _topline_ (hard, durable,
worth owning) versus _commodity_ (table-stakes, available everywhere) across all three. § 7 is
a one-paragraph bridge to the positioning RFC. § 8 is the source register with verification
status.

---

## 1. The naming paradox

Intent Solutions' niche is **agent-native evaluation**. The platform is literally named the
**Intent Eval Platform**. Yet today the ecosystem evaluates exactly one kind of unit: a
`SKILL.md` — a packaged Claude Code Skill, frozen as a `SkillSnapshot` (Blueprint B § 2.9) and
referenced by `EvalRun.skill_snapshot_id` (Blueprint B § 2.2; kernel `EvalRun.ts:88-89`). The
j-rig harness goes further and hardcodes the unit _by name_: its `EvalSpec` carries a
`skill_name` field "Name of the skill being evaluated" (`j-rig-binary-eval/packages/core/src/schemas/eval-spec.ts:33-37`).

Meanwhile the industry has moved the centre of gravity from the _prompt_ to the _context_. A
prompt and a context template are, in the platform's own terms, just other shapes of
intent-bearing artifact — eval targets the platform cannot yet name. This document surveys the
outside world's answer to "how do you evaluate a prompt / a context?" so the platform's own
answer can be positioned against it (the RFC).

---

## 2. The thesis shift: prompt engineering ⊂ context engineering

Four primary sources, 2025, converge on the same claim: prompt engineering is now a _subset_
of the broader discipline of context engineering.

- **Anthropic, "Effective context engineering for AI agents" (2025-09-29).** The canonical
  vendor framing: _"At Anthropic, we view context engineering as the natural progression of
  prompt engineering."_ Where prompt engineering crafts instructions, context engineering
  optimizes the **entire** set of tokens (system instructions, tools, external data, message
  history) competing for the model's limited attention budget. [S1]

- **Andrej Karpathy (2025, X/Twitter).** Popularized the term over "prompt engineering":
  _"+1 for 'context engineering' over 'prompt engineering' … context engineering is the
  delicate art and science of filling the context window with just the right information."_
  [S2]

- **Gartner (mid-2025).** Framed the shift in market terms ("context engineering is in,
  prompt engineering is out"). _Primary Gartner page is paywalled;_ the claim and ~July-2025
  timing are corroborated by multiple secondary outlets — recorded as **partial** in § 8.3.
  [S3]

- **LangChain, "Context Engineering for Agents" (2025-07-02).** The operational taxonomy:
  context engineering decomposes into **Write** (save tokens outside the window),
  **Select** (pull the right tokens in — the RAG pattern), **Compress** (retain only the
  tokens a task needs), **Isolate** (split context across agents/sandboxes). [S4]

**Why it matters for the platform.** If prompt engineering is a subset of context engineering,
then a SKILL.md — which bundles an instruction prompt _and_ the context scaffolding (tool
descriptions, references, bundled files) the skill injects — is already a **packaged
prompt+context artifact**. The platform is already evaluating one point in the
prompt→context space; it simply hasn't generalized the _name_ of the thing it evaluates. That
is the entire thrust of the companion RFC.

---

## 3. Prompt-engineering evaluation (2024–2026)

### 3.1 Methodologies

| Methodology                                       | What it is                                                                                                                                                                             | Canonical source                                                                                                                                                                                                                                                   | Status   |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| **LLM-as-judge / G-Eval**                         | Use a strong LLM to score outputs; **G-Eval** adds chain-of-thought + form-filling for reference-free scoring. G-Eval reports Spearman ρ≈0.51 with humans on summarization.            | G-Eval, Liu et al., EMNLP 2023, arXiv:2303.16634 [S5]                                                                                                                                                                                                              | verified |
| **Pairwise / preference ranking (Bradley-Terry)** | Rank models/prompts by pairwise human preference; **Chatbot Arena / LMArena** fits a Bradley-Terry model (MLE) over 1.7M+ votes for stable Elo-like ratings with confidence intervals. | Chatbot Arena, Chiang et al., arXiv:2403.04132 [S6]                                                                                                                                                                                                                | verified |
| **Golden / regression datasets ("sacred cases")** | Freeze a curated set of input→expected pairs; re-run on every change as a CI gate; a regression on a "sacred" case blocks release regardless of average gain.                          | Practice is universal across eval tools (Braintrust experiments, Langfuse datasets, DeepEval); **"sacred case" is a colloquial term, not a named academic methodology** — see § 8.3 [F1]. The platform's own `RegressionPack` (Blueprint B § 2.7) is this pattern. | partial  |
| **Assertion gates (structure-only)**              | Deterministic checks: JSON-valid, contains-string, schema-conformance, regex. Cheap, exact, no model in the loop.                                                                      | Implemented universally (DeepEval `DAGMetric`, promptfoo asserts, Braintrust). No single methodology paper.                                                                                                                                                        | partial  |
| **Reference-free vs reference-based**             | Reference-based compares to a gold answer (BLEU/ROUGE/exact-match); reference-free scores intrinsic quality (LLM-judge). G-Eval explicitly contrasts the two.                          | arXiv:2303.16634 [S5]                                                                                                                                                                                                                                              | verified |
| **Red-team / jailbreak / prompt-injection**       | Adversarially probe for unsafe behavior; **OWASP LLM Top 10** ranks prompt injection #1 (direct + indirect). Automated red-teaming is now a productized category.                      | OWASP LLM Top 10 [S7]                                                                                                                                                                                                                                              | verified |
| **Statistical A/B testing**                       | Treat a prompt change as an experiment; compare arms with significance testing.                                                                                                        | Supported by Braintrust / Langfuse experiment surfaces; no dedicated methodology paper.                                                                                                                                                                            | partial  |

### 3.2 Tools

| Tool                                   | Role                                                                                                      | Source | Notable fact                                                                                                                                                                            |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **promptfoo**                          | OSS prompt/LLM eval + red-teaming; config-driven test suites; GitHub Action gate                          | [S8]   | **Acquired by OpenAI, announced 2026-03-09**; folds into OpenAI Frontier for automated red-teaming; _remains open source_. Corroborated by TechCrunch + Bloomberg. [S8, S8b] — verified |
| **DeepEval** (Confident AI)            | OSS eval framework; 50+ metrics incl. G-Eval impl, RAG metrics, deterministic `DAGMetric`                 | [S9]   | pytest-style; the closest OSS analogue to "unit tests for prompts"                                                                                                                      |
| **Inspect** (UK AISI)                  | Govt-built frontier-eval framework; datasets + solvers + scorers; 200+ prebuilt evals; agent + multimodal | [S10]  | the most _eval-harness-shaped_ of the set; strong agent-eval support                                                                                                                    |
| **Braintrust**                         | Commercial eval + observability; LLM-judge + heuristic + human scoring; PR-blocking gates                 | [S11]  | side-by-side experiments with significance reporting                                                                                                                                    |
| **Langfuse**                           | OSS LLM engineering platform; observability + eval + prompt mgmt + datasets                               | [S12]  | OpenTelemetry-native; overlaps the platform's OTel posture                                                                                                                              |
| **lm-evaluation-harness** (EleutherAI) | Academic benchmark harness; 60+ benchmarks (MMLU, GSM8K, …)                                               | [S13]  | backend of the HF Open LLM Leaderboard; _model_ eval, not _prompt-artifact_ eval                                                                                                        |
| **Arize Phoenix**                      | OSS observability + eval; tracing + LLM-judge metrics                                                     | [S14]  | self-hostable; OTel-based                                                                                                                                                               |
| **HELM** (Stanford CRFM)               | Holistic model evaluation across scenarios                                                                | [S15]  | academic, model-centric                                                                                                                                                                 |
| **Anthropic cookbook**                 | Recipes for Claude-as-evaluator; "building evals" notebook                                                | [S16]  | reference patterns, not a framework                                                                                                                                                     |

### 3.3 Topline vs commodity (prompt eval)

- **Commodity (table-stakes, available everywhere):** assertion gates, LLM-as-judge wiring,
  dataset/experiment management, tracing, prompt versioning. Five+ OSS tools do each.
- **Topline (hard, durable, defensible):** _audit-grade, signed, replayable_ evidence of an
  eval; _binary_ ship/no-ship gates with sacred-case regression that cannot be averaged out;
  rollout safety tied to a snapshot pin. The commodity tools produce dashboards and scores;
  almost none produce a **cryptographically attestable** verdict an external auditor can
  verify without trusting the vendor. That is the platform's Evidence Bundle thesis
  (Blueprint A § 1.2 principle 10; glossary § 2.4).

---

## 4. Context-engineering evaluation (2024–2026)

### 4.1 Definition + primary sources

Context-engineering evaluation asks: given everything that lands in the window (retrieved
docs, memory, tool outputs, history), did the system assemble the _right_ context, and did the
model _use_ it? Primary sources are the four in § 2 ([S1]–[S4]). The dominant, most-mature
sub-discipline is **RAG evaluation** — evaluation of the _Select_ quadrant.

### 4.2 Metrics

| Metric family            | What it measures                                                                                                                                                                | Source                                       | Status                                                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **RAGAS** core four      | **Faithfulness** (answer grounded in context), **answer relevancy**, **context precision** (are retrieved docs relevant), **context recall** (was all needed context retrieved) | RAGAS docs/repo [S17]                        | metrics verified; **the "> 0.8 = production-ready" rule of thumb is community guidance, not official RAGAS doctrine** — flagged § 8.3 [F2] |
| **TruLens RAG triad**    | **Context relevance**, **groundedness**, **answer relevance**                                                                                                                   | TruLens docs [S18]                           | verified                                                                                                                                   |
| **Needle-in-a-haystack** | Can the model retrieve one planted fact across context depths/lengths?                                                                                                          | Kamradt, `LLMTest_NeedleInAHaystack` [S19]   | verified                                                                                                                                   |
| **RULER**                | Synthetic multi-task long-context benchmark; shows perfect NIAH scores hide failures on retrieval/aggregation/reasoning as length grows                                         | NVIDIA, arXiv:2404.06654 [S20]               | verified                                                                                                                                   |
| **LongBench**            | Bilingual multitask long-context benchmark (21 datasets, 6 categories); v2 (2024-12) harder                                                                                     | THUDM, arXiv:2308.14508 [S21]                | verified                                                                                                                                   |
| **Lost in the middle**   | Performance peaks when relevant info is at the start/end of context, degrades in the middle                                                                                     | Liu et al., Stanford, arXiv:2307.03172 [S22] | verified                                                                                                                                   |
| **Context rot**          | Output quality degrades non-uniformly as input length grows; models do better on shuffled haystacks than coherent long docs                                                     | Chroma research [S23]                        | verified                                                                                                                                   |

### 4.3 Tools

RAGAS [S17], TruLens [S18], Arize Phoenix [S14], DeepEval RAG metrics [S9], LlamaIndex
evaluation module [S24], Inspect [S10] for agent/context eval. The RAG-eval tools cluster on
the same 4–5 metrics; the long-context benchmarks are research artifacts, not productized
gates.

### 4.4 Maturity assessment

- **RAG evaluation: mature.** Convergent metric set (faithfulness / context precision /
  context recall / answer relevancy ± groundedness), 5+ production frameworks, LLM-judge
  automation, de-facto standardization on RAGAS. [S25]
- **General context-engineering evaluation: emerging.** The _definition_ stabilized in 2025
  (Karpathy + Gartner + Anthropic + LangChain), but evaluation _beyond retrieval_ — measuring
  Write/Compress/Isolate, "context utilization," "context-window decay" — is research-stage
  and ad-hoc (RULER, lost-in-the-middle, context-rot are diagnostics, not CI gates). No
  production-grade general-context-eng metric exists yet. [S23, S26]

---

## 5. Prompt-as-code / optimization frameworks (the "Python tools to work with prompts")

### 5.1 The "compile against a metric" school

These frameworks treat a prompt not as a hand-tuned string but as **code that is compiled**:
you declare the task and a metric, and an optimizer searches the prompt/few-shot/instruction
space to maximize the metric.

| Framework                                  | Mechanism                                                                                                         | Source                                                                                                               | Status                                                                                                                                                |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **DSPy** (Stanford)                        | Signatures (typed I/O) + Modules (composable) + Optimizers/teleprompters that compile a pipeline against a metric | arXiv:2310.03714 "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines" [S27]; site [S27b] | paper verified; optimizer names **GEPA** verified, **MIPROv2 / BootstrapFewShot** are in DSPy docs/secondary but not the repo README — see § 8.3 [F3] |
| **"Is It Time To Treat Prompts As Code?"** | Empirical multi-use-case DSPy study; prompt-eval task 46.2% → 64.0%                                               | Lemos, Alves, Ferraz (U. Minho), arXiv:2507.03620 [S28]                                                              | verified — title is the thesis statement of this school                                                                                               |
| **TextGrad**                               | "Automatic differentiation via text" — LLM-generated textual feedback as gradients over prompts/code              | Yuksekgonul et al. (Zou group), arXiv:2406.07496; _Nature_ 2025; repo [S29]                                          | verified                                                                                                                                              |
| **AdalFlow**                               | LLM-AutoDiff: textual gradients + few-shot bootstrap + instruction-history optimization                           | repo/docs [S30]                                                                                                      | verified; **not** a rename of "LightRAG" (distinct projects) — flagged § 8.3 [F4]                                                                     |
| **PromptWizard** (Microsoft)               | Feedback-driven self-evolving prompt + in-context-example optimization                                            | MS Research + repo [S31]                                                                                             | verified                                                                                                                                              |
| **Promptomatix** (Salesforce)              | Task-description → optimized prompt; meta-prompt optimizer + DSPy-powered compiler                                | arXiv:2507.14241 [S32]                                                                                               | verified                                                                                                                                              |
| **CoolPrompt** (ITMO)                      | Zero-config auto prompt optimization (ReflectivePrompt / DistillPrompt / HyPE)                                    | repo [S33]                                                                                                           | verified                                                                                                                                              |

**The framing, sourced.** The DSPy abstract: _"DSPy modules are parameterized … the framework
includes a compiler that will optimize any DSPy pipeline to maximize a given metric."_ [S27]
The arXiv title "Is It Time To Treat Prompts As Code?" [S28] is itself the slogan of the
school. This matters because **Intent Solutions already ships a member of this school**: the
Skill Refiner is a DSPy-class optimizer specialized to `SKILL.md` (compile-against-a-metric,
accept only on strict-improvement). The RFC develops the integration seam.

### 5.2 Adjacent — templating / management

LangChain `PromptTemplate` [S34], Jinja2 [S35], Langfuse prompt management [S12]. These
_construct and version_ prompts; they do not evaluate them.

### 5.3 Adjacent — structured output / constrained generation

Instructor (Pydantic-typed extraction) [S36], Outlines (regex/JSON-schema/CFG-constrained
decoding) [S37], Guidance (token-level steering) [S38], BAML (prompts-as-typed-functions DSL)
[S39]. These _shape_ the output of a prompt; they do not evaluate it. They are how an eval
target of type `prompt` or `context-template` would be **built**, not **judged** — a
distinction the RFC leans on (keep construction libraries out of the eval kernel).

---

## 6. Synthesis — topline vs commodity, across all three categories

1. **Most of "prompt eval" and "RAG eval" is now commodity.** Assertion gates, LLM-as-judge,
   the RAGAS/TruLens metric sets, tracing, prompt versioning, dataset management — each has
   5+ interchangeable implementations. Building another is not a wedge.
2. **The durable, topline surface is evidence, not scoring.** Signed, replayable,
   externally-verifiable **Evidence Bundles**; binary ship/no-ship gates with sacred-case
   regressions that cannot be averaged out; rollout safety bound to an immutable snapshot pin.
   The j-rig 7-layer stack already covers much of the _behavioral_ topline (LLM-judge,
   baseline A/B, regression packs, per-model variance, rollout safety). The platform's wedge
   is the _attestation substrate underneath the scores_, not the scores.
3. **The optimization school (DSPy et al.) is a mechanism, not a moat.** Anyone can call DSPy.
   The defensible asset is the **acceptance gate** the optimizer runs against — the
   strict-improvement predicate the Skill Refiner already specifies (AC-7: mechanism
   swappable, gate durable). DSPy/TextGrad/GEPA become _backends_, not differentiators.
4. **General context-engineering evaluation is an open frontier.** Beyond RAG retrieval,
   nobody has a production gate for Write/Compress/Isolate quality. This is greenfield — and
   it maps cleanly onto the platform's MatcherMap vocabulary (RFC § 4).

---

## 7. Bridge to the positioning RFC

The landscape says three things the platform should act on: (a) a SKILL.md is _already_ a
packaged prompt+context artifact, so generalizing the unit-under-test is a renaming exercise
at the contract layer, not a new engine; (b) the platform's wedge is the evidence substrate,
which is already target-agnostic; (c) the optimization school plugs in behind the acceptance
gate. The companion RFC
[`043-DR-RFC-intent-eval-target-generalization-2026-06-06.md`](043-DR-RFC-intent-eval-target-generalization-2026-06-06.md)
turns these into a concrete (gated) recommendation: `EvalTarget = skill | prompt | context-template | agent`.

---

## 8. Source register

> Every URL below was fetched or surfaced via live search on 2026-06-06. Verification status:
> **verified** = confirmed against the primary source; **partial** = corroborated via
> secondary sources / primary gated; **flagged** = see § 8.3.

### 8.1 Primary thesis sources

- **[S1]** Anthropic, _Effective context engineering for AI agents_ (2025-09-29) — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents> — **verified** (title + date + anchor quote confirmed)
- **[S2]** A. Karpathy, X post on context engineering (2025) — <https://x.com/karpathy/status/1937902205765607626> — **verified**
- **[S3]** Gartner, "context engineering is in, prompt engineering is out" (~2025-07) — <https://www.gartner.com/en/articles/context-engineering> — **partial** (primary paywalled; corroborated by secondary outlets)
- **[S4]** LangChain, _Context Engineering for Agents_ (2025-07-02) — <https://www.langchain.com/blog/context-engineering-for-agents> — **verified** (Write/Select/Compress/Isolate confirmed)

### 8.2 Methods, metrics, tools, frameworks

- **[S5]** G-Eval, Liu et al., EMNLP 2023 — <https://arxiv.org/abs/2303.16634> — verified
- **[S6]** Chatbot Arena, Chiang et al. — <https://arxiv.org/abs/2403.04132> — verified
- **[S7]** OWASP Top 10 for LLM Applications (prompt injection #1) — <https://genai.owasp.org/llm-top-10/> — verified
- **[S8]** promptfoo — <https://www.promptfoo.dev/> ; acquisition: <https://openai.com/index/openai-to-acquire-promptfoo/> — verified
- **[S8b]** OpenAI–promptfoo acquisition coverage — <https://techcrunch.com/2026/03/09/openai-acquires-promptfoo-to-secure-its-ai-agents/> ; <https://www.bloomberg.com/news/articles/2026-03-09/openai-buying-ai-security-startup-promptfoo-to-safeguard-ai-agents> — verified
- **[S9]** DeepEval — <https://github.com/confident-ai/deepeval> ; <https://deepeval.com/> — verified
- **[S10]** Inspect (UK AISI) — <https://inspect.aisi.org.uk/> ; <https://github.com/UKGovernmentBEIS/inspect_ai> — verified
- **[S11]** Braintrust — <https://www.braintrust.dev/> — verified
- **[S12]** Langfuse — <https://github.com/langfuse/langfuse> ; prompt mgmt: <https://langfuse.com/docs/prompt-management/overview> — verified
- **[S13]** lm-evaluation-harness — <https://github.com/EleutherAI/lm-evaluation-harness> — verified
- **[S14]** Arize Phoenix — <https://github.com/Arize-ai/phoenix> — verified
- **[S15]** HELM — <https://github.com/stanford-crfm/helm> ; <https://arxiv.org/abs/2211.09110> — verified
- **[S16]** Anthropic cookbook (building evals) — <https://github.com/anthropics/anthropic-cookbook/blob/main/misc/building_evals.ipynb> — verified
- **[S17]** RAGAS — <https://github.com/vibrantlabsai/ragas> ; <https://docs.ragas.io/> — verified (repo moved from `explodinggradients/ragas`; old URL redirects)
- **[S18]** TruLens RAG triad — <https://www.trulens.org/getting_started/core_concepts/rag_triad/> — verified
- **[S19]** Needle-in-a-haystack (G. Kamradt) — <https://github.com/gkamradt/LLMTest_NeedleInAHaystack> — verified
- **[S20]** RULER (NVIDIA) — <https://arxiv.org/abs/2404.06654> ; <https://github.com/NVIDIA/RULER> — verified
- **[S21]** LongBench (THUDM) — <https://arxiv.org/abs/2308.14508> ; <https://github.com/THUDM/LongBench> — verified
- **[S22]** Lost in the Middle (Liu et al.) — <https://arxiv.org/abs/2307.03172> — verified
- **[S23]** Context rot (Chroma) — <https://research.trychroma.com/context-rot> — verified
- **[S24]** LlamaIndex evaluation — <https://docs.llamaindex.ai/> — verified
- **[S25]** RAG eval maturity (2026 guide) — <https://datavlab.ai/post/rag-evaluation-methods-metrics-2026-guide> — partial (secondary)
- **[S26]** "From RAG to context" review (2025) — <https://ragflow.io/blog/rag-review-2025-from-rag-to-context> — partial (secondary)
- **[S27]** DSPy paper — <https://arxiv.org/abs/2310.03714> — verified; **[S27b]** site — <https://dspy.ai/> ; repo <https://github.com/stanfordnlp/dspy> — verified
- **[S28]** "Is It Time To Treat Prompts As Code?" — <https://arxiv.org/abs/2507.03620> — verified
- **[S29]** TextGrad — <https://arxiv.org/abs/2406.07496> ; <https://github.com/zou-group/textgrad> — verified
- **[S30]** AdalFlow — <https://github.com/SylphAI-Inc/AdalFlow> — verified
- **[S31]** PromptWizard (Microsoft) — <https://github.com/microsoft/PromptWizard> — verified
- **[S32]** Promptomatix (Salesforce) — <https://arxiv.org/abs/2507.14241> ; <https://github.com/SalesforceAIResearch/promptomatix> — verified
- **[S33]** CoolPrompt (ITMO) — <https://github.com/CTLab-ITMO/CoolPrompt> — verified
- **[S34]** LangChain PromptTemplate — <https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.prompt.PromptTemplate.html> — verified
- **[S35]** Jinja2 — <https://jinja.palletsprojects.com/> — verified
- **[S36]** Instructor — <https://github.com/567-labs/instructor> ; <https://python.useinstructor.com/> — verified
- **[S37]** Outlines — <https://github.com/dottxt-ai/outlines> — verified
- **[S38]** Guidance (Microsoft) — <https://github.com/guidance-ai/guidance> — verified
- **[S39]** BAML (BoundaryML) — <https://github.com/BoundaryML/baml> ; <https://docs.boundaryml.com/> — verified

### 8.3 Flagged / could-not-fully-verify

- **[F1] "Sacred-case" / "golden dataset" as a named methodology.** The _practice_
  (snapshot/regression datasets as CI gates) is universal, but "sacred case" is colloquial,
  not an academic term. Stated in this doc as practice, not as a cited methodology. (The
  platform's own normative term is `RegressionPack`, Blueprint B § 2.7.)
- **[F2] RAGAS "> 0.8 = production-ready."** Widely repeated (community blogs cite 0.75–0.85),
  but **not** found in official RAGAS documentation. Treat as community heuristic, not vendor
  doctrine.
- **[F3] DSPy optimizer names.** GEPA is confirmed in DSPy research material; **MIPROv2** and
  **BootstrapFewShot** appear in DSPy docs and secondary sources but were not confirmed in the
  repo README during this pass. The optimizer-as-compiler claim itself is verified [S27].
- **[F4] AdalFlow ≠ LightRAG.** The plan-draft hypothesized AdalFlow was "formerly LightRAG";
  search shows them as distinct repositories. No rename on record. Stated as distinct.
- **[S3] Gartner pronouncement.** Primary URL is paywalled (HTTP 403); the claim + ~July-2025
  timing are corroborated by multiple secondary outlets but the exact wording is from
  secondary reporting.

---

_Research recon, non-normative. Author: Jeremy Longshore (Intent Solutions). 2026-06-06._
