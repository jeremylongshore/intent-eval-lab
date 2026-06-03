---
date: 2026-05-28
status: NEEDS-AMENDMENT — incremental Plan Audit 2026-05-28 returned 12 P0 + 17 P1 across 7 seats with 3 convergent themes. See `000-docs/audit/2026-05-28-sak-incremental-audit/synthesis.md` + STATUS.md. Plan 031 v7 amendment must fold C1/C2/C3 remediations BEFORE ISEDC Class-1 charter (DR-032 draft) convenes. Hard gate: SAK-labeled beads (sak + iec-E11*) NOT claimable under NEEDS-AMENDMENT per `audit/2026-05-28-sak-incremental-audit/STATUS.md`. Refiner-labeled beads remain claimable under DR-028 RATIFIED.
supersedes_relationship: AMENDS plan 027 v5 (does NOT supersede). Plan 027 v5 body remains canonical for §§ 1-13; this doc adds § 14 SAK and is the v6 amendment.
author: Jeremy Longshore (executor: Claude as drafting CTO; CTO-mode delegation 2026-05-28)
---

# Skill Refiner Plan v6 Amendment — Spec Authority Kernel (SAK)

## Tri-link block (per § 3.5 PR-1)

```text
Beads: bd_000-projects-<iec-E11 TBA>, bd_000-projects-<ccp-d4-followup TBA>, bd_000-projects-<isedc-charter TBA>, bd_000-projects-<6767h-kernel-map TBA>
GitHub: jeremylongshore/intent-eval-lab#<TBA>
```

> **Read order:** Plan 027 v5 (the ratified body) → this doc (the v6 amendment) → DR-028 (the original ratifying decision) → 029-DR-BAND (bandwidth) → 030-AT-DECR (eval-set bootstrap) → THIS file → DR-032 (pending ISEDC Class-1 charter)

## Revision history

- **2026-05-26 v1** — original SkillOpt-Pattern draft (plan 025)
- **2026-05-26 v2** — j-rig Keeper / Pre-Trip / Evidence sub-product framing (superseded)
- **2026-05-26 v3** — Skill Refiner peer-product collapse
- **2026-05-26 v4** — ecosystem-integration rigor, SkillMD spec pinning, per-repo bead structure, ASCII diagram catalog, tri-linkage discipline, plan-audit phase, execution sequence
- **2026-05-27 v4.1** — 4-reviewer internal pre-flight pass; 6 P0 BLOCKERs folded
- **2026-05-27 v5 (inline in 027)** — DR-028 amendments folded; STATUS → RATIFIED-WITH-DELTAS → RATIFIED
- **2026-05-28 v6 (THIS DOC)** — fold-in of § 14 Spec Authority Kernel (SAK) — kernel `schemas/authoring/v1/` architecture, IS-marketplace-tier discipline binding, 6 authoring contracts, 6-phase migration sequencing, ISEDC Class-1 charter ratification gate

## Status

**State:** PROPOSED. The Skill Refiner plan body (§§ 1-13 of plan 027 v5) is RATIFIED per DR-028. § 14 SAK is **NEW work** that:

1. Adds a parallel `intent-eval-core/schemas/authoring/v1/` family alongside the existing `schemas/v1/` runtime contracts (bicameral kernel architecture)
2. Encodes 6 authoring contracts (skill-frontmatter, plugin-manifest, agent-definition, mcp-config, hook-config, marketplace-catalog) at the **IS enterprise marketplace tier** per § 14.10 binding
3. Requires ISEDC Class-1 charter ratification before kernel v0.4.0 ships
4. Triggers § 12 recurrence rule #1 ("a new Phase is added to the plan") → Plan Audit re-fires INCREMENTALLY on § 14 content
5. Gates the 3,044-file CCP SKILL.md corpus migration through Skill Refiner Phase B

**Hard gate state (per bd-claim-precheck.sh logic):** Skill Refiner beads remain CLAIMABLE under existing STATUS=RATIFIED (this amendment is additive). SAK-specific beads (iec-E11\* prefix) require their own claim-gate check that waits for the ISEDC Class-1 charter DR to land — see § 14.8 directive 4 + § 7.2 below.

## Relationship to ratified plan 027 v5

This doc is **purely additive**. No clause in §§ 1-13 of 027 v5 is modified, superseded, or contradicted. § 14 SAK extends the plan by:

- Adding 14.10 (Enterprise-standard discipline) as a BINDING constraint that reinforces (does not replace) AC-11 + § 2.5
- Adding `iec-E11` epic + child beads as new bead cluster (no existing bead is changed)
- Adding 6 new authoring contracts to kernel scope — these are NEW schemas, not modifications of the 14 existing runtime contracts
- Adding the 6767-h master spec as an explicit upstream citation source for kernel authoring schemas

§ 14 does NOT change Phase A/B/C/D/E/F sequencing; it adds SAK Phase 0-5 as a parallel track that **interlocks** with Refiner Phase B (corpus migration). § 14.9 documents the interlock points explicitly.

## What's in this doc

