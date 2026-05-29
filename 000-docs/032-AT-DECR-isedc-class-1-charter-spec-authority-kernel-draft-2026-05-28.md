---
title: ISEDC Class-1 Charter — Spec Authority Kernel (kernel v0.4.0 authoring/v1)
date: 2026-05-28
status: DRAFT — DEFERRED 2026-05-28 pending plan 031 v7 amendment per § 14 SAK incremental Plan Audit verdict NEEDS-AMENDMENT (12 P0 + 17 P1; 3 convergent themes C1/C2/C3). Charter scope (6 decisions in § 3) is UNCHANGED — convening defers until v7 closes the P0 cluster. Audit synthesis: `intent-eval-lab/000-docs/audit/2026-05-28-sak-incremental-audit/synthesis.md`.
class: Class-1 charter (entity-expansion / kernel-scope-bound; distinct from Session-N tension arbitration)
author: Jeremy Longshore (drafter: Claude as acting CTO under CTO-mode delegation 2026-05-28)
parent_plan: intent-eval-lab/000-docs/031-PP-PLAN-skill-refiner-sak-amendment-v6-2026-05-28.md § 14.8 directive 4
beads: bd_000-projects-8vq0 (charter), bd_000-projects-3kye (SAK epic)

# Tri-link block (per § 3.5 PR-1)
Beads: bd_000-projects-8vq0, bd_000-projects-3kye
GitHub: jeremylongshore/intent-eval-lab#<TBA>
---

# ISEDC Class-1 Charter — Spec Authority Kernel (SAK) — kernel v0.4.0 authoring/v1

> **What this is:** the ratifying decision record for the kernel scope expansion proposed by plan 031 v6 § 14. This doc is DRAFT until (a) user signoff via ExitPlanMode equivalent, (b) live 7-seat ISEDC convening (in person or asynchronous on bd), and (c) verbatim seat positions captured per adversarial-integrity protocol.

> **Why "Class-1" not "Session-N":** prior ISEDC sessions (Session 4 = DR-010 widened-scope lock; Session 5 = DR-018 j-rig reconciliation; Session 6 = DR-022 beads re-engage; Session 7 = DR-028 Skill Refiner plan ratification) ratified tension arbitrations against in-flight plans. This charter is **different in kind** — it expands the kernel's scope (the 14 → 14+6 entity surface) and requires written charter rather than tension arbitration. Class-1 = charter-class session; Class-2 = future entity-scope changes that follow this template; subsequent tension-arbitration sessions resume the Session-N numbering.

## Drafter's note

This doc is authored as a DRAFT to be circulated to ISEDC seats before convening. The 6 decisions listed in § 3 below are presented as PROPOSED ratifications. Live convening (in-person OR asynchronous bd channel) is where each seat issues their verbatim position; this drafter does not pre-fill seat positions.

The drafter's recommended dispositions (per CTO-mode delegation per user 2026-05-28) are included alongside each decision but are NOT binding — they are pre-positioned arguments for the seats to consider, not pre-decided outcomes.

## 1. Context

### 1.1 What gets ratified

Kernel v0.4.0 adds `intent-eval-core/schemas/authoring/v1/` as a parallel family alongside the existing `schemas/v1/` runtime contracts. The 14 existing runtime entities are unchanged; 6 NEW authoring contracts are added:

1. `skill-frontmatter.schema.json` — SKILL.md YAML head
2. `plugin-manifest.schema.json` — `plugin.json`
3. `agent-definition.schema.json` — `agents/*.md` frontmatter
4. `mcp-config.schema.json` — `.mcp.json` + plugin.json `mcpServers`
5. `hook-config.schema.json` — `hooks.json`
6. `marketplace-catalog.schema.json` — `marketplace.json`

Each contract carries 3 `$defs` tiers per plan § 14.10: `standardFloor` (minimal Anthropic-spec floor), `openStandardCompliant` (agentskills.io v1 surface where applicable), `isMarketplace` (IS enterprise standard — 8-field required-set + IS extras).

### 1.2 Why this requires a Class-1 charter (not a CTO call)

Per `claude-code-plugins/000-docs/SCHEMA_CHANGELOG.md` NON-NEGOTIABLES item 7: *"Architectural changes need explicit user approval BEFORE the change lands."* The kernel scope expansion is architectural (bicameral kernel; new entity family). It is NOT a tactical CTO call (cf. CTO calls § 14.6 Q1-Q5 in plan 031). The 5 CTO calls already made are tactical (charter scope, D4 sequencing, vendor pattern, quorum-pin, global-skills posture); they apply WITHIN the scope of a ratified charter. The charter itself is the ratification gate.

### 1.3 Triggering event

User direction 2026-05-28 (verbatim): *"intent eval lab, jrig, all of this will be the source of truth for the schemas, the scaffolding, the context, all the rules, regulations regarded to building these items"* — and *"we want to make sure that we encode an enterprise standard"*.

