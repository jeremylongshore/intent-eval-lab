---
title: Shared Bibliography — Iterative Snacking Walrus Phase B Research Program
filing_code: 000-RR-BIBL
date: 2026-05-20
status: working — citation backbone for the immediate-deliverable 60-100pg findings PDF
program_bead: bd_000-projects-ppt2
---

# Shared Bibliography

Compiled 2026-05-20 from Semantic Scholar MCP `paper_bulk_search` × 16 seed queries spanning the 21 advisory gap areas. Cluster tags map to the 5-team research framework (§ 4 of the plan). Tier-1 = ≥ 100 citations, Tier-2 = 30-99, Tier-3 = 10-29. Pre-2026 only — frontier moves fast, but we want defensible bedrock.

## Coverage matrix (queries × hits)

| Seed query | Hits returned | Cluster | Notable papers |
|---|---|---|---|
| LLM agent trajectory benchmark | 124 (top 100 captured) | A | AgentRewardBench (S2 `9202e94`), AgentRx diagnose failures (S2 `0515b69`), TRAJECT-Bench (S2 `f7a4272`), AgenTracer (S2 `7fdbdd7`) |
| OpenTelemetry distributed tracing semantic conventions | 0 | D | (academic literature thin — confirms our W4 is in standards-track work, not papers; pivot to WebFetch) |
| OpenTelemetry GenAI agent observability tracing | 0 | D | (ditto — community/standards-driven, not paper-driven) |
| LLM agent observability monitoring trace | 1 | D | AgentOps (S2 `3d6b189`) — the *only* peer-reviewed paper on the specific observability surface as of May 2026 |
| Synthetic data quality LLM training reasoning diversity | 7 | B | Prismatic Synthesis (S2 `b71a9a4`), Smaller Weaker Better (S2 `41a4234`), MathSmith (S2 `3da24e1`), MegaMath (S2 `7a070ce`) |
| LLM self verification reasoning checker | 0 | B | (re-search needed with broader terms — covered by inference-time-compute hits) |
| Memory poisoning retrieval augmented generation attack | 6 | C | AgentPoison (S2 `b6948a9` — 293 cites, foundational), MemoryGraft (S2 `b1d80b2`), CtrlRAG (S2 `b308393`), NeuroGenPoisoning (S2 `a776dcb`) |
| LLM tool use agent function calling | 12 | D | xLAM (S2 `a75da88`), Granite (S2 `cbde6f0`), TinyAgent (S2 `ff05249`), MCPToolBench++ (S2 `153e322`) |
| Inference time compute scaling test time reasoning | 38 | D / B | Sample Scrutinize Scale (S2 `b67c8d2`), When To Solve When To Verify (S2 `d170e69`), JETTS judges-as-evaluators (S2 `5f2dbd4`), Survey of Test-Time Compute (S2 `1fd282f`) |
| Chain of thought faithfulness | 57 | B | Turpin et al. "Models Don't Always Say" (S2 `7dc928f` — 1097 cites, the Anthropic foundational paper), "Reasoning Models Don't Always Say What They Think" (S2 `b9ca6db` — 297 cites), Measuring Faithfulness (S2 `827afa7` — 422 cites), When CoT is Necessary LMs Struggle to Evade Monitors (S2 `ab75715`) |
| LLM as judge evaluation bias | 56 | B / C | MT-Bench Zheng et al. (S2 `a0a79da` — 8440 cites, FOUNDATIONAL), Survey on LLM-as-Judge (S2 `e242442` — 1319 cites), Justice or Prejudice biases (S2 `e142887` — 306 cites), Position Bias (S2 `dfbfe75`), Self-Preference Bias (S2 `cf01d7c`), Preference Leakage (S2 `24e8029`), Principles & Guidelines for LLM Judges (S2 `a78fbbe`) |
| Multi agent LLM coordination communication | 17 | E | RoCo (S2 `c5d18db`), MegaAgent (S2 `d5b8474`), Red-Teaming Multi-Agent Communication (S2 `4669474`), SagaLLM context management (S2 `356b85a`), "Large Language Models Miss the Multi-Agent Mark" (S2 `d70edc1`) |
| LLM model routing cascade cost | 5 | E | MasRouter (S2 `086830d`), Unified Routing & Cascading (S2 `05e3853`), Uncertainty-Based Two-Tier Selection (S2 `8d59f23`), Agreement-Based Cascading (S2 `3e75ac5`) |
| LLM uncertainty quantification calibration | 6 | B | UQ&Calibration Survey (S2 `422b00c` — KDD 2025), Aligning with Human Judgement (S2 `aae01e9`), SPUQ perturbation-based UQ (S2 `9f02a3f`) |
| Prompt injection attack LLM agent defense | 23 | C | Agent Security Bench (S2 `5f4efbe` — 219 cites), Defeating Prompt Injections by Design (S2 `f25f0e3`), AgentDojo (S2 `cf95279`), Prompt Infection multi-agent (S2 `165921d`), Meta SecAlign (S2 `fc3d1be`), DRIFT (S2 `ec90620`) |
| SWE-bench autonomous benchmark | 7 | A / D | Agentless (S2 `ae50c8e` — 348 cites), SWE-Bench Pro long-horizon (S2 `4b83aa6`), HyperAgent (S2 `e786754`), Demystifying SWE Agents (S2 `d712280`) |
| LLM evaluation reproducibility deterministic | 3 | A / B | Reproducible LLM Eval (S2 `d019880`), REAL deterministic websites (S2 `1026a4d`) |
| RAG memory benchmark | 12 | C | LoCoMo (S2 `0bf3a18` — 432 cites, ACL 2024 long conversational memory), Mem0 (S2 `1d9c21a` — 319 cites), BABILong (S2 `b47507f` — 203 cites), Zep temporal KG (S2 `12407be`), "Memory in the Age of AI Agents" survey (S2 `d362b76`) |

