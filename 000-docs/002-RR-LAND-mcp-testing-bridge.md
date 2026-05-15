# Bridging Static Repo Analysis to Protocol-Level Runtime Conformance Testing

> **Document type:** RR-LAND (Research Report — Landscape Mapping) per Document Filing Standard v4.3
> **Date:** 2026-05-10
> **Status:** Draft v1.0 — Part 2 research deliverable (Workstream C)
> **Author:** Intent Solutions LLC — `jeremy@intentsolutions.io`
> **Workstream:** Part 2 of three-repo convergence (Workstream C: Bridge-Gap Landscape)
> **Master plan:** `~/.claude/plans/please-take-your-time-glimmering-stardust.md` § Part 2
> **Sibling workstreams:** A (Spec-anchored OTel Phase B handoff), B (Vendor-neutral conformance harness design)

---

## 1. Mission and scope

### 1.1 The gap this document maps

The three-repo convergence (`intent-eval-lab` + `audit-harness` + `j-rig-skill-binary-eval`) currently spans two of the three rungs of evaluation. The two existing rungs are:

1. **Static repo analysis** — `audit-harness` performs hash-pinning, CRAP-score computation, architecture inspection, escape-scan, Gherkin lint, and bias detection against a repo *at rest*. It inspects files; it does not exercise behavior at runtime.
2. **Behavioral skill evaluation** — `j-rig-skill-binary-eval` runs deterministic prompts against a deployed skill or plugin and grades the outcome with an LLM-as-judge or rule-based oracle. It exercises behavior; it does not observe the protocol-level signals that explain *why* a behavior emerged.

A third rung is missing and that is what this document maps:

3. **Protocol-level runtime conformance testing** — given a deployed MCP plugin and an executing agent harness emitting OpenTelemetry signals, assert that the plugin satisfies its declared conformance properties *across* an OTel signal stream that crosses async boundaries, hook executions, server cooldowns, and read-after-write barriers.

The first two rungs are well-developed in the engineering community. The third rung is the live frontier where most production reliability bugs in agent plugins emerge. This landscape document maps the academic prior art, protocol-conformance prior art in adjacent ecosystems, and the OSS tooling that the bridge can borrow from — and identifies the concrete gap that the Intentional Mapping methodology (introduced in `intent-eval-lab/specs/mcp-plugin-observability/`) fills.

### 1.2 Not in scope

This document is a *landscape map*, not an implementation plan. It does not:

- Stand up an OTel collector or specify collector configuration
- Author conformance tests against any specific MCP plugin
- Propose a new academic publication
- Make any vendor-specific claim about a partner-engagement plugin
- Make measurement claims about plugins not yet measured

Implementation belongs to Phase B (handoff RFC) and Phase C (executable harness) — see § 11 for the split.

---

## 2. Empirical anchor — the Intentional Mapping methodology in the public spec

This landscape is grounded in the methodology described in `intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/`. The anchoring claim of that spec, restated abstractly, is:

> An MCP plugin is **operationally observable** when a third party (a regression suite, a partner, an auditor) can assert on the plugin's protocol-level behavior using the standard signal stream emitted by the agent harness, without modifying the plugin's MCP server.

The spec codifies five normative requirements (R1 tool-call observability, R2 hook-firing observability, R3 transport observability, R4 vendor-neutral test harness, R5 documented Intentional Mapping) and one templated artifact, the **Intentional Mapping** — a vendor-neutral three-column table that maps each abstract failure-shape to the hook matcher that addresses it and the OTel signal that proves the matcher fired.

Six vendor-neutral failure-shape categories are defined in `intentional-mapping-template.md`:

| ID | Failure-shape (vendor-neutral) | Plain-language gloss |
|---|---|---|
| **MM-1** | Asynchronous write returns success but read-after-write sees stale state | Race condition between async completion and dependent read |
| **MM-2** | Read-side response shape drifts across consecutive calls | List-shape vs detail-shape inconsistency, paginated drift, schema variance |
| **MM-3** | Operation requires a cooldown / debouncing window before next equivalent operation | Rate-limiting, debounce, anti-flood |
| **MM-4** | Operation requires verification of side-effect completion before downstream reliance | Poll-until-verified, propagation-aware waits |
| **MM-5** | Tool inputs need mandatory context the model isn't reliably providing | Caller identity, intent string, policy tag injection |
| **MM-6** | Server-side endpoint requires strict-mode protocol compliance the model's default input doesn't enforce | W3C-strict / RFC-strict payload reformatting |

These six categories are vendor-neutral by construction — they describe *shapes* of failure mode, not bugs in any specific plugin. They are the lens through which the rest of this landscape is interpreted: every academic finding, every adjacent-ecosystem pattern, and every OSS tool surveyed below is assessed for what it offers toward observing one or more of MM-1 through MM-6.

---

## 3. Academic state of the art

### 3.1 Foundations — distributed tracing and property-based testing

Two foundational papers anchor the prior art the bridge must build on:

**[Sigelman et al. 2010] *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure***
*Google Technical Report; 709 citations; <https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/>*

**Claims:** Trace-context propagation across asynchronous service boundaries can be done with sub-1% overhead via sampling, application-level instrumentation libraries, and a small central collector. The trace-id / span-id / parent-span-id triple is sufficient to reconstruct causality across thousands of services without any synchronous coordination.

**Methodology:** Light-weight instrumentation injected at common abstractions (RPC, thread-pool, control-flow); offline trace analysis on sampled records.

**Applicability to MCP-plugin testing bridge:** Dapper's primitives — trace context propagated through asynchronous boundaries — are *the foundational mechanism* that makes MM-1 (async race) and MM-4 (state verification) observable at all. Without them, there is no way to correlate the `PreToolUse` hook span with the downstream `tool_decision` event with the eventual `tool_result` event when those events are produced minutes apart by different async paths. OpenTelemetry inherits this model directly. The `claude_code.hook` span / `claude_code.tool` span / `claude_code.tool_result` event triple in Claude Code's telemetry surface is a domain-specific instantiation of Sigelman's general primitive.

