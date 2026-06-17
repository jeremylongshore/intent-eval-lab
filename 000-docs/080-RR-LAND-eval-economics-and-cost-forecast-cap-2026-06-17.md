---
title: Eval Economics and the Cost-Forecast-and-Cap mechanism — token/context economics of a long-running agentic eval, Team vs Enterprise, subagent/context-fork accounting, and the up-front budget-cap feasibility
date: 2026-06-17
authors:
  - Jeremy Longshore (Intent Solutions)
status: RESEARCH (non-normative)
state_label: RESEARCH
filing_standard: Document Filing Standard v4.3
epic: bd_000-projects-qm77 (IEP competitive-lane + cost/budget strategy questions)
bead: bd_000-projects-qm77.2
relates_to:
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — § 4.1 execution ceilings incl. token_ceiling, § 4.2 budget enforcement, § 2.12 CostRecord)
  - 014-DR-GLOS-canonical-glossary.md (canonical glossary — CostRecord, RuntimeReceipt, replay)
companion:
  - 073-AT-STND-economics-and-cost-governance-2026-06-18.md (the NORMATIVE in-platform anchor — CostRecord, budget enforcement, three breach behaviors)
  - 079-RR-LAND-competitive-landscape-agent-eval-2026-06-17.md (the competitive-landscape companion under the same epic; § 4 names the wedge this doc prices)
  - 042-RR-LAND-prompt-and-context-eval-landscape-2026-06-06.md (prompt/context eval tool landscape)
verification: every external claim carries a live source URL in § 6; verification status (verified / partial / flagged) recorded per source. Live search 2026-06-17. Pricing is point-in-time (2026-06) and will drift — treat figures as illustrative orders of magnitude, not contractual.
---

> **Scope.** Three parts, exactly per bead `bd_000-projects-qm77.2`:
> **(1) Token/context economics** — what a long-running agentic eval task reasonably costs for
> a small-to-medium org via the API, compared on the **Claude Team** vs **Enterprise** plan,
> accounting for subagents and context-forking (§ 1–3).
> **(2) Cost-Forecast-and-Cap feasibility** — is an up-front token-budget estimate + per-
> subagent context accounting + hard-ceiling enforcement possible, and if so, the mechanism
> shape, anchored to the in-platform `CostRecord` (doc 073) + Blueprint B § 4.2 budget
> enforcement (§ 4).
> **(3) The pinpointed lane** — one concise paragraph (§ 5).
>
> **Non-normative.** This doc prices and reasons; the binding doctrine is doc
> [`073`](073-AT-STND-economics-and-cost-governance-2026-06-18.md). On any conflict, **073
> wins** for governance and **Blueprint B § 2.12 wins** for the `CostRecord` schema. All IEP
> terms are defined in the canonical glossary [`014`](014-DR-GLOS-canonical-glossary.md).
>
> **Citation + figure discipline (same as doc 042).** Every external figure carries a live
> source URL in § 6 with a verification status. **Pricing is point-in-time (2026-06)** and
> drifts fast (Anthropic changed Enterprise token bundling in 2026 — § 6 [S3]); figures are
> illustrative orders of magnitude, not quotes.

---

## 0. How to read this document

§ 1 establishes the per-token cost basis (2026 Anthropic API rates). § 2 builds a worked
"long-running agentic eval" cost model with the subagent/context-fork multiplier. § 3 compares
the **Team vs Enterprise** plan economics for an SMB. § 4 answers the Cost-Forecast-and-Cap
feasibility question and gives the mechanism shape. § 5 pinpoints the lane. § 6 is the source
register.

---

## 1. The cost basis (2026 Anthropic API rates, point-in-time)

Per-million-token API pricing as surfaced 2026-06 [S1]:

| Model | Input ($/M) | Output ($/M) | Notes |
| --- | --- | --- | --- |
| **Opus 4.8** (flagship) | $5.00 | $25.00 | 1M-token context at flat rate, no surcharge |
| **Sonnet 4.6** | $3.00 | $15.00 | 1M-token context at flat rate |
| **Haiku 4.5** | $1.00 | $5.00 | the cheap eval/judge tier |

Two cost levers materially change the math and are load-bearing for any forecast [S1]:

- **Prompt caching** cuts cached-input cost by **~90%**. For an eval harness that re-sends a
  large fixed context (the skill body, the eval rubric, fixtures) across many runs, this is
  the single biggest lever.
- **Batch processing** is **~50% cheaper** across all models. Offline eval is the canonical
  batchable workload — a regression suite run nightly is a batch job, not interactive traffic.

Output is **5× input** across all current models [S1] — so an eval that asks a judge for long
free-text rationales is dramatically more expensive than one that asks for a binary verdict +
short reason. This directly rewards the IEP's **binary, deterministic-first** posture
(Blueprint A principle 1; doc 079 § 3): a short structured verdict is cheaper to produce _and_
cheaper to attest.

