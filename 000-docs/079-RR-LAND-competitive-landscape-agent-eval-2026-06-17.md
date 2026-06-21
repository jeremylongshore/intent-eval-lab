---
title: Competitive Landscape — the agent-eval / LLM-eval / CI-gating / observability / rollout-gating space, and where the Intent Eval Platform is better / missing / needs improving
date: 2026-06-17
authors:
  - Jeremy Longshore (Intent Solutions)
status: RESEARCH (non-normative)
state_label: RESEARCH
filing_standard: Document Filing Standard v4.3
epic: bd_000-projects-qm77 (IEP competitive-lane + cost/budget strategy questions)
bead: bd_000-projects-qm77.1
relates_to:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — 12 binding principles, 5-repo taxonomy, anti-goals)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — 13-entity model, gate-result/v1, budget enforcement)
  - 014-DR-GLOS-canonical-glossary.md (canonical glossary — Evidence Bundle, predicate URIs)
companion:
  - 042-RR-LAND-prompt-and-context-eval-landscape-2026-06-06.md (the prompt/context-eval TOOL landscape this doc is the agent-eval PLAYER counterpart to)
  - 043-DR-RFC-intent-eval-target-generalization-2026-06-06.md (the unit-under-test generalization the lane rests on)
  - 080-RR-LAND-eval-economics-and-cost-forecast-cap-2026-06-17.md (the economics + cost-forecast-and-cap companion under the same epic)
verification: every external claim carries a live source URL in § 7; verification status (verified / partial / flagged) is recorded per source. Live search 2026-06-17.
---

> **Scope.** This is a research/landscape recon doc. Doc
> [`042`](042-RR-LAND-prompt-and-context-eval-landscape-2026-06-06.md) surveyed the
> _prompt + context evaluation **methodology and tool** landscape_ (G-Eval, RAGAS,
> promptfoo, DeepEval, Inspect, DSPy et al.). **This doc is its agent-eval _player_
> counterpart**: it surveys the commercial + OSS **products and benchmarks** in the
> agent-eval / LLM-eval / CI-gating / observability-trace-eval / rollout-gating space, and
> states — per competitive axis — where the **Intent Eval Platform (IEP)** is differentiated
> (**better**), where it has a real gap (**missing**), and where it is present but weak
> (**needs improving**). It is **non-normative**: it asserts no platform commitment; it maps
> terrain so the IEP's lane can be named against it.
>
> **Anchors.** The IEP is anchored throughout to its **5-repo taxonomy** (Blueprint A § 2.1:
> `intent-eval-core` · `intent-eval-lab` · `audit-harness` · `j-rig-skill-binary-eval` ·
> `intent-rollout-gate`) and its **Evidence Bundle convergence thesis** (the five repos
> compose via a shared signed-evidence schema, not via package consolidation — Blueprint A
> § 1.2 principle 10; glossary § 2.4). Every IEP term used here is defined in the canonical
> glossary [`014`](014-DR-GLOS-canonical-glossary.md).
>
> **Citation discipline (same as doc 042).** Every external claim carries a live source URL
> in § 7 with a verification status. Vendor revenue/funding figures and roadmap deprecations
> are corroborated against ≥1 primary source where possible; un-traceable or
> single-secondary-source claims are **flagged** in § 7.3 rather than asserted as fact.

---

## 0. How to read this document

§ 1 frames the market segmentation (five overlapping segments) and where the IEP sits. § 2
profiles the **players** segment-by-segment, each with a one-line "what it is" + the primary
source. § 3 is the **per-axis better / missing / needs-improving** table — the core of the
doc. § 4 names the **wedge** that survives the comparison. § 5 lists the **honest gaps** (what
the IEP genuinely does not do that competitors do). § 6 bridges to the economics companion
([`080`](080-RR-LAND-eval-economics-and-cost-forecast-cap-2026-06-17.md)) and the lane it
pinpoints. § 7 is the source register with verification status.

---

## 1. Market segmentation

The space the IEP competes in is not one market — it is five overlapping segments, and most
products span two or three. The IEP spans all five but is **strong** in only one (§ 4).

