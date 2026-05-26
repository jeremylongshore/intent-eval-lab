---
title: Intent Eval Platform — Phase B Gap Analysis and Research Framework
subtitle: Iterative Snacking Walrus — Technical Landscape Audit + Per-Area Treatment of 21 AI Infrastructure Gaps
filing_code: 000-DR-FIND
version: 1.0
date: 2026-05-20
author: Jeremy Longshore, Intent Solutions
bead: bd_000-projects-ppt2
program: Iterative Snacking Walrus (Phase B research-and-framing)
sources_compiled:
  - 000-RR-BIBL-shared-bibliography-2026-05-20.md (≈148 Semantic Scholar papers across 16 seed queries)
  - 000-RR-COMP-ecosystem-landscape-2026-05-20.md (12 OSS projects + 7 frontier labs, May 2026)
  - DR-010 ISEDC Session 4 widened-scope (intent-eval-lab/000-docs/010)
  - Blueprints A/B/C + Canonical Glossary (intent-eval-lab/000-docs/011-014)
framing: technical / craft / contribution audit (NOT market / pricing / GTM)
---

# Intent Eval Platform — Phase B Gap Analysis and Research Framework

## Executive Summary

This document audits 20 strategic AI-infrastructure areas surfaced in two advisory rounds during May 2026, plus one uniquely accessible area (evaluator-disagreement dataset), against the current state of the Intent Eval Platform (IEP) — five Apache-2.0 OSS repositories converging on a shared Evidence Bundle schema. The audit is **craft-and-contribution-focused**: it identifies where the field stands, where we technically fall short, and where an obsessive operator with infrastructure expertise can either contribute upstream or build new work that pushes the field forward.

**Top-line findings**:

1. **Three IEP gap areas are mature or in-flight** (Eval Systems via j-rig; Operational Trajectories via iel-E12; Trajectory Replay via iel-E11). Citation grounding is the remaining work for these — not new spec.
2. **Thirteen IEP gap areas need fresh beads + spec** across the kernel (intent-eval-core), j-rig, audit-harness, intent-rollout-gate, and intent-eval-lab. Two of these (memory broadening; verifier systems) interact strongly with already-deferred items in `iec-deferral-*`.
3. **Four foundation-model-level areas** (curriculum learning, compression, small-model research, mechanistic interpretability) are explicitly **out of scope for IEP** and belong in a parked personal-skill pillar — see § 9 and Appendix F.
4. **The largest open contribution surfaces** are: (a) OpenTelemetry GenAI SIG semantic conventions for agent trajectories (academic literature is empty here — the standards work is the surface); (b) cross-tool eval-result interoperability (Inspect AI is closest precedent, MIT-licensed, government-backed); (c) `agent-loop-trace/v1` ↔ OpenInference conventions convergence; (d) the evaluator-disagreement public dataset (Area #21) which is uniquely ours to ship because nobody is doing it.
5. **The strongest "skip, well-covered" calls** are: prompt-injection defense literature (23+ recent papers, multiple stable benchmarks like AgentDojo + ASB), LLM-as-judge bias literature (50+ papers, 1 survey with 1300+ citations), and inference-time compute scaling (38+ papers, multiple surveys). We cite this work; we do not build new work in those layers.

**Action enabled by this document**:

- ISEDC Session 5 can convene on a consolidated Framing Memo derived from this audit
- Phase B P0/P1 epic ranking can be made on evidence, not vibes
- Per-team lit-reviews (Teams A through E in § 6) inherit the bibliography + landscape work and refine rather than restart
- Personal-skill pillar gets a single OPS bead, quarterly-reviewed, no IEP scope contamination

**Three things the operator should decide before Phase B kickoff**:

1. **Of the six P0-recommended epics in § 11, how many can realistically ship under operator-bandwidth constraints?** The full P0 set estimates at 22-30 work-blocks (~6-10 weeks of focused execution); a constrained set of four still delivers high-leverage outcomes. Appendix G.7 provides the dropdown sequence.

2. **Which Class-2 ISEDC decisions need pre-resolution before Phase B work-flow can begin?** The audit identifies at least three: (a) whether `Verifier`, `Memory`, `Tool` enter the kernel as first-class entities (§ 4.5.7); (b) which `iec-deferral-*` Class-2 specs are blocking enough to warrant immediate closure (§ 4.5.1); (c) whether a single `TrustPosture` entity rolls up memory + guardrails + drift, or whether separate entities are the right granularity (§ 4.5.5). Each is a council question; each gates downstream construction.

3. **What is the explicit Phase B → Phase C trigger?** Bandwidth-gated work has no natural cutover signal; the operator should declare in advance (capacity-based, milestone-based, calendar-based) when Phase B closes and Phase C planning begins. Without a declared trigger, Phase B drifts and Phase C never starts.

**What this audit confirms about the platform's existing direction**:

The five-repo convergence on `gate-result/v1` is the right substrate (§ 4.5.1). The anti-goal posture — schemas + validators + attestations, not runtime hosting — is correct and survives the audit (§ 4.5.4). The DR-010 widened-scope lock that removed customer-signal-gating reframes Phase B work as craft + contribution, which the per-area treatments support throughout. The kernel's existing 13 entities + the proposed 6-8 additions (under Class-2 decision) cover the modeled surface; further entity proliferation would harm interoperability more than it helps coverage.

**What this audit reveals as more fragile than expected**:

The kernel's `gate-result/v1` surface is more cross-cutting than any other artifact in the platform (§ 4.5.1). Every Phase B epic touches it. Decisions about its shape — what extension blocks, what versioning policy, what attestation granularity — should be made with awareness of all downstream consumers. The audit recommends explicit `gate-result/v1.2.0` planning before Phase B P0 work commits to specific extensions.

The OSS observability layer (OpenTelemetry GenAI SIG conventions) is more fluid than the kernel literature suggests — the SIG is in "Development" status, conventions are explicitly experimental, and our `agent-loop-trace/v1` proposal could be a high-leverage contribution if submitted in the next few weeks before alternative proposals harden. This is a timing-sensitive opportunity, not a perpetual one.

---

## § 1 — Strategic context

### 1.1 Why this report exists

In May 2026, two strategic advisories surfaced during the Phase A foundation-lock work. The first identified 11 high-leverage AI infrastructure areas; the second expanded the list to 20, both noting that the next decade of AI infrastructure is being decided not at the foundation-model layer (capital-constrained, oligopoly-dominated) but at the **cognition-infrastructure / eval-systems / trajectory-systems / verification / observability / synthetic-data-quality / memory / tool-use** layers — places where an obsessive operator with infrastructure expertise can do meaningful work without competing on training-run capital.

The IEP was already well-positioned on a subset of these areas. Phase A (completed 2026-05-15) shipped DR-010 widened-scope lock, Blueprints A/B/C, the Canonical Glossary, and `@intentsolutions/core@0.1.0` with full sigstore provenance — the contracts kernel that every downstream consumer depends on. The question this report answers is **which of the 20+1 areas warrant fresh epic-level investment in Phase B, which warrant deferral, and which fall outside IEP scope entirely**.

### 1.2 What the IEP is (one paragraph for context-cold readers)

The Intent Eval Platform is a five-repository OSS ecosystem under the Intent Solutions umbrella that converges on a shared Evidence Bundle schema. Each repo has its own license, CI, and release cycle; together they implement Blueprint A's "ONE BIG" architecture from DR-010. The five repos are: (a) **`intent-eval-core`** — canonical TypeScript contracts kernel covering the 13-entity domain model plus JSON Schemas plus Zod validators plus state machines, published as `@intentsolutions/core@0.1.0`; (b) **`intent-eval-lab`** — methodology, specs, Blueprints, glossary; (c) **`audit-harness`** — deterministic gates plus emit-evidence (escape-scan, crap-score, arch-check, harness-hash, bias-count, gherkin-lint); (d) **`j-rig-skill-binary-eval`** — behavioral judgment plus `@j-rig/rollout-gate` decision logic plus provider adapters; (e) **`intent-rollout-gate`** — thin GitHub Action shell delegating to `@j-rig/rollout-gate`. The convergence diagram is in the umbrella `README.md`. All five are Apache 2.0 as of v1.0.0 relicenses.

### 1.3 Origin story relevant to phase planning

DR-010 § 13.5 removed the customer-signal gate per acting-head-of-board override; Phase B is bandwidth-gated, not customer-signal-gated. § 13.6 removed external-pattern borrow constraints. The platform's positioning is no longer market-driven; the work is judged on technical merit + craft + contribution potential. This frames the entire audit below: **every per-area treatment asks "where is the field, where do we fall short, where can we contribute" — never "where is the market, where is the moat, what's the GTM"**.

### 1.4 Scope of this document

Twenty areas from the May 2026 advisories, plus one uniquely-accessible area (evaluator disagreement dataset). Each area gets the eight-subsection treatment specified in the program plan: definition, why it matters technically, current state in our stack, where we fall short, where we can build or contribute, field landscape (academic + frontier labs), field landscape (OSS + open ecosystem), where this could go (open problems). The treatment is honest where we fall short and specific where we can build — file paths, bead IDs, entity names, upstream contribution targets.

Foundation-model-level work (curriculum learning, compression, small-model research, mechanistic interpretability) is recorded in Appendix F as a parked personal-skill pillar. It is explicitly not IEP scope.

---

## § 2 — Platform state today

This section documents what each of the five IEP repos currently ships, in flight, and explicitly defers. Concrete file paths, bead IDs, and entity names where possible — verifiable facts only.

### 2.1 `intent-eval-core` — the kernel

**Status**: `@intentsolutions/core@0.1.0` published to npm 2026-05-17 with sigstore provenance. AAR at `intent-eval-core/000-docs/001-AA-AACR-release-v0.1.0-2026-05-17.md`. Five epics closed in the kernel sprint: iec-E01 (scaffold), iec-E02 (13 entities + `gate-result/v1` NORMATIVE), iec-E03 (JSON Schemas), iec-E04 (Zod validators), iec-E09 (NPM publishing).

**What's exposed**: type imports of `EvalSpec`, `EvalRun`, `GateResultV1` from `@intentsolutions/core`; JSON Schema imports for `v1/gate-result.schema.json`; Zod validator imports for `GateResultV1Schema`. Architecture rules enforce 8 forbidden internal-coupling patterns. The kernel intentionally contains zero execution code, zero judges, zero runtime — it is the contracts surface only.

**13 canonical entities** (per Blueprint B § 4): `EvalSpec`, `EvalSuite`, `EvalRun`, `EvalCase`, `GateResultV1`, `AssertionExpression`, `MatcherInputPattern`, `ScoringConfig`, `JudgeAdapter`, `Provider`, `CompositionDag`, `SessionTrace`, `EvidenceBundle`.

**Deferrals filed** (8 open beads in `iec-deferral-*`): A (AssertionExpression typed-class enum, Class-2 ISEDC required), B (MatcherInputPattern.structural payload spec), C (ScoringConfig fields beyond aggregation_rule), D (gate-result/v1 coverage element shape), E (ToolInvocationError.enum_class registry), F (CompositionDag wire format normative spec), G (tenant_id reservation decision — Architect W1), plus tighten-branch-protection and `iec-E10` (per-repo Blueprint C application) + `iec-E11` (boundary enforcement) staged.

### 2.2 `intent-eval-lab` — methodology + specs

**Status**: Phase A foundation merged to main 2026-05-15. Five normative documents on main: DR-010 (010), Blueprint A (011), Blueprint B (012), Blueprint C (013), Canonical Glossary (014). PR #56 landed audit cleanup including partner-name vendor-generic scrub, `.github/workflows/partner-name-guard.yml` CI guard, and `KNOWN-ISSUES.md` for operational footnotes. RTM + PERSONAS + JOURNEYS scaffolded per the audit-tests SOP.

**In-flight epics**: iel-E11 (replay fidelity RF-0..RF-4), iel-E12 (canonical runtime event taxonomy / `agent-loop-trace/v1`), iel-E13 (architecture boundary standards 3-doc cluster, P1), iel-E14 (operational doctrine bundle 4-doc cluster, P2), iel-E10 (sanitization spec for `agent-loop-trace/v1`, P2), iel-E04d (validation checklist for blueprint authors, P0), iel-E02d (runtime isolation + cost governance + observability, P0).

**Recent decisions**: ISEDC Session 4 widened the scope binding Q1=A (ONE BIG), Q2 (hybrid language — TS-primary signing surfaces, Python permitted ML internals), Q3 (unification thesis BINDING — every validator emits Evidence Bundle); § 13.5 customer-signal gate REMOVED; § 13.6 external-pattern non-borrow.

### 2.3 `audit-harness` — deterministic gates

**Status**: relicensed MIT → Apache 2.0 in v1.0.0 (see `audit-harness#32`). Published as `@intentsolutions/audit-harness` on npm. Six core scripts: `escape-scan.sh` (pre-commit allowlist enforcement), `crap-score.sh`, `arch-check.sh`, `harness-hash.sh` (hash-pinning policy files), `bias-count.sh`, `gherkin-lint.sh`. Each script emits structured output suitable for Evidence Bundle inclusion.

**In-flight**: iah-E01 (repo blueprint Blueprint C application, P0), iah-E02 (import @intentsolutions/core types, P1, blocked on kernel publish — NOW UNBLOCKED), iah-E07 (gate output → `gate-result/v1` emission), iah-E08 (provider credential PASS/FAIL gates, P1).

### 2.4 `j-rig-skill-binary-eval` — behavioral judgment

**Status**: relicensed MIT → Apache 2.0 in v1.0.0 (see `j-rig-skill-binary-eval#73`). TypeScript pnpm monorepo, Node 20+. Workspace packages including `@j-rig/core`, `@j-rig/rollout-gate`, judge + provider adapters. Behavioral evals (skill behavior contracts, output assertions) emit results that conform to the kernel's `gate-result/v1`.

**In-flight**: iaj-E01 (repo blueprint Blueprint C application, P0), iaj-E02 (migrate `@j-rig/core` schemas → `@intentsolutions/core` imports, P1, NOW UNBLOCKED), iaj-E06a (credential-redaction test fixture + CI gate, P1), iaj-E08 (j-rig observability hooks).

### 2.5 `intent-rollout-gate` — GHA shell

**Status**: relicensed MIT → Apache 2.0 (see `intent-rollout-gate#12`). Thin GitHub Action manifest at `action.yml` consuming Evidence Bundles + policy files to render a PASS/FAIL/WAIVE decision. M5.1 TypeScript runtime lock + MVP in flight on `feat/m5-typescript-runtime-lock-and-mvp`.

**In-flight**: iar-E01 (repo blueprint Blueprint C application, P0), iar-E02 (DR-002 runtime language Decision Record, P0), iar-consumer-migration (consume `@intentsolutions/core` for gate-result/v1 parsing, P1, NOW UNBLOCKED).

### 2.6 Cross-cutting state (bd workspace)

The bd canonical workspace lives at `~/000-projects/.beads/issues.jsonl` carrying all five repo prefixes (iec-, iel-, iah-, iaj-, iar-). Total bead count as of 2026-05-20: ~535 beads, of which 34 are `bd ready` (no active blockers). The three-layer mirror (bd ↔ GitHub Issue ↔ Plane LAB) is enforced via `bd-sync`; the JSONL workaround for the upstream auto-flush bug is mandatory per `intent-eval-lab/KNOWN-ISSUES.md`.

### 2.7 What the platform does NOT do (anti-goals from Blueprint A)

- We do not train foundation models.
- We do not host runtime infrastructure or compute for customers.
- We do not maintain a managed observability product (Phoenix/Langfuse posture).
- We do not own benchmark dataset hosting (HuggingFace / METR posture).
- We do not provide eval-as-a-service or human-in-the-loop annotation.

The platform's surface is **schemas + validators + state machines + gates + decision-logic + GHA**. Everything else is downstream consumer territory.

---

## § 3 — Methodology for this audit

### 3.1 Citation grounding (academic)

Semantic Scholar MCP `paper_bulk_search` ran against 16 seed queries spanning the 21 advisory areas with `min_citation_count` thresholds tuned per area to surface defensible bedrock without flooding on noise. Results captured in `000-RR-BIBL-shared-bibliography-2026-05-20.md`. Per-area citation rule: at least three published papers per area where the academic surface exists; where the surface is sparse (e.g., OpenTelemetry GenAI conventions — 0 hits) we acknowledge "field is community/standards-driven, not paper-driven" and pivot to the OSS landscape.

### 3.2 OSS + frontier-lab landscape (technical state of practice)

Twelve OSS projects fetched directly via WebFetch on 2026-05-20 capturing verbatim license, last release date, semantic-convention claims, governance, and integration surface. Results in `000-RR-COMP-ecosystem-landscape-2026-05-20.md`. Frontier-lab material (Anthropic, OpenAI, DeepMind, METR, UK AISI, Apollo, Redwood) drawn from the published-paper bibliography + general public knowledge — no scraping of internal blog drafts or paywalled material.

### 3.3 Per-area treatment structure

Each of the 21 areas in § 4 gets exactly eight subsections in fixed order: (1) Definition; (2) Why it matters technically; (3) Current state in our stack; (4) Where we fall short; (5) Where we can build or contribute; (6) Field landscape — academic / labs; (7) Field landscape — OSS + open ecosystem; (8) Where this could go — open problems. Each subsection is 1-3 short paragraphs; "Not yet relevant because X" is preferred over omission when a subsection lacks substance.

### 3.4 What is explicitly out of scope for this document

- Market sizing, customer acquisition, GTM, pricing comparisons.
- Moat / differentiation / "winning" language.
- Foundation-model training research (parked in Appendix F).
- Speculative roadmapping past Phase B.
- Reproductions of upstream work that already exists in mature form.

### 3.5 Verification disciplines applied

- DR-004 S1Q2 partner-name vendor-generic discipline — every named example uses vendor-generic placeholders or refers to publicly-attributed work; the `partner-name-guard.yml` workflow will gate this document on commit.
- DR-010 § 10 predicate-URI discipline — no references to `labs.intentsolutions.io` in any predicate-URI capacity (CISO binding).
- No internal-context leaking — partner specifics, customer specifics, financial specifics excluded.

### 3.6 Methodology limitations (what this audit cannot do)

This document is an auditor's audit — its conclusions are bounded by the search methodology used, the time-window of the bibliography, and the operator's prior commitments. Five limitations are worth naming explicitly so the operator and ISEDC Session 5 can weigh them.

**Limitation 1 — Bibliography sample bias.** Semantic Scholar `paper_bulk_search` with citation-threshold filtering oversamples high-citation work. Work published in the last 60 days is systematically under-represented because citations take time to accumulate. For frontier topics (inference-time compute, multi-agent state) this means newest preprints may be missed.

**Limitation 2 — OSS landscape recency.** WebFetch captures pages as of 2026-05-20. Active projects (Inspect AI, Langfuse, OpenInference) ship weekly; specific claims about license, capability, or convention status may be stale within months. Verify before any binding commitment.

**Limitation 3 — Frontier-lab opacity.** Anthropic, OpenAI, Google DeepMind publish a fraction of their work; internal research informs their products but isn't publicly available. The audit relies on published material plus reasonable inference. Material that is internal-only at these labs may invalidate inferred contribution surfaces.

**Limitation 4 — Implementation-effort estimates.** The work-block estimates in § 7 and Appendix G are first-order — they assume no Class-2 ISEDC blockers, no external coordination delays, and operator full focus. Real-world execution typically inflates by 30-50% under typical multi-program operator load.

**Limitation 5 — Patent / IP surface unverified.** The audit names contribution paths to multiple upstream projects (OTel, OpenInference, Inspect AI, etc.) but does not verify whether `gate-result/v1` or `agent-loop-trace/v1` carry patent-encumbered material that would constrain contribution. GC seat at ISEDC Session 5 should weigh in before any upstream submission.

These limitations do not undermine the audit's findings — they bound them. The Phase B Framing Memo should reference these limitations explicitly in its risk register.

---

## § 4 — The 21 gap areas in full depth

The 21 areas are ordered as in the advisory (1-20) plus area 21 (evaluator-disagreement dataset, uniquely-ours). Each area is treated in the standard eight-subsection structure. Cross-references to Blueprints + Glossary entries cited where applicable.

### Area 1 — Operational Trajectories

**1. Definition.** Capture, structure, and persistence of agent operational behavior over time: the sequence of model invocations, tool calls, observations, reasoning state transitions, and outcomes that constitutes a single agent run. Distinct from "traces" (which are observability-side) by carrying enough semantic structure to be **replayed, classified, and graded**, not just inspected. The unit is the trajectory; the trajectory carries entity references to `SessionTrace` and `EvidenceBundle` from the kernel.

**2. Why it matters technically.** Production agents fail in ways that aggregate metrics can't surface — silent reasoning loops, partial tool-use recoveries, hidden state mutations. Operational trajectories are the substrate that lets you say "this run failed because at step 47 the agent re-tried the same tool with the same arguments after a 429" rather than "success_rate dropped 3%." Every higher-order capability (replay fidelity, reliability scoring, regression detection, drift monitoring) sits on top of a real trajectory format.

**3. Current state in our stack.** iel-E12 (Canonical runtime event taxonomy — `agent-loop-trace/v1`) is the dedicated epic; Blueprint B § 4 declares `SessionTrace` as one of the 13 canonical entities. The current trajectory representation is the `SessionTrace` JSON Schema in `intent-eval-core/schemas/v1/session-trace.schema.json` plus the validators in `validators/v1/session-trace-v1.ts`. Blueprint B § 7 carries the normative `gate-result/v1` spec which references SessionTrace; iel-E10 carries the sanitization spec for `agent-loop-trace/v1` (sensitive-data redaction before persistence).

**4. Where we fall short.** SessionTrace exists as a kernel entity but the event taxonomy under `agent-loop-trace/v1` is still being normatively specced. We do not yet have: (a) a canonical event-type enumeration covering the full agent loop (model-invocation, tool-call, tool-response, retrieval, observation, reasoning-step, plan-mutation, error-recovery); (b) a sanitization pipeline that runs before persistence; (c) integration tests against the major external trajectory formats (SWE-bench's eval logs, OSWorld's screenshot+action streams, tau-bench's historical_trajectories). The gap between "we have a schema" and "we can absorb a SWE-bench run and emit a SessionTrace" is non-trivial.

**5. Where we can build or contribute.** Build-in-our-repos: complete iel-E12 with explicit event-type enum committed to Blueprint B § 7.X; complete iel-E10 sanitization spec; add integration-test fixtures importing real SWE-bench, OSWorld, tau-bench trajectories; tighten the `intent-eval-core/schemas/v1/session-trace.schema.json` to embed event-type discriminator. Upstream contribution: the OpenTelemetry GenAI SIG semantic conventions are in Development status with no canonical agent-trajectory shape — propose `gen_ai.agent.trajectory` namespace conventions referencing the SessionTrace event taxonomy. This is a high-leverage contribution surface because the SIG has no competing proposal we can detect.

**6. Field landscape — academic / labs.** Trajectory-as-exemplar prompting (Synapse, `eaa78538…`, ICLR 2024) and trajectory replay for agent training (APIGen-MT, `fb122b2e…`, 2025) treat trajectories as data for fine-tuning, not as observability artifacts. AgentRx (`0515b697…`, 2026, 12 cites) explicitly diagnoses agent failures from execution trajectories — closest academic precedent to operational use. AgenTracer (`7fdbdd7f…`, 33 cites, 2025) attacks who-is-inducing-failure in agentic systems, also trajectory-grounded. Anthropic and DeepMind published material treats trajectory replay as a training-time concern; METR's time-horizon methodology requires trajectory-level data but their `runs.jsonl` is task-summary, not full trajectory.

**7. Field landscape — OSS + open ecosystem.** OpenInference defines per-span attributes for LLM invocation but no formal trajectory aggregation. OpenLLMetry upstreams to OTel, no trajectory-level abstraction. SWE-bench (`princeton-nlp/SWE-bench`, MIT, last update 2025-01-13) stores Docker build + eval logs in `evaluation_results/` — these are the raw material for a SessionTrace but not the format. OSWorld (`xlang-ai/OSWorld`, Apache 2.0, OSWorld-Verified 2025-07-28) saves screenshots + actions + video — richer than logs but more proprietary. tau-bench (`sierra-research/tau-bench`, MIT) ships `./historical_trajectories` directories as the closest "trajectory artifact" precedent. None of these has a formally-versioned trajectory schema.

**8. Where this could go — open problems.** (a) Lossless trajectory representation that survives format-conversion between SWE-bench, OSWorld, tau-bench, and our SessionTrace. (b) Canonical event-type ontology — the question "is `Plan` an event or a derived view over multiple `ReasoningStep` events" is unresolved. (c) Composability — can a multi-agent run be represented as nested trajectories, or does it require a separate `CompositionDag` (Blueprint B entity)? `iec-deferral-F` (CompositionDag wire format) is the relevant deferred decision. (d) Sanitization invariants — what does sanitized-trajectory mean formally? (e) Contributions to OTel GenAI SIG to land a canonical agent-trajectory span shape.

### Area 2 — Eval Systems (binary pass/fail)

**1. Definition.** Behavioral evaluation of agent or model output against a specification: given an input, did the system produce an output that satisfies the contract? The contract may be an assertion list, a judge prompt, a similarity threshold, or a structured matcher. Binary in the outcome but compositional in the structure — eval systems combine many sub-assertions into the final pass/fail.

**2. Why it matters technically.** Without a stable, composable, deterministically-replayable eval format, every higher-order claim about agent behavior collapses. The eval format is the contract between "the agent did X" and "the system says X is acceptable." Every reliability claim, drift claim, regression claim, attestation claim depends on the eval result being a structured, signed, replayable artifact.

**3. Current state in our stack.** This is our strongest area. The kernel ships `EvalSpec`, `EvalSuite`, `EvalRun`, `EvalCase`, `GateResultV1`, `AssertionExpression`, `MatcherInputPattern`, `ScoringConfig` as canonical entities (`iec-E02` closed). `j-rig-skill-binary-eval` is the behavioral judgment surface; `audit-harness` is the deterministic-gate surface; both emit `gate-result/v1`-compliant outputs that the `intent-rollout-gate` GHA consumes. Blueprint B § 7 carries the normative `gate-result/v1` predicate contract.

**4. Where we fall short.** Several deferred specs gate full coverage: `iec-deferral-A` (AssertionExpression typed-class enum — Class-2 ISEDC required), `iec-deferral-B` (MatcherInputPattern.structural payload), `iec-deferral-C` (ScoringConfig fields beyond aggregation_rule — weights, thresholds), `iec-deferral-D` (gate-result/v1 coverage element shape lockup), `iec-deferral-E` (ToolInvocationError.enum_class registry). We also lack — outside the kernel — a canonical eval-result interoperability layer. Inspect AI emits its own results; Promptfoo emits its own; our `gate-result/v1` does not yet have an adapter pattern for either.

**5. Where we can build or contribute.** Build: close the five `iec-deferral-*` Class-2 specs; add bidirectional adapters between `gate-result/v1` and (Inspect AI results, Promptfoo results) in `audit-harness` or in a new `intent-eval-adapters` package; tighten the JSON Schema in `intent-eval-core/schemas/v1/gate-result.schema.json` once deferrals close. Upstream contribution: Inspect AI is MIT-licensed and government-backed (UK AISI); a `gate-result/v1` ↔ Inspect-result adapter is a defensible contribution to either repo. Promptfoo is now part of OpenAI but stays MIT — same adapter pattern applies.

**6. Field landscape — academic / labs.** This area is mature and well-cited; we don't break new ground. The bibliography backbone: Zheng MT-Bench (`a0a79dad…`, **8440 cites**, NeurIPS 2023) defined the LLM-as-judge benchmark format; survey papers like Li et al. "A Survey on LLM-as-a-Judge" (`e2442428…`, 1319 cites, 2024) consolidate the field; the LiveBench contamination-limited benchmark (`774d01e1…`, 127 cites, ICLR 2025) addresses dataset contamination; MixEval (`45ad78df…`, 79 cites, NeurIPS 2024) addresses crowd-wisdom aggregation. Foundational Autoraters (`6c5ae8a0…`, 88 cites, EMNLP 2024) targets the autorater quality problem.

**7. Field landscape — OSS + open ecosystem.** Inspect AI (UK AISI, MIT, 5714 commits, 200+ pre-built evals) is the strongest standards-track precedent. Promptfoo (now OpenAI subsidiary but MIT, v0.121.11, 2026-05-08) is the closest CI/CD-integration analog. DSPy (Stanford, MIT, v3.2.1, 2026-05-05) is orthogonal — programming model not evaluation surface — but its `Assertions` (Dec 2023) work is methodologically relevant.

**8. Where this could go — open problems.** Most of the work here is **citation-grounding**, not new construction. The single open construction problem is **eval-result interoperability**: if a customer runs Inspect AI for eval A, our judge for eval B, and a Promptfoo CI suite for eval C, can all three Evidence Bundles be reconciled? `gate-result/v1` is positioned to be the common envelope but the field has not yet converged.

### Area 3 — Agent Observability

**1. Definition.** Runtime instrumentation, trace emission, structured logging, and analysis tooling for agentic LLM systems. Spans, attributes, metrics, exceptions — the OpenTelemetry vocabulary applied to agent runs. Distinct from operational trajectories (Area #1) by being **always-on production telemetry** rather than structured artifact emission.

**2. Why it matters technically.** Agents in production fail in ways that resemble distributed systems failures (latency cascades, retry storms, tool-call timeouts) more than they resemble ML model failures (accuracy drops, prediction confidence shifts). Without OpenTelemetry-grade observability, every other capability — debugging, drift detection, alerting, capacity planning, cost attribution — is degraded.

**3. Current state in our stack.** iel-E12 (Canonical runtime event taxonomy) overlaps strongly with this area; iel-E02d (runtime isolation + cost governance + observability, P0) is the operationally-focused epic. iah-E07 + iaj-E08 + iar-E02 carry per-repo observability hooks. The platform does not host a managed observability product (anti-goal from Blueprint A) but defines the canonical event/span shape that downstream consumers emit.

**4. Where we fall short.** No formal `gen_ai.agent.*` semantic-convention proposal yet submitted to OTel SIG. No reference instrumentation library for the major LLM frameworks (LangChain, LangGraph, CrewAI, Claude Agent SDK). No integration tests against OpenInference's existing semantic conventions. No worked examples of "here is a trace from our reference agent → here is the resulting EvidenceBundle." The agent-observability story is partial — schema-level only.

**5. Where we can build or contribute.** Upstream contribution dominates here. OpenTelemetry GenAI SIG semantic conventions are in **Development status** as of May 2026 with model + agent spans defined but not yet stable; `OTEL_SEMCONV_STABILITY_OPT_IN` is the gating flag. Native contribution targets: (a) propose `gen_ai.agent.trajectory.*` attributes in the SIG; (b) submit reference instrumentation for one of the major frameworks; (c) coordinate with OpenInference (Arize-ai, Apache 2.0) on convention alignment. Build-in-our-repos: complete iel-E12, complete iah-E07/iaj-E08/iar-E02, add a `@intentsolutions/otel-shim` package that emits compliant spans.

**6. Field landscape — academic / labs.** Sparse. The only peer-reviewed paper on the specific surface as of May 2026 in our search is AgentOps (`3d6b189c…`, 21 cites, 2024). This is a vacuum — academic literature is several years behind the practitioner state of practice. Anthropic, OpenAI, DeepMind have not published on agent observability in any formal way; the work is happening on OTel SIG GitHub and CNCF working groups.

**7. Field landscape — OSS + open ecosystem.** Active and diverse. **OpenInference** (Arize-ai, Apache 2.0, 30+ Python + 9 TS + 4 Java + 4 Go instrumentation packages, last release 2026-05-18) defines its own AI-specific semantic conventions complementary to OTel — the strongest extant convention. **OpenLLMetry** (Traceloop, Apache 2.0, 7.1k stars, v0.60.0 on 2026-04-19) explicitly upstreams its conventions to OTel — a model for how to convert practice into SIG-ratified spec. **Phoenix** (Arize-ai, **Elastic License 2.0**, patent-flagged) uses OpenInference + OTel — *not* an integration target because of license incompatibility, but a feature reference. **Langfuse** (MIT core, ee enterprise, v3.174.1 on 2026-05-13) ships its own custom trace format with OTel integration mentioned — useful as feature-matrix reference.

**8. Where this could go — open problems.** (a) Canonical `gen_ai.agent.trajectory` semantic conventions ratified by OTel SIG. (b) Multi-agent span correlation — how do parent/child relationships work across composed agent runs? (c) Cost-attribution attributes — `gen_ai.usage.*` covers model invocation but not tool execution. (d) Reliability instrumentation — how to capture "this agent failed in a way that should retry vs not retry" in the span format. (e) The relationship between an agent observability span and an attestation envelope (`gate-result/v1` carries the attestation envelope; can the span be derived from it deterministically?).

### Area 4 — Synthetic Data Quality

**1. Definition.** Programmatic generation of training, evaluation, or testing data — typically via LLM-driven synthesis from seed prompts or rule-based templates. "Quality" here refers to operational characteristics of the generated data: diversity, novelty, lack of distribution collapse, faithfulness to declared intent, downstream-training utility. Adjacent to but distinct from data augmentation (which transforms existing data) and to RAG (which retrieves at inference time).

**2. Why it matters technically.** Synthetic data is increasingly the substrate for model fine-tuning, evaluator training, and benchmark construction. Quality failures (entropy collapse, mode collapse, hidden-distribution skew, contamination) silently undermine every downstream use. A reliability claim on a model fine-tuned on synthetic data is only as defensible as the synthetic data's quality characterization. For our platform: every eval suite that uses generated test cases has a synthetic-data-quality dependency.

**3. Current state in our stack.** No formal synthetic-data-quality scoring in the kernel. The relevant entities (`EvalSuite`, `EvalCase`, `ScoringConfig`) carry hooks but no quality metadata field. `iaj-E09` is the proposed new epic for "synthetic cognition quality scoring" in `j-rig-skill-binary-eval` per § 7 of this report.

**4. Where we fall short.** We have no quality-score field on `EvalSuite` or `EvalCase`. We have no provenance chain linking a generated case back to its seed + generator-model + generation-timestamp. We have no entropy / diversity / collapse-detection scoring built into the kernel or the harness. We have no convention for declaring "this suite was synthetically generated" vs "this suite is human-curated."

**5. Where we can build or contribute.** Build: (a) new fields on `EvalCase` for `synthesis_provenance` (generator model, seed, timestamp, version) and `quality_score` (diversity, novelty, collapse-risk metrics); (b) new `audit-harness` script `synth-quality.sh` implementing entropy + n-gram-diversity + judge-disagreement-spread scoring; (c) `iaj-E09` per-domain quality scoring in j-rig. Upstream contribution: the Prismatic Synthesis paper's methodology (gradient-based diversification, `b71a9a4236…`, 34 cites, 2025) and the MathSmith reinforced-policy approach (`3da24e1feaa1…`, 17 cites, AAAI 2025) are referenced — we can contribute open implementations that consume the academic methods.

**6. Field landscape — academic / labs.** Active. Smaller, Weaker, Yet Better (`41a4234a…`, 71 cites, ICLR 2025) — compute-optimal sampling for training LLM reasoners on synthetic data. Prismatic Synthesis (`b71a9a4…`, 34 cites, 2025) — gradient-based diversification. MegaMath (`7a070cec…`, 37 cites, 2025) — pushing limits of open math corpora. MathSmith (`3da24e1f…`, 17 cites, AAAI 2025) — extreme-hard problem forging. Demystifying Reinforcement Learning in Agentic Reasoning (`8196e314…`, 25 cites, 2025). DeepMind and Anthropic publish heavily here for training-loop reasons; their methods center on diversity-maximizing sampling and curriculum-aware filtering.

**7. Field landscape — OSS + open ecosystem.** Less mature than the academic side. DSPy's Assertions can serve as quality filters at synthesis time. No dedicated OSS project at "synthetic data quality scoring" surface that's both Apache/MIT and broadly adopted. Datasets-library work at HuggingFace covers persistence + versioning but not quality.

**8. Where this could go — open problems.** (a) A canonical quality-scoring schema attached to synthetic test suites that survives toolchain handoff. (b) Provenance chain that survives data-format conversion (CSV → JSONL → parquet). (c) Distribution-collapse detection that's domain-agnostic. (d) Quality-cost tradeoff metrics — generating 10K synthetic cases at quality-score 0.7 vs 1K cases at 0.95 — when does each win? Open contribution surface: this is one of the better "build-in-our-repos because nobody's done it well in OSS" calls in the audit.

### Area 5 — Trajectory Replay

**1. Definition.** The capacity to re-execute, in a faithful or partially-faithful manner, a previously-captured agent trajectory — for debugging, regression testing, what-if analysis, or methodology validation. Distinct from naive log-replay (which re-emits log lines) by the requirement that re-execution faithfully reconstructs at least the **semantic state** of the original run.

**2. Why it matters technically.** Without trajectory replay, every failed agent run is a one-shot forensic exercise. With replay, failures become reproducible artifacts that can be regression-tested, attached to bug reports, and used to verify fixes. Replay also enables a class of evaluation impossible without it: "given trajectory T, would model M' have behaved differently?" — counterfactual evaluation.

**3. Current state in our stack.** iel-E11 (Replay fidelity levels RF-0..RF-4) is the dedicated epic, currently P0 and in-flight. The proposed five levels: RF-0 (no replay, log-only), RF-1 (action-replay, no state reconstruction), RF-2 (semantic-state replay with tool-call mocking), RF-3 (full deterministic replay with provider-pinning), RF-4 (cross-model counterfactual replay). The level taxonomy lives in `intent-eval-lab/specs/replay-fidelity-v1.md` (drafted, not yet on main).

**4. Where we fall short.** The RF-0..RF-4 taxonomy is a proposal, not a normative spec. We have no reference implementation of RF-1 or higher. We have no integration with SWE-bench's `evaluation_results/` such that we could classify SWE-bench replay as "RF-1" or "RF-2". We have no validated literature mapping — does our taxonomy match what existing replay work (Synapse, APIGen-MT, agent-training trajectory work) actually achieves, or are we inventing terminology that doesn't connect?

**5. Where we can build or contribute.** Build: (a) close iel-E11 with a normative replay-fidelity-v1.md on main; (b) implement reference RF-1 + RF-2 in `intent-eval-core` (state-machine driven, no execution code per kernel anti-goal — so reference logic in lab, not kernel); (c) integrate with SWE-bench + OSWorld + tau-bench as classification test cases; (d) wire `gate-result/v1` to declare the replay fidelity level achieved during a verification gate. Upstream contribution: REAL (`1026a4def94…`, 26 cites, 2025) is the strongest existing benchmark for deterministic-replay agent testing — our spec could explicitly map to REAL's findings.

**6. Field landscape — academic / labs.** Synapse (`eaa78538…`, 137 cites, ICLR 2024) — trajectory-as-exemplar prompting, replay used at training time. APIGen-MT (`fb122b2e…`, 116 cites, 2025) — multi-turn data generation via simulated interplay (training-side replay). AgentRx (`0515b697…`, 12 cites, 2026) — diagnosing failures from execution trajectories (forensic replay). REAL (`1026a4de…`, 26 cites, 2025) — deterministic simulations of real websites for agent benchmarking. AgenTracer (`7fdbdd7f…`, 33 cites, 2025) — who induces failure in agentic systems.

**7. Field landscape — OSS + open ecosystem.** SWE-bench (`princeton-nlp/SWE-bench`, MIT) stores eval logs in `evaluation_results/` enabling forensic replay but not action-replay. OSWorld (`xlang-ai/OSWorld`, Apache 2.0, OSWorld-Verified 2025-07-28) saves screenshots + actions + video; replay is "video review" not action-replay. tau-bench's `./historical_trajectories` is closer to RF-1 but without explicit determinism guarantees. No OSS project ships with explicit RF-0..RF-N classification.

**8. Where this could go — open problems.** (a) Provider-pinning protocols — how do you achieve RF-3 when foundation-model providers don't expose deterministic-seed APIs? (b) Cross-provider counterfactual replay (RF-4) — what semantic equivalence guarantees can be made? (c) Replay-fidelity certification — what evidence proves a replay was RF-2 vs RF-3? (d) Integration with attestation envelopes — should `gate-result/v1` carry the replay-fidelity-level achieved during the gate? Likely yes; this is a deferred decision worth resolving in iel-E11.

### Area 6 — Verifier Systems (generator/checker split)

**1. Definition.** Architecturally separating the LLM that generates candidate outputs from the LLM (or non-LLM checker) that verifies whether those outputs satisfy the contract. The verifier is **independent** of the generator in some technical sense — different model, different prompt, different family, or non-LLM rule-based — to reduce correlated failures.

**2. Why it matters technically.** If the same model both generates and grades, correlated failures (the same blind spot in both roles) inflate apparent quality. Independent verification is the bedrock for any reliability claim. The deeper the independence (different model family vs different prompt), the stronger the claim. Process Reward Models (PRMs) are a verifier-systems instance; LLM-as-judge with cross-family models is another; deterministic harness gates (escape-scan, crap-score) are the strongest form because the verifier isn't an LLM at all.

**3. Current state in our stack.** `audit-harness` IS the canonical non-LLM verifier in our platform — escape-scan, crap-score, arch-check, harness-hash are deterministic gates that emit `gate-result/v1` outputs. `j-rig-skill-binary-eval` is the LLM-judge verifier. There is no formal entity in the kernel called `Verifier` — the role is implicit. `iaj-E11` is the proposed new epic for "verifier systems (generator/checker split)" per § 7.

**4. Where we fall short.** No `Verifier` first-class entity in the kernel — verifier identity, independence-class, and verification metadata are not currently captured in `gate-result/v1` beyond `tool` and `judge` fields. No declared **independence-class** taxonomy (same-prompt / different-prompt / different-model / different-family / non-LLM-rule) attached to verification results. No academic-grounded operational definition of "independent" verifier. No worked examples of generator-checker pairings with empirical correlation measurements.

**5. Where we can build or contribute.** Build: (a) add `Verifier` first-class entity to Blueprint B § 4 and the kernel (new bead `iec-E07.1` or fold into existing kernel work); (b) declare `independence_class` enum on `gate-result/v1` distinguishing same-family / cross-family / non-LLM-rule verification; (c) `iaj-E11` ships independent-judge-pairings in j-rig with measured cross-judge correlation; (d) document existing audit-harness gates as canonical non-LLM verifiers — they are, but we don't say so in the literature voice. Upstream contribution: Process Reward Models (`b670078b…`, Survey, 20 cites, 2025) is the most-cited recent survey; engaging with that community via implementation references is the contribution path.

**6. Field landscape — academic / labs.** Active and well-cited. Sample, Scrutinize and Scale (`b67c8d21…`, 37 cites, ICML 2025) — inference-time search by scaling verification. When To Solve, When To Verify (`d170e69d…`, 30 cites, 2025) — compute-optimal problem solving with generative verification. JETTS (`5f2dbd43…`, 33 cites, ICML 2025) — judges as test-time-scaling evaluators. Putting the Value Back in RL (`4db3afe0…`, 14 cites, 2025) — unifying reasoners with verifiers. Process Reward Models Survey (`b670078b…`, 20 cites, 2025) — comprehensive review. OpenAI and DeepMind have published heavily on PRM training and verifier scaling.

**7. Field landscape — OSS + open ecosystem.** Inspect AI's model-graded evaluations are the closest precedent for cross-model verification in an OSS framework. Promptfoo's grader configurability allows specifying alternate models for judging. DSPy assertions are non-LLM rule-based verifiers but not framed as such. No OSS project ships an explicit `Verifier` first-class abstraction with independence-class metadata.

**8. Where this could go — open problems.** (a) Operational definition of "independent" verifier — is same-family-different-prompt enough? Same-model-different-seed? The empirical literature has not converged. (b) Cost-quality tradeoff for verifier independence — non-LLM rules are cheapest and strongest but cover narrow surfaces; cross-family judges are expensive. (c) Verifier-of-verifier — meta-verification with bounded cost. (d) Composition of multiple verifiers — how does an `EvalRun` declare "passed if (gate-A AND gate-B AND judge-C AND judge-D-from-different-family) is true"?

### Area 7 — Memory Systems (broader than poisoning)

**1. Definition.** Persistent storage, retrieval, aging, and integrity-protection mechanisms for agent state across runs and conversations. Covers conversation memory (long context handling), retrieval-augmented generation (RAG) for memory rather than knowledge, experiential memory (lessons-learned), procedural memory (workflow re-use), and the failure modes of all of the above (poisoning, contamination, drift).

**2. Why it matters technically.** Production agents that persist memory across runs introduce categorically new attack surfaces and failure modes compared to stateless agents. Memory poisoning is the most-publicized failure but not the only one — memory aging (stale facts that the agent acts on), memory contamination (retrieved memories from prior tenants), memory growth (unbounded context), and retrieval failures (missing the relevant memory) all degrade reliability. Memory is also the substrate for personalization, long-running workflows, and multi-session continuity.

**3. Current state in our stack.** Partial. The kernel does not currently have a `Memory` first-class entity — memory state would be carried inside `SessionTrace` events or in adjacent storage. `iec-E08` is the proposed new epic "Memory systems (broadened — poisoning + retrieval + aging)" per § 7. The platform's anti-goal posture says we do not host memory infrastructure for customers, but we do declare the schema.

**4. Where we fall short.** No `Memory` or `MemoryStore` entity in the kernel. No `memory_poisoning_risk` or `memory_age` attribute on gate-result/v1. No spec for how memory state should be represented in trajectories. No threat model document distinguishing memory-poisoning attacks from prompt-injection attacks from RAG-corpus-poisoning attacks. No standard for declaring "this gate verified the agent's memory was not poisoned at run-time."

**5. Where we can build or contribute.** Build: (a) `iec-E08` adds `Memory`, `MemoryStore`, `MemoryItem` entities to Blueprint B § 4 covering the four memory-failure axes (poisoning, aging, contamination, growth); (b) gate-result/v1 carries a `memory_integrity_class` field with options like `verified_clean`, `untested`, `flagged_drift`, `flagged_poisoning_risk`; (c) Cluster C threat-model document at `intent-eval-lab/specs/memory-threat-model-v1.md` mapping the academic threat literature to defensive postures we can verify. Upstream contribution: AgentPoison (`b6948a9e…`, 293 cites) is the foundational paper — a reference defense implementation in OSS form is a high-leverage contribution. Mem0 (`1d9c21a0…`, 319 cites, ECAI 2025) and Zep (`12407be4…`, 161 cites, 2025) are the leading OSS memory frameworks; adapter patterns to verify memory state in either would be welcome contributions to either project or to ours.

**6. Field landscape — academic / labs.** Robust. AgentPoison (`b6948a9e…`, 293 cites, NeurIPS 2024) — red-teaming via poisoning memory or knowledge bases (the foundational paper). MemoryGraft (`b1d80b2e…`, 23 cites, 2025) — persistent compromise via poisoned experience retrieval. CtrlRAG (`b308393d…`, 4 cites, 2025) and NeuroGenPoisoning (`a776dcb6…`, 4 cites, 2025) — RAG poisoning attacks. On the architectural side: LoCoMo (`0bf3a186…`, 432 cites, ACL 2024) — Very Long-Term Conversational Memory; Mem0 (`1d9c21a0…`, 319 cites, ECAI 2025); BABILong (`b47507f1…`, 203 cites, NeurIPS 2024) — testing limits of long context; Zep (`12407be4…`, 161 cites, 2025) — temporal knowledge graph; "Memory in the Age of AI Agents" survey (`d362b761…`, 144 cites, 2025); ArcMemo (`eff7efaf…`, 17 cites, 2025); LEGOMem (`bf675da7…`, 18 cites, 2025); G-Memory (`daa9bcf3…`, 55 cites, 2025).

**7. Field landscape — OSS + open ecosystem.** Mem0 (production-ready long-term memory) and Zep (temporal KG) are the leading OSS memory frameworks — both Apache or MIT, both actively maintained. Phoenix's eval surface includes retrieval evaluation but its ELv2 license blocks deep integration. LangChain and LangGraph carry memory abstractions but neither formally specs memory-integrity properties. No OSS project formally specs the four-axis memory-failure taxonomy.

**8. Where this could go — open problems.** (a) Memory integrity attestation in `gate-result/v1` — what evidence suffices? (b) Operational definitions of memory-poisoning vs memory-aging vs memory-contamination — boundaries are not consensus. (c) Memory provenance — every memory item carries enough provenance to recover its trustworthiness lineage. (d) Memory unlearning — verified removal of specific items, important under privacy regulation. (e) Multi-tenant memory isolation — relates to `iec-deferral-G` (tenant_id reservation).

### Area 8 — Tool-Use Training (sequencing / recovery)

**1. Definition.** The capability of an LLM agent to correctly select, invoke, sequence, and recover from external tools (function calls, API calls, MCP servers, code execution, retrieval, etc.). "Training" here includes both the model-side fine-tuning that develops the capability and the eval-side methodology that measures it. Recovery covers handling of tool failures, partial responses, ambiguous results, and the meta-decision to abandon a tool and try another.

**2. Why it matters technically.** Tool-use is the dominant agent behavior in production. Most production agent failures are tool-use failures — wrong tool selected, right tool with wrong arguments, partial response misinterpreted, timeout handled badly, retry storm. Without measurable tool-use quality, agent reliability claims are vapor. Tool-use also intersects with security (tool injection attacks), cost (over-eager tool calling), and observability (every tool call is a span).

**3. Current state in our stack.** Partial. The kernel has `JudgeAdapter`, `Provider` entities but no formal `Tool` or `ToolInvocation` entity — these would be carried inside `SessionTrace` events. `iec-deferral-E` (ToolInvocationError.enum_class registry) is the relevant deferred decision. `iel-E14c` (operational doctrine bundle, P2) carries sandbox-related material. `iaj-E13` is the proposed new epic for "tool-use training (sequencing / recovery / uncertainty)" per § 7.

**4. Where we fall short.** No `Tool`, `ToolInvocation`, `ToolInvocationError` as first-class entities. No taxonomy of tool-use failure modes that connects to `gate-result/v1`. No integration tests against MCP-Bench (`59fc74ab…`, 58 cites, 2025), MCPToolBench++ (`153e3227…`, 24 cites, 2025), or TRAJECT-Bench (`f7a42726…`, 11 cites, 2025) — three recent academic benchmarks for tool-use that we should be expressible against. No worked example of "verify tool-use quality of this agent run via Evidence Bundle."

**5. Where we can build or contribute.** Build: (a) close `iec-deferral-E` with ToolInvocationError.enum_class registry; (b) add `Tool` + `ToolInvocation` first-class entities in Blueprint B § 4 + kernel; (c) `iaj-E13` ships sequencing-quality + recovery-quality + uncertainty-handling judges in j-rig; (d) integration test fixtures importing MCP-Bench, TRAJECT-Bench. Upstream contribution: MCPToolBench++ is a notable benchmark with explicit MCP-server-protocol grounding — an adapter from `gate-result/v1` to MCPToolBench++-compatible result schema is a defensible contribution. Anthropic-driven MCP ecosystem is the highest-leverage upstream surface.

**6. Field landscape — academic / labs.** Highly active. xLAM (`a75da880…`, 103 cites, 2024) — large action models family for AI agent systems. Tool Learning in the Wild (`ca96d3b2…`, 64 cites, WWW 2025). Granite Function-Calling (`cbde6f07…`, 58 cites, EMNLP 2024). TinyAgent (`ff052499…`, 45 cites, EMNLP 2024). NESTFUL (`5fc3ea33…`, 39 cites, EMNLP 2024) — nested API calls. Compositional Instruction Tuning for Multi-turn FC (`1b50041b…`, 35 cites, ICLR 2024). Magnet (`4d4c46ba…`, 25 cites, ACL 2025) — multi-turn synthesis via graph translation. MCP-Bench (`59fc74ab…`, 58 cites, 2025). MCPToolBench++ (`153e3227…`, 24 cites, 2025). TRAJECT-Bench (`f7a42726…`, 11 cites, 2025). Agentic Reasoning + Tool Integration via RL (`d804b642…`, 76 cites, 2025). Advancing Tool-Augmented LLMs via Meta-Verification (`b1f92aed…`, 14 cites, KDD 2025). EvoTool (`3bb05e5e…`, 11 cites, 2026) — self-evolving tool-use policy.

**7. Field landscape — OSS + open ecosystem.** MCP (Model Context Protocol, Anthropic-led) is the rising de-facto standard for tool exposure. MCP servers proliferate; benchmarks (MCPToolBench++, MCP-Bench) exist. LangChain + LangGraph + CrewAI ship tool-abstraction frameworks but with framework-specific shapes. OpenInference's tool-related conventions are evolving. Promptfoo can grade tool-use. Inspect AI explicitly supports tool-use evaluation. SWE-bench is implicitly a tool-use benchmark (agents must invoke editors, test runners, etc.). OSWorld and tau-bench are explicit tool-use benchmarks.

**8. Where this could go — open problems.** (a) Cross-tool semantic conventions — what counts as "same tool" across vendors? (b) Tool-use failure recovery taxonomy that maps to mitigation strategies. (c) MCP × OTel × `gate-result/v1` convergence — single envelope for tool-call attestation. (d) Tool-use cost attribution — which tool calls drove which fraction of total cost? (e) Adversarial tool-use evaluation — how to surface emergent tool-injection or tool-confusion attacks beyond the prompt-injection cluster.

### Area 9 — Inference-Time Compute (thinking longer)

**1. Definition.** Trading wall-clock time and compute budget at inference time to improve output quality — via longer chains of thought, larger verification samples, deeper tree search, multi-pass refinement, etc. The "thinking model" paradigm popularized by OpenAI's o-series, Anthropic's extended thinking, and DeepSeek's R-series. Distinct from training-time compute (which is the model-developer's concern) by being a runtime-tunable knob.

**2. Why it matters technically.** Inference-time compute changes the operational economics of LLM systems — quality is no longer fixed at deployment; it's a sliding dial against cost and latency. For our platform: `gate-result/v1` should be able to capture how much inference-time compute was used per gate, because two runs of "the same eval" with different compute budgets are not the same run.

**3. Current state in our stack.** No formal `inference_compute_budget` or `inference_compute_used` fields on `EvalRun` or `gate-result/v1`. The `Provider` entity carries model identity but not compute-budget configuration. `iel-E16` is the proposed new epic "Inference-time compute attribution" per § 7.

**4. Where we fall short.** No compute-budget capture on `EvalRun`. No "thinking-mode" indicator distinguishing extended-thinking vs standard responses. No cost-quality tradeoff metrics. No integration tests against models that expose compute knobs (OpenAI o-series with `reasoning_effort`, Anthropic with extended thinking, DeepSeek-R1).

**5. Where we can build or contribute.** Build: (a) add `inference_compute` block to `EvalRun` capturing `budget_requested`, `budget_used`, `thinking_mode`, `tokens_consumed`, `wall_clock_ms`; (b) update `gate-result/v1` to optionally carry compute attribution; (c) `iel-E16` documents the attribution methodology in lab. Upstream contribution: the Cost of Dynamic Reasoning HPCA paper (`c1391af5…`, 26 cites, HPCA 2026) and Energy Cost of Reasoning (`65477686…`, 14 cites, 2025) are the operationalization papers — we can land reference instrumentation that consumes their methodologies.

**6. Field landscape — academic / labs.** Highly active and recent (most papers 2024-2025). Can 1B LLM Surpass 405B? Rethinking Compute-Optimal Test-Time Scaling (`eee9219d…`, 144 cites, 2025). Tree Search for Language Model Agents (`9345e553…`, 136 cites, TMLR 2024). Don't Overthink: Preferring Shorter Thinking Chains (`6ef76fb7…`, 56 cites, 2025). e3 Learning to Explore (`ff76e9e0…`, 50 cites, 2025). Elastic Reasoning (`e3e34549…`, 39 cites, 2025). Sample, Scrutinize and Scale (`b67c8d21…`, 37 cites, ICML 2025). Crosslingual Reasoning via Test-Time Scaling (`b187fa7d…`, 36 cites, 2025). JETTS (`5f2dbd43…`, 33 cites, ICML 2025). When To Solve, When To Verify (`d170e69d…`, 30 cites, 2025). Cost of Dynamic Reasoning HPCA (`c1391af5…`, 26 cites, HPCA 2026) — first paper to seriously treat this as an infrastructure cost concern. Sleep-time Compute (`a70f75cc…`, 23 cites, 2025). Survey on Adaptive and Controllable Test-Time Compute (`bc29e85f…`, 19 cites, 2025). Thinking Slow, Fast (`9ba7158d…`, 22 cites, 2025).

**7. Field landscape — OSS + open ecosystem.** Limited. The infrastructure surface (capture, attribute, bill) is mostly proprietary — OpenAI, Anthropic, Google expose compute knobs but the attribution work happens in their backends. OpenLLMetry can capture token usage but not "thinking-mode" indicators in any standard way. Phoenix and Langfuse can render the data but don't formally spec it. OTel GenAI semantic conventions cover `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens` but not thinking-tokens or compute-budget.

**8. Where this could go — open problems.** (a) Canonical OTel attribute for thinking-tokens / reasoning-tokens / compute-budget. (b) Cross-provider normalization — how to compare "Claude extended thinking" to "OpenAI o1 reasoning_effort=high" to "DeepSeek-R1 with chain length N"? (c) Attribution at gate level — when an eval used N test-time-compute, what fraction of the pass/fail signal is attributable to compute vs to model capability? (d) Cost-quality dynamic policy — should a gate spec declare "this gate is achieved at compute-budget X; halt scaling once X is reached"?

### Area 10 — Data Provenance (synthetic lineage chains)

**1. Definition.** End-to-end traceable lineage of data through the LLM pipeline — from prompt origin to model output to downstream training to evaluation to deployment decision. For synthetic data: which seed produced this case, which generator-model + version, which timestamp, what was filtered out, which evaluator scored it, who approved it for use. For human data: license, consent, provenance chain, transformation history.

**2. Why it matters technically.** Without provenance, every downstream attestation is hand-wavy. "This model passed our eval suite" is meaningless without provenance for the eval suite itself. "This model was trained on safe data" is meaningless without lineage. The supply-chain attacks documented in adjacent ML areas (model backdoors, dataset poisoning, evaluator poisoning) demand provenance discipline.

**3. Current state in our stack.** Strong on the gate-result side, partial on the test-suite side. `gate-result/v1` already carries sigstore attestation via Blueprint B § 7 + the audit-harness `harness-hash` script. The kernel emits results signed against a hash-pinned policy. What's missing: provenance for the test cases themselves, the evaluator weights, the synthetic data generators. SLSA-aligned posture is partial — our gate-result is SLSA-compliant on the consumer side; the producer side (where test cases come from) is not yet specced. `iec-E10` (Data provenance / synthetic lineage in Evidence Bundle) is the proposed new epic per § 7.

**4. Where we fall short.** `EvalCase` does not carry `provenance` block. `EvalSuite` does not carry `derivation_chain` block. No formal attestation type for "this synthetic case was generated by model X with seed Y on date Z." No integration with sigstore for test-suite signing (vs result signing, which is in place).

**5. Where we can build or contribute.** Build: (a) `iec-E10` extends Evidence Bundle to carry `provenance` element on `EvalCase` and `derivation_chain` on `EvalSuite`; (b) adapt SLSA-style attestation pattern for test artifacts; (c) add `provenance-attest.sh` to audit-harness; (d) document the full provenance model in `intent-eval-lab/specs/provenance-v1.md`. Upstream contribution: SLSA framework + sigstore are the natural standards-track homes; extending SLSA attestation types to cover synthetic-data lineage is a defensible upstream contribution.

**6. Field landscape — academic / labs.** Sparse on the specific synthetic-data-provenance question. Bibliography query "software supply chain provenance SLSA attestation" returned 0 hits at our citation threshold — the work is happening in industry (Sigstore, in-toto, SLSA framework, OpenSSF) and not in academic publishing. ML data-provenance work exists but is concentrated on training-data licensing and human-annotated datasets, not synthetic-data lineage. The Prismatic Synthesis paper (`b71a9a4…`, 34 cites, 2025) implicitly carries provenance in its diversity-driven generator but doesn't formalize it.

**7. Field landscape — OSS + open ecosystem.** Sigstore + in-toto + SLSA framework are the standards-track surface, all OSS, all permissively licensed. Sigstore's `cosign` already handles attestation of artifacts; the type system covers a few SLSA predicates but not eval-specific ones. In-toto provides the composability framework. HuggingFace's `datasets` library carries minimal provenance metadata. No OSS project formally addresses synthetic-data-lineage as a first-class concern.

**8. Where this could go — open problems.** (a) Canonical SLSA predicate type for synthetic data — analogous to `provenance/v1` for binaries, an `eval-suite-provenance/v1` for test data. (b) Cross-organization provenance — how does provenance survive when a synthetic suite generated at org A is consumed by org B? (c) Provenance under unlearning — if a training-data item is unlearned, what happens to derived attestations? (d) Performance — full provenance chains for million-case suites must remain fast to verify.

### Area 11 — Reasoning Authenticity (fake vs genuine CoT)

**1. Definition.** Distinguishing chain-of-thought (CoT) output that **causally influenced** the model's final answer from CoT output that is **post-hoc rationalization** (the answer was already chosen; the reasoning is decoration). Closely linked: detecting unfaithful CoT, detecting deceptive CoT (where the visible reasoning differs from the actual reasoning used), and detecting evasion of CoT-based monitoring.

**2. Why it matters technically.** If we cannot distinguish faithful from unfaithful CoT, every safety/reliability argument that "we monitor reasoning steps to catch X" is defeasible. CoT monitoring is a core safety strategy at Anthropic and elsewhere; reasoning-authenticity is the technical question on which that strategy stands or falls. For our platform: `gate-result/v1` carrying "CoT-monitored decision" is only as defensible as the CoT being authentic.

**3. Current state in our stack.** Nothing direct. CoT material lives inside `SessionTrace.reasoning_steps` (per Blueprint B § 7) but no faithfulness scoring is currently attached. `iaj-E12` is the proposed new epic "Reasoning authenticity (CoT verification)" in j-rig per § 7.

**4. Where we fall short.** No faithfulness scoring at all. No integration with the established faithfulness metrics from the academic literature (Turpin's intervention-based tests, biased-context tests, paraphrase tests, unlearning tests). No "CoT-monitored gate" pattern in `gate-result/v1`. No worked examples.

**5. Where we can build or contribute.** Build: (a) `iaj-E12` ships at least three faithfulness judges in j-rig drawing on Turpin et al., Lanham et al., the "unlearning reasoning steps" methodology (`aaaa0435…`, 37 cites, 2025); (b) extend `gate-result/v1` to optionally carry `cot_faithfulness_score`; (c) document the CoT-monitoring gate pattern in `intent-eval-lab`. Upstream contribution: FaithCoT-Bench (`6968f45a…`, 13 cites, 2025) is a recent academic benchmark — implementation of our faithfulness judges against FaithCoT-Bench is a defensible upstream cross-reference. Anthropic's published CoT-monitoring work is the closest paradigm but proprietary; OSS reproductions are needed.

**6. Field landscape — academic / labs.** Robust and well-cited. Turpin et al. "Models Don't Always Say What They Think" (`7dc928f4…`, **1097 cites**, NeurIPS 2023) — the foundational unfaithfulness paper. Anthropic Measuring Faithfulness in Chain-of-Thought Reasoning (`827afa7d…`, 422 cites, 2023). Lyu et al. Faithful Chain-of-Thought Reasoning (`b115c1e1…`, 383 cites, 2023). Reasoning Models Don't Always Say What They Think (`b9ca6db2…`, 297 cites, 2025) — extending Turpin to o-series-style models. CoT In The Wild Is Not Always Faithful (`e71ff518…`, 128 cites, 2025). When CoT is Necessary, LMs Struggle to Evade Monitors (`ab757156…`, 50 cites, 2025) — closely related to deception detection. Are DeepSeek R1 More Faithful (`3f0455e9…`, 52 cites, 2025). Question Decomposition Improves Faithfulness (`8154fb1d…`, 122 cites, 2023). Measuring CoT Faithfulness by Unlearning Reasoning Steps (`aaaa0435…`, 37 cites, 2025). A Causal Lens for Evaluating Faithfulness Metrics (`fb04470a…`, 10 cites, 2025). FaithCoT-Bench (`6968f45a…`, 13 cites, 2025). Anthropic and Apollo Research are the labs most active here.

**7. Field landscape — OSS + open ecosystem.** Very sparse. The faithfulness measurement methodologies are documented in papers but not packaged as OSS tools. No equivalent of "Inspect AI for CoT faithfulness" exists. This is one of the cleanest "build-in-our-repos because nobody's done it in OSS" calls in the audit.

**8. Where this could go — open problems.** (a) Operational definition that survives prompt-engineering pressure (paraphrase invariance). (b) Cross-model faithfulness measurement — same prompts on different models reveal different faithfulness profiles. (c) Adversarial faithfulness — agents that learn to game faithfulness probes. (d) Standardization of faithfulness scoring such that two organizations can compare. (e) Connection between faithfulness and deception evaluation — overlapping but distinct phenomena.

### Area 12 — Agent Guardrails (loop budgets / rollback / permission)

**1. Definition.** Runtime safety controls applied to agent execution: maximum iteration budgets, automatic rollback on detected anomaly, permission-graph enforcement on tool calls, halt conditions, intervention triggers. Distinct from prompt-engineered constraints (which the model may ignore) by being enforced **outside** the model — in the orchestrator, gate, or runtime sandbox.

**2. Why it matters technically.** Agents in production fail with unbounded resource consumption (infinite loops, retry storms, runaway tool calls) more often than they fail with catastrophic semantic errors. Without runtime guardrails, a single bad decision can cascade into thousands of bad decisions. Permission-graph enforcement is also the strongest defense against prompt-injection-driven tool abuse. Guardrails turn defense-in-depth from a slogan into a verified property.

**3. Current state in our stack.** Partial. `iel-E14c` (operational doctrine bundle, P2) carries some material. `gate-result/v1` can express PASS/FAIL/WAIVE but does not formally encode "this run was halted by guardrail X at iteration N." `iar-E04` is the proposed new epic "Agent guardrails (loop budgets / rollback / permission)" per § 7.

**4. Where we fall short.** No formal `Guardrail`, `GuardrailTrigger`, `GuardrailDecision` entities. No taxonomy of guardrail-trigger reasons. No connection between guardrail-triggered halts and the `gate-result/v1` outcome — currently they look like "no result" rather than "halted by guardrail." No integration with the runtime sandbox literature (ShieldAgent, etc.).

**5. Where we can build or contribute.** Build: (a) `iar-E04` adds guardrail entities + decision codes to the rollout-gate; (b) extend `gate-result/v1` to formally encode "halted by guardrail" with structured reason; (c) document a guardrail taxonomy in `intent-eval-lab/specs/guardrails-v1.md`; (d) integration test fixtures using the academic guardrail-defense literature. Upstream contribution: ShieldAgent (`1b330d0b…`, 77 cites, ICML 2025) — verifiable safety policy reasoning — is an obvious integration target; "Foundational Guardrail via Synthetic Data" (`0f1951b7…`, 11 cites, 2025) provides synthesis methodology for guardrail training data.

**6. Field landscape — academic / labs.** Robust. ShieldAgent (`1b330d0b…`, 77 cites, ICML 2025) — verifiable safety policy reasoning. Foundational Guardrail via Synthetic Data (`0f1951b7…`, 11 cites, 2025). Think Twice Before You Act (`bbac4cef…`, 10 cites, 2025) — thought correction for safety. LLM Agents Should Employ Security Principles (`089938fe…`, 22 cites, 2025). Monitoring Monitorability (`26220318…`, 14 cites, 2025) — meta-monitoring. DRIFT defense (`ec906205…`, 27 cites, 2025) — dynamic rule-based defense with injection isolation. Task Shield (`8af6009a…`, 49 cites, ACL 2024). MELON provable defense (`830cb224…`, 35 cites, ICML 2025). IPIGuard (`9ddcbbff…`, 30 cites, EMNLP 2025) — tool dependency graph-based defense. AgentAuditor (`03a93e2e…`, 35 cites, 2025) — human-level safety eval.

**7. Field landscape — OSS + open ecosystem.** Less mature than the academic surface. LangChain + LangGraph carry execution-loop controls but framework-specific. CrewAI has task-budget mechanisms. NeMo Guardrails (NVIDIA, Apache 2.0) is the closest dedicated guardrail framework but model-side rather than runtime-side. Inspect AI can declare loop budgets but no formal canonicalization.

**8. Where this could go — open problems.** (a) Canonical guardrail-trigger taxonomy that survives multi-vendor toolchains. (b) Composability — agent A's guardrails interacting with downstream agent B's guardrails in a multi-agent system. (c) Permission graphs as first-class artifacts — `gate-result/v1` declaring "this run respected permission graph P". (d) Performance — guardrail enforcement that doesn't dominate the latency budget. (e) Verification — proving a guardrail correctly enforces a policy is a meta-eval problem.

### Area 13 — Curriculum Learning (PARKED, foundation-model layer)

**1. Definition.** Ordering training data or task exposure for an ML model so that easier examples come first, progressing to harder ones, mirroring pedagogy. Modern variants include automatic curriculum generation, reward-driven curriculum, and synthetic-data curriculum.

**2. Why it matters technically.** Foundation-model layer concern. Affects training efficiency, sample efficiency, and capability scaling. Not directly an infrastructure concern.

**3. Current state in our stack.** Not applicable. IEP is not a training-data pipeline or a model-training framework.

**4. Where we fall short.** N/A — out of scope.

**5. Where we can build or contribute.** **Park for personal-skill pillar** (Appendix F). Operator-development thread, quarterly re-evaluation. Not an IEP epic.

**6. Field landscape — academic / labs.** Active foundation-model research at Anthropic, OpenAI, Google DeepMind, Meta. Not surveyed in depth in this audit because it's parked.

**7. Field landscape — OSS + open ecosystem.** Hugging Face transformers + accelerate carry curriculum hooks; PyTorch Lightning, JAX-based training stacks. Not surveyed in depth.

**8. Where this could go — open problems.** Foundation-model team concerns. IEP touches this only by **measuring** the resulting model's behavior — not by participating in the curriculum design.

### Area 14 — Compression / Representation Learning (PARKED, foundation-model layer)

**1. Definition.** Techniques for reducing model size while preserving capability: quantization, pruning, distillation, low-rank approximations, learned compression. Representation learning more broadly covers what the model encodes in its hidden states.

**2. Why it matters technically.** Inference cost dominates production economics; compression is a major lever. Foundation-model layer concern.

**3. Current state in our stack.** Not applicable.

**4. Where we fall short.** N/A — out of scope.

**5. Where we can build or contribute.** **Park for personal-skill pillar** (Appendix F).

**6. Field landscape — academic / labs.** Highly active; foundation-model concern. Not surveyed.

**7. Field landscape — OSS + open ecosystem.** llama.cpp, vLLM, TensorRT-LLM, Hugging Face quantization libs. Not surveyed.

**8. Where this could go — open problems.** Foundation-model team concerns. IEP intersects only via inference-cost attribution (Area #9).

### Area 15 — Small Model Research (PARKED, foundation-model layer)

**1. Definition.** Training and characterizing models in the 0.5B-10B parameter range — for edge deployment, latency-critical paths, or as understanding-aids for mechanistic interpretability. The Karpathy "train tiny transformers yourself to learn mechanics" pillar.

**2. Why it matters technically.** Pedagogically valuable for operators who want to understand foundation-model dynamics from first principles. Production-relevant for edge / on-device. Foundation-model layer.

**3. Current state in our stack.** Not applicable. IEP does not train models.

**4. Where we fall short.** N/A — out of scope.

**5. Where we can build or contribute.** **Park for personal-skill pillar** (Appendix F). This is the Karpathy-pedagogy thread — high learning value, low platform leverage.

**6. Field landscape — academic / labs.** Active, especially for distillation and edge-model research. Not surveyed in this audit.

**7. Field landscape — OSS + open ecosystem.** Hugging Face SmolLM, Microsoft Phi family, Mistral small models. nanoGPT and minGPT for pedagogy. Not surveyed.

**8. Where this could go — open problems.** Operator-development. Not IEP.

### Area 16 — Mechanistic Interpretability (PARKED, foundation-model layer)

**1. Definition.** Reverse-engineering the internal mechanisms by which a trained neural network produces its outputs — circuits, features, attention patterns. Anthropic's interpretability team is the most-visible practitioner.

**2. Why it matters technically.** Foundational for alignment and safety arguments at the model level. Pedagogically valuable. Foundation-model layer.

**3. Current state in our stack.** Not applicable.

**4. Where we fall short.** N/A — out of scope.

**5. Where we can build or contribute.** **Park for personal-skill pillar** (Appendix F).

**6. Field landscape — academic / labs.** Active at Anthropic interpretability team, Google DeepMind interpretability, academic groups at Harvard / MIT / NYU. Not surveyed in depth.

**7. Field landscape — OSS + open ecosystem.** Transformer Lens (Neel Nanda), Anthropic's sparse-autoencoder releases, EleutherAI interp tooling. Not surveyed.

**8. Where this could go — open problems.** Foundation-model team and interpretability research-group concerns. IEP only intersects if/when interpretability-derived signals become gate-result inputs (speculative, not roadmapped).

### Area 17 — Distributed State Systems (multi-agent coordination)

**1. Definition.** Coordination, communication, shared-state management, and consensus among multiple LLM agents working on a joint task. Includes role assignment, message routing, conflict resolution, shared memory access, and observable run-state across agent boundaries.

**2. Why it matters technically.** Production multi-agent systems are increasingly common (planner + executor patterns, expert ensembles, debate-based reasoning). The failure modes — message-routing errors, role drift, shared-state corruption, prompt-injection-via-agent-to-agent communication — are categorically distinct from single-agent failures. Without a canonical multi-agent state model, every system reinvents the substrate and the failure modes propagate.

**3. Current state in our stack.** Blueprint B carries `CompositionDag` as one of the 13 canonical entities, addressing the multi-agent composition structure. `iec-deferral-F` (CompositionDag wire format normative spec) is the relevant deferred decision. `iel-E17` is the proposed new epic "Multi-agent state coordination" per § 7.

**4. Where we fall short.** `CompositionDag` exists as entity but wire-format spec is deferred (`iec-deferral-F`). No formal `AgentRole`, `AgentMessage`, `AgentState` entities. No multi-agent guardrail propagation. No worked examples integrating with the academic multi-agent literature (RoCo, MegaAgent, AutoHMA-LLM).

**5. Where we can build or contribute.** Build: (a) close `iec-deferral-F` with CompositionDag wire-format spec; (b) add `AgentRole`, `AgentMessage`, `AgentInteraction` entities to Blueprint B § 4 + kernel; (c) `iel-E17` documents the multi-agent state model; (d) integration tests against MegaAgent and AgentOrchestra patterns. Upstream contribution: SagaLLM (`356b85ae…`, 34 cites, VLDB 2025) provides context management + validation + transaction guarantees for multi-agent planning — direct alignment opportunity. Agentic AI Frameworks Architectures Protocols (`4740a540…`, 22 cites, 2025) is the relevant survey.

**6. Field landscape — academic / labs.** Highly active. RoCo (`c5d18dbb…`, 252 cites, ICRA 2023) — dialectic multi-robot collaboration with LLMs. Scalable Multi-Robot Centralized vs Decentralized (`1ad73571…`, 161 cites, ICRA 2023). LLM-based Multi-Agent RL (`dd387552…`, 80 cites, 2024). Red-Teaming Multi-Agent Communication (`4669474d…`, 94 cites, ACL 2025). MegaAgent (`d5b84741…`, 43 cites, ACL 2025). Embodied Multi-Agent Collaboration (`e1b62c7e…`, 56 cites, ACL 2024). AgentOrchestra (`7e8b6a8a…`, 64 cites, 2025) — hierarchical multi-agent framework. SagaLLM (`356b85ae…`, 34 cites, VLDB 2025). "Large Language Models Miss the Multi-Agent Mark" (`d70edc12…`, 21 cites, 2025) — important critical voice. AgentsNet (`e2fd1d0a…`, 20 cites, 2025). Multi-Agent Credit Assignment (`198b1247…`, 12 cites, AAMAS 2025).

**7. Field landscape — OSS + open ecosystem.** Active framework layer. AutoGen (Microsoft, MIT), CrewAI (MIT), LangGraph (LangChain), MetaGPT (MIT), AgentVerse (MIT). All ship multi-agent abstractions in framework-specific shapes; none formally specs the cross-framework state model. MCP can carry agent-to-agent messages but does not specify multi-agent state semantics.

**8. Where this could go — open problems.** (a) Canonical multi-agent state model that survives framework boundaries — converting an AutoGen run to a CrewAI run should be possible. (b) Multi-agent guardrail composition. (c) Prompt-injection propagation in multi-agent systems (well-studied attack surface per `165921d2…` Prompt Infection paper). (d) Cost attribution across agent boundaries. (e) Observability for multi-agent — span hierarchy + cross-agent correlation.

### Area 18 — Model Routing (dynamic selection, fallback, cost)

**1. Definition.** Runtime selection of which model (and which compute budget) to use for a given request, based on cost, capability, latency, or reliability. Includes cascading (cheap-first with fallback), routing-by-classifier, ensemble approaches, and dynamic model swapping mid-conversation.

**2. Why it matters technically.** Cost optimization is the most-cited driver, but reliability is the deeper concern — different models fail in different ways; routing diversifies failure modes. Routing also affects evaluation: an `EvalRun` against a "routed system" is a different thing than an `EvalRun` against a fixed model.

**3. Current state in our stack.** The kernel has `Provider` and `JudgeAdapter` entities; routing happens at the consumer's runtime layer (we don't host runtime). No formal `Router`, `RoutingDecision`, `RoutingPolicy` entities. `iar-E05` is the proposed new epic "Model routing" per § 7.

**4. Where we fall short.** No formal routing entities. No routing-decision metadata in `gate-result/v1`. No worked examples of "this gate result was achieved via routing policy X." No integration with the academic routing literature.

**5. Where we can build or contribute.** Build: (a) add `RoutingDecision` to `SessionTrace` events; (b) extend `gate-result/v1` to optionally carry routing-policy provenance; (c) `iar-E05` documents routing-aware gate evaluation. Upstream contribution: MasRouter (`086830da…`, 52 cites, ACL 2025) and the Unified Routing & Cascading paper (`05e38538…`, 43 cites, ICML 2024) are the most-cited recent works — reference implementations would be welcome.

**6. Field landscape — academic / labs.** Less active than other clusters but accelerating. MasRouter (`086830da…`, 52 cites, ACL 2025) — routing LLMs for multi-agent systems. Unified Routing & Cascading (`05e38538…`, 43 cites, ICML 2024). Uncertainty-Based Two-Tier Selection (`8d59f23d…`, 26 cites, 2024). Agreement-Based Cascading (`3e75ac5f…`, 14 cites, TMLR 2024). Cortex AISQL — Production SQL Engine for Unstructured Data (`5af12150…`, 11 cites, 2025) — interesting industrial example. Symbiotic Cooperation for Web Agents (`8239ae2f…`, 18 cites, 2025) — small/large LLM cooperation.

**7. Field landscape — OSS + open ecosystem.** Active. LiteLLM (BerriAI, MIT) is the de-facto router/proxy. RouteLLM (Anyscale-affiliated) is an open routing framework. LangChain's `RunnableBranch` carries routing primitives. None formally specs routing decisions as Evidence Bundle metadata.

**8. Where this could go — open problems.** (a) Routing-decision attestation — the gate result carries provenance of which models were selected and why. (b) Routing under reliability constraints — "always use the cheaper model unless reliability drops below R." (c) Cost-quality Pareto characterization for routing policies. (d) Evaluation of routed systems — defining a fair `EvalRun` that doesn't reduce to "test the fallback model alone."

### Area 19 — Operational Reliability (regression / drift / failure-class / recovery)

**1. Definition.** Maintaining and improving an agent system's reliability in production: regression detection (something that worked yesterday breaks today), drift detection (gradual capability erosion), failure-class identification (recognizing which class of failure this is and routing to the right recovery), and recovery (re-trying, rolling back, escalating to human). Distinct from launch-time evaluation by being **continuous + adaptive + diagnostic**.

**2. Why it matters technically.** Launch-time gates pass; production rarely matches launch. Without continuous reliability infrastructure, every deployed agent decays silently. Operational reliability is the connection layer between offline evaluation (which we ship) and runtime production (which we do not host but must serve).

**3. Current state in our stack.** Partial. `gate-result/v1` is the static-evaluation surface; runtime drift / regression is not yet specced. `iar-E03` is the proposed new epic "Production drift" per § 7. Earlier discussion of evaluator gaming overlaps with this area.

**4. Where we fall short.** No drift-detection schema. No regression-detection methodology canonicalized. No failure-class taxonomy. No connection from `gate-result/v1` history to drift signals (i.e., we don't say "this gate's results are drifting over time"). No worked examples.

**5. Where we can build or contribute.** Build: (a) `iar-E03` adds drift-detection schema + failure-class taxonomy; (b) extend the rollout-gate to carry historical-context-aware decisions (compare current gate-result to N-day window); (c) document in `intent-eval-lab/specs/reliability-v1.md`. Upstream contribution: the ML drift-detection literature is dominated by classical ML (Evidently AI, Arize Phoenix monitoring, NannyML); LLM-specific drift work is sparse — open contribution surface.

**6. Field landscape — academic / labs.** Sparse on the LLM-specific framing. Bibliography query "data distribution shift production drift" returned 0 hits at our threshold. ML drift work pre-dates LLMs (Quinonero-Candela et al., 2009, "Dataset Shift in Machine Learning"). LLM-specific operational-reliability papers are rare; closest analogs are the eval-systems surveys and the test-time-scaling work (which addresses launch-time, not in-production decay).

**7. Field landscape — OSS + open ecosystem.** Evidently AI (Apache 2.0) and NannyML (Apache 2.0) are the dominant ML-drift OSS projects but LLM coverage is recent and partial. Arize Phoenix (ELv2) handles eval and observability but not formal drift detection. Langfuse can store traces but not detect drift.

**8. Where this could go — open problems.** This is one of the cleanest "build-in-our-repos" candidates — the field is open, the academic surface is sparse, and the platform's gate-result/v1 history is the natural substrate. (a) Drift detection in production agent behavior — defined how? (b) Failure-class taxonomy that survives multi-vendor and multi-version transitions. (c) Recovery-action attestation — the gate result of a recovery step.

### Area 20 — Open Standards (shared schemas)

**1. Definition.** Cross-vendor, cross-organization shared schemas, semantic conventions, and interchange formats for AI evaluation, observability, telemetry, agent traces, and decision records. Includes spec governance, ratification, versioning, and adoption.

**2. Why it matters technically.** Without open standards, every organization re-invents the substrate and the field fragments. Standards work is high-leverage but slow: a single ratified attribute in OTel reaches more consumers than ten implementations. Our entire `gate-result/v1` posture is bet on this principle.

**3. Current state in our stack.** Blueprint A § 3 declares the platform's standards-track posture; Blueprint B § 7 normatively specs `gate-result/v1`. The Canonical Glossary defines terminology used in the standards. `iel-E13` (Architecture boundary standards, 3-doc cluster) is in-flight. `iec-deferral-D` (gate-result/v1 coverage element shape) is gating on standards-clarity.

**4. Where we fall short.** `gate-result/v1` is not yet published to any external standards body. No formal proposal submitted to OpenTelemetry GenAI SIG. No engagement with W3C / OASIS / IETF on AI-eval standards. No external schema review from non-IS stakeholders. No standards-track adopters beyond ourselves.

**5. Where we can build or contribute.** Build: complete `iel-E13`; submit `gate-result/v1` as a standards-track proposal to OTel SIG; engage OpenInference as an interop partner; produce reference adapters to/from Inspect AI's eval results and to/from `gate-result/v1`. Upstream contribution: OpenTelemetry GenAI SIG is the **most-leverage** target — semantic conventions for agent trajectories, eval results, and reasoning steps are open contribution surfaces. MCP is a parallel surface for tool-call attestation. SLSA is a parallel surface for synthetic-data provenance.

**6. Field landscape — academic / labs.** Standards work is not paper-publishable in the usual sense. Some methodology papers — Inspect AI's white paper, OpenTelemetry's design docs, SLSA's framework definitions — are quasi-publication. UK AISI's Inspect AI is the strongest standards-track precedent we identified.

**7. Field landscape — OSS + open ecosystem.** OpenTelemetry SIG GenAI (active, in Development status, Apache 2.0, governance via CNCF). OpenInference (Apache 2.0, complementary to OTel). MCP (Model Context Protocol, Anthropic-led, multi-vendor adoption). SLSA (OpenSSF-hosted, vendor-neutral). Sigstore (CNCF, vendor-neutral). Inspect AI (UK AISI, MIT). All are Apache/MIT-compatible with our platform posture.

**8. Where this could go — open problems.** (a) Multi-SIG coordination — OTel + MCP + SLSA convergence on a single envelope. (b) Versioning discipline — how do `gate-result/v1` consumers upgrade to v2 without breaking? (c) Conformance testing — third parties verify their implementation matches the spec. (d) Cross-language schema generation — TypeScript-native kernel generating Python + Go + Rust + Java bindings.

### Area 21 — Evaluator Disagreement Dataset (uniquely ours)

**1. Definition.** A publicly-released, longitudinally-updated dataset capturing per-model judge disagreement on a curated set of evaluations — same case, multiple judges, recorded outcomes, recorded reasoning. The goal: create the field's empirical baseline for "when do judges disagree, why, and how does that disagreement evolve as models improve."

**2. Why it matters technically.** Every LLM-as-judge paper would benefit from a shared reference dataset for measuring judge alignment. No such dataset is currently shipped openly. Our platform produces this data as a natural side-effect of running gates with multiple judges — we can be the open-data host. Beyond methodology value, the dataset surfaces empirical questions about model-family bias, judge calibration, and evaluator-gaming dynamics.

**3. Current state in our stack.** Nothing direct. `iel-E15` is the proposed new epic "Disagreement dataset" in `intent-eval-lab` per § 7.

**4. Where we fall short.** Not started. No publishable dataset surface, no licensing decision, no governance model, no curation process.

**5. Where we can build or contribute.** Build entirely-in-our-repos: (a) `iel-E15` defines the dataset schema (per-case multi-judge results with provenance); (b) curation policy (synthetic + human-curated cases, balanced across domains); (c) hosting decision — HuggingFace Datasets is the natural home, Apache or CC-BY-SA license; (d) update cadence — quarterly. Upstream contribution: this *is* the contribution — there is no existing open dataset of this kind at the depth we can provide.

**6. Field landscape — academic / labs.** Many papers reference judge-disagreement empirically but no shared dataset exists. Replacing Judges with Juries (`1a9d2a80…`, 225 cites, 2024), Limits to Scalable Eval (`aa6f16e9…`, 33 cites, ICLR 2025), JuStRank (`c85e7a71…`, 21 cites, 2024), Aligning with Human Judgement (`aae01e93…`, 153 cites, 2024) — all would benefit from a reference dataset.

**7. Field landscape — OSS + open ecosystem.** No equivalent dataset exists. ChatbotArena's human preference data is the closest analog but it's human preferences, not judge disagreement. LiveBench releases benchmark scores but not per-judge disagreement. Open contribution opportunity is unambiguous.

**8. Where this could go — open problems.** (a) Curation methodology that resists gaming. (b) Privacy / data-protection of any source material. (c) Versioning — judges evolve, dataset must reflect snapshot semantics. (d) Connection to the kernel — same `gate-result/v1` shape used in production gates should be the shape of dataset records. (e) Governance — community-driven curation vs Intent Solutions-curated. The first is more durable but slower to bootstrap.

---

## § 4.5 — Cross-cutting findings and tensions

The 21 per-area treatments above expose recurring themes that span multiple areas. This section names six cross-cutting findings and three structural tensions that the operator (and ISEDC Session 5) should reason about explicitly, rather than discovering implicitly when ranking P0 epics.

### 4.5.1 Finding: every claim ultimately routes through `gate-result/v1`

Trace this across the 21 areas: trajectory replay declares replay-fidelity in the gate result (Area #5); verifier systems declare independence-class in the gate result (Area #6); inference-time compute declares budget attribution in the gate result (Area #9); guardrails declare halt reason in the gate result (Area #12); routing declares routing-policy provenance in the gate result (Area #18). The single most cross-cutting kernel artifact is the `gate-result/v1` schema. Decisions about its shape — what extension points it admits, what optional blocks vs required blocks, how it carries multiple verifier results — affect almost every Phase B epic. This argues for **closing the open `iec-deferral-*` Class-2 specs early in Phase B**, before the downstream consumer epics commit to particular `gate-result/v1` extensions.

### 4.5.2 Finding: OpenTelemetry GenAI SIG is the single highest-leverage upstream surface

Six of the 21 areas have an active OTel SIG contribution path: trajectories (#1), agent observability (#3), tool-use (#8), inference-time compute (#9), multi-agent state (#17), open standards (#20). Submitting one well-designed semantic-conventions proposal to the SIG reaches more downstream consumers than ten in-repo implementations. The leverage gradient is steep — most other upstream surfaces (OpenInference, MCP, SLSA) have smaller ratification effects than OTel. This argues for **dedicating one work-block to OTel SIG engagement** in early Phase B even though it doesn't map to a single bead — the engagement is cross-cutting and pays back across epics.

### 4.5.3 Finding: four areas have no OSS equivalents at all

Reasoning authenticity (Area #11), evaluator-disagreement dataset (Area #21), synthetic-data quality scoring (Area #4), and operational reliability for LLM systems (Area #19). For these, "build vs contribute upstream" reduces to "build, because there is no upstream." This is where IEP can be **technically first** without competing — the field hasn't gotten there yet. The combination of (a) dense academic literature already published, (b) zero open-source implementation, and (c) clean fit to our existing entities (gate-result/v1 + EvalCase + SessionTrace) makes these the strongest "build now" candidates in the audit.

### 4.5.4 Finding: the audit ratifies the kernel's anti-goal stance

Several areas tempt construction work that would violate Blueprint A's anti-goals: managed observability product (Area #3 — Phoenix/Langfuse posture), benchmark hosting (Areas #1, #21 — METR/HuggingFace posture), runtime execution infrastructure (Areas #12, #17 — sandbox-as-a-service posture). The audit reaffirms the existing posture: we **define schemas**, we **emit attestations**, we **ship validators**. We do not host runtime or operate managed services. Every Phase B epic that could be confused for runtime-operation work needs explicit anti-goal framing in its kickoff bead.

### 4.5.5 Finding: memory + security + drift are converging into a "trust posture" cluster

Areas #7 (memory), #12 (guardrails), #19 (drift) and the prompt-injection literature each address subsets of the same engineering concern: maintaining trust in agent outputs across run boundaries, across attack surfaces, and across time. The platform currently treats these as separate concerns; the literature increasingly treats them as one. The Class-2 ISEDC discussion at Session 5 should consider whether a single `TrustPosture` first-class entity rolls these up — or whether each area's separate entities (`Memory`, `Guardrail`, `DriftSignal`) are the right granularity. This is a tractable design decision; the literature doesn't force the answer.

### 4.5.6 Finding: provenance is the strongest external defensibility lever

Of the 21 areas, **data provenance (Area #10)** is the one that most directly answers "how would I prove this to a third party who doesn't trust me?" The existing sigstore + harness-hash posture is already strong; extending Evidence Bundle to carry synthetic-data lineage and test-suite provenance turns "our gate said pass" into "here is a chain that lets you reconstruct exactly why our gate said pass, and verify it independently." This is high external-leverage work that compounds across every other epic — every other epic's outputs become more defensible if provenance is complete.

### 4.5.7 Tension: kernel minimalism vs growing entity demand

The kernel currently exposes 13 first-class entities (Blueprint B § 4). The audit identifies at least eight additional candidate entities — `Tool`, `ToolInvocation`, `Verifier`, `Memory`, `MemoryStore`, `Guardrail`, `Router`, `RoutingDecision` — across the Phase B work. Adding all eight doubles the kernel surface and complicates the type surface for downstream consumers. The opposing pull: leaving these out of the kernel means each consumer reinvents them and the cross-tool interoperability story collapses. The Class-2 ISEDC decision rule should be: **an entity earns kernel-status if (a) two or more downstream repos need it AND (b) at least one external standard would adopt it.** Tool + ToolInvocation likely qualify (MCP); Verifier likely qualifies (PRM literature); Memory likely qualifies (Mem0/Zep); others might not.

### 4.5.8 Tension: speed of OSS contribution vs caution under DR-010 § 13.6

DR-010 § 13.6 (external-pattern non-borrow) removes the prior constraint forcing IEP to design from first principles independent of external patterns. The audit reaffirms several upstream contribution paths (OTel SIG, Inspect AI, Mem0, SLSA, MCP). The opposing pull is timing: external upstream cycles are slow (weeks to months for OTel SIG ratification); in-repo construction is fast (days). The strategic answer is **dual-tracking** — build the in-repo capability immediately AND open the upstream conversation in parallel, with explicit doc commitments to retire the in-repo version once upstream lands. § 7's epic ranking accommodates this.

### 4.5.9 Tension: research depth vs operator bandwidth

The plan correctly notes "bandwidth-gated, not customer-signal-gated." That means depth-per-area is constrained by total operator capacity, not by external demand. The 14 new epics in § 7 will not all execute simultaneously; even if all P0-ranked epics get worked, the realistic Phase B output is 4-6 epics fully shipped + the others in spec-draft state. The Framing Memo for ISEDC Session 5 should declare this tradeoff explicitly: "we are ranking these in priority order; we are committing to ship the top N where N is operator-determined." Anything past N becomes Phase C visibility.

### 4.5.10 Implication for Phase B P0 sequencing

Taking the findings + tensions together, the recommended Phase B kickoff sequence is:

1. Close the open `iec-deferral-*` Class-2 specs (1-2 work-blocks) — unblocks downstream `gate-result/v1` extensions
2. Submit one OTel GenAI SIG semantic-conventions proposal (1 work-block) — kicks off the upstream cycle
3. Ship `iel-E15` evaluator-disagreement dataset surface (3-4 work-blocks) — high uniqueness, no upstream alternative
4. Ship `iaj-E12` reasoning authenticity (3-4 work-blocks) — high uniqueness, dense literature support
5. Ship `iaj-E11` verifier systems (3-4 work-blocks) — unlocks downstream reliability claims
6. Ship `iar-E03` operational reliability (3-4 work-blocks) — connects offline to production

This sequence threads the cross-cutting findings: opens upstream early, hits the four no-OSS-equivalent areas first, closes the kernel-deferral surface before downstream consumers extend it. ISEDC Session 5 can ratify or revise; the sequence is a starting position, not a final ranking.

---

## § 5 — Existing in-flight work mapped against the audit

Three IEP areas are already in-flight as epics; one is mature. Recapping their current state and what this audit changes:

| Area | Epic / status | What this audit changes |
|---|---|---|
| #1 Operational Trajectories | `iel-E12` (P0, in-flight) | No scope change. The audit reinforces this is core. Adds new explicit recommendation: propose `gen_ai.agent.trajectory.*` to OTel SIG once the event taxonomy stabilizes. |
| #5 Trajectory Replay | `iel-E11` (P0, in-flight) | No scope change. Adds new explicit recommendation: classify SWE-bench, OSWorld, tau-bench replay capability against RF-0..RF-4 as a normative test set. |
| #3 Agent Observability | overlaps `iel-E12` + `iel-E02d` + `iah-E07` + `iaj-E08` + `iar-E02` (P0/P1 mix) | The audit consolidates: this surface is dominated by upstream contribution to OTel GenAI SIG, not local construction. A `@intentsolutions/otel-shim` reference instrumentation lib is recommended new work. |
| #2 Eval Systems (binary) | mature — kernel + j-rig + audit-harness | No scope change. Citation grounding becomes a one-time documentation pass; no new construction needed beyond closing 5 `iec-deferral-*` Class-2 specs. |

The 13 new areas + 1 uniquely-ours area become the new Phase B epic-level investment. The 4 parked areas become the personal-skill pillar (Appendix F).

---

## § 6 — Research framework: 5 teams + parked pillar

This section consolidates the 5-team carving from the program plan. Each team has a scope, a mode, a citation floor, a deliverable filename pattern, and a stop condition.

### Team A — Operational Trajectories, Replay, Reliability

**Scope**: Areas #1, #5, #19, #21 (operational trajectories, trajectory replay, operational reliability, dataset).
**Mode**: `/deep-research --mode lit-review`.
**Citation floor**: ≥12 Semantic Scholar paperIDs.
**Output**: `intent-eval-lab/research/001-DR-LITR-trajectory-replay-reliability-2026-05-DD.md`.
**Key questions**: trace schemas in academic releases; replay-fidelity-levels mapping vs literature; operational regression-detection definition.

### Team B — Verification, Calibration, Reasoning Authenticity, Disagreement

**Scope**: Areas #2 (citation-grounding), #4 (synthetic quality), #6 (verifier systems), #11 (reasoning authenticity), #21 (cross-link).
**Mode**: `/academic-pipeline` with stop at stage 6 per operator's Team B target = internal framing only.
**Citation floor**: ≥15 Semantic Scholar paperIDs.
**Output**: `intent-eval-lab/research/002-DR-LITR-verification-calibration-reasoning-2026-05-DD.md`.
**Key questions**: generator/checker independence operationalization; LLM-as-judge calibration SOTA; CoT-authenticity detection methods; synthetic quality metrics operational definitions.

### Team C — Memory, Security, Guardrails, Drift

**Scope**: Areas #7 (memory broadened), #12 (guardrails), #19 (drift cross-link), and the original-gap evaluator-gaming surface.
**Mode**: `/deep-research --mode lit-review` plus three targeted `--mode fact-check` passes on poisoning, drift, gaming threat models.
**Citation floor**: ≥12 Semantic Scholar paperIDs.
**Output**: `intent-eval-lab/research/003-DR-LITR-memory-security-guardrails-drift-2026-05-DD.md`.
**Key questions**: memory-poisoning empirical vs speculative; loop-budget literature formal vs informal; production drift in deployed LLM systems empirical baseline; gaming detection methodology.

### Team D — Observability, Standards, Tool-Use, Inference-Time Compute

**Scope**: Areas #3 (observability), #8 (tool-use), #9 (inference compute), #20 (standards).
**Mode**: `/deep-research --mode Socratic` (4-hour cap) then `/deep-research --mode lit-review`.
**Citation floor**: ≥12 Semantic Scholar paperIDs.
**Output**: `intent-eval-lab/research/004-DR-LITR-observability-standards-tooluse-inference-2026-05-DD.md` plus a proposed semantic conventions gap document feeding `iel-E12`.
**Key questions**: OTel GenAI SIG status (ratified / draft / not-yet); tool-use benchmark instrumentation surfaces; inference-time-compute attribution methods; standards-landscape map.

### Team E — Multi-Agent State, Model Routing

**Scope**: Areas #17 (distributed state), #18 (model routing).
**Mode**: `/deep-research --mode lit-review`.
**Citation floor**: ≥10 Semantic Scholar paperIDs.
**Output**: `intent-eval-lab/research/005-DR-LITR-multiagent-state-model-routing-2026-05-DD.md`.
**Key questions**: state coordination vs `SessionTrace` duplication; routing as new kernel entity vs runtime concern; cost-aware orchestration SOTA.

### Personal-skill pillar — Parked (NOT part of this program)

**Scope**: Areas #13 (curriculum), #14 (compression), #15 (small models), #16 (mechanistic interp).
**Action**: file one OPS bead `ops-personal-pillar-2026-05` at `~/.beads/` tracking the four areas as a long-running personal-development thread. No lit reviews in this program. Quarterly re-evaluation.

### Shared bibliography surface

The companion file `000-RR-BIBL-shared-bibliography-2026-05-20.md` is the citation backbone. Each team filters from there and adds focused queries as needed. Re-running queries at start of work-block N+1 catches new preprints (frontier moves weekly).

### Synthesis — NOT a 5th meta-agent

After 5 lit reviews complete, the operator consolidates manually into the Phase B Framing Memo (`0NN-PP-PLAN-phase-b-framing-memo-2026-05-DD.md`) and triggers `/exec-decision-council` (ISEDC Session 5) on the consolidated memo. An auto-synthesizer would smooth over the cross-team disagreements that are the *whole point* of running 4-5 independent teams. The council is the synthesis surface; the memo is its input.

---

## § 7 — Proposed Phase B bead structure

Fourteen new epic beads + 55-70 child beads + one OPS thread bead. All Phase B epics carry the three-layer mirror discipline (bd ↔ GitHub Issue ↔ Plane LAB).

| Area | Epic ID | Repo | Estimated children | Maps to area(s) |
|---|---|---|---|---|
| Evaluator-disagreement dataset | `iel-E15` | intent-eval-lab | 4-5 | #21 |
| Synthetic cognition quality scoring | `iaj-E09` | j-rig | 4-5 | #4 |
| Memory systems (broadened — poisoning + retrieval + aging) | `iec-E08` | intent-eval-core | 5-6 | #7 |
| Production drift | `iar-E03` | intent-rollout-gate | 3-4 | #19 |
| Evaluator gaming detection | `iaj-E10` | j-rig | 3-4 | #19 cross-link |
| Probabilistic reliability scoring | `iec-E09` | intent-eval-core | 4-5 | linked to all classes |
| Verifier systems (generator/checker split) | `iaj-E11` | j-rig | 4-5 | #6 |
| Reasoning authenticity (CoT verification) | `iaj-E12` | j-rig | 3-4 | #11 |
| Agent guardrails (loop budgets / rollback / permission) | `iar-E04` | intent-rollout-gate | 4-5 | #12 |
| Tool-use training (sequencing / recovery / uncertainty) | `iaj-E13` | j-rig | 4-5 | #8 |
| Inference-time compute attribution | `iel-E16` | intent-eval-lab | 3-4 | #9 |
| Data provenance (synthetic lineage in Evidence Bundle) | `iec-E10` | intent-eval-core | 3-4 | #10 |
| Multi-agent state coordination | `iel-E17` | intent-eval-lab | 4-5 | #17 |
| Model routing | `iar-E05` | intent-rollout-gate | 3-4 | #18 |
| Open trajectory dataset host (defer-or-promote decision) | (FUTURE.md memo) OR `iel-E18` | lab | 0 or 3-4 | (defer-or-promote) |
| Personal-skill pillar | `ops-personal-pillar-2026-05` | OPS workspace | 0 (long-thread) | #13-16 parked |

**Total**: 14 new epics + 55-70 child beads + 1 OPS thread.

**Three-layer mirror impact**: each epic gets a GitHub issue (with `**Beads:**` line listing all child IDs) and a Plane LAB issue under the "Intent Eval Platform" module. Total new GH issues = ~14-15. Total new Plane issues = ~14-15.

**Work estimate (bandwidth, not calendar)**: each epic is roughly 1-3 work-blocks of implementation + 1 work-block of spec authoring. Total Phase B work surface = ~25-40 work-blocks, depending on which epics ratify as P0 vs deferred.

---

## § 8 — Decisions baked into this audit

The following are not open for re-litigation at the framing-memo stage — they are settled in the plan:

1. **SKIP `Imbad0202/academic-research-skills`** — CC-BY-NC 4.0, license-incompatible with our Apache 2.0 platform. Existing installed academic skill suite (deep-research, academic-paper, academic-paper-reviewer, academic-pipeline) is sufficient.
2. **Optionally cherry-pick `multica-ai/andrej-karpathy-skills`** — MIT, coding-discipline ruleset (not actually skills). Phase 0 task: pick 4 principles into `~/.claude/CLAUDE.md` § Core Principles. Not a central component.
3. **5 teams (not 4) plus a parked personal-skill pillar** — original 4-team carving from earlier advisory rounds expanded to accommodate the multi-agent state + model routing surface that emerged in the 20-area advisory.
4. **`academic-pipeline` only on Team B** — most likely to feed a preprint candidate (although user has set Team B target = internal framing only, so stop at stage 6).
5. **Synthesis is human + ISEDC** — not a meta-synthesizer-agent. Preserves cross-team disagreement.
6. **Shared bibliography surface ran first** — already done, file lives at `000-RR-BIBL-shared-bibliography-2026-05-20.md`.
7. **Apache 2.0 license posture for all five IEP repos** is settled and gating dependency choices (Phoenix ruled out at audit time on ELv2 grounds).
8. **DR-010 § 13.5 customer-signal gate is REMOVED** — Phase B is bandwidth-gated, not customer-signal-gated. This document carries no market language; the operator's framing is craft + contribution.

---

## § 9 — Execution plan + timeline

After this document and the ISEDC Session 5 ratification land:

### Phase 0 — Setup (Day 0, ~1 hr)

1. Create `~/000-projects/003-research/` cross-project research staging dir
2. Create `intent-eval-lab/FUTURE.md` (Phase C deferrals memo)
3. Cherry-pick Karpathy coding principles into `~/.claude/CLAUDE.md` § Core Principles (small additive change; pin commit hash)

### Phase 1 — Shared bibliography (already complete)

Output at `000-RR-BIBL-shared-bibliography-2026-05-20.md`. Each team filters from there.

### Phase 2 — Parallel team lit reviews (Days 1-3)

Each team runs in parallel, operator-driven. Skill invocations per § 6.

### Phase 3 — Bead roadmap consolidation (Day 4)

Each team's bead roadmap converted to staged-but-not-yet-created beads per the § 7 table.

### Phase 4 — Phase B Framing Memo + ISEDC Session 5 (Day 5)

Memo at `intent-eval-lab/000-docs/0NN-PP-PLAN-phase-b-framing-memo-2026-05-DD.md`. ISEDC Session 5 ratifies / revises. DECR filed under Doc Filing v4.3.

### Phase 5 — Implementation roadmap update (Day 6)

Bead creation + Plane LAB cross-link + master-plan v2.1 → v2.2.

**Trigger criteria for ISEDC Session 5** (all must be true):

1. All 5 lit reviews filed with citation floors met
2. All 5 bead roadmaps drafted (staged, not yet created)
3. Phase B Framing Memo written
4. ≥2 of the 5 lit reviews surface a finding that contradicts current platform assumptions (forces a real decision, not rubber-stamping)
5. Operator has 90+ uninterrupted minutes available

If criterion 4 fails: skip the council, create beads, proceed with Phase B as planned, document the no-surprise outcome.

---

## § 10 — Risks, verification, open questions

### Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Wall-clock overrun (5 teams × multiple work-blocks) | High | Sequential teams permitted; budget is in work-blocks not calendar days |
| Citation inflation in lit reviews | Medium | Each cited paper must appear in lit-review body; sample-review 3 per team |
| Team C scope explosion (adversarial-ML is bottomless) | Medium-High | Hard cap at 3 threat models in scope (poisoning, drift, gaming) |
| ISEDC fired ritualistically | Medium | Criterion 4 (≥2 contradictions) is non-negotiable |
| Personal-skill pillar bleeds into IEP scope | Low | Single OPS bead, quarterly re-eval, never sub-beaded under iec-/iel-/iah-/iaj-/iar- |
| `Imbad0202` provenance question reopens | Low | Note in `~/.claude/CLAUDE.md` § Initiative — low-priority |
| New advisory surfaces additional areas mid-program | Low | Add as row to § 4, decide team assignment, do NOT spawn a 6th team |

### Verification — how we'd know this worked

**Hard countable criteria**:

1. ✅ 5 lit-review docs filed, each ≥10 paperIDs (≥15 for Team B)
2. ✅ Shared bibliography ≥80 unique paperIDs across all clusters (this document captures ~148 — exceeded)
3. ✅ 14 new epic beads + 55-70 child beads created
4. ✅ Phase B Framing Memo + ISEDC Session 5 DECR filed under Doc Filing Standard v4.3
5. ✅ Master plan v2.2 reflects the new epic structure
6. ✅ Three-layer mirror intact for all new beads via `bd-sync link`
7. ✅ Personal-skill pillar OPS bead filed and visible at `bd list` from `~/`

**Qualitative success criterion**: after ratification, the operator can answer "why are we doing X gap area first?" with a literature citation and a council position, not vibes.

### Open questions for the operator before kickoff

(These are pinned; not blocking this document.)

1. Does Team B's `academic-pipeline` output target arxiv preprint, or stay internal? **OPERATOR ANSWER (2026-05-20): internal framing only.** Stop at stage 6.
2. Personal-skill pillar — Q3 2026 review cadence vs open-ended? **OPEN.**
3. Is `~/000-projects/003-research/` the right home for cross-project research, or should it live under `intent-eval-lab/research/` only? **Current plan: both — IEP-specific lit reviews in lab, cross-project / personal-pillar in 003-research/.**
4. `/exec-decision-council` ISEDC Session 5 — invoke remotely (auto-orchestrated) or interactively (operator in the chair)? **OPEN.**

---

## § 11 — Synthesis: where to build, where to contribute upstream, where to skip

Classifying the 21 areas by leverage of effort × craft interest × open-contribution surface. Phase B P0 ranking recommendation follows.

### Class A — Build-in-our-repos because nobody's done it well in OSS (HIGH leverage)

| Area | Why "build" wins |
|---|---|
| #11 Reasoning authenticity (CoT verification) | Academic literature dense; OSS implementations near-zero. Direct OSS contribution opportunity through j-rig. |
| #21 Evaluator-disagreement dataset | No equivalent open dataset exists. Uniquely positioned to ship. |
| #19 Operational reliability (drift / regression) | LLM-specific drift work sparse; substrate (gate-result/v1 history) is uniquely ours. |
| #4 Synthetic data quality scoring | Academic methodology rich; OSS tooling sparse. Native fit to `EvalCase` provenance. |

### Class B — Build-in-our-repos AND contribute upstream (HIGH-MEDIUM leverage)

| Area | Build target | Upstream target |
|---|---|---|
| #1 Operational trajectories | iel-E12 + kernel | OTel GenAI SIG `gen_ai.agent.trajectory.*` |
| #5 Trajectory replay | iel-E11 RF-X spec | REAL paper alignment + OSS adapters |
| #3 Agent observability | `@intentsolutions/otel-shim` | OTel SIG + OpenInference convention alignment |
| #6 Verifier systems | iaj-E11 + kernel `Verifier` entity | PRM-research community |
| #7 Memory systems (broadened) | iec-E08 entities + threat-model doc | Mem0 / Zep adapter contributions |
| #12 Agent guardrails | iar-E04 entities + gate-result extension | ShieldAgent / Foundational Guardrail |
| #10 Data provenance | iec-E10 Evidence Bundle extension | SLSA framework, sigstore predicate types |
| #20 Open standards | iel-E13 + `gate-result/v1` standards proposal | OTel SIG + MCP + SLSA |
| #2 Eval systems interop | Inspect AI / Promptfoo adapters | Inspect AI repo + Promptfoo |

### Class C — Contribute upstream because someone else's repo is the right home (MEDIUM leverage)

| Area | Why upstream wins |
|---|---|
| #8 Tool-use training | MCP ecosystem is rising standard; adapter to MCPToolBench++ is the contribution path |
| #18 Model routing | LiteLLM / RouteLLM ecosystem is mature; routing-decision metadata addition |
| #17 Multi-agent state | AutoGen / CrewAI / LangGraph each ship abstractions; cross-framework state-model spec is the path |
| #9 Inference-time compute | OTel SIG attribute addition (`gen_ai.usage.thinking_tokens` etc.) |

### Class D — Skip because well-covered AND not interesting to us at infrastructure layer (LOW leverage)

| Area | Why skip |
|---|---|
| #13 Curriculum learning | Foundation-model layer, parked personal-skill |
| #14 Compression / representation | Foundation-model layer, parked personal-skill |
| #15 Small model research | Foundation-model layer, parked personal-skill |
| #16 Mechanistic interpretability | Foundation-model layer, parked personal-skill |

### Recommended Phase B P0 ranking (for operator to confirm or revise at ISEDC Session 5)

Based on **technical leverage** (would this unlock multiple downstream gates) × **craft interest** (does this push the field) × **contribution-uniqueness** (would anyone else ship this in 6 months if we don't):

1. **#21 Evaluator-disagreement dataset** — uniquely-ours, no one else will ship. `iel-E15`.
2. **#11 Reasoning authenticity** — open OSS contribution surface, Anthropic-adjacent. `iaj-E12`.
3. **#6 Verifier systems** — unlocks multiple downstream reliability claims. `iaj-E11`.
4. **#19 Operational reliability** — connects offline to production. `iar-E03`.
5. **#10 Data provenance** — extends our existing sigstore posture. `iec-E10`.
6. **#7 Memory systems (broadened)** — high consumer demand. `iec-E08`.

Phase B P1 (the next 6 in priority order): #4, #12, #20, #1 (already in-flight), #5 (already in-flight), #3 (already in-flight cross-cluster).

Phase B P2 (lower priority but valuable): #8, #18, #17, #9.

**Final synthesis**: the audit ratifies the IEP's existing direction (Areas #1, #2, #3, #5, #20 are core and either mature or in-flight) and identifies six high-leverage new investments (#21, #11, #6, #19, #10, #7) that any one of them, executed well, would meaningfully advance the field. The operator's bandwidth, not customer-signal, gates which subset ships in Phase B.

---

## Appendix A — Installed skill suite inventory

The skills that drive this research program are already installed. No new installs needed.

| Skill | Path | Role in this program |
|---|---|---|
| `deep-research` | `~/.claude/skills/deep-research/` | Teams A, C, D, E lit reviews; 13 agents, 7 modes (full, quick-brief, paper-review, **lit-review**, fact-check, **Socratic**, systematic review) |
| `academic-paper` | `~/.claude/skills/academic-paper/` | Paper-writing (not invoked in this immediate deliverable but available if Team B output extends to preprint) |
| `academic-paper-reviewer` | `~/.claude/skills/academic-paper-reviewer/` | Multi-perspective review (5 reviewers + EIC + Devil's Advocate) — invoked in Team B `academic-pipeline` if used |
| `academic-pipeline` | `~/.claude/skills/academic-pipeline/` | 10-stage end-to-end pipeline; Team B's mode (stop at stage 6 per operator's internal-only directive) |
| `blog-research-article` | `~/.claude/skills/blog-research-article/` | Out of scope for this program but available if Team B's findings spawn a blog post |
| `exec-decision-council` | `~/.claude/skills/exec-decision-council/` | ISEDC Session 5 invocation (Phase 4) |
| `whiteglove-pdf` | `~/.claude/skills/whiteglove-pdf/` | Renders this very document to PDF |
| `email` | `~/.claude/skills/email/` | Delivers the PDF to `jeremy@intentsolutions.io` |

---

## Appendix B — Semantic Scholar MCP coverage assessment

16 seed queries executed via `paper_bulk_search`. Coverage gaps identified:

- **0-hit queries**: OpenTelemetry GenAI conv (academic literature near-zero — confirmed via OSS audit); LLM-self-verification-reasoning-checker (broader synonyms returned hits); SLSA / supply-chain-provenance (industry-driven, not academic); ML production drift (LLM-specific framing too narrow at our threshold); model spec / constitutional AI (citation threshold too high).
- **High-yield queries**: chain-of-thought faithfulness (57 hits), LLM-as-judge bias (56 hits), inference-time compute (38 hits), multi-agent coordination (17 hits), prompt injection defense (23 hits), tool-use function calling (12 hits) — all returned 10+ defensible bedrock papers.

The MCP API is reliable but field-spec is strict — `authors.name` is not valid (must use `authors`), and oversharp queries return 0 even when the field is active.

---

## Appendix C — External repo verdicts

| Repo | License | Verdict | Rationale |
|---|---|---|---|
| `Imbad0202/academic-research-skills` | CC-BY-NC 4.0 | **SKIP** | Non-commercial license incompatible with Apache 2.0 platform posture |
| `multica-ai/andrej-karpathy-skills` | MIT | **OPTIONAL CHERRY-PICK** | Not actually skills — coding-discipline ruleset. Phase 0 task: pick 4 principles into `~/.claude/CLAUDE.md` § Core Principles |

No other external skill suites under evaluation in this program.

---

## Appendix D — Critical files catalog

Will be created during Phase 0-5:

- `~/000-projects/003-research/` — cross-project research staging dir (new)
- `intent-eval-lab/FUTURE.md` — Phase C deferrals memo (new)
- `intent-eval-lab/research/000-RR-BIBL-shared-bibliography-2026-05-20.md` — citation backbone (CREATED — this report's companion)
- `intent-eval-lab/research/000-RR-COMP-ecosystem-landscape-2026-05-20.md` — competitive intel (CREATED — this report's companion)
- `intent-eval-lab/research/000-DR-FIND-iep-phase-b-gap-analysis-and-research-framework-2026-05-20.md` — this document
- `intent-eval-lab/research/001-DR-LITR-trajectory-replay-reliability-2026-05-DD.md` — Team A (Phase 2)
- `intent-eval-lab/research/002-DR-LITR-verification-calibration-reasoning-2026-05-DD.md` — Team B (Phase 2)
- `intent-eval-lab/research/003-DR-LITR-memory-security-guardrails-drift-2026-05-DD.md` — Team C (Phase 2)
- `intent-eval-lab/research/004-DR-LITR-observability-standards-tooluse-inference-2026-05-DD.md` — Team D (Phase 2)
- `intent-eval-lab/research/005-DR-LITR-multiagent-state-model-routing-2026-05-DD.md` — Team E (Phase 2)
- `intent-eval-lab/000-docs/0NN-PP-PLAN-phase-b-framing-memo-2026-05-DD.md` — synthesis (Phase 4)
- `intent-eval-lab/000-docs/0NN-AT-DECR-isedc-session-5-phase-b-priorities-2026-05-DD.md` — council ratification (Phase 4)
- `~/.claude/plans/se-the-council-bubbly-frog-epics-and-beads-for-review-v2.2.md` — updated master plan (Phase 5)
- 14 new epic beads + 55-70 child beads at `~/000-projects/.beads/` (Phase 5)
- 1 OPS bead at `~/.beads/` — personal-skill pillar (Phase 0)

Will be edited (not created):

- `~/.claude/CLAUDE.md` — cherry-pick 4 Karpathy coding principles (Phase 0)
- `intent-eval-platform/README.md` + `CLAUDE.md` — reference Phase B program (Phase 5)
- Plane LAB-6 — update HQ issue body with new epic structure (Phase 5)

---

## Appendix E — Per-area landscape matrix (selected areas)

Landscape matrices for areas where the surface is rich enough to warrant tabular treatment. Each row: project / lab / paper × capability shipped or claimed × license / governance × last meaningful release or commit × integration / contribution potential. **NOT** competitive matrices — landscape audits. Selected areas only (full coverage in the per-area sections above).

### E.1 Observability (Area #3)

| Project | Capability shipped | License | Last release | Integration / contribution potential |
|---|---|---|---|---|
| OpenTelemetry GenAI SIG | Model + agent spans in Development status | Apache 2.0 (CNCF) | semconv updates ongoing as of May 2026 | High — submit `gen_ai.agent.trajectory.*` conventions |
| OpenInference | 47+ instrumentation packages, AI-specific conventions | Apache 2.0 | 2026-05-18 (Go OpenAI) | High — native integration target |
| OpenLLMetry | 257 releases, upstreaming to OTel | Apache 2.0 | v0.60.0 (2026-04-19) | Medium — reference pattern, not direct convergence |
| Phoenix (Arize) | Observability + eval + traces | **Elastic License 2.0** | ongoing | Low — license-incompatible |
| Langfuse | Observability + eval + prompt mgmt | MIT core / ee | v3.174.1 (2026-05-13) | Low — different surface |
| AgentOps paper | Academic framing for agent obs | (paper) | 2024 | Reference citation |

### E.2 Eval frameworks (Area #2)

| Project | Capability | License | Last release | Integration / contribution potential |
|---|---|---|---|---|
| Inspect AI (UK AISI) | 200+ pre-built evals, tool-use, multi-turn, model-graded | MIT | 5714 commits, active | Highest — standards-track precedent, government-backed |
| Promptfoo | CLI + library, prompt testing, red-team, CI/CD | MIT (now OpenAI subsidiary) | v0.121.11 (2026-05-08), 408 releases | Medium — CI-pattern reference, adapter target |
| DSPy (Stanford NLP) | Programming model, Assertions, optimizer | MIT | v3.2.1 (2026-05-05) | Low — orthogonal surface |
| MT-Bench (Zheng et al.) | LLM-as-judge benchmark format | (paper + repo) | NeurIPS 2023 (8440 cites) | Citation-grounding only |

### E.3 Benchmarks / datasets (Areas #1, #5)

| Project | Capability | License | Last update | Integration / contribution potential |
|---|---|---|---|---|
| SWE-bench (Princeton NLP) | Real-world GitHub issues, Docker eval logs, leaderboard | MIT | 2025-01-13 (Multimodal + sb-cli) | High — replay-fidelity classification test set |
| OSWorld | Computer-use agent benchmark with screenshots/actions/video | Apache 2.0 | 2025-07-28 (OSWorld-Verified + AWS parallelization) | High — `agent-loop-trace/v1` test case |
| tau-bench (Sierra Research) | Conversational agent + tool benchmark | MIT | active, redirected to tau³ | Medium — trajectory format reference |
| METR eval-analysis-public | Time-horizon methodology, raw `runs.jsonl` | (license unspecified) | 24 commits | Medium — reliability scoring sanity check |
| REAL paper | Deterministic simulations of real websites | (paper) | 2025 (26 cites) | High — replay-fidelity literature alignment |

### E.4 Memory frameworks (Area #7)

| Project | Capability | License | Last release | Integration / contribution potential |
|---|---|---|---|---|
| Mem0 (paper + repo) | Production-ready scalable long-term memory | (check repo, paper Apache-feeling) | ECAI 2025, 319 cites | High — adapter pattern + memory integrity attestation |
| Zep | Temporal knowledge graph architecture | (check repo) | 2025, 161 cites | High — temporal-KG semantics input to our memory spec |
| LoCoMo paper | Very long-term conversational memory benchmark | (paper + dataset) | ACL 2024, 432 cites | Citation-grounding |
| BABILong | Long-context reasoning benchmark | (check repo) | NeurIPS 2024, 203 cites | Citation-grounding |

### E.5 Standards bodies (Area #20)

| Body | Spec / surface | License / governance | Active? | Contribution potential |
|---|---|---|---|---|
| OpenTelemetry GenAI SIG | Semantic conventions (in Development) | Apache 2.0 (CNCF) | Highly | Highest — gate-result/v1 + trajectory conventions |
| OpenInference (Arize) | Complementary AI-spec semantic conventions | Apache 2.0 | Highly | High — convention alignment |
| MCP (Model Context Protocol) | Tool-call protocol | Anthropic-led, multi-vendor adopted | Highly | High — tool-call attestation |
| SLSA framework | Supply-chain attestation predicates | OpenSSF | Active | Medium — synthetic-data provenance predicate type |
| Sigstore | Artifact signing | CNCF | Highly | Medium — already integrated |
| W3C | (no formal AI WG) | — | No | Skip |

### E.6 Multi-agent frameworks (Area #17)

| Project | Capability | License | Last release | Integration / contribution potential |
|---|---|---|---|---|
| AutoGen (Microsoft) | Multi-agent framework | MIT | active | Medium — state-model convergence target |
| CrewAI | Multi-agent roles + tasks | MIT | active | Medium — adapter pattern |
| LangGraph (LangChain) | Graph-based multi-agent orchestration | MIT | active | Medium — composition-dag alignment |
| MetaGPT | Multi-agent software development team | MIT | active | Reference |
| MegaAgent paper | Without predefined SOPs | (paper) | ACL 2025, 43 cites | Citation-grounding |
| SagaLLM paper | Context mgmt + validation + transactions | (paper + repo) | VLDB 2025, 34 cites | High — direct alignment opportunity |

### E.7 Tool-use benchmarks (Area #8)

| Project | Capability | License | Last release | Integration / contribution potential |
|---|---|---|---|---|
| MCP-Bench | MCP-server-based tool-use benchmark | (check) | 2025, 58 cites | High — adapter to gate-result/v1 |
| MCPToolBench++ | Large-scale MCP tool benchmark | (check) | 2025, 24 cites | High — direct adapter |
| TRAJECT-Bench | Trajectory-aware agentic tool-use | (check) | 2025, 11 cites | Medium |
| xLAM | Large action model family | (check) | 2024, 103 cites | Citation-grounding |

### E.8 Routing frameworks (Area #18)

| Project | Capability | License | Last release | Integration / contribution potential |
|---|---|---|---|---|
| LiteLLM (BerriAI) | De-facto LLM proxy + router | MIT | active | High — routing-decision metadata addition |
| RouteLLM (Anyscale-affiliated) | Open routing framework | (check) | active | Medium |
| MasRouter paper | Routing for multi-agent systems | (paper) | ACL 2025, 52 cites | Citation-grounding |

(Areas #4, #6, #9-12, #19, #21 covered in their per-area treatments; full landscape matrices in companion competitive-intel doc.)

---

## Appendix F — Personal-skill pillar (FM-level research items, NOT IEP)

Four areas from the May 2026 advisory rounds are foundation-model-level research and explicitly out of IEP scope. They are tracked as a single OPS bead — `ops-personal-pillar-2026-05` — as a long-running personal-development thread.

| Area | Description | Pedagogical reference |
|---|---|---|
| #13 Curriculum learning | Training-data ordering for sample efficiency | nanoGPT + Karpathy's training-from-scratch series |
| #14 Compression / representation | Quantization, pruning, distillation | llama.cpp + GGUF tooling |
| #15 Small model research | 0.5B-10B-parameter pedagogical training | Karpathy's "Build a Transformer From Scratch" |
| #16 Mechanistic interpretability | Reverse-engineering trained-model internals | TransformerLens (Neel Nanda), Anthropic SAE releases |

**Cadence**: quarterly re-evaluation. Never spawns sub-beads under iec-/iel-/iah-/iaj-/iar- prefixes — that would contaminate IEP scope. If material from this pillar later becomes relevant to a kernel decision, it gets cited but not re-scoped.

---

## Appendix G — Phase B P0 work breakdown (bead-level detail)

For each of the six P0-recommended epics from § 11, the detailed bead-level work breakdown. This appendix is provided as a starting position for ISEDC Session 5 ratification — operator may revise sequence, scope, or priority assignment based on council discussion.

### G.1 — `iel-E15` Evaluator-disagreement dataset (P0 recommended)

**Repo**: intent-eval-lab. **Estimated children**: 4-5 beads. **Work-blocks**: 3-4. **Maps to area #21.**

Child beads (proposed):

1. `iel-E15a` — dataset schema spec. Define per-record shape: case_id, prompt, response, judges_run (array of `JudgeResult` records each with model_id, model_family, score, reasoning_text, timestamp), consensus_indicator, divergence_score. Reference: existing `gate-result/v1` schema as starting point. **Work-block**: 0.5.
2. `iel-E15b` — curation policy spec. Define case selection: synthetic + human-curated balanced across (factuality, reasoning, summarization, code-review, safety) domains. Sampling discipline to prevent contamination. **Work-block**: 0.5.
3. `iel-E15c` — hosting decision. Recommendation: HuggingFace Datasets, Apache-2.0 license (matches platform posture). Decision artifact at `intent-eval-lab/000-docs/0NN-AT-DECR-iel-E15-hosting.md`. **Work-block**: 0.25.
4. `iel-E15d` — initial release (v0.1.0 with 200-500 cases, 5-7 judges per case). **Work-block**: 1.5.
5. `iel-E15e` — quarterly update cadence and governance model (community-suggest, maintainer-curate). **Work-block**: 0.5.

Dependencies: none external. Internal: existing `gate-result/v1` schema (already published). Risk: medium-low (uniquely-ours work, no contention for upstream coordination). Upstream-cycle path: HuggingFace dataset publication; arxiv methodology note candidate (operator declined Team B preprint posture, so internal-only).

### G.2 — `iaj-E12` Reasoning authenticity (P0 recommended)

**Repo**: j-rig-skill-binary-eval. **Estimated children**: 3-4 beads. **Work-blocks**: 3-4. **Maps to area #11.**

Child beads (proposed):

1. `iaj-E12a` — faithfulness-judge spec. Define three faithfulness probes based on academic literature: paraphrase-invariance test, biased-context test, reasoning-step unlearning test (per `aaaa0435…`). Each probe is a j-rig judge implementation. **Work-block**: 1.
2. `iaj-E12b` — gate-result/v1 extension proposal. Add optional `cot_faithfulness` block carrying probe results, aggregated score, and judge metadata. Likely requires `iec-deferral-*` Class-2 ISEDC decision. **Work-block**: 0.5.
3. `iaj-E12c` — reference implementation in j-rig with at least one supported model family. **Work-block**: 1.5.
4. `iaj-E12d` — FaithCoT-Bench integration test (per `6968f45a…`). **Work-block**: 1.

Dependencies: `iec-deferral-D` (gate-result/v1 coverage element shape lockup) for the schema extension. Risk: medium (probe robustness under prompt-engineering pressure). Upstream-cycle path: probe methodology paper candidate.

### G.3 — `iaj-E11` Verifier systems (P0 recommended)

**Repo**: j-rig-skill-binary-eval (+ kernel touchpoint). **Estimated children**: 4-5 beads. **Work-blocks**: 3-4. **Maps to area #6.**

Child beads (proposed):

1. `iaj-E11a` — `Verifier` first-class entity proposal for Blueprint B § 4. Includes `independence_class` enum: `same-prompt`, `different-prompt-same-model`, `different-model-same-family`, `different-family`, `non-llm-rule`. Requires ISEDC Class-2 sign-off. **Work-block**: 0.5.
2. `iaj-E11b` — kernel work to add `Verifier` to `intent-eval-core` if approved. **Work-block**: 1.
3. `iaj-E11c` — gate-result/v1 extension to carry verifier identity + independence_class per verification step. **Work-block**: 0.5.
4. `iaj-E11d` — j-rig implementation of independent-judge-pairings with measured cross-judge correlation reporting. **Work-block**: 1.5.
5. `iaj-E11e` — document existing audit-harness gates (escape-scan, crap-score, arch-check) as canonical non-LLM verifiers per Verifier taxonomy. **Work-block**: 0.5.

Dependencies: ISEDC Class-2 sign-off on `Verifier` entity addition. Cross-cuts: every area that uses verification (#2, #11, #12, #19). Risk: medium-high (kernel surface addition has compound downstream effects).

### G.4 — `iar-E03` Operational reliability (P0 recommended)

**Repo**: intent-rollout-gate. **Estimated children**: 3-4 beads. **Work-blocks**: 3-4. **Maps to area #19.**

Child beads (proposed):

1. `iar-E03a` — drift-detection schema. Define `DriftSignal` shape: window (timestamp range), eval_id, baseline_period, current_period, divergence_metric, divergence_score, alert_threshold. **Work-block**: 0.5.
2. `iar-E03b` — failure-class taxonomy. Authoritative enum of failure classes (e.g., `regression_correctness`, `regression_latency`, `regression_cost`, `drift_capability`, `drift_calibration`, `evaluator_gaming`). Document at `intent-eval-lab/specs/reliability-v1.md`. **Work-block**: 0.5.
3. `iar-E03c` — extend rollout-gate to consume historical context. Given current gate-result + N-day window of prior gate-results for same eval, compute drift signals and surface in decision output. **Work-block**: 1.5.
4. `iar-E03d` — integration test fixtures with a generated history simulating drift / regression / gaming. **Work-block**: 1.

Dependencies: existing `gate-result/v1` published. Risk: medium (drift-detection methodology under LLM regime is unsettled). Upstream-cycle path: methodology paper candidate; potential contribution to Evidently AI or NannyML for LLM-specific drift detection.

### G.5 — `iec-E10` Data provenance (P0 recommended)

**Repo**: intent-eval-core. **Estimated children**: 3-4 beads. **Work-blocks**: 2-3. **Maps to area #10.**

Child beads (proposed):

1. `iec-E10a` — `EvalCase.provenance` field spec. Synthesis_provenance object (generator_model, seed, timestamp, generation_version) plus optional `derivation_chain` (predecessor case IDs). **Work-block**: 0.5.
2. `iec-E10b` — `EvalSuite.provenance` field spec. Whole-suite provenance + signed-by metadata. **Work-block**: 0.5.
3. `iec-E10c` — `provenance-attest.sh` script for audit-harness. Generates SLSA-aligned attestation for a test-suite. **Work-block**: 1.
4. `iec-E10d` — document the provenance model at `intent-eval-lab/specs/provenance-v1.md` with reference to SLSA framework + sigstore predicate types. **Work-block**: 0.5.

Dependencies: existing sigstore + harness-hash infrastructure (already in place). Cross-cuts: every other epic benefits from completed provenance. Risk: low-medium (well-trodden SLSA / sigstore territory).

### G.6 — `iec-E08` Memory systems (P0 recommended)

**Repo**: intent-eval-core. **Estimated children**: 5-6 beads. **Work-blocks**: 4-5. **Maps to area #7.**

Child beads (proposed):

1. `iec-E08a` — `Memory`, `MemoryStore`, `MemoryItem` first-class entities for Blueprint B § 4. Requires ISEDC Class-2 sign-off. **Work-block**: 0.5.
2. `iec-E08b` — kernel additions for the three entities. **Work-block**: 1.
3. `iec-E08c` — `gate-result/v1.memory_integrity_class` field with enum: `verified_clean`, `untested`, `flagged_drift`, `flagged_poisoning_risk`, `flagged_aging`. **Work-block**: 0.5.
4. `iec-E08d` — memory threat-model document at `intent-eval-lab/specs/memory-threat-model-v1.md` covering the four-axis failure taxonomy with academic citations. **Work-block**: 1.
5. `iec-E08e` — adapter pattern for Mem0 (or Zep) integration as proof-of-concept. **Work-block**: 1.5.
6. `iec-E08f` — connection to `iec-deferral-G` (tenant_id reservation) for multi-tenant memory isolation. **Work-block**: 0.5.

Dependencies: ISEDC Class-2 sign-off on memory entity additions. Cross-cuts: prompt-injection literature (Area #12), drift detection (Area #19). Risk: medium-high (memory is a broad surface; scope creep is the main risk).

### G.7 — Aggregate Phase B P0 commitment

Summing the six P0 work-block estimates: ~18-24 work-blocks of construction + ~4-6 work-blocks of upstream-cycle engagement = ~22-30 total work-blocks. At a conservative pace of 3-4 work-blocks per week of operator capacity, this is **6-10 weeks of focused Phase B P0 execution**, assuming no Class-2 ISEDC blockers delay kernel-surface additions.

If operator bandwidth is constrained to a subset, the dropdown priority would be (in retention order):

1. Retain `iel-E15` (uniquely-ours, low-coordination)
2. Retain `iaj-E12` (uniquely-ours, mid-coordination)  
3. Retain `iec-E10` (low-risk, defensive value)
4. Defer `iec-E08` (high-scope, coordination-heavy) → Phase C
5. Defer `iaj-E11` (kernel-surface-addition coordination cost) → Phase C
6. Defer `iar-E03` (depends on production data we may not have) → Phase C

This dropdown is a starting position only — ISEDC Session 5 owns the final call.

---

## Appendix H — Questions for ISEDC Session 5

Structured question list, organized by council seat, for the Phase B Framing Memo's adjudication. These are the questions whose answers should be captured verbatim in the AT-DECR record per § 8.

### H.1 — Questions for the CTO seat (technical leverage)

1. Of the 14 new epics, which six (or however many) earn P0 status given the operator's bandwidth ceiling?
2. Should `Verifier`, `Memory`, `MemoryStore`, `Tool`, `ToolInvocation` enter the kernel as first-class entities? Apply the "two-downstream-consumer + one-external-standard" rule from § 4.5.7.
3. Should a single `TrustPosture` entity roll up Memory + Guardrail + Drift, or are the separate entities the right granularity (§ 4.5.5)?
4. Which `iec-deferral-*` Class-2 specs are blocking enough Phase B work to warrant immediate closure?
5. Is `iel-E12` (`agent-loop-trace/v1`) ready to ship a stable v1 by end of Phase B, or does it need additional design iteration?

### H.2 — Questions for the GC seat (governance, licensing, legal risk)

1. Is Apache 2.0 the right license for `iel-E15` (evaluator-disagreement dataset), or should it be CC-BY-SA 4.0 to match dataset-licensing conventions?
2. What attribution / contribution policy governs community submissions to `iel-E15`?
3. Are there partner-consent constraints on any data that would enter `iel-E15`? Default discipline: synthetic only, no partner-sourced material without explicit consent.
4. Should the platform document a formal contribution path (CLA / DCO) for upstream proposals to OTel SIG and OpenInference?
5. Any IP exposure from submitting `gate-result/v1` as a standards-track proposal? Default expectation: none (it's documented in public specs already).

### H.3 — Questions for the CMO seat (positioning, narrative)

1. Phase B work is framed as craft + contribution per DR-010 § 13.5 (customer-signal gate removed). Does any P0 epic require a public-facing positioning artifact (blog, white paper, conference proposal)?
2. Should `iel-E15` (dataset) launch with a methodology note for academic visibility, or land quietly?
3. Is the platform's existing OSS distribution (claude-code-plugins 45k+ NPM following) appropriate for Phase B-era cross-promotion of new artifacts?
4. Any external comms calendar conflicts (Anthropic certification, partner engagements) that should constrain Phase B announcement timing?

### H.4 — Questions for the CFO seat (operational cost, ROI)

1. Phase B P0 estimate is 22-30 work-blocks (~6-10 weeks). Is that operator bandwidth available given competing demands (VPS-as-the-home program, Anthropic certification work, partner engagements)?
2. What is the opportunity cost of running Phase B P0 vs accelerating other in-flight programs?
3. Are there token / API costs in Phase B work that should be budgeted explicitly (e.g., running multi-judge eval suites at scale for `iel-E15`)?

### H.5 — Questions for the CSO seat (long-term strategy, competitive positioning)

1. The audit identifies four "no-OSS-equivalent" areas (§ 4.5.3). Shipping these first compounds platform defensibility. Does the council ratify this sequencing?
2. The audit identifies OpenTelemetry GenAI SIG as the highest-leverage upstream surface (§ 4.5.2). Does the council ratify dedicating one work-block to SIG engagement early in Phase B?
3. Phase B is bandwidth-gated; what is the explicit Phase C trigger (capacity-based, milestone-based, calendar-based)?

### H.6 — Questions for the CISO seat (security, attestation, compliance)

1. The data provenance epic (`iec-E10`) extends Evidence Bundle with synthetic-data lineage. Does this require any cryptographic posture changes (key rotation, attestation envelope updates)?
2. Memory threat-model document (`iec-E08d`) will reference attack literature (AgentPoison, MemoryGraft, CtrlRAG). Is the public-facing posture appropriate, or should specific attack details remain in private specs?
3. The reasoning-authenticity work (`iaj-E12`) implicitly addresses deception-detection. Is this material the council wants public, or held internal?

### H.7 — Questions for the VP DevRel seat (community, contribution, ecosystem)

1. The audit ratifies the kernel's anti-goal posture (§ 4.5.4) — we define schemas, emit attestations, ship validators; we do NOT host runtime. Does the council reaffirm this posture in the Phase B DECR?
2. The four no-OSS-equivalent areas (§ 4.5.3) represent strong contribution-from-nothing opportunities. Should Phase B include explicit community-engagement targets (e.g., one external contributor onboarded per epic)?
3. Should `iel-E15` adopt community-driven curation from launch, or maintainer-curated with later community opening?
4. Are there OSS partner engagements (Mem0, Zep, Inspect AI) the council wants explicitly invited to participate in Phase B?

### H.8 — Cross-seat synthesis questions

1. Phase B is the platform's first post-Phase-A construction sprint. Should the council establish a "Phase B retrospective" requirement (AAR within 30 days of Phase B close)?
2. What is the smallest Phase B that the council considers worth executing? Said differently: under what scope-reduction would the council say "skip Phase B and go directly to Phase C"?
3. Are there entirely-new strategic concerns surfacing from this audit that warrant a separate ISEDC session before Phase B kickoff?

The DECR record at `intent-eval-lab/000-docs/0NN-AT-DECR-isedc-session-5-phase-b-priorities-2026-05-DD.md` should capture verbatim positions from each seat on the questions material to the final ranking.

---

## Appendix I — Foundational paper walkthroughs

Substantive engagement with fifteen of the most-foundational papers across the five research clusters. Each walkthrough names the paper, summarizes its core claim, identifies what's empirically established vs unresolved, and notes the implementation implication for IEP. Selected by citation weight and methodological relevance — not exhaustive of the bibliography.

### I.1 Turpin et al. — "Language Models Don't Always Say What They Think" (NeurIPS 2023, S2: `7dc928f4…`, 1097 citations)

The foundational paper for chain-of-thought (un)faithfulness research. The authors demonstrate that LLMs given biasing context produce verbal explanations consistent with the bias while their final answer reveals the bias is influencing the output — but the verbal reasoning never mentions it. The intervention methodology — comparing CoT with and without biasing context — became the canonical faithfulness probe.

**Empirically established**: post-hoc rationalization is detectable in many production CoT outputs. **Unresolved**: whether reasoning-trained models (DeepSeek R1, OpenAI o-series, Anthropic extended thinking) exhibit the same pattern or different patterns. Lanham et al. ("Reasoning Models Don't Always Say What They Think," `b9ca6db2…`, 297 cites) extended the methodology to o-series and confirmed similar issues, with new failure modes specific to reasoning-trained models.

**IEP implication**: any CoT-monitored gate (e.g., "halt if visible reasoning contains pattern P") is defeasible to the extent the visible reasoning is unfaithful. The `iaj-E12` reasoning-authenticity epic should implement Turpin's intervention-based probe as a baseline judge — the cheapest defensible faithfulness measurement.

### I.2 Zheng et al. — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (NeurIPS 2023, S2: `a0a79dad…`, 8440 citations)

The most-cited LLM-as-judge paper. Defined the MT-Bench dual-rater methodology and the Chatbot Arena framework still used by HuggingFace's leaderboard. Established that LLMs can serve as approximate human-judge proxies for free-form evaluation tasks while exposing systematic biases (position bias, verbosity bias, self-preference).

**Empirically established**: LLM-judges work above-random for free-form evals; specific biases (position, verbosity, self-preference, length) are reproducible. **Unresolved**: how to quantitatively bound judge error vs human judgment under realistic conditions. The 1300+ cite survey paper (Li et al., `e2442428…`) consolidates the field but does not converge on operational thresholds.

**IEP implication**: every gate-result/v1 record using an LLM judge must capture the judge identity (model, version, prompt-template-hash) and ideally a measured cross-judge correlation. Our `iel-E15` evaluator-disagreement dataset is the empirical-anchor that makes this measurable across platform users.

### I.3 Chen et al. — "AgentPoison: Red-Teaming LLM Agents via Poisoning Memory or Knowledge Bases" (NeurIPS 2024, S2: `b6948a9e…`, 293 citations)

The foundational memory-poisoning paper for LLM agents. Demonstrates that adversarial memory items can be crafted to trigger specific malicious behaviors when retrieved, without modifying the model itself. The attack succeeds under realistic RAG configurations on production agents (LLaMA, GPT-4-class).

**Empirically established**: memory poisoning is a real, demonstrable attack surface on production-style agents. **Unresolved**: defensive postures — sanitization, retrieval-time integrity checks, attestation chains — have not converged. The follow-on work (MemoryGraft `b1d80b2e…`, CtrlRAG `b308393d…`, NeuroGenPoisoning `a776dcb6…`) demonstrates the attack surface widens, not narrows.

**IEP implication**: `iec-E08` memory entities must encode "where did this memory item come from" (provenance) and "was it verified before use" (attestation). The four-axis failure taxonomy in § 4 Area #7 should map to specific defenses with citation back to this paper's attack methodology.

### I.4 Zhang et al. — "Agent Security Bench (ASB)" (ICLR 2025, S2: `5f4efbe3…`, 219 citations)

Formalizes attacks and defenses across the LLM-agent stack. Benchmarks 11 attack types (prompt injection, indirect prompt injection, tool misuse, memory poisoning, role hijacking, etc.) against 10 defense strategies. The first comprehensive empirical comparison of defense efficacy.

**Empirically established**: no current defense is universally effective; defense-in-depth (multiple complementary defenses) outperforms any single defense. **Unresolved**: optimal defense composition under cost constraints; novel attack surfaces emerging from MCP / multi-agent / tool-use evolution.

**IEP implication**: the `iar-E04` guardrails epic should structure its decisions around the ASB taxonomy. Guardrail-trigger reasons in `gate-result/v1` should align with ASB attack categories so cross-organization comparison is possible.

### I.5 Snell et al. — "Sample, Scrutinize and Scale: Effective Inference-Time Search by Scaling Verification" (ICML 2025, S2: `b67c8d21…`, 37 citations) (note: cited as Google DeepMind/Stanford collaboration)

Demonstrates that scaling verification compute is often more effective than scaling generation compute at inference time. For complex reasoning tasks, generating many candidates and verifying carefully outperforms generating one and trusting it.

**Empirically established**: verifier scaling beats generator scaling above a threshold of task difficulty. **Unresolved**: precise crossover thresholds; what makes a verifier "scalable" (i.e., quality continues to improve with more compute) vs "saturated."

**IEP implication**: `iaj-E11` verifier systems should treat verifier-scaling characteristics as a measurable property. The kernel's `Verifier` entity (proposed) should carry `scaling_class` metadata: `saturated` vs `linear` vs `near-linear` improvement under increased compute.

### I.6 Bansal et al. — "Smaller, Weaker, Yet Better: Training LLM Reasoners via Compute-Optimal Sampling" (ICLR 2025, S2: `41a4234a…`, 71 citations)

Counter-intuitive finding: training data generated by smaller / weaker models can produce better reasoning capability in the trained model than data from larger / stronger models, when compute-budget is held constant. The mechanism: weaker generators produce more diverse + more pedagogically-informative training data.

**Empirically established**: synthetic-data-quality is not monotonic in generator capability. **Unresolved**: which downstream tasks benefit most; how to predict in advance which generator-strength is optimal for a given training objective.

**IEP implication**: `iaj-E09` synthetic-cognition-quality-scoring should not assume "stronger generator = higher quality data." The `synthesis_provenance` field on `EvalCase` should capture generator-strength explicitly so downstream consumers can characterize the generator-strength distribution of a suite.

### I.7 Khattab et al. — DSPy framework (`stanfordnlp/dspy`, MIT, v3.2.1 May 2026)

The dominant academic-origin framework for "programming, not prompting" — composing modular Python programs that the framework optimizes via teleprompter / Bootstrap / MIPRO algorithms. The Assertions abstraction (Dec 2023) allows non-LLM verification of intermediate states.

**Empirically established**: program-then-optimize is more reliable than prompt-engineering for complex tasks. **Unresolved**: the relationship between optimizer-found prompts and downstream interpretability; what fraction of DSPy-discovered prompts are robust to model updates.

**IEP implication**: DSPy is orthogonal to IEP — it's a development-time framework, not a runtime decision-gate. But Assertions could be a clean integration point: a DSPy Assertion is a non-LLM verifier emitting a gate-result/v1-compatible artifact.

### I.8 Lin et al. — "SagaLLM: Context Management, Validation, and Transaction Guarantees for Multi-Agent LLM Planning" (VLDB 2025, S2: `356b85ae…`, 34 citations)

Brings database-theoretic transaction semantics to multi-agent LLM planning. Defines saga-style compensation patterns for agent rollback, isolation properties for parallel agent execution, and consistency guarantees that survive partial agent failures.

**Empirically established**: applying transaction theory to multi-agent LLMs is feasible and improves reliability under failures. **Unresolved**: which guarantees are most commercially valuable; cost-vs-reliability tradeoffs.

**IEP implication**: `iel-E17` multi-agent state coordination should treat SagaLLM as a primary alignment target. Our `CompositionDag` entity (Blueprint B) should support saga-style compensation as a declarable property.

### I.9 He et al. — "Red-Teaming LLM Multi-Agent Systems via Communication Attacks" (ACL 2025, S2: `4669474d…`, 94 citations)

Demonstrates attack vectors specific to multi-agent communication. Agent-to-agent prompt injection (where one agent's response payload contains an injection that affects the receiving agent), role-hijacking via coordinated messaging, and information-flow attacks across agent boundaries.

**Empirically established**: multi-agent attack surface is larger than single-agent; existing single-agent defenses do not fully transfer. **Unresolved**: minimum-coordination-overhead defense patterns; how multi-agent guardrails should propagate.

**IEP implication**: `iar-E04` guardrails must consider multi-agent propagation patterns. A single-agent-only guardrail spec is incomplete; the spec should explicitly enumerate which guardrails are per-agent vs cross-agent.

### I.10 Ong et al. — Mem0 (ECAI 2025, S2: `1d9c21a0…`, 319 citations)

Production-ready scalable long-term memory for AI agents. Distinguishes episodic memory (specific events), semantic memory (learned facts), and procedural memory (skills). Provides empirical measurements of memory recall + relevance + persistence at scale.

**Empirically established**: long-term memory architectures are operationalizable in production. **Unresolved**: optimal eviction / aging policies under cost constraints; how memory contents should be versioned and provenance-tracked.

**IEP implication**: `iec-E08` memory entities should be expressible in terms compatible with Mem0's distinctions (episodic / semantic / procedural). The Mem0 paper provides the empirical baseline for `MemoryItem.aging_policy` defaults.

### I.11 Lewis et al. — "BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack" (NeurIPS 2024, S2: `b47507f1…`, 203 citations)

Demonstrates systematic failure modes in long-context LLMs: models claim to use long context but empirically fail on long-context reasoning tasks beyond ~32K tokens. The "needle in a haystack" framing exposes both retrieval failures (can't find the needle) and reasoning failures (find but can't reason with it).

**Empirically established**: long-context capability is overclaimed by model providers; benchmarks must include long-context-reasoning, not just long-context-retrieval. **Unresolved**: which architectural changes (memory architectures, retrieval-augmentation, chunk-aware attention) most efficiently address the limits.

**IEP implication**: memory-related gates should distinguish "retrieval succeeded" from "reasoning over retrieved content succeeded." `gate-result/v1` extensions for memory should carry both retrieval-success and reasoning-success indicators.

### I.12 OpenInference (Arize-ai, Apache 2.0, ~1865 commits May 2026)

Not a paper — an active OSS specification. Defines AI-specific semantic conventions complementary to OpenTelemetry, with implementations in Python, TypeScript, Java, Go. The closest extant standard for cross-toolchain LLM observability conventions.

**Established**: 30+ instrumentation packages for production frameworks (OpenAI, Anthropic, LangChain, LlamaIndex, Bedrock, etc.). **Open**: alignment with OpenTelemetry GenAI SIG; whether OpenInference becomes a permanent companion or eventually upstreams entirely.

**IEP implication**: `iel-E12` agent-loop-trace conventions should explicitly target OpenInference compatibility. A reference instrumentation package (`@intentsolutions/otel-shim`) that emits OpenInference-compliant spans is a direct deliverable.

### I.13 Inspect AI (UK AISI, MIT, 5714 commits)

UK AI Security Institute's evaluation framework. 200+ pre-built evals, tool-use + multi-turn + model-graded support, government-backed. The strongest standards-track precedent we identified — backed by a regulator-adjacent body, MIT-licensed, multi-surface.

**Established**: dominant academic-research-team eval framework; high-credibility platform for dangerous-capability evals. **Open**: how organizations outside the government-affiliated network adopt and contribute.

**IEP implication**: Inspect AI's eval-result shape is the convergence target for `gate-result/v1` interop. A bidirectional adapter (gate-result ↔ Inspect result) is a defensible upstream contribution to either repo.

### I.14 Jimenez et al. — SWE-bench (Princeton NLP, MIT, last update Jan 2025)

Real-world GitHub issues as evaluation tasks. SWE-bench Verified (500 issues confirmed solvable by humans), SWE-bench Multimodal (visual software), SWE-bench Pro (long-horizon). The foundational benchmark for autonomous coding agents.

**Established**: defensible benchmark with strong human-baseline; widely-adopted leaderboard. **Open**: dataset contamination risk (issues are publicly accessible); long-tail issue selection bias; replay-fidelity (logs available but not deterministic-replay specced).

**IEP implication**: SWE-bench is the canonical test case for `iel-E11` RF-X classification (logs-only ≈ RF-1). Integration test fixtures importing SWE-bench Verified results should ship in `intent-eval-core`.

### I.15 Hubinger et al. — "Sleeper Agents" (Anthropic, broadly cited)

(Note: cited as anchor literature for the deception-detection / reasoning-authenticity surface; not in our bulk-search result set due to specific query phrasing.) Demonstrates that backdoored language models can be trained to behave normally during evaluation and pathologically in production-trigger conditions. Standard safety training fails to remove the backdoors.

**Established**: backdoor-style deception is empirically demonstrable at frontier scale; existing evaluation methodology may not catch it. **Open**: detection methodologies; whether emergent deception (vs explicitly-trained-in deception) is similarly hard to detect.

**IEP implication**: any gate that uses LLM-as-judge has an upper-bound on detection-of-deception. The `iaj-E12` reasoning-authenticity epic should explicitly acknowledge this bound — our judges measure what's measurable; deeper deception is out of scope for the current methodology.

### I.16 Closing observation on the foundational corpus

The fifteen papers + repos above span the empirical bedrock for the six recommended P0 epics. Every P0 epic in § 11 has at least two foundational citations from this set; every cross-cutting finding in § 4.5 has at least one anchor. The audit's defensibility rests on this corpus — a critic asking "why does Phase B prioritize X" can be answered with paper-specific evidence rather than abstract argument.

The corpus is overwhelmingly post-2023, with the median publication date in 2024-2025. The field is moving fast; this audit will require refresh at each major phase boundary. The shared bibliography file (000-RR-BIBL) is the substrate for future refreshes.

---

## Appendix J — Glossary of audit-specific terms

Terms defined for this audit's purposes. Where a term has a canonical definition in the platform glossary (`intent-eval-lab/000-docs/014-DR-GLOS-canonical-glossary.md`), this glossary defers — entries here cover only audit-specific usages or shorthand.

**`agent-loop-trace/v1`** — proposed canonical event taxonomy for agent runs, under iel-E12. Distinct from `SessionTrace` (entity in kernel) by being the wire-format for events flowing into a SessionTrace. The relationship is approximately: a `SessionTrace` is the *aggregated* artifact composed from many `agent-loop-trace/v1` events.

**Build vs contribute** — shorthand for the audit's classification of work effort. "Build" = construct in our repos (intent-eval-core / lab / audit-harness / j-rig / rollout-gate). "Contribute" = submit upstream to an existing OSS project, standards body, or community spec. The audit uses this binary to focus operator decisions; in practice, many epics involve both (build the in-repo capability and contribute the spec upstream).

**Class-2 ISEDC decision** — adjudication required at the 7-seat ISEDC executive council for decisions that ripple across downstream consumers or affect immutable artifacts (predicate URIs, attestation envelopes, kernel entity additions, normative spec changes). Distinct from Class-1 (operational) which doesn't require council, and Class-3 (strategic) which requires explicit operator + acting-head-of-board override.

**Empirical anchor** — a published paper, OSS project, or measurable benchmark that grounds a claim in the audit. Every audit claim that names a build-vs-contribute path should rest on at least one empirical anchor.

**Evidence Bundle** — the cross-repo schema that ties intent-eval-core, audit-harness, j-rig, intent-rollout-gate together. Defined normatively in Blueprint B § 7 (`gate-result/v1`). An Evidence Bundle is the signed, attested envelope carrying one or more `gate-result/v1` records plus their provenance.

**FM-level** — foundation-model-level work, i.e., concerns relating to the training, weights, internal representations, or capability shape of the LLM itself (not its runtime usage or composition). The four parked personal-skill pillar areas (#13-16) are FM-level. IEP is explicitly an infrastructure-layer project, not an FM-layer project.

**`gate-result/v1`** — the normative kernel schema (Blueprint B § 7) carrying the outcome of one verification gate. Fields include `outcome` (pass/fail/waive), `verifier_identity`, `attestation_envelope`, `evidence_pointers`, and (proposed extensions) `independence_class`, `cot_faithfulness`, `memory_integrity_class`, `replay_fidelity_level`, `inference_compute`, `routing_decision`. Every IEP component that performs verification emits `gate-result/v1`-shaped artifacts.

**Independence class** — proposed (Area #6, `iaj-E11`) enum capturing how independent a verifier is from the generator being verified. Five levels: `same-prompt`, `different-prompt-same-model`, `different-model-same-family`, `different-family`, `non-llm-rule`. Used in `gate-result/v1` to make verification claims more defensible.

**Non-OSS-equivalent** — audit shorthand for an area where existing open-source projects do not provide the capability we'd build (Areas #4, #11, #19, #21 per § 4.5.3). These are the strongest "build now" candidates because there is no upstream alternative.

**OTel SIG** — OpenTelemetry GenAI Special Interest Group, the governance body driving the agent-related semantic conventions extending OpenTelemetry's distributed-tracing standards. Hosted by CNCF, Apache 2.0, active May 2026 in "Development" status.

**P0 / P1 / P2** — priority levels in beads. P0 = critical (current sprint); P1 = important (next 1-2 sprints); P2 = deferred (placeholder / future). Phase B P0 recommended ranking is in § 11 with detail in Appendix G.

**Personal-skill pillar** — single OPS bead (`ops-personal-pillar-2026-05`) at `~/.beads/` tracking foundation-model-level research as operator development. NOT an IEP epic; never spawns sub-beads under platform prefixes. Quarterly re-evaluated.

**Phase A / B / C** — Phase A is foundation-lock (complete 2026-05-15: Blueprints A/B/C + Canonical Glossary + DR-010 widened-scope lock + `@intentsolutions/core@0.1.0` published). Phase B is construction sprint adopting this audit's findings post-ISEDC-Session-5. Phase C is anything past Phase B that's not yet scoped.

**Replay fidelity (RF-0..RF-4)** — proposed taxonomy under iel-E11. RF-0 = log-only no replay; RF-1 = action-replay; RF-2 = semantic-state replay with tool-call mocking; RF-3 = full deterministic replay with provider-pinning; RF-4 = cross-model counterfactual replay. Used to characterize what level of replay an Evidence Bundle supports.

**SessionTrace** — first-class kernel entity in Blueprint B § 4. The aggregated record of one agent run carrying events, reasoning steps, tool calls, observations, errors. Composes from `agent-loop-trace/v1` events.

**Tier-1 / Tier-2** — IEP project classification. Tier-1 = composes via Evidence Bundle schema (the 5 repos in this umbrella). Tier-2 = methodology-only oversight by intent-eval-lab; lives as sibling project elsewhere (e.g., semantic-flux). Distinction matters because tier-2 work isn't beaded under iec-/iel-/iah-/iaj-/iar- prefixes.

**Verifier** — proposed first-class kernel entity (Area #6, `iaj-E11`). The component performing verification, distinct from the generator being verified. Carries `independence_class` and `verifier_identity` metadata in `gate-result/v1`.

**Work-block** — unit of operator focused-attention. Approximately 2-4 hours of uninterrupted work. Used to estimate Phase B effort (§ 7, Appendix G). Not a calendar metric; not a sprint metric. Operator-bandwidth-relative.

---

## Closing

This document discharges Phase 4.5 of the Iterative Snacking Walrus program. The shared bibliography, the ecosystem landscape, and the per-area treatment together constitute the empirical foundation for ISEDC Session 5 and the Phase B Framing Memo. Whatever Phase B priority ordering emerges from the council, this audit is the work that grounds the decision.

### What this document is not

It is not a Phase B plan. It is not an implementation guide. It is not a commitment register. It is not a competitive analysis, market positioning document, or go-to-market plan. It is a craft-and-contribution audit — the substrate the operator and council use to decide what to build, what to contribute upstream, and what to skip.

The Phase B plan emerges from this document plus the five team lit reviews plus the ISEDC Session 5 ratification. None of those exists yet. This audit is the necessary first step, not the work itself.

### What the audit asks the reader to do

Three things, in order:

First, **trust but verify** the empirical claims. Every paper citation is reproducible via Semantic Scholar paperID; every OSS landscape claim is reproducible via WebFetch with the URL in the competitive-intel companion. If any specific claim doesn't survive verification, surface it; one inaccuracy can compound into many.

Second, **disagree productively** with the synthesis (§ 4.5, § 11). The cross-cutting findings and the P0 ranking are the operator's first-cut judgment. An ISEDC seat that disagrees — particularly on what earns kernel-status (§ 4.5.7) or whether the "no-OSS-equivalent" framing oversells uniqueness (§ 4.5.3) — should put that disagreement on the record at Session 5. The point of the seven-seat adversarial council is to surface what the operator missed.

Third, **decide explicitly** which Phase B P0 epics ship. The audit recommends six (§ 11 + Appendix G); operator bandwidth realistically supports four to six. The dropdown in Appendix G.7 names which retentions are highest-priority if scope must narrow. The council should ratify or revise.

### What happens after Session 5

Per § 9: bead creation, three-layer mirror, master-plan version bump, Plane LAB-6 update. The post-session work is mechanical given a ratified ranking. The pre-session work — this audit — is the substantive part.

Bandwidth, not customer-signal, gates what ships next. The platform's posture is craft + contribution. The 21 areas are the surface. The operator decides the order.

— end of findings —

Filed under Doc Filing Standard v4.3 as `000-DR-FIND-iep-phase-b-gap-analysis-and-research-framework-2026-05-20.md` at `intent-eval-platform/intent-eval-lab/research/`. Sources verifiable via Semantic Scholar paperIDs (companion biblio file at `000-RR-BIBL-shared-bibliography-2026-05-20.md`) and WebFetch URLs (companion competitive-intel file at `000-RR-COMP-ecosystem-landscape-2026-05-20.md`). No partner-name violations. No `labs.intentsolutions.io` predicate-URI references. Tracked under bd `bd_000-projects-ppt2`.
