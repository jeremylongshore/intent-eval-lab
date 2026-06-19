# Plan: Skill Refiner — Eval-Guided Improvement Loop for the Intent Eval Platform

**Codename**: snoopy-fluttering-comet
**Status**: ENHANCED 2026-05-26 (this revision supersedes the prior SkillOpt-Pattern draft; the original Section spine is preserved, with 7 new interleaved sections per user direction "enhance the plan, don't delete it")
**Owner**: Jeremy Longshore (executor: Claude as drafting CTO; user is in CTO-mode delegation per 2026-05-26 messages)
**Filed**: 2026-05-26 at `intent-eval-lab/000-docs/027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md`

| Field  | Value                                                                                                                                                                                                                                                                                           |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Beads  | bd_000-projects-rqwk (RC-IEL), bd_000-projects-brij (RC-IEC), bd_000-projects-214c (RC-IAJ), bd_000-projects-aon3 (RC-IAH), bd_000-projects-r8ir (RC-IAR), bd_000-projects-pu35 (TL-EPIC), bd_000-projects-0r8m (product epic)                                                                  |
| GitHub | jeremylongshore/intent-eval-lab#78 (RC-IEL), jeremylongshore/intent-eval-lab#79 (TL-EPIC), jeremylongshore/intent-eval-core#12 (RC-IEC), jeremylongshore/j-rig-skill-binary-eval#81 (RC-IAJ), jeremylongshore/intent-audit-harness#42 (RC-IAH), jeremylongshore/intent-rollout-gate#15 (RC-IAR) |

**Revision history (this file)**:

- 2026-05-26 v1 — original SkillOpt-Pattern draft
- 2026-05-26 v2 — j-rig Keeper / Pre-Trip / Evidence sub-product framing (superseded)
- 2026-05-26 v3 — Skill Refiner peer-product collapse (current brand canon)
- 2026-05-26 v4 — fold-in of: ecosystem-integration rigor, SkillMD/agentskills.io spec pinning, per-repo bead structure, ASCII diagram catalog, tri-linkage discipline, plan-audit phase, execution sequence
- 2026-05-27 v4.1 — P0 patches from internal pre-Plan-Audit review (`000-docs/audit/2026-05-26-plan-audit/internal-review-2026-05-27.md`): § 4 Phase B L3 mechanism `PostToolUse:Bash` → `PreToolUse:Bash` (Anthropic hooks reference: PostToolUse cannot block already-ran bash); § 4 Phase B exit criterion uncoupled from Phase E public hosting (resolves prior Phase B↔E circular dependency); § 4 Phase A `score()` `modelTier` union narrowed to `'haiku' | 'sonnet'` (AC-5 binds Opus to final-validation only); AC-11 rewritten to split open-standard layer (6 fields) from Claude Code extension layer (8 fields, including new `disallowed-tools` from v2.1.152) with locally-forked snapshots replacing moving-target external dependency. 12 P1 findings deferred to § 13 Step 5 remediation queue post-Plan-Audit § 12.
- 2026-05-27 v5 (THIS) — DR-028 amendments folded inline per `000-docs/028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md` (ISEDC Session 7 ratification + 13-thinker tension arbitration). See **§ DR-028 Amendments Index** below for the per-section change list. Phase D removed (anti-goal in Blueprint A § 3.X). AC-12 rewritten (T3 COLLAPSE consensus). New AC-13 (RefinerStrategy interface). New Phase A.0 (null-hypothesis baseline). SkillVersion entity ships with `version_kind` + `parent_version_id` + `source_snapshot_hash` (T1 DISCRIMINATOR resolution). Phase-budget weeks superseded by FTE-week model at `029-DR-BAND-skill-refiner-bandwidth-model-2026-05-27.md`. § 13 Step 7 hard gate machine-enforced via `intent-eval-lab/scripts/bd-claim-precheck.sh`.

## DR-028 Amendments Index (v5 changes — read first)

This block is the canonical pointer to the v5 deltas. The full underlying decisions live in `000-docs/028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md`. Section-level changes:

| Section affected               | Delta                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Revision history (above)       | v5 entry added                                                                                                                                                                                                                                                                                                                                                                              |
| § 3 AC-3                       | `accept()` predicate formally specified: Pareto-dominant on `behavioral` + non-regressing on all named dims + significance threshold T at α=0.05 + Pareto-incomparable → REJECT to rejected-edit buffer with reason `pareto-incomparable`. Predicate ships NORMATIVELY in `skill-refiner-pass/v1` JSON Schema (per CSO Session 7 binding).                                                  |
| § 3 AC-7                       | Operationalized via new AC-13 RefinerStrategy interface — claim no longer un-substantiated.                                                                                                                                                                                                                                                                                                 |
| § 3 AC-12                      | REWRITTEN: tri-link discipline = bd is the CANONICAL writer; GH issue bodies + doc front-matter are GENERATED PROJECTIONS via `bd-sync`; humans editing GH or doc bodies directly is a CI-detected anomaly that re-projects from bd. The 7 process disciplines (PR-1..5 + validate-trilink + spec-refresh) collapse to ONE: "bd is source; everything else is projection."                  |
| § 3 NEW AC-13                  | RefinerStrategy interface defined in `@j-rig/refiner-core/strategies/`. Phase A ships TWO reference implementations: `NaiveInContextStrategy` (also serves as Phase A.0 null-hypothesis baseline) + `SkillOptStyleStrategy` (original v4.1 propose() mechanism refactored). `refiner_strategy_id` field added to SkillVersion schema; signed in predicate payload (CISO Session 7 binding). |
| § 3.5 PR-1..5                  | COLLAPSED into single discipline per T3 consensus. PR-1 is now: "bd is the canonical writer of bead↔doc↔GH-issue cross-refs; bd-sync generates the projections." Replaces all 5 prior PR-N rules.                                                                                                                                                                                           |
| § 4 NEW Phase A.0              | Null-hypothesis bitter-lesson baseline: naive Opus-in-context vs proposed Refiner on `/validate-skillmd`. Decision rule: if naive achieves > 70% of projected Refiner lift, DESCOPE Phase B mechanism. Per VP DevRel binding: result PUBLISHED as blog post regardless of outcome. Bandwidth: 3.5 FTE-days per 029-DR-BAND. GATES Phase A.                                                  |
| § 4 Phase A                    | Inserts Phase A.0; ships RefinerStrategy interface + 2 reference impls; ships EvalSet versioning (`eval_set_version` + `lineage_parent` + `refresh_due_at`); ships eval-set quality eval (coverage/leakage/calibration/adversarial-pass-rate per Karpathy F-AK-005 binding). Bandwidth: 11.5 FTE-days (≈ 2.3 FTE-weeks) per 029-DR-BAND.                                                    |
| § 4 Phase B                    | L3 hook clarified PreToolUse:Bash per v4.1. Plugin CLI surface unchanged. Bandwidth: 9.5 FTE-days.                                                                                                                                                                                                                                                                                          |
| § 4 Phase C                    | SkillVersion entity: separate from SkillSnapshot, carries `version_kind: 'edit'                                                                                                                                                                                                                                                                                                             | 'revert' | 'restore'`+`parent_version_id`(SkillVersion → SkillVersion) +`source_snapshot_hash`(read-only reference to SkillSnapshot, NOT FK) +`refiner_strategy_id`(signed).`pending_production`intermediate state for sigstore Rekor outages; outbox + reconciler pattern with`retry_after`+`max_retries: 5`+`signing_failed`surfacing. Cross-field invariant amended:`rekor_log_index non-null iff signing_mode='production' AND status='active'`. Bandwidth: 15 FTE-days, gated on `uprg`+`9pi3` close. |
| § 4 Phase D                    | REMOVED. Anti-goal language lives in Blueprint A § 3.X amendment per DR-028 T2 majority (12 of 14 voices). Re-opening trigger per Karpathy + Gregg minority: `self-gen lift > +8pp on kernel-pinned eval set on any frontier release, OR internal acceptance rate parity`. ISEDC reconvenes if observed.                                                                                    |
| § 4 Phase E                    | Unchanged. Bandwidth: 4.5 FTE-days concurrent with Phase B.                                                                                                                                                                                                                                                                                                                                 |
| § 4 NEW AAR-cadence subsection | Per Cunningham F-WC-001: post-phase-exit AAR + quarterly mini-review + post-incident (≤7 days) retrospective. Discipline that produced AAR-023's 9+ findings and this very Plan Audit's 46 findings.                                                                                                                                                                                        |
| § 4 "~N weeks" phase budgets   | All superseded by FTE-week model at `029-DR-BAND-skill-refiner-bandwidth-model-2026-05-27.md`. Aggregate: ~8.8 FTE-weeks ≈ ~3 calendar months (bandwidth + sync + external-blocker wait).                                                                                                                                                                                                   |
| § 4.5 Ecosystem Fold matrix    | `iec-E12` row expanded to show transitive chain `E12a + E12b → E12 → uprg + 9pi3 → Phase C` per Cunningham F-WC-005 dependency-direction-honesty binding.                                                                                                                                                                                                                                   |
| § 5.5 validate-trilink.sh      | Simplified per T3 collapse: Check 1 (bead carries Doc + GitHub fields) stays; Checks 2 + 3 demoted to advisory-only (they check generator output).                                                                                                                                                                                                                                          |
| § 6.5 D5 ER diagram            | Updated to show SkillVersion as separate entity from SkillSnapshot with `source_snapshot_hash` as a reference (not a FK arrow); `version_kind` discriminator shown as a typed enum field.                                                                                                                                                                                                   |
| § 8 Risks                      | New rows: "Bandwidth model under-estimated" (mitigated by per-phase re-validation); "External blockers `uprg`/`9pi3` not closed before Phase C kickoff" (mitigated by A+B-as-v0.1.0 fallback).                                                                                                                                                                                              |
| § 13 Step 7                    | Hard gate now MACHINE-ENFORCED via `intent-eval-lab/scripts/bd-claim-precheck.sh` (P0-RATIFY-4). DR-028 partial-lift authorized 6 shorthands; external-contributor PRs see CI WARNING + contributor-acknowledgment (not hard block) per VP DevRel binding.                                                                                                                                  |

**T4 brand framing resolution (DR-028):** Skill Refiner stays as a NAMED product in the 3-product agent-rig stack (Test → Improve → Ship). The "eval is the product" framing (thinker-majority architectural truth) lives in Blueprint A as the internal architectural reality but does NOT override consumer-facing 3-product brand. AC-7 + AC-13 are the engineering bridge. CMO + CFO + VP DevRel business-axis trio overrode thinker-majority on brand-instability + developer-mental-model grounds.

**Filing-number reservations adjusted from in-conversation draft**:

- This plan: `027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` (was tentatively unreserved)
- Future doc — skill-refiner-pass/v1 predicate spec: `028-AT-SPEC-skill-refiner-pass-v1-predicate.md` (was 027 in draft)
- Future doc — skill-refiner 3-layer hooks architecture: `029-AT-ARCH-skill-refiner-3-layer-hooks.md` (was 028 in draft)
- Future doc — tri-linkage discipline standard: `030-AT-STND-tri-linkage-discipline.md` (was 029 in draft)

**Scope**: Design + roadmap the **Skill Refiner** product — the second product in the Intent Solutions 3-product agent-rig stack (J-Rig Skill Binary Eval → Skill Refiner → Rollout Gate). Eval-guided improvement loop that proposes safe, minimal SKILL.md edits and accepts only on strict score improvement. Delivered as a Claude Code plugin with 3-layer hooks (sinker/line/hook); emits signed evidence reports (md + HTML); integrates as the 14th canonical kernel entity (SkillVersion) + new predicate URI (skill-refiner-pass/v1). Folds additively into the existing 5-repo IEP ecosystem.

**Decision basis**: User-confirmed across multiple AskUserQuestion rounds 2026-05-26 (philosophy=refiner-primary + creator-deferred-indefinitely; IEP integration=Tier-1; report shape=md+HTML; MVP-to-scale roadmap; ecosystem-fold-not-fork; tri-linkage doc↔bead↔GH-issue mandatory; per-repo bead clusters via labels in umbrella workspace).

---

## Context — why this plan exists

The 2026-05-22 SkillOpt arXiv paper (`2605.23904`) proposes a text-space optimizer for agent skills with the structural template: separate optimizer model → bounded add/delete/replace edits on a skill doc → edit accepted only if held-out validation score strictly improves. Anthropic's security-guidance plugin (`code.claude.com/docs/en/security-guidance`, released ~2026-05) is the canonical hook-based template for "spawn separate model call from a hook, feed findings back to session" — Anthropic explicitly publishes its source as the reference implementation for this pattern.

The two compose. SkillOpt's mechanism + security-guidance's hook architecture = a Claude Code plugin that performs evals-gated skill edits in-session. The user owns `claude-code-plugins` (2000+ stars, 30+ human-curated skills, ~45k npm downloads), the IEP ecosystem (kernel + lab + audit-harness + j-rig + rollout-gate), and j-rig is the canonical 7-layer skill evaluator that already produces `gate-result/v1` Evidence Bundle rows with scores. **Every piece needed to build the Skill Refiner already exists; the work is composition, not new infrastructure.**

Per DR-010 § 13.6 (external-pattern non-borrow): cited prior art informed the design space but does not dictate the architecture. Skill Refiner is IS-native; SkillOpt + security-guidance + SkillsBench are referenced for reproducibility, not borrowed for branding.

**Frontier-landscape context (Phase 1 deep-dive, May 2026):**

| Paper                                                        | Date       | Mechanism                                                                                                          | Relevance                                                                                                             |
| ------------------------------------------------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| **SkillOpt** (arXiv 2605.23904)                              | 2026-05-22 | Text-space SGD-style optimizer; bounded edits + held-out-strict-improvement gate; rejected-edit buffer             | Primary reference (re-ingest per user direction)                                                                      |
| **Skill-R1** (arXiv 2605.09359)                              | 2026-05-10 | RL bi-level GRPO; intra+inter-generation advantage; lightweight skill generator conditions frozen task LLM         | Direct competitor — different optimizer technique (RL vs text-space SGD); same "frozen agent + external state" thesis |
| **SHARP** (arXiv 2605.06822)                                 | 2026-05-07 | Self-Evolving Human-Auditable Rubric Policy; bounded symbolic rule edits + walk-forward validation                 | Architectural analog in finance domain; identical "policy drift → bounded structured edits" pattern                   |
| **Learning to Self-Evolve (LSE)** (arXiv 2603.18620)         | 2026-03-19 | RL trains 4B model to evolve its own contexts; beats GPT-5 + Sonnet 4.5 + GEPA + TextGrad on prompt-opt benchmarks | Direct competitor; **4B beats Sonnet 4.5** is a bitter-lesson alarm                                                   |
| **Skill-CMIB** (arXiv 2605.08526)                            | 2026-05-08 | Multimodal skill construction via Conditional Multimodal Information Bottleneck                                    | Adjacent — multimodal generalization vector                                                                           |
| **Skill-Pro** (arXiv 2602.01869)                             | ~2026-02   | Non-Parametric PPO + PPO Gate + Semantic Gradients                                                                 | Adjacent — "PPO Gate Pass Rate" is the same idea as held-out-strict-improvement                                       |
| **CUA-Skill** (Microsoft, arXiv 2601.21123)                  | 2026-01    | Computer-use agent skill library; 57.5% on WindowsAgentArena                                                       | Industry investment — Microsoft is investing here                                                                     |
| **EvoFSM** (arXiv 2601.09465)                                | 2026-01-14 | Self-evolving via Finite State Machine (constrained) instead of free-form rewriting                                | Adjacent — same "unconstrained = drift" problem, different shape (FSM)                                                |
| **AgenticRecTune** (arXiv 2604.26969)                        | 2026-04-21 | Multi-agent + Self-Evolving Skillhub for recommendation systems                                                    | Adjacent industry application                                                                                         |
| **SkillsBench** (Microsoft + 40 authors, arXiv 2602.12670)   | ~2026-02   | Benchmark: how well do agent skills work across tasks                                                              | **CRITICAL FINDING** — see below                                                                                      |
| **Generate-Filter-Control-Replay** survey (arXiv 2605.02913) | 2026-05-08 | 23-author survey framing the rollout-strategy space                                                                | Field-mapping document                                                                                                |

**The most strategically important finding from the deep-dive — SkillsBench:**

> _"Skills provide substantial but variable benefit. Skills improve performance by +16.2pp on average across 7 model-harness configurations… Self-generated Skills provide negligible or negative benefit. When prompted to generate their own procedural knowledge before solving tasks, models achieve −1.3pp on average compared to the no-Skills baseline… effective Skills require human-curated domain expertise that models cannot reliably self-generate."_

**This is the IP-defense argument for `claude-code-plugins`'s 30+ human-curated skills.** Human-curated skills give +16.2pp; self-generated give −1.3pp (NEGATIVE). The role of the Skill Refiner is **NOT to replace human curation but to refine it via evals-gated edits**. SkillsBench provides the empirical baseline that justifies the single-product positioning: the Refiner is anchored on the +16.2pp curated baseline; the deferred creator sub-product would have had to beat the −1.3pp self-generated baseline before any skill ships.

**Action: re-ingestion of SkillOpt paper (per user direction 2026-05-26)** — the paper is NOT currently cached locally (Phase 1 exploration confirmed). § 13 Execution Sequence Step 0 includes a WebFetch of the paper to pin its citations against this plan's claims and to surface any details from the 23-page document not captured in this Context.

---

## 1. Carry-over from prior plan (release sweep) — incomplete items

The release sweep (steps 0-7 of prior plan) is COMPLETE. Three items were explicitly deferred via the `iep-gist-coverage` follow-up bead. They are folded into Phase A of this plan:

| Item                                                                                                                      | Status   | Carry into                                                        |
| ------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------- |
| `/gist-auditor --repo j-rig-binary-eval` on existing gist `d1c4570a8dd54cba6517c56a3dae17f5`                              | DEFERRED | Phase A pre-flight                                                |
| Regenerate j-rig gist with v1.1.0 content (per old plan Step 4 Phase 7.5)                                                 | DEFERRED | Phase A pre-flight                                                |
| `iep-gist-coverage` bead's 4 missing gists (intent-audit-harness, intent-eval-core, intent-eval-lab, intent-rollout-gate) | DEFERRED | Phase E — Reports/Brand surface (quality-over-speed per CTO call) |

