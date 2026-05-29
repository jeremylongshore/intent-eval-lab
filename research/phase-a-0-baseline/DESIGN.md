# Phase A.0 — Null-Hypothesis Baseline: Experimental Design

**Bead:** `bd_000-projects-214c.8` · **GH:** `jeremylongshore/j-rig-skill-binary-eval#81`
**Authority:** Plan 027 § 13 Step 7 + DR-028 P0-RATIFY-3 + DR-BAND § 2 Phase A.0
**Status:** DRAFT — Session 1 deliverable (2026-05-28)
**Bandwidth budget:** 3.5 FTE-days · **Cost ceiling:** see § 7

---

## 1. Decision rule (verbatim from DR-028 P0-RATIFY-3)

> If naive-Opus-in-context-with-eval-set achieves **> 70% of projected Refiner lift** on the Phase B demo skill, DESCOPE Phase B mechanism. Per VP DevRel binding: result is PUBLISHED as a blog post REGARDLESS of outcome.

**Target skill (Phase B demo per Step 0 CTO call 2026-05-27):** `/validate-skillmd`.

**Why this skill:** meta-recursive (a SKILL.md authoring validator validated against its own corpus); IP-defense story is sharper; eval-set bootstrap is easiest (a SKILL.md is its own most natural input).

## 2. Null vs alternative hypotheses

| Hypothesis | Statement |
|---|---|
| **H₀ (null, bitter-lesson)** | Naive Opus 4.7 prompted with the eval-set in-context produces SKILL.md edits whose post-edit validator scores match or exceed ≥70% of the projected Refiner-mechanism lift, with no propose/accept loop, no rejected-edit buffer, no multi-pass refinement |
| **H₁ (alternative)** | The Refiner's bounded-edit-ops + strict-improvement-gate mechanism produces > 30% additional lift beyond naive Opus in-context — enough to justify Phase B mechanism build |

Reject H₀ → ship Phase B as planned. Fail to reject H₀ → DESCOPE Phase B mechanism; document the bitter-lesson finding; pivot remaining FTE-weeks to the durable contribution (the acceptance gate per AC-7).

## 3. Arms

### Arm A — Naive Opus-in-context (null hypothesis)

**Prompt template:**
```
You are improving a SKILL.md frontmatter file for the Intent Solutions marketplace
tier. The IS marketplace tier requires 8 fields: name, description, allowed-tools,
version, author, license, compatibility, tags. Disallowed-tools is recognized.

Here are <K> exemplars of SKILL.md frontmatter that pass the IS marketplace
validator:

<exemplar 1 frontmatter>
<exemplar 2 frontmatter>
...
<exemplar K frontmatter>

Now improve the following SKILL.md to maximize its IS-marketplace-tier validator
score. Return only the updated frontmatter block.

<input SKILL.md frontmatter>
```

**Model:** `claude-opus-4-7` via Anthropic API.
**K (exemplar count):** sweep K ∈ {0, 3, 8, 16} to map the in-context lift curve.
**Temperature:** 0.0 (deterministic for replication).
**No iteration:** single forward pass. No accept/reject. No rejected-edit buffer. **Whatever Opus emits is the candidate.**

### Arm B — Proposed Refiner mechanism (alternative)

The Refiner mechanism per Plan 027 § 4 Phase A + § 14 SAK § 14.4:
1. `propose(input, K-exemplars) → EditProposal` (Opus generates bounded add/del/replace ops)
2. `apply(input, EditProposal) → SkillDocV2`
3. `score(SkillDocV2) → ScoreRecord` (multi-dim per AC-3)
4. `accept(score_v1, score_v2) → bool` (strict improvement on every dim, no regression)
5. If reject: log to rejected-buffer; re-propose with rejection rationale in context (max N=3 iterations)
6. Final SkillDocV2 = highest-scoring accepted version

**Projected lift basis:** Plan 027 § 9 + plan 033 § 14.4 do NOT yet give a numeric projection. **Phase A.0 must establish this number empirically** by running Arm B on a sample of the corpus (~10 specimens) before extrapolating to the full Arm A vs Arm B comparison.