These statements established (a) kernel-as-source-of-truth for authoring artifacts (not just runtime) and (b) IS-marketplace-tier as the binding enterprise standard. Plan 031 § 14 operationalizes these directives; this charter ratifies the operationalization.

### 1.4 Cited authorities

| Authority | Citation |
|---|---|
| Plan 027 v5 | Ratified per DR-028; binding for §§ 1-13 |
| DR-018 § 6.4 (Option α-minus) | Kernel-canonical + lab redirect-stubs pattern; basis for SAK architecture |
| CCP NON-NEGOTIABLES (SCHEMA_CHANGELOG.md) | 7-item discipline; item 1 (8-field IS set), item 3 (rubric-sits-on-top), item 7 (architectural change gating) |
| 6767-h master spec | `claude-code-plugins/000-docs/6767-h-SPEC-DR-STND-claude-code-extensions-master.md` — prose authority |
| agentskills.io v1.0 | `intent-eval-lab/research/agentskills-spec-v1.0-snapshot.md` — open standard floor |
| Claude Code spec tree 2026-05-27 | `intent-eval-lab/research/claude-docs-spec-tree-2026-05-27.md` — 22-URL walk |

## 2. Pre-session briefing — what every seat must read

Each of 7 seats must have read the following before issuing their position:

1. Plan 031 v6 amendment (THIS plan)
2. DR-028 (Session 7 ratification) for context on the original Skill Refiner plan
3. SCHEMA_CHANGELOG.md NON-NEGOTIABLES (items 1, 3, 7)
4. agentskills.io v1.0 spec snapshot
5. Claude Code spec tree (22-URL walk, 2026-05-27)
6. 6767-h master spec (relevant sections per the recommendation: skill-frontmatter, plugin-manifest, agent, MCP, hook, marketplace)
7. `validate-skills-schema.py` current state at SCHEMA 3.7.0 (D4 wedge merged) — so seats see what's already in flight

Pre-reading load is comparable to DR-028 brief pack (~10 docs); manageable for the existing 7-seat panel.

## 3. Decisions to ratify (6)

Each decision is presented as PROPOSED — seats discuss, vote, and the result is captured verbatim in the final ratified version of this doc.

### 3.1 Decision D-SAK-1: Kernel scope expansion

**PROPOSED:** Ratify `intent-eval-core/schemas/authoring/v1/` as Tier-1 kernel material at parity with `schemas/v1/` runtime contracts. The kernel becomes BICAMERAL: runtime contracts (existing) + authoring contracts (new).

**Drafter's recommended disposition:** YES.

**Rationale (drafter):** authoring contracts have ≥16 consumers (8 CCP + 8 global validators) + 6 creators + 3,543 SKILL.md corpus + every CCP CI workflow. Lab placement would invert the dependency direction (lab → kernel rather than kernel → lab) and break DR-018 § 6.4 Option α-minus precedent.

**Anticipated minority positions:**
- *CSO*: kernel scope creep risk — every entity added is a future maintenance burden. Counter: the 6 contracts replace 16+ partial-knowledge validators with one canonical surface; net maintenance reduction.
- *CTO*: prefer single-contract-at-a-time (skill-frontmatter first). Counter: § 14.6 Q1 CTO call already weighed this; one charter is cheaper than six convenings; package-deal honors DR-028 Session 7 precedent.

### 3.2 Decision D-SAK-2: IS marketplace tier as canonical

**PROPOSED:** Ratify § 14.10 binding — kernel `$defs.isMarketplace` is the CANONICAL position; lower tiers exist only as composition floors for external consumers seeking subset compliance.

**Drafter's recommended disposition:** YES.

**Rationale (drafter):** anchored on NON-NEGOTIABLES item 3 ("IS rubric SITS ON TOP of Anthropic's spec"). Sanded-down kernel = sanded-down Skill Refiner signal = brand promise dilution per § 14.10 "Why this matters beyond aesthetics".

**Anticipated minority positions:**
- *CMO/VP DevRel*: lower-tier defaults would expand TAM (cross-vendor distribution per § 2.5 Phase F consideration). Counter: tiers are still exposed via `$defs.openStandardCompliant` and `$defs.standardFloor`; external consumers opt-in to the strictness they need. Default-canonical is IS marketplace.

### 3.3 Decision D-SAK-3: Anti-realignment guard CI gate

**PROPOSED:** Ratify `kernel-rubric-floor-guard.yml` as authoritative CI gate. PRs that remove required-fields from `$defs.isMarketplace.required` without an explicit ISEDC Class-1 ADR fail red.

**Drafter's recommended disposition:** YES.