## Citation roster (148 unique papers, ranked by cluster)

### Cluster A — Operational Trajectories, Replay, Reliability

- **Foundational benchmarks**: AgentRewardBench (`9202e949…`, 41 cites, 2025), TRAJECT-Bench (`f7a42726…`, 11 cites, 2025), AgentRx execution-trajectory diagnosis (`0515b697…`, 12 cites, 2026), AgenTracer who-induces-failure (`7fdbdd7f…`, 33 cites, 2025), REAL deterministic websites (`1026a4de…`, 26 cites, 2025).
- **SWE-bench cluster**: Agentless (`ae50c8e2…`, 348 cites, 2024), Demystifying SWE Agents (`d712280b…`, 121 cites, 2025), SWE-Bench Pro (`4b83aa6…`, 91 cites, 2025), HyperAgent (`e786754…`, 48 cites, 2024), Live-SWE-agent (`b1b1a459…`, 41 cites, 2025), Skywork-SWE (`e0922959…`, 19 cites, 2025).
- **Trajectory training / capture**: APIGen-MT multi-turn (`fb122b2e…`, 116 cites, 2025), AgentOhana unified data pipeline (`3ae65bb6…`, 53 cites, 2024), AgentGym evolving across environments (`3072ad49…`, 85 cites, 2024), TOUCAN 1.5M tool-agentic data (`00f3a348…`, 23 cites, 2025), AgentSynth (`d3944d49…`, 17 cites, 2025).
- **Reproducibility**: Reproducible LLM Eval Uncertainty (`d019880e…`, 29 cites, 2024).

### Cluster B — Verification, Calibration, Reasoning Authenticity, Disagreement

