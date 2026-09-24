# 107 · RA · ANLY — Governed Judgment: prior-art survey and proven-method stack

| Field          | Value                                                                                                                                                                                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Date**       | 2026-07-12                                                                                                                                                                                                                                                                    |
| **Author**     | Jeremy Longshore (research pass 2026-07-11; filed 2026-07-12)                                                                                                                                                                                                                 |
| **Status**     | Evidence base — cited analysis. Non-normative. Feeds the design doc `108-AT-ARCH` and the ISEDC ruling `109-AT-DECR`.                                                                                                                                                         |
| **Category**   | RA-ANLY (research / analysis)                                                                                                                                                                                                                                                 |
| **Scope**      | Prior art for a **governed, brain-grounded, measured judgment layer** — the "eval moat" wedge. Establishes that the _integrated_ system is novel whitespace built **entirely from proven, citable parts**, and enumerates the exact method stack to compose (not JRig alone). |
| **Provenance** | Semantic Scholar + web survey, 2026-07-11; competitive-intelligence sweep, 2026-07-12. Citations are recorded as gathered (author · year · venue). This doc is the evidence base the design doc and council cite; it does not itself decide anything.                         |

---

## 0. Why this document exists

The proposed wedge — an agent that judges whether an external event is _worth a human_,
**grounded in a living brain** (the Governed Second Brain: people, places, things, work),
**forward-looking** (hypothesising what the future entails), **serendipity-capturing** (keeping
"nuggets" that could pay off later), and whose judgment **quality is itself measured** — is not an
abstract "is this meaningful" classifier. Jeremy's instinct (2026-07-11) was that this may be new
territory and that **proven methods must be surveyed before any build**. This document is that
survey. Its single most important finding:

> **Every individual capability is well-studied and citable; the integrated system does not exist.**
> The defensible wedge is **judgment governance itself** — cited, hash-chained, measured relevance
> verdicts — which the owned AGP + GSB + IEP stack maps onto 1:1.

The corollary that shapes the whole design: a **single LLM-as-judge (JRig alone) is insufficient**
for the hard, grounded, contextual decisions this system makes. The literature is explicit about
where single judges fail and what composes around them to recover reliability.

---

## 1. The prior-art verdict (Semantic Scholar + web, 2026-07-11)

**Novel whitespace built ENTIRELY from proven parts.** Each area below is a mature, citable
discipline; the contribution is their _integration under governance_, not any single method.

### 1.1 Grounded / faithfulness evaluation — SOLVED, open-source

The question "did the judgment stay grounded in retrieved context, or did it hallucinate?" is
answered by a well-developed toolchain we can compose directly:

- **RAGAS** (Es et al., 2023) — reference-free faithfulness / answer-relevance / context-relevance metrics for RAG.
- **TruLens "RAG Triad"** — context-relevance → groundedness → answer-relevance as three composable checks.
- **HHEM-2.1-Open** (Vectara) — a cheap fine-tuned hallucination/grounding classifier usable as an _independent_ second opinion over (retrieved context → judgment rationale).
- **ARES** — an automated RAG evaluation framework (LLM-judge + lightweight classifiers with statistical guarantees).
- **ALCE** (Gao et al., 2023) — citation **precision / recall**: does the answer actually cite the sources it used, and are those citations correct? Directly transferable to "the judgment must cite the brain nuggets it relied on."

**Implication:** groundedness and citation-accuracy are _measurable today_ with open tools. Requiring
the agent to cite the `qmd://` brain nuggets it used, then scoring ALCE-style precision/recall + a
faithfulness metric + an independent HHEM classifier, catches the "confident but hallucinated"
judgment — the exact failure mode governance exists to prevent.

### 1.2 LLM-as-judge — SOLVED on easy tasks, OPEN on hard ones (Jeremy's doubt is correct)

- **MT-Bench / Chatbot Arena** (Zheng et al., 2023) — LLM judges reach **~80% agreement with humans** on _easy_ pairwise/scoring tasks. This is the optimistic headline.
- **ContextualJudgeBench** (Xu et al., 2025) — on **hard, grounded, contextual** decisions, the best judges top out at **~55% accuracy**. **This is exactly our regime**: contextual, grounded, high-stakes act/don't-act calls. A single big judge is not reliable here.
- **Mitigations, all citable:**
  - **Panel-of-LLM-judges (PoLL)** (Verga et al., 2024) — a panel of **disjoint-family** smaller jurors _beats_ one large judge and is **~7× cheaper**; also reduces intra-family self-preference bias.
  - **Pairwise + position-swap** — swap the order of candidates to cancel position bias.
  - **Rubric- and reference-guided grading** — **Prometheus** (Kim et al., 2024) shows fine-grained rubric-guided evaluation tracks human judgment far better than free-form scoring.
  - **JudgeBench / G-Eval** — establish the calibration and chain-of-thought-scoring baselines the panel is measured against.