---

## 2. What a long-running agentic eval reasonably costs (worked model)

A "long-running agentic eval task" in IEP terms = one `EvalRun` (glossary § 2.2) that drives a
skill through trigger / functional / regression / adversarial / baseline layers (j-rig L2),
each layer possibly spawning a **subagent** with its **own context window**, then a judge layer
(L4) scoring outputs. The cost is the sum of all model calls across all subagents, not just the
root agent's tokens.

**The subagent / context-fork multiplier (the part the bead specifically asks about).** Per
Anthropic's Agent SDK [S2]:

- A **subagent** runs in its **own context window** and returns only a clean summary — so its
  token cost is _additive_ but its context does **not** bloat the parent. N parallel subagents
  ≈ N independent context budgets (good for isolation, but you pay for each).
- A **fork** is a subagent that **inherits the entire conversation so far** — same system
  prompt, tools, model, **and full message history**. A fork therefore **re-pays the input cost
  of the whole accumulated context** at fork time. Forking 5 ways from a 100k-token point =
  ~500k input tokens just to seed the forks, _before_ any new work.
- When accumulated subagent results approach the window limit, the SDK **auto-compresses**
  history — which is itself a model call (cost) and a fidelity decision (replay implication).

**Illustrative single-run cost (orders of magnitude, not a quote).** Take a moderately complex
eval: ~50k input tokens of fixed context (cached after first call), 5 subagents each doing
~20k input / ~5k output of work, a judge pass of ~30k input / ~3k output on Sonnet 4.6:

| Component | Tokens | Rate (Sonnet 4.6, [S1]) | ~Cost |
| --- | --- | --- | --- |
| Fixed context, first call (uncached) | 50k in | $3.00/M | $0.15 |
| Fixed context, re-sent ×5 subagents (cached, 90% off) | 250k in | $0.30/M eff. | $0.075 |
| Subagent work | 100k in / 25k out | $3 / $15 | $0.675 |
| Judge pass | 30k in / 3k out | $3 / $15 | $0.135 |
| **Per-run total (Sonnet, cached, interactive)** | | | **~$1.11** |
| Same run on **Opus 4.8** (no cache, no batch) | | | **~$3–5** |
| Same run **batched + cached on Sonnet** (~50% off non-cached) | | | **~$0.60** |

So a single agentic eval run is **cents to a few dollars**. The cost problem is **not** one run
— it is **volume × forking**. A regression suite of 200 cases, each forking 5 ways, run on Opus
without caching, is the difference between ~$120 (cached/batched/Sonnet) and ~$5,000+
(uncached/forked/Opus). **The forecast must price the fork fan-out, not the per-call rate** —
that is the entire feasibility insight for § 4. (Flagged § 6.3 [F1]: these are modeled
illustrative numbers, not measured; a real forecast calibrates against logged `CostRecord`
rows.)

---

## 3. Team vs Enterprise — the SMB economics

The bead asks specifically what this "looks like on the Claude Team plan vs Enterprise." The
key 2026 fact: **plan seats do not meaningfully subsidize API/eval token spend** — eval cost is
metered token cost either way [S3].

| Dimension | **Team** | **Enterprise** |
| --- | --- | --- |
| Seat price | ~$25/seat/mo monthly, ~$20 annual (Standard); Premium ~$125/$100; **min 5 members** [S3] | Custom, ~$20/seat/mo starting, API billed separately [S3] |
| Context window | 200K [S3] | 500K [S3] |
| Bundled tokens | minimal/none for programmatic eval | **none** — Anthropic **removed bundled tokens** from Enterprise seat deals (renewals from Nov 2025, default for new agreements by Feb 2026) [S3] |
| Governance | basic | SSO, SCIM, RBAC, audit logging, HIPAA-readiness, higher limits [S3] |
| Eval-token billing | standard API rates (separate) | standard API rates (separate) [S3] |

**The SMB takeaway.** For a small-to-medium org running an eval _harness_ (programmatic, via
the API), **the plan tier barely changes the eval bill** — you pay metered API token rates (§ 1)
on either plan; Enterprise's value is governance (SSO/audit/RBAC) and the bigger window, not
cheaper evals. An SMB should: (a) stay on **Team** unless it needs the Enterprise governance
controls; (b) drive eval cost down with **caching + batching + cheap-judge (Haiku) for the
deterministic-first layers, reserving Opus for adversarial/baseline only**; (c) treat the eval
budget as a **token budget**, not a seat decision. This is exactly the lever doc 073 § 5 frames
as bandwidth-vs-budget, and it is where Galileo's cheap-eval-model play (doc 079 § 3 MISSING
row) bites: a 97%-cheaper guard model changes high-volume monitoring economics in a way the
IEP's frontier-judge posture does not (yet) match.