This file embeds the complete § 14 content as proposed for the v6 amendment. The substance is reproduced verbatim from the user-presented v6 prompt 2026-05-28 to preserve fidelity. Cross-references to plan 027 sections (e.g., "§ 4 Phase B", "AC-11") refer to plan 027 v5 sections, not sections within this file.

---

## 14. Spec Authority Kernel (SAK) — schema-authority extension (NEW 2026-05-28)

**Status:** PROPOSED — pending ISEDC Class-1 charter ratification + user ExitPlanMode signoff.
**Codename:** Spec Authority Kernel (SAK). Tracking prefix: `iec-E11`.
**Relationship to the Skill Refiner:** the Refiner is the eval-gated _mechanism_ that fixes individual SKILL.md files; SAK is the _authority play_ that makes "fix" well-defined. SAK enables Skill Refiner Phase B to operate at the 3,044-file scale without ambiguity about what counts as a valid SKILL.md.

### 14.1 Context — why this section exists

Per user direction 2026-05-28 ("intent eval lab, jrig, all of this will be the source of truth for the schemas, the scaffolding, the context, all the rules, regulations regarded to building these items"). Three parallel Explore agents 2026-05-28 audited the surface area and produced the following ground truth:

| Layer                                 | Today                                                                                                                               | Gap                                                     |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| CCP scripts/                          | 9 (8 validator-class)                                                                                                               | each validator owns partial spec knowledge              |
| CCP 000-docs/ spec docs               | 8 — including `6767-h-SPEC-DR-STND-claude-code-extensions-master.md` (the CURRENT MASTER, landed 2026-05-28, supersedes 6767-a/b/c) | prose only; no machine-checkable counterpart            |
| CCP plugins/                          | 449 dirs × 19 categories = **3,044 SKILL.md files**                                                                                 | varied frontmatter shape; no kernel-canonical gate      |
| CCP CI workflows                      | 21 (`validate-plugins.yml` is the required check)                                                                                   | runs CCP-side validator only; no kernel pin             |
| Global `~/.claude/skills/`            | 53 SKILL.md + 238 spec/reference files in 38 `references/` subdirs                                                                  | each skill carries private spec snapshots; drift hazard |
| Per-project `.claude/skills/`         | ~30+ scattered                                                                                                                      | unchecked entirely                                      |
| Kernel `intent-eval-core/schemas/v1/` | 14 RUNTIME-time schemas already canonical                                                                                           | **NO authoring-time schemas** — the gap SAK closes      |

