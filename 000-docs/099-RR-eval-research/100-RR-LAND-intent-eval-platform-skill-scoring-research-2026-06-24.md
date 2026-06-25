# RR-LAND — Skill-scoring research: `meta_skill` + the 13-tool eval landscape vs. what IEP already owns

**Filing:** `099-RR-eval-research/100-RR-LAND-...` (coded research cluster, Doc Filing Standard v4.4 §3.1)
**Date:** 2026-06-24
**Status:** Research / landscape (RR-LAND). Non-normative. Input to a possible scoring-layer epic; not a binding spec.
**Companion:** `101-RR-BIBL-skill-scoring-tool-references-2026-06-24.md` (every source cited here).
**Evidence basis:** 3 Explore-agent sweeps (meta_skill source cloned to `/tmp/meta_skill`; 13-tool survey via repo + docs fetch; IEP inventory against live repo paths). Raw per-tool breakdown persisted at the session tool-result `toolu_01WwXuuf5KucopK3aVgYmp9b.json`.

---

## 0. The one-paragraph answer

`meta_skill` (Jeffrey Emanuel's `Dicklesworthstone/meta_skill`, a local-first Rust+SQLite skill-manager) and the broader 13-tool eval landscape are worth studying, but this is a **gap analysis, not a greenfield design**. The Intent Eval Platform already owns the hard parts — a 14-entity contracts kernel, binary-criteria behavioral eval, deterministic gates, signed Evidence Bundles, a verify-before-render dashboard, and a 10-dimension SKILL.md grader. Measured against `meta_skill`, IEP is **missing exactly two things**: (a) a **usage → feedback → bandit loop** (a learned "which skill actually helped" signal), and (b) **slice-level utility** (scoring per block — policy/rule/example — not just per skill). Two softer adjacents are also absent: hybrid BM25+semantic catalog search, and a single rolled "quality+usefulness+feedback" score (which collides with the dashboard's hard C3 no-aggregate-PASS binding and should probably stay un-rolled). Everything else the brief asked us to "propose" already exists at a known path. **Recommendation: extend the kernel + j-rig + dashboard with a feedback/usage entity and a catalog-search layer — do NOT fork a new tool.**

A blunt caveat that shapes the whole report: **`meta_skill` does not actually compute "usefulness."** Its headline "utility" number is a hand-assigned `const fn` keyed on slice type (§2). The one genuinely-computed score it has is `quality` (§3A), and the one genuinely-learned signal is its feedback→bandit reward map (§3C) — and that learned loop is precisely gap (a).

---

## 1. What `meta_skill` actually is (verified from source, not marketing)

| Aspect | Finding | Evidence |
|---|---|---|
| Identity | `Dicklesworthstone/meta_skill`; CLI binary `ms`. A **local-first Rust CLI + SQLite** skill-management platform — the author's primary tool to grade/rank/score/search/manage AI skills. **No separate web-app repo.** | repo `github.com/Dicklesworthstone/meta_skill`; `Cargo.toml` |
| Language / DB | **Rust (Edition 2024, 1.85+)**, **SQLite + FTS5** (`fsqlite`), full-text via **Tantivy 0.26**, embeddings via **deterministic FNV-1a hash, 384-dim** (no external model), CLI **Clap 4.5**, TUI Ratatui. | `Cargo.toml` |
| Storage model | **Dual persistence** — SQLite (fast queries, FTS, metadata filter) + Git (immutable history, diffs, audit). Neither privileged: corrupt SQLite → rebuild from Git; no Git → DB still works. | `README.md:87-96` |
| Surface | **57 CLI commands** across Metadata/Discovery, Quality/Mgmt, Content/Slicing, Indexing/Sync, Graph/Deps, Advanced. | `src/cli/commands/` |
| MCP | `ms mcp serve` (stdio / `--port`), protocol `2024-11-05`, exposes **6 tools** (`search`, `load`, `evidence`, `list`, `show`, `doctor`). | `src/cli/commands/mcp.rs:1-39` |
| Design DNA | deterministic embeddings (reproducible), RRF rank-fusion search, Thompson-sampling bandit for recommendations, multi-layer command/injection safety, evidence-as-provenance, session-quality gate before mining, **slice-based (per-block) utility**. | README + code (below) |

Reading note: `meta_skill` is a **single-user, local-first** system. Several of its choices (hash embeddings, local Git audit, a personal bandit) are excellent for one operator on one box and **do not transfer unchanged** to a multi-tenant / CI / signed-attestation platform. That mismatch is itself a finding (§9 open questions).

---

## 2. The blunt finding: "usefulness" is a static constant, not a computed score

