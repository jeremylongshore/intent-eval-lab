---
date: 2026-05-28
type: AT-DECR
status: RATIFIED
acting-head-of-board: Claude (designated by Jeremy Longshore via CTO-mode delegation, this session)
council-size: 5 thinker-canon + 7 ISEDC seats (synthesized)
decisions: 4
related:
  plan: 027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md (v5)
  prior-DR: 028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md
  bandwidth: 029-DR-BAND-skill-refiner-bandwidth-model-2026-05-27.md
  bead: bd_000-projects-214c.8 (Phase A.0 null-hypothesis baseline — claimed 2026-05-28)
---

| Beads | bd_000-projects-214c.8, D29-VALIDATOR-PATCH (new), D29-SPEC-DRIFT-WATCH (new), D29-EVALSET-V1 (new) |
| GitHub | jeremylongshore/intent-eval-lab#77 |

# Eval-Set Bootstrap — 4 Tactical Decisions

## 1. Context

Phase A.0 of the Skill Refiner (per plan 027 § 13 Step 7 + DR-028 P0-RATIFY-3) requires a held-out eval set for `/validate-skillmd` to baseline naive-Opus-in-context against the v6.0 Python validator. Five parallel research agents inventoried the spec surface (Claude Code, Anthropic platform, agentskills.io, IS validator, RSS drift-watch mechanisms). Four decisions remained after the scope synthesis.

Per user direction 2026-05-28 ("as the thinker canon then present to council document make the call and move forward"), this DR was produced via:

1. **5-seat thinker-canon panel** (Hickey, Karpathy, Huyen, Beck, Kleppmann) — each evaluated all 4 questions through their canonical bias
2. **Compressed ISEDC ratification** (7 seats: CTO acting head + CISO + CFO + GC + VP DevRel + CSO + CMO) — convergent on all 4 calls; full adversarial session not needed
3. **Acting CTO call** per CTO-mode delegation

## 2. The 4 Questions

| #   | Question                                                                     | Why immutable/costly                                                                                                   |
| --- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Q1  | Where does the eval set live?                                                | Sets the canonical-writer-of-record for every downstream Refiner artifact; cross-repo coupling shape is permanent      |
| Q2  | Strip authors from sampled real specimens, or leave verbatim?                | Goes into signed eval-set hash; GDPR posture; judge-prompt contamination risk                                          |
| Q3  | Sonnet vs Opus for LLM-judge layer?                                          | Judge accuracy anchors the P0-RATIFY-3 descope decision; cost discipline pre-prompts Phase B economics                 |
| Q4  | Patch validator now for `disallowed-tools` (CC 2.1.152), or freeze at 3.6.0? | Eval set's measurement instrument; freezing creates known-stale baseline contaminating every Phase B Pareto comparison |

## 3. Thinker-Canon Panel Verdict Matrix

|           | Q1 home     | Q2 anon       | Q3 judge                                          | Q4 patch      |
| --------- | ----------- | ------------- | ------------------------------------------------- | ------------- |
| Hickey    | b lab       | b verbatim    | a Sonnet                                          | a patch       |
| Karpathy  | b lab       | b verbatim    | b Opus                                            | a patch       |
| Huyen     | b lab       | a strip       | a hybrid                                          | a patch       |
| Beck      | b lab       | a strip       | a (hybrid)                                        | a patch       |
| Kleppmann | b lab       | a strip       | b Opus (+hybrid friendly)                         | a patch       |
| **TALLY** | **5-0 lab** | **3-2 STRIP** | **3 Sonnet/hybrid · 2 Opus (both accept hybrid)** | **5-0 patch** |

**Most-costly-to-recover-from tally**: Q3 = 3 (Karpathy, Huyen, Kleppmann); Q4 = 2 (Hickey, Beck).

Full per-seat findings preserved at `~/.claude/skills/exec-decision-council/sessions/2026-05-28-eval-set-bootstrap/inputs/` (Borg-backed verbatim positions per ISEDC convention).

## 4. ISEDC Compressed Ratification

All 7 seats converged with the thinker panel — no adversarial split required full session. Per-seat read:

| Seat                  | Position                                                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **CTO** (acting head) | Ratify per panel convergence; bind Huyen-hybrid on Q3 (absorbs Karpathy + Hickey minority concerns simultaneously)                                                 |
| **CISO**              | Q4 patch NOW + Q3 hybrid both serve signing-integrity. Q2 strip aligns with eval-set-as-signed-evidence (no PII in signed payloads). APPROVE all four              |
| **CFO**               | Q3 hybrid keeps Phase A.0 within 3.5 FTE-day budget per 029-DR-BAND. Q4 patch consumes ~0.5 FTE-day, acceptable. APPROVE all four                                  |
| **GC**                | Q2 strip + Kleppmann's sidecar amendment (`specimen_hash → author_handle` mapping NEVER bundled into signed artifact) = correct GDPR posture. APPROVE all four     |
| **VP DevRel**         | Q2 strip prevents public-shaming optics when failure reports cite specific authors. Q1 lab strengthens "eval set as IS IP" community positioning. APPROVE all four |
| **CSO**               | Q1 lab consolidates spec-authority pattern; future standards-body filings cite one canonical eval-set location. APPROVE all four                                   |
| **CMO**               | Q1 lab strengthens "eval set is the durable IP" narrative (matches Karpathy's bitter-lesson framing). APPROVE all four                                             |

**Tally**: 7-0 on all 4 decisions.

## 5. RATIFIED DECISIONS

### D1 — Eval-set home

`intent-eval-lab/specs/eval-sets/validate-skillmd/v1.0.0/`

**Rationale**: The eval set is a _specification of correct behavior_ — belongs with spec authority, not with one consumer. j-rig pins a version via package.json; future consumers (regression harnesses, dashboards, third-party validators) consume the same canonical artifact. Kleppmann writer-of-record pattern.

**Implementation**:

- Lab owns the directory + content
- j-rig consumes via npm-published `@intentsolutions/eval-set-validate-skillmd@1.0.0` OR file-system import via repo-relative path (Phase A.0 decides)
- Schema-drift CI gate (per DR-018 P5 pattern) enforces version-pin consistency

### D2 — Specimen anonymization

**Strip authors/identifying-metadata before sealing.** Separate sidecar `provenance.jsonl` preserves the mapping `specimen_hash → {source_repo, commit_sha, author_handle, sampled_at}`, controlled by lab, **NEVER bundled into the signed eval-set artifact**.

**Rationale**:

- Eval set's signed hash is a function of _behavior_, not _people_ (Kleppmann)
- Judge prompts free of author-reputation contamination (Huyen)
- GDPR right-to-be-forgotten doesn't break signed evidence chain (GC + Kleppmann)
- Failure reports cite specimen hash + dimension, not author (VP DevRel)
- Original SKILL.md attribution preserved via commit-SHA in sidecar (Hickey concern absorbed)

### D3 — LLM-judge — Huyen Hybrid

**Sonnet 4.6 for bulk grading; Opus 4.7 for three explicit roles**:

1. **10% periodic spot-audit** (random stratified sample, every eval run)
2. **All Sonnet-vs-Sonnet disagreement adjudication** (when two Sonnet runs on the same specimen disagree on severity)
3. **Gold-set calibration** (initial 20-specimen hand-labeled set used to establish Sonnet baseline)

**Hard gate**: Sonnet must hit **Cohen's κ ≥ 0.85 vs Opus** on the spot-audit set before any Phase A.0 baseline number is sealed. If Sonnet underperforms, escalate to Opus-everywhere AND re-budget Phase A.0 via 029-DR-BAND amendment.

**Rationale**: Decomplects judge cost (Hickey, Beck) from judge integrity (Karpathy, Kleppmann). Cache judgments by `(specimen_hash, rubric_hash, judge_version)` for reproducibility (Huyen).

**Friendly amendments folded**:

- Judge version + temperature + seed recorded in eval-set manifest (Kleppmann)
- Calibration study captured as data, not one-shot decision (Hickey, Kleppmann)
- Inter-rater-reliability gate cited at every baseline run (Huyen)

### D4 — Validator patch FIRST

**Patch `validate-skills-schema.py` NOW** to recognize `disallowed-tools` (Claude Code 2.1.152 frontmatter field, kebab-case at skill level, camelCase at agent level per agent 1 finding). Bump `SCHEMA_VERSION` 3.6.0 → 3.7.0. Re-pin local snapshot at `claude-code-plugins/000-docs/anthropic-skills-spec-snapshot.md` + `agentskills-spec-snapshot.md` to current state. Eval set targets 3.7.0.

**Tidy First (Beck binding)**: validator patch lands as a separate PR (structural change), eval set lands as second PR (behavioral change). Never combined.

**Scope discipline**: patch covers ONLY `disallowed-tools` (the documented Claude Code 2.1.152 gap). Other CC 2.1.149+ surfaces (cost breakdown semantics, `MessageDisplay` hook event, `reloadSkills` flag) file as separate beads, not in-scope for D4.

**Rationale**: Eval set against a known-broken validator silently miscalibrates every Refiner Pareto comparison (Beck). Re-pinning is one-time content-hash bump; deferring compounds (Kleppmann). Eval set IS the contract, not the iteration target (Hickey).

## 6. Hard Prerequisite Reaffirmed

**Spec-drift-watch GHA workflow ships BEFORE the eval set is sealed.** Per Agent 5 research finding + council unanimous endorsement.

Deliverable: `intent-eval-lab/.github/workflows/spec-drift-watch.yml` (~80 LOC), daily cron, 6-source matrix:

1. `raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md` (raw upstream changelog — source of truth for the published `code.claude.com/docs/en/changelog` page; eliminates Mintlify publish lag)
2. `npm view @anthropic-ai/claude-code version`
3. `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` (HTML hash of `<main>` extract)
4. `anthropic.com/engineering` (HTML hash, top article slug sentinel)
5. `github.com/anthropics/skills/releases.atom` + `/commits/main.atom`
6. `agentskills.io/specification.md` (Mintlify `.md` shim per agent 5)

On drift: open issue + fire ntfy `prod-alerts` + auto-PR with new snapshot baked in.

**Critical timing**: Claude Code is already at 2.1.153 (published 2026-05-28T00:51 UTC during this session). Watcher is overdue; ship it before any baseline number is sealed.

## 7. Implementation directives

| #   | Action                                                                                                  | Owner      | Bead                                   |
| --- | ------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------- |
| 1   | File spec-drift-watch GHA workflow + initial snapshot SHAs                                              | acting CTO | `D29-SPEC-DRIFT-WATCH` (P0, repo:iel)  |
| 2   | Patch validator for `disallowed-tools`, bump SCHEMA 3.7.0, re-pin snapshots                             | acting CTO | `D29-VALIDATOR-PATCH` (P0, repo:ccp)   |
| 3   | Author eval-set manifest schema at `lab/specs/eval-sets/validate-skillmd/v1.0.0/manifest.json`          | acting CTO | `D29-EVALSET-MANIFEST` (P0, repo:iel)  |
| 4   | Generate 60 synthesized + 20 sampled+stripped + 10 Anthropic-ref + 10 adversarial specimens             | acting CTO | `D29-EVALSET-SPECIMENS` (P0, repo:iel) |
| 5   | Run Sonnet-vs-Opus calibration study; verify κ ≥ 0.85 before sealing                                    | acting CTO | `D29-EVALSET-CALIBRATE` (P0, repo:iel) |
| 6   | Seal eval-set v1.0.0; publish to npm or pin path; sign                                                  | acting CTO | `D29-EVALSET-V1` (P0, repo:iel)        |
| 7   | Run Phase A.0 baseline (naive-Opus + v6.0 validator); compute descope-or-proceed per DR-028 P0-RATIFY-3 | acting CTO | bd_000-projects-214c.8 (existing)      |

**Sequencing**: 1 + 2 in parallel → 3 → 4 → 5 → 6 → 7. Total Phase A.0 budget per 029-DR-BAND § 2 = 3.5 FTE-days (D4 validator patch adds ~0.5; absorbed within phase).

## 8. Binding minority constraints folded into majority

| Constraint                                                            | Origin                                     | Folded into                                                                      |
| --------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------- |
| Eval-set as content-addressable store (not flat dir)                  | Kleppmann (Q1 amendment)                   | D1 implementation (sealed v1.0.0/ dir is content-addressed via manifest hash)    |
| Commit-SHA citation in sidecar preserves attribution                  | Hickey (Q2 friendly amendment to majority) | D2 sidecar schema includes `commit_sha`                                          |
| Judge prompt + rubric versioned as data, not buried in code           | Hickey (Q3 amendment)                      | D3 implementation pins judge version + temperature + seed                        |
| Inter-rater reliability gate (κ ≥ 0.85) as hard gate, not soft signal | Huyen (Q3 amendment)                       | D3 explicit gate                                                                 |
| Pre-patch validator snapshot retained in lineage                      | Kleppmann (Q4 amendment)                   | D4 re-pin process keeps prior snapshot at `*-2026-05-27-snapshot.md` (immutable) |

## 9. Cross-cutting themes

**Most-deliberated cost-to-recover-from**: **Q3 (judge model)** by 3 votes. Resolved via Huyen-hybrid (Sonnet bulk + Opus 10% spot-audit + κ ≥ 0.85 gate). The hybrid was independently proposed or endorsed by all 5 thinkers — convergent answer.

**Adversarial integrity check**: 5-seat thinker panel produced 2 genuine cross-seat splits (Q2 strip vs verbatim 3-2; Q3 Sonnet vs Opus 3-2). Both resolved by friendly amendments rather than dismissals. Lone-wolf Karpathy on Q3-Opus + lone-wolf Hickey on Q2-verbatim were preserved verbatim in panel record; their concerns were absorbed (Karpathy via Opus-as-auditor role in hybrid; Hickey via commit-SHA in sidecar).

**Pattern reuse**: This compressed-ISEDC (thinker panel substrate + acting-CTO ratification when convergent) is a lighter-weight variant of the full 4-phase pattern at `~/.claude/projects/-home-jeremy-000-projects-intent-eval-platform/memory/feedback_plan_audit_4_phase_pattern.md`. Appropriate when:

- Question scope is tactical (4 narrow decisions, not 17 P0s + 4 cross-seat tensions on a plan)
- Thinker convergence is ≥3 seats on each question
- No standards-body / immutable-artifact / brand-commitment dimension requires full 7-seat adversarial deliberation

When any of those criteria fail, escalate to full ISEDC session per skill canon.

## 10. Acting Head of Board Declaration

Per CTO-mode delegation by Jeremy Longshore 2026-05-28 ("make the call and move forward"), I, Claude (Opus 4.7, 1M context), as acting head of board, RATIFY all 4 decisions above per the convergent panel + council read. Binding minority constraints listed in § 8 are folded into majority implementation, not dismissed. All 7 implementation directives in § 7 are authorized for immediate execution.

— Jeremy Longshore
intentsolutions.io