**Open question (resolve before any API calls):** is the projected Refiner lift a *plan-stipulated target* (pre-registered) or an *empirically-discovered* lift from running the mechanism? Per DR-028 P0-RATIFY-3 wording, it's the *projected* lift — implying pre-registration. Files `intent-eval-lab/000-docs/{027,033}-PP-PLAN-*.md` do not currently contain a number. **Acting CTO must fix this BEFORE running Arm A.** Recommendation: 1.5pp marketplace-tier score lift (the midpoint of "barely worth the engineering" and "obvious win") as the projected target. Document in DR-028 amendment if accepted.

## 4. Judge (scoring function)

**Authoritative scorer:** `claude-code-plugins/scripts/validate-skills-schema.py` SCHEMA 3.7.0 (post-D4 merge, commit `7b9eb8f`).

**Score record dimensions (per AC-3 multi-dimensional discipline):**

| Dimension | How computed |
|---|---|
| `marketplace_pass` | boolean — does it satisfy the 8-field IS marketplace required set? |
| `marketplace_score_pct` | int 0–100 — % of marketplace-tier rubric points awarded |
| `field_completeness` | 0–8 — count of `ALWAYS_REQUIRED` fields present |
| `deprecated_field_count` | 0–N — number of deprecated fields (e.g. `compatible-with`) |
| `security_finding_count` | 0–N — count of shell-substitution / wildcard / scope security findings (highest-severity tier) |
| `description_chars` | int — combined length of `description` + `when_to_use` |
| `is_extras_present` | int 0–11 — count of IS-extras (visibility, env-config, progressive-disclosure, semver, etc. per plan 033 § 14.10) |

**Acceptance gate (Arm B `accept()`):** `marketplace_pass: false→true` is a strict improvement IF no other dim regresses. `marketplace_score_pct +ε` with no regression on other dims is a strict improvement. Any dim regression rejects the edit.

