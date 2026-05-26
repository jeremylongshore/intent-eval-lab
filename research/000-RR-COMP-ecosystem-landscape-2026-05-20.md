---
title: Ecosystem Landscape — OSS + Frontier-Lab Audit for IEP Phase B
filing_code: 000-RR-COMP
date: 2026-05-20
status: working — feeds the per-area landscape matrices in the findings PDF
program_bead: bd_000-projects-ppt2
framing: technical / craft / contribution audit — NOT market / pricing / GTM
---

# Ecosystem Landscape — OSS + Frontier-Lab Audit

Verbatim project state captured via WebFetch on 2026-05-20. Goal: identify where to **contribute upstream** vs **build in our repos** vs **skip because well-covered**. Not a competitive scan — a craft-contribution audit.

## Trace / observability layer

| Project | Maintainer | License | Last meaningful release | Conventions | Posture toward our work |
|---|---|---|---|---|---|
| **OpenTelemetry GenAI semconv** | CNCF / OTel SIG | Apache 2.0 | In Development status as of May 2026 | Model + agent spans; experimental, gated on `OTEL_SEMCONV_STABILITY_OPT_IN` | **Active SIG; contribution surface open.** Our `agent-loop-trace/v1` (iel-E12) can converge with this. |
| **OpenInference** | Arize-ai | Apache 2.0 | go-instrumentation-openai-go v0.1.0 (2026-05-18); 30+ Python + 9 TS + 4 Java + 4 Go packages | Defines own AI-specific semantic conventions, **complementary** to OTel, transport-agnostic | Closest analog to what we'd need for cross-tool trace portability. **Native integration target.** |
| **OpenLLMetry** | Traceloop | Apache 2.0 | v0.60.0 (2026-04-19), 7.1k stars, 257 releases | "Semantic conventions are now part of OpenTelemetry" — actively upstreamed | Less novel — upstreams to OTel SIG. Reference for how to seed OTel contributions. |
| **Phoenix** | Arize-ai (commercial parent) | **Elastic License 2.0** (patent-flagged) | active, OTel + OpenInference base, MCP server bindings | Uses OpenInference + OTel | **License incompatibility** — ELv2 is not OSI-OSI; our Apache 2.0 platform won't depend on it. Useful as competitive reference, not as upstream. |
| **Langfuse** | Langfuse GmbH (YC W23) | MIT (`ee/` folders enterprise) | v3.174.1 (2026-05-13), 562 releases, 7051 commits | Custom + OTel integration mentioned, no specific GenAI conv claim | **MIT core + ee enterprise split.** Closer to a typical commercial-OSS posture. Useful as feature-matrix reference. |

**Verdict for our work**: contribute upstream to OTel GenAI SIG via `agent-loop-trace/v1` proposal in iel-E12 spec process. Native integration with OpenInference. Phoenix is a "look but don't import" reference because of ELv2. Don't try to compete with Langfuse — different surface (they ship a hosted observability product; we ship a contracts kernel + gate-result spec).

## Eval framework layer

| Project | Maintainer | License | Last meaningful release | Eval surface | Posture toward our work |
|---|---|---|---|---|---|
| **Inspect AI** | UK AISI (`UKGovernmentBEIS`) | MIT | 5714 commits, active | 200+ pre-built evals, tool-use + multi-turn + model-graded | **Strongest standards-track precedent** — government-backed, MIT, multi-surface. Worth deep schema review. Our `gate-result/v1` should be expressible as an Inspect output. |
| **Promptfoo** | Promptfoo (now part of OpenAI) | MIT | v0.121.11 (2026-05-08), 408 releases | CLI + library, prompt testing, red-team, CI/CD, PR scanning | Adjacent — focused on prompt-grade testing + redteam, not our agent + gate-result domain. No spec convergence opportunity but valuable as CI-integration reference. |
| **DSPy** | Stanford NLP | MIT | v3.2.1 (2026-05-05), 108 releases | Programming-not-prompting; built-in Assertions (Dec 2023) for self-refining pipelines | Orthogonal — DSPy is a programming model; we're a verification surface. Could integrate as `EvalSpec` source. |

**Verdict**: Inspect AI is the right schema-comparison reference for `gate-result/v1`. Promptfoo + DSPy live in adjacent surfaces — useful but not convergence targets.

## Benchmark / dataset layer