---

## 4. Cost-Forecast-and-Cap — is it possible, and what shape?

**The bead's question: "do we have a budget mechanism that takes a long-shot task and
calculates the cost up front — is that impossible?"** Short answer: **not impossible, and the
in-platform primitives already exist.** It decomposes into three sub-mechanisms, each with an
existing anchor.

### 4.1 Up-front token-budget estimation (the forecast)

**Feasible, with a known error bar.** A forecast is a function of (a) the fixed-context size
(known: skill body + rubric + fixtures are measurable before the run), (b) the per-layer
expected fan-out (the eval plan declares how many cases × how many subagents/forks), and (c) a
per-layer token-per-call estimate **calibrated from historical `CostRecord` rows** (glossary
§ 2.12; doc 073 R2 attribution dimensions give exactly the per-judge / per-provider / per-run
breakdown a calibrator needs). The forecast is therefore: `Σ over layers (cases × fan-out ×
calibrated_tokens_per_call × rate)`, with the **fork multiplier from § 2** applied (a fork
re-pays accumulated context). The honest limitation: agentic runs have variable-length
trajectories, so the estimate is a **distribution, not a point** — forecast a P50 and a P95, and
cap against the P95. (This is why "impossible" is wrong but "exact" is also wrong.)

### 4.2 Per-subagent context accounting (the meter)

**Already specified.** Blueprint B § 4.1 fixes per-`EvalSpec` execution ceilings including a
**`token_ceiling`** (default 50,000; per-platform hard cap 10,000,000). `ToolInvocation` +
`CostRecord` rows carry **leaf-level attribution** (doc 073 R2; glossary § 2.11/2.12) — i.e.
each subagent's spend is already an attributable leaf row, and the `RuntimeReceipt` (glossary
§ 2.6) summarizes the run total at terminal-state transition. The accounting substrate for
"per-subagent context cost" exists; it needs the forecaster to _consume_ it, not new schema.

### 4.3 Hard-ceiling enforcement (the cap)

**Already specified as doctrine.** Doc 073 R7–R9 + Blueprint B § 4.2 fix budget enforcement at
the **runtime boundary** with a **closed set of exactly three breach behaviors** [doc 073 R8]:

| Behavior | Effect | For Cost-Forecast-and-Cap |
| --- | --- | --- |
| `hard_stop` | runtime refuses the spend; `EvalRun` → terminal `archived_failed` with budget-breach reason | the literal "cap" — the long-shot task cannot exceed its forecast ceiling |
| `require_human_ack` | pause + HR-5 human-review trigger; a budget owner must ack before resuming | the "this is going long, approve the overage?" path for a genuinely open-ended task |
| `advisory` | proceed + record a budget-advisory event | tripwire mode for exploration |