**Why this judge is post-D4 credible:** prior to D4 merge (PR #788, 2026-05-28 22:40Z), validator would have flagged `disallowed-tools` as unknown field — biasing scores on the ~50% of corpus already using it. Post-D4, judge accurately reflects current Anthropic spec floor + IS marketplace rubric.

## 5. Corpus

**Source pools** (in priority order):

| Pool | Count | Status |
|---|---|---|
| `~/.claude/skills/*/SKILL.md` (global IS-authored) | 52 | curated, high-signal |
| `claude-code-plugins/plugins/**/SKILL.md` (marketplace corpus) | 3,044 | varied quality, the migration target |
| `~/000-projects/*/.claude/skills/**/SKILL.md` (per-project) | ~30 | unchecked baseline |

**Phase A.0 sample design:**
- **N = 60 specimens** (statistically-meaningful for 70%-threshold test with α=0.05)
- **Stratification:**
  - 20 global (~/.claude/skills) — represents IS-authored quality floor
  - 20 marketplace high-validator-score (random sample from passing-3.7.0 subset)
  - 20 marketplace low-validator-score (random sample from failing-3.7.0 subset — these are the *highest-value* migration targets)
- **Held-out:** 20 additional specimens reserved for Arm B's rejected-buffer iteration validation; NEVER shown to either arm during evaluation

### 5.1 Fixture canonical home — REVISED 2026-05-28

**Canonical home for SKILL.md frontmatter fixtures:** `~/000-projects/claude-code-plugins/tests/fixtures/skill-frontmatter/<sha>/`.

**Why this and not `intent-eval-lab/research/`:** the claude-code-plugins repo already has test infrastructure (`tests/TESTING.md`, RTM, PERSONAS, JOURNEYS) + a required CI check (`validate-plugins.yml`) that runs fixtures on every PR. Fixtures live where CI consumes them — no symlinks, no drift. This also makes the Phase A.0 corpus directly available as regression tests for `validate-skills-schema.py` (the 7 global `~/.claude/skills/validate-*` skills get fixtures by transitive coverage).

**SAK alignment:** this canonical home is the first wave of the SAK § 14.10 `ackp` fixtures-discipline bead (240 fixtures across 6 authoring contracts). Phase A.0 lands wave 1 (60 SKILL.md frontmatter specimens); SAK Phase 1 schema ship adds waves 2–6 for the other 5 contracts under sibling buckets (`tests/fixtures/plugin-manifest/`, `tests/fixtures/agent-definition/`, `tests/fixtures/mcp-config/`, `tests/fixtures/hook-config/`, `tests/fixtures/marketplace-catalog/`).

**Fixture file layout (per specimen):**

```
tests/fixtures/skill-frontmatter/<sha8>/
├── input.md            # the SKILL.md file (frontmatter + body)
├── expected.json       # validator's expected verdict (schema below)
├── label.txt           # short human label (e.g., "marketplace-passing-with-disallowed-tools")
└── provenance.json     # source plugin path, sampling seed, stratum, capture timestamp
```

**`expected.json` schema (the regression-test contract):**

```jsonc
{
  "fixture_sha": "sha256(input.md)",
  "validator_version": "3.7.0",
  "validator_commit": "7b9eb8f",
  "tiers": {
    "standard":    { "pass": true,  "score_pct": 100, "findings": [] },
    "marketplace": { "pass": false, "score_pct": 62,  "findings": [{ "field": "version", "severity": "ERROR", "code": "MISSING_REQUIRED" }] },
    "deep":        { "pass": false, "score_pct": 48,  "findings": [/* ... */] }
  },
  "field_completeness": 5,
  "deprecated_field_count": 1,
  "security_finding_count": 0,
  "is_extras_present": 2
}
```

**`intent-eval-lab/research/phase-a-0-baseline/corpus/manifest.json`** retains the *sampling decisions*: which 60 of the 3,044 we picked, stratum assignment, RNG seed, held-out 20-set fixture SHAs. This is the experimental record — fixtures are the artifacts CI consumes.

Manifest + first 60 fixtures: Session 2 deliverable.

## 6. Replication discipline

1. **Pre-register** corpus + sampling seed + K-sweep values + acceptance-gate predicate + projected-lift target BEFORE any API call. File as `corpus/PRE-REGISTRATION-<sha>.md`. Hash-pin via `audit-harness init` once finalized.
2. **Single judge version:** all scoring uses validator at commit `7b9eb8f` (D4 merge). Re-runs after subsequent validator changes are explicitly versioned + reported separately.
3. **Determinism:** temperature=0.0; max_tokens fixed; seed model calls if API permits.
4. **All raw inputs + outputs persisted** to `results/<arm>/<sample>/{prompt.json,response.json,score.json}` content-addressed by SHA. Append-only per AC-2.
5. **No silent retries** — failed API calls land in `results/errors.jsonl` and the sample is excluded from headline stats (reported separately).

## 7. Cost ceiling (DR-028 plan-033 § 14.4 binding)

- **Mean per sample:** $50 ceiling (Refiner mechanism, full pass with up-to-3 iterations + judge)
- **Max per sample:** $200 ceiling (Wave B outlier handling)
- **Total Wave B budget:** $35,000 (Phase 4 migration corpus; Phase A.0 is a tiny prefix)
- **Phase A.0 estimated burn:**
  - Arm A: 60 samples × 4 K-values × ~2K tokens × Opus = ~$120
  - Arm B: ~10 samples × Refiner pass (avg 2 iterations × 2K tokens) × Opus = ~$40
  - **Total Phase A.0 budget: $200 hard ceiling.** Stop the experiment if burn exceeds. File AAR + remediation bead.

## 8. Output deliverables (Session N final)

1. `RESULTS.md` — score deltas + decision (descope or proceed) + confidence intervals
2. `BLOG-DRAFT.md` — VP DevRel binding (DR-028): publish regardless of outcome
3. `AAR.md` — per § 13 Step 8 phase-exit pattern
4. Updated `031-PP-PLAN-...` or follow-on amendment if H₀ holds
5. Closed bead `bd_000-projects-214c.8` with link to RESULTS

## 9. Open items requiring CTO resolution BEFORE Session 2 begins

| # | Question | Recommendation |
|---|---|---|
| Q1 | Numeric projected-Refiner-lift pre-registration value | 1.5pp marketplace-tier score lift |
| Q2 | API budget approval ($200 hard ceiling) | Approve via DR-BAND amendment |
| Q3 | Anthropic API key location for harness scripts | Confirm `pass anthropic/api-key` or env var path |
| Q4 | Where to commit experiment artifacts (gitignore policy) | `results/raw/` gitignored; `results/aggregated/` committed |
| Q5 | Pre-register vs adaptive on K-sweep ({0,3,8,16}) | Pre-register; no mid-experiment expansion |

## 10. What this session (Session 1) produces

This DESIGN.md (the document you are reading) + the harness directory tree at `phase-a-0-baseline/`. **Nothing else.** No API calls. No score generation. No corpus sampling. The next session begins ONLY after Q1–Q5 are answered.

---

— Jeremy Longshore
intentsolutions.io