| Project | Maintainer | License | Last update | Replay support | Posture |
|---|---|---|---|---|---|
| **SWE-bench** | Princeton NLP | MIT | 2025-01-13 (SWE-bench Multimodal + sb-cli) | Docker build + eval logs, no explicit replay determinism | Foundational benchmark; we should be able to **emit Evidence Bundles from SWE-bench runs** for iel-E11 RF-X classification. |
| **OSWorld** | xlang-ai | Apache 2.0 | 2025-07-28 (OSWorld-Verified + AWS parallelization, 1hr runtime) | Screenshots + actions + video, no explicit determinism | Computer-use benchmark; **our replay-fidelity spec (iel-E11) could absorb OSWorld trajectories** as a test case. |
| **τ-bench / τ²-bench / τ³-bench** | Sierra Research | MIT | active, redirected to τ³ (banking, voice) | Historical trajectories in `./historical_trajectories`, no replay determinism claim | Agent-tool-use benchmark; trajectory format reference for iel-E12. |
| **METR eval-analysis-public** | METR | License referenced but not enumerated | 24 commits, recent activity | `runs.jsonl` raw + bootstrap fits | Time-horizon methodology; **our reliability scoring (iec-deferral-A AssertionExpression) should be expressible against METR runs**. |
| **AgentBench** | Tsinghua | check repo | 2024 | unclear from this fetch | Reference benchmark — not deep-fetched in this pass; add to follow-on if needed. |

**Verdict**: SWE-bench and METR are the two most useful schema-bridges. iel-E11 RF-X spec should explicitly accommodate SWE-bench and OSWorld trajectory shapes. METR's `runs.jsonl` is a sanity-check format for iec's gate-result/v1 to render against.

## Frontier-lab research surfaces (mapped via prior context + bibliography)

| Lab | Most-relevant published material | Surface |
|---|---|---|
| **Anthropic** | Turpin "Models Don't Always Say" (Sleeper Agents); Measuring Faithfulness in CoT; Constitutional AI; Sleeper Agents (Hubinger 2024) | CoT authenticity (Area #11), reasoning monitoring, alignment-pretraining contamination |
| **OpenAI** | Process reward models; verifier scaling; OpenAI Evals (deprecated → Inspect-style); contamination work | Verifiers (Area #6), test-time compute (Area #9), benchmark contamination (Area #2) |
| **Google DeepMind** | JETTS (judges-as-evaluators); FunSearch; Verifier scaling; Sample/Scrutinize/Scale | Verifier (Area #6), inference compute (Area #9), reasoning eval |
| **METR** | Time-horizon methodology, RE-Bench, dangerous capability evals | Reliability scoring (Area #19), long-horizon agent evals |
| **UK AISI** | Inspect AI framework, dangerous-capability evaluations, foundation-model eval methodology | Eval-systems (Area #2), standards-track precedent (Area #20) |
| **Apollo Research** | Deception evaluations, situational awareness measurement | Reasoning authenticity (Area #11), evaluator gaming (Area #19 shared) |
| **Redwood Research** | Evaluator gaming theoretical work, alignment evaluations | Evaluator gaming (Area #19 shared), gradient routing |

**Verdict on frontier-lab posture**: their published work overwhelmingly addresses Areas #2, #6, #9, #11, #19, and the personal-skill pillar (#13-16). Their work on Areas #1, #5, #10, #12, #17, #18, #20, #21 is sparse. Sparse means contribution surface is open. Dense means our work should explicitly cite and not reinvent.

## Standards-track surfaces (community / SIG / WG)

- **OpenTelemetry SIG GenAI** — active, semantic conventions in Development status. Contribution open via GitHub issues, RFCs, weekly meetings.
- **W3C** — no formal AI WG identified at our scan depth. Suggest: deferred.
- **CNCF** — hosts OpenTelemetry; tangential AI work in cloud-native AI WG (KubeAI, OpenInference, Phoenix). Not a standards body for evaluation schemas yet.
- **AgentSkills.io / Anthropic** — informal open standard followed by Claude Code skills; relevant for skill-eval but not gate-result.
- **MCP (Model Context Protocol)** — Anthropic-led, fast-moving, multi-vendor adoption. Our iar (intent-rollout-gate) work could expose gate-result via an MCP surface.
- **OASIS / IETF / ISO** — none active in this space.

**Verdict**: OpenTelemetry GenAI is the only live standards body. MCP is an open de-facto standard with rapid uptake. Our `gate-result/v1` should be expressible against both.

## License compatibility quick-check (with our Apache 2.0 platform posture)

| Project | License | Compatible? |
|---|---|---|
| OpenTelemetry / semconv | Apache 2.0 | ✅ |
| OpenInference | Apache 2.0 | ✅ |
| OpenLLMetry | Apache 2.0 | ✅ |
| Inspect AI | MIT | ✅ |
| Promptfoo | MIT | ✅ |
| DSPy | MIT | ✅ |
| SWE-bench | MIT | ✅ |
| OSWorld | Apache 2.0 | ✅ |
| τ-bench | MIT | ✅ |
| METR | unspecified | ⚠ (clarify before depending) |
| Langfuse | MIT core / ee enterprise | ✅ (core only) |
| Phoenix (Arize) | **Elastic License 2.0** | ❌ (not OSI-compatible) |

**Verdict**: every project we'd plausibly converge or contribute against is Apache-2.0 / MIT compatible except Phoenix. Phoenix becomes a reference, not a dependency.

— landscape captured by WebFetch direct queries; verbatim quotes preserved where licensing or capability claims were given.