---

## 2. Product structure

Per user brand-canon ratification 2026-05-26, this is the **3-product Intent Solutions agent-rig stack**:

| Product                                                | Lifecycle role                                                                            | Status                                      | Output                                    |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------- |
| **J-Rig Skill Binary Eval**                            | TEST — evaluates skill behavior across 7-layer taxonomy                                   | SHIPPED (existing)                          | Behavioral ScoreRecord                    |
| **Skill Refiner** (THIS PLAN)                          | IMPROVE — proposes safe, minimal SKILL.md edits, accepts only on strict score improvement | NEW — this buildout                         | Refined SKILL.md + signed evidence report |
| **Rollout Gate** (`intent-rollout-gate`, M5 in flight) | SHIP — CI ship/no-ship decision from Evidence Bundle + policy                             | EXISTING (M5 substantive runtime in flight) | Ship/no-ship verdict                      |

User's brand positioning: _"Skill Refiner is the eval-guided improvement loop that proposes safe, minimal changes to a SKILL.md until it passes the rollout gate without regressing sacred tests."_

### Skill Refiner internal structure (one product, three engineering facets)

Engineering structure is 3 epics; consumer-facing surface is ONE product:

| Facet                                    | Engineering home                                                                            | Role                                             | Visible as         |
| ---------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------ | ------------------ |
| **Refiner core loop**                    | `@j-rig/refiner-core` + `@j-rig/refiner` (two-package split per § 6)                        | The bounded-edit propose+accept loop             | Internal — library |
| **3-layer hooks** (hook · line · sinker) | `claude-code-plugins/plugins/productivity/j-rig/`                                           | Delivery mechanism inside Claude Code            | Internal — plugin  |
| **Signed evidence reports**              | `intent-eval-lab/specs/skill-refiner-evidence-report/` + Hugo template in `partner-portals` | Output artifact (markdown AAR + HTML projection) | Internal — output  |

**Creator sub-product (would generate NEW skills from scratch)**: DEFERRED INDEFINITELY at P3. SkillsBench evidence: self-generated skills underperform no-skill baseline. Re-open trigger: (a) external work demonstrates the bar can be cleared OR (b) a partner explicitly asks AND accepts the risk profile. Until then: no code, no design, no marketplace listing. Filed as standalone deferred bead `bd_000-projects-vbqp`.

---

## 2.5. SkillMD Avenue — Agent Skills Open Standard fold-in

**Per user direction 2026-05-26**: "Given the new information we got that was published the other day in regards to the SkillMD, is there any new avenue of approach that we might want to implement with all of our ecosystem now?"

**Resolution (Plan agent investigation):** "SkillMD" maps to the **Agent Skills Open Standard** at `agentskills.io/specification` — the SKILL.md file format Anthropic published December 2025, since adopted by ~32 tools (Claude Code, Codex CLI, Gemini CLI, Cursor, VS Code Copilot, Junie, Kiro, Goose, Cline, Windsurf, OpenCode). The "published the other day" reference likely points to one of: (a) a recent spec revision at `agentskills.io/specification`, (b) the Anthropic `skills/spec/agent-skills-spec.md` in `github.com/anthropics/skills`, (c) a recent adoption announcement (Vercel's `skills.sh` marketplace claims 89,753 skills as of May 2026), or (d) a `paperclipped.de` interoperability writeup. **Research item carried into § 13 Step 0 — confirm specific publication via WebFetch.**

### Why this matters for Skill Refiner

The Refiner edits SKILL.md files. Until now the plan treated SKILL.md as Claude-Code-specific. Under the open standard, **a SKILL.md is a portable cross-vendor artifact** — refining one improves it on Codex CLI, Gemini CLI, Cursor, Junie, Kiro, Goose, VS Code, Cline, and Windsurf simultaneously. This is a force-multiplier for the 3-product narrative: Test → Improve → Ship now operates across ~32-tool surface area, not one.

### Fold-in mandates (binding constraints added to the plan)

1. **Spec compliance gate (NEW Architectural Commitment AC-11)**: The Refiner's edit grammar (add/delete/replace ops) must respect the `agentskills.io/specification` frontmatter requirements: required `name` + `description`, optional `allowed-tools`, `disallowed-tools`, `model`, `version`, `author`, `license`, `compatibility`, `tags`. The L1 Sinker hook extends `/validate-skillmd` Tier 2 to validate against the **published spec snapshot pinned in the Refiner repo** (not against a moving target).
2. **Spec version pinning in every SkillVersion record (NEW)**: extend the SkillVersion entity schema (§ 4 Phase C) to include `skill_md_spec_version: "agentskills.io/v1.0.0"` (or whatever the current spec version resolves to in § 13 Step 0). When the spec revs, refiner runs become traceably bound to the spec generation that produced them.
3. **Portability claim per Refiner pass (NEW)**: each Refiner pass publishes "this skill validated against Claude Code, Codex CLI, Gemini CLI parsers" — done via the existing `/validate-plugin` skill's cross-harness compatibility check (already in user's skill arsenal). Failure on any parser surface is a P2 finding in the Evidence Report, not a BLOCKER (different harnesses may differ on optional fields).
4. **Cross-vendor distribution channel option (NEW market consideration)**: refined skills become potentially distributable across multiple marketplaces (Vercel skills.sh, Anthropic skills marketplace, etc.) rather than `claude-code-plugins` only. This expands TAM but adds distribution-policy complexity; deferred to Phase F (out of scope here; flagged for future ISEDC decision).

### Canonical spec URL inventory (per user direction 2026-05-26: incorporate the validate-\* + skill-creator skill family's authoritative references)

The Refiner edits SKILL.md, plugin.json, hooks.json, marketplace.json, agents/\*.md, and .mcp.json artifacts. Each artifact has a canonical spec. The user's existing validator skill family is already grounded in these specs — the Refiner MUST reuse the same anchors. **No re-deriving spec details; cite the same URLs the validators cite.**

| Spec domain                             | Canonical URL                                                                                                                                                                        | Validator(s)                                     | What it specifies                                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| SKILL.md Frontmatter (Anthropic)        | `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`                                                                                                         | validate-skillmd, skill-creator                  | Required fields (name, description); optional fields per Anthropic                                |
| SKILL.md Best Practices (Anthropic)     | `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`                                                                                                   | validate-skillmd                                 | Progressive disclosure, degrees of freedom, evaluation guidance                                   |
| Claude Code Skills Reference            | `https://code.claude.com/docs/en/skills`                                                                                                                                             | validate-skillmd, validate-plugin, skill-creator | Skills as component, triggering, invocation control, frontmatter extensions                       |
| Claude Code Frontmatter Extensions      | `https://code.claude.com/docs/en/skills#frontmatter-reference`                                                                                                                       | skill-creator                                    | Platform-specific fields (argument-hint, disable-model-invocation, context, agent, effort, hooks) |
| Claude Code Skill Invocation Control    | `https://code.claude.com/docs/en/skills#control-who-invokes-a-skill`                                                                                                                 | skill-creator                                    | User invocation, background knowledge only, explicit triggers                                     |
| SKILL.md Open Standard (AgentSkills.io) | `https://agentskills.io/specification`                                                                                                                                               | validate-skillmd, validate-plugin, skill-creator | Interoperable SKILL.md format                                                                     |
| Plugin Manifest (Anthropic)             | `https://code.claude.com/docs/en/plugins-reference`                                                                                                                                  | validate-plugin                                  | plugin.json schema, all 10 component types                                                        |
| Plugin Overview (Anthropic)             | `https://code.claude.com/docs/en/plugins`                                                                                                                                            | validate-plugin                                  | Plugin authoring, structure, conventions                                                          |
| Plugin Marketplaces (Anthropic)         | `https://code.claude.com/docs/en/plugin-marketplaces`                                                                                                                                | validate-plugin, validate-marketplace            | marketplace.json schema, catalog structure, source types                                          |
| Sub-agents / Agents (Anthropic)         | `https://code.claude.com/docs/en/sub-agents`                                                                                                                                         | validate-plugin, validate-agent                  | Agent frontmatter (name, description, tools, model, permissionMode, color enum)                   |
| Plugin Manifest Agents Section          | `https://code.claude.com/docs/en/plugins-reference#agents`                                                                                                                           | validate-agent                                   | Agents as plugin component                                                                        |
| Hooks (Anthropic)                       | `https://code.claude.com/docs/en/hooks`                                                                                                                                              | validate-hook, validate-plugin                   | ~30-event allowlist, handler types, matcher regex, exit codes                                     |
| Plugin Manifest Hooks Section           | `https://code.claude.com/docs/en/plugins-reference#hooks`                                                                                                                            | validate-hook                                    | Hooks in plugin manifest structure                                                                |
| MCP Integration (Claude Code)           | `https://code.claude.com/docs/en/mcp`                                                                                                                                                | validate-mcp, validate-plugin                    | MCP server discovery, transport types, credential handling                                        |
| Plugin Manifest MCP Servers Section     | `https://code.claude.com/docs/en/plugins-reference#mcp-servers`                                                                                                                      | validate-mcp                                     | MCP servers as plugin component                                                                   |
| MCP Open Specification                  | `https://modelcontextprotocol.io/specification`                                                                                                                                      | validate-mcp, validate-plugin                    | Transport schemas, tool/resource/prompt protocol                                                  |
| Claude Code Changelog                   | `https://code.claude.com/docs/en/changelog`                                                                                                                                          | skill-creator                                    | Extensions and version history                                                                    |
| Anthropic Official Skills Repo          | `https://github.com/anthropics/skills`                                                                                                                                               | skill-creator                                    | Official SKILL.md examples + reference impl                                                       |
| SKILL.md Template (Anthropic)           | `https://github.com/anthropics/skills/blob/main/template/SKILL.md`                                                                                                                   | skill-creator                                    | Skeleton for new skill creation                                                                   |
| Official Skill Examples (10)            | `https://github.com/anthropics/skills/blob/main/skills/{algorithmic-art,canvas-design,claude-api,doc-coauthoring,docx,frontend-design,internal-comms,mcp-builder,pdf,xlsx}/SKILL.md` | skill-creator                                    | 10 canonical examples of published skills                                                         |
| Skills Deep Dive (Technical)            | `https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/`                                                                                                            | skill-creator                                    | Authoritative technical reference on skill philosophy                                             |
| Anthropic Engineering Blog (Skills)     | `https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills`                                                                                        | skill-creator                                    | Agent skills philosophy, outcomes-driven thinking, NOI framing                                    |

**Authoritative local snapshots** (immutable ground truth for Refiner validation runs):

| Path                                                                                        | Purpose                                                                           |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `~/000-projects/claude-code-plugins/000-docs/6767-b-SPEC-DR-STND-claude-skills-standard.md` | IS marketplace rubric (100-point grading) + 8-field enterprise required-field set |
| `~/000-projects/claude-code-plugins/000-docs/anthropic-skills-spec-snapshot.md`             | Anthropic SKILL.md spec snapshot (quarterly refresh)                              |
| `~/000-projects/claude-code-plugins/000-docs/agentskills-spec-snapshot.md`                  | AgentSkills.io spec snapshot                                                      |
| `~/000-projects/claude-code-plugins/scripts/validate-skills-schema.py`                      | IS validator (v7.0, schema 3.3.1) — authoritative grading engine                  |
| `~/000-projects/claude-code-plugins/000-docs/SCHEMA_CHANGELOG.md`                           | Schema version history and breaking changes                                       |

### Refiner spec-binding (NEW AC-11 detail)

- The Refiner's Sinker hook (L1, Phase B) invokes `/validate-skillmd` which already grounds in the URLs above; no re-derivation needed
- The Refiner's Hook-layer hook (L3, Phase B) invokes `/validate-plugin` for cross-harness portability claims (per § 2.5 fold-in #3)
- Spec snapshots in `claude-code-plugins/000-docs/*-snapshot.md` ARE the authoritative ground truth for validator verdicts; live URLs are reference-checked quarterly (snapshot drift triggers a new bead under `TL-EPIC` cluster)
- § 13 Step 0 includes a quarterly-spec-snapshot refresh as part of pre-execution research
- Every SkillVersion record's `skill_md_spec_version` field cites the snapshot path + the live URL of record

### Recursive link-following discipline (NEW per user direction 2026-05-26)

**The 22 URLs above are ENTRY POINTS, not exhaustive coverage.** The first page of the Claude Code docs (e.g., `code.claude.com/docs/en/skills`) is an index; the real spec content lives in linked sub-pages — frontmatter reference, invocation control, tool allowlist semantics, hook event allowlist, MCP transport details, plugin manifest field-by-field, marketplace catalog entries, etc.

**Pre-execution research (§ 13 Step 0) MUST follow links depth-1 at minimum** from each of the 22 entry URLs. For complex spec domains (plugins-reference, skills, hooks), depth-2 is required to capture nested specs (e.g., plugin.json → hooks section → individual handler types → matcher regex semantics).

**Resulting research artifact:** an expanded URL inventory (likely 40-80 URLs after recursive walk) cached at `intent-eval-lab/research/claude-docs-spec-tree-<date>.md` with each URL annotated: (a) what spec section it covers, (b) which Refiner artifact it bears on (SKILL.md / plugin.json / hooks.json / etc.), (c) snapshot timestamp.

**Quarterly refresh discipline:** the recursive walk re-runs every 90 days; diffs against prior snapshot are surfaced as bd memories and CLAUDE.md notes per § 3.5 PR-4 + PR-5.

---

## 3. Architectural commitments (synthesized from thinker-canon panel + ratified by user decisions)

These are non-negotiable design constraints:

1. **Tier-1 IEP integration** (user choice): new `SkillVersion` entity in `intent-eval-core` kernel + new `skill-refiner-pass/v1` predicate URI on `evals.intentsolutions.io`. The 14th canonical entity. Blocks on `iec-E12` v0.2.0 release (gated by P0 beads `uprg` Evidence Bundle compat policy + `9pi3` OTel semconv).
2. **Append-only event log; never in-place SKILL.md mutation** (Hickey-aligned). Each accepted edit produces a content-addressed `SkillVersion` value; "current best" is a separate mutable pointer.
3. **Multi-dimensional score records** (Goodhart-resistant). Score is `(skill_hash, eval_set_hash, behavioral_score, readability_score, adversarial_pass_rate, ...)` — never collapsed to a scalar.
4. **Shadow → canary → promote ladder, human-gated promotion** (Huyen-aligned). The Refiner NEVER auto-writes SKILL.md on main; produces candidate values that humans review + promote.
5. **Default Haiku/Sonnet for scoring + Opus only for final validation** (Huyen economics: $9.30/pass naive, ~$370/epoch/skill — order-of-magnitude reduction by tiered routing).
6. **Eval-set bootstrap is non-optional** (Karpathy-aligned — every new skill needs a held-out set; `bootstrap` is a first-class command). Sources: (a) synthetic from SKILL.md, (b) j-rig rollout harvest, (c) human-nominated golden traces.
7. **The acceptance gate is the durable contribution; the refiner mechanism is swappable** (Karpathy bitter-lesson check). When frontier-native skill refinement arrives, you keep the harness + gate; throw away the propose() internals.
8. **Three-layer hook architecture from security-guidance** (Anthropic-canonical pattern, IS-renamed sinker/line/hook). Per-edit deterministic check (no model call) + end-of-turn background review (with finding-feedback) + commit-time deeper agentic gate.
9. **Single-signer audit trail** (ISEDC pattern). Refiner proposes; human + acting CTO disposes. Read-only roles preserved.
10. **Marketing as "evals-gated skill edits" not "automated skill optimization"** (Karpathy verdict — durable framing when frontier-native lands).
11. **NEW AC-11: agentskills.io + Claude Code spec compliance** (per § 2.5; revised 2026-05-27 post-internal-review). The Refiner's edit grammar respects two layered spec surfaces, each pinned to a locally-forked snapshot (drift is detected by quarterly bd memory, never silently embedded in SkillVersion records). (a) **Open-standard layer (agentskills.io v1)** — `name` + `description` REQUIRED; `license`, `compatibility`, `metadata`, `allowed-tools` (experimental) OPTIONAL. Source-of-truth snapshot at `intent-eval-lab/research/agentskills-spec-v1.0.0.md`. (b) **Claude Code extension layer** — `disallowed-tools` (added v2.1.152, 2026-05-27), `model`, `argument-hint`, `disable-model-invocation`, `context`, `agent`, `effort`, `hooks` OPTIONAL. Source-of-truth snapshot at `intent-eval-lab/research/claude-docs-spec-tree-2026-05-27.md`. The Refiner's L1 Sinker hook invokes `/validate-skillmd` Tier 2 which validates against both layers independently. SkillVersion records pin BOTH spec generations: `skill_md_open_spec: "agentskills.io/v1.0-<snapshot-sha256-prefix>"` and `skill_md_cc_extension_version: "claude-code/2.1.152-<snapshot-sha256-prefix>"`.
12. **AC-12: tri-linkage discipline — REWRITTEN v5 per DR-028 T3 COLLAPSE (20/20 consensus)**: bd is the CANONICAL writer of bead↔doc↔GH-issue cross-refs. GH issue bodies and doc front-matter Beads-rows are GENERATED PROJECTIONS produced by `bd-sync` from the bead's notes. Humans editing GH issues or doc front-matter directly is a CI-detected anomaly that triggers re-projection from bd. The 7 process disciplines in v4.1's § 3.5 (PR-1..5 + validate-trilink + spec-refresh) collapse to ONE rule in v5: "bd is source; everything else is projection." Multiple-writers-of-the-same-fact is replaced by single-writer + verifiable-projection per CSO Session 7 standards-body-realpolitik binding (matches in-toto + SLSA + Sigstore direction).

13. **NEW AC-13: RefinerStrategy interface (v5 per DR-028 P0-RATIFY-5)**. The Refiner mechanism is operationalized as a swappable strategy behind a typed interface in `@j-rig/refiner-core/strategies/`. Phase A ships TWO reference implementations: `NaiveInContextStrategy` (single-pass Opus-in-context — also serves as the Phase A.0 null-hypothesis baseline per DR-028 P0-RATIFY-3) and `SkillOptStyleStrategy` (the original v4.1 propose() mechanism refactored as a strategy impl). `refiner_strategy_id` field added to SkillVersion schema; signed in predicate payload per CISO Session 7 binding (mechanism-swappable must NOT become mechanism-untraceable). AC-7's bitter-lesson swap claim is no longer un-substantiated. Per VP DevRel binding: the interface is documented in `j-rig-binary-eval/000-docs/` with a conformance-test suite for community contributors — the swap from internal API becomes a community extension point.