The brief asked how `meta_skill` scores "usefulness." It does not compute one. Its "utility" is a **static, semantically-motivated hierarchy keyed on slice type**, embedded as a `const fn`:

```rust
// src/core/slicing.rs:161-172
const fn utility_score(slice_type: SliceType) -> f32 {
    match slice_type {
        SliceType::Policy => 0.95,      // Highest utility
        SliceType::Rule => 0.9,
        SliceType::Pitfall => 0.85,
        SliceType::Checklist => 0.75,
        SliceType::Command => 0.7,
        SliceType::Example => 0.65,
        SliceType::Overview => 0.55,
        SliceType::Reference => 0.4,     // Lowest utility
    }
}
```

This is **not machine-learned and not dynamically computed** — policies/rules are *declared* more useful than examples/references. Slice classification that feeds it is also rule-based (`src/core/slicing.rs:96-111`): a `Rule` block becomes `Policy` if its id contains "policy"/"invariant", `Code`→`Example`, `Checklist`→`Checklist`, etc. Packing modes (`src/core/packing.rs:447-465`) then bias selection by these constants (BalancedPacking, UtilityFirst, RuleHeavy, SafetyFirst).

**The `jeffreys-skills.md` website — unconfirmed, do not assert.** The meta_skill repo has **no web-app code** (no JS/TS/Node/web-framework files), **no Netlify/Vercel config**, and a standalone `jeffreys-skills.md` repo **does not resolve** (clone → "repository not found"). The README references a "JeffreysPrompts Premium Cloud" sync but nothing public. **Conclusion to carry forward: the site is powered by something not in the repo (private / different tool / hosted elsewhere) — the CLI + SQLite DB is the authoritative system, and the report must not claim the site's backing is confirmed.**

Where the real dynamic signal lives: feedback flows into a Thompson-sampling contextual bandit that drives *recommendations* (`ms recommend`), and `quality` uses a genuine weighted formula. "Usefulness/utility" itself is the constants above.

---

## 3. The scoring internals that ARE real

### 3A. `quality` — the one genuinely-computed score

Weighted average of 6 dimensions, each normalized 0.0–1.0 (`src/quality/skill.rs:24-57`, weights `:95-105`):

| Dimension | Weight | Signal | Function |
|---|---|---|---|
| content | **0.25** | depth of explanation + code examples | `content_score :146-172` (graduated by length; +0.1 code-block bonus; cap 1.0) |
| evidence | **0.20** | provenance refs linked | `evidence_score :174-181` (0=0.2 … 5+=1.0) |
| usage | **0.20** | times loaded/used | `usage_score :183-191` (0=0.1 … 11+=1.0) |
| structure | **0.15** | section organization | `structure_score :136-144` (0=0.1 … 3+=1.0) |
| toolchain | **0.10** | env compatibility | match=1.0 / no-match=0.4 (`:29`) |
| freshness | **0.10** | recency | `freshness_score :193-207` (0-30d=1.0 … 180+d=0.3; unknown=0.5) |

Issue/suggestion detection at `:223-276` (missing sections, low content, no examples, low evidence, low usage, missing tags).

### 3B. Slice utility — see §2 (static constants, not a rubric)

### 3C. Feedback → reward map — the learned signal (this is gap (a))

Feedback enum (`src/suggestions/bandit/rewards.rs:10-50`): `ExplicitHelpful`, `UsedDuration{minutes}`, `LoadedOnly`, `Ignored`, `ExplicitNotHelpful{reason}`, `UnloadedQuickly`, `Rating{stars}`, `TaskCompleted{success,duration}`. Reward mapping (`:84-130`):

| Feedback | Reward |
|---|---|
| ExplicitHelpful | 1.0 |
| UsedDuration >5 min | 0.8 (0–5 min scales 0.4–0.8) |
| LoadedOnly | 0.3 |
| Ignored | 0.1 |
| ExplicitNotHelpful / UnloadedQuickly | 0.0 |
| Rating | `(stars-1)/4` (1★=0.0, 3★=0.5, 5★=1.0) |
| TaskCompleted (success+fast) | 0.7–0.9 (failure → 0.2) |

Contextual adjustment (`:139-163`): context-match >0.7 → ×1.1, <0.3 → ×0.9; was-top-suggestion & reward>0.5 → ×1.1; capped 1.0. Aggregate weights (`:169-188`): Explicit ×2.0; Rating/TaskCompleted ×1.5; UsedDuration ×1.0; LoadedOnly/UnloadedQuickly ×0.8; Ignored ×0.5. **This is a contextual bandit driven by real observed adoption — the single most interesting thing IEP does not have.**