**Implication:** the grader must be a **PoLL panel** (disjoint-family, rubric+reference-guided,
position-swapped), **validated against a human golden set before it is trusted**, with **JRig as the
binary SHIP/BLOCK gate on top** — not the whole measurement.

### 1.3 Decision evaluation (act / don't-act) — SOLVED

Treat "act vs don't-act" as a classification problem with the standard, defensible apparatus:

- **Precision / recall / F1 per class** — false-alarm rate and miss rate are first-class, separately reportable.
- **τ-bench pass^k** (Yao et al., 2024) — measures _consistency_ across k repetitions, catching judges that are right on average but unstable per-call.
- **Inter-annotator agreement first** — measure **Cohen's κ / Krippendorff's α** on the human golden set _before_ trusting any automated judge. A judge cannot be more reliable than the labels validating it.

### 1.4 Serendipity — FORMALIZED (but not for deferred value)

- Serendipity in recommender systems is formalized as **relevance + novelty + unexpectedness + value** (Silveira et al., 2017; Kotkov et al., surveys).
- **"Value" is the least-formalized axis**, and recsys treats it as _immediate_ value. **Our delta:** _deferred_ value — "keep this nugget; the loop tells you later whether it paid off." That deferred-value framing is under-occupied territory.

### 1.5 Forward-looking / weak-signal detection — a whole DISCIPLINE

- **Weak-signal theory** (Ansoff, 1975) — acting on faint early indicators before they are unambiguous.
- **Keyword-emergence / issue maps** (Yoon, 2012) — detecting emerging topics from term dynamics.
- **BERTopic / WISDOM** (Ebadi et al., 2024) — modern topic-emergence and weak-signal mining over corpora.
- **Anticipatory agents (ProAct-style)** — proactive rather than reactive agent framings.

**Our delta:** these operate on **trend corpora**, not a **personal event stream** grounded in one
operator's brain. Transferring weak-signal detection to a _personal_ forward-looking judgment is open.

### 1.6 Memory-worthiness — ADAPT from RL, transfer is unpublished

- **Surprise-novelty** signals (Le et al., 2023), **value-of-information (VOI)**, and **intrinsic-motivation** rewards decide "what is worth retaining" for game/RL agents.
- **Our delta:** transferring these to "retain this for an **unknown future personal payoff**" is non-trivial and, as far as the survey found, **unpublished**.

### 1.7 Scoring forward-looking judgment — SOLVED (the answer to "how do you grade 'will matter later'")

This is the pivotal methodological finding. You _can_ grade a judgment about the future:

- Log each "beneficial-later" call as a **dated probabilistic prediction with a resolution horizon**.
- Resolve it when the horizon arrives.
- Score with **Brier score / calibration** (Tetlock's forecasting work; Kleinberg et al., 2023 "U-Calibration" — calibration for forecasts whose downstream _consumer utility is unknown_, which is exactly our case).

**Implication:** the forward-looking layer is a **delayed, deferred eval loop** — structurally
distinct from JRig's instant pass/fail — and it is grounded in established forecasting science, not
hand-waving.

---

## 2. The integrated system is unoccupied (competitive read)

**Closest existing systems, and precisely what each lacks:**

| System                                                                                          | What it is                                                                                                                    | What it does NOT do (our wedge)                                                                                                                                    |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Glean** ($7.2B val / ~$300M ARR)                                                              | Governed company brain + cited agents; enterprise search; markets "Build, Govern, AND Measure agents" (May-2026 ADLC roadmap) | No per-tool-call HITL, no signed journal, no harness-neutrality; a groundedness _evaluator_ but not a **self-improving judgment loop**; not external-signal triage |
| **Khoj**                                                                                        | Agentic personal brain                                                                                                        | No governance, no measurement                                                                                                                                      |
| **Notion / Dust** ($40M)                                                                        | Enterprise brains acting grounded w/ access control                                                                           | Do not cite + measure + self-improve the _judgment_                                                                                                                |
| **Fiddler** (~$100M raised)                                                                     | "Neutral control plane: policy + audit + evaluation" — nearest architecture neighbor                                          | One release from grounded-judgment _scoring_; no cross-harness brain-grounding                                                                                     |
| Academic governed-knowledge clusters (EMA2 2025; AGL-1 / GKS-5 2026; Collaborative Memory 2025) | Mirror AGP's kernel — govern **access / retrieval**                                                                           | Do **not** govern the **judgment** (the cited, measured verdict)                                                                                                   |

**Security-adjacent consolidation already happened** (validating the category's value): Lakera →
Check Point, Protect AI → Palo Alto, Robust Intelligence → Cisco, Invariant → Snyk, Promptfoo →
OpenAI.

**Verdict:** nobody owns all three axes of our intersection — **① govern actions · ② ground + cite
judgment · ③ measure + self-improve judgment.** That triple intersection is the defensible wedge.
**Primary risk:** Glean or Fiddler (both 2/3 today) shipping the third axis first.

---

## 3. The proven method stack to COMPOSE (not JRig alone)

For "did the agent judge correctly AND stay grounded in the brain, not hallucinate":

1. **Correctness** — a hand-curated **golden set** (≥2 annotators; report **κ / α**), scored by
   precision / recall / F1 + **pass^k** consistency.
2. **Groundedness** — **RAGAS-faithfulness** or **TruLens-groundedness** + **HHEM** as an
   independent cheap classifier over (retrieved brain context → judgment rationale); require the
   agent to **cite the `qmd://` brain nuggets** it used and score **ALCE-style citation
   precision / recall**.
3. **The grader** — a **PoLL panel** of **disjoint-family** judges (free **Groq** + **NVIDIA NIM** +
   **DeepSeek**), **rubric + reference-guided**, **position-swapped** — **validated against the human
   golden set before it is trusted**. **JRig is the binary SHIP/BLOCK gate on top**, not the whole
   measurement.
4. **Forward-looking** — log "beneficial-later" calls as **dated forecasts**; score by
   **Brier / U-calibration** at the resolution horizon (a **delayed** eval loop, distinct from
   JRig's instant pass/fail).

Every element is open-source or already owned. Technical risk is **low** — this is hardening +
integration of proven parts, not invention.

---

## 4. Runway and market timing (competitive-intelligence sweep, 2026-07-12)

Three parallel CI streams (incumbents/platform; eval + governance layer; memory/brain layer) **all
independently converged on a ~12–18 month runway** before a 2/3 player ships 3/3 and closes the
whitespace.

- **The market = three "one-half companies."** Eval vendors (Arize $1B+, Braintrust ~$800M val,
  LangSmith ~$1.25B val, Galileo, Patronus ~$50M) **measure text/traces**, do not gate actions or
  sign audit. Control planes (Fiddler; NVIDIA **NeMo Guardrails** OSS; OpenAI **AgentKit**)
  **gate + audit**, do not score decision groundedness. Enterprise brains (Glean, Dust, Notion)
  **act grounded in a brain w/ access control**, do not cite + measure + self-improve the judgment.
- **Model labs commoditise the GATE half for free** (OpenAI AgentKit guardrails + HITL + evals;
  Anthropic PreToolUse / PostToolUse hooks). This **raises our floor and validates the category** but
  the labs will not build **cross-harness, brain-grounded judgment** (it would help rivals' models).
- **The one-line verdict (recorded verbatim from the sweep):** _"the moat is the judgment-grounding
  loop, not the governance plumbing."_ **Defend the LOOP, not the gate.**
- **The accelerant — EU AI Act full enforcement ~Aug 2, 2026 (~7 months):** requires lineage-backed
  auditability + reasoning-trace provenance for high-risk AI = exactly compile → govern → retrieve +
  hash-chained receipts + `qmd://` citations. A tailwind **and** a runway-compressor (it pushes
  incumbents toward our direction).

**OSS to compose (do not rebuild):** RAGAS, TruLens, **DeepEval**, **Inspect (UK AISI — assurance-grade;
track it)**, NeMo Guardrails, **Graphiti** (provenance model), **Mem0 / Letta**, **Khoj**, **GraphRAG**.

**The Governed-Judgment CI method (repeatable — run quarterly or on a major funding/launch event, via
`/product-researcher` + this rubric):**

1. **3-axis intersection test** — score every player on ① govern actions ② ground + cite judgment
   ③ measure + self-improve judgment → **3/3 = direct competitor** (none today), **2/3 = adjacent
   threat**, **≤1 = compose / ignore**.
2. **Layer taxonomy scan** — eval · control-plane · enterprise/personal-brain · memory-infra; new
   entrants appear in one layer and expand toward the centre.
3. **Moat checklist** — we must own **≥4** (see §5).
4. **Leading indicators** — Fiddler releases · Inspect agent-assurance · Glean "measure" depth ·
   OpenAI/Anthropic SDK moves · EU AI Act milestones.
5. **Runway model** — whitespace closes when a 2/3 player **ships** 3/3; nearest are Glean / Fiddler;
   ~12–18 months, compressing toward Aug 2026.

---

## 5. Our defensible moat (competitors own ≤2; we must own ≥4)

1. **Harness-agnostic** — competitors are locked to their own cloud/harness.
2. **OSS / Apache-2.0** — competitors are closed SaaS. _(This is why build-in-public is on-thesis, not a leak — see `108-AT-ARCH` §Positioning.)_
3. **Signed, hash-chained audit of every tool call** — competitors have logs, not receipts.
4. **The grounded-judgment SELF-IMPROVING loop (the Circle of Life)** — on nobody's roadmap.
5. **Anthropic-partner posture** — complement, not competitor (matters for the Enterprise program).
6. **EU AI Act fit** — lineage + provenance are the regulation's exact asks.

---

## 6. Citation ledger (as gathered — for the design doc + council to cite)

Grouped by method area. Entries are recorded as the survey captured them (author · year · venue/tool).
This ledger is the shared reference substrate; the design doc `108-AT-ARCH` cites into it.

- **Grounded / faithfulness eval:** RAGAS (Es et al., 2023) · TruLens RAG-Triad · HHEM-2.1-Open (Vectara) · ARES · ALCE citation precision/recall (Gao et al., 2023).
- **LLM-as-judge:** MT-Bench / Chatbot Arena (Zheng et al., 2023) · **ContextualJudgeBench (Xu et al., 2025)** · Panel-of-LLM-judges / PoLL (Verga et al., 2024) · Prometheus (Kim et al., 2024) · G-Eval · JudgeBench.
- **Decision / consistency eval:** precision/recall/F1 per class · τ-bench pass^k (Yao et al., 2024) · Cohen's κ / Krippendorff's α (inter-annotator agreement).
- **Serendipity:** Silveira et al., 2017 · Kotkov et al. (surveys) — relevance + novelty + unexpectedness + value.
- **Weak-signal / forward-looking:** Ansoff, 1975 · Yoon, 2012 · BERTopic / WISDOM (Ebadi et al., 2024) · anticipatory/ProAct agent framings.
- **Memory-worthiness:** surprise-novelty (Le et al., 2023) · value-of-information · intrinsic motivation.
- **Scoring forward-looking judgment:** Tetlock (forecasting/Brier) · U-Calibration (Kleinberg et al., 2023).
- **Competitors / systems:** Glean · Khoj · Notion · Dust · Fiddler · Arize · Braintrust · LangSmith · Galileo · Patronus · NeMo Guardrails · OpenAI AgentKit · Inspect (UK AISI).
- **Academic governed-knowledge:** EMA2 (2025) · AGL-1 / GKS-5 (2026) · Collaborative Memory (2025).
- **OSS to compose:** RAGAS · TruLens · DeepEval · Inspect · NeMo Guardrails · Graphiti · Mem0 / Letta · Khoj · GraphRAG.

> **Integrity note.** These are recorded by name · year · venue from the 2026-07-11 research pass. Any
> downstream artifact that _quotes a specific result, table, or number_ from one of these works should
> re-verify it against the primary source before publication (especially anything reaching the paper
> or the public Evidence-Bench scorecard). This ledger fixes _which_ works are load-bearing; it is not
> a substitute for reading them.

---

## 7. What this establishes for the design + the council

1. **The wedge is real and buildable from proven parts** — low technical risk; the novelty is the
   _integration under governance_, which is citable-novel (product **and** paper territory).
2. **JRig alone is insufficient** — the grader must be a composed stack (PoLL panel + groundedness +
   citation + a κ-validated golden set), with JRig as the binary gate. This is a design constraint,
   not a preference.
3. **Forward-looking judgment is gradable** — via dated forecasts + Brier/U-calibration; Layer 2 is
   scientifically grounded, not speculative.
4. **The moat is the loop, not the gate** — the gate is commoditising (labs ship it free); the
   self-improving grounded-judgment loop (Circle of Life) is on nobody's roadmap.
5. **The window is ~12–18 months, compressing toward the EU AI Act (Aug 2026)** — the design/council
   phase should be _fast and moat-centred_, per Jeremy's "research-deep, then fast-build" north star.

---

_Filed under Document Filing Standard v4.4. Non-normative evidence base. Feeds `108-AT-ARCH-governed-judgment-layer` and `109-AT-DECR`. Bead: `iel-25a.1` (epic `iel-25a`)._