- **CoT faithfulness foundations**: Turpin Models Don't Always Say (`7dc928f4…`, **1097 cites**, NeurIPS 2023), Anthropic Measuring Faithfulness (`827afa7d…`, **422 cites**, 2023), Faithful CoT Reasoning (`b115c1e1…`, 383 cites, 2023), Question Decomposition Improves Faithfulness (`8154fb1d…`, 122 cites, 2023), Reasoning Models Don't Always Say (`b9ca6db2…`, **297 cites**, 2025), Are DeepSeek R1 More Faithful (`3f0455e9…`, 52 cites, 2025), CoT In The Wild Is Not Always Faithful (`e71ff518…`, 128 cites, 2025), Measuring CoT Faithfulness by Unlearning (`aaaa0435…`, 37 cites, 2025), When CoT Necessary LMs Struggle to Evade Monitors (`ab757156…`, 50 cites, 2025), FaithCoT-Bench (`6968f45a…`, 13 cites, 2025).
- **LLM-as-Judge**: Zheng MT-Bench (`a0a79dad…`, **8440 cites**, NeurIPS 2023 — must-cite), Survey on LLM-as-Judge (`e2442428…`, 1319 cites, 2024), JudgeLM (`69ecf88a…`, 324 cites, 2023), Justice or Prejudice quantifying biases (`e142887a…`, 306 cites, ICLR 2024), Humans or LLMs as Judge (`a28071c6…`, 298 cites, EMNLP 2024), Position Bias study (`dfbfe75e…`, 141 cites, 2024), Self-Preference Bias (`cf01d7c4…`, 182 cites, 2024), Replacing Judges with Juries (`1a9d2a80…`, 225 cites, 2024), Preference Leakage Contamination (`24e80291…`, 104 cites, 2025), Foundational Autoraters (`6c5ae8a0…`, 88 cites, EMNLP 2024), JuStRank (`c85e7a71…`, 21 cites, 2024), Principles & Guidelines for LLM Judges (`a78fbbe5…`, 27 cites, 2025), Limits to Scalable Eval (`aa6f16e9…`, 33 cites, ICLR 2025), LiveBench contamination-limited (`774d01e1…`, 127 cites, ICLR 2025), MixEval (`45ad78df…`, 79 cites, NeurIPS 2024), Aligning with Human Judgement Pairwise Preference (`aae01e93…`, 153 cites, 2024).
- **Verifier-side (inference-time compute as a verifier surface)**: Sample Scrutinize Scale (`b67c8d21…`, 37 cites, ICML 2025), When To Solve When To Verify (`d170e69d…`, 30 cites, 2025), JETTS Judges as Evaluators (`5f2dbd43…`, 33 cites, ICML 2025), Putting the Value Back in RL with Verifiers (`4db3afe0…`, 14 cites, 2025), Process Reward Models Survey (`b670078b…`, 20 cites, 2025), Survey Test-Time Compute (`1fd282ff…`, 18 cites, 2025), Reasoning on a Budget Survey (`bc29e85f…`, 19 cites, 2025).
- **Uncertainty / calibration**: UQ & Confidence Calibration Survey (`422b00c3…`, 81 cites, KDD 2025), SPUQ (`9f02a3fa…`, 40 cites, EACL 2024), UProp uncertainty propagation in agents (`86d60374…`, 13 cites, 2025), Empirical Analysis Uncertainty in LLM Eval (`4af30e08…`, 22 cites, ICLR 2025), Are LLM-Judges Robust to Uncertainty Markers (`0a978932…`, 27 cites, NAACL 2024), CalibraEval (`0b960c8f…`, 23 cites, ACL 2024).

### Cluster C — Memory, Security, Guardrails, Drift

