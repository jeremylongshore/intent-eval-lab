# Internal Pre-Plan-Audit Review — 2026-05-27

**Trigger:** user direction "send out consistency auditors and code reviewers just to make sure everything's nice and tight" before committing/landing Steps 1-3 work.

**Reviewers (4 parallel agents, isolated context):**
1. `article-consistency-checker` — plan 027 internal consistency (thesis drift, contradictions, tone, cross-refs)
2. `architect-reviewer` — plan 027 architecture vs Blueprints A/B + DR-010/DR-018 + ecosystem
3. `code-reviewer` — `validate-trilink.sh` security + correctness
4. `fact-checker` — plan 027 citations vs cached research artifacts

**Approximate role:** these four reviews collectively approximate § 12 Plan Audit Phase 2 (parallel seat review) for the artifacts produced by Steps 1-3. They are NOT a substitute for the full § 12 7-seat audit; they are a CHEAP-FIRST pre-flight check on what's been built so far.

## Convergent P0 BLOCKERs (6 — fix-before-commit)

| # | Finding | Source reviewer | Section / line | Patch landed in this PR |
|---|---|---|---|---|
| P0-1 | L3 Hook mechanism — PostToolUse:Bash can't block already-ran bash | architect P0-1 | § 4 Phase B + D3 diagram | YES — switched to PreToolUse:Bash |
| P0-2 | Phase B ↔ Phase E circular exit-dependency | article-consistency P0-1 | § 4 Phase B exit / § 4 Phase E exit | YES — softened Phase B exit text |
| P0-3 | AC-5 (Opus-only-for-validation) vs `score()` type sig (accepts 'opus') | article-consistency P0-4 | § 4 Phase A API surface | YES — removed 'opus' from `score()` modelTier union |
| P0-4 | AC-11 over-states open-standard (9 fields claimed, spec has 6) | fact-checker E1 + spec snapshot | § 3 AC-11 | YES — adopted revised AC-11 splitting open-standard vs CC-extension layers |
| P0-5 | Shell arg-injection via `for num in $nums` (gh fallback) | code-reviewer P0-1 | `validate-trilink.sh` line ~98 | YES — added regex whitelist `[[:space:]]+` |
| P0-6 | gh-unauthenticated false-PASS on Check 3 | code-reviewer P0-2 | `validate-trilink.sh` line ~93 | YES — added `gh auth status` pre-flight |

## P1 findings — deferred to § 13 Step 5 remediation (post-§ 12 Plan Audit)

| # | Finding | Source | Section | Remediation strategy |
|---|---|---|---|---|
| P1-1 | AC-11 binds Refiner to moving external spec without fork discipline | architect P0-2 | § 3 AC-11 + § 2.5 | Amend AC-11 to "locally-forked snapshot pinned at sha256"; surface drift via quarterly bd memory |
| P1-2 | SkillVersion redefines SkillSnapshot semantics implicitly | architect P1-1 | § 4 Phase C + D5 diagram | Either explicitly amend Blueprint B § 7, OR make SkillVersion fully orthogonal (no FK to SkillSnapshot) |
| P1-3 | Two-package split (refiner-core + refiner) gratuitous | architect P1-2 | § 4 Phase A | Collapse to one package `@j-rig/refiner` with internal `src/core/` boundary enforced by lint |
| P1-4 | iec-E12 transitive chain (E12a + E12b → E12 → uprg + 9pi3) not shown | architect P1-3 | § 4.5 Ecosystem Fold matrix + D6 | Expand the matrix row; update D6 |
| P1-5 | Sample findings § 12 cite plan-section headings that don't exist | article-consistency P1.2 | § 12 Sample Findings | Add header note: "Section citations in samples are illustrative paraphrases, not direct anchors" |
| P1-6 | § 9 ≤0 BLOCKERs vs § 10 "BLOCKER remediable in 2 iterations" | article-consistency P1.3 | § 9 + § 10 | Reword § 9 to "≤ 0 unresolved BLOCKERs" |
| P1-7 | "audit-harness" vs "intent-audit-harness" inconsistent | article-consistency | Multiple | sed-replace all standalone "audit-harness" → "intent-audit-harness" except npm package + CLI binary references |
| P1-8 | "sinker/line/hook" vs "hook-line-sinker" ordering inconsistent | article-consistency | § 4 Phase B section header | Pick "sinker/line/hook" per AC-8 |
| P1-9 | Anthropic security-guidance "explicitly published" citation unverified | fact-checker E2 | § Context + AC-8 | Soften to "Anthropic ships a security-guidance plugin (local path verified); public URL unconfirmed" |
| P1-10 | \r\n line endings could corrupt validate-trilink regex matches | code-reviewer P1-3 | `validate-trilink.sh` | YES — add `tr -d '\r'` before grep (landing in this PR alongside P0 patches) |
| P1-11 | `find` symlink escape risk | code-reviewer P1-4 | `validate-trilink.sh` | YES — `find -P` flag (landing in this PR) |
| P1-12 | SkillsBench −1.3pp / +16.2pp figures unverified — load-bearing for Phase D deferral | fact-checker O1 | § Context + § 2 Phase D | Step 5 remediation: WebFetch arXiv 2602.12670; if figures don't replicate, escalate to ISEDC |