**[Claessen & Hughes 2000] *QuickCheck: a lightweight tool for random testing of Haskell programs***
*ACM SIGPLAN ICFP; 1,306 citations; <https://doi.org/10.1145/351240.351266>*

**Claims:** Tests should be specified as *properties* (universally quantified predicates over input domains) rather than as concrete input/output pairs; random generators sample the input space; failures shrink to minimal counterexamples; stateful systems are modeled as state machines on which sequences of operations are generated and the post-condition is checked against an abstract model.

**Methodology:** Type-class-driven random generation; stateful command-sequence generation via a state-machine spec; integrated shrinking.

**Applicability:** This is the foundational pattern for testing stateful protocols. The Intentional Mapping's six categories (MM-1..MM-6) are property classes; a conformance harness implementing them in QuickCheck-style — generating tool-call sequences, running them against the plugin via `claude -p`, observing the OTel stream, and asserting properties such as "no `tool_decision` for a downstream read tool fires before the upstream `confirm` tool's side-effect has been verified" — is a direct generalization of QuickCheck's stateful model to the agent-protocol domain. The shrinking primitive is high-value because failed conformance runs from real agent traces are huge; producing a minimal failing trace is exactly what an operator needs.

### 3.2 Recent state of the art — top reviewed papers

**Citation block 1 — [Mialon et al. 2024] *GAIA: A Benchmark for General AI Assistants***
*ICLR 2024 / arXiv:2311.12983; 716 citations; <https://arxiv.org/abs/2311.12983>*

**Summary:** GAIA introduces 466 real-world questions requiring multi-step reasoning, multimodality, and tool-use proficiency. The benchmark scores human respondents at 92% vs GPT-4-with-plugins at 15%, deliberately inverting the trend of benchmarks-harder-for-humans.

**Methodology:** Outcome-only evaluation — judged on final-answer correctness against a hidden answer key. The 466 questions exercise multi-tool workflows (web browsing, document reading, code interpretation) sequenced over many steps.

**Reviewed strengths:** First widely adopted benchmark that takes real-world tool-use sequencing seriously. The "fundamental abilities" framing — reasoning + multimodality + web + tool-use — maps directly onto what an MCP plugin in production has to perform.