- **Memory architecture**: LoCoMo Very Long-Term Memory (`0bf3a186…`, **432 cites**, ACL 2024), Mem0 production-ready memory (`1d9c21a0…`, **319 cites**, ECAI 2025), BABILong (`b47507f1…`, 203 cites, NeurIPS 2024), Zep temporal KG (`12407be4…`, 161 cites, 2025), Memory in the Age of AI Agents survey (`d362b761…`, 144 cites, 2025), G-Memory hierarchical multi-agent (`daa9bcf3…`, 55 cites, 2025), MemGen latent memory (`50daa134…`, 49 cites, 2025), Evaluating Memory in LLM Agents (`dc7c6878…`, 78 cites, 2025), Mem Construction & Retrieval Personalized (`a195d79a…`, 56 cites, ICLR 2025), ArcMemo (`eff7efaf…`, 17 cites, 2025), AMA-Bench long-horizon memory (`9fadf4b3…`, 10 cites, 2026), MemEvolve (`fc6e9b47…`, 34 cites, 2025), LEGOMem modular procedural memory (`bf675da7…`, 18 cites, 2025).
- **Memory poisoning**: AgentPoison (`b6948a9e…`, **293 cites**, NeurIPS 2024 — must-cite), MemoryGraft persistent compromise (`b1d80b2e…`, 23 cites, 2025), CtrlRAG black-box poisoning (`b308393d…`, 4 cites, 2025), NeuroGenPoisoning (`a776dcb6…`, 4 cites, 2025), Tricking Retrievers with Influential Tokens (`eb38fda0…`, 10 cites, NAACL 2025).
- **Prompt injection / agent security**: Agent Security Bench ASB (`5f4efbe3…`, **219 cites**, ICLR 2025), AgentDojo (`cf95279b…`, **115 cites**, NeurIPS 2024), Defeating Prompt Injections by Design (`f25f0e35…`, 126 cites, 2025), Prompt Infection LLM-to-LLM (`165921d2…`, 96 cites, 2024), Adaptive Attacks Break Defenses (`0ed8da38…`, 75 cites, NAACL 2025), Meta SecAlign (`fc3d1be5…`, 46 cites, 2025), Task Shield (`8af6009a…`, 49 cites, ACL 2024), MELON provable defense (`830cb224…`, 35 cites, ICML 2025), DRIFT defense (`ec906205…`, 27 cites, 2025), IPIGuard (`9ddcbbff…`, 30 cites, EMNLP 2025), PromptArmor (`560fc5db…`, 71 cites, 2025), AgentVigil (`9538721e…`, 28 cites, 2025), Safety at Scale Survey (`6f5fd241…`, 38 cites, 2025), Prompt Injection Attack to Tool Selection (`eb6cbd2b…`, 71 cites, NDSS 2026), BlindGuard multi-agent unknown attacks (`f583a040…`, 20 cites, 2025).
- **Guardrails**: ShieldAgent verifiable safety policy reasoning (`1b330d0b…`, 77 cites, ICML 2025), Foundational Guardrail via Synthetic Data (`0f1951b7…`, 11 cites, 2025), Think Twice Before You Act (`bbac4cef…`, 10 cites, 2025), LLM Agents Should Employ Security Principles (`089938fe…`, 22 cites, 2025), Monitoring Monitorability (`26220318…`, 14 cites, 2025).
- **AgentAuditor**: Human-Level Safety & Security Eval (`03a93e2e…`, 35 cites, 2025).

### Cluster D — Observability, Standards, Tool-Use, Inference-Time Compute

- **Observability (sparse academic — see WebFetch sweep for OSS-side)**: AgentOps (`3d6b189c…`, 21 cites, 2024 — *only* peer-reviewed paper on the specific surface).
- **Tool-use / function calling**: xLAM (`a75da880…`, 103 cites, 2024), Tool Learning in the Wild (`ca96d3b2…`, 64 cites, WWW 2025), Granite Function-Calling (`cbde6f07…`, 58 cites, EMNLP 2024), TinyAgent edge (`ff052499…`, 45 cites, EMNLP 2024), NESTFUL nested API calls (`5fc3ea33…`, 39 cites, EMNLP 2024), Compositional Instruction Tuning for Multi-turn FC (`1b50041b…`, 35 cites, ICLR 2024), Magnet multi-turn synthesis (`4d4c46ba…`, 25 cites, ACL 2025), CoALM (`3076cfba…`, 23 cites, ACL 2025), MCPToolBench++ (`153e3227…`, 24 cites, 2025), MCP-Bench (`59fc74ab…`, 58 cites, 2025), Agentic Reasoning Tool Integration via RL (`d804b642…`, 76 cites, 2025), Multi-modal Agent Tuning (`616a8e2e…`, 53 cites, 2024), Advancing Tool-Augmented LLMs Meta-Verification (`b1f92aed…`, 14 cites, KDD 2025), EvoTool (`3bb05e5e…`, 11 cites, 2026), TRAJECT-Bench (`f7a42726…`, 11 cites, 2025), TP-RAG benchmark (`2a919d50…`, 12 cites, EMNLP 2025).
- **Inference-time compute**: Sample Scrutinize Scale (`b67c8d21…`, 37 cites), Don't Overthink Shorter Chains (`6ef76fb7…`, 56 cites), e3 Learning to Explore (`ff76e9e0…`, 50 cites), Elastic Reasoning (`e3e34549…`, 39 cites), Survey Test-Time Compute (`1fd282ff…`, 18 cites), Cost of Dynamic Reasoning HPCA (`c1391af5…`, 26 cites, HPCA 2026), Sleep-time Compute (`a70f75cc…`, 23 cites, 2025), Thinking Longer Not Larger SE Agents (`7d03e6e1…`, 23 cites, ASE 2025), Reasoning on a Budget Survey (`bc29e85f…`, 19 cites, 2025), Energy Cost of Reasoning (`65477686…`, 14 cites, 2025), Energy-per-Token in LLM Inference (`284fca39…`, 16 cites, EuroMLSys 2025).
- **Self-improving / experience-driven**: EvolveR (`26f887d7…`, 46 cites, 2025), Learning on the Job (`f6352c67…`, 13 cites, 2025), Self-Generated In-Context (`1125a016…`, 11 cites, 2025), Iterative Self-Incentivization (`91c5af45…`, 10 cites, 2025).