## P2 / NIT — backlog (no action this PR)

| # | Finding | Source | Action |
|---|---|---|---|
| P2-1 | § 2.5 marketing/TAM voice collision | article-consistency P1.1 | Move cross-vendor distribution language to § 8 risks |
| P2-2 | Sample findings include "Proposed remediation" — may train seats toward predetermined answers | article-consistency P2 | Add panel-protocol note OR strip remediations from samples |
| P2-3 | Phase D "deferred indefinitely" creates hidden 2-product narrative | architect P2-1 | Retire "Create" axis entirely; rebrand 3-product framing as canonical |
| P2-4 | CI gate `paths:` filter could be noisy | architect P2-2 | Tighten workflow to pre-filter label before running script |
| P2-5 | Hardcoded `UMBRELLA="/home/jeremy/000-projects"` breaks CI | code-reviewer NIT | Make it `SCRIPT_DIR`-derived |
| P2-6 | API rate-limit not bounded across CI matrix | code-reviewer P2 | Documentation-only comment |
| P2-7 | 9 frontier papers (Skill-R1, SHARP, LSE, etc.) unverified | fact-checker U1 | Cache the papers OR add "(unverified — cited from offline knowledge)" to the table |
| P2-8 | "32 tools adopting agentskills.io" and "89,753 skills on Vercel" unverified | fact-checker U3 | Add inline citation or remove the figures |
| NIT-1 | D3 ASCII diagram column alignment | architect NIT | Reflow ASCII |
| NIT-2 | User-direction quote in § 5.5 mid-spec | article-consistency NIT | Move to blockquote callout |

## Verdicts

| Reviewer | Verdict |
|---|---|
| article-consistency-checker | **AMEND-BEFORE-AUDIT** — 4 P0/P1 BLOCKERs (3 landed P0 + 1 P1 wording in this PR) |
| architect-reviewer | **AMEND-AC-11** — 2 P0 + 3 P1; 1 P0 (L3 mechanism) landed in this PR; others deferred to Step 5 |
| code-reviewer | **PATCH-BEFORE-CI-ENABLEMENT** — 2 P0 + 2 P1; ALL landed in this PR |
| fact-checker | **FIX-CITATIONS** — 1 P0 (AC-11) landed; 1 P1 (SkillsBench) deferred for WebFetch; 1 P1 (security-guidance wording) deferred to Step 5 |

## What lands in this PR

1. Plan 027 + plan 025 mods + research artifacts (3) + validate-trilink.sh
2. P0 patches: L3 mechanism switch, Phase B exit clarification, score() type sig fix, AC-11 rewrite, script hardening (auth, regex, CR strip, symlink)
3. This review summary + 4 individual reviewer reports (cached separately)
4. validate-trilink + validate-consistency reports (Step 3 output)

## What does NOT land (deferred)

- 12 P1 findings — go into § 13 Step 5 remediation queue
- 9 P2 + 2 NIT findings — backlog for Plan Audit § 12 panel to weigh
- The actual § 12 Plan Audit (7-seat thinker-canon panel review) — separate run

## Hard gate preserved

Per plan § 13 Step 7: NO `bd claim` against any Skill Refiner bead until Plan Audit § 12 STATUS.md = RATIFIED. This pre-flight review does NOT substitute for that audit; it reduces the surface the audit panel has to find.

— Claude (acting CTO)
2026-05-27
