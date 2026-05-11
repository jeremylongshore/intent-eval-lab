# Intent Eval Lab — Master Reading List

> Consolidated literature survey + competitive landscape for the Intent Eval Lab methodology.
> Every link below renders clickable in the GitHub UI. This file is the canonical "literature surveys, paper notes, competitive landscape" landing per the [repo README](../README.md) structural framing.

**Compiled:** 2026-05-10 · Sources: four landscape docs from Part 2 research workstreams (Workstream A audit-harness · Workstream B j-rig multi-provider · Workstream C MCP testing bridge · Workstream D synthesis) — see [§ Source landscape docs](#source-landscape-docs) at end.

**Counts:** 7 reviewed academic papers (Workstream A) + 5 reviewed papers (Workstream C) + 9 vendor canonical specs (Workstream B) + ~120 supporting primary sources across 14 categories.

---

## Table of contents

1. [Top reviewed academic papers](#1-top-reviewed-academic-papers)
2. [MCP specification + tooling](#2-mcp-specification--tooling)
3. [OpenTelemetry — semantic conventions + GenAI SIG](#3-opentelemetry--semantic-conventions--genai-sig)
4. [Per-vendor agentic CLI canonical specs](#4-per-vendor-agentic-cli-canonical-specs)
5. [Open standards (AgentSkills.io · AGENTS.md · MCP)](#5-open-standards)
6. [Distributed tracing foundations](#6-distributed-tracing-foundations)
7. [Property-based + stateful testing](#7-property-based--stateful-testing)
8. [Distributed-systems consistency testing](#8-distributed-systems-consistency-testing)
9. [Agent evaluation methodology](#9-agent-evaluation-methodology)
10. [Attestation + supply-chain provenance](#10-attestation--supply-chain-provenance)
11. [Consumer-driven contract testing + BDD](#11-consumer-driven-contract-testing--bdd)
12. [Mutation testing](#12-mutation-testing)
13. [AI test review + LLM evaluation](#13-ai-test-review--llm-evaluation)
14. [Static analysis + quality-gate prior art](#14-static-analysis--quality-gate-prior-art)
15. [CRAP metric origin](#15-crap-metric-origin)
16. [Source landscape docs](#source-landscape-docs)

---

## 1. Top reviewed academic papers

These twelve papers were reviewed in detail (via the `academic-research:paper-reviewing` Claude skill + Semantic Scholar MCP retrieval) and directly anchor design decisions in the Intent Eval Lab methodology.

### Agent evaluation + LLM-system observability (Workstream C, 5 papers)

- [**GAIA: A Benchmark for General AI Assistants**](https://arxiv.org/abs/2311.12983) — Mialon et al., ICLR 2024 · 716 citations
  Outcome-only evaluation benchmark (466 questions). Diagnostic: GAIA cannot distinguish *right answer for wrong reason* from *right answer through correct protocol-level sequence*. The Intentional Mapping sits one level below GAIA — complementary, not competitive.

- [**Survey on Evaluation of LLM-based Agents**](https://arxiv.org/abs/2503.16416) — Yehudai et al., 2025 · 141 citations
  First comprehensive survey of LLM-agent evaluation methods. Names three critical gaps: *cost-efficiency*, *safety*, *robustness*. Diagnostic: the survey is conducted entirely at the outcome-evaluation layer; protocol-level conformance is not a recognized perspective. Intent Eval Lab fills that gap.

- [**Elle: Finding Isolation Violations in Real-World Databases**](https://doi.org/10.1145/3465084.3467483) — Kingsbury, ACM PODC 2021
  Companion paper to the Jepsen distributed-testing library. Linear-time history checker detecting Adya-formalism transactional anomalies. **Highest-leverage borrowable pattern this landscape identifies** — the nemesis-generator-checker model applied to OTel traces is the most direct prior art for the Intentional Mapping conformance harness.

- [**Willful Disobedience: Automatically Detecting Failures in Agentic Traces (AgentPex)**](https://arxiv.org/abs/2603.23806) — Sharma, Barke, Zorn 2026 · 2 citations
  First paper to operationalize *the trace itself is an evaluable target*. Evaluates 424 traces from τ2-bench. AgentPex extracts rules from prompts; the Intentional Mapping declares rules from failure-shape categories independent of any prompt. Deeply complementary.

- [**Property-Based Testing in Practice**](https://doi.org/10.1145/3597503.3639581) — Goldstein et al., ICSE 2024 · 27 citations
  Qualitative study of PBT users at Jane Street. Finds that industrial PBT collapses to a small number of high-leverage idioms — structurally identical to the Intentional Mapping's MM-1..MM-6 collapse.

### Test-quality + supply-chain attestation (Workstream A, 7 papers)

- [**An Analysis and Survey of the Development of Mutation Testing**](https://www.semanticscholar.org/paper/d7c38286734419b52de4262c9802ebdfcf4b9447) — Jia & Harman, IEEE TSE · 1,818 citations
  Foundational survey establishing mutation-score as the gold-standard test-quality metric beyond line coverage. Cited by every modern mutation tool. Justifies the audit-harness "kill-rate ≥ 70%" wall above coverage-only gates.

- [**Mutation Testing in Practice: Insights From Open-Source Software Developers**](https://www.semanticscholar.org/paper/dd96541648125a3eab01f2bdc5e80d24f10de6ec) — Sánchez, Parejo, Segura, Durán, Papadakis, IEEE TSE 2024
  Survey of 104 OSS contributors. Key finding: **performance is the dominant barrier**, not adoption willingness. Implication: any mutation gate must run in CI on changed-code-only mode.

- [**An Empirical Study on Automatically Detecting AI-Generated Source Code: How Far Are We?**](https://www.semanticscholar.org/paper/e41ceafe77d394b650430ff144cd87811fcc27f4) — Suh, Tafreshipour, Li, Bhattiprolu, Ahmed, ICSE 2025 · 20 citations
  Best AI-code classifier reaches F1 82.55; existing detectors generalize poorly. Implication: "is this test AI-generated?" cannot be a single deterministic check — the audit-harness escape-scan REFUSE/CHALLENGE/FLAG grammar is more honest than binary detection.

- [**Benchmarking and Studying the LLM-based Code Review (SWRBench)**](https://www.semanticscholar.org/paper/ba3c99d34d03c47b99f07f30e65b7b599b20b243) — Zeng et al. · 8 citations · also at [arXiv:2509.01494](https://arxiv.org/abs/2509.01494)
  1,000-PR benchmark for AI code reviewers. **Multi-reviewer aggregation boosts F1 by up to 43.67%**. Direct argument for the j-rig "binary eval" pattern — aggregate multiple gate verdicts into one evidence row, not one verdict.

- [**Software Supply Chain Attribute Integrity (SCAI)**](https://www.semanticscholar.org/paper/2415020c4faaa61c9f78607f12299781690a8c25) — Melara · also at [arXiv:2210.05813](https://arxiv.org/abs/2210.05813)
  Defines a data format for *functional attribute + integrity information* of software artifacts. SCAI is registered as an in-toto predicate type. Direct precedent for "test-gate result" as an in-toto predicate.

- [**Agentic AI for Autonomous Defense in Software Supply Chain Security**](https://www.semanticscholar.org/paper/7ef12e7f28b538a044f3b2c2af4160446723a200) — Syed et al., Int. Conf. Computing Advancements 2025
  Frames SLSA + SBOM + in-toto as **necessary but insufficient** — they prove what was built but not what's safe to merge. The Evidence Bundle plays the same role for *test quality* that SCAI plays for *binary integrity*.

- [**Advanced Mutation Testing with Zero and Few-Shot Evaluation Using GPT-V4**](https://www.semanticscholar.org/paper/eaac22fe50ba4fa2dd93224892963890f7f0d649) — Hemmat et al., IoT 2025
  LLM-driven mutation generation as a new branch of the field. Forward-looking flag: in 12-24 months the harness's mutation layer will likely dispatch an LLM-mutation step alongside Stryker/PIT.

---

## 2. MCP specification + tooling

- [MCP specification (canonical)](https://modelcontextprotocol.io/specification)
- [MCP specification GitHub](https://github.com/modelcontextprotocol/specification)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) — official Anthropic-maintained debug tool
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [mcp-validator](https://github.com/Janix-ai/mcp-validator) — AGPL-3.0; protocol conformance for spec versions 2024-11-05 / 2025-03-26 / 2025-06-18
- [mcp-server-tester (steviec)](https://github.com/steviec/mcp-server-tester) — MIT; YAML-defined tests in tools / evals / compliance modes
- [mcp-server-tester (gleanwork)](https://github.com/gleanwork/mcp-server-tester) — MIT; Playwright + Zod schemas + LLM-as-judge for tool-discoverability
- [mcptap](https://github.com/mcptap/mcptap) — Vitest extension with MCP-specific matchers

---

## 3. OpenTelemetry — semantic conventions + GenAI SIG

- [OTel SIG-GenAI charter](https://github.com/open-telemetry/community/blob/main/projects/gen-ai.md) — explicitly lists agent-level conventions as long-term with no current roadmap target
- [OTel GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai)
- [OTel GenAI dedicated repo](https://github.com/open-telemetry/semantic-conventions-genai)
- [OTel LLM-observability blog](https://opentelemetry.io/blog/2024/llm-observability/)
- [OTel Collector](https://github.com/open-telemetry/opentelemetry-collector)
- [OpenLLMetry / Traceloop](https://github.com/traceloop/openllmetry) — OTel SDK for LLMs across providers

---

## 4. Per-vendor agentic CLI canonical specs

The 9 agentic-CLI runtimes that j-rig multi-provider work surveyed. Each maintains its own canonical spec for skills / plugins / hooks / MCP integration.

### Anthropic

- [Claude Code skills spec](https://code.claude.com/docs/en/skills)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code MCP integration](https://code.claude.com/docs/en/mcp)
- [Anthropic Agent Skills (SDK)](https://docs.anthropic.com/en/api/agent-skills)

### OpenAI

- [OpenAI Codex CLI](https://github.com/openai/codex) — Apache-2.0 · Rust 96%
- [OpenAI function-calling guide](https://platform.openai.com/docs/guides/function-calling)

### Google

- [Google Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [Gemini API docs](https://ai.google.dev/gemini-api/docs)

### Cursor

- [Cursor docs (canonical post-2026 redirect from `docs.cursor.com`)](https://cursor.com/docs)
- [Cursor context rules](https://docs.cursor.com/context/rules)
- [Cursor MCP integration](https://docs.cursor.com/context/model-context-protocol)

### Windsurf (Codeium)

- [Windsurf Cascade rules / memories](https://docs.windsurf.com/windsurf/cascade/memories)
- [Codeium broader ecosystem](https://github.com/Exafunction/codeium.vim)

### GitHub Copilot

- [Copilot CLI legacy (`gh copilot`)](https://github.com/github/gh-copilot) — **archived 2025-10-30**; successor "Copilot Coding Agent" has no public CLI spec yet
- [Copilot Extensions concept](https://docs.github.com/en/copilot/concepts/about-extensions)

### Continue.dev

- [Continue.dev source](https://github.com/continuedev/continue) — Apache-2.0 · 21,498+ commits
- [Continue.dev docs](https://docs.continue.dev/)

### Aider

- [Aider](https://aider.chat/)
- [Aider source](https://github.com/Aider-AI/aider) — Apache-2.0
- [**Aider multi-provider eval leaderboard**](https://aider.chat/docs/leaderboards/) — already-working multi-provider eval; polyglot benchmark = 225 Exercism exercises × 6 languages (C++, Go, Java, JS, Python, Rust). **Direct template for j-rig per-vendor reporting.**

### Cline

- [Cline](https://github.com/cline/cline) — Apache-2.0 © 2026

---

## 5. Open standards

- [AgentSkills.io specification](https://agentskills.io/specification) — open spec Claude Code follows
- [AGENTS.md](https://agents.md/) — cross-tool plugin convention (recognized by ~20 vendors per the harness count analysis)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification) — canonical (also listed in § 2)

---

## 6. Distributed tracing foundations

- [**Dapper: A Large-Scale Distributed Systems Tracing Infrastructure**](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/) — Sigelman et al., Google 2010 — foundational
- [Honeycomb Refinery](https://github.com/honeycombio/refinery) — Apache 2.0; trace sampling + correlation; relevant for filtering Intentional Mapping-relevant signals
- [Grafana Tempo + TraceQL](https://github.com/grafana/tempo) — AGPL; distributed trace store; alternative collector backend

---

## 7. Property-based + stateful testing

- [**QuickCheck**](https://doi.org/10.1145/351240.351266) — Claessen & Hughes 2000 — foundational PBT paper
- [Hypothesis](https://github.com/HypothesisWorks/hypothesis) — MPL 2.0; property-based test framework with stateful + shrinking; **MM-1..MM-6 shapes ARE properties — Hypothesis is the canonical impl pattern**
- [**Property-Based Testing in Practice**](https://doi.org/10.1145/3597503.3639581) — Goldstein et al., ICSE 2024 (also reviewed in § 1)
- [**Empirical Evaluation of Property-Based Testing in Python**](https://doi.org/10.1145/3764068) — Ravi & Coblenz 2025

---

## 8. Distributed-systems consistency testing

- [Jepsen](https://github.com/jepsen-io/jepsen) — Eclipse Public License; Kyle Kingsbury's distributed-systems testing methodology — the gold standard for finding async races
- [**Elle paper**](https://doi.org/10.1145/3465084.3467483) — Kingsbury, ACM PODC 2021 (also reviewed in § 1)

---

## 9. Agent evaluation methodology

(See § 1 for the 5 fully reviewed papers. Additional sources worth following:)

- [ReliabilityBench (Gupta 2026)](https://arxiv.org/abs/2601.06112)
- [AgentSight: Trace-based runtime observability (Zheng et al., PACMI@SOSP 2025)](https://arxiv.org/abs/2508.02736)

---

## 10. Attestation + supply-chain provenance

- [in-toto framework](https://in-toto.io/) — CNCF graduated
- [in-toto attestation spec](https://github.com/in-toto/attestation) — Apache 2.0
- [in-toto Statement v1 spec](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) — Evidence Bundle envelope candidate
- [SLSA v1.0 provenance](https://slsa.dev/spec/v1.0/provenance)
- [Sigstore docs](https://docs.sigstore.dev/)
- [Cosign overview](https://docs.sigstore.dev/cosign/signing/overview/)
- [Rekor transparency log](https://docs.sigstore.dev/logging/overview/)
- [DSSE (Dead Simple Signing Envelope)](https://github.com/secure-systems-lab/dsse)
- [GUAC](https://github.com/guacsec/guac) — Apache 2.0; graph supply-chain metadata
- [OpenSSF Scorecard](https://github.com/ossf/scorecard) — Apache 2.0
- [Scorecard checks reference](https://github.com/ossf/scorecard/blob/main/docs/checks.md)

---

## 11. Consumer-driven contract testing + BDD

- [Pact specification](https://github.com/pact-foundation/pact-specification) — MIT; consumer-driven-contract pattern → MCP plugin/host conformance
- [Cucumber / Gherkin](https://github.com/cucumber) — MIT; BDD step-definition pattern → Intentional Mapping step-definition format

---

## 12. Mutation testing

- [PIT mutation testing (Java)](https://pitest.org/) — Apache 2.0; foundational
- [Stryker (JS/TS/.NET/Scala)](https://stryker-mutator.io/) — Apache 2.0; mutation testing config + CI report format
- [mutmut (Python)](https://github.com/boxed/mutmut)
- [cargo-mutants (Rust)](https://github.com/sourcefrog/cargo-mutants)
- [Jia & Harman mutation-testing survey](https://www.semanticscholar.org/paper/d7c38286734419b52de4262c9802ebdfcf4b9447) (also reviewed in § 1)
- [Sánchez et al. OSS practitioner survey](https://www.semanticscholar.org/paper/dd96541648125a3eab01f2bdc5e80d24f10de6ec) (also reviewed in § 1)

---

## 13. AI test review + LLM evaluation

- [SWRBench (Zeng et al.)](https://arxiv.org/abs/2509.01494) — 1,000-PR benchmark for AI code reviewers (also reviewed in § 1)
- [CWEval (Peng et al.)](https://arxiv.org/abs/2501.08200) — security-quality evaluation
- [AI-code detection (Suh et al., ICSE 2025)](https://www.semanticscholar.org/paper/e41ceafe77d394b650430ff144cd87811fcc27f4) (also reviewed in § 1)
- [AVID — AI Vulnerability Database](https://avidml.org/) — AI vulnerability disclosure; pattern reference for failure-shape catalogs
- [CodeRabbit](https://github.com/coderabbitai) — Mixed license; AI-review automation patterns
- [Qodo PR-Agent](https://github.com/Qodo-AI/pr-agent) — Apache 2.0; AI-generated test suggestion
- [Greptile](https://www.greptile.com/) — Closed source; read-only concepts
- [SemGrep](https://github.com/semgrep/semgrep) — LGPL; rule-based static analysis

---

## 14. Static analysis + quality-gate prior art

- [SonarQube quality gates](https://www.sonarsource.com/products/sonarqube/) — named-gate-bundle pattern
- [Semgrep](https://semgrep.dev/) — rule-based static analysis

### Multi-provider abstraction libraries (Workstream B)

- [LiteLLM](https://github.com/BerriAI/litellm) — MIT; **canonical "one interface, N providers" library** — direct ModelTarget enum replacement source
- [Vercel AI SDK](https://github.com/vercel/ai) — Apache 2.0; cleanest TypeScript provider abstraction
- [LangChain](https://github.com/langchain-ai/langchain) — MIT; older but battle-tested provider abstraction

---

## 15. CRAP metric origin

The CRAP metric is industry-original (never had a peer-reviewed primary citation):

- [Alberto Savoia, "Will your tests destroy your code?"](https://www.artima.com/weblogs/viewpost.jsp?thread=210575) — Crap4j origin column (2007). Formula `C² × (1 - cov)³ + C` where `cov` is the coverage fraction (0.0 ≤ cov ≤ 1.0). The metric has never had a peer-reviewed primary citation — worth flagging when defending the gate to academic reviewers.

---

## Source landscape docs

The four Part 2 research workstream landscape docs from which this Master Reading List was consolidated:

| Workstream | Landscape doc | Size | URLs cited |
|---|---|---|---|
| **A** — audit-harness upgrade landscape | [`audit-harness/000-docs/002-RR-LAND-upgrade-landscape.md`](https://github.com/jeremylongshore/audit-harness/blob/main/000-docs/002-RR-LAND-upgrade-landscape.md) | 3,591w · 272 lines | 56 |
| **B** — j-rig multi-provider spec matrix | [`j-rig-binary-eval/000-docs/018-RR-LAND-multi-provider-spec-matrix.md`](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/main/000-docs/018-RR-LAND-multi-provider-spec-matrix.md) | 5,990w · 508 lines | 32 |
| **C** — MCP testing bridge | [`intent-eval-lab/000-docs/002-RR-LAND-mcp-testing-bridge.md`](../000-docs/002-RR-LAND-mcp-testing-bridge.md) | 6,386w · 461 lines | 75 |
| **D** — Phase B scope synthesis | [`intent-eval-lab/000-docs/003-PP-PLAN-phase-b-scope-refinement.md`](../000-docs/003-PP-PLAN-phase-b-scope-refinement.md) | 6,151w · 447 lines | 14 |

For the full context behind each citation, click through to the source landscape doc — each URL above appears in context within one of the four docs.

---

## Maintenance

When a new research source surfaces during Intent Eval Lab work, add it here under the appropriate category. When a source becomes load-bearing for a published artifact, also cite it in the relevant `specs/` or `000-docs/` artifact. This file is the *canonical reading list*; landscape docs are the *contextual citation*.

Compiled and committed 2026-05-10 per user direction *"i need to be able to go into the repo ui and click the links."*