**Reviewed weaknesses (relevant to this landscape):** Outcome-only. GAIA cannot distinguish a plugin that produces the right answer for the wrong reason (e.g., the agent guessed the tool didn't actually need to fire) from a plugin that produces the right answer through a correct protocol-level sequence. GAIA has no concept of OTel signals, no hook observability, no notion of an MM-3 cooldown violation that the agent papered over.

**Applicability to Intentional Mapping methodology:** GAIA sits one level above the Intentional Mapping. Where GAIA asks *did the system get the right answer?*, the Intentional Mapping asks *did the protocol-level mechanism that produces correct answers fire correctly?* They are complementary, not competitive. A plugin can pass MM-1..MM-6 conformance and still fail GAIA (the agent reasoning over the tool's correct output may still be wrong); a plugin can pass GAIA on a single try and still fail MM-3 cooldown conformance under load.

---

**Citation block 2 — [Yehudai et al. 2025] *Survey on Evaluation of LLM-based Agents***
*arXiv 2503.16416; 141 citations; <https://arxiv.org/abs/2503.16416>*

**Summary:** First comprehensive survey of LLM-agent evaluation methods, organized across five perspectives: (1) core LLM capabilities (planning, tool use), (2) application-specific benchmarks (web, SWE agents), (3) generalist-agent evaluation, (4) dimensions of agent benchmarks, (5) frameworks and tools for developers.

**Methodology:** Taxonomic survey; cross-paper synthesis; explicit gap-naming.

**Reviewed strengths:** Maps the SOTA cleanly. Identifies the three critical gaps the field has not addressed: *cost-efficiency* evaluation, *safety* evaluation, *robustness* evaluation. Explicitly notes that evaluation methods are shifting toward "more realistic, challenging evaluations with continuously updated benchmarks."

**Reviewed weaknesses (relevant to this landscape):** The survey is conducted entirely at the *outcome-evaluation* layer. It does not survey protocol-level conformance evaluation as a category. The word "OpenTelemetry" does not appear in the abstract; "trace correlation across async boundaries" is not a recognized perspective. This is itself diagnostic — the field has not yet recognized that the runtime signal stream is an evaluable target.

**Applicability:** The Intentional Mapping methodology fills the gap Yehudai et al. name without naming: a *robustness-evaluation* methodology that is grounded in the runtime signal stream rather than in outcome correctness. The survey's "frameworks and tools for agent developers" perspective is where a conformance-harness implementing MM-1..MM-6 would land if reframed as a publication.

---

**Citation block 3 — [Kingsbury 2021] *Elle: Finding Isolation Violations in Real-World Databases***
*ACM SIGACT-SIGOPS Principles of Distributed Computing 2021; <https://doi.org/10.1145/3465084.3467483>*

**Summary:** Companion paper to the Jepsen distributed-testing library. Elle is a linear-time history checker that detects every Adya-formalism transactional anomaly except predicates. By carefully choosing the datatypes and operations submitted to a database, Elle generates histories whose client-observable structure constrains the dependency graph of every possible Adya history the database could have executed.

**Methodology:** Property-based testing applied to distributed databases: a generator submits operations, a nemesis injects faults (network partitions, clock skew, process kills), and a checker (Elle) analyzes the resulting history for cycles in the Adya dependency graph that prove an isolation violation.

**Reviewed strengths:** Found consistency violations in 26 systems over 8 years across PostgreSQL, Dgraph, Redis-Raft, and many others. The history-checking model is robust precisely because it consumes only client-observable observations — exactly analogous to what an OTel signal stream provides for a plugin. Elle's automatic minimal-counterexample extraction is the same primitive QuickCheck introduced for stateful systems.

**Reviewed weaknesses (relevant to this landscape):** Elle's checker is database-specific (it formalizes transaction-isolation predicates). It does not, out of the box, accept OTel traces. Its dependency-graph machinery requires the input history to be typed in the database operational vocabulary (read, write, append, etc.), not the more open-ended vocabulary of MCP tool calls.

**Applicability to Intentional Mapping methodology:** Elle's *pattern* is directly applicable. Each of MM-1..MM-6 can be reformulated as a history property: MM-1 ("async write returns success but downstream read sees stale state") is structurally equivalent to a read-your-writes anomaly; MM-3 ("cooldown") is a rate-control invariant; MM-4 ("verification before reliance") is a happens-before invariant. The Jepsen nemesis-generator-checker pattern, with the OTel trace stream as the history-source, is the most concrete adoption candidate this landscape identifies. See § 9 borrowable pattern B-1.

---

**Citation block 4 — [Sharma, Barke, Zorn 2026] *Willful Disobedience: Automatically Detecting Failures in Agentic Traces (AgentPex)***
*arXiv 2603.23806; 2 citations; <https://arxiv.org/abs/2603.23806>*

**Summary:** AgentPex extracts behavioral rules from agent prompts and system instructions, then automatically evaluates execution traces for compliance with those specifications. Evaluated on 424 traces from τ2-bench across telecom, retail, and airline customer-service domains. Shows that outcome-only scoring misses procedural failures (incorrect workflow routing, unsafe tool usage, violations of prompt-specified rules) that AgentPex surfaces.

**Methodology:** Rule-extraction from prompts → trace-evaluation against extracted rules.

**Reviewed strengths:** First paper to operationalize the insight that *the trace itself is an evaluable target*, distinct from the outcome. The 424-trace study with model-by-domain breakdowns demonstrates real differentiation: prompt-rule violations are common, model-dependent, and invisible to outcome-only scoring.

**Reviewed weaknesses (relevant to this landscape):** Rules are extracted from *prompts*. This makes the methodology adaptive to whatever the operator wrote in the agent prompt, but it does not provide a vendor-neutral methodology for cases where the operator does not write prompts (e.g., a plugin reviewer asserting against a partner's plugin from the outside). It does not address protocol-level signals (OTel hook spans, transport events, server-side observability).

**Applicability:** AgentPex and the Intentional Mapping methodology are deeply complementary. AgentPex extracts rules from prompts; Intentional Mapping declares rules from *failure-shape categories* that are independent of any prompt. AgentPex evaluates traces of prompt-driven dialogues; Intentional Mapping evaluates OTel signal streams of any agent-driven interaction. Together they would form a stack: prompt-level rules (AgentPex layer) + protocol-level conformance (Intentional Mapping layer) + outcome-level correctness (GAIA / τ-bench layer).

---

**Citation block 5 — [Goldstein et al. 2024] *Property-Based Testing in Practice***
*ICSE 2024; 27 citations; <https://doi.org/10.1145/3597503.3639581>*

**Summary:** Empirical study of 30 in-depth interviews with experienced PBT users at Jane Street. Finds that PBT's main strengths are testing complex code and increasing confidence beyond what is available through conventional testing methodologies. Most uses fall into a relatively small number of high-leverage idioms; main weaknesses are the relative complexity of writing properties and the difficulty of evaluating their effectiveness.

**Methodology:** Qualitative, interview-driven; in-vivo industrial PBT usage study.

**Reviewed strengths:** Empirical grounding that PBT in industrial use generalizes to a small number of high-leverage patterns. This is structurally identical to the Intentional Mapping insight that finding-shape categories collapse to a small set (MM-1..MM-6).

**Reviewed weaknesses (relevant to this landscape):** Findings are restricted to Jane Street's domain (financial systems). The "difficulty of evaluating effectiveness" of property-based tests is a known open problem — and one that the Intentional Mapping's tight coupling to OTel signals helps address (a Intentional Mapping row is *evaluable* by asserting on the named signal, vs an abstract property whose effectiveness is opaque).

**Applicability:** Strong validation that the Intentional Mapping's collapse-to-N-categories pattern is the right shape. Goldstein et al. independently confirm that operators at scale converge on small idiom sets; the Intentional Mapping is the agent-protocol-specific version of that convergence.

### 3.3 Adjacent recent work worth following

Beyond the five top reviews, the literature search surfaced a frontier of recent work to track:

- **AgentSight (eBPF-based agent observability)** — [Zheng et al. 2025 PACMI@SOSP, arXiv 2508.02736] uses eBPF to monitor agents at the OS boundary, intercepting TLS-encrypted LLM traffic and correlating with kernel events. Out-of-band complementary methodology to OTel-from-the-agent.
- **ReliabilityBench (LLM agent reliability evaluation)** — [Gupta 2026, arXiv 2601.06112] introduces a chaos-engineering-style fault-injection framework for agents, measuring `pass^k` consistency, perturbation-robustness, and fault-tolerance. Closest to a Jepsen-for-agents in spirit.
- **Butterfly Effects in Toolchains** — [Xiong et al. EMNLP 2025] taxonomy of tool-agent parameter failures; useful prior art for the *kinds* of failures MM-1..MM-6 abstract over.
- **Proxy State-Based Evaluation** — [Chuang et al. 2026, arXiv 2602.16246] LLM-driven simulation framework that preserves final-state evaluation without a deterministic backend; relevant for cases where building a Jepsen-style deterministic backend is impractical.
- **Saving SWE-Bench (benchmark mutation)** — [Garg et al. 2025, arXiv 2510.08996] shows existing benchmarks overestimate agent capabilities by >50% over real-world chat-based queries. Cautionary for any "build a new benchmark" Phase-C direction.

---

## 4. Protocol prior art in adjacent ecosystems

The Intentional Mapping methodology is not the first attempt to make a protocol *conformance-testable* in a vendor-neutral way. Adjacent ecosystems have solved analogous problems, and their solutions inform Phase B / C scope.

### 4.1 in-toto attestation framework

The [in-toto project](https://github.com/in-toto/attestation) (CNCF-governed) provides a three-layer model for verifiable claims about software-production steps: **envelope** (the container) → **statement** (metadata about what's being attested) → **predicate** (domain-specific format for the use case). Common predicates include SLSA Provenance, Link (supply-chain-step detail), and VSA (Vulnerability Statement Attestation).

**Relevance to MCP-plugin testing bridge:** in-toto's predicate model is the right shape for *signed conformance reports*. An MCP-plugin Intentional Mapping conformance run produces an evidence bundle (an OTel trace, a per-row PASS/PARTIAL/FAIL determination, the spec version, plugin commit SHA). Wrapping this evidence bundle as an in-toto predicate would let an auditor verify the bundle's signature and schema before trusting the conformance claim. The Phase A OTel RFC (`001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` § 4 `agent.evidence_bundle.*` events) is partly built on this insight — but the framework borrowing is not yet codified into the Intentional Mapping conformance-report spec.

### 4.2 SLSA Provenance v1.0

[SLSA Provenance v1.0](https://slsa.dev/spec/v1.0/provenance) defines a structured format for build provenance: **BuildDefinition** (what was built, with external/internal parameter split) + **RunDetails** (execution environment + builder.id identifying the trusted build platform). License: Community Specification License 1.0.

**Relevance:** SLSA Provenance shows the right level of detail for an *attestation about a process that produced an artifact*. By analogy, a "Conformance Provenance" attestation could capture: Intentional Mapping version, plugin commit SHA, harness version, env-var gate set, collector configuration, signed OTel-bundle URI. The format is already standardized; a Conformance Provenance is a new predicate type, not a new format.

### 4.3 Pact consumer-driven contract testing

The [Pact specification](https://github.com/pact-foundation/pact-specification) (MIT) defines a contract-testing framework where the *consumer* writes the contract (a set of expected request/response interactions), generates a JSON pact file, and the *provider* independently verifies that its real responses match the contract. Pact follows Postel's Law: strict about what consumers send, lenient about what they accept.

**Relevance:** Pact's model maps cleanly onto MCP plugin/host conformance. A "consumer-driven MCP pact" would let an agent-harness (consumer) declare its expectations of a plugin's MCP server (provider) — e.g., "given a `confirmAppUpload` tool call, the response will have a non-null `appId` field that becomes queryable via `getApp` within 5 seconds" — and the plugin would verify its server satisfies the pact. This is a sibling methodology to the Intentional Mapping, complementary in scope: Pact covers schema-and-shape conformance; Intentional Mapping covers *sequence and timing* conformance. See § 9 borrowable pattern B-3.

### 4.4 gRPC conformance test suite

The [gRPC project](https://grpc.io) maintains language-cross-cutting conformance tests where each language SDK runs the same test scenarios against a reference server. The pattern: a *test driver* (language-agnostic) drives both a SUT-server and an oracle-server and asserts behavioral parity.

**Relevance:** This is the right shape for ensuring future MCP harnesses (Claude Code, Codex CLI, Gemini CLI, Copilot CLI, etc.) emit *equivalent* signals against the same plugin. The Phase A OTel RFC's goal of vendor-neutral semantic conventions is the precondition for a gRPC-style cross-harness conformance suite.

### 4.5 GraphQL contract testing patterns

GraphQL has a related pattern where schemas serve as contracts and tooling (Apollo Studio, GraphQL Inspector) detect breaking changes between schema versions. This is *schema drift* detection, structurally identical to MM-2 (response-shape drift).

**Relevance:** Lighter touch than Pact, but adoption of a "schema lint" tool against the MCP tool-input/output schemas would catch MM-2 violations before they emerge in production traces.

---

## 5. MCP tooling ecosystem scan

The MCP testing-tools ecosystem is approximately 18 months old (since the MCP spec went public 2024-11). It is moving fast and is largely community-driven. The table below catalogues what exists as of 2026-05.

| Project | License | Capability layer | Maturity | Borrowability | URL |
|---|---|---|---|---|---|
| **MCP Inspector** (official) | MIT | Interactive debug (web UI + CLI). Examines tools/resources/prompts; streams responses. | Active (Anthropic-maintained) | Useful as a *reference* of what an MCP client must do; not a conformance harness. | <https://github.com/modelcontextprotocol/inspector> |
| **MCP Specification** repo | MIT | TypeScript-first schema + JSON-Schema export. Versions: 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25. **No conformance test suite shipped with the spec.** | Active | The schema is the *input* to a conformance harness; the spec is the canonical reference for what to assert. | <https://github.com/modelcontextprotocol/specification> |
| **modelcontextprotocol/python-sdk** | MIT | Reference SDK with `/tests` directory; some pytest fixtures usable as test scaffolding. | Active | Source of testing primitives; not a conformance harness. | <https://github.com/modelcontextprotocol/python-sdk> |
| **modelcontextprotocol/typescript-sdk** | Apache 2.0 (new) / MIT (legacy) | Reference SDK; Vitest test harness; `examples/` directory with reference implementations. | Active | Source of testing primitives; not a conformance harness. | <https://github.com/modelcontextprotocol/typescript-sdk> |
| **Janix-ai/mcp-validator** | AGPL-3.0-or-later | Protocol conformance for spec versions 2024-11-05, 2025-03-26, 2025-06-18. Tests STDIO + HTTP transports, OAuth 2.1, JSON-RPC batching, structured tool output, elicitation. | 74 stars; active | High borrowability *for the schema/transport layer*. AGPL means code cannot be copied directly into an Apache 2.0 harness — but **subprocess/CLI execution (running the validator as a standalone tool from CI or via `subprocess.run()`) does NOT trigger copyleft on the calling harness**. Usable as a black-box conformance check. Direct vendoring of validator source remains license-incompatible. | <https://github.com/Janix-ai/mcp-validator> |
| **steviec/mcp-server-tester** | MIT | YAML-defined tests in three modes: `tools` (direct call, no LLM), `evals` (LLM integration), `compliance` (spec validation, WIP). Both runtime behavior and basic compliance. | 35 stars; active | High. YAML test format is reusable; the three-mode split (tools / evals / compliance) is exactly the bucketing a Intentional Mapping harness needs. | <https://github.com/steviec/mcp-server-tester> |
| **gleanwork/mcp-server-tester** | MIT | Playwright-based runtime tests + JSON eval datasets. Built-in matchers: text, regex, Zod schema, snapshot. Includes LLM-as-judge for "tool discoverability" assertions. | 15 stars; active | High. Tool-discoverability assertions are an unobvious test category that matters in production but isn't captured in Intentional Mapping yet — candidate MM-7. | <https://github.com/gleanwork/mcp-server-tester> |
| **mcptap/mcptap** | MIT | Vitest extension with MCP-specific matchers (`toListTool`, `toListTools`). Subprocess + in-process modes; stdio-safe logging; smart-mask snapshot testing. | 0 stars; new | High for the assertion-library layer. The Vitest extension model is the right shape for embedding Intentional Mapping assertions in a developer's existing test suite. | <https://github.com/mcptap/mcptap> |
| **mcp-use/mcp-conformance-action** | MIT | GitHub Action wrapping conformance test execution. | 4 stars; new | Useful as a CI-integration reference; not a harness on its own. | <https://github.com/mcp-use/mcp-conformance-action> |
| **Datasculptures/mcp-test-harness** | Not specified | Automated security + protocol conformance for spec 2025-11-25. | 0 stars; new | Low-medium — license unclear, low maturity. | <https://github.com/Datasculptures/mcp-test-harness> |

**Ecosystem assessment:** The existing MCP test tooling covers (a) schema/transport conformance well (mcp-validator), (b) tool-call functional testing well (steviec, gleanwork), (c) developer-facing assertion ergonomics well (mcptap). **It does not cover** runtime-behavior conformance across an OTel signal stream — none of the existing tools consume an OTel trace as a test input. This is the precise gap the Intentional Mapping methodology occupies.

---

## 6. Adjacent-OSS tooling ecosystem

These are the broader OSS tools the bridge can borrow patterns from. None of them are MCP-specific but their primitives transfer.

| Project | License | Capability layer | Maturity | Borrowability | URL |
|---|---|---|---|---|---|
| **Jepsen** | Eclipse Public License 1.0 | Distributed-systems testing framework. Nemesis (fault injection) + Generator (workload) + Checker (history analysis). | Mature; 10+ years | **Highest.** The nemesis/generator/checker triad applied to OTel traces is the most direct bridge pattern. See § 9 B-1. | <https://github.com/jepsen-io/jepsen> |
| **Elle** (Jepsen checker) | Eclipse Public License 1.0 | Linear-time history checker for transactional consistency. | Mature | Direct: history-checking adapted from databases to tool-call sequences. | <https://github.com/jepsen-io/elle> |
| **Hypothesis** | Mozilla Public License 2.0 | Property-based testing for Python (and now most languages via Hypothesis-strategies). Stateful testing via rule-based state machines. Integrated shrinking. | Mature; 8.6k stars | High. Hypothesis's rule-based state-machine model maps directly onto MCP tool-call sequencing; shrinking applied to failed OTel traces produces minimal counterexamples. | <https://github.com/HypothesisWorks/hypothesis> |
| **Pact** | MIT | Consumer-driven contract testing for HTTP/message-queue. Polyglot SDK; broker model for sharing pacts across organizations. | Mature | High. Pact-style consumer-driven contracts for MCP plugin/host. See § 9 B-3. | <https://github.com/pact-foundation/pact-specification> |
| **OpenTelemetry Collector** | Apache 2.0 | Vendor-neutral telemetry pipeline: receivers + processors + exporters. Filter, transform, tail-based sampling, attribute matching. | Mature | High. The Collector *is* the telemetry plumbing the Intentional Mapping harness sits on top of. It does not provide test-harness or conformance-validation surfaces — those must be built. | <https://github.com/open-telemetry/opentelemetry-collector> |
| **Honeycomb Refinery** | Apache 2.0 | Trace-aware tail-based sampling proxy. Rules-based sampling (keep 100% of error traces); dynamic sampling; debug metadata. | Mature | Medium-high. Refinery's "examine whole trace before deciding" model is the precondition for Intentional Mapping assertions that span multiple spans. | <https://github.com/honeycombio/refinery> |
| **Grafana Tempo** | AGPL-3.0-only (Apache exceptions) | Trace storage backend with TraceQL query language. Accepts OTLP. Includes `tempo-vulture` consistency-checking tool. | Mature | High for the *query* layer. TraceQL is the right shape for declaring Intentional Mapping assertions ("all `tool_decision` events parented by a `claude_code.hook` span where attribute X..."). | <https://github.com/grafana/tempo> |
| **Cucumber / Gherkin** | MIT | Behavior-driven development. Given-When-Then scenarios; polyglot step-definition compilers; JSON message protocol between Gherkin parser and step runners. | Mature | High for the *scenario-authoring* layer. Gherkin scenarios as the human-readable expression of Intentional Mapping rows is a strong adoption candidate. See § 9 B-4. | <https://github.com/cucumber> |
| **AgentSight** | Apache 2.0 | eBPF-based system-level agent observability. TLS interception + kernel event correlation. | New; arXiv 2025 | Medium. Complementary to OTel approach — useful when OTel is not configured but agents are running. | <https://github.com/eunomia-bpf/agentsight> |

---

## 7. Primary-source reading list

Categorized URLs (≥20) every Phase B / C session should keep within one click:

### MCP specification + tooling

- MCP specification (canonical) — <https://modelcontextprotocol.io/specification>
- MCP specification GitHub — <https://github.com/modelcontextprotocol/specification>
- MCP Inspector — <https://github.com/modelcontextprotocol/inspector>
- Python SDK — <https://github.com/modelcontextprotocol/python-sdk>
- TypeScript SDK — <https://github.com/modelcontextprotocol/typescript-sdk>
- mcp-validator — <https://github.com/Janix-ai/mcp-validator>
- mcp-server-tester (steviec) — <https://github.com/steviec/mcp-server-tester>
- mcp-server-tester (gleanwork) — <https://github.com/gleanwork/mcp-server-tester>
- mcptap — <https://github.com/mcptap/mcptap>

### OpenTelemetry semantic conventions

- OTel SIG-GenAI charter — <https://github.com/open-telemetry/community/blob/main/projects/gen-ai.md>
- OTel GenAI semantic conventions — <https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai>
- OTel GenAI dedicated repo — <https://github.com/open-telemetry/semantic-conventions-genai>
- OTel LLM-observability blog — <https://opentelemetry.io/blog/2024/llm-observability/>
- OTel Collector — <https://github.com/open-telemetry/opentelemetry-collector>

### Distributed tracing foundations

- Dapper paper — <https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/>
- Honeycomb Refinery — <https://github.com/honeycombio/refinery>
- Grafana Tempo + TraceQL — <https://github.com/grafana/tempo>

### Property-based and stateful testing

- QuickCheck (Claessen & Hughes 2000) — <https://doi.org/10.1145/351240.351266>
- Hypothesis — <https://github.com/HypothesisWorks/hypothesis>
- *Property-Based Testing in Practice* (Goldstein et al. ICSE 2024) — <https://doi.org/10.1145/3597503.3639581>
- *Empirical Evaluation of Property-Based Testing in Python* (Ravi & Coblenz 2025) — <https://doi.org/10.1145/3764068>

### Distributed-systems consistency testing

- Jepsen — <https://github.com/jepsen-io/jepsen>
- Elle (Kingsbury PODC 2021) — <https://doi.org/10.1145/3465084.3467483>

### Agent evaluation methodology

- GAIA (Mialon et al. ICLR 2024) — <https://arxiv.org/abs/2311.12983>
- *Survey on Evaluation of LLM-based Agents* (Yehudai et al. 2025) — <https://arxiv.org/abs/2503.16416>
- AgentPex / *Willful Disobedience* (Sharma et al. 2026) — <https://arxiv.org/abs/2603.23806>
- ReliabilityBench (Gupta 2026) — <https://arxiv.org/abs/2601.06112>
- AgentSight (Zheng et al. PACMI@SOSP 2025) — <https://arxiv.org/abs/2508.02736>

### Attestation and supply-chain provenance

- in-toto attestation — <https://github.com/in-toto/attestation>
- SLSA Provenance v1.0 — <https://slsa.dev/spec/v1.0/provenance>
- Sigstore cosign — <https://docs.sigstore.dev/>

### Consumer-driven contract testing

- Pact specification — <https://github.com/pact-foundation/pact-specification>

### Behavior-driven development

- Cucumber / Gherkin — <https://github.com/cucumber>

---

## 8. Bridge-gap map — failure-shape category × required signals × existing tooling × gap

This is the load-bearing table of the document. Each row maps one Intentional Mapping failure-shape category to the signals required to observe it, the existing tooling that can emit or consume those signals, and the gap that remains.

| ID | Failure-shape (vendor-neutral) | Required signals (per `intentional-mapping-template.md`) | Existing tooling that touches this | Gap |
|---|---|---|---|---|
| **MM-1** | Async write returns success but downstream read sees stale state | `claude_code.hook_execution_complete` log event correlated with upstream `tool_decision`; downstream `tool_result` event reflecting reconciled state. Trace-context propagation across async boundary (Dapper-style). | OTel Collector (transport); Honeycomb Refinery (whole-trace inspection); Jepsen / Elle (history-checking pattern); Hypothesis (state-machine generation). | **No MCP-specific harness emits "race detected" assertions from the OTel stream.** The trace plumbing exists; the assertion library does not. |
| **MM-2** | Read-side response shape drifts across consecutive calls | `claude_code.tool_result` events for both list and detail tools; assertion on shape parity via response-side payload-size attribute (e.g., `tool_output_size_bytes` if exposed, or counting structured-content fields on the result side); optional content shape via `OTEL_LOG_TOOL_CONTENT=1`. **Note:** `tool_input_size_bytes` is the argument-side counterpart and does NOT reflect response drift — MM-2 is strictly about the result payload returned by the tool. | gleanwork/mcp-server-tester (snapshot + Zod-schema matchers, but on direct calls, not on OTel stream); GraphQL Inspector pattern (schema-drift detection). | **No tool consumes OTel `tool_result` content and asserts cross-call shape parity.** Existing tooling asserts per-call; Intentional Mapping needs cross-call. |
| **MM-3** | Cooldown / debouncing window required before next equivalent operation | `claude_code.hook_execution_complete` log event with handler-emitted `decision: block` semantics; subsequent `claude_code.tool_decision` showing the retry attempt. | Cucumber/Gherkin (scenario authoring); Pact (request-shape contracts); OTel Collector (filtering and grouping). | **No declarative DSL for cooldown invariants over an OTel signal stream.** Closest pattern is Jepsen's nemesis-as-rate-limiter, but that's for the SUT not the harness side. |
| **MM-4** | Operation requires verification of side-effect completion before downstream reliance | `claude_code.hook_execution_start` → `claude_code.hook_execution_complete` (verified) → downstream `tool_decision` events parented under the same trace. | Dapper-style trace-context propagation (mature, via OTel); Tempo TraceQL (query language for trace shape); Elle history-checking (formalism for happens-before). | **Trace plumbing exists; happens-before assertion library for MCP does not.** TraceQL can express the query but no library composes the assertion at conformance-spec level. |
| **MM-5** | Tool inputs need mandatory context (caller identity, intent, policy tag) the model isn't reliably providing | `claude_code.hook_execution_complete` log event; `claude_code.tool_decision` with augmented inputs visible (under `OTEL_LOG_TOOL_DETAILS=1`). | OTel Collector attribute-matching processor; mcp-validator (input-schema validation). | **Hook-mutation observation requires a deeper-beta gate** (`OTEL_LOG_TOOL_DETAILS=1`). The signal is observable; no conformance harness asserts on it. Plus: tool-discoverability problem (gleanwork) is a sibling MM-5 issue that may warrant its own MM-7 category. |
| **MM-6** | Server-side endpoint requires strict-mode protocol compliance the model's default input doesn't enforce | `claude_code.hook_execution_complete` log event; `claude_code.tool_result` showing the server accepted (not rejected) the call. | Pact (strict-mode request reformat); mcp-validator (W3C / RFC strict-mode schemas). | **No bridge between Pact-style request contracts and OTel-stream verification.** Pact handles "did we send right format?"; Intentional Mapping needs "did the server accept it, observable from the agent side?" |

**Cross-cutting gap:** All six rows assume the agent harness exposes the named OTel signals at the named gate (`CLAUDE_CODE_ENABLE_TELEMETRY=1`, `OTEL_LOGS_EXPORTER=otlp`, sometimes `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` or deeper). The Phase A RFC at `001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` proposes complementary signals (`agent.rollout.gate.*`, `agent.evidence_bundle.*`) but does not yet codify the Intentional Mapping signal vocabulary as a vendor-neutral OTel semantic convention. Phase B handoff is to file the Intentional Mapping signal vocabulary as an SIG-GenAI RFC alongside the rollout-gate RFC.

---

## 9. Borrowable patterns — concrete adoption candidates

The literature and ecosystem surveys converge on five concrete patterns the Intentional Mapping methodology can adopt without inventing from scratch.

### B-1. Jepsen nemesis-generator-checker, with OTel trace as history-source

**Pattern:** Adapt Jepsen's three-component model. The *generator* produces tool-call sequences (via `claude -p` invoking the agent against the plugin under test). The *nemesis* injects faults at the OTel pipeline boundary (network partitions between agent and MCP server, tool-result delays, clock skew between hook and tool spans). The *checker* consumes the OTel trace stream and asserts the Intentional Mapping predicates.

**Estimated effort:** Phase C, 6-10 weeks of engineering for v0.1.
**Primary sources:** <https://github.com/jepsen-io/jepsen>, Kingsbury (2021), Sigelman et al. (2010).
**Why this pattern:** Most mature; production-proven over 10+ years; checker model is reusable; nemesis taxonomy is well-established.

### B-2. Hypothesis-style executable Intentional Mapping (DSL → executable specs)

**Pattern:** Evolve the current Intentional Mapping from a markdown table into an executable specification. Each Intentional Mapping row becomes a Python function decorated with `@matcher_map_rule(category="MM-1", signal="claude_code.hook_execution_complete")`; the Hypothesis state-machine framework drives input generation; shrinking produces minimal failing traces.

**Estimated effort:** Phase C, 4-6 weeks.
**Primary sources:** <https://github.com/HypothesisWorks/hypothesis>, Goldstein et al. (2024), Claessen & Hughes (2000).
**Why this pattern:** Lower bar for plugin authors than B-1 (write a property, not a checker); leverages an existing mature toolchain; output is an executable conformance harness, not just a doc.

### B-3. Pact-style consumer-driven MCP-plugin contract

**Pattern:** Define a "MCP plugin pact": the agent-harness-side (consumer) declares its expectations of the plugin's MCP server, the plugin (provider) verifies its server satisfies the pact. The pact format extends Pact JSON with an OTel-signal section: "given tool X is called, expect Y signals on the OTel stream within Z seconds."

**Estimated effort:** Phase B (spec) 2 weeks; Phase C (verifier) 6 weeks.
**Primary sources:** <https://github.com/pact-foundation/pact-specification>, Schwarz et al. (2025).
**Why this pattern:** Lowest barrier to multi-org adoption; pact files are easy to share via partner agreements; Postel's-Law shape fits agent-to-plugin interaction.

### B-4. Cucumber-style Gherkin scenarios as human-readable Intentional Mapping rows

**Pattern:** Each Intentional Mapping row gets a Gherkin scenario. `Given the agent invokes confirmAppUpload / When the harness emits claude_code.tool_decision / Then within 5 seconds claude_code.hook_execution_complete with decision="approve" must appear / And the downstream getApp tool_result must reflect the new appId`. Step definitions compile to assertions against an OTel trace store (Tempo + TraceQL).

**Estimated effort:** Phase B, 2 weeks.
**Primary sources:** <https://github.com/cucumber>, <https://github.com/grafana/tempo>.
**Why this pattern:** Makes Intentional Mapping rows readable by non-engineers (legal, partner reviewers, auditors); separates spec authoring from harness implementation.

### B-5. in-toto attestation envelope for signed conformance reports

**Pattern:** Each conformance run produces a signed `conformance/v1` predicate (new predicate type). The envelope wraps: the Intentional Mapping spec version, plugin commit SHA + tag, the OTel trace evidence bundle URI, the per-row PASS/PARTIAL/FAIL with optional finding evidence, the harness identity + version (`builder.id` analogue), the env-var gate set. Signed via cosign.

**Estimated effort:** Phase B (predicate definition) 1 week; Phase C (cosign integration) 2 weeks.
**Primary sources:** <https://github.com/in-toto/attestation>, <https://slsa.dev/spec/v1.0/provenance>, <https://docs.sigstore.dev/>.
**Why this pattern:** Maps cleanly onto existing supply-chain attestation infrastructure; auditors can verify conformance bundles using the same tooling they use for SLSA provenance; complements Phase A RFC's `agent.evidence_bundle.*` events.

---

## 10. Research gaps the Intentional Mapping methodology fills

Synthesizing § 3-§ 9, four gaps in the literature and tooling ecosystem are clear, and the Intentional Mapping methodology fills each:

1. **Outcome-evaluation overhang.** The agent-evaluation literature (GAIA, AgentBench, SWE-Bench, τ-bench) is dominated by outcome scoring; protocol-level signal-stream evaluation is barely addressed. The Yehudai 2025 survey identifies *robustness* as an open gap without naming the signal-stream approach. Matcher-map provides a robustness-evaluation methodology grounded in runtime signals.

2. **Vendor-neutrality gap in MCP test tooling.** Every existing MCP test tool (mcp-validator, mcp-server-tester variants, mcptap) targets the schema/transport layer or the per-call functional layer. None defines a vendor-neutral, finding-shape-based assertion vocabulary that operates on the OTel signal stream. The Intentional Mapping's six categories MM-1..MM-6 are that vocabulary.

3. **Trace-context-propagation without an assertion library.** OpenTelemetry inherits Dapper's trace-context propagation, and the Collector + Refinery + Tempo stack makes trace data abundant. But there is no library that consumes an OTel trace and asserts on the agent-protocol predicates that production reliability depends on (race conditions, cooldowns, state verification). The Intentional Mapping row format *is* the missing assertion library, in declarative form, ready to be compiled to executable assertions (via B-2 Hypothesis pattern).

4. **No attestation predicate for conformance evidence.** in-toto + SLSA make it routine to attest *that an artifact was built correctly*. There is no analogous predicate for *that an artifact's runtime behavior conforms to a spec*. The Conformance Provenance predicate (per B-5) closes this gap and lets MCP-plugin conformance claims travel as signed bundles between partner organizations.

---

## 11. Phase B + C scope recommendation

Split into Phase B (spec + minimal collector setup) and Phase C (executable conformance harness). Each work item names rationale, estimated effort, and primary-source links.

### Phase B — Spec and minimal-collector setup (8-12 weeks total)

**B-1. File Intentional Mapping signal vocabulary as OTel SIG-GenAI RFC.**
Rationale: § 8 cross-cutting gap. Filing the vocabulary into the upstream semantic-conventions repo is the multiplier — it makes every future agent harness emit the right signals by default.
Effort: 3 weeks (drafting + community review).
Primary sources: <https://github.com/open-telemetry/community/blob/main/projects/gen-ai.md>, <https://github.com/open-telemetry/semantic-conventions>.

**B-2. Define the Pact-style MCP plugin contract format (extend Pact v4 with OTel-signal section).**
Rationale: § 9 pattern B-3. Lowest-friction multi-org adoption path.
Effort: 2 weeks.
Primary sources: <https://github.com/pact-foundation/pact-specification>.

**B-3. Define the in-toto Conformance Provenance predicate.**
Rationale: § 9 pattern B-5. Companion to Phase A RFC.
Effort: 1 week.
Primary sources: <https://github.com/in-toto/attestation>, <https://slsa.dev/spec/v1.0/provenance>.

**B-4. Stand up a minimal OTel Collector + Tempo + Refinery reference deployment.**
Rationale: § 6 adjacent-OSS tooling. Phase C cannot start until there's somewhere for traces to land.
Effort: 1 week.
Primary sources: <https://github.com/open-telemetry/opentelemetry-collector>, <https://github.com/grafana/tempo>, <https://github.com/honeycombio/refinery>.

**B-5. Author Gherkin scenarios for the six MM-1..MM-6 categories (one per row).**
Rationale: § 9 pattern B-4. Makes the spec auditable by non-engineers.
Effort: 1-2 weeks.
Primary sources: <https://github.com/cucumber>.

### Phase C — Executable conformance harness (12-16 weeks)

**C-1. Build the Jepsen-style nemesis-generator-checker harness against the Intentional Mapping.**
Rationale: § 9 pattern B-1. Most mature production-proven model.
Effort: 6-10 weeks.
Primary sources: <https://github.com/jepsen-io/jepsen>, Kingsbury (2021).

**C-2. Implement Hypothesis-based executable-Intentional Mapping decorator library (`@matcher_map_rule`).**
Rationale: § 9 pattern B-2. Lower bar for plugin authors to write their own conformance checks against MM-1..MM-6.
Effort: 4-6 weeks.
Primary sources: <https://github.com/HypothesisWorks/hypothesis>, Goldstein et al. (2024).

---

## 12. What's NOT in scope here

To prevent scope drift in Phase B / C:

- **Not implementation.** This document is a landscape map; the implementation is Phase B + C work items above.
- **Not collector deployment.** B-4 is referenced as a Phase B work item but specifying exact YAML config and infrastructure choices is Phase B's job, not this document's.
- **Not test authorship.** Authoring Intentional Mapping rows for a *specific* MCP plugin is engagement work, not landscape work.
- **Not vendor-specific findings.** Every observation here is vendor-neutral. The first reference implementation case study against an enterprise MCP plugin is engagement-private until the plugin maintainer consents to being named — see `intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/SPEC.md` § "Conformance reporting."
- **Not a competitive frame against existing OSS.** The existing MCP test tools (mcp-validator, mcp-server-tester variants, mcptap) are surveyed for *what they cover well*, with the Intentional Mapping methodology positioned as the orthogonal protocol-runtime-conformance layer that sits on top of them.
- **Not a publication.** A future academic publication based on this work would extract the Intentional Mapping methodology and the Phase B+C conformance results into venue-appropriate form; this document is the precursor research log, not the paper.

---

## 13. Cross-references

- Phase A OTel RFC draft: [`000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`](./001-DR-RFC-otel-agent-rollout-gate-signals-draft.md)
- Public Intentional Mapping methodology: [`specs/mcp-plugin-observability/v0.1.0-draft/SPEC.md`](../specs/mcp-plugin-observability/v0.1.0-draft/SPEC.md)
- Matcher-map template: [`specs/mcp-plugin-observability/v0.1.0-draft/intentional-mapping-template.md`](../specs/mcp-plugin-observability/v0.1.0-draft/intentional-mapping-template.md)
- Sibling workstreams (separate documents): Workstream A (spec-anchored OTel handoff), Workstream B (vendor-neutral conformance harness design), Workstream D (synthesis)

---

*Generated 2026-05-10 as Part 2 Workstream C deliverable.*