### Cluster E — Multi-Agent State, Model Routing

- **Multi-agent coordination**: RoCo (`c5d18dbb…`, 252 cites, ICRA 2023), Scalable Multi-Robot Centralized vs Decentralized (`1ad73571…`, 161 cites, ICRA 2023), LLM-based MARL (`dd387552…`, 80 cites, 2024), Multi-Robot Systems Survey (`ebf086a0…`, 44 cites, 2025), MegaAgent without predefined SOPs (`d5b84741…`, 43 cites, ACL 2025), Embodied Multi-Agent Collaboration (`e1b62c7e…`, 56 cites, ACL 2024), Red-Teaming Multi-Agent Communication (`4669474d…`, 94 cites, ACL 2025), SagaLLM context management transactions (`356b85ae…`, 34 cites, VLDB 2025), Multi-Agent Mark Miss (`d70edc12…`, 21 cites, 2025), AgentsNet Coordination (`e2fd1d0a…`, 20 cites, 2025), AgentOrchestra hierarchical (`7e8b6a8a…`, 64 cites, 2025), Multi-Agent Credit Assignment (`198b1247…`, 12 cites, AAMAS 2025), Agentic AI Frameworks Architectures Protocols (`4740a540…`, 22 cites, 2025), AutoHMA-LLM heterogeneous coordination (`1487ff63…`, 37 cites, IEEE TCCN 2025).
- **Model routing**: MasRouter routing for multi-agent (`086830da…`, 52 cites, ACL 2025), Unified Routing & Cascading (`05e38538…`, 43 cites, ICML 2024), Uncertainty-Based Two-Tier Selection (`8d59f23d…`, 26 cites, 2024), Agreement-Based Cascading (`3e75ac5f…`, 14 cites, TMLR 2024), Cortex AISQL routing in production (`5af12150…`, 11 cites, 2025).

## Gaps observed (drives WebFetch sweep priorities)

1. **OpenTelemetry GenAI semantic conventions** → 0 academic hits. The work is happening in the OTel SIG GitHub repo + CNCF working groups, not in published papers. Must WebFetch the SIG status page.
2. **Open standards for eval / trace formats** → also community/spec-driven. WebFetch OpenInference + OpenLLMetry + W3C AI WG.
3. **Inspect AI / Promptfoo / Phoenix / Langfuse** → tool-vendor work, not academic. WebFetch each.
4. **Generator/checker verifier separation** → spotty academic surface; literature is dominated by self-verification + process reward models. The "independent generator vs checker" framing comes from Anthropic/DeepMind blog content. WebFetch Anthropic Sleeper Agents + DeepMind Verifier blog posts.
5. **Drift detection in deployed LLM systems** → no direct academic hits at our query depth; ML drift literature is mostly pre-LLM. Need to anchor on ML monitoring frameworks (Evidently AI, Arize Phoenix) via WebFetch.

## Note on citation handling in the findings PDF

- Inline cite format: `[arXiv: 2305.04388]` or `[S2: 7dc928f4…]` plus author-year for in-flow prose
- Each cited paper appears at least once in document body (no append-only bibliography padding)
- Numeric ranking (`Tier-1 / Tier-2 / Tier-3`) used to discriminate must-cite vs supporting where space is tight
- All non-academic / community / vendor evidence sourced via the parallel competitive-intel doc (000-RR-COMP)

— bibliography assembled by author; queries reproducible via Semantic Scholar MCP `paper_bulk_search` with the seed strings in the coverage matrix above.
