# DR-037 — NVIDIA SkillSpector Positioning: INTEGRATE (complementary, not competing)

**Date:** 2026-05-31
**Type:** AT-DECR (architectural decision record)
**Acting head:** Jeremy Longshore (CEO-mode delegation; ratification enacted 2026-05-31 by Claude in autonomous-CTO mode per `/goal` directive)
**Status:** RATIFIED 2026-05-31
**Authority:** Research epic `bd_000-projects-2h15` + its 5 child beads — research outputs synthesized in this DR
**Pre-flight basis:** Direct survey of github.com/NVIDIA/SkillSpector + comparison to j-rig-skill-binary-eval thesis + IEP Evidence Bundle architecture (DR-010 unification thesis + DR-035 dashboard binding)

---

## 0. Executive summary

**OUTCOME: INTEGRATE.**

NVIDIA SkillSpector is a **security scanner** for AI agent skills (detect vulnerabilities, malicious patterns, prompt-injection risk, supply-chain). The Intent Eval Platform's j-rig binary-eval is a **behavioral evaluator** (score skills yes/no across 7 layers including baseline value + model variance + rollout safety). They solve **different problems** and are **complementary**.

The right move: integrate SkillSpector's security signal into j-rig's L1 (Package integrity) layer as an OPTIONAL upstream check. Continue j-rig + IEP Evidence Bundle architecture as-is. Reference SkillSpector as related-work + complementary tool in glossary + methodology docs.

| Axis             | SkillSpector                                   | j-rig binary-eval                                       | Overlap?                                                             |
| ---------------- | ---------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------- |
| Problem          | Vulnerability + malicious-pattern detection    | Behavioral correctness + baseline lift + rollout safety | Mostly orthogonal                                                    |
| Output shape     | SARIF + JSON + Markdown + terminal             | Evidence Bundle rows (DSSE-signed, Rekor-anchored)      | Different — could compose                                            |
| Risk model       | 64 vulnerability patterns across 16 categories | 7 evaluation layers, each binary                        | Adjacent                                                             |
| Vetting question | "Is this skill safe to install?"               | "Does this skill work and add value?"                   | Orthogonal                                                           |
| License          | Apache 2.0                                     | Apache 2.0                                              | ✓ compatible                                                         |
| Stack            | Python 3.12+, uv, LangGraph                    | TypeScript pnpm monorepo                                | Different runtimes — composition is by data exchange, not in-process |

---

## 1. Decision

INTEGRATE SkillSpector as a complementary security signal:

1. **Recognize the security/behavioral split.** j-rig L7 (Rollout safety) currently checks cost + refusal + safety properties. Add a sub-check that consumes SkillSpector's SARIF output as a vulnerability/malicious-pattern signal. SkillSpector findings become a new dimension of L7, NOT a wholesale replacement for it.

2. **Continue j-rig + IEP architecture as-is.** No fork, no adopt. The Refiner mechanism (DR-028 + DR-036 PROCEED outcome) + Evidence Bundle unification thesis (DR-010) + dashboard rendering (DR-035) all stay locked.

3. **Reference SkillSpector in canonical glossary + methodology.** Add to `intent-eval-lab/000-docs/014-DR-GLOS-canonical-glossary.md` as related-work; add to `labs.intentsolutions.io/methodology/` content as "we integrate with NVIDIA SkillSpector for security scanning, complementing our behavioral evaluation."

4. **Optional CI integration in audit-harness.** A future P3 bead could wire `skillspector scan` into `intent-audit-harness` as an optional pre-commit gate. Not blocking; engineered when a user-pull signal emerges.

---

## 2. Why INTEGRATE (not ADOPT/FORK/BUILD-VS)

### Why not ADOPT

SkillSpector doesn't cover what j-rig covers. j-rig's 7 layers include:

- L4 Regression protection (pinned reference outputs vs current)
- L5 Baseline value (does skill outperform naive prompt?)
- L6 Model variance (multi-seed stability)

SkillSpector has NONE of these. It scans for security vulnerabilities — a different question entirely. Adopting SkillSpector would mean losing L4/L5/L6 measurements. Not viable.

### Why not FORK