| Segment                                                | The question it answers                                                               | Representative players                                                                          |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **A. LLM/prompt-eval frameworks**                      | "Did this output meet the criteria?" (scores, judges, assertions)                     | OpenAI Evals, DeepEval, promptfoo, Braintrust, Inspect — surveyed in doc 042                    |
| **B. Agent observability + trace-eval**                | "What did the agent _do_ across a multi-step run, and where did it break?"            | LangSmith, Arize Phoenix, Comet Opik, Langfuse, Patronus Percival, Datadog LLM Obs              |
| **C. Agent reliability / runtime-guardrail platforms** | "Is the agent reliable enough to run in production, and can I guard it in real time?" | Galileo (Luna-2 guard models), Patronus, Guardrails-class products                              |
| **D. CI-gating / ship-no-ship**                        | "Should this change be allowed to merge / deploy?"                                    | promptfoo GitHub Action, Braintrust PR gates, LangSmith CI hooks, **IEP `intent-rollout-gate`** |
| **E. Agentic benchmarks (research-grade)**             | "How does this agent rank on a standardized task suite?"                              | τ-bench / τ²-bench, SWE-bench, GAIA, WebArena, Patronus TRAIL                                   |

**Where the IEP sits.** The IEP is not primarily a segment-A scorer (its judge layer is a
_means_, not the product), not a segment-B dashboard (it emits OTel but does not sell
observability), and not a segment-E benchmark author. Its declared territory is the
**intersection of D (CI-gating) and a substrate underneath all of A–E that none of them sell:
cryptographically attestable, replayable signed evidence of the verdict** (Blueprint A
principle 7 "auditability first"; doc 042 § 6 synthesis). The IEP's segment-D shell
(`intent-rollout-gate`) is thin _by design_ — the value is the Evidence Bundle it consumes,
not the gate logic (Blueprint A § 2.1).

---

## 2. The players (segment by segment)

### 2.1 Segment B — agent observability + trace-eval

| Player                        | What it is                                                                                                                                                                | Source    | Notable fact                                                                                                                                                                                                     |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LangSmith** (LangChain)     | Agent-engineering platform: tracing + datasets-from-traces + online evals on production traces + prompt mgmt + deploy; framework-agnostic (LangGraph, custom Python, any) | [S1]      | As of 2026 unifies cost across the whole agent workflow — LLM calls **plus** retrieval, tool execution, external-API spend — not just model tokens. The most mature trace→dataset→online-eval loop in the field. |
| **Arize Phoenix**             | OSS observability + eval SDK; OpenTelemetry tracing via OpenInference; configure evaluators + attach to datasets, auto-scored                                             | [S2]      | OTel-native; self-hostable; overlaps the IEP's OTel posture directly (Blueprint B § 4.3 `*.event` taxonomy).                                                                                                     |
| **Comet Opik**                | OSS LLM eval + observability; trace each LLM call / tool use / RAG retrieval                                                                                              | [S2]      | "Open-source, similar in spirit to Arize." A credible self-host alternative.                                                                                                                                     |
| **Langfuse**                  | OSS LLM-engineering platform; observability + eval + prompt mgmt + datasets; OTel-native                                                                                  | [042 S12] | Already cataloged in doc 042 § 3.2.                                                                                                                                                                              |
| **Patronus Percival**         | Automated agent-trace _debugging_: detects 20+ failure modes (bad tool use, context misunderstanding, planning errors) across large traces                                | [S3]      | Reduces human trace-analysis from ~1 hr to ~1–1.5 min (vendor claim, partial). Pairs with the **TRAIL** benchmark — best system scores only 11%, i.e. trace-issue localization is genuinely hard.                |
| **Datadog LLM Observability** | APM-vendor LLM-trace + eval add-on                                                                                                                                        | [S4]      | The "your existing observability vendor now does LLM eval" pressure on every pure-play.                                                                                                                          |

### 2.2 Segment C — agent reliability / runtime guardrails

| Player          | What it is                                                                                                                                                                            | Source | Notable fact                                                                                                                                                                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Galileo**     | Agent reliability platform: offline evals + production monitoring + **runtime guardrails**; agentic metrics (flow adherence, task completion, conversation quality, agent efficiency) | [S5]   | Differentiator = **Luna-2** purpose-built eval SLMs (3B/8B) running guardrails at sub-200 ms and ~$0.02/M tokens, claiming up to 97% monitoring cost reduction. Raised $68M total ($45M Series B, Scale VP-led); Fortune-50 logos. The best-funded direct adjacency. |
| **Patronus AI** | Scalable agent supervision + eval (Percival + TRAIL + LLM-judge tooling)                                                                                                              | [S3]   | Positions as "first scalable supervision solution for agentic systems." Research-credible (TRAIL benchmark).                                                                                                                                                         |