---

## 3.5. Process Rigor — non-negotiable workflow gates

Per user direction 2026-05-26: "No shortcuts. I want to make sure every repo has its own fine detailed beads … beads represent the internal documentation … create GitHub issues that house the correlating bead ID … validate the consistency among all that."

### PR-1 — Doc ↔ Bead ↔ GH-Issue tri-linkage (AC-12 enforcement)

Every Skill Refiner artifact (doc, bead, GH issue) must cite its peers in the other two layers.

**Doc** — every `000-docs/NNN-*-skill-refiner-*.md` (any IEP repo) carries a front-matter table with mandatory rows:

```markdown
| Beads | bd_000-projects-3zol, bd_000-projects-0r8m.1, RC-IEC |
| GitHub | jeremylongshore/intent-eval-core#42 |
```

**Bead** — every Skill Refiner bead description ends with two lines (regardless of position of body prose):

```text
Doc: intent-eval-core/000-docs/030-AT-SPEC-skill-version-entity.md
GitHub: jeremylongshore/intent-eval-core#42
```

**GH Issue** — every Skill Refiner GH issue body ends with two lines:

```text
Bead: bd_000-projects-0r8m.1
Doc: intent-eval-core/000-docs/030-AT-SPEC-skill-version-entity.md
```

The line-prefix tokens (`Beads:`, `Doc:`, `GitHub:`, `Bead:`) match the regex already used inside `~/bin/bd-sync`. See § 5.5 for the verifier script and CI integration.

### PR-2 — `/validate-consistency` pre-code gate

`/validate-consistency` (skill at `~/.claude/skills/validate-consistency/SKILL.md`) runs before ANY code change in a Skill Refiner phase. Invocation points:

| When                         | What it checks                                                                                                                                                                                  |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Phase kickoff                | Brand canon coherence across plan, companion docs, beads, GH issues, READMEs                                                                                                                    |
| Every PR pre-merge (CI hook) | The 7 drift categories: status drift, API/interface drift, capability/behavior drift, CI/validation drift, planning-vs-implementation confusion, cross-doc contradiction, index/reference drift |
| Doc reorganization           | Cross-doc reference integrity                                                                                                                                                                   |
| Plan revision                | Plan ↔ companion plan ↔ glossary ↔ blueprint alignment                                                                                                                                          |
| Quarterly                    | Full ecosystem sweep across all 5 IEP repos                                                                                                                                                     |

Output: severity-tagged markdown report (`🔴 BLOCKER` / `🟡 WARN` / `🔵 INFO`). BLOCKERS fail the gate; WARNS surface to the next ISEDC review; INFOS accumulate to backlog.

### PR-3 — Sequential execution discipline (per user direction 2026-05-26)

**Mandatory order, no skipping:**

1. **Plan** — this document (and companion plan 025) ratified
2. **Beads** — file all per-repo cluster beads with annotations, notes, dependencies (see § 5.5 + § 13)
3. **GH issues** — create corresponding issues in each IEP repo with bead IDs in the body (see § 13)
4. **Validate** — run `/validate-consistency` + `validate-trilink.sh` to verify coherence
5. **Plan Audit** — convene the 7-seat thinker-canon panel against the plan (see § 12)
6. **Ratify** — ISEDC session if BLOCKERs surface; user approval otherwise
7. **THEN code** — first `bd claim` against a Skill Refiner bead

§ 13 codifies this sequence step-by-step with checkpoints.

### PR-4 — bd memories discipline (per user direction 2026-05-26)