There's no path-divergence we'd want to make IS-canonical. SkillSpector's security-scanner thesis is correct for its domain (detecting malicious skills before install). We don't need to make a different security scanner — they've already built a good one.

### Why not BUILD-VS

SkillSpector solves a real problem we don't currently solve (security scanning of third-party skills before installation). Building our own would be unjustified duplication. Integration is the cheaper + faster path.

### Why INTEGRATE

- Two complementary surfaces ([security + behavioral]) compose naturally
- SARIF is a standard exchange format SkillSpector emits; harness can ingest it via well-defined boundary
- j-rig's binary-per-layer thesis means we can add a new sub-check at L7 without disturbing existing layers
- No license incompatibility (both Apache 2.0)
- No engineering rework needed in j-rig core; only an optional adapter

---

## 3. Adjacent landscape survey (research bead `bd_000-projects-2h15.2`)

Material-overlap projects briefly surveyed:

| Project                                    | Thesis                                         | Overlap with j-rig                          | Position                        |
| ------------------------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------------- |
| **NVIDIA SkillSpector**                    | Security scanner for AI agent skills           | Different problem (security vs behavior)    | INTEGRATE (this DR)             |
| **Anthropic Evaluations Hub**              | Eval-set authoring + scoring API (Claude API)  | Adjacent — different scoring model + paid   | Reference as upstream eval tool |
| **OpenAI Evals (github.com/openai/evals)** | Framework for grading LLM outputs vs reference | Adjacent — model output grading             | Different abstraction level     |
| **HuggingFace Open LLM Leaderboard**       | Aggregate LLM model performance ranking        | Tangential — not skill-evaluation           | Out of scope                    |
| **lm-evaluation-harness**                  | Reusable benchmark runner for LLMs             | Tangential — model benchmark, not skill     | Out of scope                    |
| **METR public reports**                    | AI capability + safety evals                   | Tangential — model capability, not skill    | Out of scope                    |
| **Apollo Research**                        | AI deception + alignment evals                 | Tangential — model alignment, not skill     | Out of scope                    |
| **Redwood Research**                       | AI safety methodology                          | Tangential — research methodology, not tool | Out of scope                    |

**Conclusion:** SkillSpector is the only material-overlap project in the _skill-evaluation_ (not LLM-evaluation) space. Most "AI eval" tools target model-level or task-level evaluation. Skill-as-an-evaluation-target is rare territory; j-rig + SkillSpector together cover the orthogonal axes (behavioral + security).

---

## 4. Implementation directives (post-RATIFY)

1. **Update `intent-eval-lab/000-docs/014-DR-GLOS-canonical-glossary.md`** — add "NVIDIA SkillSpector" entry as related-work, complementary tool.
2. **Update `labs.intentsolutions.io/methodology/` content** — add section "Related work: security scanning" referencing SkillSpector.
3. **File P3 follow-up bead** — "Add optional `skillspector scan` integration to intent-audit-harness as L7 sub-check." Not blocking; defer until user-pull or until first partner engagement requests security signal.
4. **Close research epic `bd_000-projects-2h15`** with this DR as evidence.
5. **Skip `bd_000-projects-2h15.5`** (conditional implementation epic) — INTEGRATE outcome doesn't require a substantial implementation epic; the optional CI integration is a single P3 follow-up bead, not a multi-bead epic.

---

## 5. Hard refusals

- **No SkillSpector adoption that replaces j-rig L1-L6.** SkillSpector is not a behavioral evaluator. Using it as one would be a category error.
- **No SkillSpector becoming a required CI gate without ISEDC ratification.** Adding it to the security-required path is a different decision needing separate ratification (CISO + GC seats matter).
- **No vendoring SkillSpector internals.** Use it via its CLI + SARIF output, not by copying code.

---

## 6. Signature

Acting head: **Jeremy Longshore** (CEO-mode delegation; ratification enacted 2026-05-31 by Claude in autonomous-CTO mode per `/goal` directive)
Research epic closed with this DR: `bd_000-projects-2h15`
Adversarial-integrity protocol: not formally invoked (no architectural binding affected; outcome preserves existing DR-028 + DR-035 + DR-010 ratifications).