A policy that names no behavior **defaults to `hard_stop`** (doc 073 R8 — "do not spend money
you did not budget"). So the **cap half of Cost-Forecast-and-Cap is built doctrine**, enforced
at the runtime boundary, with `token_ceiling` as the concrete knob.

### 4.4 What is actually missing (the honest gap)

The **enforcement** (cap) is specified; the **forecast** (the up-front estimator that turns an
eval plan into a P50/P95 token budget _before_ the run) is **not yet a built component**. It is
feasible (the calibration data is in `CostRecord`), it is the natural next layer above § 4.1–4.3,
and it is **bandwidth-gated, not signal-gated** (DR-010 § 13.5; doc 073 R11). It is also a
**Class-2-ish** addition (a new runtime estimator consuming existing entities, not a new
canonical entity) — so it does not require a kernel-schema ISEDC change the way doc 043's
`EvalTarget` does. **Verdict: not impossible — the cap exists, the meter exists, the calibration
data exists; only the forecaster is unbuilt, and it is a tractable bandwidth-gated build.**

> **Anti-pattern to avoid (from doc 073 § 6):** do not encode a budget threshold in a predicate
> URI (R7 — "budget is policy, not predicate"), and do not invent a fourth breach behavior
> (R8). The forecaster proposes a number; the policy chooses one of the three behaviors; the
> predicate stays budget-agnostic.

---

## 5. The pinpointed lane (concise)

> **The IEP's lane is the signed, replayable system-of-record for AI ship decisions — and its
> economic edge inside that lane is _attestable cost-governance_, not cheap scoring.** The
> crowded fights (cheap eval models à la Galileo Luna-2, trace-debugging à la Patronus Percival,
> unified observability à la LangSmith) are not where the IEP wins (doc 079 § 4). Where it wins
> is: an SMB can forecast an eval's cost up front against historical `CostRecord` data, cap it
> with a `hard_stop` at the runtime boundary, run it cheaply (cache + batch + Haiku-first), and
> walk away with a **signed, externally-verifiable Evidence Bundle** proving both the verdict
> _and_ what it cost to reach — a tamper-evident `cost-attribution/v1` record no dashboard
> competitor produces. The lane is "**the auditable budget-and-verdict notary for agent
> evaluation**," delivered as a CI gate, moated by signed evidence, priced for the bandwidth-
> gated solo/SMB reality — not the best scorer, the most _accountable_ one.

---

## 6. Source register

> URLs surfaced via live search 2026-06-17. **Pricing is point-in-time and will drift.**
> verified = primary/vendor source; partial = secondary/aggregator; flagged = § 6.3.

### 6.1 Pricing + plans + agent mechanics

- **[S1]** Anthropic Claude API pricing 2026 (Opus 4.8 $5/$25; Sonnet 4.6 $3/$15; Haiku 4.5 $1/$5; output 5× input; caching ~90% off cached input; batch ~50% off; 1M context flat) — <https://www.cloudzero.com/blog/claude-api-pricing/> ; <https://www.finout.io/blog/anthropic-api-pricing> — **partial** (aggregator pages; cross-corroborated across multiple 2026 guides — verify against the official Anthropic pricing page before any public assertion per the verify-before-public-assertion discipline)
- **[S2]** Anthropic Agent SDK — subagents (own context window, return clean summary) + fork (inherits full conversation/history) + auto-compression at window limit — <https://platform.claude.com/docs/en/agent-sdk/subagents> ; secondary explainer: <https://www.ksred.com/the-claude-agent-sdk-what-it-is-and-why-its-worth-understanding/> — **verified** (primary SDK docs) + **partial** (fork-cost framing via secondary)
- **[S3]** Claude Team vs Enterprise pricing 2026 (Team ~$25/$20 Standard, ~$125/$100 Premium, min 5; Enterprise custom ~$20/seat, API separate; 200K vs 500K window; SSO/SCIM/RBAC/audit/HIPAA; **bundled tokens removed from Enterprise** — renewals Nov 2025, default by Feb 2026) — <https://www.finout.io/blog/claude-pricing-in-2026-for-individuals-organizations-and-developers> ; <https://runbear.io/posts/claude-enterprise-pricing-mid-market> ; <https://redresscompliance.com/anthropic-claude-pricing-2026.html> — **partial** (aggregator; the bundled-token-removal claim is attributed to The Register reporting via these secondaries — verify against primary before public assertion)

### 6.2 IEP internal anchors (not external)

- Doc 073 `073-AT-STND` — NORMATIVE cost governance: R1–R2 CostRecord + attribution dimensions, R7–R9 budget enforcement + three breach behaviors, R10–R11 bandwidth ceiling, § 6 anti-patterns
- Blueprint B `012-AT-ARCH` — § 4.1 execution ceilings (`token_ceiling` default 50k / hard cap 10M), § 4.2 budget enforcement, § 2.12 CostRecord schema authority
- Canonical glossary `014-DR-GLOS` — CostRecord § 2.12, RuntimeReceipt § 2.6, ToolInvocation § 2.11, replay § 3
- Companion docs `079` (competitive landscape — § 4 wedge, § 3 Galileo cheap-model gap), `042` (tool landscape), `043` (EvalTarget generalization)
- DR-010 § 13.5 (bandwidth-gated not customer-signal-gated)

### 6.3 Flagged / could-not-fully-verify

- **[F1] The worked cost model (§ 2 table).** Token counts and per-run dollar figures are
  **modeled illustrative orders of magnitude**, not measured runs. A production forecast must
  calibrate against logged `CostRecord` rows (§ 4.1). Stated as illustrative, not as a quote.
- **[F2] Pricing volatility.** All 2026 pricing/plan figures are point-in-time and sourced from
  aggregator guides; Anthropic changed Enterprise token bundling within 2026 [S3], proving the
  figures drift. Treat § 1 and § 3 as a snapshot to re-confirm against the primary Anthropic
  pricing/plans pages before any public/customer-facing use.
- **[F3] "Bundled tokens removed from Enterprise."** Attributed to The Register reporting via
  secondary aggregators; the timing (renewals Nov 2025, default Feb 2026) is secondary-sourced.
  Material to the Team-vs-Enterprise conclusion, so flagged for primary re-verification.

---

_Research recon, non-normative. Companion to doc 079 (competitive landscape) and doc 073
(NORMATIVE cost governance). Author: Jeremy Longshore (Intent Solutions). 2026-06-17._

## License

Apache 2.0 — see [LICENSE](../LICENSE) at repo root.