**Rationale (drafter):** mirrors CCP `SCHEMA_CHANGELOG.md` NON-NEGOTIABLES discipline (established 2026-04-28 after a one-day debacle). Machine-enforced beats honor system. NON-NEGOTIABLES item 1 already says no relaxation without explicit Jeremy approval; this gate operationalizes it for the kernel.

**Anticipated minority positions:**
- *CFO*: CI gate adds maintenance overhead. Counter: gate is one bash script; same cost as `harness-hash-verify.yml`. Trivial.

### 3.4 Decision D-SAK-4: 6767-h as upstream citation source

**PROPOSED:** Ratify 6767-h master spec (`claude-code-plugins/000-docs/6767-h-SPEC-DR-STND-claude-code-extensions-master.md`) as the prose master that kernel authoring schemas cite via `$comment`. Drift between prose and schema is resolved by ONE PR amending both — never unilaterally.

**Drafter's recommended disposition:** YES.

**Rationale (drafter):** 6767-h is the existing CCP-side prose authority that landed 2026-05-28 (supersedes 6767-a/b/c). Kernel schemas as its machine-readable shadow preserves the human-readable authority. `prose-schema-coherence.yml` CI gate (NEW per § 14.5) enforces the citation invariant.

**Anticipated minority positions:**
- *GC*: prose-schema coupling could create license/IP ambiguity if 6767-h moves outside CCP. Counter: 6767-h is repo-bound to claude-code-plugins; the citation is by section heading, not by content reproduction. Schemas remain license-clean.

### 3.5 Decision D-SAK-5: Phase 0 sequencing (D4 before convening; parallelizable)