The `bd remember` subsystem stores persistent knowledge in the bd workspace (distinct from Claude's auto-memory and from per-repo CLAUDE.md). It's the right home for _operational findings_ — non-obvious lessons surfaced during Skill Refiner work that future sessions/agents must inherit.

**Mandatory `bd remember` trigger events:**

| Trigger                                                                          | Content captured                                            | Owner      |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------- | ---------- |
| Spec snapshot pinned (§ 13 Step 0)                                               | URL + pinned version + local-snapshot path + date           | Acting CTO |
| ISEDC Session ratifies a binding constraint                                      | DR-NNN reference + verbatim binding rule                    | Acting CTO |
| A risk in § 8 materializes in production                                         | Risk row + what actually happened + remediation taken       | Engineer   |
| A Phase exit-criterion misses by > 2 weeks                                       | Phase + criterion + cause + corrective action               | Acting CTO |
| Plan Audit (§ 12) surfaces a P0 finding                                          | Finding-ID + remediation-bead-ID + plan-section-amended     | Acting CTO |
| Frontier model release shifts the bitter-lesson surface (Karpathy concern)       | Model + release date + observed effect on Refiner mechanism | Acting CTO |
| `validate-trilink.sh` exception is granted (legacy bead exempt from tri-linkage) | Bead-ID + reason + sunset date                              | Engineer   |
| A SkillVersion record cites a deprecated agentskills.io spec version             | SkillVersion-ID + deprecated-version + migration-path       | Acting CTO |
| Tri-linkage drift detected by nightly verifier                                   | Detected drift pattern + resolution                         | Acting CTO |

**Memory naming convention:** `bd remember --key skill-refiner-<topic>-<date> "<content>"`. Example:

```bash
bd remember --key skill-refiner-agentskills-spec-pin-2026-05-26 \
  "Pinned agentskills.io spec to v1.0.0 (snapshot at claude-code-plugins/000-docs/agentskills-spec-snapshot.md). Next refresh due 2026-08-26. SkillVersion records emitted before next refresh carry skill_md_spec_version='agentskills.io/v1.0.0'."
```

**Search discipline:** before opening a new bead on a topic, run `bd memories <topic-keyword>` first. If a memory exists, the new bead should cite it in the description.

### PR-5 — Per-repo CLAUDE.md update discipline (per user direction 2026-05-26)

Every IEP repo has a CLAUDE.md that future sessions read first. When Skill Refiner work touches a repo, that repo's CLAUDE.md MUST be updated in the same PR so the next session inherits the context. Repo-level CLAUDE.md is the local-context source-of-truth; the plan + glossary are the global-context source-of-truth.

**Mandatory CLAUDE.md update events:**

| Trigger                                                          | Content added to repo CLAUDE.md                                    | Section    |
| ---------------------------------------------------------------- | ------------------------------------------------------------------ | ---------- |
| First Skill Refiner bead opens against a repo                    | "## Skill Refiner work in flight" section with bead IDs + doc refs | New §      |
| New doc added to repo's `000-docs/` for Skill Refiner            | Cross-link in CLAUDE.md's doc index                                | Existing § |
| Skill Refiner CLI command added (e.g., `j-rig refine bootstrap`) | Command documented under "## Commands" or equivalent               | Existing § |
| Skill Refiner Phase ships in this repo                           | "### Phase X status: SHIPPED" line with date + AAR reference       | New §      |
| repo:<short> labels added/changed                                | Note in bd-workflow section                                        | Existing § |
| Plan Audit ratifies remediations affecting this repo             | Brief note + DR reference                                          | New §      |

**Touch points (one per IEP repo):**

| Repo                 | CLAUDE.md path                                              | Likely updates                                                                                                                                       |
| -------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| intent-eval-lab      | `intent-eval-platform/intent-eval-lab/CLAUDE.md`            | New `## Skill Refiner` section pointing at plan 025 + plan 026 + doc 028/029/030; bead refs RC-IEL + leaf IEL-N1/N2/N3; ISEDC Session 7 DR reference |
| intent-eval-core     | `intent-eval-platform/intent-eval-core/CLAUDE.md`           | New `## Skill Refiner kernel integration` section; SkillVersion entity addition; v0.3.0 release notes; bead refs RC-IEC + IEC-N1/N2                  |
| intent-audit-harness | `intent-eval-platform/audit-harness/CLAUDE.md` (or renamed) | New `## Skill Refiner evidence` section; refiner-pass row schema; bead refs RC-IAH + IAH-N1/N2                                                       |
| j-rig-binary-eval    | `intent-eval-platform/j-rig-binary-eval/CLAUDE.md`          | New `## Skill Refiner package` section; @j-rig/refiner-core + @j-rig/refiner; CLI subcommands; bead refs RC-IAJ + IAJ-N1..N5                         |
| intent-rollout-gate  | `intent-eval-platform/intent-rollout-gate/CLAUDE.md`        | New `## Skill Refiner consumer` section; skill-refiner-pass/v1 consumption in M5; bead refs RC-IAR + IAR-N1                                          |

**Umbrella CLAUDE.md** (`intent-eval-platform/CLAUDE.md`) also updates — extends the existing "Active plans" section to point at the ratified plan + per-repo CLAUDE.md pointers.

**Verification:** `/validate-consistency` (§ 3.5 PR-2) checks CLAUDE.md ↔ repo state alignment as part of its 9-check suite. Drift triggers a BLOCKER.

---

## 4. Phased roadmap — MVP through full-scale

Five phases (A-F, with D deferred). Each phase ships independently. Each later phase consumes earlier-phase value artifacts. See § 4.5 Ecosystem Fold matrix for how each phase binds to in-flight P0/P1 chains in the existing IEP evolution.

### Phase A — Skill Refiner discipline library (Foundation) — ~1 week budget; see § 4.5 for bandwidth model

**Goal**: Ship the value-oriented core that everything else builds on. NO hooks. NO new entity. NO plugin shape. Pure library + thin CLI. Two-package split per CTO recommendation (refiner-core pure + refiner with I/O).

**Deliverables**:

- New packages: `@j-rig/refiner-core` (pure value-oriented; zero adapters) + `@j-rig/refiner` (orchestrator + adapters + CLI) — both inside `j-rig-binary-eval` monorepo at `packages/refiner-core/` and `packages/refiner/`
- API surface (illustrative — final shape lands in the package):

```typescript
// Value types (refiner-core)
type SkillDocHash = Sha256;
type EvalSetHash = Sha256;
type ScoreRecord = {
  skill: SkillDocHash;
  evalSet: EvalSetHash;
  behavioral: number;
  readability: number;
  [dimension: string]: unknown;
};
type EditProposal = {
  parent: SkillDocHash;
  ops: Array<AddOp | DeleteOp | ReplaceOp>;
  refiner_model: string;
  rationale: string;
};

// Pure operations (refiner-core; declare-only interfaces for I/O ops)
declare function bootstrap(skillDoc: SkillDoc): EvalSet;
// modelTier intentionally excludes 'opus' — AC-5 binds Opus to final-validation only,
// never to per-pass scoring. Final validation runs through a separate `validate()` entry point.
declare function score(
  skillDoc: SkillDoc,
  evalSet: EvalSet,
  modelTier?: "haiku" | "sonnet",
): ScoreRecord;
declare function propose(
  skillDoc: SkillDoc,
  scoredRollouts: ScoredRollout[],
  refinerModel?: string,
): EditProposal;
declare function apply(skillDoc: SkillDoc, edit: EditProposal): SkillDocV2;
declare function accept(scoreV1: ScoreRecord, scoreV2: ScoreRecord): boolean;
```

- Append-only event log at `.j-rig/refiner/log.jsonl` (each line is a value-record)
- Content-addressed store at `.j-rig/refiner/store/<hash>` (each SkillVersion + EditProposal + ScoreRecord persists as immutable value)
- Single mutable pointer file: `.j-rig/refiner/pointers/<skill>/best` (just a hash)
- CLI: `j-rig refine bootstrap <skill>`, `j-rig refine score <skill> --eval-set <path>`, `j-rig refine propose <skill>`, `j-rig refine apply <proposal>`, `j-rig refine status <skill>`
- **Phase A pre-flight: complete deferred old-plan items** — run `/gist-auditor --repo j-rig-binary-eval` and update existing j-rig gist `d1c4570a8...` to v1.1.0 content. Ships as standalone PR before Phase A library work to clear the in-flight queue.

**Build order (within Epic 1)** — adjusted from filed-bead-order per CTO recommendation:

| Order | Task                                                                                                               | Why this order                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| 1     | Scaffold `@j-rig/refiner-core` package + value types                                                               | Foundation; everything else depends on types                |
| 2     | Implement `apply()` + `accept()` — pure transformation + strict-improvement gate                                   | The durable contribution per AC-7; get the gate right first |
| 3     | Implement `bootstrap()` — eval-set synthesis from SKILL.md + harvest + golden                                      | Unsexy 80%; non-optional per AC-6                           |
| 4     | Implement event log + content-addressed store + best-pointer                                                       | Persistence layer; depends on types                         |
| 5     | Implement `score()` — delegate to j-rig Binary Eval via shell-out                                                  | Adapter layer (lives in refiner, not refiner-core)          |
| 6     | Implement `propose()` — Anthropic SDK adapter + tiered routing                                                     | Most complex; comes last because everything feeds it        |
| 7     | Build CLI (5 commands)                                                                                             | Thin shim over orchestrator                                 |
| 8     | Release ceremony — `@j-rig/refiner-core@0.1.0` + `@j-rig/refiner@0.1.0` synchronized tag, sigstore provenance, AAR | Synchronized release on both packages                       |

**Reuses existing infrastructure**:

- `j-rig score` and `j-rig optimize` already exist (`packages/cli/src/commands/{eval,optimize}.ts`); Phase A library DELEGATES scoring to j-rig (no new evaluator)
- `j-rig` `ChangeProposal` and `Experiment` types already exist in `packages/core/src/optimizer/types.ts`; Phase A library wraps them with the value-oriented hash-chaining discipline
- `validate-skillmd` Tier 2 deterministic checks are reusable as a pre-acceptance gate (no Goodhart in frontmatter)
- `audit-harness emit-evidence` is the existing wrapper for in-toto Statement v1 emission; Phase A library uses it via shell-out (no re-implementation)
- The two-package split (refiner-core + refiner) mirrors the existing IS kernel pattern (intent-eval-core types + downstream runtime adapters)

**Exit criteria**: ship `@j-rig/refiner-core@0.1.0` + `@j-rig/refiner@0.1.0` to npm with sigstore provenance. Demo: `j-rig refine bootstrap /release` produces a valid eval set; `j-rig refine score /release` returns a ScoreRecord; `j-rig refine propose /release` returns an EditProposal; `j-rig refine apply` produces a SkillDocV2 value.

### Phase B — `/j-rig` plugin v0.1.0 (Refiner + 3-layer hooks, hook-shaped) — ~2 weeks budget

**Goal**: Wrap Phase A library in a Claude Code plugin with 3-layer hooks. This is the user-visible product that lives in `claude-code-plugins`. Single plugin path `/j-rig` (the Refiner is delivered through j-rig's existing engineering home; user-facing brand is "Skill Refiner" even though plugin command lives under `/j-rig`).

**Architecture (3 layers, hook-line-sinker)**:

```text
plugins/productivity/j-rig/
├── .claude-plugin/
│   ├── plugin.json
│   └── hooks/hooks.json
├── hooks/
│   ├── sinker.sh           # L1 — PostToolUse:Edit/Write on SKILL.md
│   ├── line.sh             # L2 — Stop hook — end-of-turn rollout capture
│   └── hook.sh             # L3 — PreToolUse:Bash on git commit/push (CAN block via exit-2)
├── skills/
│   └── j-rig/SKILL.md
└── scripts/
    └── refiner-loop.ts
```

| Layer           | Hook event                                       | Mechanism                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Cost                                                                   |
| --------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Sinker (L1)** | `PostToolUse:Edit/Write` on `SKILL.md` files     | Run `validate-skillmd` Tier 2 (deterministic frontmatter checks per AC-11 agentskills.io compliance); append warning to context if fails                                                                                                                                                                                                                                                                                                                                | $0 (no model call)                                                     |
| **Line (L2)**   | `Stop` hook                                      | If a skill was invoked during the turn AND j-rig has scored its rollouts: append to `.j-rig/refiner/log.jsonl`. After N rollouts on a skill: fire refiner in background, surface candidate in next-turn context                                                                                                                                                                                                                                                         | $ (Sonnet refiner model; Haiku rollout scoring)                        |
| **Hook (L3)**   | `PreToolUse:Bash` matcher `git commit\|git push` | If staged diff modifies a SKILL.md: run agentic gate that reads the surrounding skills directory + checks for regression-against-rejected-buffer + (optional) shadow-validation against held-out set. `PreToolUse` is in the Anthropic hooks "Can block" allowlist (exit-2 or `permissionDecision: deny`) — chosen over `PostToolUse:Bash` because the latter fires AFTER the bash has already executed and therefore cannot prevent the commit/push that triggered it. | $$ (Opus for agentic gate; rate-limited per security-guidance pattern) |

**Plugin CLI surface (commands users invoke explicitly)**:

- `/j-rig refine bootstrap <skill>` — create initial eval set
- `/j-rig refine propose <skill>` — manual refiner pass
- `/j-rig refine shadow <skill>` — run candidate in shadow mode
- `/j-rig refine promote <skill>` — promote candidate → main (human-gated, AC-4)
- `/j-rig refine status <skill>` — show trajectory + budget + rejected log

**MVP demo**: pick ONE existing skill in `claude-code-plugins` (open question § 7: `/audit-tests` for cleaner blog post OR `/validate-skillmd` for sharper IP-defense story); run full bootstrap → score → propose → shadow → promote cycle; produce the Phase E Evidence report (markdown + HTML); publish as case-study blog post.

**Exit criteria**:

- Plugin published to `claude-code-plugins` marketplace at `plugins/productivity/j-rig/`
- One real skill refined end-to-end with shipped score-delta evidence
- Phase E Evidence report (markdown form, generated locally) attached to the demo; **public HTML hosting + blog post publication is Phase E's exit criterion, NOT Phase B's** (resolves prior circular Phase B↔E dependency)

### Phase C — Tier-1 IEP integration (kernel) — ~3-4 weeks budget; gated on uprg + 9pi3

**Goal**: Promote `SkillVersion` to the 14th canonical entity in `intent-eval-core`. Mint `skill-refiner-pass/v1` predicate URI. j-rig becomes an emitter of skill-refiner-pass rows; intent-rollout-gate becomes a consumer.

**Architectural commits**:

- New entity `SkillVersion` in `intent-eval-core/schemas/v1/skill-version.schema.json`:

```jsonc
{
  "id": "uuidv7",
  "skill_id": "kebab-slug",
  "skill_doc_hash": "sha256",
  "parent_version_id": "uuidv7 | null",
  "edit_proposal_hash": "sha256 | null",
  "eval_set_hash": "sha256",
  "score_record": {},
  "accepted_by": "actor-identity",
  "accepted_at": "rfc3339",
  "signing_mode": "staging | production",
  "rekor_log_index": "int64 | null",
  "skill_md_spec_version": "agentskills.io/v1.0.0",
}
```

- New predicate URI `https://evals.intentsolutions.io/skill-refiner-pass/v1`
- Blueprint B § 7 extension documenting the new predicate body
- Cross-field invariants per CISO binding (filed as `bd_000-projects-1is2`): `rekor_log_index` non-null iff `signing_mode='production'`
- Companion governance: P0 bead `uprg` (Evidence Bundle compat policy) MUST land before this predicate URI is signed into production Rekor. **Phase C cannot complete until `uprg` is closed.**

**j-rig changes**:

- New CLI command `j-rig emit-refiner-pass` parallel to existing `j-rig emit-evidence` — emits `skill-refiner-pass/v1` rows
- Existing `optimizer/` module extended to use `@j-rig/refiner-core` value types (Phase A becomes a transitive dep within the monorepo)

**intent-rollout-gate changes**:

- M5 substantive runtime (still in flight per repo status) consumes `skill-refiner-pass/v1` rows as enrichment (not blocking advisory by default)

**Companion P0 bead dependencies (already filed)**:

- `bd_000-projects-uprg` — Evidence Bundle predicate compatibility policy (BLOCKS this phase)
- `bd_000-projects-9pi3` — OTel semconv pin (BLOCKS kernel v0.3.0 ship)
- `bd_000-projects-59tx` — Release workflow failure alerting (CROSS-CUTTING — should land alongside)

**Exit criteria**:

- `@intentsolutions/core@0.3.0` published with `SkillVersion` entity + spec-version pinning
- `j-rig-binary-eval` ships `j-rig emit-refiner-pass` command
- intent-eval-lab Blueprint B § 7 extended with new predicate spec
- ISEDC Session 7 ratifies the URI namespace addition (CISO binding: must be on `evals.intentsolutions.io` not `labs.`)

### Phase D — REMOVED v5 per DR-028 T2 (ANTI-GOAL — 12 of 14 voices)

**v5 status: This phase is REMOVED from the plan.** Per DR-028 T2 majority (Cunningham + Fowler + Torvalds + Pike + Thompson + Armstrong + 6 ISEDC seats = 12 of 14 voices), Phase D is replaced by an explicit anti-goal in Blueprint A § 3.X:

> **Blueprint A § 3.X Anti-goal:** Intent Solutions does not build a creator product for SKILL.md generation. SkillsBench (arXiv 2602.12670) demonstrates that self-generated skills underperform the no-skill baseline ("no benefit on average") while human-curated skills deliver +16.2pp. IS's role is to refine human-curated skills via evals-gated edits, not to displace human curation.

**Re-opening trigger** (per Karpathy + Gregg minority binding from DR-028): `self-gen lift > +8pp on kernel-pinned eval set on any frontier model release, OR internal acceptance rate parity`. ISEDC reconvenes if this metric is observed externally OR internally.

The standalone deferred bead `bd_000-projects-vbqp` is updated to status `closed: superseded-by-DR-028-T2-anti-goal` in Step 5 remediation.

### Phase E — Evidence report production / proof-of-work deliverable spec — ongoing

**Goal**: Define the per-Refiner-pass deliverable shape so consumers SEE the eval ran and produced something defensible. User direction: "we need well-defined template and I believe we have eval.intentsolutions.io [namespace] — we need to figure this out."

**Dual-format spec**:

#### E.1 — Markdown AAR (canonical, git-versioned, machine-parseable)

Filename convention per Doc Filing Standard v4.x:
`<repo>/000-docs/NNN-RL-REPT-skill-refiner-<skill>-<date>.md`

Template structure (each section is REQUIRED for the report to be considered complete; missing sections fail the BLOCKING gate):

```markdown
# Skill Refiner Evidence Report — pass on `<skill-id>`

| Field                       | Value                                                        |
| --------------------------- | ------------------------------------------------------------ | ------ | -------- |
| Date                        | YYYY-MM-DD                                                   |
| Skill                       | <skill-id>                                                   |
| Skill version (input)       | sha256(...) (8-char prefix)                                  |
| Skill version (output)      | sha256(...) (8-char prefix)                                  |
| Eval set                    | sha256(...) (8-char prefix)                                  |
| Score delta                 | behavioral +N.Mpp; readability +N.Mpp                        |
| Refinement passes           | N (M accepted, K rejected)                                   |
| Compute cost                | $X.XX (Haiku tier $X.XX; Sonnet tier $X.XX; Opus tier $X.XX) |
| Wall-clock                  | HH:MM:SS                                                     |
| Confidence tier             | `alpha`                                                      | `beta` | `stable` |
| agentskills.io spec version | v1.0.0                                                       |
| Portability claim           | Validated against: Claude Code, Codex CLI, Gemini CLI        |

## 1. Context

<why this skill was refined; trigger (manual / drift / scheduled)>

## 2. Eval set composition

<source: synthetic / harvested / golden / hybrid>
<size: N items>
<diversity: stratified by ...>
<eval_set_hash + storage location>

## 3. Score trajectory

<table or sparkline of behavioral + readability scores across passes>
<final delta vs baseline>

## 4. Accepted edits (replayable)

<for each accepted edit:>
- Pass N
- Refiner model + rationale (verbatim from LLM output)
- Op type (add/delete/replace)
- Diff (unified, syntax-highlighted)
- Pre-score → post-score
- Acceptance gate evidence

## 5. Rejected edits (audit trail)

<for each rejected edit:>
- Pass N
- Op type
- Refiner model
- Pre-score → post-score (delta showed no improvement)
- Reason for rejection (gate-output)

## 6. Hook-layer gate evidence (per pass)

<table mapping pass-number → SkillVersion ID → ScoreRecord hash → signed Evidence Bundle row>
<Rekor log index per signed row>
<which hook fired: sinker (L1) / line (L2) / hook (L3)>

## 7. Signed Evidence Bundle (in-toto Statement v1)

<inline JSON OR link to bundle file>
<predicateType: skill-refiner-pass/v1>
<verification command: cosign verify-blob ... | jq ...>

## 8. Architectural bindings

<DR-010 + Blueprint B § 7 + Canonical Glossary citations>
<which P0 beads are honored: uprg, 9pi3, 59tx>

## 9. Limitations + risks

<failure modes that didn't trigger but should be watched>
<Goodhart-corner cases the eval set may miss>
<recommended re-validation cadence>

## 10. Status banding

ACTIVE | SUPERSEDED-BY-NNN | INVERTED-BY-EMPIRICAL-FINDING | RATIFIED-AND-STABLE

— Jeremy Longshore
intentsolutions.io
```

#### E.2 — HTML projection (derived from markdown AAR)

Generated from the markdown source via a deterministic renderer (NOT a separate authoring path). Single source of truth (markdown); HTML is a view.

Sections rendered:

- Hero: skill name + score delta + cost + wall-clock (callout box)
- Score-trajectory chart (recharts or similar; data sourced from § 3 of markdown)
- Side-by-side diff browser for accepted edits (rendered from § 4)
- Rejected edits table (collapsible, source § 5)
- Verification panel: clickable Rekor log indices + cosign-verify command (copy-pasteable)
- Portability badges row: which parsers validated (Claude Code / Codex CLI / Gemini CLI / etc.)
- Footer with architectural-bindings links

Hosted at `evals.intentsolutions.io/reports/<skill-id>/<sha-prefix>/`. Static HTML from a Hugo template (mirrors the partner-portal pattern already in use). DNSSEC + CAA record pinning required before first signed-prod attestation (CISO binding from earlier DRs).

#### E.3 — Where reports live (storage spec)

| Artifact               | Storage                                                                                              | Retention                                           |
| ---------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Markdown AAR           | `<repo>/000-docs/NNN-RL-REPT-skill-refiner-*.md` (committed to git)                                  | Forever                                             |
| Signed Evidence Bundle | `<repo>/.j-rig/refiner/evidence/<sha>.json` (gitignored if signed-prod, committed if signed-staging) | Indexed by sha; orphaned bundles GC'd after 90 days |
| HTML render            | `evals.intentsolutions.io/reports/<skill-id>/<sha-prefix>/` (Hugo build artifact)                    | Pinned per version; never overwritten               |
| Rekor log entry        | Public sigstore Rekor                                                                                | Permanent (by design — one-way door)                |

**Phase E exit criteria**:

- Markdown template committed to `intent-eval-lab/specs/skill-refiner-evidence-report/v1.0.0-draft/SPEC.md`
- HTML renderer (~200 LOC of Hugo template + recharts JS) shipped as part of partner-portal infrastructure
- ISEDC Session 7 ratifies the predicate URI carrying the report's canonical sha
- One real report generated end-to-end (Phase B exit-criteria demo skill)

### Phase F — MLOps scale-up (long-term, ~Q3 2026) — beyond MVP

Per Huyen — when this works for 30 skills it becomes MLOps for prompts. Long-term scale needs:

| Layer                                     | Mechanism                                                                                            | Filed bead                                                   |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Skill registry**                        | SkillVersion entity + lineage graph in `intent-eval-core`                                            | Phase C extends to this                                      |
| **Eval-set governance**                   | Versioned + reviewed quarterly + rolling-production + adversarial-append                             | `bd_000-projects-l44w`                                       |
| **Canary rollouts**                       | Per-partner traffic routing of skill versions                                                        | `bd_000-projects-l5ut`                                       |
| **A/B at partner layer**                  | Partner pins skill version; promotion is per-partner                                                 | `bd_000-projects-n6oj`                                       |
| **Promotion graph**                       | Shadow → canary-10% → canary-50% → 100% → archived                                                   | Phase C SkillVersion entity + Decision Record per transition |
| **Drift policy**                          | Weekly re-validation; event-triggered on upstream model bump; auto re-refinement on persistent drift | `bd_000-projects-b5o6`                                       |
| **Cost dashboard**                        | OTel-spans + per-skill cost trajectory + hard alerts at 80% budget                                   | Subsumes `iel-E12-attributes-pinned` (already P0 in `9pi3`)  |
| **Cross-vendor distribution** (per § 2.5) | Refined skills distributable across Vercel skills.sh, Anthropic skills marketplace, etc.             | TBD ISEDC decision                                           |

Phase F is NOT in scope for this plan. **Phase F triggers**: when (a) > 5 partners actively consume refined skills OR (b) > 100 active SkillVersion records OR (c) drift incident in production causes the first rollback.

---

## 4.5. Ecosystem Fold integration matrix

Per user direction 2026-05-26: "This part of the plan has to incorporate with the fleshed out evolution of the entire ecosystem. So we can't give up on the entire ecosystem. We have to work this into the ecosystems fold."

Binds Skill Refiner phases to in-flight P0/P1 chains so the Refiner work is additive rather than parallel-universe.

| In-flight chain                                      | Repo(s)                           | Skill Refiner phase affected                               | Dependency direction                                               | Risk if ignored                                                                                        | Mitigation                                                                                        |
| ---------------------------------------------------- | --------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| **`uprg` — Evidence Bundle compat policy (P0)**      | intent-eval-core, intent-eval-lab | Phase C (Tier-1 kernel)                                    | `uprg` → blocks Phase C                                            | Phase C ships predicate URI that violates whatever policy `uprg` lands → must re-key, breaks consumers | Phase C explicitly waits on `uprg` closure; Phases A+B unblocked                                  |
| **`9pi3` — OTel semconv pin (P0)**                   | intent-eval-core, intent-eval-lab | Phase C kernel ship, Phase F cost dashboard                | `9pi3` → blocks kernel v0.3.0; Phase F subsumes its delivery       | Refiner emits OTel spans that don't match consumer expectations                                        | Phase A `j-rig refine score` instrumentation pinned to whatever `9pi3` settles                    |
| **`59tx` — Release workflow failure alerting (P0)**  | all 5 repos                       | Phase A, B, C release ceremonies                           | `59tx` ⊢ companion (not blocker)                                   | Refiner release fails silently → no rollback signal                                                    | Phase A/B/C release scripts adopt `59tx` pattern when it lands; pre-`59tx`, manual checklist      |
| **`iec-E12` v0.2.0 kernel work**                     | intent-eval-core                  | Phase C SkillVersion ships in v0.3.0                       | `E12` → must land before SkillVersion (expand-contract per `xcs4`) | Adding 14th entity simultaneously with EvidenceBundlePayload work creates merge hazard                 | Honor Parallel Change discipline; SkillVersion lands in v0.3.0 only after v0.2.0 ships            |
| **`iep-P2` j-rig hardening**                         | j-rig-binary-eval                 | Phase A package lives in j-rig monorepo                    | `iep-P2` ⊢ companion (releases ride together)                      | Refiner v0.1.0 ships into a monorepo that's mid-hardening                                              | Coordinate Refiner v0.1.0 + j-rig hardening release into one tagged event                         |
| **`iep-P3` audit-harness supply-chain**              | intent-audit-harness              | Phase A `emit-evidence` shell-out, Phase C signed Evidence | `iep-P3` → strengthens Refiner attestation                         | If supply-chain work lands after Refiner ships, Refiner evidence chain is weaker than it could be      | Phase A uses current `emit-evidence` as-is; Phase C upgrades when `iep-P3` lands                  |
| **`intent-rollout-gate M5` substantive runtime**     | intent-rollout-gate               | Phase C consumer extension                                 | `M5` → must land for `RC-IAR` work                                 | If Refiner ships skill-refiner-pass rows that rollout-gate can't consume, ecosystem fold is broken     | Defer `RC-IAR` task-level work until `M5` runtime exists; Phase C exit criterion explicitly notes |
| **`iah-npm-publish-gap`**                            | intent-audit-harness              | Phase C consumer reach                                     | gap → blocks programmatic consumption of audit-harness from npm    | Refiner consumers can't `npm install @intentsolutions/audit-harness` until closed                      | Phase C either closes the gap OR explicitly documents the shell-out fallback                      |
| **`tyck` bd memories backfill (P1)**                 | umbrella                          | tri-linkage discipline                                     | `tyck` ⊢ companion                                                 | Bead descriptions lack the cross-refs the verifier expects                                             | Tri-linkage verifier tolerates pre-`tyck` beads with grandfathering note; new beads must comply   |
| **`q9vn` bd ↔ GH ↔ Plane projection inversion (P2)** | umbrella                          | Per-repo cluster filing                                    | `q9vn` ⊢ orthogonal                                                | Per-repo clusters filed today might need re-projection later                                           | File per-repo clusters under current bd model; accept rework if `q9vn` redesign lands             |
| **`bj5m` branch-protection tag-trigger pattern**     | all 5 repos                       | Phase C kernel release                                     | `bj5m` ⊢ already-canonical                                         | Pre-`bj5m`, Phase C kernel release would have hit the same failure that triggered `bj5m`               | Phase C uses tag-trigger pattern (already adopted) — no action needed                             |

**Reading guide:** "→ blocks" = hard dependency; "⊢ companion" = soft dependency, can ship in parallel but coordinate; "⊢ orthogonal" = independent but worth noting. Every Phase exit criterion in § 9 must be readable against this matrix — if a Phase exit-claims to ship but a "→ blocks" row is unresolved, the Phase did not ship.

---

## 5. Critical files to be modified / created

### NEW packages (Phase A)

- `@j-rig/refiner-core` — new package inside j-rig monorepo at `j-rig-binary-eval/packages/refiner-core/`
- `@j-rig/refiner` — new package inside j-rig monorepo at `j-rig-binary-eval/packages/refiner/`

### `intent-eval-platform/intent-eval-core/` (Phase C)

- `schemas/v1/skill-version.schema.json` — NEW entity schema (14th canonical)
- `src/validators/v1/skill-version.ts` — NEW Zod validator (regenerated via `pnpm run codegen:validators`)
- `src/validators/v1/index.ts` — export new validator
- `schemas/v1/skill-refiner-pass.schema.json` — NEW predicate schema
- `schemas/v1/index.json` — register new entity + predicate
- `CHANGELOG.md` — `[0.3.0]` entry per Keep-a-Changelog 1.1.0 (hyphen, not em-dash, per bd memory)
- `package.json` — version 0.2.x → 0.3.0 (MINOR bump because new entity is additive; following Parallel Change discipline per `bd_000-projects-xcs4`)
- `000-docs/NNN-AA-AACR-release-v0.3.0-<date>.md`

### `intent-eval-platform/intent-eval-lab/` (Phase C + E)

- `000-docs/012-AT-ARCH-platform-runtime-blueprint.md` — extend § 7 with `skill-refiner-pass/v1` normative spec
- `000-docs/014-DR-GLOS-canonical-glossary.md` — add SkillVersion + Skill Refiner + 3-layer hooks (sinker/line/hook) + ScoreRecord + EditProposal + agentskills.io spec-pin entries
- `specs/skill-refiner-evidence-report/v1.0.0-draft/SPEC.md` — NEW report template spec (Phase E.1)
- `000-docs/NNN-AT-DECR-isedc-session-7-skill-refiner-tier1.md` — DR ratifying the predicate URI + entity addition
- NEW docs to create (driven by leaf-task beads in § 5.5):
  - `000-docs/028-AT-SPEC-skill-refiner-pass-v1-predicate.md` (normative predicate spec)
  - `000-docs/029-AT-ARCH-skill-refiner-3-layer-hooks.md` (architecture ref + D1/D3/D6 ASCII diagrams)
  - `000-docs/030-AT-STND-tri-linkage-discipline.md` (D7 tri-link standard)

### `intent-eval-platform/j-rig-binary-eval/` (Phase A + Phase C)

- `packages/refiner-core/` — new package directory (Phase A)
- `packages/refiner/` — new package directory (Phase A)
- `packages/cli/src/commands/emit-refiner-pass.ts` — NEW command parallel to `emit-evidence.ts` (Phase C)
- `packages/core/src/optimizer/index.ts` — extend to use `@j-rig/refiner-core` types (Phase C)
- `000-docs/021-AT-SPEC-refiner-core-api.md` — NEW API spec doc with D4 + D8 ASCII diagrams
- `CHANGELOG.md` — `[v1.2.0]` MINOR entry

### `intent-eval-platform/intent-audit-harness/` (Phase C)

- `000-docs/001-DR-DESIGN-evidence-bundle-envelope-design-notes.md` — extend with skill-refiner-pass/v1 gate-result row schema + D9 ASCII diagram
- `000-docs/010-TQ-SOPS-audit-harness-baseline-2026-05-01.md` — update baseline to include refiner-pass

### `~/000-projects/claude-code-plugins/` (Phase B)

- `plugins/productivity/j-rig/.claude-plugin/plugin.json`
- `plugins/productivity/j-rig/.claude-plugin/hooks/hooks.json`
- `plugins/productivity/j-rig/hooks/{sinker.sh,line.sh,hook.sh}`
- `plugins/productivity/j-rig/skills/j-rig/SKILL.md`
- `plugins/productivity/j-rig/scripts/refiner-loop.ts`

### `intent-eval-platform/scripts/` (Process Rigor)

- `scripts/validate-trilink.sh` — tri-linkage verifier (see § 5.5)

### bd workspace (`~/000-projects/.beads/`)

See § 5.5 for the full per-repo bead structure. Highlights:

- 3 existing product epics (3zol Refiner library, jsy3 plugin+hooks, 0r8m evidence+kernel) — keep as roll-up umbrellas
- 5 NEW per-repo coordination epics (RC-IEL, RC-IEC, RC-IAJ, RC-IAH, RC-IAR) labeled `repo:<short>`
- ~13 NEW leaf tasks filling per-repo gaps the product epics don't cover
- 5 NEW tri-linkage backfill beads (one per repo) under a new umbrella TL-EPIC
- 9 NEW ASCII diagram beads (one per canonical diagram in § 6.5)
- 5 standalone deferred beads (vbqp creator, l44w/l5ut/n6oj/b5o6 Phase F) — already filed; no changes

---

## 5.5. Per-Repo Skill Refiner Bead Structure

Per user direction 2026-05-26: "I want to make sure every repo has its own fine detailed beads that are housed in the intent eval platform."

Per user clarification 2026-05-26 (reinforced 3x): "the per repo beads though i want housed here … it should be easy to distinguish which directory repo that the Epic can be correlates to so there's no confusion … I don't want a shit ton of bead files and all the fucking repos. The beads live here. The epics and beads live here, but it should be easy to distinguish what repo they're for."

### ★ CANONICAL RULE (load-bearing, cannot be misread) ★

**ALL Skill Refiner beads — every epic, every leaf task, every diagram bead, every tri-link bead — live in the ONE umbrella workspace at `~/000-projects/.beads/`.** NO per-repo `.beads/` workspaces will be created. NO bead files will be scattered across the 5 IEP repos. There is ONE bd workspace, ONE `bd_000-projects-*` prefix, ONE pane of glass.

**Per-repo distinguishability** is achieved without per-repo workspaces, via four overlapping mechanisms:

1. **Plain-English titles** that explicitly name the repo (e.g., "Skill Refiner — intent-eval-lab coordination", "Backfill Beads: header in intent-eval-core docs touched by Skill Refiner work")
2. **Mandatory `repo:<short>` labels** on every Refiner bead — `short ∈ {iel, iec, iah, iaj, iar, iep}`. Queryable via `bd list --label repo:iec --label refiner --status open`
3. **`Doc:` field in bead description** points to a file in the relevant repo, anchoring the repo by filesystem path
4. **`GitHub:` field in bead description** points to an issue in the relevant repo, anchoring the repo by GH org/repo

When a future reader asks "what Skill Refiner work is in flight for intent-eval-core?", they run `bd list --label repo:iec --label refiner --status open` and get an answer in one command, with zero workspace-switching. That's the entire goal of this structure.

The "RC-IEL", "RC-IEC", "IAJ-N1", "DIAG-D1", "TL-IAH" identifiers used throughout this plan are **plan-document shorthand only** — when filed via `bd create`, each will receive an auto-generated `bd_000-projects-<3char>` ID like every other bead. The shorthand exists so the plan can refer to specific beads-to-be-created without depending on IDs that don't yet exist. After filing, the shorthand maps to actual bd IDs in the audit deliverable cluster.

### Reality check on prefixes (constraint that shaped the design)

The bd tool supports ONE `issue-prefix` per workspace. The umbrella `~/000-projects/.beads/` uses `bd_000-projects-*` (auto-derived from directory name). Per-repo prefixes like `iec-skill-refiner-*` would require one workspace per repo, which breaks the single-pane-of-glass + cross-repo dependency edges the user already depends on.

**Decision: per-repo locality via mandatory LABELS in the umbrella workspace.** Label namespace: `repo:<short>` where `short ∈ {iel, iec, iah, iaj, iar, iep}`. `iep` is the cross-cutting bucket for beads touching ≥ 2 repos.

The user's literal ask ("iec-skill-refiner-1") is not achievable in a single workspace; the _intent_ ("I can find every iec Skill Refiner bead trivially") is satisfied by `bd list --label repo:iec --label refiner --status open`.

### Bead architecture: Hybrid (Option C — chosen)

Keep the 3 product-epics as **umbrella beads**; add **per-repo Skill Refiner coordination epics** as siblings; cross-link bidirectionally via bd dependency edges. Each task-level bead lives in **exactly one** per-repo cluster (single owner) and is **referenced from** one or more product-epic umbrellas (cross-cutting tracking).

```text
              ┌─────────────────────────────────────────────────────┐
              │  PRODUCT-EPIC UMBRELLAS  (consumer narrative)       │
              ├─────────────────────────────────────────────────────┤
              │  3zol — Refiner library                             │
              │  jsy3 — /j-rig plugin + 3-layer hooks               │
              │  0r8m — Evidence + Tier-1 kernel integration        │
              └────┬────────┬────────┬────────┬────────┬────────────┘
                   │        │        │        │        │   (refs-only edges)
                   ▼        ▼        ▼        ▼        ▼
      ┌────────────────────────────────────────────────────────────┐
      │  PER-REPO COORDINATION EPICS  (work-owner locality)        │
      ├──────────┬──────────┬──────────┬──────────┬───────────────┤
      │ RC-IEL   │ RC-IEC   │ RC-IAJ   │ RC-IAH   │ RC-IAR        │
      │ iel      │ iec      │ iaj      │ iah      │ iar           │
      │          │          │          │          │               │
      │ specs    │ kernel   │ j-rig    │ audit-   │ intent-       │
      │ glossary │ entity   │ pkg+CLI  │ harness  │ rollout-gate  │
      │ DRs      │ schema   │ plugin   │ baseline │ consumer      │
      │ HTML     │ release  │ hooks    │          │               │
      └──────────┴──────────┴──────────┴──────────┴───────────────┘
```

### Per-repo cluster epic inventory (5 NEW beads)

| New bead | Title                                                                                                     | Labels                                 | Touch points                                                                                                                                              |
| -------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RC-IEL` | Skill Refiner — intent-eval-lab coordination (specs, glossary, DRs, blueprints)                           | `refiner`, `epic`, `coord`, `repo:iel` | Blueprint B extension, glossary update, ISEDC DR, SPEC.md template, HTML renderer Hugo template, tri-link spec doc, 3 new architecture docs (028/029/030) |
| `RC-IEC` | Skill Refiner — intent-eval-core coordination (SkillVersion entity, validator, schema, release)           | `refiner`, `epic`, `coord`, `repo:iec` | SkillVersion schema + Zod validator, skill-refiner-pass predicate schema, v0.3.0 release ceremony, boundary table update                                  |
| `RC-IAJ` | Skill Refiner — j-rig-binary-eval coordination (refiner pkg, CLI, plugin, hooks, evidence emit)           | `refiner`, `epic`, `coord`, `repo:iaj` | refiner-core + refiner packages, j-rig refine CLI, j-rig emit-refiner-pass CLI, optimizer-types extension                                                 |
| `RC-IAH` | Skill Refiner — intent-audit-harness coordination (gate-result row for refiner-pass, baseline update)     | `refiner`, `epic`, `coord`, `repo:iah` | Evidence Bundle envelope design notes update, baseline update for refiner-pass                                                                            |
| `RC-IAR` | Skill Refiner — intent-rollout-gate coordination (consume skill-refiner-pass/v1 predicate, action wiring) | `refiner`, `epic`, `coord`, `repo:iar` | M5 runtime extension to consume skill-refiner-pass/v1 rows as advisory enrichment                                                                         |

### Leaf task inventory (13 NEW beads, filling per-repo gaps)

| New bead | Repo | Title                                                                                                            | Parent (product epic) | Also deps on       |
| -------- | ---- | ---------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------ |
| `IAJ-N1` | iaj  | Create `packages/refiner-core/` boundary split (pure value-objects, zero adapters)                               | `3zol`                | `RC-IAJ`           |
| `IAJ-N2` | iaj  | Wire `@j-rig/refiner` into existing j-rig pnpm workspace + release flow                                          | `3zol`                | `RC-IAJ`           |
| `IAJ-N3` | iaj  | Add `j-rig refine bootstrap <skill-path>` CLI subcommand (synthetic eval-set generator)                          | `3zol`                | `RC-IAJ`           |
| `IAJ-N4` | iaj  | Vitest coverage gate ≥ 80% on `refiner-core/` per j-rig harness baseline                                         | `3zol`                | `RC-IAJ`           |
| `IAJ-N5` | iaj  | Document refiner-core API in `j-rig-binary-eval/000-docs/021-AT-SPEC-refiner-core-api.md`                        | `3zol`                | `RC-IAJ`, `RC-IEL` |
| `IEC-N1` | iec  | Add `SkillVersion` entry to `intent-eval-core` boundary table doc                                                | `0r8m`                | `RC-IEC`           |
| `IEC-N2` | iec  | Update `intent-eval-core` repo blueprint ER diagram to show 14th entity                                          | `0r8m`                | `RC-IEC`           |
| `IEL-N1` | iel  | Author `intent-eval-lab/000-docs/028-AT-SPEC-skill-refiner-pass-v1-predicate.md` (normative predicate spec)      | `0r8m`                | `RC-IEL`           |
| `IEL-N2` | iel  | Author `intent-eval-lab/000-docs/029-AT-ARCH-skill-refiner-3-layer-hooks.md` (architecture ref + ASCII diagrams) | `jsy3`                | `RC-IEL`           |
| `IEL-N3` | iel  | Update `014-DR-GLOS-canonical-glossary.md` with Skill Refiner brand canon                                        | `0r8m.5`              | `RC-IEL`           |
| `IAH-N1` | iah  | Add `skill-refiner-pass/v1` gate-result row schema to audit-harness Evidence Bundle envelope design notes        | `0r8m`                | `RC-IAH`           |
| `IAH-N2` | iah  | Update audit-harness baseline to include refiner-pass                                                            | `0r8m`                | `RC-IAH`           |
| `IAR-N1` | iar  | Wire intent-rollout-gate Action to consume `skill-refiner-pass/v1` rows from Evidence Bundle                     | `0r8m`                | `RC-IAR`           |

### Tri-linkage backfill inventory (5 NEW beads + 1 umbrella)

| New bead  | Repo     | Title                                                                                 |
| --------- | -------- | ------------------------------------------------------------------------------------- |
| `TL-EPIC` | umbrella | Doc/bead/GH-issue tri-linkage discipline rollout                                      |
| `TL-IEL`  | iel      | Backfill Beads: header in all 28 intent-eval-lab docs touched by Skill Refiner work   |
| `TL-IEC`  | iec      | Backfill Beads: header in all intent-eval-core docs touched by Skill Refiner work     |
| `TL-IAJ`  | iaj      | Backfill Beads: header in all 20 j-rig-binary-eval docs touched by Skill Refiner work |
| `TL-IAH`  | iah      | Backfill Beads: header in all audit-harness docs touched by Skill Refiner work        |
| `TL-IAR`  | iar      | Backfill Beads: header in all intent-rollout-gate docs touched by Skill Refiner work  |

### Diagram inventory (9 NEW beads — one per canonical diagram in § 6.5)

| New bead  | Diagram                                                 | Lives in (doc)                                                            | Parent    |
| --------- | ------------------------------------------------------- | ------------------------------------------------------------------------- | --------- |
| `DIAG-D1` | 3-product agent-rig stack                               | `iel/029-AT-ARCH-skill-refiner-3-layer-hooks.md` § 1                      | `RC-IEL`  |
| `DIAG-D2` | 5-repo IEP ecosystem                                    | `iel/011-AT-ARCH-ecosystem-master-blueprint.md` (append § 12)             | `RC-IEL`  |
| `DIAG-D3` | 3-layer hook architecture (hook/line/sinker)            | `iel/029-AT-ARCH-skill-refiner-3-layer-hooks.md` § 3                      | `RC-IEL`  |
| `DIAG-D4` | Skill Refiner data flow                                 | `iaj/021-AT-SPEC-refiner-core-api.md` § 2                                 | `RC-IAJ`  |
| `DIAG-D5` | SkillVersion ER diagram                                 | `iec/002-AT-ARCH-repo-blueprint-2026-05-18.md` (replace existing § ER)    | `RC-IEC`  |
| `DIAG-D6` | Bead dependency graph                                   | `iel/029-AT-ARCH-skill-refiner-3-layer-hooks.md` appendix A               | `RC-IEL`  |
| `DIAG-D7` | Doc ↔ bead ↔ GH-issue tri-link topology                 | `iel/030-AT-STND-tri-linkage-discipline.md` § 2                           | `TL-EPIC` |
| `DIAG-D8` | Refiner library architecture (core vs adapter)          | `iaj/021-AT-SPEC-refiner-core-api.md` § 3                                 | `RC-IAJ`  |
| `DIAG-D9` | Evidence bundle row lifecycle for skill-refiner-pass/v1 | `iah/001-DR-DESIGN-evidence-bundle-envelope-design-notes.md` (append § 9) | `RC-IAH`  |

### Total bead count

Existing: 3 product epics + 26 leaf children + 5 deferred standalone = 34
NEW: 5 RC-_+ 13 leaf-N + 1 TL-EPIC + 5 TL-_ + 9 DIAG-\* = 33
**Grand total: 67 beads** (within the 60-bead cap target with light overshoot for diagram beads).

### Tri-linkage verification (`validate-trilink.sh`)

A bash script lives at `intent-eval-platform/intent-eval-lab/scripts/validate-trilink.sh` (symlinked from `~/bin/validate-trilink`). It does three checks:

1. **Bead → Doc/GH presence.** For every bead labeled `refiner`, parse description; require both `Doc:` and `GitHub:` lines. Report missing.
2. **Doc → Bead presence.** For every `000-docs/*.md` in the five repos that contains any `bd_000-projects-` substring in its body, require a `Beads:` line in the front-matter table. Report missing.
3. **GH issue → Bead/Doc presence.** For every GH issue under labels `refiner` across the five repos, fetch body via `gh issue list --json`; require both `Bead:` and `Doc:` lines.

Output: one line per violation, prefixed with violation class (`MISS-DOC`, `MISS-GH`, `MISS-FRONT`, `MISS-GH-BEAD`), then the artifact id and a short title. Exit non-zero on any violation.

CI integration: add a `.github/workflows/trilink.yml` to each of the five repos that runs the script scoped to that repo (filter `--label refiner` to that repo's GH; filter docs to that repo's `000-docs/`). Fires on PRs that touch `000-docs/**.md` or `.beads/issues.jsonl`. Failure blocks merge for Skill Refiner-labeled work only; legacy work is exempted by the label filter.

### bd-sync extension

The existing `~/bin/bd-sync` already extracts `GitHub:` and `Plane:` refs. Extending for tri-link enforcement:

1. **New extractor `extract_doc_refs`** mirroring the existing two, grepping for `^Doc:\s*[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+\.md`.
2. **New `bd-sync link` precondition**: when running with `--gh OWNER/REPO#N`, require the bead's description already carries a `Doc:` line, OR accept a new `--doc <path>` flag that injects one as the link is created.
3. **New mirror step inside `gh_comment`/`gh_close`**: when bd-sync posts to GH, also inject/update the `Bead:` and `Doc:` footer in the GH issue body via `gh issue edit --body-file`. Self-healing drift.

Scope: only activate the new enforcement for beads carrying label `refiner`. Legacy beads keep the old two-corner discipline.

---

## 6. Reused infrastructure (per Plan Mode discipline — reuse over reinvent)

| Component                                                                        | Location                                                                                      | Reused for                                                                                                                                 |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `/skill-creator` skill                                                           | `~/.claude/skills/skill-creator/SKILL.md`                                                     | (was Phase D scaffold; Phase D deferred)                                                                                                   |
| `/validate-skillmd` skill                                                        | `~/.claude/skills/validate-skillmd/SKILL.md`                                                  | Phase B Sinker (L1) deterministic gate (Tier 2 checks); extended per AC-11 for agentskills.io spec compliance                              |
| `/audit-tests` + `/implement-tests`                                              | `~/.claude/skills/`                                                                           | Phase A bootstrap — eval-set bootstrap can mirror their 7-layer taxonomy approach                                                          |
| `/validate-consistency` skill                                                    | `~/.claude/skills/validate-consistency/SKILL.md`                                              | PR-2 pre-code gate; runs at Phase kickoff, every PR pre-merge, doc reorg, plan revision, quarterly                                         |
| `/validate-plugin` skill                                                         | `~/.claude/skills/validate-plugin/SKILL.md`                                                   | Phase B plugin validation pre-marketplace-publish; AC-11 portability claim emission                                                        |
| `/exec-decision-council` skill                                                   | `~/.claude/skills/exec-decision-council/SKILL.md`                                             | Phase C ISEDC Session 7; § 12 Plan Audit ratification                                                                                      |
| `/appaudit` skill                                                                | `~/.claude/skills/appaudit/SKILL.md`                                                          | Phase E HTML render — appaudit already produces partner-grade PDF reports                                                                  |
| `/release` skill                                                                 | `~/.claude/skills/release/SKILL.md`                                                           | Phase A + B release ceremonies (8-phase)                                                                                                   |
| `/branch-protection` skill                                                       | `~/.claude/skills/branch-protection/SKILL.md`                                                 | Phase C kernel v0.3.0 release uses this for protected-main push pattern                                                                    |
| `/gist-auditor` skill                                                            | `~/.claude/skills/gist-auditor/SKILL.md`                                                      | Phase A pre-flight: run against j-rig gist (carry-over from old plan)                                                                      |
| `j-rig optimizer/types.ts` (`ChangeProposal`, `Experiment`, `OptimizerProvider`) | `j-rig-binary-eval/packages/core/src/optimizer/`                                              | Phase A library extends these with value-oriented hash-chain wrapping                                                                      |
| `j-rig eval`/`optimize`/`check`/`emit-evidence` CLI                              | `j-rig-binary-eval/packages/cli/src/commands/`                                                | Phase A library DELEGATES scoring to these (no re-implementation)                                                                          |
| `audit-harness emit-evidence` subcommand                                         | `intent-audit-harness/scripts/emit-evidence.sh`                                               | Phase A library uses for in-toto Statement v1 emission                                                                                     |
| `SkillSnapshot` entity (existing)                                                | `intent-eval-core/schemas/v1/skill-snapshot.schema.json`                                      | Phase C SkillVersion extends/references this (NOT a duplicate — SkillSnapshot pins source state; SkillVersion captures refinement lineage) |
| `gate-result/v1` predicate                                                       | `intent-eval-core/schemas/v1/gate-result.schema.json` + Blueprint B § 7                       | Phase A library emits these from refinement passes via j-rig                                                                               |
| Anthropic security-guidance plugin source                                        | `~/anthropic/claude-code/plugins/security-guidance/` (locally cached per Phase 1 exploration) | Phase B reference implementation for 3-layer hook architecture                                                                             |
| Partner-portal infrastructure (Hugo)                                             | `~/000-projects/partner-portals/`                                                             | Phase E HTML render hosting (same Hugo template; new section `evals.intentsolutions.io/reports/`)                                          |
| `~/bin/bd-sync` three-layer mirror                                               | (extended per § 5.5 for tri-link discipline)                                                  | All new beads filed per the discipline                                                                                                     |
| `~/.claude/agents/beads-guru.md`                                                 | created earlier this session                                                                  | Authoritative bd workflow expert; consult for any per-repo bead structure questions                                                        |
| 14 thinker-canon reviewer agents                                                 | `~/.claude/agents/*-reviewer.md`                                                              | § 12 Plan Audit panel (7 seats picked)                                                                                                     |
| Doc Filing Standard v4.x                                                         | `intent-eval-lab/000-docs/` + `/doc-filing` skill                                             | All new doc filenames + numbering                                                                                                          |

---

## 6.5. ASCII Diagrams Catalog

Per user direction 2026-05-26: "ASCII diagrams, reference for reference and beads. I want documentation everywhere that's appropriate."

Nine canonical diagrams. Each has a corresponding bead (DIAG-D1..D9 in § 5.5) tracking its production. Diagrams are sourced HERE; embedded in companion docs by reference.

### D1 — Three-product agent-rig stack

**Lives in:** `intent-eval-lab/000-docs/029-AT-ARCH-skill-refiner-3-layer-hooks.md` § 1
**Bead:** `DIAG-D1`

```text
┌──────────────────────────────────────────────────────────────────────┐
│         INTENT SOLUTIONS — AGENT-RIG STACK (3 products)              │
└──────────────────────────────────────────────────────────────────────┘

   ┌────────────────────────┐    ┌────────────────────────┐    ┌────────────────────────┐
   │  J-Rig Skill Binary    │    │   Skill Refiner        │    │   Rollout Gate         │
   │  Eval     (shipped)    │───▶│   (this build)         │───▶│   (in flight M5)       │
   │                        │    │                        │    │                        │
   │  TEST                  │    │  IMPROVE               │    │  SHIP                  │
   │  7-layer harness       │    │  bounded SKILL.md      │    │  GitHub Action         │
   │  rollouts → scores     │    │  edits, gated by       │    │  evidence + policy     │
   │                        │    │  score deltas          │    │  → ship / no-ship      │
   └─────────┬──────────────┘    └─────────┬──────────────┘    └─────────┬──────────────┘
             │                              │                              │
             │ ScoreRecord                 │ SkillVersion +               │ verdict +
             │                              │ skill-refiner-pass/v1        │ Evidence Bundle
             ▼                              ▼                              ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │       EVIDENCE BUNDLE  (intent-eval-core canonical schema, 14 entities) │
    └─────────────────────────────────────────────────────────────────────────┘
```

### D2 — Five-repo IEP ecosystem with Skill Refiner integration points

**Lives in:** `intent-eval-lab/000-docs/011-AT-ARCH-ecosystem-master-blueprint.md` (append § 12)
**Bead:** `DIAG-D2`

```text
                       ┌─────────────────────────────┐
                       │   intent-eval-lab  (iel)    │
                       │   methodology + specs       │
                       │   ★ skill-refiner-pass/v1   │  ← new normative spec
                       │     predicate spec          │
                       └──────────────┬──────────────┘
                                      │ governs
                ┌─────────────────────┼─────────────────────┐
                ▼                     ▼                     ▼
   ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
   │ intent-eval-core   │  │ j-rig-binary-eval  │  │ intent-audit-      │
   │       (iec)        │  │       (iaj)        │  │ harness    (iah)   │
   │                    │  │                    │  │                    │
   │ ★ SkillVersion     │◀─│ ★ @j-rig/refiner   │  │ ★ refiner-pass     │
   │   (14th entity)    │  │   pkg + /j-rig     │  │   gate-result row  │
   │ ★ Zod validator    │  │   plugin + 3-layer │  │   schema           │
   │ ★ release v0.3.0   │  │   hooks            │  │                    │
   └─────────┬──────────┘  └─────────┬──────────┘  └─────────┬──────────┘
             │                       │                       │
             │  schema dep           │  emits                │  emits
             ▼                       ▼                       ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │              Evidence Bundle  (the schema-layer convergence)     │
   └──────────────────────────────┬───────────────────────────────────┘
                                  │ consumed by
                                  ▼
                       ┌─────────────────────────────┐
                       │ intent-rollout-gate  (iar)  │
                       │ ★ consume refiner-pass row  │
                       │   → ship/no-ship verdict    │
                       └─────────────────────────────┘

   ★ = new touch-point for Skill Refiner buildout
```

### D3 — 3-layer hook architecture (hook · line · sinker)

**Lives in:** `intent-eval-lab/000-docs/029-AT-ARCH-skill-refiner-3-layer-hooks.md` § 3
**Bead:** `DIAG-D3`

```text
   CLAUDE CODE LIFECYCLE                  REFINER LAYER          COST TIER    MODEL
   ════════════════════════════════════════════════════════════════════════════════

   PostToolUse: Edit/Write on SKILL.md  →  ┌─────────────┐
                                            │  SINKER L1  │       $0          (none)
                                            │  deterministic    drops fast
                                            │  validate-     ─── anchors rig
                                            │  skillmd Tier 2│
                                            └──────┬──────┘
                                                   │ pass?
                                                   ▼ (warning to context if fails)

   Stop  (end of turn)                  →   ┌─────────────┐
                                            │  LINE   L2  │       $           Haiku (score)
                                            │  rollout       fires refiner    Sonnet (refine)
                                            │  capture +     after N rollouts
                                            │  bg refiner   │
                                            └──────┬──────┘
                                                   │ proposal accepted?
                                                   ▼ (candidate surfaced next turn)

   PostToolUse: Bash matches            →   ┌─────────────┐
   git commit | git push                    │  HOOK   L3  │       $$          Opus
   on staged SKILL.md diff                  │  agentic gate  rate-limited
                                            │  + rejected-   sets the catch
                                            │  edit buffer +
                                            │  shadow eval  │
                                            └──────┬──────┘
                                                   │
                                                   ▼ (block commit or annotate PR)
                                          ┌─────────────────┐
                                          │  Evidence emit  │  signed AAR (md)
                                          │  + Rekor log    │  + HTML projection
                                          └─────────────────┘
```

### D4 — Skill Refiner data flow

**Lives in:** `j-rig-binary-eval/000-docs/021-AT-SPEC-refiner-core-api.md` § 2
**Bead:** `DIAG-D4`

```text
   ┌─────────────┐
   │  rollouts   │  (N runs of skill against held-out eval-set)
   │  (j-rig     │
   │   harness)  │
   └──────┬──────┘
          │  ScoreRecord[]
          ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                        REFINER-CORE  (pure)                 │
   │  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
   │  │ score()  │───▶│ propose()│───▶│ accept() │               │
   │  └──────────┘    └──────────┘    └─────┬────┘               │
   │  multi-dim score   bounded edit ops    │ strict improvement │
   │  never collapsed   (add/del/replace)   │ on all dims?       │
   └─────────────────────────────────────────┼───────────────────┘
                                             │ yes               │ no
                                             ▼                   ▼
                              ┌──────────────────────┐  ┌──────────────────┐
                              │  new SkillVersion    │  │ rejected-edit    │
                              │  (content-addressed) │  │ buffer (kept,    │
                              │  parent = prior hash │  │ shown in AAR)    │
                              └──────────┬───────────┘  └──────────────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  promotion ladder    │
                              │  shadow → canary →   │
                              │  promote (HUMAN)     │
                              └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  Evidence Bundle row │
                              │  skill-refiner-pass  │
                              │  /v1  → Rekor (stg)  │
                              └──────────────────────┘
```

### D5 — SkillVersion ER diagram

**Lives in:** `intent-eval-core/000-docs/002-AT-ARCH-repo-blueprint-2026-05-18.md` (replace existing § ER)
**Bead:** `DIAG-D5`

```text
   ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
   │  SkillSnapshot  │         │   SkillVersion  │         │    EvalSet      │
   │─────────────────│         │─────────────────│         │─────────────────│
   │ hash (PK)       │◀────────│ parent_hash (FK)│         │ hash (PK)       │
   │ skill_md_text   │         │ hash (PK, ★14th)│         │ items[]         │
   │ created_at      │         │ ops[]           │         │ bootstrap_src   │
   └─────────────────┘         │ refiner_model   │         │ created_at      │
                               │ rationale       │         └────────┬────────┘
                               │ accepted_at     │                  │
                               │ actor_id        │                  │
                               │ spec_version    │                  │
                               └────────┬────────┘                  │
                                        │ scored by                 │ scored against
                                        ▼                           │
                               ┌─────────────────┐                  │
                               │  ScoreRecord    │◀─────────────────┘
                               │─────────────────│
                               │ skill_hash (FK) │
                               │ eval_set (FK)   │
                               │ behavioral      │
                               │ readability     │
                               │ adv_pass_rate   │
                               │ ...             │
                               └────────┬────────┘
                                        │ informs
                                        ▼
                               ┌─────────────────┐
                               │  EditProposal   │
                               │─────────────────│
                               │ parent (FK)     │
                               │ ops[]           │
                               │ status: a/r     │
                               │ refiner-pass-v1 │ ──→ Evidence Bundle
                               └─────────────────┘

   ★ = the 14th canonical entity added by this buildout
```

### D6 — Bead dependency graph (Skill Refiner work)

**Lives in:** `intent-eval-lab/000-docs/029-AT-ARCH-skill-refiner-3-layer-hooks.md` appendix A
**Bead:** `DIAG-D6`

```text
   PRODUCT EPICS (roll-up)              PER-REPO COORD EPICS (locality)
   ─────────────────────────            ────────────────────────────────
   3zol  Refiner lib v0.1.0  ─┐       ┌─ RC-IAJ  j-rig coord
                              │       │
   jsy3  /j-rig plugin       ─┤       ├─ RC-IEC  intent-eval-core coord
         + 3-layer hooks      │       │
                              ├──────▶├─ RC-IEL  intent-eval-lab coord
   0r8m  SkillVersion +      ─┘       │
         Tier-1 kernel               ─┤─ RC-IAH  intent-audit-harness coord
                                       │
                                      └─ RC-IAR  intent-rollout-gate coord

   P0 CRITICAL CHAIN  (must close in order)
   ────────────────────────────────────────
   uprg ──▶ 9pi3 ──▶ 0r8m.7 (ISEDC-7) ──▶ 0r8m.1..6 ──▶ 0r8m.8 (release)
   (compat  (OTel    (decision)            (kernel work)    (ceremony)
    pol)     pin)

   TRI-LINK ROLLOUT (parallel track)
   ─────────────────────────────────
   TL-EPIC ──▶ TL-IEL, TL-IEC, TL-IAJ, TL-IAH, TL-IAR  (one per repo, parallel)

   DIAGRAM TRACK (parallel)
   ─────────────────────────
   DIAG-D1..D9  (each blocks its parent RC-* epic from closing)
```

### D7 — Doc ↔ bead ↔ GH-issue tri-link topology

**Lives in:** `intent-eval-lab/000-docs/030-AT-STND-tri-linkage-discipline.md` (NEW) § 2
**Bead:** `DIAG-D7`

```text
              ┌────────────────────────────┐
              │      DOC  (.md in repo)    │
              │ NNN-XX-CCCC-<slug>.md      │
              │ front-matter:              │
              │   Beads: bd_…-0r8m.1       │
              │   Beads: RC-IEC            │
              │   GitHub: owner/repo#42    │
              └────────────┬───────────────┘
                           │                                  cited in
        cites in           │                          ┌──────────────────────┐
        description        │                          │                      │
              ┌────────────┴───────────────┐          ▼                      │
              │     BEAD  (bd issue)       │   ┌────────────────────┐        │
              │ id: bd_…-0r8m.1            │◀──│  GH ISSUE          │        │
              │ description ends with:     │   │  body ends with:   │        │
              │   Doc: iec/000-docs/...    │   │    Bead: bd_…-0r8m.1│       │
              │   GitHub: owner/repo#42    │──▶│    Doc: iec/000-... │       │
              └────────────────────────────┘   └──────────┬─────────┘        │
                           ▲                              │                  │
                           │                              │ comments mirrored│
                           │      bd-sync mirrors         │ via bd-sync      │
                           └──────────────────────────────┴──────────────────┘

   INVARIANT: any new artifact in the triangle must be born with the other two
   references already present. CI gate (validate-trilink.sh in § 5.5) rejects
   merges that violate the invariant for any artifact in 000-docs/ touching
   label 'refiner'.
```

### D8 — Refiner library architecture (core vs adapter)

**Lives in:** `j-rig-binary-eval/000-docs/021-AT-SPEC-refiner-core-api.md` § 3
**Bead:** `DIAG-D8`

```text
   ┌──────────────────────────────────────────────────────────────────────┐
   │                       @j-rig/refiner  (npm)                          │
   │   thin orchestrator + CLI binding; depends on refiner-core           │
   └──────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │                   @j-rig/refiner-core  (npm)                         │
   │   PURE value-oriented library — zero adapters, zero side effects     │
   │                                                                       │
   │   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │
   │   │ score()        │  │ propose()      │  │ accept()       │         │
   │   │ (interface)    │  │ (interface)    │  │ (PURE FN)      │         │
   │   └────────────────┘  └────────────────┘  └────────────────┘         │
   │                                                                       │
   │   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │
   │   │ apply()        │  │ bootstrap()    │  │ value types    │         │
   │   │ (PURE FN)      │  │ (synthesis     │  │ (SkillDocHash, │         │
   │   │                │  │  helper)       │  │  ScoreRecord,  │         │
   │   │                │  │                │  │  EditProposal) │         │
   │   └────────────────┘  └────────────────┘  └────────────────┘         │
   │   No fs. No network. No process.exit. Deterministic given inputs.    │
   │   ≥80% coverage gate. Mutation testing optional.                     │
   └──────────────────────────────────────────────────────────────────────┘

   ADAPTERS (live in @j-rig/refiner, NOT core):
     • model adapter (Anthropic SDK / mock)
     • fs adapter   (read SKILL.md, write SkillVersion)
     • binary-eval adapter (shell-out to j-rig CLI)
     • emit adapter (audit-harness shell-out → Evidence Bundle + Rekor)
     • cost meter   (tiered routing budget)

   Swap rule: when frontier-native refinement arrives, replace
   propose() impl in refiner with a thin shim; keep adapters,
   keep tests, keep the acceptance gate. THAT is the durable contribution.
```

### D9 — Evidence bundle row lifecycle for skill-refiner-pass/v1

**Lives in:** `intent-audit-harness/000-docs/001-DR-DESIGN-evidence-bundle-envelope-design-notes.md` (append § 9)
**Bead:** `DIAG-D9`

```text
   refiner accept()              audit-harness                intent-rollout-gate
   ─────────────────              ─────────────                ───────────────────

   SkillVersion v_new   ──emit──▶  gate-result row
                                  ┌────────────────────────┐
                                  │ predicate:             │
                                  │   skill-refiner-pass/v1│
                                  │ subject:               │
                                  │   sha256:<v_new.hash>  │
                                  │ result: pass | fail    │
                                  │ score_deltas: {…}      │
                                  │ rejected_buffer: [...] │
                                  │ actor: <human|claude>  │
                                  │ provenance: sigstore   │
                                  │ spec_version: v1.0.0   │
                                  └───────────┬────────────┘
                                              │  bundle.jsonl
                                              ▼
                                  ┌────────────────────────┐
                                  │  Evidence Bundle       │
                                  │  (canonical, signed)   │
                                  └───────────┬────────────┘
                                              │
                                              ▼  consumed
                                  ┌────────────────────────┐
                                  │  intent-rollout-gate   │
                                  │  Action evaluates row  │
                                  │  against TESTING.md    │
                                  │  policy →              │
                                  │  ship / no-ship verdict│
                                  └────────────────────────┘
```

---

## 7. Open questions for user (deferred to Phase A kickoff, not blocking plan)

Resolved in earlier brand-canon iterations:

- ~~§ 7.1 packaging (separate repo vs monorepo)~~ — **RESOLVED**: j-rig monorepo, `@j-rig/*` scope, two packages `refiner-core` + `refiner`
- ~~§ 7.2 creator-product name~~ — **RESOLVED**: deferred indefinitely (no creator product ships)
- ~~§ 7.3 npm scope~~ — **RESOLVED**: `@j-rig/*` (not `@intentsolutions/*`)
- ~~§ 7.4 brand framing (sub-product vs peer-product)~~ — **RESOLVED**: Skill Refiner is peer-product to J-Rig Binary Eval + Rollout Gate

Still open (Phase A claim should resolve):

1. **Phase B target skill for end-to-end demo**: `/audit-tests` (rich invocation history, cleaner blog post) OR `/validate-skillmd` (meta-recursive, sharper IP-defense story)?
2. **Phase C kernel version sequencing**: v0.2.0 ships `EvidenceBundlePayload` per existing `iec-E12`; SkillVersion lands in v0.3.0. Honors expand-contract Parallel Change (`bd_000-projects-xcs4`). Confirm.
3. **§ 2.5 research item**: which specific SkillMD publication did the user reference? Phase 1 brief-pack assembly (§ 13 Step 0) resolves via WebFetch against `agentskills.io/specification`.

---

## 8. Risks + mitigations

| Risk                                                                                                                                         | Mitigation                                                                                                                                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Frontier moves faster than this plan — Skill Refiner gets eaten by frontier-native skill refinement in 6-12mo (Karpathy bitter-lesson check) | Phase A library exposes pure-function value API; refiner mechanism (add/delete/replace + textual learning rate) is a pluggable strategy behind the gate, not the core contract. When frontier-native arrives: swap the strategy, keep the harness                                                                      |
| Self-generated skills (deferred creator) clear our internal eval but bomb in the wild — Goodhart (SkillsBench warning)                       | Multi-dimensional score records (behavioral + readability + adversarial-set-pass-rate) per AC-3. `confidence_tier` field gates marketplace publication. Hard refuse to ship a generated skill that fails the SkillsBench negative-baseline check. Phase D deferred indefinitely until external evidence clears the bar |
| Cost runaway — naive Opus-everywhere costs $11K/month for 30 skills (Huyen)                                                                  | Tiered routing per AC-5: Haiku for rollout-scoring, Sonnet for refiner-proposer, Opus only for final-validation. Hard budget cap at workflow level + alert at 80%                                                                                                                                                      |
| Phase C blocks on `uprg`+`9pi3` indefinitely                                                                                                 | Phase A + Phase B are NOT blocked on Phase C — they use existing `gate-result/v1` and `SkillSnapshot` + emit via j-rig. Phase C is the polish/first-class-ness layer. Plan can ship A+B without C                                                                                                                      |
| `bd_000-projects-bj5m`-style branch-protection failures on Phase C kernel release                                                            | Already mitigated — j-rig adopted tag-trigger pattern (PR #80, 2026-05-26). Phase C uses same pattern in intent-eval-core release.yml (already canonical)                                                                                                                                                              |
| Eval-set bootstrap is the unsexy 80% (Huyen) and Phase A skips it = no usable plugin                                                         | Phase A bootstrap is FIRST-CLASS (not deferred) per AC-6. Three sources: synthetic-from-SKILL.md + j-rig rollout-harvest + human-nominated-golden. All three implemented in Phase A                                                                                                                                    |
| `iah-npm-publish-gap` (audit-harness git v1.1.4 vs npm v0.1.0) blocks consumer reach                                                         | Phase C must close this — intent-audit-harness needs release.yml + first npm publish from v1.1.4 OR Phase C explicitly notes the gap. Filed as bead; tracked separately                                                                                                                                                |
| Reports become a brand-surface explosion if every refinement run gets a public HTML page                                                     | Markdown is canonical (in git); HTML is OPT-IN per-report (defaults to internal-only). Public reports gated by quality + human approval (mirrors `iep-gist-coverage` policy)                                                                                                                                           |
| Plugin (Phase B) marketed as "automated skill optimization" → consumer expects auto-magic → trust failure on first bad edit                  | Marketing position is "evals-gated skill edits" per AC-10. Every report shows the rejected-edits buffer alongside accepted ones. Trust comes from showing the work, not hiding it                                                                                                                                      |
| agentskills.io spec changes between plan ratification and Phase A code                                                                       | AC-11 pins the spec version in every SkillVersion record. § 13 Step 0 freezes a spec snapshot in the Refiner repo at Phase A kickoff. Spec revs trigger a re-pin event (new bead, new SkillVersion records carry new spec_version) — not a retroactive change                                                          |
| per-repo bead clusters require label discipline that's easy to forget                                                                        | § 5.5 `validate-trilink.sh` runs in CI; bd-sync extension enforces at link-time; beads-guru agent at `~/.claude/agents/beads-guru.md` is the authoritative reference for any human in doubt                                                                                                                            |
| this plan is itself a risk — written by one author (Claude), might miss things                                                               | § 12 Plan Audit phase: 7-seat thinker-canon panel reviews plan BEFORE any code; § 13 Step 5 codifies this as mandatory before first `bd claim`                                                                                                                                                                         |
| tri-linkage backfill burden could swamp Skill Refiner work                                                                                   | Scope discipline: tri-link backfill is in-scope only for Skill Refiner-labeled artifacts. Legacy 322+ beads are tolerated debt; not retroactively swept. New work is born compliant via CI gate                                                                                                                        |

---

## 9. Verification (end-to-end)

Phase-by-phase exit criteria are listed inline in § 4. Aggregate plan-completion criteria (when does the WHOLE plan ship?):

1. **§ 12 Plan Audit ratified**: ≤ 0 BLOCKERs, ≤ 3 MAJORs across 7 seats; ISEDC ratification filed
2. **§ 13 Execution Sequence Steps 1-4 complete**: all per-repo beads filed, all GH issues created with bead citations, `validate-trilink.sh` exits 0, `/validate-consistency` reports zero BLOCKERs
3. **Phase A ships**: `npm view @j-rig/refiner-core` + `npm view @j-rig/refiner` both return v0.1.0+ with sigstore provenance
4. **Phase B ships**: `/j-rig` plugin available in claude-code-plugins marketplace; ONE real skill refined end-to-end with shipped score-delta evidence; blog post published
5. **Phase C ships** (gated on `uprg`+`9pi3`): `@intentsolutions/core@0.3.0` npm-published with SkillVersion entity; `skill-refiner-pass/v1` predicate URI live (test signed via cosign + Rekor staging); ISEDC Session 7 DR filed
6. **Phase D**: stays DEFERRED until external trigger fires
7. **Phase E ships**: report template at `intent-eval-lab/specs/skill-refiner-evidence-report/v1.0.0-draft/SPEC.md`; HTML renderer live at `evals.intentsolutions.io/reports/`; one real report generated end-to-end (Phase B demo)
8. **Phase F triggers** (NOT ship — trigger): when ≥ 5 partners consume refined skills OR ≥ 100 active SkillVersion records OR first rollback incident

If any phase exit-criterion fails for > 2 weeks past target: pause, file an ISEDC session, re-plan.

---

## 10. Stopping criteria

- Frontier ships a frontier-native skill-refinement mechanism that subsumes Phase A's discipline → archive Phases A-D as historical OSS contribution; keep Phase E (reports) as durable interface; Phase F may still be relevant
- Phase B end-to-end demo fails to show meaningful score-delta on ANY real skill → DO NOT promote to wider rollout; the discipline didn't work in this codebase, no point doubling down
- SkillsBench-style negative-baseline finding REPLICATES on our skills → keep Phases A+B as internal-only tooling; do not market externally
- Phase C `uprg` or `9pi3` cannot be closed (e.g., compat policy can't be agreed) → Phase C stays deferred; Phases A+B continue without first-class kernel integration
- Plan Audit (§ 12) returns ≥1 BLOCKER that cannot be remediated within 2 audit iterations → plan is declared structurally broken and re-drafted from scratch

---

## 11. What this plan does NOT do

- Does not advance ANY current bead beyond the ones already filed (uprg, 9pi3, 59tx, tyck, uop6, 5qcy, 9yhe, xcs4, bj5m, q9vn, iah-npm-publish-gap, iep-gist-coverage). Per-repo cluster bead filing happens during § 13 Execution Sequence Step 1, NOT during plan mode.
- Does not write any code. Plan mode is design-only. Implementation begins at § 13 Step 7 (first `bd claim`).
- Does not pick the Phase B demo skill (`/audit-tests` vs `/validate-skillmd`) — open question.
- Does not address the broader gist-coverage work (4 missing gists across intent-audit-harness, intent-eval-core, intent-eval-lab, intent-rollout-gate). Those stay under `iep-gist-coverage` bead per prior plan's CTO call.
- Does not address P6 Phase A3+ linting infrastructure (separate workstream).
- Does not advance the Plane / GH / bd projection inversion (`q9vn` design spike) — separate workstream.
- Does not retroactively backfill tri-linkage discipline against the 322+ legacy open beads. Only Skill Refiner beads + new work are in scope.
- Does not commit to cross-vendor distribution channels (Vercel skills.sh, Anthropic skills marketplace, etc.) beyond noting them as Phase F considerations.
- Does not specify the bandwidth model in calendar weeks beyond rough budgets. Calendar weeks are placeholders; actual durations depend on bandwidth and ecosystem-fold P0 chain closures.

---

## 12. Plan Audit phase

### Framing

A plan written by its author (even a multi-agent author) is a plan that has not been falsified. The plan must be audited _before_ code is written, because the cheapest defect to fix is one that was never coded against. The Plan Audit's job is **not to improve the plan** — its job is to **find what is wrong with the plan**. Improvement is a downstream remediation step the user (acting CTO) authorizes after reading the findings.

This is DISTINCT from the broader system audit at `intent-eval-lab/000-docs/026-PP-PLAN-iep-full-stack-thinker-canon-and-engineers-audit-2026-05-26.md` (that one audits the BUILT system). The Plan Audit is **Phase 0 of plan 026**: cheap-then-expensive ordering. Auditing the plan first prevents 026 from later finding "the codebase faithfully implements a defective plan" — a finding that wastes a panel.

### Panel composition (7 seats)

Plan-quality audit demands different seats than codebase audit. A codebase audit needs performance + refactoring eyes; a plan audit needs strategy, scope-discipline, eval-governance, and bitter-lesson skepticism eyes:

| Seat                                                                   | Why this seat for _plan_ audit                                                                                                                                                  | Primary axes                     |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Rich Hickey** (`~/.claude/agents/rich-hickey-reviewer.md`)           | Simple-vs-easy lens cuts plans that conflate "we'll just add a phase" with actual conceptual simplification                                                                     | GAPS, SCOPE INTEGRITY            |
| **Kent Beck** (`~/.claude/agents/kent-beck-reviewer.md`)               | Tidy First + small-step feedback. Audits whether each Phase has a real working-end-state or is a "big bang" disguised as incremental                                            | SCOPE INTEGRITY, RISK MITIGATION |
| **Andrej Karpathy** (`~/.claude/agents/andrej-karpathy-reviewer.md`)   | Bitter-lesson check. THE most important seat for an LLM-eval plan. Asks "Is this plan building scaffolding that the next frontier model release will eat?"                      | GAPS, SCOPE INTEGRITY            |
| **Chip Huyen** (`~/.claude/agents/chip-huyen-reviewer.md`)             | Eval-set governance is THE production-ML discipline this product depends on. Critical given the SkillsBench negative-baseline finding                                           | GAPS, RISK                       |
| **Leslie Lamport** (`~/.claude/agents/leslie-lamport-reviewer.md`)     | Formal-spec discipline. Asks "What invariants does the plan claim, and are they stated precisely enough to falsify?"                                                            | GAPS, RISK                       |
| **Ward Cunningham** (`~/.claude/agents/ward-cunningham-reviewer.md`)   | Technical-debt and AAR discipline. Audits whether the plan has feedback loops, AAR cadence, and whether deferred work is named-and-tracked                                      | GAPS, SCOPE INTEGRITY            |
| **Martin Kleppmann** (`~/.claude/agents/martin-kleppmann-reviewer.md`) | Plans that touch eval-set storage, lineage, and skill-refinement-record provenance are distributed-data plans whether they admit it or not. Audits durability, replay, ordering | RISK, RISK MITIGATION            |

Dropped from prior AAR-023 panel: Fowler (his lens is refactoring-of-code; less load-bearing pre-code), Gregg (no perf surface to audit yet). Considered but not seated: Armstrong, Pike, Torvalds.

### Four axes (every finding tagged exactly one)

| Axis                    | Definition                                                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **(a) GAPS**            | Topics the plan does not address but should, given its declared scope                                                                                   |
| **(b) RISK**            | Failure modes the plan does not name                                                                                                                    |
| **(c) RISK MITIGATION** | Risks the plan _does_ name but mitigates with hand-waving                                                                                               |
| **(d) SCOPE INTEGRITY** | Over-promise (asserts outcomes without mechanism), under-promise (omits required work), or hidden-dependency (Phase B silently requires un-named infra) |

### Severity rubric (5 levels)

| Level   | Name     | Definition                                                                                           | Action                                                   |
| ------- | -------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **P0**  | BLOCKER  | Plan cannot proceed to code without remediation; defect would cause work to fail or be unfalsifiable | Plan amendment required before any Phase begins          |
| **P1**  | CRITICAL | Plan can proceed but named risk is materially under-mitigated; high probability of mid-build rework  | Plan amendment required before the affected Phase begins |
| **P2**  | MAJOR    | Real gap or risk; plan should address but not blocking                                               | New bead filed; addressed in plan v5                     |
| **P3**  | MINOR    | Improvement opportunity; not a defect                                                                | Tracked in AAR backlog                                   |
| **NIT** | NIT      | Wording, clarity, citation                                                                           | Inline edit during synthesis                             |

### Methodology

**Phase 1 — Brief pack assembly** (acting CTO prepares). Lives at `intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/brief-pack/`:

1. `00-plan-under-audit.md` — this plan (snoopy-fluttering-comet v4)
2. `01-companion-plan-025.md` — IEP Skill Refiner companion plan
3. `02-broader-audit-plan-026.md` — full-stack audit plan
4. `03-DR-010.md` — decision record this plan implements
5. `04-blueprint-a.md`, `05-blueprint-b.md` — architecture blueprints
6. `06-canonical-glossary.md` — term definitions
7. `07-bd-snapshot.json` — `bd list --open --json` at audit start
8. `08-aar-023-findings.md` — prior panel findings (so seats can check whether this plan addresses them)
9. `09-skillsbench-baseline-report.md` — the negative-baseline finding the plan must reckon with
10. `10-agentskills-spec-snapshot.md` — agentskills.io v1.0.0 spec pinned at audit time

Each seat instructed: read the entire brief pack before writing findings. No seat may cite a doc not in the brief pack.

**Phase 2 — Parallel review.** Seven seats run in parallel (one Task invocation each, subagent_type matching the seat). Each seat writes to `<seat-name>-findings.md` in the audit directory. Seats do NOT see each other's findings during review — divergence is signal.

**Phase 3 — Synthesis.** Acting CTO reads all 7 findings files and produces `synthesis.md`:

- **Convergent findings** (≥3 seats raised same defect) — high confidence, near-automatic remediation
- **Divergent findings** (only 1-2 seats raised) — kept verbatim, flagged for user judgment
- **Cross-seat tensions** (seat A says X is required, seat B says X is over-engineering) — escalated to user for arbitration
- **Remediation map** — every P0/P1 finding mapped to (a) plan amendment, (b) new bead, or (c) update to existing bead

**Phase 4 — Ratification.** User reviews synthesis. If P0 findings or unresolved seat-tensions exist → convene ISEDC session (`/exec-decision-council`) for adversarial ratification, producing an AT-DECR record. If only P1/P2 → user ratifies directly via journal entry.

**Phase 5 — Remediation.** Plan amendments land in this doc; new beads are filed; the audit directory closed with a `STATUS.md` marking ratification date and pointing to the amended plan version.

### Output deliverable cluster

```text
intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/
├── README.md                        # entry point; names panel, links pack and findings
├── brief-pack/                      # the 10 docs above
├── findings/
│   ├── hickey-findings.md
│   ├── beck-findings.md
│   ├── karpathy-findings.md
│   ├── huyen-findings.md
│   ├── lamport-findings.md
│   ├── cunningham-findings.md
│   └── kleppmann-findings.md
├── synthesis.md
├── remediation-map.md               # finding-ID → plan-section / bead-ID
└── STATUS.md                        # OPEN | RATIFIED | CLOSED + dates
```

If ISEDC ratification fires:

```text
intent-eval-lab/000-docs/NNN-AT-DECR-isedc-session-N-plan-audit-ratification-2026-05-26.md
```

Per-seat findings file structure (uniform):

```markdown
# <Seat Name> — Plan Audit Findings — 2026-05-26

## Summary (3 bullets: top concerns)

## Findings

### F-<seat-initials>-001 [P0|P1|P2|P3|NIT] [GAPS|RISK|MITIGATION|SCOPE]

**Plan section cited:** §X.Y
**Defect:** ...
**Why this matters:** ...
**Proposed remediation:** ...

### F-<seat-initials>-002 ...

## Out-of-scope observations (things noticed but not panel's job)
```

This gives the synthesis step a clean grep target (`grep -h "^### F-" findings/*.md`).

### When it runs

**Trigger:** Immediately after this plan iteration is written. The Plan Audit fires before _any_ bead in Skill Refiner Phase A is claimed for implementation.

**Hard gate:** No `bd claim` against a Skill Refiner bead is permitted until `STATUS.md` reads `RATIFIED`.

### Recurrence

The Plan Audit re-fires when:

1. A new Phase is added to the plan
2. An existing Phase is removed or merged
3. A P0 finding from prior audit is marked "deferred" rather than remediated
4. Canonical glossary changes a load-bearing term (Refiner, Promotion, Eval Set)
5. A major DR (e.g., DR-011+) supersedes a DR the plan cites

Each re-audit is _incremental_ — the prior brief pack is the starting point; only changed sections trigger fresh seat review.

### Sample findings (illustrative, written as if from panel reviewing the current draft)

**F-CH-001 [P0] [GAPS] — Eval-set bootstrap has no fallback for low-volume skills**
Plan section: Phase A "Bootstrap eval set from production invocations"
Defect: Plan assumes each candidate-for-refinement skill has sufficient historical invocations to bootstrap a ≥N-example eval set. Marketplace contains skills with single-digit lifetime invocations. Plan defines no fallback (synthetic generation? human curation? skill-pair eval transfer?) and no minimum-volume gate for entry into the Refiner pipeline.
Why this matters: Without fallback, the Refiner becomes "tool only for popular skills" — exactly the inverse of where refinement adds most value (low-volume skills with unclear contracts).
Proposed remediation: Add Phase A.5 "Eval-set bootstrap policy" defining three tiers — high-volume (production bootstrap), medium-volume (production + synthetic augmentation), low-volume (human-curated seed set required before entry).

**F-AK-001 [P1] [SCOPE INTEGRITY] — Plan over-engineers prompt-refinement scaffolding the next model release may obviate**
Plan section: Phase B "Refinement engine with N-pass iterative prompt mutation"
Defect: Plan describes multi-pass mutation-and-eval loop resembling 2023-era prompt-engineering pipelines. Frontier models in 2026 increasingly handle ambiguous skill prompts robustly without elaborate refinement. Plan does not test null hypothesis: "does simply re-issuing the skill prompt to Opus 4.7 with the eval set as in-context examples outperform the multi-pass engine?"
Why this matters: Bitter lesson. If null hypothesis holds, Phase B is wasted engineering.
Proposed remediation: Insert Phase A.7 "Bitter-lesson baseline" — run eval set against un-refined skill with naive in-context augmentation. If lift > 70% of projected Phase B lift, descope Phase B's iterative engine.

**F-LL-001 [P0] [GAPS] — "Refined" is not formally defined**
Plan section: Throughout; especially §3 promotion criteria
Defect: Plan uses "refined" as a primitive term. No invariant defines what distinguishes a refined skill from a modified skill. No predicate states "skill S' is a valid refinement of S iff..." Promotion criteria reference "improvement" without a typed comparison.
Why this matters: Unfalsifiable. Two engineers will implement contradictory promotion logic and both will claim conformance.
Proposed remediation: Add canonical-glossary entry: _Refinement(S, S', E) holds iff S' passes ≥k% more eval cases in E than S, S' is semantically dominant (passes superset of E-cases S passes), and no eval case regresses below severity threshold T._ All Phase C/D code must cite this predicate.

**F-KB-001 [P1] [SCOPE INTEGRITY] — Phase timeboxes lack any bandwidth model**
Plan section: §4 phase budgets
Defect: Phase A is "~1 week", Phase B "~2 weeks". No FTE assumption, no critical-path identification, no acknowledgment that uprg + 9pi3 + 59tx beads gate Phase C entry. Reader cannot tell whether "1 week" assumes user works alone, parallel agent work is presumed, or what slippage tolerance is.
Why this matters: Schedule risk is invisible. First slip cascades silently.
Proposed remediation: Replace timeboxes with (a) explicit FTE-week budget per phase, (b) named critical-path beads, (c) explicit gate-bead callouts. Drop calendar weeks in favor of bead-throughput estimates.

**F-MK-001 [P1] [RISK MITIGATION] — SkillVersion lineage is asserted but durable storage details under-specified**
Plan section: Phase C SkillVersion entity definition
Defect: Plan names the entity but does not state (a) where it persists at runtime, (b) whether the prior skill version is retained byte-for-byte or by hash, (c) what happens to records when a refined skill is later rolled back. Without these the lineage claim is decorative.
Why this matters: Promotion → rollback → re-promotion cycles will corrupt audit trail. Product's primary trust artifact (audit trail) becomes weakest link.
Proposed remediation: Already partially specified via append-only event log (AC-2); make this explicit: "no record is ever mutated; rollback is a new SkillVersion record citing the prior."

**F-WC-001 [P2] [GAPS] — No AAR cadence is built into the plan**
Plan section: § 6 Operations
Defect: AAR-023 produced 9+ findings _because_ a panel was convened. The Skill Refiner plan defines no equivalent retrospective trigger — no "after first 5 promotions, convene AAR" or "monthly Refiner review". Institutional memory will leak.
Why this matters: Lesson of AAR-023 was adversarial review _finds things_. Not scheduling it means next finding arrives post-incident.
Proposed remediation: Add §X "AAR cadence" — first AAR after first 5 successful promotions OR first rollback (whichever first), then quarterly.

(Findings shown as samples to set the quality bar; actual audit will produce real findings tagged similarly.)

---

## 13. Execution Sequence — Plan → Beads → GH Issues → Validate → Audit → Code

Per user direction 2026-05-26: "Obviously the plan has to be then incorporated into epics and beads. So and those have to have annotations, note, dependencies, etc. And then once the beads are created with bead IDs, then you have to create the corresponding issues in the GitHub repo. And then you have to validate the consistency among all that. It's a bunch of work, but that's okay. We have time."

This is the **mandatory ordered choreography** that takes us from ratified plan to first line of code. No skipping. Each step has a checkpoint.

### Step 0 — Pre-execution research (resolve open items)

**Owner:** acting CTO (Claude)
**Output:** filled-in checklist in `intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/brief-pack/`

1. **Fetch SkillOpt paper** (arXiv 2605.23904) via WebFetch; cache locally at `intent-eval-lab/research/2605.23904-skillopt.pdf` (NEW directory); produce 1-page digest at `intent-eval-lab/000-docs/NNN-RR-LITS-skillopt-paper-digest-2026-05-26.md` confirming the plan's citations match the paper's actual claims
2. **Fetch agentskills.io spec snapshot** via WebFetch against `agentskills.io/specification`; cache at `intent-eval-lab/research/agentskills-spec-v1.0.0.md` AND refresh `~/000-projects/claude-code-plugins/000-docs/agentskills-spec-snapshot.md` if more than 90 days stale; pin the version in this plan's AC-11 and in the SkillVersion entity schema
3. **Fetch all 22 canonical Anthropic/Claude Code spec URLs** from § 2.5 inventory **with depth-1 recursive link-following** (depth-2 for plugins-reference, skills, hooks per § 2.5 "Recursive link-following discipline"). Refresh local snapshots at `~/000-projects/claude-code-plugins/000-docs/anthropic-skills-spec-snapshot.md` if stale. Cache the expanded URL tree (likely 40-80 URLs after recursive walk) at `intent-eval-lab/research/claude-docs-spec-tree-2026-05-26.md` with per-URL annotations (spec section + Refiner artifact bearing + snapshot timestamp). Record snapshot timestamps + URL count via `bd remember --key skill-refiner-spec-snapshots-2026-05-26 "..."` per § 3.5 PR-4
4. **Resolve § 7.1 (Phase B demo skill)**: review `/audit-tests` and `/validate-skillmd` invocation histories; CTO call documented in audit brief-pack
5. **Confirm § 7.2 (kernel version sequencing)**: verify `iec-E12` v0.2.0 work is on track per current bd state; CTO call documented
6. **`bd memories` sweep**: run `bd memories skill` and `bd memories refiner` and `bd memories spec`; surface any existing memories that bear on this plan; cite each in the brief pack

**Checkpoint:** all 6 items resolved or explicitly flagged "research-incomplete; proceeding with default assumptions documented in plan v4.1". `bd remember --key skill-refiner-pre-execution-research-<date> "..."` filed summarizing pre-execution state.

### Step 1 — File per-repo bead clusters (annotations + notes + dependencies)

**Owner:** acting CTO via bd CLI
**Output:** all 33 new beads filed per § 5.5 inventory

For EACH new bead:

- Plain-English title (per bead-naming rule in force 2026-05-22)
- Full description body including:

  - Plan section citation (e.g., "Per plan 025 § 4 Phase A …")
  - Architectural commitment refs (e.g., "Honors AC-2 append-only event log")
  - Dependencies on companion beads (via `--deps`)
  - Parent (via `--parent` for tasks under product epics)
  - Labels: `refiner`, `repo:<short>`, plus 1-2 topic words
  - **Trailing tri-link block (MANDATORY per AC-12)**:

    ```text
    Doc: <repo>/000-docs/<filename>
    GitHub: <will-be-added-in-Step-2>
    ```

Sequence: file in dependency order so `--deps` resolve cleanly. Roughly: RC-IEL → RC-IEC → RC-IAJ → RC-IAH → RC-IAR → leaf tasks → TL-EPIC → TL-\* → DIAG-D1..D9.

After every 10 beads: run `bd backup sync` to push to `file:///home/jeremy/000-projects/beads-backups/` per § 3.5 PR-1.

**Checkpoint:** `bd list --label refiner --status open` returns ≥ 60 beads (33 new + 27 pre-existing).

### Step 2 — Create corresponding GitHub issues (cite bead IDs in body)

**Owner:** acting CTO via `gh issue create`
**Output:** GH issues in each IEP repo, with bead IDs in body

For each bead that has a code-anchored unit of work (i.e., not just an epic umbrella):

- Create GH issue in the appropriate repo per § 5.5 cluster mapping
- Title: same as bead title (plain English)
- Body: includes:

  - `**Beads:**` line listing all related bead IDs
  - Brief restatement of scope
  - Acceptance criteria (from bead description)
  - **Trailing tri-link block (MANDATORY per AC-12)**:

    ```text
    Bead: bd_000-projects-<id>
    Doc: <repo>/000-docs/<filename>
    ```

- Label: `refiner` (per § 3.5 PR-1)
- Use `bd-sync link <bead> --gh OWNER/REPO#N` to plant the cross-ref in the bead and announce linkage

GH issue clustering per bead-naming rules: ONE GH issue per logical cluster, not one per task. Per-repo coordination epics (RC-\*) get their own GH issue per repo, with all per-repo leaf tasks linked in the body. Product epics (3zol/jsy3/0r8m) get their own GH issue per repo touched (umbrella-level tracking).

Estimated GH issue count: ~20 (1 RC-_issue per repo × 5 + 3 product epic umbrella issues per repo × ~3 typical touch + 1 TL-EPIC issue + DIAG-D_ clustered into 1 issue per repo).

**Checkpoint:** `gh search issues "label:refiner is:open" --owner jeremylongshore` returns ≥ 20 issues. Each cited in a bead's `GitHub:` field.

### Step 3 — Run `/validate-consistency` + `validate-trilink.sh`

**Owner:** acting CTO
**Output:** two validation reports

1. `/validate-consistency` invoked at umbrella `~/000-projects/intent-eval-platform/` level. Output to `intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/validate-consistency-report.md`. Expected: 0 BLOCKERs.
2. `intent-eval-platform/intent-eval-lab/scripts/validate-trilink.sh` invoked. Output to `intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/validate-trilink-report.md`. Expected: exit code 0 (zero violations).

If either reports BLOCKERs / violations: stop, fix at the source (doc, bead, or GH issue), re-run, until both clean.

**Checkpoint:** both reports pass.

### Step 4 — Convene § 12 Plan Audit

**Owner:** acting CTO orchestrates; 7 panel seats execute in parallel via Task tool
**Output:** the full audit deliverable cluster at `intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/`

Per § 12 methodology. Brief pack already assembled in Step 0. Run 7 seats in parallel; synthesize; ratify.

**Checkpoint:** `STATUS.md` reads `RATIFIED`. ≤ 0 BLOCKERs; ≤ 3 MAJORs.

### Step 5 — Apply remediation deltas (if any)

**Owner:** acting CTO
**Output:** plan v5 (with revision history entry), updated beads, new beads filed if needed

For each P0/P1 finding:

- If amendment: edit this plan doc in place; update revision-history in front-matter
- If new bead: file via bd; ensure tri-linkage discipline; reference finding-ID in description
- If existing-bead update: `bd update <id> --append-notes "remediation per F-XX-NNN: ..."`

Re-run Step 3 (validation) after remediations land.

**Checkpoint:** `STATUS.md` updated to `RATIFIED-WITH-DELTAS` (or stays `RATIFIED` if no deltas needed).

### Step 6 — Ratification banner in plan + bd memory + per-repo CLAUDE.md seed

**Owner:** acting CTO
**Output:** banner at top of this plan doc + bd memory + 5 per-repo CLAUDE.md seed sections (per § 3.5 PR-5)

6a. Add a line to plan front-matter:

> **Plan Audit Status:** RATIFIED 2026-MM-DD per `intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/STATUS.md`. Cleared for execution.

6b. File ratification memory:

```bash
bd remember --key skill-refiner-plan-ratified-2026-05-26 \
  "Plan snoopy-fluttering-comet v4 ratified per Plan Audit. ≤0 BLOCKERs, ≤3 MAJORs. Audit deliverable cluster at intent-eval-lab/000-docs/audit/2026-05-26-plan-audit/. ISEDC DR at NNN-AT-DECR-isedc-session-N-plan-audit-ratification. Execution begins Step 7."
```

6c. Seed Skill Refiner section in each of 5 IEP repo CLAUDE.md files + umbrella CLAUDE.md per § 3.5 PR-5 touch-points table. Each seed section cites:

- Plan doc paths (snoopy-fluttering-comet.md + companion 025 + audit-plan 026)
- Relevant bead IDs for that repo (RC-_cluster + leaf tasks + TL-_ backfill)
- Relevant doc paths in that repo's `000-docs/` (existing + planned)
- AAR seed: "Phase X status: not-yet-started"

This is the visible signal that gates Step 7. After Step 6, every IEP repo's CLAUDE.md primes a future session correctly without re-reading the entire plan.

### Step 7 — First `bd claim` (code begins; v5 MACHINE-ENFORCED)

**Owner:** acting CTO or designated engineer
**Output:** first commit on a Skill Refiner feature branch
**Enforcement (v5 per DR-028 P0-RATIFY-4):** Hard gate is MACHINE-ENFORCED by `intent-eval-lab/scripts/bd-claim-precheck.sh`. The script reads `000-docs/audit/2026-05-26-plan-audit/STATUS.md`, refuses `bd claim` against any refiner-labeled bead when STATUS = OPEN, partially permits under RATIFIED-WITH-DELTAS using the DR-028-authorized-shorthand whitelist (6 shorthands: SkillVersion-entity-schema-with-version_kind, RefinerStrategy-interface, Phase-A.0-null-hypothesis-baseline, bd-sync-cross-ref-generator, bd-claim-precheck.sh-script, sigstore-Rekor-outbox-reconciler), and fully permits under RATIFIED. Per VP DevRel binding: external-contributor PRs see the gate as a CI WARNING + contributor-acknowledgment, NOT a hard block.

**v5 first-claim order (post-DR-028, gated):**

1. The Phase A.0 null-hypothesis baseline bead (filed via DR-028 directive #5) — this is the FIRST claim because it GATES Phase A per DR-028 P0-RATIFY-3 (if naive beats Refiner, Phase B descopes)
2. After Phase A.0 result lands: IAJ-N1 (Scaffold @j-rig/refiner-core) OR descope per Phase A.0 decision rule

Run `bd update <id> --claim` (with the wrapper that calls bd-claim-precheck.sh first). Begin code.

**Checkpoint:** first commit pushed to feature branch with full commit message referencing bead ID + plan section + DR-028 authorization note.

### Step 8 — Per-phase exit verification (recurring) + bd memory + CLAUDE.md update

**Owner:** acting CTO at each phase exit
**Output:** updated `STATUS.md` per phase + bd memory per phase + per-repo CLAUDE.md updates

For each phase exit per § 9:

- Run `/validate-consistency` (full sweep) — per § 3.5 PR-2
- Run `validate-trilink.sh` (full sweep) — per § 3.5 PR-1
- Run audit-harness verification
- Phase A: verify `npm view @j-rig/refiner-core@0.1.0` + `npm view @j-rig/refiner@0.1.0`
- Phase B: verify plugin installable from marketplace
- Phase C: verify `npm view @intentsolutions/core@0.3.0`
- All phases: file AAR doc at `intent-eval-lab/000-docs/NNN-AA-AACR-skill-refiner-phase-<X>-<date>.md`
- **bd memory per phase (per § 3.5 PR-4):**

  ```bash
  bd remember --key skill-refiner-phase-<X>-shipped-<date> \
    "Phase X exit criteria met per § 9 verification #N. AAR at intent-eval-lab/000-docs/NNN-AA-AACR-skill-refiner-phase-X-<date>.md. Compute cost actual: $X; budget was $Y. Lessons: <key non-obvious operational finding>."
  ```

- **Per-repo CLAUDE.md update per phase (per § 3.5 PR-5):**
  - Update `### Phase X status: not-yet-started` → `### Phase X status: SHIPPED <date>` with AAR reference
  - Add any new doc paths created in this repo during the phase
  - Add any new CLI commands or APIs that landed
  - Verify `/validate-consistency` still passes after CLAUDE.md update

**Checkpoint:** AAR filed per phase; § 9 verification criteria met; bd memory filed; all 5 per-repo CLAUDE.md files (+ umbrella) updated.

### Step 9 — Long-term recurrence (Phase F trigger watch + spec snapshot refresh + memory hygiene)

**Owner:** acting CTO (quarterly)
**Output:** monitoring + AAR per § 9 Phase F triggers; spec snapshot refreshes; bd memory hygiene

Quarterly review of:

- Number of partners consuming refined skills
- Number of active SkillVersion records
- Drift / rollback incidents
- **Spec snapshot freshness** (per § 2.5 canonical URL inventory): re-fetch the 22 live URLs; diff against local snapshots in `~/000-projects/claude-code-plugins/000-docs/*-snapshot.md`; if drift, refresh snapshots + file `bd remember --key skill-refiner-spec-snapshot-refresh-<date> "..."` + bump SkillVersion records' `skill_md_spec_version` field accordingly
- **bd memory hygiene**: `bd memories` enumeration; close obsolete memories with `bd forget`; cross-link new memories to relevant beads
- **Per-repo CLAUDE.md staleness check**: run `/validate-consistency` against each of 5 IEP repos; any drift between CLAUDE.md and repo state is a P2 finding to remediate

When Phase F triggers fire, re-enter plan mode for Phase F design.

---

## Prior art (cited for reproducibility, not borrowed for branding)

Public work on text-space agent-skill optimization (arXiv 2605.23904 SkillOpt, 2026-05-22), 3-layer in-session hook architectures (Anthropic published a reference implementation around mid-2026 as `security-guidance`), and skill benchmark measurement (arXiv 2602.12670 SkillsBench, 40-author multi-org study). The Agent Skills Open Standard at `agentskills.io/specification` and the Anthropic `skills/spec/agent-skills-spec.md` in `github.com/anthropics/skills` define the SKILL.md format the Refiner edits.

Skill Refiner is IS-native. Cited work informed the design space and provides reproducibility anchors; the architectural framing, sub-product naming, and positioning are forward-deployed from first principles within the Intent Solutions agent-rig stack per DR-010 § 13.6 (external-pattern non-borrow).

---

— end plan —

— Jeremy Longshore
intentsolutions.io