**Existing patterns to extend (not re-invent):** DR-018 § 6.4 Option α-minus (kernel canonical + lab redirect-stubs, ratified 2026-05-21) + `intent-eval-lab/.github/workflows/schema-drift.yml` (enforces `x-redirect` on lab Evidence Bundle stubs) + `spec-drift-watch.yml` (shipped 2026-05-28, PR #77 commit 62e0443; daily-cron polling 6 upstream sources).

### 14.2 Architecture — the kernel becomes bicameral

Today `intent-eval-core/schemas/v1/` ships 14 runtime contracts. After SAK lands, the kernel ALSO ships a parallel authoring family:

```text
intent-eval-core/schemas/v1/                  # unchanged — runtime
intent-eval-core/schemas/authoring/v1/        # NEW — authoring contracts
  index.json
  _common.schema.json                          # branded-primitive $defs (shared)
  skill-frontmatter.schema.json                # SKILL.md YAML head
  plugin-manifest.schema.json                  # plugin.json
  agent-definition.schema.json                 # agents/*.md frontmatter
  mcp-config.schema.json                       # .mcp.json + plugin.json mcpServers
  hook-config.schema.json                      # hooks.json (30-event allowlist)
  marketplace-catalog.schema.json              # marketplace.json
  _vendor/anthropic/                           # snapshotted upstream specs (read-only)
    claude-code-2.1.X-hooks-events.json
    plugins-reference-YYYY-MM-DD.md
    sub-agents-YYYY-MM-DD.md
    agentskills-io-spec-YYYY-MM-DD.md
```

**Why kernel, not lab.** DR-018 § 6.4 already ratified the pattern: kernel canonical, lab redirect-stubs. Authoring contracts have at least as many consumers (16 validators today, 6 creators, the 3,044 SKILL.md corpus, plus every CCP CI workflow) as runtime contracts. Putting them in the lab would invert the dependency.

**Relationship to 6767-h.** 6767-h is the _prose_ master spec (the human-readable authority for Claude Code extensions). The authoring schemas are its _machine-readable shadow_ — each schema's `$comment` cites the 6767-h section it implements. Drift between them is detected by `schema-drift.yml` (extended) plus a new `prose-schema-coherence.yml`. 6767-h does not move under SAK; it remains the canonical CCP master spec that the kernel ratifies.

**Relationship to `~/.claude/skills/*/references/`.** These 238 files become _consumer-side caches_ of the kernel's `_vendor/anthropic/` snapshots. Validator skills get a thin `references/_kernel-snapshot.json` whose content is byte-identical to the kernel's vendored copy. A new `harness-hash-verify.yml`-style workflow asserts that hash equality. Kills the 238-file drift problem at the root.

**How CCP validators consume.** Each validator (`validate-skills-schema.py`, etc.) takes a `--kernel-version` flag and pulls schema from a **vendored copy at `claude-code-plugins/.kernel-vendor/authoring/v1/`** (CTO call per § 14.6 Q3 — matches `audit-harness` vendor pattern; avoids Python-side npm-install pain). CCP CI pins kernel via single `KERNEL_VERSION=` env var; bumping is a one-line PR.

### 14.3 Consumer matrix (steady state)

| Consumer                                                                                           | Today                    | After SAK                                                                            |
| -------------------------------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------ |
| 16 validators (8 CCP + 8 global)                                                                   | each owns its own checks | each delegates schema validation to kernel-loaded JSON Schema; keeps semantic checks |
| 6 creators (skill-creator, agent-creator, repo-blueprint, repo-dress, mcp-builder, plugin-creator) | hand-rolled output       | template fills against kernel schema; output is schema-valid by construction         |
| 3,044 CCP SKILL.md                                                                                 | varied frontmatter       | migrated by Skill Refiner Phase B; gated by kernel schema in `validate-plugins.yml`  |
| 53 global skills                                                                                   | drift-prone              | gated by same kernel schema via thin git-remote pre-commit (CTO call per § 14.6 Q5)  |
| Per-project skills                                                                                 | unchecked                | optional opt-in via `.claude/skills/.kernel-pin`                                     |

### 14.4 Migration sequencing — 6 phases, each shippable

#### Phase 0 — D4 wedge + ISEDC convening (week 1)

- Deliverable: D4 validator patch (`disallowed-tools` add, SCHEMA 3.7.0) in `validate-skills-schema.py`. ISEDC Class-1 session convened to ratify kernel v0.4.0 entity expansion via single charter covering all 6 authoring contracts (CTO call per § 14.6 Q1).
- Exit: D4 merged to CCP main; ISEDC decision record landed as `AT-DECR-spec-authority-kernel-charter`.
- D4 sequencing: ships **BEFORE** ISEDC convening (CTO call per § 14.6 Q2 — single-validator local fix, doesn't touch kernel, un-blocks Skill Refiner Phase A.0's judge).
- Beads: `iec-E11a` (kernel v0.4.0 charter), `ccp-d4-followup`.
- Intersection: Skill Refiner Phase A.0 calibration set must include `disallowed-tools` cases; otherwise eval-loop ground truth lags validator.

#### Phase 1 — Kernel authoring/v1 ships read-only (weeks 2–4)

- Deliverable: `intent-eval-core/schemas/authoring/v1/` with all 6 schemas + `_vendor/anthropic/` snapshots + `index.json`. No consumers cut over yet.
- Exit: kernel v0.4.0 published to npm; `schema-drift.yml` extended to enforce `_vendor/` hash freshness against upstream URLs polled by `spec-drift-watch.yml`.
- Beads: `iec-E11b` through `iec-E11g` (one per schema).
- Intersection: intent-eval-core v0.3.0 (SkillVersion entity, currently in flight per DR-028 P0-RATIFY-1) must already be cut so v0.4.0 is a clean minor. If v0.3.0 still in flight, Phase 1 waits.

#### Phase 2 — Validator cutover (weeks 5–7)

- Deliverable: all 8 global validators + 2 heavy CCP validators (`validate-skills-schema.py`, `validate-plugin`) load schema from kernel; semantic checks remain skill-side.
- Exit: every validator's `references/` directory contains ONLY a `_kernel-snapshot.json` (hash-pinned) + skill-specific rubric files. Drift impossible by construction.
- Beads: one per validator (10 total).
- Intersection: prerequisite for Skill Refiner Phase B's eval loop to have a stable judge — otherwise the loop chases a moving target.

#### Phase 3 — Creator cutover (weeks 8–9)

- Deliverable: 6 creators emit kernel-schema-valid output by construction.
- Exit: creator self-tests assert generated output passes corresponding validator without remediation.
- Beads: one per creator.

#### Phase 4 — Corpus migration via Skill Refiner Phase B (weeks 10–16)

- Deliverable: 3,044 CCP SKILL.md + 53 global + per-project SKILL.md migrated to kernel-schema-valid frontmatter via `batch-remediate.py` (deterministic wave A, ~80%) + Skill Refiner's eval-guided edit loop (ambiguous wave B, ~20%).
- Exit: `validate-plugins.yml` flips from advisory to **blocking** on kernel schema. Flip is **quorum-pinned at 99.5% with 30-day calendar ceiling** (CTO call per § 14.6 Q4).
- Beads: rolled up under existing Skill Refiner Phase B epic + new `iec-E11h` umbrella for cross-repo coordination.
- Intersection: this is _the_ mechanism the whole initiative enables.

#### Phase 5 — Hook + MCP + agent + marketplace gating (weeks 17–18)

- Deliverable: `validate-plugins.yml` adds blocking gates for the 5 remaining authoring contracts (plugin.json, agent, MCP, hooks, marketplace.json).
- Exit: every PR to CCP touching a plugin passes all 6 kernel-schema gates.
- Beads: one per gate.

### 14.5 CI gate strategy

| Gate                               | Where               | What it enforces                                                                                                                                                                                                                                                                                       |
| ---------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `schema-drift.yml` (EXTEND)        | intent-eval-lab     | Today: `x-redirect` on lab Evidence Bundle stubs. ADD: every file under kernel `schemas/authoring/v1/_vendor/anthropic/` carries `x-upstream-url` + `x-upstream-fetched-at` + `x-upstream-sha256`; workflow computes current upstream sha and fails red if differs (auto-opens `[stale-vendor]` issue) |
| `prose-schema-coherence.yml` (NEW) | claude-code-plugins | Nightly. Parses 6767-h section headings; asserts every `$comment` in authoring schemas cites a currently-existing 6767-h section. Catches 6767-h renumbering without schema update                                                                                                                     |
| `kernel-vendor-hash.yml` (NEW)     | claude-code-plugins | Mirrors `harness-hash-verify.yml` pattern. Asserts `.kernel-vendor/authoring/v1/*.schema.json` equals kernel npm package's shipped file for pinned `KERNEL_VERSION`. Same green/red discipline                                                                                                         |
| `validate-plugins.yml` (MODIFY)    | claude-code-plugins | Phase-gated. Phases 1-3: kernel schema runs in **advisory** mode. Phase 4: flips to **blocking** for SKILL.md. Phase 5: flips to blocking for the other 5 contracts                                                                                                                                    |
| `spec-drift-watch.yml` (UNCHANGED) | intent-eval-lab     | Already shipped 2026-05-28. Continues to anchor the snapshot timestamp                                                                                                                                                                                                                                 |

### 14.6 CTO calls made (5 — overrideable at execution)

Per CTO-mode delegation (no full ISEDC session needed for tactical calls; Plan agent recommendations adopted):

1. **ISEDC charter scope**: ONE charter, six schedule slots. Rationale: matches DR-028 ISEDC Session 7 pattern (one DR covered 10 decisions). Avoids 6× council convening cost.
2. **D4 sequencing**: D4 ships BEFORE ISEDC convening. Rationale: single-validator local fix, doesn't touch kernel; un-blocks Skill Refiner Phase A.0 judge credibility.
3. **CCP kernel consumption**: VENDORED at `.kernel-vendor/authoring/v1/` (NOT npm dependency). Rationale: matches already-mastered `audit-harness` vendor pattern; no Python-side npm-install pain.
4. **Phase 4 advisory→blocking gate flip**: QUORUM-PINNED at 99.5% of CCP SKILL.md passing advisory, with 30-day calendar ceiling. Rationale: highest-risk single moment in initiative; quorum prevents premature flip while ceiling prevents indefinite stall.
5. **Global skills repo posture**: BLOCKING via thin git remote. Rationale: 53 global skills are the soft underbelly that would re-introduce drift if left advisory. Thin git remote pattern (lightweight repo just for the pre-commit hook) prevents that.

### 14.7 Risks + mitigations

| Risk                                                                                                                                                                                                       | Mitigation                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **A. Kernel authoring schema disagrees with 6767-h at edge cases.** 6767-h is prose, schemas are machine-strict. First time a schema rejects a SKILL.md that 6767-h ostensibly permits, kernel gets blamed | Every schema entity carries `$comment` citing exact 6767-h section. `prose-schema-coherence.yml` enforces link. When prose ↔ schema disagree, canonical resolution is an ADR in CCP that amends 6767-h **and** bumps kernel schema in ONE PR. Never let them drift unilaterally                                    |
| **B. 3,044-file migration stalls in Phase 4.** Skill Refiner Phase B's eval-guided loop has unknown per-file latency; 24-hour budget at scale could mean weeks                                             | `batch-remediate.py` runs deterministic migrations first (≈80% of corpus is mechanical frontmatter normalization); eval loop handles only ambiguous tail (~20%). Phase 4 ships in two waves — wave A (deterministic) gates first, wave B (eval-loop) gates second. Stalled wave B doesn't block rest of initiative |
| **C. Consumer repos pin different kernel versions, fragmenting the contract.** CCP pins v0.4.0, global skills pin v0.4.1, per-project pins v0.5.0 → "kernel-valid" loses meaning                           | Generalize `sync-testing-harness` pattern → new `/sync-kernel-pin` skill that detects kernel-version drift across all `~/000-projects/` repos and offers to bump. Only major versions allowed to be breaking; minor/patch must be additive. Enforced by kernel-side `kernel-semver-guard.yml`                      |

### 14.8 Implementation directives (Phase 0, ordered)

| #   | Action                                                                                                                                                                                                                | Owner      | Bead                                                                                           |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------- |
| 1   | D4 validator patch — add `disallowed-tools` to `SKILL_FIELDS` registry + parse rule in `validate-skills-schema.py`; bump SCHEMA 3.6.0 → 3.7.0; re-pin local snapshots at `claude-code-plugins/000-docs/*-snapshot.md` | acting CTO | `ccp-d4-followup` (NEW, P0, repo:ccp)                                                          |
| 2   | Update Skill Refiner Phase A.0 eval-set bootstrap to include `disallowed-tools` specimens (per DR-030 § 5 specimen sources)                                                                                           | acting CTO | rolled into existing `D28-PHASE-A0` precondition + extends to `D30-EVALSET-SPECIMENS` if filed |
| 3   | File SAK epic `iec-E11` (Spec Authority Kernel) with 6 child schema beads `iec-E11a..g` + corpus-migration umbrella `iec-E11h`                                                                                        | acting CTO | `iec-E11` (NEW, P0, repo:iec)                                                                  |
| 4   | Convene ISEDC Class-1 session — single charter for kernel v0.4.0 authoring/v1 entity expansion covering all 6 contracts. File DR as `AT-DECR-spec-authority-kernel-charter`                                           | acting CTO | `iec-E11-isedc-charter` (NEW, P0, repo:iel)                                                    |
| 5   | Author 6767-h ↔ kernel-authoring/v1 mapping doc in CCP `000-docs/` (which 6767-h section maps to which schema; bidirectional citation table)                                                                          | acting CTO | `ccp-6767h-kernel-map` (NEW, P1, repo:ccp)                                                     |

Phases 1-5 unblock after charter ratifies + Phase 0 ships. Bandwidth budget per phase to be modeled in a follow-on DR-BAND doc.

### 14.9 How SAK and the Skill Refiner interlock

| Skill Refiner side                                              | SAK side                                                                                                                                  |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Phase A.0 baseline (judge: `/validate-skillmd`)                 | Needs D4 patch to make judge credible → SAK Phase 0 ships D4                                                                              |
| Phase A library (`@j-rig/refiner-core`)                         | Refiner's `accept()` predicate evaluates "is the post-edit SKILL.md kernel-schema-valid" — depends on SAK Phase 1 schema availability     |
| Phase B plugin (3-layer hooks)                                  | L1 Sinker (`validate-skillmd` Tier 2) cuts over to kernel schema in SAK Phase 2                                                           |
| Phase C kernel integration (SkillVersion entity, predicate URI) | SkillVersion records pin `skill_md_spec_version` — that field now points at kernel authoring/v1 version, not agentskills.io snapshot date |
| Phase F MLOps scale-up                                          | The 3,044-file corpus migration IS Phase F's first concrete batch — driven by Refiner mechanism, gated by SAK schema                      |

**The two initiatives are mutually accelerating.** Refiner without SAK = ambiguous "is this SKILL.md valid" target. SAK without Refiner = canonical schemas but no mechanism to migrate the 3,044-file corpus to comply. Together: precise target + mechanism to hit it.

### 14.10 Enterprise-standard discipline — BINDING (NEW per user direction 2026-05-28)

**Rule:** kernel authoring schemas encode the FULL Intent Solutions enterprise standard at the marketplace tier, NOT a sanded-down Anthropic-floor or agentskills.io-floor union. Per `claude-code-plugins/000-docs/SCHEMA_CHANGELOG.md` § NON-NEGOTIABLES item 3: _"The IS rubric SITS ON TOP of Anthropic's spec. Don't try to 'realign' the IS rubric to Anthropic's spec floor."_ This rule is now BINDING on the SAK architecture.

**What this means concretely** (per the audit-finding ground truth from Agent 4, the 2026-05-26 IS validator inventory):

| Layer                                    | Required fields                                                                                                              | Where it lives in kernel `authoring/v1/skill-frontmatter.schema.json`                                              |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Standard tier** (Anthropic spec floor) | 2: `name`, `description`                                                                                                     | Base schema with these 2 as `required`                                                                             |
| **agentskills.io open standard**         | 2 req + 4 opt = 6 total (`license`, `compatibility`, `metadata`, `allowed-tools`)                                            | `$defs.openStandardCompliant` — composition over base                                                              |
| **IS marketplace tier (ENTERPRISE)**     | **8 required (ERROR each)**: `name`, `description`, `allowed-tools`, `version`, `author`, `license`, `compatibility`, `tags` | `$defs.isMarketplace` — strict superset; `version`/`author`/`tags` are IS-only extensions NOT in any upstream spec |
| **IS deep tier**                         | Marketplace + 100-point rubric (5 pillars + modifiers ±15)                                                                   | Codified as separate `authoring/v1/scoring-rubric.schema.json`                                                     |
| **IS thorough tier**                     | Deep + JRig 7-layer behavioral eval                                                                                          | Out-of-scope for schema; delegated to `j-rig-skill-binary-eval` per existing tier model                            |

**Kernel schema shape**: every authoring schema ships with explicit `$defs` for each tier so consumers opt into the strictness level they need. CCP validators target `isMarketplace` by default (matches `validate-plugins.yml` current behavior). External adopters can target `openStandardCompliant` for cross-vendor portability. The base 2-field standard exists only for completeness; **IS-owned consumers default to marketplace**.

**6767-h alignment**: 6767-h is the human-readable authority for the marketplace tier. The `schema.$comment` citations referenced in § 14.2 always cite the marketplace-tier section of 6767-h, not a lower tier. Same applies to plugin.json, agent, MCP, hooks, marketplace schemas — kernel encodes the IS enterprise position, not the upstream floor.

**Anti-realignment guard**: kernel-side CI gate `kernel-rubric-floor-guard.yml` (NEW) — asserts that every `authoring/v1/*.schema.json` `$defs.isMarketplace.required` array contains the canonical 8-field IS set (or its per-artifact equivalent). PRs that remove required fields without an explicit ISEDC Class-1 ADR fail red. Mirrors the existing CCP `SCHEMA_CHANGELOG.md` NON-NEGOTIABLES discipline.

**IS extras beyond the 8-field set** (per user direction 2026-05-28 "we do versioning there are some extras we do" + Agent 4 inventory of `validate-skills-schema.py` v6.0 / SCHEMA 3.6.0):

The kernel `authoring/v1/skill-frontmatter.schema.json` `$defs.isMarketplace` encodes these IS-only extensions ALONGSIDE the 8 required fields. They are NOT in any upstream spec — they are pure IS-enterprise additions, and they belong in the kernel-canonical position too:

| IS extra                                                                                                                     | Schema-version introduced                 | Purpose                                                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Visibility fields (4)**: `requires_env`, `requires_tools`, `fallback_for_env`, `fallback_for_tools`                        | 3.5.0 (2026-05-14)                        | Conditional visibility — skill appears only when env/tools available; declares fallback chain                         |
| **Self-declared config surface**: `required_environment_variables` (list of `{name, prompt, help?, required_for?}`)          | 3.6.0 (2026-05-14)                        | Skill enumerates its own env-var requirements; surfaces during install                                                |
| **`metadata.intent-solutions.config`**: `{key, description, default}` triples                                                | 3.6.0 (2026-05-14)                        | Skill-declared config surface for user-tunable behavior; replaces hand-rolled "you might want to edit X" instructions |
| **Progressive disclosure 3-tier catalog markers**: L0 metadata (~150B/skill) / L1 body / L2 references                       | 3.4.0 (2026-05-14)                        | Token-economy discipline — Claude loads only the tier it needs                                                        |
| **Semver-strict `version` field** (`^\d+\.\d+\.\d+`)                                                                         | 3.3.0                                     | Not just "version exists" — must be semver. Breaking change discipline enforced                                       |
| **Deprecation surface**: `DEPRECATED_FIELDS` set + migration-suggestion W on use (e.g., `compatible-with` → `compatibility`) | 3.3.0                                     | Migration runway during field rename; `batch-remediate.py` consumes the same registry                                 |
| **`author` must contain `@`** (W if absent)                                                                                  | 3.3.0                                     | Contact-resolvability; not just a string                                                                              |
| **`shell` enum** (`bash` \| `powershell`)                                                                                    | 3.3.x                                     | Cross-platform skill discipline                                                                                       |
| **`when_to_use` combined-with-`description` ≤ 1536 chars**                                                                   | (CC 2.1.X cap)                            | Description budget enforcement; consumer-side too                                                                     |
| **YAML shell-substitution security check** (`$(...)`, backticks, ungated `${VAR}` outside allow-list)                        | 3.3.x                                     | Supply-chain hardening; one of the highest-severity validator gates                                                   |
| **`metadata.*` namespacing**: arbitrary metadata permitted but namespace-prefixed by vendor                                  | (agentskills.io spec base + IS extension) | Multi-vendor metadata coexistence; `metadata.intent-solutions.*` is IS namespace                                      |

**Versioning discipline (the META-extras)**:

The kernel itself ships under semver, but `SCHEMA_VERSION` discipline from CCP is more nuanced and **must propagate to the kernel**:

| Discipline                                                                | Where it lives today (CCP)                         | Where it lives after SAK (kernel)                                                                                        |
| ------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `SCHEMA_VERSION` constant                                                 | `validate-skills-schema.py:84` (currently `3.6.0`) | `intent-eval-core/schemas/authoring/v1/index.json` `$schemaVersion` field + Zod constant export                          |
| `SCHEMA_CHANGELOG.md` with NON-NEGOTIABLES header                         | `claude-code-plugins/000-docs/SCHEMA_CHANGELOG.md` | DUAL-MAINTAINED — kernel ships its own `schemas/authoring/v1/CHANGELOG.md` + the CCP one cross-references via `$comment` |
| NON-NEGOTIABLES (7 items, established 2026-04-28 post-debacle)            | CCP changelog header                               | Promoted to kernel-canonical at `schemas/authoring/v1/NON-NEGOTIABLES.md`; CCP changelog cites kernel as source-of-truth |
| Tier alias drift (`TIER_ENTERPRISE = TIER_MARKETPLACE`)                   | Cosmetic-only in validator                         | Kernel uses single canonical `marketplace` tier name; CCP validator aliases preserved for backward-compat                |
| Bug fixes that bring validator into spec compliance can ship autonomously | NON-NEGOTIABLE § 6                                 | Same rule applies to kernel schema patches                                                                               |
| Architectural changes need explicit user approval BEFORE landing          | NON-NEGOTIABLE § 7                                 | Same rule — ISEDC Class-1 ratification gate                                                                              |
| Required-fields set changes need explicit user approval                   | NON-NEGOTIABLE § 1 (8-field set)                   | Same — kernel `$defs.isMarketplace.required` is locked under Class-1 ratification                                        |

**Schema version sequencing through migration**:

| Phase                            | CCP `SCHEMA_VERSION`                                       | Kernel `authoring/v1/$schemaVersion`                                                   |
| -------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Pre-SAK (today)                  | 3.6.0                                                      | n/a                                                                                    |
| Phase 0 (D4 wedge)               | 3.7.0 (adds `disallowed-tools` + IS extras above codified) | n/a (kernel authoring/v1 not yet shipped)                                              |
| Phase 1 (kernel ships read-only) | 3.7.0                                                      | 1.0.0 (mirrors CCP 3.7.0 content; kernel resets to v1.0.0 as initial public-canonical) |
| Phase 2 (validator cutover)      | 3.7.x → 3.8.0 (validator loads kernel schema)              | 1.0.0 → 1.0.x (patch fixes)                                                            |
| Phase 3+                         | 3.8.x                                                      | 1.0.x or 1.1.0 if additive                                                             |
| Future major changes             | 4.0.0                                                      | 2.0.0 (coupled bumps; major = required-field-set change = Class-1 ISEDC)               |

**Drift between CCP `SCHEMA_VERSION` and kernel `$schemaVersion` is monitored** by the new `kernel-vendor-hash.yml` gate (§ 14.5) — CCP validator's `SCHEMA_VERSION` constant must declare which kernel `$schemaVersion` it pinned to; mismatch fails red.

**Tier model for the other 5 authoring contracts:**

| Contract                                 | Standard floor                                   | IS marketplace required-superset                                                                                                           |
| ---------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `plugin-manifest` (plugin.json)          | Anthropic plugins-reference required fields only | + `version`, `description`, `author`, `license`, `repository`, `keywords`, `engines.claude-code`                                           |
| `agent-definition`                       | `name` + `description`                           | + `tools` (explicit allowlist), `model`, `permissionMode`, `color`                                                                         |
| `mcp-config`                             | MCP spec required transport fields               | + `description`, `version`, scopes pinned, no wildcard `*` tools without `disabled` reason                                                 |
| `hook-config`                            | event + handler                                  | + `description`, `matcher` regex explicit (no implicit `.*`), `enabled` boolean explicit                                                   |
| `marketplace-catalog` (marketplace.json) | Anthropic marketplace required                   | + `version`, `maintainer`, `categories` cross-validated against catalog enum, every plugin entry passes `plugin-manifest` marketplace tier |

**Why "full enterprise standard" matters beyond aesthetics**:

1. **Validator credibility**: a Skill Refiner whose judge runs the IS marketplace rubric and not the spec floor produces ScoreRecords that mean what we say they mean. Sanded-down judge = sanded-down signal.
2. **3,044-file corpus**: the existing CCP corpus was authored against the IS marketplace standard. Targeting any lower tier in the kernel means the corpus instantly looks "over-validated" and creates an incentive to relax future skills.
3. **Brand promise**: "@intentsolutions/core" carries the IS brand. The kernel encoding less than the IS standard would dilute that.
4. **Forward-deployed**: per DR-010 § 13.6 (external-pattern non-borrow), IS-native standards are the position; floors are reference points. SAK ships the position.

**Implementation directive added to § 14.8 Phase 0**: the D4 patch (`disallowed-tools` add) MUST land at the IS marketplace tier in `validate-skills-schema.py` (not just spec-floor recognition). Future ISEDC charter for kernel v0.4.0 explicitly enumerates the 8-field IS marketplace required set in its decision record.

### 14.11 Stopping criteria / re-plan triggers

- **Anthropic ships a first-party SKILL.md spec authority** (machine-readable, versioned, public) that supersedes both 6767-h and SAK → archive SAK as historical IS contribution; keep the `_vendor/anthropic/` pinning pattern; CCP validators cut over to upstream-canonical.
- **3,044-file migration's wave B stalls past Phase 4's 30-day ceiling** with < 95% quorum → re-plan Phase 4 with smaller eval-loop scope, push remainder to a Phase 4.5 deferred-tail bucket.
- **Kernel v0.4.0 charter rejected by ISEDC** (any blocking minority) → re-scope to ship one authoring contract at a time (skill-frontmatter first); accept the 6× convening cost.
- **6767-h ↔ kernel-authoring/v1 drift exceeds 3 unresolved ADR backlog items at any point** → freeze further phases until drift cleared; mandatory ISEDC review.

---

## Plan-Audit incremental gate (per § 12 recurrence rule #1)

§ 14 is a NEW Phase added to the plan. § 12 recurrence rule #1 fires: "A new Phase is added to the plan" → Plan Audit re-fires INCREMENTALLY.

Incremental scope:

- **NOT re-audited**: §§ 1-13 (ratified per DR-028; covered by 2026-05-26 plan audit deliverable cluster)
- **RE-AUDITED**: § 14 SAK content only — 11 sub-sections (14.1 through 14.11)
- **Brief pack updates** (delta only): add to existing `audit/2026-05-26-plan-audit/brief-pack/`:
  - `11-sak-amendment-v6.md` (THIS doc as the artifact)
  - `12-claude-docs-spec-tree-2026-05-27.md` (the existing spec-tree from prior session that establishes 2.1.152 + `disallowed-tools` ground truth)
  - `13-agentskills-spec-v1.0-snapshot.md` (the spec snapshot)
  - `14-ccp-validator-inventory.md` (to author: enumerate validate-skills-schema.py v6.0 surface — used by panel to verify § 14.10 IS-extras claims)
  - `15-6767-h-master-spec-snapshot.md` (to author: read claude-code-plugins/000-docs/6767-h-\* + summarize structure)
- **Panel composition**: SAME 7 seats (Hickey, Beck, Karpathy, Huyen, Lamport, Cunningham, Kleppmann). Already mobilized; re-fire is incremental.
- **Methodology delta**: each seat reviews § 14 sub-sections through their lens; produces `<seat>-sak-findings.md`. Synthesis appends to existing `synthesis.md` as `synthesis-sak-addendum.md`. STATUS.md updated to reflect incremental ratification.

**Panel guidance** (added to invocation prompt):

> § 14 SAK is a kernel-architecture decision. Karpathy + Hickey + Lamport are primary; Huyen + Kleppmann secondary; Beck + Cunningham tertiary. Focus on (a) does the bicameral kernel architecture create durability or fragility? (b) is the 6767-h ↔ kernel coupling well-specified or under-specified? (c) does the 3,044-file Phase 4 migration plan have realistic stalling-mode mitigation? (d) is § 14.10 IS-marketplace-tier binding load-bearing or aesthetic? (e) does Phase 4 advisory→blocking flip's quorum-pin actually de-risk the highest-blast-radius moment?

## ISEDC Class-1 charter gate

§ 14.8 directive 4: convene ISEDC Class-1 session, single charter for kernel v0.4.0 entity expansion covering all 6 authoring contracts. DR codename: `AT-DECR-spec-authority-kernel-charter` (next sequential number after this doc; likely 032 or 033 depending on bead-filing order).

**Charter scope (binding decisions to ratify):**

1. **Kernel scope expansion**: ratify `intent-eval-core/schemas/authoring/v1/` as Tier-1 kernel material (parity with `schemas/v1/` runtime)
2. **IS marketplace tier as canonical**: ratify § 14.10 binding — the 8-field required-set + IS extras are kernel-canonical, NOT lower tiers
3. **Anti-realignment guard**: ratify the `kernel-rubric-floor-guard.yml` CI gate as authoritative; PRs reducing required-fields without Class-1 ADR fail red
4. **6767-h as upstream citation source**: ratify 6767-h as the prose master spec the kernel cites; drift resolution requires ONE PR amending both
5. **Phase 0 sequencing**: ratify D4 ships before convening (already taken as CTO call § 14.6 Q2); ratify ISEDC Class-1 charter session can run in parallel to D4 patch landing
6. **Phase 4 advisory→blocking quorum-pin**: ratify 99.5% with 30-day ceiling as the gate-flip discipline (CTO call § 14.6 Q4)

**Panel composition for charter session**: 7-seat ISEDC (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel) — same canonical roster as DR-028. Acting head: user (Jeremy Longshore) or delegated Claude per CTO-mode delegation.

## Stopping criteria for this amendment

This amendment (v6) is itself bounded:

- If incremental Plan Audit returns ≥ 1 BLOCKER on § 14 → amendment is reverted to PROPOSED-WITH-DELTAS; remediation applied; re-audit
- If ISEDC Class-1 charter rejects kernel v0.4.0 scope → § 14 is reverted to single-contract-at-a-time variant (skill-frontmatter first); v7 amendment authored
- If 6767-h master spec is itself unstable at audit time → § 14 deferred until 6767-h ratification freeze

## Companion artifacts (this amendment ships with these)

- **iec-E11 SAK epic + 6 schema children + corpus umbrella + ISEDC charter bead + 6767-h kernel-map bead** (filed in same execution as this doc)
- **ccp-d4-followup bead** (filed) — gates D4 patch
- **Brief-pack additions 11-15** (THIS doc + spec tree + agentskills snapshot + validator inventory + 6767-h snapshot)
- **DR-032 (forthcoming) ISEDC Class-1 charter session ratification** (post-this-amendment, before Phase 1 ship)

## Status banding

PROPOSED — pending § 12 incremental Plan Audit (panel mobilization deferred to next session for context economy) + ISEDC Class-1 charter session ratification (DR-032 forthcoming) + user ExitPlanMode signoff.

— Jeremy Longshore
intentsolutions.io
