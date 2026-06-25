# RR-BIBL — Skill-scoring research: source & reference index

**Filing:** `099-RR-eval-research/101-RR-BIBL-...` (coded research cluster, Doc Filing Standard v4.4 §3.1)
**Date:** 2026-06-24
**Companion (main):** `100-RR-LAND-intent-eval-platform-skill-scoring-research-2026-06-24.md`
**Purpose:** Every source the landscape report draws on, grouped by kind. Citations into `meta_skill` are file:line against the repo at clone time (commit not pinned — `meta_skill` is a moving target; re-verify before quoting in anything normative).

---

## 1. Primary subject — `meta_skill`

- Repo: `https://github.com/Dicklesworthstone/meta_skill` (Jeffrey Emanuel / `Dicklesworthstone`). Local-first Rust + SQLite skill manager; CLI binary `ms`.
- Related: `https://github.com/Dicklesworthstone/xf` (referenced in passing).
- Site (UNCONFIRMED backing): `jeffreys-skills.md/skills` — no corresponding public repo resolves; not powered by anything in `meta_skill`. Do not design against it.

**File:line citations** (cloned to `/tmp/meta_skill` during research):

| Area                               | Path:lines                                                                                                                                                      |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Quality score (formula + weights)  | `src/quality/skill.rs:24-57`, weights `:95-105`, sub-scorers `:136-207`, issue detection `:223-276`                                                             |
| Slice utility constants            | `src/core/slicing.rs:161-172`                                                                                                                                   |
| Slice classification               | `src/core/slicing.rs:96-111`; token estimate `:174-178`                                                                                                         |
| Feedback → reward map / bandit     | `src/suggestions/bandit/rewards.rs:10-50` (enum), `:84-130` (rewards), `:139-163` (contextual), `:169-188` (aggregate)                                          |
| Session-quality mining gate (CASS) | `src/cass/quality.rs:1-241`                                                                                                                                     |
| Packing modes                      | `src/core/packing.rs:447-465`                                                                                                                                   |
| CLI commands                       | `src/cli/commands/{search,quality,feedback,recommend,experiment,mcp}.rs`                                                                                        |
| MCP server                         | `src/cli/commands/mcp.rs:1-39`                                                                                                                                  |
| DB schema                          | `migrations/001_initial_schema.sql` (skills `:6-37`, evidence `:69-77`, usage `:141-166`, experiments `:212-221`), `migrations/009_add_skill_feedback.sql:1-14` |
| Manifests / docs                   | `Cargo.toml`, `README.md` (storage model `:87-96`), `skills/crafting-readme-files/skill.spec.json`                                                              |

---

## 2. The eval-tool landscape (13 + 2)

| Tool                               | Repo / docs                                                                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Promptfoo                          | `github.com/promptfoo/promptfoo` (evaluators: `/tree/main/src/evaluators`); `promptfoo.dev/docs`                                            |
| Inspect AI (UK AISI)               | `github.com/UKGovernmentBEIS/inspect_ai`                                                                                                    |
| OpenAI Evals                       | `github.com/openai/evals` (`/blob/main/docs/custom-eval.md`)                                                                                |
| DeepEval (Confident AI)            | `github.com/confident-ai/deepeval`                                                                                                          |
| Ragas                              | `github.com/vibrantlabsai/ragas`                                                                                                            |
| Braintrust                         | `github.com/braintrustdata`; `braintrust.dev/docs/annotate/human-review`; `braintrust.dev/articles/agent-observability-complete-guide-2026` |
| Langfuse                           | `github.com/langfuse/langfuse`; `langfuse.com/docs/evaluation/overview`; `.../evaluation-methods/annotation`                                |
| Arize Phoenix                      | `github.com/Arize-ai/phoenix`                                                                                                               |
| LangSmith                          | `docs.langchain.com/langsmith/evaluation`                                                                                                   |
| lm-evaluation-harness (EleutherAI) | `github.com/EleutherAI/lm-evaluation-harness` (`/blob/main/docs/task_guide.md`)                                                             |
| Giskard                            | `github.com/Giskard-AI/giskard-oss`                                                                                                         |
| SWE-bench                          | `github.com/swe-bench`                                                                                                                      |
| MCP Registry                       | `registry.modelcontextprotocol.io`; `github.com/modelcontextprotocol/registry`                                                              |
| Claude Code Plugins/Skills         | `github.com/anthropics/claude-plugins-official`; community: `alirezarezvani/claude-skills`, `sickn33/antigravity-awesome-skills`            |
| awesome-mcp ecosystem              | `smithery.ai`, `mcp.so`, `glama.ai/mcp`, `punkpeye/awesome-mcp-*`                                                                           |

---

## 3. Standards & background

- MCP spec: `modelcontextprotocol.io/specification/2025-11-25`; server schema `static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`; `github.com/modelcontextprotocol/modelcontextprotocol`
- Provenance / signing: in-toto (`in-toto.io`), sigstore (`sigstore.dev`)
- Regression / observability background: `futureagi.com/blog/prompt-regression-testing-2026`; OTel GenAI semantic conventions `greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions`

---

## 4. IEP internal references (the "already owns" inventory)

| Surface                                                                                     | Path                                                                                                                           |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Kernel `@intentsolutions/core` (14 entities, gate-result/v1, EvidenceBundle, SAK authoring) | `intent-eval-core/src/entities/*`, `schemas/v1/*`, `schemas/authoring/v1..v2/*`, `src/validators/v1/*`                         |
| j-rig 7-layer binary harness + Refiner                                                      | `j-rig-binary-eval/packages/*`                                                                                                 |
| audit-harness deterministic gates + emit-evidence + classify/conform                        | `audit-harness/scripts/*`                                                                                                      |
| dashboard verify-before-render + freshness + C3 gate                                        | `intent-eval-dashboard/src/{results,freshness,ingest}/*` (C3: `src/results/c3-scan.ts`)                                        |
| `validate-skillmd` 10-dimension deep-eval + 8-field rubric                                  | `~/.claude/skills/validate-skillmd/SKILL.md`; validator `~/000-projects/claude-code-plugins/scripts/validate-skills-schema.py` |
| Governance bindings (DR-010, DR-028, DR-035, Blueprints A/B)                                | `intent-eval-lab/000-docs/{010,012,028,035}-*.md`                                                                              |

---

## 5. Provenance of this research

- 3 Explore-agent sweeps (2026-06-24 prior session): meta_skill source clone + read; 13-tool repo+docs survey; IEP path inventory.
- Raw per-tool aspect-by-aspect breakdown (6 cross-cutting comparison tables + "Key Learnings for Intent" + competitive-advantage closing) persisted at session tool-result `toolu_01WwXuuf5KucopK3aVgYmp9b.json` — read directly for the long-form survey detail not reproduced in `100-RR-LAND`.

---

_Reference index only. URLs captured 2026-06-24; `meta_skill` line numbers are unpinned and should be re-verified before any normative citation._