### 3D. Session-quality mining gate (`src/cass/quality.rs:1-241`)

Before a skill is mined from a session, the session must clear a quality bar: tests_passed +0.25, clear_resolution +0.25, code_changes +0.15, user_confirmed +0.15; backtracking −0.10 (≥2 reverts), abandoned −0.20; **threshold 0.3 to pass.** A disciplined "don't learn from a bad session" gate.

### 3E. DB schema (data-model reference)

`skills` (`migrations/001:6-37`, stores `quality_score REAL`), `skill_feedback` (`009:1-14`), `skill_usage` (`001:141-166`, has `success_signal`, `experiment_id`, `variant_id`, `context_keywords`), `skill_evidence` (`001:69-77`), `skill_experiments` (`001:212-221`, A/B variants, scope skill|slice). Search (`cli/commands/search.rs:1-50`): 3 modes — **Hybrid (default) = BM25 + semantic via RRF**, BM25-only (Tantivy), Semantic-only (FNV-1a hash); filters tags/layer/min_quality/include_deprecated.

---

## 4. The 13-tool eval landscape (what to learn, what to avoid)

Twelve eval/benchmark tools + the MCP Registry pattern (the brief's "13"); two extra catalog patterns (#14–15) included for completeness. Verdicts are "what's worth copying" / "what to avoid," not endorsements.

| # | Tool | What it does | LEARN | AVOID |
|---|---|---|---|---|
| 1 | **Promptfoo** | declarative prompt/agent testing, red-team, regression diff, CI | bootstrap-95%-CI regression on a **delta vector** (baseline = prior version's score vector, not a frozen number); cost-per-run + prompt versioning first-class | ad-hoc result storage |
| 2 | **Inspect AI** (UK AISI) | eval framework, 200+ prebuilt evals, model-graded | **Solvers** abstraction (separate task def from solve strategy) | no enforced metadata schema |
| 3 | **OpenAI Evals** | eval framework + GitHub registry | **spec-first YAML rubrics**; YAML-only registry as a quality gate | custom code in the eval registry (they learned this the hard way) |
| 4 | **DeepEval** | Python eval framework, rich metric lib | scorer-interface pattern; cost tracking first-class | duck-typed extensibility; "agent-native v4" vaporware |
| 5 | **Ragas** | RAG-specialized, reference-free metrics | **Metric-Family** concept; typed dataset schema (Single/MultiTurnSample) | HuggingFace tight coupling |
| 6 | **Braintrust** | observability + eval; tracing + human feedback | **side-by-side human + automated scores**; typed error/retry trace schema | cloud lock-in |
| 7 | **Langfuse** | OSS observability + eval + prompt mgmt | **datasets as first-class artifact**; annotation queues with an open-ended **TEXT score type** | overloading one platform with everything |
| 8 | **Arize Phoenix** | OSS observability + eval, **OTel-native** | **explanations as first-class eval output**; OTel > proprietary trace schema | Jupyter-first DX |
| 9 | **LangSmith** | LangChain commercial observability + eval | low- + high-level evaluator helper-library pattern | vendor lock-in |
| 10 | **lm-evaluation-harness** (EleutherAI) | few-shot LLM eval; backs HF Open LLM Leaderboard | **filter/pipeline scoring** (extract→normalize→match→aggregate, composable) | coupling scoring to task definition |
| 11 | **Giskard** | LLM-agent testing + red-team; auto-generated Scan suites | **auto adversarial test generation from a plain description**; test behaviors not just outputs | over-relying on LLM-generated adversarial cases |
| 12 | **SWE-bench** | benchmark for code agents on real GitHub issues | **execution-based ground truth** (run repo tests = pass/fail) — the gold standard | repo-specific bespoke harnesses |
| 13 | **MCP Registry** | community discovery for MCP servers | **reverse-DNS naming** kills collision; strict submission format; env-var schema (`isRequired`/`isSecret`) | per-registry submission overhead |
| 14 | Claude Code Plugins/Skills | plugin/skill/agent/MCP discovery | **SKILL.md (YAML+MD) is portable**; `metadata.version` + `reviewed_at`; `allowed-tools` privilege guard | fragmented competing registries |
| 15 | awesome-mcp ecosystem | competing curated MCP lists | objective **ranking framework** (stars/recency/license/docs/activity); Smithery **Toolbox meta-MCP** routing | accepting fragmentation as inevitable |

**Cross-cutting patterns worth internalizing:** (i) regression baselines are **vectors with confidence intervals**, not frozen scalars (Promptfoo); (ii) **execution-based ground truth** beats LLM-judge where you can get it (SWE-bench); (iii) **explanations + OTel-native traces** as first-class eval outputs (Phoenix); (iv) **human review side-by-side with automated scores** (Braintrust/Langfuse); (v) **open-ended TEXT scores** for things that don't fit a number (Langfuse). The full aspect-by-aspect tables (Storage/Serialization, Scoring Model, Human Feedback, Regression Testing, Traces & Provenance) live in the persisted survey artifact (see §Bibliography).

---

## 5. COPY / DON'T-COPY / BEST-DIRECTION

**COPY (the real gaps):**
- The **usage → feedback → bandit loop** (`meta_skill` §3C) — a learned "which skill/version actually helped" signal driven by real adoption, not self-description.
- **Slice-level utility** — score per block (policy/rule/example), not only per skill.
- **Hybrid BM25 + semantic catalog search** with rank-fusion over a skill catalog (softer adjacent).
- From the landscape: delta-vector regression with CIs (Promptfoo), explanations-as-output + OTel (Phoenix), human-review-beside-automated (Braintrust/Langfuse), execution-based ground truth where available (SWE-bench).

**DON'T COPY:**
- A **static "utility" constant** dressed up as a computed score (§2). If IEP adds utility, compute it.
- **Hash-only embeddings** (FNV-1a) — fine for a reproducible single-user box, wrong for a catalog that needs real semantic recall.
- **Single-user local-first assumptions** — a personal Git audit log and a personal bandit do not survive multi-tenant / CI / signed-attestation requirements.

**BEST DIRECTION:** extend the **kernel + j-rig + dashboard** — add a feedback/usage entity and a catalog-search layer. **Do not fork a new Rust tool.** IEP's differentiators (signed Evidence Bundles, binary criteria, verify-before-render, deterministic gates) are exactly what `meta_skill` lacks; the only thing `meta_skill` has that IEP lacks is the adoption-feedback loop.

---

## 6. Proposed scoring model — tagged existing / gap / add

Eight scores. Each tagged with where it already lives in IEP, or GAP.

| Score | What it measures | Computed? | IEP status |
|---|---|---|---|
| **Quality** | structure/content/evidence/freshness of the artifact | computed | **EXISTS** — `validate-skillmd` 10-dimension deep-eval engine v6.0 (`~/.claude/skills/validate-skillmd/SKILL.md`); kernel `SkillSnapshot`/`SkillVersion` |
| **Reliability** | does it pass its behavioral eval across models | computed | **EXISTS** — j-rig 7-layer binary harness; per-model matrix |
| **Regression** | did a change break a sacred case | computed | **EXISTS** — j-rig `regressions`/`RegressionPack`; "regressions are sacred" |
| **Evidence** | provenance / signed-bundle backing | computed | **EXISTS** — kernel `EvidenceBundle` + `gate-result/v1`; audit-harness `emit-evidence` |
| **Freshness** | recency / drift | computed | **EXISTS** — dashboard `src/freshness/*` (24h buckets, USE-method); kernel timestamps |
| **Adoption / usage** | times loaded/used, real-world pickup | computed | **GAP (a)** — no `usage_events` entity anywhere |
| **Human-trust** | reviewer thumbs / annotations | curated | **GAP** — no `human_reviews` entity; landscape says make it first-class (Braintrust/Langfuse) |
| **Usefulness (slice)** | per-block policy/rule/example value | hybrid | **GAP (b)** — `meta_skill` fakes it with constants; IEP has none. If added, compute it. |

Anti-gaming note: every added score needs a guardrail (e.g. usage counted only from verified sessions à la `meta_skill`'s session-quality gate §3D, not raw load counts). **Do not roll these into one headline number** — see §9 (C3 tension).

---

## 7. Proposed data model — map to kernel entities first

Twelve conceptual tables; most are already a kernel entity. Only two are genuinely new.

| Table | Covered by existing kernel entity? |
|---|---|
| `eval_subjects` | `SkillSnapshot` / `SkillVersion` |
| `eval_runs` | `EvalRun` |
| `eval_cases` | `EvalSpec` (criteria/test cases) |
| `eval_results` | `JudgeDecision` / `criterion_results` (j-rig) |
| `scorecards` | `EvidenceBundle` (gate-result rows) |
| `evidence_items` | `EvidenceBundle` payload / audit-harness rows |
| `provenance_events` | `RuntimeReceipt` / `SessionTrace` |
| `skill_versions` | `SkillVersion` (14th entity, DR-028 T1) |
| `tool_versions` / `agent_versions` | `ToolInvocation` + (SAK authoring artifacts) |
| **`usage_events`** | **NEW** — adoption signal (gap a) |
| **`human_reviews`** | **NEW** — curated trust signal |

**Only `usage_events` + `human_reviews` are new.** Both should ship as kernel contract triplets (JSON Schema + Zod + state machine) per DR-010's unification thesis, and emit Evidence-Bundle-compatible rows.

---

## 8. Proposed CLI — map to existing surfaces

`intent-eval { scan, score, test, compare, publish-scorecard, ingest-skill, evidence add, review, ci-gate }` — most already exist:

| Verb | Already provided by |
|---|---|
| `scan` / `classify` | audit-harness `classify`/`scan` |
| `score` | `validate-skillmd` + j-rig |
| `test` | j-rig binary harness |
| `compare` | j-rig baseline/regression |
| `evidence add` | audit-harness `emit-evidence` |
| `ci-gate` | `intent-rollout-gate` Action |
| `publish-scorecard` | dashboard results browser |
| **`ingest-skill` / `review`** | **partially GAP** — the usage/human-review intake (gaps a + Human-trust) |

---

## 9. 30-day MVP + open questions

**30-day MVP (wire existing surfaces + add the two gaps, not build-from-zero):** wk1 — `usage_events` + `human_reviews` kernel triplets + ingestion; wk2 — adoption/usefulness scoring on top of existing j-rig/validate-skillmd; wk3 — CLI `ingest-skill`/`review` + a scorecard report; wk4 — CI gate + scorecard surface on the dashboard.

**Open questions:**
1. **What actually powers `jeffreys-skills.md`?** Unconfirmed (§2). Do not design against it.
2. **Does a contextual bandit fit a multi-tenant / CI context** at all, or only a single-user local box? `meta_skill`'s bandit assumes one operator's feedback stream.
3. **The C3 tension (important).** A single rolled "usefulness %" collides with the dashboard's **hard C3 binding — no aggregate PASS% across heterogeneous predicates** (`src/results/c3-scan.ts`, CTO+CMO+VP-DevRel triple-refusal). A skill scorecard that averages quality+usefulness+adoption into one headline number would violate the platform's own integrity rule. **Lean toward per-dimension scores shown side-by-side, never one rolled number.**
4. Anti-gaming of adoption: count usage only from session-quality-gated sessions (§3D), else "load it in a loop" inflates the score.

---

## 10. Closing four lists

**(1) Top-10 takeaways**
1. This is a gap analysis — IEP already owns the hard parts.
2. `meta_skill` "usefulness" is a static `const fn`, not computed (`slicing.rs:161-172`).
3. The only genuinely-learned signal is the feedback→bandit loop (`rewards.rs`) — that's gap (a).
4. The only genuinely-computed score is `quality` (`skill.rs:24-57`).
5. `jeffreys-skills.md` backing is unconfirmed — don't design against it.
6. Two real gaps: usage/feedback loop + slice-level utility. Two soft adjacents: hybrid catalog search + a rolled score (avoid the latter).
7. Landscape gold standards: delta-vector regression CIs, execution-based ground truth, explanations+OTel, human-beside-automated, open-ended TEXT scores.
8. Only two new kernel tables needed: `usage_events`, `human_reviews`.
9. Most of the proposed CLI already exists; only intake (`ingest-skill`/`review`) is new.
10. A rolled "usefulness %" would violate the dashboard's C3 binding — keep dimensions un-rolled.

**(2) Five features to build first**
1. `usage_events` kernel triplet + verified-session intake.
2. `human_reviews` kernel triplet (open-ended TEXT score, à la Langfuse).
3. Adoption score computed from verified usage (anti-gaming gated).
4. Slice-level utility — **computed**, not constant.
5. Delta-vector regression baselines with CIs (Promptfoo pattern) layered onto j-rig.

**(3) Five traps to avoid**
1. Forking a new standalone tool.
2. Static constants masquerading as computed utility.
3. Hash-only embeddings for catalog search.
4. A single rolled headline score (C3 violation).
5. Counting raw loads as adoption (gameable).

**(4) Files created**
- `099-RR-eval-research/100-RR-LAND-intent-eval-platform-skill-scoring-research-2026-06-24.md` (this file)
- `099-RR-eval-research/101-RR-BIBL-skill-scoring-tool-references-2026-06-24.md` (sources)

---

*Non-normative research. If a scoring-layer epic proceeds, the two new entities (`usage_events`, `human_reviews`) route through the kernel per DR-010, and any "usefulness %" surfacing must be reconciled against the C3 no-aggregate-PASS binding before it ships.*