**PROPOSED:** Ratify CTO call § 14.6 Q2 — D4 validator patch ships BEFORE this charter convenes. Parallel pathway is acceptable: live convening can occur while D4 is in PR review (already the case: D4 is on PR #788, awaiting Gemini review, as of charter draft 2026-05-28).

**Drafter's recommended disposition:** YES (already executing; CTO call documented).

**Rationale (drafter):** D4 is a single-validator local fix that doesn't touch the kernel. Sequencing it BEFORE convening un-blocks Skill Refiner Phase A.0 judge credibility. Class-1 charter scope does NOT include validator-only patches; D4 lives within tactical CTO authority.

**Anticipated minority positions:**
- None expected. CTO call is uncontroversial.

### 3.6 Decision D-SAK-6: Phase 4 advisory→blocking quorum-pin

**PROPOSED:** Ratify CTO call § 14.6 Q4 — `validate-plugins.yml` flips from advisory to BLOCKING when (a) ≥99.5% of CCP SKILL.md corpus passes kernel schema in advisory mode AND (b) at least 30 calendar days have elapsed in advisory mode (the 30-day calendar ceiling caps both directions: prevents premature flip and prevents indefinite stall).

**Drafter's recommended disposition:** YES.

**Rationale (drafter):** Phase 4 advisory→blocking is the SINGLE HIGHEST-BLAST-RADIUS moment in the SAK initiative. A premature flip breaks every plugin author. An indefinite-deferred flip keeps drift accumulating. Quorum + ceiling de-risks both.

**Anticipated minority positions:**
- *CTO*: 99.5% might be too lenient (15-ish files left ambiguous in a 3,543-file corpus). Counter: those 15 land in `eval-loop wave B` per § 14.4 Phase 4 — Skill Refiner handles them post-flip. Lenient is intentional.
- *CSO*: 30-day ceiling might rush late-discovered edge cases. Counter: if true emergencies discovered, ISEDC Class-2 (future) can extend the ceiling; gate is overrideable by charter.

## 4. Panel composition (7 seats)

Same canonical ISEDC roster as DR-028 + prior sessions:

| Seat | Acronym | Primary lens | Reading focus |
|---|---|---|---|
| Chief Technology Officer | CTO | Engineering durability | § 14.2 architecture; § 14.6 CTO calls already taken |
| General Counsel | GC | License / IP / contractual | § 14.10 brand-promise; D-SAK-4 6767-h coupling |
| Chief Marketing Officer | CMO | Brand / positioning / TAM | § 14.10 brand-promise; D-SAK-2 tier-default disposition |
| Chief Financial Officer | CFO | Cost / bandwidth / overhead | § 14.6 Q1 charter scope (single vs six); D-SAK-3 CI gate cost |
| Chief Strategy Officer | CSO | Long-horizon / risk surface | § 14.7 risks; D-SAK-1 scope creep counter; D-SAK-6 lenient-quorum counter |
| Chief Information Security Officer | CISO | Supply chain / trust / drift | § 14.5 CI gate strategy; D-SAK-3 anti-realignment guard; D-SAK-6 30-day ceiling |
| VP DevRel | VP DevRel | External adopter / community | § 14.3 consumer matrix; § 14.10 brand-promise; D-SAK-2 tier-default counter |

Acting head: user (Jeremy Longshore) or Claude per CTO-mode delegation (consistent with DR-028 acting-head pattern).

## 5. Convening modality

Two acceptable forms (per DR-028 § established methodology):

### 5.1 Synchronous in-person convening
~2 hours; live capture of verbatim positions; acting head moderates; consensus per decision.

### 5.2 Asynchronous bd-channel convening
Each seat issues their verbatim position by writing to a per-seat findings file (analogous to Plan Audit synthesis pattern but for charter ratification):

```
intent-eval-lab/000-docs/audit/2026-05-28-sak-charter/
├── README.md
├── brief-pack/   (the 7 pre-reading docs listed in § 2)
├── positions/
│   ├── cto-position.md
│   ├── gc-position.md
│   ├── cmo-position.md
│   ├── cfo-position.md
│   ├── cso-position.md
│   ├── ciso-position.md
│   └── vp-devrel-position.md
├── synthesis.md
└── STATUS.md (DRAFT | RATIFIED | RATIFIED-WITH-DELTAS | REJECTED)
```

Asynchronous form is acceptable here because the 6 decisions are well-scoped; no tension arbitration needed.

## 6. Ratification gates

This charter is RATIFIED when:

1. All 7 seats have issued positions (per § 5.1 transcript or § 5.2 per-seat files)
2. All 6 decisions have either consensus-YES or consensus-NO; tied decisions trigger drafter's recommendation as tiebreak per CTO-mode delegation
3. STATUS.md says RATIFIED
4. THIS doc (032) is finalized with verbatim seat positions and the consensus disposition for each decision
5. Companion implementation (bd updates): `bd_000-projects-3kye` (SAK epic) is unblocked from `bd_000-projects-8vq0` (this charter); Phase 1 schema beads become CLAIMABLE.

If ANY decision is REJECTED:
- `D-SAK-1` REJECTED → SAK is reverted to per-contract-at-a-time; v7 plan amendment authored
- `D-SAK-2` REJECTED → re-plan § 14.10 to acknowledge lower-tier defaults
- `D-SAK-3` REJECTED → kernel `$defs.isMarketplace.required` becomes honor-system; CI gate removed from plan
- `D-SAK-4` REJECTED → 6767-h kernel-map (bd_000-projects-yum7) downgraded to advisory; prose-schema-coherence.yml not deployed
- `D-SAK-5` REJECTED → D4 is unwound (commit ca0ca57bf reverted on PR #788); embarrassing but not catastrophic
- `D-SAK-6` REJECTED → Phase 4 sequencing re-planned; quorum + ceiling discipline replaced with alternative per ISEDC direction

## 7. Verbatim seat positions (TO BE FILLED AT CONVENING)

```
CTO: [TO BE FILLED]
GC: [TO BE FILLED]
CMO: [TO BE FILLED]
CFO: [TO BE FILLED]
CSO: [TO BE FILLED]
CISO: [TO BE FILLED]
VP DevRel: [TO BE FILLED]

Acting head ruling (if any binding minority overrides): [TO BE FILLED]
```

## 8. Final dispositions (TO BE FILLED AT CONVENING)

```
D-SAK-1: [RATIFIED | REJECTED | RATIFIED-WITH-DELTAS]  — vote tally  — minority binding (if any)
D-SAK-2: [...]
D-SAK-3: [...]
D-SAK-4: [...]
D-SAK-5: [...]
D-SAK-6: [...]
```

## 9. Post-ratification action map

Once RATIFIED:

| Bead | Action |
|---|---|
| `bd_000-projects-3kye` (SAK epic) | Status: open (was blocked on charter; now claimable by Phase 1 work) |
| `bd_000-projects-azj4` (E11a skill-frontmatter) | First Phase 1 schema; first claimable after charter |
| `bd_000-projects-htsa/ggef/3f0i/9gu8/yc87` (E11b-f) | Claimable in parallel with E11a per dep graph (all dep on SAK epic + charter) |
| `bd_000-projects-9l35` (E11h corpus migration) | Stays blocked on E11a shipping in kernel v0.4.0 (per § 14.4 Phase 4 sequencing) |
| `bd_000-projects-yum7` (6767-h kernel-map) | Claimable in parallel; depends on at-least-one E11* schema for the map to have content |
| `bd_000-projects-8vq0` (THIS charter) | Closed with reason "RATIFIED" + DR pointer |

## 10. Status banding

**DRAFT** — pending:
- User signoff via ExitPlanMode equivalent (acting-CTO-drafted; user-as-acting-head must authorize convening per DR-028 precedent)
- Live ISEDC convening (synchronous or asynchronous per § 5)
- Verbatim seat positions captured (§ 7)
- Final dispositions filled (§ 8)
- STATUS.md updated to RATIFIED in `audit/2026-05-28-sak-charter/`

— Jeremy Longshore
intentsolutions.io