### 2.3 Segment D — CI-gating / ship-no-ship

| Player                        | What it is                                                                                           | Source                       | Notable fact                                                                                                                                                                                                        |
| ----------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **promptfoo**                 | OSS prompt/LLM eval + red-team; config-driven suites; GitHub Action gate                             | [042 S8]                     | **Acquired by OpenAI (announced 2026-03-09)**; folds into OpenAI Frontier, remains OSS. The dominant OSS CI-gate today.                                                                                             |
| **Braintrust**                | Commercial eval + observability; PR-blocking gates, side-by-side experiments with significance       | [042 S11]                    | The commercial CI-gate standard.                                                                                                                                                                                    |
| **LangSmith CI hooks**        | Eval-in-CI via the LangSmith SDK + GitHub integration                                                | [S1]                         | CI-gating bolted onto the observability platform.                                                                                                                                                                   |
| **IEP `intent-rollout-gate`** | Thin GitHub Action: consume an Evidence Bundle + a `tests/TESTING.md` policy → ship/no-ship decision | Blueprint A § 2.1; CLAUDE.md | Live at v0.2.0 with keyless cosign signing to the production Rekor transparency log (logIndex 1809941980). **The only gate in this row that emits a signed, externally-verifiable attestation of its own verdict.** |

### 2.4 Segment E — agentic benchmarks (research-grade)

| Benchmark                       | What it is                                                                                                                                                                                         | Source | Notable fact                                                                                                                   |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| **τ-bench / τ²-bench** (Sierra) | Tool-Agent-User interaction across retail/airline/telecom; τ² adds a **dual-control** (Dec-POMDP) telecom domain where both agent and simulated user act on shared state; 279 multi-turn dialogues | [S6]   | The reference for conversational tool-calling agent eval. Recent updates add native-voice full-duplex eval.                    |
| **SWE-bench**                   | Resolve real GitHub issues against real repos                                                                                                                                                      | [S7]   | The de-facto coding-agent benchmark.                                                                                           |
| **GAIA**                        | General-assistant reasoning + tool-use benchmark                                                                                                                                                   | [S7]   | General-agent capability.                                                                                                      |
| **WebArena**                    | Web-navigation agent benchmark in realistic sites                                                                                                                                                  | [S7]   | Web-agent capability.                                                                                                          |
| **Patronus TRAIL**              | Trace Reasoning and Agentic Issue Localization — can a system find the failing step in an agent trace?                                                                                             | [S3]   | Best system 11% — quantifies how unsolved trace-issue-localization is. Cited as evidence that segment B is _hard_, not _done_. |

**Caveat on benchmarks (flagged § 7.3 [F1]).** A growing 2026 literature argues LLM-simulated
users are unreliable proxies for human users in agentic eval — i.e. even the best benchmarks
in segment E carry a known validity gap. The IEP does not compete here and should not claim a
benchmark.

---

## 3. Per-axis: where the IEP is better / missing / needs improving

The axis set below is the union of what segments A–E actually differentiate on. For each axis:
**better** = IEP has a defensible edge; **missing** = IEP does not do this at all and a
competitor does; **needs improving** = IEP does this but weakly relative to the field.

| Axis                                                                    | Field state (who's strong)                                                                                                                                                                  | IEP position                                                                                                                                                                                                         | Verdict                                                                                                  |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Signed, externally-verifiable verdict (attestation substrate)**       | _Nobody._ Galileo/LangSmith/Patronus produce dashboards + scores; none produce a cosign/Rekor-anchored, replayable Evidence Bundle an external auditor verifies without trusting the vendor | IEP's entire thesis: every validator/gate/judge emits an Evidence Bundle row; `intent-rollout-gate` signs to production Rekor (logIndex 1809941980)                                                                  | **BETTER** (the wedge — § 4)                                                                             |
| **Binary, non-averageable ship/no-ship gate**                           | promptfoo / Braintrust gate on aggregate thresholds; a regression can be averaged out                                                                                                       | IEP gates are binary with sacred-case (`RegressionPack`, Blueprint B § 2.7) regressions that block regardless of mean gain (doc 042 § 3.1)                                                                           | **BETTER**                                                                                               |
| **Replayability of a frozen verdict**                                   | LangSmith/Arize store traces; replay-to-a-declared-fidelity-level is not a contract they sell                                                                                               | IEP: replay levels enumerated _per predicate_ as part of the kernel contract (Blueprint A principle 2; doc 066 replay-fidelity-levels)                                                                               | **BETTER**                                                                                               |
| **Deterministic-first judgment with declared non-determinism boundary** | LLM-judge is the default everywhere; the determinism boundary is rarely declared in the artifact                                                                                            | IEP: deterministic gates first, LLM-judge second, and the boundary is _declared in the emitted row_ (Blueprint A principle 1)                                                                                        | **BETTER**                                                                                               |
| **Agent-trace observability + failure-mode debugging**                  | LangSmith, Arize Phoenix, **Patronus Percival** (20+ failure modes, ~1 hr→~1.5 min)                                                                                                         | IEP emits OTel events (Blueprint B § 4.3) but ships **no** trace-debugging UI, no failure-mode catalog, no annotation queue                                                                                          | **MISSING**                                                                                              |
| **Runtime guardrails (real-time interception)**                         | **Galileo Luna-2** (sub-200 ms, ~$0.02/M), Patronus supervision                                                                                                                             | IEP is an _offline / pre-deployment_ gate; it does not intercept a live agent at runtime                                                                                                                             | **MISSING** (and arguably out of scope per anti-goals — Blueprint A § 3)                                 |
| **Purpose-built cheap eval models**                                     | Galileo Luna-2 SLMs (3B/8B) — 97% monitoring cost cut                                                                                                                                       | IEP has no proprietary eval model; it calls frontier judges at frontier prices (economics → doc 080)                                                                                                                 | **MISSING**                                                                                              |
| **Breadth of unit-under-test**                                          | LangSmith/Arize/Galileo eval _any_ agent/app trace                                                                                                                                          | IEP today evaluates exactly one unit — a `SkillSnapshot` (`skill_name` hardcoded in two places — doc 043 § 3). The `EvalTarget` generalization is proposed, **not built** (doc 043, Class-1 ISEDC + bandwidth-gated) | **NEEDS IMPROVING**                                                                                      |
| **Online / production-traffic eval**                                    | LangSmith online evals on live traces; Galileo production monitoring                                                                                                                        | IEP runs offline against frozen snapshots; no online-eval-on-production-traffic loop                                                                                                                                 | **NEEDS IMPROVING** (partly an anti-goal; partly a real gap for the rollout story)                       |
| **Hosted product + onboarding ergonomics**                              | LangSmith/Braintrust/Galileo are polished hosted SaaS with free tiers                                                                                                                       | IEP is OSS repos + a GitHub Action; no hosted onboarding, no free-tier funnel (bandwidth-gated, not customer-signal-gated — DR-010 § 13.5)                                                                           | **NEEDS IMPROVING** (deliberately deprioritized, but a real adoption-friction gap)                       |
| **Cost attribution + governance**                                       | LangSmith 2026 unified cost view; Galileo cheap-model economics                                                                                                                             | IEP has a NORMATIVE cost-governance doctrine (doc 073 + `CostRecord` glossary § 2.12 + budget enforcement Blueprint B § 4.2) but the signed `cost-attribution/v1` surface is CONDITIONAL (not yet production-signed) | **NEEDS IMPROVING** (doctrine ahead of implementation — the right order, but still a gap until it ships) |
| **CI/PR-gate ergonomics**                                               | promptfoo + Braintrust have mature, low-friction CI integrations                                                                                                                            | IEP `intent-rollout-gate` is dispatch-only / dry-run-default today; production signing path is gated                                                                                                                 | **NEEDS IMPROVING**                                                                                      |

---

## 4. The wedge that survives the comparison

Read down § 3's "better" rows and one pattern holds: **the IEP's edge is the attestation
substrate underneath the verdict, not the verdict-production itself.** Every competitor can
produce a score; some produce better scores (Galileo's purpose-built models) or richer
debugging (Patronus Percival) or a more mature loop (LangSmith). **None of them produce a
cryptographically attestable, replayable, externally-auditable record of _why_ a change was
allowed to ship** — signed to a public transparency log, verifiable without trusting Intent
Solutions. That is the Evidence Bundle convergence thesis, and it is the only axis where the
IEP is not just competitive but categorically different (doc 042 § 6 synthesis points 1–2;
Blueprint A principle 7).

The corollary, stated bluntly so it stays honest: **scoring is commodity, debugging is a
crowded fight the IEP is not equipped to win, and runtime guardrails are out of scope.** The
IEP wins by being the _system of record_ for ship decisions, not the _best scorer_ — the
notary, not the judge.

---

## 5. The honest gaps (don't paper over these)

1. **No trace-debugging product.** Patronus Percival + LangSmith own this; the IEP emits
   telemetry but does not help a human find the failing step. (MISSING.)
2. **No runtime guardrails.** Galileo Luna-2 is a real, well-funded category the IEP does not
   touch — defensibly out of scope, but a buyer comparing "agent reliability platforms" will
   see the absence. (MISSING / anti-goal.)
3. **No cheap proprietary eval model.** The IEP pays frontier-judge prices; Galileo's 97%
   cost edge is real and material for high-volume monitoring (economics → doc 080). (MISSING.)
4. **Single unit-under-test.** Until the `EvalTarget` generalization ships (doc 043), the IEP
   evaluates only skills while competitors evaluate any agent. (NEEDS IMPROVING.)
5. **No hosted product / adoption funnel.** OSS-by-default + bandwidth-gated is the chosen
   posture (DR-010 § 13.5), but it is an adoption gap relative to polished SaaS competitors.
   (NEEDS IMPROVING.)
6. **Cost-attestation not yet signed.** The doctrine (doc 073) is ahead of the
   `cost-attribution/v1` production-signing surface, which is CONDITIONAL. (NEEDS IMPROVING.)

---

## 6. Bridge to the economics companion + the pinpointed lane

The landscape says three things the platform should act on. (a) The crowded segments (scoring,
trace-debugging, runtime guardrails) are not where the IEP wins; the **attestation substrate**
is (§ 4). (b) The competitors that _will_ pressure the IEP economically are the cheap-model
plays (Galileo Luna-2) and the unified-cost-view plays (LangSmith 2026) — which is exactly why
the economics + Cost-Forecast-and-Cap analysis matters; that lives in the companion
[`080`](080-RR-LAND-eval-economics-and-cost-forecast-cap-2026-06-17.md). (c) The lane the IEP
should pinpoint and defend, stated concisely:

> **The signed, replayable, externally-verifiable system-of-record for AI ship decisions —
> the notary for the agent-eval space.** Not the best scorer, not the best debugger, not a
> runtime guard — the layer that turns any score (its own or, via Evidence Bundle ingestion,
> anyone else's) into an auditable, tamper-evident verdict a regulator, partner counsel, or
> future auditor can verify without trusting the vendor. CI-gating is the delivery surface;
> the Evidence Bundle is the moat.

Doc 080 develops the cost dimension of that lane; doc 043 develops the unit-under-test
generalization that widens its addressable surface from skills to all intent-bearing artifacts.

---

## 7. Source register

> Every URL below was surfaced via live search on 2026-06-17. Verification status:
> **verified** = confirmed against a primary/vendor source; **partial** = corroborated via
> secondary sources or single-source vendor claim; **flagged** = see § 7.3. Sources already
> in doc 042's register are cited as `[042 Sx]` and not re-verified here.

### 7.1 Players

- **[S1]** LangSmith — observability + evals platform — <https://www.langchain.com/langsmith-platform> ; evals: <https://www.langchain.com/langsmith/evaluation> ; 2026 unified-cost-view + LangChain 1.0 context: <https://nerova.ai/guides/what-is-langsmith-practical-guide-2026> ; <https://www.digitalapplied.com/blog/agent-observability-2026-evals-traces-cost-guide> — **verified** (vendor pages) + **partial** (2026 feature framing via secondary)
- **[S2]** Arize Phoenix — <https://arize.com/docs/phoenix/evaluation/llm-evals> ; Comet Opik + OSS agent-eval roundup — <https://datatalks.club/blog/open-source-free-ai-agent-evaluation-tools.html> — **verified** (Phoenix docs) + **partial** (Opik via roundup)
- **[S3]** Patronus AI — Percival debugging: <https://docs.patronus.ai/docs/guides/workflows/debugging-agents> ; supervision launch: <https://www.prnewswire.com/news-releases/patronus-ai-unveils-first-scalable-supervision-solution-for-agentic-systems-302455117.html> ; VentureBeat coverage (1 hr→1.5 min, 20+ modes): <https://venturebeat.com/ai/patronus-ai-debuts-percival-to-help-enterprises-monitor-failing-ai-agents-at-scale> ; TRAIL benchmark (best 11%): <https://www.patronus.ai/blog/introducing-trail-a-benchmark-for-agentic-evaluation> — **verified** (vendor + named outlet); efficiency figures **partial** (vendor/early-customer claim)
- **[S4]** Datadog LLM Observability — referenced via the agent-observability roundup <https://www.digitalapplied.com/blog/agent-observability-2026-evals-traces-cost-guide> — **partial** (secondary roundup; representative of the APM-vendor pressure, not a deep profile)
- **[S5]** Galileo — Agent Reliability Platform: <https://galileo.ai/agent-reliability> ; free-platform + Luna-2 + metrics + funding announcement: <https://www.prnewswire.com/news-releases/galileo-announces-free-agent-reliability-platform-302508172.html> ; <https://aithority.com/machine-learning/galileo-announces-free-agent-reliability-platform/> — **verified** (vendor page + PRNewswire); $68M/$45M-Series-B/834%/Fortune-50 figures **partial** (press-release-sourced — see § 7.3 [F2])
- **[S6]** τ-bench / τ²-bench (Sierra Research) — paper: <https://arxiv.org/pdf/2406.12045> ; τ² dual-control: <https://openreview.net/forum?id=LGmO9VvuP5> ; repo: <https://github.com/sierra-research/tau2-bench> — **verified**
- **[S7]** Agentic benchmarks SWE-bench / GAIA / WebArena — surveyed via the OSS agent-eval roundup <https://datatalks.club/blog/open-source-free-ai-agent-evaluation-tools.html> and named in the τ-bench literature [S6] — **partial** (named, not individually deep-profiled; well-established benchmarks)

### 7.2 IEP internal anchors (not external; for cross-reference)

- Blueprint A `011-AT-ARCH` (5-repo taxonomy § 2.1; 12 principles; anti-goals § 3)
- Blueprint B `012-AT-ARCH` (13-entity model; `gate-result/v1` § 7; budget enforcement § 4.2; `*.event` taxonomy § 4.3)
- Canonical glossary `014-DR-GLOS` (Evidence Bundle § 2.4; `CostRecord` § 2.12)
- Companion docs `042` (prompt/context tool landscape), `043` (EvalTarget generalization), `066` (replay-fidelity), `073` (cost governance), `080` (economics companion)
- `intent-rollout-gate` v0.2.0 production Rekor logIndex 1809941980 (CLAUDE.md "Current state" 2026-06-13)

### 7.3 Flagged / could-not-fully-verify

- **[F1] LLM-simulated-user validity gap.** A 2026 arXiv line ("Lost in Simulation," <https://arxiv.org/pdf/2601.17087>) argues simulated users are unreliable proxies in agentic eval. Surfaced in search; cited as a caveat on segment E, not as a settled result. **partial.**
- **[F2] Galileo funding/revenue figures.** $68M total / $45M Series B / 834% revenue growth / six Fortune-50 customers are from the vendor press release and aggregator coverage, not an independent filing. Stated as reported, not as independently verified. **partial.**
- **[F3] Vendor efficiency claims.** Patronus "~1 hr → ~1.5 min" and Galileo "97% cost reduction / sub-200 ms / ~$0.02/M" are vendor / early-customer claims. Repeated as vendor claims, not benchmarked independently here. **partial.**
- **[F4] OpenAI Evals deprecation.** Search surfaced that OpenAI is deprecating the Evals platform (read-only 2026-10-31, shutdown 2026-11-30) and graders. Relevant to segment A/D but adjacent to this doc's agent-eval focus; noted, not load-bearing. Source: OpenAI API docs surfaced via <https://developers.openai.com/api/docs/guides/trace-grading>. **partial** (search-surfaced; verify against primary OpenAI changelog before any public assertion per `feedback_verify_anthropic_docs_before_public_assertion` discipline applied generally).

---

_Research recon, non-normative. Companion to doc 042 (tool landscape) and doc 080 (economics).
Author: Jeremy Longshore (Intent Solutions). 2026-06-17._

## License

Apache 2.0 — see [LICENSE](../LICENSE) at repo root.
