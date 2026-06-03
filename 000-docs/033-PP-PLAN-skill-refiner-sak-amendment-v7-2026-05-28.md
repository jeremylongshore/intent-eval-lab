---
date: 2026-05-28
status: PROPOSED-FOR-REAUDIT — pending incremental Plan Audit on v7 deltas + ISEDC Class-1 charter ratification (032 deferred until v7 RATIFIED-WITH-DELTAS or RATIFIED)
supersedes_relationship: REVISES + EXTENDS plan 031 v6 (the v6 amendment to plan 027 v5). v7 does NOT supersede v6; it lands the audit remediations as deltas. § 14 sub-section numbers from v6 are preserved; v7 introduces new sections (§ 14.A, § 14.B, § 14.12-14.28) and REVISES existing ones (§ 14.2, § 14.4, § 14.10, § 14.11, § 14.20).
author: Jeremy Longshore (executor: Claude as drafting acting-CTO under CTO-mode delegation 2026-05-28)
parent_audit: intent-eval-lab/000-docs/audit/2026-05-28-sak-incremental-audit/synthesis.md
audit_verdict_being_remediated: NEEDS-AMENDMENT (12 P0 + 17 P1 + 13 P2 = 42 findings; 3 convergent P0 themes C1/C2/C3; 2 convergent P1 themes C4/C5; 4 cross-seat tensions T1-T4)
---

# Skill Refiner Plan v7 Amendment — Spec Authority Kernel (SAK) — audit-closure deltas

## Tri-link block (per § 3.5 PR-1)

```text
Beads: bd_000-projects-3kye, bd_000-projects-8vq0, plus ~25 new remediation beads (filed in companion action; IDs land at filing)
GitHub: jeremylongshore/intent-eval-lab#<TBA>
```

> **Read order:** Plan 027 v5 (ratified body) → plan 031 v6 amendment (SAK introduction) → THIS doc (v7 audit-closure) → 032 charter draft (deferred convening) → audit synthesis (the spec for what v7 remediates).

## Revision history (extends 031 v6)

- 2026-05-26 v1 / v2 / v3 / v4 — original drafts (plan 025 + 027 evolution)
- 2026-05-27 v4.1 / v5 — internal pre-flight pass; DR-028 amendments folded; STATUS → RATIFIED
- 2026-05-28 v6 — plan 031 amendment introducing § 14 SAK (Spec Authority Kernel)
- **2026-05-28 v7 (THIS DOC)** — audit-closure amendment. Folds the C1/C2/C3 P0 remediations + C4/C5 P1 remediations + T1-T4 tension resolutions + 17 individual P1/P2 patches. Authored same-day as v6 because the incremental audit returned NEEDS-AMENDMENT same-day as v6 was filed.

## Status

**State:** PROPOSED-FOR-REAUDIT. This amendment exists to close the 12 P0 cluster surfaced by the 2026-05-28 incremental Plan Audit. The proper next step is a re-audit on v7's deltas only (not a full re-audit of §§ 1-13 or all of v6 — only what v7 changed).

**Hard gate state** (per `bd-claim-precheck.sh` logic): SAK-labeled beads (`sak` + `iec-E11*`) REMAIN not-claimable under NEEDS-AMENDMENT carry-over. v7 amendment work itself proceeds via Refiner-labeled discipline (RATIFIED per DR-028) since it's plan-edit work, not SAK-implementation work. When v7 re-audit closes the P0 cluster, STATUS flips and SAK beads become claimable per the audit's STATUS-flip protocol.

## What v7 changes vs v6

v7 is **purely additive + revising** — no v6 clause is deleted. Where v6 had a stub, v7 fills it. Where v6 was ambiguous, v7 disambiguates. Where v6 had a single section, v7 may decompose into named sub-sections. Net effect: v6 content is preserved; v7 sub-sections override v6 stubs at the point of conflict.

Specifically, v7 introduces:

- **2 new normative sections** at the top of § 14: § 14.A (formal predicate) + § 14.B (cross-schema invariants) — these close C2.
- **REVISED § 14.2** — bicameral kernel framing clarified into 3 named values (closes C3 / F-RH-002).
- **REVISED § 14.4 Phase 4** — decomposed into 4a / 4b / 4b.5-shadow / 4c (closes C1 / F-KB-001).
- **REVISED § 14.10** — `$defs.isMarketplace` decomposed into 4 composable `$defs` (closes C3 / F-RH-001 / F-RH-006).
- **REVISED § 14.11** — Anthropic leading indicators added (closes T2 / F-AK-001).
- **§ 14.12 through § 14.28** — 17 new sub-sections, one per remediation cluster. Most are short (5-15 paragraphs); each closes a specific finding.
- **Bead inventory** — ~25 new remediation beads (§ 14.29) to be filed in a companion action.
- **Re-audit gating** — § 14.30 specifies what triggers v7 re-audit.

## Cross-reference index for the audit

For each P0 / P1 / P2 finding from the synthesis, v7's response:

| Finding                                                                | Closed by                                                      | Notes                                                                                                          |
| ---------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **C1** Phase 4 deployment discipline (5 seats)                         | § 14.4 REVISED + § 14.4.shadow + § 14.4.rollback + § 14.4.cost | Decompose Phase 4 into 4 sub-phases with state machine + shadow + rollback + cost ceiling                      |
| **C2** Schemas-as-policy without evals/predicate/test-corpus (3 seats) | § 14.A + § 14.B + § 14.21                                      | Formal predicate + cross-schema invariants + test corpus discipline                                            |
| **C3** Bicameral architecture complecting + identity (3 seats)         | § 14.2 REVISED + § 14.10 REVISED + § 14.18                     | Three named values + 4-fold `$defs` decomposition + decompose-first-then-test ordering                         |
| **C4** Governance + cadence (2 seats)                                  | § 14.12 + § 14.13                                              | Named seat-bound owners + AAR cadence + dashboard                                                              |
| **C5** Doc sprawl (2 seats)                                            | § 14.13 + § 14.28                                              | Dashboard consolidates; documentation singularity strategy                                                     |
| **T1** Decompose-first vs test-first                                   | § 14.18                                                        | Resolved as Phase 1 test corpus → Phase 1.5 decompose-via-test-failure → Phase 2                               |
| **T2** Bitter-lesson stop vs invest-and-ship                           | § 14.11 EXPANDED + § 14.14                                     | Leading indicators added; port-not-delete discipline ensures investment transfers                              |
| **T3** Formal predicate vs evolving-doc                                | § 14.A                                                         | Predicate lives IN schema `$comment` as structured block; co-located with schema                               |
| **T4** Implicit vs explicit upstream-divergence                        | § 14.10.ext + § 14.11                                          | IS-extras catalog with per-extra upstream-convergence trigger                                                  |
| F-AK-003 det/prob boundary                                             | § 14.9 row 2 expansion (in § 14.A.boundary)                    | 4-quadrant accept/reject matrix                                                                                |
| F-MK-001 kernel-npm vs vendored consistency                            | § 14.15                                                        | Eventual consistency, bounded staleness ≤ 7d                                                                   |
| F-MK-004 wave B durability                                             | § 14.17                                                        | Side-branch + atomic + 3-retry + parked-queue                                                                  |
| F-KB-003 D4 hand-codes before kernel                                   | § 14.24                                                        | Migration plan for D4 → kernel-canonical cutover in Phase 2                                                    |
| F-CH-004 Phase A.0 judge change                                        | § 14.23                                                        | Judge-version pinning at baseline; re-baseline triggers on judge bump                                          |
| F-CH-005 Phase 5 implicit-low-risk                                     | § 14.20 REVISED                                                | Risk acknowledgement + bandwidth gate                                                                          |
| F-LL-004 version-coupling CCP↔kernel                                   | § 14.15                                                        | Coupling invariant stated                                                                                      |
| F-WC-003 IS-extras upstream-convergence trigger                        | § 14.10.ext                                                    | One row per extra                                                                                              |
| F-MK-003 three version identities                                      | § 14.15                                                        | Ordering specified: kernel `$schemaVersion` → CCP `SCHEMA_VERSION` → vendored snapshot                         |
| F-RH-004 wave A/B reconciliation                                       | § 14.17                                                        | Wave A residue + wave B failures share a reconciliation queue                                                  |
| F-RH-005 "read-only" ambiguity                                         | § 14.27                                                        | Three distinct invariants named: read-only-immutable / read-only-no-consumer-cutover / read-only-internal-test |
| F-RH-006 9 IS-extras flat-listed                                       | § 14.10 REVISED + § 14.10.ext                                  | Categories explicit; per-extra row                                                                             |
| F-KB-004 Phase 4c rollback                                             | § 14.4.rollback                                                | Full rollback protocol                                                                                         |
| F-KB-005 prose-schema-coherence parsing                                | § 14.16                                                        | Section-heading parser spec + flake mitigation                                                                 |
| F-KB-006 kernel-bump propagation to Refiner                            | § 14.22                                                        | Refiner's `accept()` pins kernel version + re-runs on kernel bump                                              |
| F-AK-005 `_vendor/anthropic/` bump policy                              | § 14.26                                                        | Bump cadence + drift threshold + auto-PR rules                                                                 |
| F-AK-006 YAML shell-substitution FP/FN                                 | § 14.25                                                        | Measurement protocol + baseline corpus                                                                         |
| F-MK-006 conditional-visibility referential integrity                  | § 14.19                                                        | Referential-integrity rule named                                                                               |
| F-LL-005 prose↔schema reconciliation liveness                          | § 14.16                                                        | Liveness bound ≤ 5 business days                                                                               |
| F-WC-004 nightly cron parsing prose flaky                              | § 14.16                                                        | Parser stability discipline + flake budget                                                                     |
| F-WC-002 doc sprawl reader cost                                        | § 14.28                                                        | Documentation singularity (one canonical entry + projections)                                                  |
| F-WC-001 CI gate re-eval cadence                                       | § 14.13                                                        | 90-day cadence specified                                                                                       |
| F-WC-005 stopping criterion dashboard                                  | § 14.13                                                        | `SAK-DASHBOARD.md` machine-rendered                                                                            |
| F-WC-006 dual-maintained changelogs                                    | § 14.28                                                        | Kernel canonical; CCP cites                                                                                    |
| F-RH-003 vendored schema = 3 values                                    | § 14.15                                                        | Version triple explicit                                                                                        |

---

## § 14.A (NEW) — Formal valid(skill) predicate (closes C2 + T3)

**Per audit synthesis remediation:** "Define the predicate IN the schema's `$comment` as a structured comment block, not in a separate doc."

### 14.A.1 — Predicate definition

For each authoring contract C ∈ {skill-frontmatter, plugin-manifest, agent-definition, mcp-config, hook-config, marketplace-catalog}, the kernel ships a formal predicate `valid_C(artifact, tier)` defined as a composition of named sub-predicates, NOT as a single JSON Schema validator function.

The skill-frontmatter case (canonical):

```text
valid_skill_frontmatter(skill_md, tier) :=
    well_formed_yaml(skill_md)
  ∧ frontmatter_parses(skill_md)
  ∧ name_constraint(skill_md.name)
  ∧ description_constraint(skill_md.description)
  ∧ (tier ⊆ openStandardCompliant → opt_field_types(skill_md))
  ∧ (tier ⊆ isMarketplace → required_field_presence(skill_md, IS_MARKETPLACE_REQUIRED))
  ∧ (tier ⊆ isMarketplace → is_extras_well_formed(skill_md))
  ∧ no_xml_tags(skill_md.name, skill_md.description)
  ∧ no_reserved_words(skill_md.name)
```

Each sub-predicate has a stated typed domain + range. The composition is monotone in `tier` (stricter tier ⇒ more conjuncts; never fewer). The composition is order-independent (a skill that's valid at tier T is valid at every t ⊆ T).

### 14.A.2 — Co-location with schema

The predicate lives in the schema's `$comment` block as structured comment:

````json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://intent-eval-core/schemas/authoring/v1/skill-frontmatter.schema.json",
  "$comment": "PREDICATE valid_skill_frontmatter(skill_md, tier) :=\n    well_formed_yaml(skill_md)\n  ∧ frontmatter_parses(skill_md)\n  ∧ ...\nSee § 14.A of plan 033 for the full composition.\n6767-h-section: §3.2 (Skill frontmatter)\nSee also: $defs.openStandardCompliant.$comment, $defs.isMarketplace.$comment",
  "type": "object",
  ...
}
```text

Consumers reading the schema see the predicate. There is no separate "predicate doc" to go stale. This resolves T3 — both Lamport's precision concern and Cunningham's "specs nobody reads" concern.

### 14.A.3 — Det/prob boundary (closes F-AK-003)

For each predicate `valid_C`, the kernel defines the deterministic vs probabilistic edge:

| Refiner edit outcome                   | valid_C result       | Disposition                                                                                                                                                                                                                                                                                    |
| -------------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| edit accepted by judge (probabilistic) | TRUE (deterministic) | ACCEPT — both gates agree                                                                                                                                                                                                                                                                      |
| edit rejected by judge                 | TRUE                 | REJECT — judge caught a regression schema didn't                                                                                                                                                                                                                                               |
| edit accepted by judge                 | FALSE                | LOG to `schema-revision-candidates` queue (per § 14.B.invariant-violation route). DO NOT auto-accept; do not auto-reject — route to human review with the artifact, judge rationale, and predicate-violation reason as triple. Aggregated weekly into ISEDC Class-2 schema-bump-consideration. |
| edit rejected by judge                 | FALSE                | REJECT — both gates agree                                                                                                                                                                                                                                                                      |

The `schema-revision-candidates` queue is the feedback mechanism that closes the deterministic/probabilistic boundary problem F-AK-003. Schema staleness becomes observable.

### 14.A.4 — Predicate-update discipline

Changing `valid_C` is a kernel breaking-change event (`$schemaVersion` major bump). Adding sub-predicates is additive (minor bump). Loosening sub-predicates (removing conjuncts) is breaking (major bump) and requires ISEDC Class-1 ADR per § 14.10 anti-realignment guard.

### 14.A.5 — Beads

- `iec-E11-valid-predicate-spec` (P0) — author the 6 predicates per § 14.A.1 + structured $comment co-location per § 14.A.2 + ship in `intent-eval-core/000-docs/NNN-AT-SPEC-authoring-predicates.md`
- `iaj-refiner-schema-boundary` (P1) — implement the 4-quadrant routing in `@j-rig/refiner-core` accept()

---

## § 14.B (NEW) — Cross-schema invariants (closes C2 + F-LL-002)

**Per audit:** "cross-field invariants between schemas (e.g., plugin-manifest cites skill-frontmatter; marketplace-catalog cites plugin-manifest) — are dependency edges formally specified?"

### 14.B.1 — Dependency edges

The 6 authoring contracts have non-trivial cross-references:

````

marketplace-catalog ──cites──▶ plugin-manifest ──contains──▶ skill-frontmatter
│ │
├──contains──▶ agent-definition
│
└──contains──▶ mcp-config
│
└──refers-to──▶ hook-config (via plugin.json hooks block)

````text

Each edge is an invariant the kernel enforces. Example: a `marketplace-catalog` entry's `plugins[].source` resolves to a directory whose `plugin.json` validates against `plugin-manifest`. Every `plugin-manifest` `mcpServers[].command` resolves to an executable per `mcp-config` schema.

### 14.B.2 — Invariant catalog

| Invariant ID           | Statement                                                                                                                                        | Where enforced                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------- |
| INV-CAT-PLUGIN         | ∀ catalog entry e ∈ marketplace-catalog.plugins, plugin_manifest_resolves(e.source) ∧ valid_plugin_manifest(content_of(e.source), isMarketplace) | `validate-marketplace --deep`                |
| INV-PLUGIN-SKILL       | ∀ p ∈ plugin-manifest, ∀ s ∈ p.skills, valid_skill_frontmatter(s, isMarketplace)                                                                 | `validate-plugin` per-skill descent          |
| INV-PLUGIN-AGENT       | ∀ p ∈ plugin-manifest, ∀ a ∈ p.agents, valid_agent_definition(a, isMarketplace)                                                                  | `validate-plugin` per-agent descent          |
| INV-PLUGIN-MCP         | ∀ p ∈ plugin-manifest, p.mcpServers[*] ⊨ valid_mcp_config                                                                                        | `validate-plugin` mcp descent                |
| INV-MCP-HOOK           | ∀ m ∈ mcp-config with hook-bindings, valid_hook_config(m.hooks)                                                                                  | `validate-mcp --with-hooks`                  |
| INV-SKILL-HOOK         | ∀ s ∈ skill-frontmatter with hooks block, valid_hook_config(s.hooks)                                                                             | `validate-skillmd` hooks descent             |
| INV-ALLOWED-DISALLOWED | ∀ s ∈ skill-frontmatter, s.allowed-tools ∩ s.disallowed-tools = ∅                                                                                | warning, not error (cross-field consistency) |

### 14.B.3 — Invariant-violation routing

When `valid_C(artifact, tier) = FALSE` due to a cross-schema invariant violation, the disposition is NOT a generic schema error. It is routed:

- Violation of structural invariant (INV-CAT-PLUGIN, INV-PLUGIN-SKILL, etc.) → REJECT with cross-schema-violation error class. Engineer fixes the upstream artifact, downstream re-validates.
- Violation of advisory invariant (INV-ALLOWED-DISALLOWED) → WARN only. Cross-field consistency hint, not gate-blocking.

### 14.B.4 — Beads

- `iec-E11-cross-schema-invariants` (P0) — author the INV-\* catalog + ship enforcement in the corresponding validators.

---

## § 14.2 REVISED (closes C3 / F-RH-002) — Bicameral kernel = 3 named values

**v6 framing collapsed under audit.** v6 § 14.2 said the kernel is "bicameral" with authoring/v1 as "machine-readable shadow of 6767-h prose." This collapses because the IS-only extras (§ 14.10) have NO 6767-h prose anchor — the shadow metaphor breaks at the IS-marketplace tier.

### 14.2.1 — Three named values (replaces the shadow metaphor)

The kernel does NOT have a single "schema-as-shadow-of-prose" identity. It has THREE distinct values:

| Value                               | Lives at                                                                                                | Identity                                                                                                                                                                                       | Owner                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Prose authority**                 | `claude-code-plugins/000-docs/6767-h-SPEC-DR-STND-claude-code-extensions-master.md`                     | Human-readable spec; cited by external parties; what 6767-h IS                                                                                                                                 | CCP-side editorial                                            |
| **IS-marketplace-policy authority** | `intent-eval-core/schemas/authoring/v1/*.schema.json` `$defs.isMarketplace` blocks                      | Machine-checkable IS enterprise policy; what the kernel encodes                                                                                                                                | Kernel maintainers                                            |
| **Coverage map**                    | `intent-eval-core/schemas/authoring/v1/6767h-coverage-map.json` (NEW artifact per F-RH-002 remediation) | Bidirectional table: each schema field cites either (a) a 6767-h section it implements, OR (b) the IS-only-extension category it belongs to with a stated rationale for why it's not in 6767-h | Joint — both editorial sides update on schema or prose change |

### 14.2.2 — Coverage map format

```json
{
  "$schemaVersion": "1.0.0",
  "fields": {
    "skill-frontmatter.$defs.isMarketplace.required.name": {
      "trace_kind": "anthropic-spec-derived",
      "6767h_section": "§3.2.1",
      "anthropic_doc": "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview"
    },
    "skill-frontmatter.$defs.isMarketplace.required.author": {
      "trace_kind": "is-only-extension",
      "6767h_section": null,
      "category": "tracking-metadata",
      "rationale": "Required at IS marketplace tier per SCHEMA_CHANGELOG NON-NEGOTIABLES item 1. No upstream prose anchor by design.",
      "upstream_convergence_trigger": "Anthropic publishes equivalent in agentskills.io v2 or platform.claude.com"
    }
  }
}
````

### 14.2.3 — Three CI gates (replaces v6's single `prose-schema-coherence.yml`)

- `coverage-map-completeness.yml` (NEW) — every schema field has a coverage-map entry. Missing entries = red.
- `prose-anchor-validity.yml` (NEW) — for `trace_kind: "anthropic-spec-derived"` entries, the cited 6767-h section exists. (Renames v6's `prose-schema-coherence.yml` to reflect actual function.)
- `is-extension-rationale.yml` (NEW) — for `trace_kind: "is-only-extension"` entries, both `rationale` AND `upstream_convergence_trigger` are non-empty.

The three gates are decoupled. A prose-side rename of `§3.2.1` to `§3.2.A` updates the coverage map; it does NOT force a schema bump. A new IS-only extension lands in the schema + the coverage map together; the rationale CI gate ensures both arrive in the same PR.

### 14.2.4 — Beads

- `iec-E11-coverage-map` (P0) — author the coverage map artifact + 3 CI gates per § 14.2.3
- `iec-E11-decomp` reframing — what v6 called "decompose `$defs.isMarketplace`" now lives at § 14.10 REVISED below; the C3 architectural remediation is split across § 14.2 (identity clarification) + § 14.10 (composition decomposition).

---

## § 14.4 REVISED (closes C1 / F-KB-001 + F-KB-004 + F-RH-004 + F-MK-002 + F-MK-005) — Phase 4 decomposed into 4a / 4b / 4b.5-shadow / 4c

**v6 Phase 4 was 5 seats' worth of P0 finding.** It's been decomposed into FOUR named sub-phases each with its own deliverable, exit gate, and rollback semantics.

### 14.4a — Wave A deterministic batch (weeks 10-12)

**Deliverable:** Run `batch-remediate.py` against the 3,543-file CCP SKILL.md corpus + 53 global skills. Deterministic frontmatter normalization to kernel-schema-valid IS marketplace tier. Migrate `compatible-with` → `compatibility`; normalize `allowed-tools` to YAML list form; add inferred `version`/`author`/`tags`/`license` from git metadata where unambiguous; emit per-file diff + remediation log.

**Exit gate:** ≥80% of corpus passes kernel schema in advisory mode AFTER wave A. NOT 99.5%; that's the flip gate, not the wave-A-complete gate. Wave A's job is to handle the easy ~80%.

**Rollback semantics:** wave A is a `git revert` of the batch-remediate commit(s). Each file's pre-wave-A state lives in git history. Reverting wave A puts the corpus back; no Evidence Bundle implications because gate is still advisory.

**Reconciliation queue:** files that wave A leaves with WARN-level open issues (not blocking) land in `audit/wave-a-residue.jsonl` for wave B consumption.

### 14.4b — Wave B eval-loop (weeks 13-15)

**Deliverable:** Skill Refiner Phase B eval-loop processes the ~20% wave A didn't handle + wave A residue. Refiner proposes edits per the strict-improvement gate (AC-7); accepted edits land as a per-file PR.

**Exit gate:** ≥99% of full corpus passes kernel schema in advisory mode. Some residue (~30-40 files) may remain — that's expected. Wave B is not required to hit 100%.

**Rollback semantics:** each Refiner edit is its own commit on a per-file branch. Rollback = `git revert` of the specific commits. If wave B's mechanism is itself broken (Refiner produces bad edits at high rate), STOP wave B + reconciliation per § 14.4.rollback below.

**Cost ceiling:** § 14.4.cost specifies the budget. Phase 4b STOPS when budget is hit, regardless of completion percentage; STOPPED wave B does NOT block Phase 4c if the existing advisory pass-rate hits 99.5%.

### 14.4b.5 (NEW) — Shadow-mode discipline (week 15.5)

**Deliverable:** Before the advisory→blocking flip, the CI `validate-plugins.yml` runs in DUAL MODE for ≥ 7 calendar days: existing CCP validator (current authority) + kernel-schema validator (proposed authority). Diff their verdicts per file; report deviation rate.

**Exit gate:** EITHER (a) deviation rate < 0.5% of corpus (acceptable noise; flip safe), OR (b) deviation rate ≥ 0.5% AND each deviation has a named disposition (schema-revision-candidate? validator-bug? file-author-fix?). Shadow mode does NOT end on a calendar; it ends on disposition completeness.

**Rationale:** the kernel-schema validator vs CCP-validator divergence is the most likely source of Phase 4c surprises. Shadow mode surfaces them before they break authors at flip time.

### 14.4c — Advisory→blocking flip (week 16)

**Deliverable:** `validate-plugins.yml` config flag flips from `mode: advisory` to `mode: blocking` for SKILL.md. PR-blocking starts.

**Exit gate (quorum-pin discipline preserved from v6 with refinements):**

- (a) ≥ 99.5% of corpus passes kernel schema in advisory + shadow modes
- (b) ≥ 7 calendar days of shadow mode complete with deviation rate < 0.5% (per § 14.4b.5)
- (c) AND (NEW) no open P0 issues in the `schema-revision-candidates` queue per § 14.A.3
- (d) AND (NEW) governance-owner sign-off per § 14.12 (CTO + CISO + VP DevRel triple)

30-day calendar ceiling carries over from v6 § 14.6 Q4 — gate flips by day 30 even if quorum is < 99.5%, with remaining files quarantined per § 14.4.rollback's `quarantine-queue`.

**Rollback semantics (NEW, addresses F-KB-004 + F-MK-005):** § 14.4.rollback below.

### 14.4.shadow (NEW) — Shadow-mode state machine

The state machine for Phase 4 is:

```text
                 ┌─────────────────┐
                 │ ADVISORY (v6)   │
                 │ default state   │
                 └────────┬────────┘
                          │ wave A runs
                          ▼
                 ┌─────────────────┐
                 │ ADVISORY-W-A    │
                 │ wave A merged   │
                 └────────┬────────┘
                          │ wave B runs (eval-loop)
                          ▼
                 ┌─────────────────┐
                 │ ADVISORY-W-AB   │
                 │ both waves done │
                 └────────┬────────┘
                          │ enable shadow
                          ▼
                 ┌─────────────────┐
                 │ SHADOW-MODE     │
                 │ dual-validator  │
                 └────┬──────┬─────┘
                      │      │
            deviations│      │ all dispositions resolved
            (P0 open) │      │
                      ▼      ▼
            ┌─────────┐    ┌─────────────────┐
            │ HOLDING │    │ READY-TO-FLIP   │
            │ (audit) │    │                 │
            └─────────┘    └────────┬────────┘
                                    │ governance triple signs
                                    ▼
                          ┌─────────────────┐
                          │ BLOCKING        │
                          │ flip complete   │
                          └────────┬────────┘
                                   │ regression detected
                                   ▼
                          ┌─────────────────┐
                          │ ROLLED-BACK     │
                          │ back to SHADOW  │
                          └─────────────────┘
```

State transitions are machine-readable in `SAK-STATE.json` (per § 14.13 dashboard). Each transition emits a kernel-side Decision Record + Evidence Bundle entry.

### 14.4.rollback (NEW, closes F-KB-004 + F-MK-005) — Phase 4 rollback protocol

Three classes of failure trigger different rollback paths:

1. **Wave A failure** (deterministic batch broke files): `git revert` the batch commit. Authors see pre-wave-A state restored. No Evidence Bundle implications. STATE → ADVISORY-W-A-ROLLED-BACK; root-cause analysis; re-attempt with fixed `batch-remediate.py`.

2. **Wave B failure** (Refiner producing bad edits): per-file rollback of specific Refiner-commits via `git revert`. Affected SKILL.md returns to wave-A-state. STATE → ADVISORY-W-AB-PARTIAL; reconciliation queue annotates which files remain unmigrated.

3. **Post-flip regression** (BLOCKING mode is breaking real PRs at high rate): governance triple (per § 14.12) authorizes a single command — `kernel-gate-revert <reason>` — which (a) flips `validate-plugins.yml` back to `mode: advisory`, (b) records a Decision Record (`AT-DECR-phase-4c-rollback-NNN`), (c) emits a kernel-side Evidence Bundle row marking BLOCKING attestations from the affected window as `signing_mode: rolled-back-superseded`, (d) opens an ISEDC Class-2 retrospective session within 7 calendar days.

**Critical constraint (F-MK-005):** snapshot semantics during rollback. Any Evidence Bundle rows emitted between SHADOW-MODE entry and BLOCKING flip are PRESERVED — they're real attestations. The rollback marks them `signing_mode: rolled-back-superseded` in a separate envelope event, NOT by mutating the original Rekor entries (Rekor is append-only). Downstream consumers learn that the BLOCKING-window attestations are advisory-not-binding via the superseding event, not by retraction.

### 14.4.cost (NEW, closes F-AK-004) — Per-file Refiner cost ceiling

Wave B Refiner runs against ~20% of corpus = ~700 files. At default Refiner cost tier (Sonnet refiner + Haiku rollout scoring per plan 027 AC-5), per-file mean budget should be tracked.

**Cost ceiling:** $50 USD per file mean, $200 max single file (hard cap). Total wave B budget: $35K USD (= $50 × 700). Tracked in `audit/wave-b-cost-ledger.jsonl`.

**Cost-meter discipline:**

- Each Refiner attempt logs token usage + model tier
- After each accept/reject, cost is rolled up into the per-file row
- Hard cap firing on a single file = move that file to `quarantine-queue` for manual review (don't keep spending)
- 80% of total budget firing = STOP wave B; whatever progress has been made is the new advisory baseline
- 100% budget firing = STOP wave B unconditionally; file becomes a P0 finding for governance triple

**Refiner cost instrument:** `bd_000-projects-<TBA>` — `iaj-refiner-cost-instrument` — instrument `@j-rig/refiner-core` to emit cost-per-attempt + per-accept rollups via existing j-rig OTel spans.

### 14.4 — Beads

- `iec-E11-phase-4-decompose` (P0) — REVISE § 14.4 of the kernel docs to reflect 4a/4b/4b.5/4c structure
- `iec-E11-phase-4b-5-shadow-mode` (P0) — implement dual-validator shadow + deviation tracking
- `iec-E11-phase-4-state-machine` (P0) — author `SAK-STATE.json` schema + state-transition emit code
- `iec-E11-phase-4-snapshot-rules` (P0) — author Rekor superseding-event protocol per F-MK-005
- `iec-E11-phase-4c-rollback-protocol` (P0) — author `kernel-gate-revert` command + governance triple gate
- `iaj-refiner-cost-instrument` (P0) — instrument cost meter per § 14.4.cost

---

## § 14.10 REVISED (closes C3 / F-RH-001 / F-RH-006) — `$defs.isMarketplace` decomposed into 4 composable `$defs`

**v6 framing complected 4 orthogonal concerns into one `$defs` per F-RH-001.** Decomposed:

| New `$defs`                               | Concern                                | Evolves under                                           | Example fields                                                                    |
| ----------------------------------------- | -------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `$defs.isMarketplace.requiredFields`      | The 8-field required-set               | ISEDC Class-1 ratification (NON-NEGOTIABLES item 1)     | `name, description, allowed-tools, version, author, license, compatibility, tags` |
| `$defs.isMarketplace.deprecationRegistry` | Field-deprecation migrations           | Validator patch (autonomous per NON-NEGOTIABLES item 6) | `compatible-with → compatibility`, `when_to_use → description`, etc.              |
| `$defs.isMarketplace.securityChecks`      | Supply-chain hardening                 | CISO-driven                                             | YAML shell-substitution checks, reserved-word constraints, no-XML-tag constraints |
| `$defs.isMarketplace.disclosureMarkers`   | Progressive disclosure / token-economy | Karpathy-axis                                           | L0/L1/L2 markers, token-budget rules                                              |

The "marketplace tier" is now the COMPOSITION of these four:

`````json
{
  "$defs": {
    "isMarketplace": {
      "allOf": [
        { "$ref": "#/$defs/isMarketplace/requiredFields" },
        { "$ref": "#/$defs/isMarketplace/deprecationRegistry" },
        { "$ref": "#/$defs/isMarketplace/securityChecks" },
        { "$ref": "#/$defs/isMarketplace/disclosureMarkers" }
      ]
    },
    "isMarketplace/requiredFields": { ... },
    "isMarketplace/deprecationRegistry": { ... },
    "isMarketplace/securityChecks": { ... },
    "isMarketplace/disclosureMarkers": { ... }
  }
}
```text

**Independent changelogs.** Each composable `$defs` has its own `$comment` documenting its semver evolution. Bumping the deprecation registry (tactical) doesn't force consumers to re-evaluate required-fields (architectural). Each gets its own SCHEMA_CHANGELOG section.

**Consumer composition.** External adopters who want only the required-fields tier can `$ref: isMarketplace/requiredFields` without inheriting deprecation-registry parsing. Internal CCP validator targets the full `isMarketplace` composition.

### 14.10.ext (NEW, closes T4 + F-WC-003 + F-AK-001 leading indicators) — IS-extras divergence catalog

Each IS-only-extension is cataloged with:

| Extension                                                      | Category (per § 14.10.4-fold decomp) | Upstream-convergence trigger                              | Leading indicator (when to start aligning)                          |
| -------------------------------------------------------------- | ------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------- |
| `version` (required at IS marketplace)                         | requiredFields                       | Anthropic adds `version` as required in agentskills.io v2 | `agentskills.io/changelog` shows `version` proposal                 |
| `author` (required, must contain `@`)                          | requiredFields                       | Anthropic adds contact-resolvability requirement          | Anthropic publishes skill-author-onboarding doc citing email format |
| `tags` (required, array)                                       | requiredFields                       | Anthropic adds discovery-tag field                        | Anthropic ships a `tags`-aware search in `claude` CLI               |
| `requires_env` / `requires_tools` / etc. (4 visibility fields) | requiredFields (advisory)            | Anthropic adds conditional visibility                     | `claude` CLI ships skill-prereq-prompting                           |
| `required_environment_variables`                               | requiredFields (advisory)            | Anthropic adds installer-prompt convention                | `claude doctor` ships env-var prompting                             |
| `metadata.intent-solutions.config`                             | requiredFields (advisory)            | Anthropic adds skill-config convention                    | Anthropic publishes skill-config standard                           |
| Semver-strict `version` regex                                  | requiredFields                       | (Same as `version` above)                                 | (Same)                                                              |
| Deprecated-field migration registry                            | deprecationRegistry                  | Anthropic publishes field-migration tool                  | `claude-codemod` or equivalent ships                                |
| `shell` enum (bash                                             | powershell)                          | securityChecks                                            | Anthropic adds cross-platform skill discipline                      | Anthropic ships skill-shell-validation |
| `when_to_use` + description ≤ 1536 chars                       | disclosureMarkers                    | Anthropic ships token-budget validator                    | `validate-skillmd` upstream-equivalent ships                        |
| YAML shell-substitution check                                  | securityChecks                       | Anthropic adds supply-chain hardening                     | Anthropic ships skill-security-audit                                |
| `metadata.*` namespacing                                       | requiredFields (advisory)            | Anthropic adopts vendor-namespacing                       | agentskills.io spec adds namespace section                          |

**Periodic review:** § 14.13 dashboard surfaces this catalog with current-state coloring (any triggers firing?). 90-day re-eval cadence per § 14.13.

### 14.10 — Beads

- `iec-E11-decomp` (P0, REVISED scope) — implement the 4-fold `$defs` decomposition + per-fold $comment
- `iec-E11-is-extras-categorize` (P2 per F-RH-006) — implement `x-is-extras-category` markers
- `iec-E11-anthropic-leading-indicators` (P0, expanded scope) — author + auto-poll the 12 leading-indicator URLs in § 14.10.ext + § 14.11

---

## § 14.11 EXPANDED (closes T2 / F-AK-001) — Anthropic leading indicators

v6 § 14.11 stopping criteria listed "Anthropic ships first-party SKILL.md spec authority" as a trigger but without leading-indicator definition. Per F-AK-001, ADDED:

### 14.11.1 — 12 leading indicators (monitored quarterly)

| #   | Indicator                                                                                               | Source                                      | Severity                           |
| --- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ---------------------------------- |
| 1   | Anthropic publishes public roadmap including machine-readable spec                                      | platform.claude.com/roadmap; Anthropic blog | High                               |
| 2   | `claude` CLI begins ingesting `.claude/schema/` directory                                               | `code.claude.com/docs/en/changelog`         | High                               |
| 3   | `claude doctor` adds plugin-format validation                                                           | (Same)                                      | High                               |
| 4   | agentskills.io v2 RFC published                                                                         | `agentskills.io/specification`              | High                               |
| 5   | Anthropic publishes machine-readable agentskills.io v2 schemas                                          | `github.com/agentskills/agentskills`        | CRITICAL                           |
| 6   | Anthropic ships skill-author-onboarding doc citing field validation                                     | Anthropic docs                              | Medium                             |
| 7   | `claude-codemod` or equivalent field-migration tool ships                                               | Anthropic GitHub                            | Medium                             |
| 8   | Anthropic ships skill-shell-validation                                                                  | Anthropic docs                              | Medium                             |
| 9   | Anthropic ships skill-security-audit                                                                    | Anthropic docs                              | Medium                             |
| 10  | agentskills.io spec adds vendor-namespacing section                                                     | agentskills.io                              | Low                                |
| 11  | Vercel skills.sh adopts kernel-schema-compatible format                                                 | `skills.sh` (third-party)                   | Low                                |
| 12  | Frontier model (Claude N+1 or competitor) demonstrates schema-validator equivalence from prose+examples | Public benchmarks                           | CRITICAL — bitter-lesson triggered |

### 14.11.2 — Disposition matrix

| Indicators firing    | Disposition                                                                 |
| -------------------- | --------------------------------------------------------------------------- |
| 0-2 Low-severity     | Continue per plan                                                           |
| 1 Medium             | Note in next AAR; no plan change                                            |
| 2-3 Medium OR 1 High | ISEDC Class-2 retrospective; consider pausing Phase ≥ 3                     |
| 1 CRITICAL           | PAUSE all SAK phases; ISEDC Class-1 re-charter to evaluate upstream cutover |
| 2 CRITICAL           | STOP SAK; archive as historical contribution; cut over to upstream          |

### 14.11.3 — Polling mechanism

`leading-indicator-watch.yml` (NEW CI gate) — daily cron. Polls the 12 sources via WebFetch + GitHub API. Diffs against last-known snapshot. Any new hit opens a `[leading-indicator]` issue + posts to ISEDC bd channel.

**Flake budget:** false-positive rate must be < 5% (audit's F-WC-004 concern). The polling parses STRUCTURED sources (RSS, GitHub releases, JSON schemas) where possible; prose-parsing (Anthropic blog) only for indicators 1, 6 with a 7-day disposition window before escalation.

### 14.11 — Beads

- `iec-E11-anthropic-leading-indicators` (P0) — author the 12-indicator polling per § 14.11.3 + disposition matrix per § 14.11.2

---

## § 14.12 (NEW, closes C4) — Governance owners

| Concern                                               | Owner seat | Responsibility                                                                   |
| ----------------------------------------------------- | ---------- | -------------------------------------------------------------------------------- |
| Kernel schema versioning + breaking-change discipline | CTO        | Sign-off on `$schemaVersion` major bumps; co-sign Phase 4c flip                  |
| IS-marketplace policy floor (anti-realignment)        | CTO + CISO | Veto on `$defs.isMarketplace.requiredFields` changes per NON-NEGOTIABLES         |
| Supply-chain hardening (security checks)              | CISO       | Own `$defs.isMarketplace.securityChecks` evolution; co-sign Phase 4c flip        |
| External adopter relations + brand promise            | VP DevRel  | Co-sign Phase 4c flip; field cross-vendor distribution conversations per Phase F |
| Cost-budget enforcement (Refiner / SAK aggregate)     | CFO        | Sign-off on Phase 4b cost ceiling exceedances; audit wave B cost ledger          |
| Legal IP review on 6767-h / kernel coupling           | GC         | Sign-off on 6767-h ↔ kernel-map ADR amendments (per § 14.16)                     |
| Brand positioning + naming (Skill Refiner, SAK)       | CMO        | Veto on brand-canon changes; review external-facing dashboard copy               |

**Decision authority taxonomy:**

- **CTO+CISO+VP DevRel triple** = required for Phase 4c advisory→blocking flip + any kernel `$schemaVersion` major bump (NON-NEGOTIABLES item 7)
- **CTO alone** = minor/patch kernel bumps; validator patches at IS marketplace tier
- **CFO** = cost-ceiling exceedance authorization (Phase 4b)
- **GC** = 6767-h ↔ kernel coverage-map ADR sign-off
- **CISO veto** = any change to `$defs.isMarketplace.securityChecks`

### 14.12 — Beads

- `iec-E11-governance-owners` (P1) — author this section as `intent-eval-lab/000-docs/NNN-AT-STND-sak-governance-owners.md`; CCP CLAUDE.md cross-references

---

## § 14.13 (NEW, closes C4 + C5 + F-WC-001 + F-WC-005) — SAK dashboard + AAR cadence

### 14.13.1 — `SAK-DASHBOARD.md` machine-rendered

Lives at `intent-eval-lab/SAK-DASHBOARD.md` (root-level for visibility; generated by GH Action on cron).

Content (rendered from `SAK-STATE.json` + bead state + leading-indicator polls):

````markdown
# SAK Dashboard — auto-generated <timestamp>

## Phase status

- Phase 0: COMPLETE (D4 wedge ca0ca57bf merged YYYY-MM-DD)
- Phase 1: IN PROGRESS (4/6 schemas shipped)
- Phase 2: BLOCKED (waits Phase 1.5 decompose-via-fail)
- ...

## State machine (Phase 4)

- Current state: ADVISORY-W-A
- Time in state: 14 days
- Next gate: wave B Refiner cost ledger ≥ 80% budget

## Leading indicators

- 12 monitored | 1 firing (Indicator 6: Anthropic skill-author-onboarding doc cites field validation)
- Disposition: MONITOR. ISEDC Class-2 retrospective scheduled YYYY-MM-DD.

## Cost ledger

- Wave B Refiner: $8,234 / $35,000 (23.5% of ceiling)
- Files completed: 312 / ~700 (45% of expected)
- Mean cost per file: $26.4 ($50 ceiling)

## Bead state

- iec-E11\* open: 17 | in-progress: 3 | closed: 4
- iaj-\* (Refiner-side): open: 12 | in-progress: 2 | closed: 8

## Coverage map state

- Fields total: 87
- Anthropic-spec-derived: 51 (59%)
- IS-only-extension: 36 (41%)
- 6767-h section references: 51 / 51 (100% valid)
`````

### 14.13.2 — AAR cadence

- **After Phase 1 ships** (kernel v0.4.0 published): AAR at `intent-eval-lab/000-docs/NNN-AA-AACR-sak-phase-1-<date>.md`
- **After Phase 2 validator cutover**: AAR
- **After Phase 4a wave A**: AAR
- **After Phase 4b wave B** (or budget exhausted): AAR
- **After Phase 4c flip** (or rollback): AAR
- **Quarterly during Phases 4-5**: AAR roll-up

### 14.13.3 — 90-day CI gate re-eval cadence (closes F-WC-001)

The 4 SAK CI gates (`coverage-map-completeness`, `prose-anchor-validity`, `is-extension-rationale`, `leading-indicator-watch`) each get a quarterly review:

- False-positive rate: target < 2%; > 5% = re-tune
- False-negative rate: target unknown (no oracle); manual sample of 20 PRs per quarter
- Maintenance burden: developer-hours spent fixing flakes; target < 4hr/quarter
- Gate utility: ratio of true-positive catches to total runs

Quarterly review lands as `intent-eval-lab/000-docs/NNN-RR-LAND-sak-ci-gate-quarterly-<date>.md`.

### 14.13 — Beads

- `iel-sak-dashboard` (P1) — author `SAK-DASHBOARD.md` generator + cron
- `iel-ci-gate-cadence` (P1) — author quarterly-review template + first-quarter run plan

---

## § 14.14 (NEW, T2 resolution) — Bitter-lesson hedge: port-not-delete discipline

Per audit T2 resolution: "structure SAK so that if a leading indicator fires, the discipline (governance owners, consistency model, snapshot rules) ports to the upstream-canonical world rather than getting deleted."

### 14.14.1 — Port-not-delete inventory

When the leading-indicator disposition matrix (§ 14.11.2) triggers STOP, the following artifacts have PORT TARGETS in the upstream world:

| SAK artifact                                        | Port target                                | Port mechanism                                                                                |
| --------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------- |
| `$defs.isMarketplace.requiredFields` 8-field policy | Upstream agentskills.io v2 enforcement     | File issue at agentskills.io; submit PR codifying IS extras as agentskills.io OPTIONAL fields |
| Coverage map artifact                               | Upstream agentskills.io spec sections      | Submit each IS-only extension as a "vendor-namespaced metadata" pattern PR                    |
| Predicate co-location in `$comment`                 | Upstream JSON Schema community pattern     | Document as a public idiom; submit to JSON Schema Specification                               |
| 4-fold `$defs` composition                          | Upstream JSON Schema community pattern     | (Same)                                                                                        |
| Shadow-mode + state machine + rollback protocol     | Upstream `validate-plugins.yml` equivalent | Contribute as PR to whatever upstream validator becomes canonical                             |
| Governance triple (CTO+CISO+VP DevRel)              | (Internal-only — port not applicable)      | Retain as IS internal discipline regardless                                                   |

### 14.14.2 — Trigger-to-port playbook

When § 14.11.2 fires STOP:

1. ISEDC Class-1 re-charter (per § 14.11.2)
2. Per artifact in § 14.14.1 with port target: open upstream PR per port mechanism
3. Track upstream PR status in `SAK-DASHBOARD.md` "port progress" section
4. SAK archived; CCP validator + 3,044 corpus migrate to upstream-canonical

**This makes the SAK investment transfer rather than evaporate.** Karpathy's bitter-lesson concern + Huyen/Kleppmann's invest-and-ship are both honored.

### 14.14 — Beads

- `iec-E11-port-not-delete-playbook` (P1) — author the playbook + ISEDC checklist

---

## § 14.15 (NEW, closes F-MK-001 + F-LL-004 + F-MK-003) — Version-coupling invariants

### 14.15.1 — Three version identities

Per F-MK-003, three version identities must be ordered:

1. **Kernel `$schemaVersion`** (canonical) — lives in `index.json` of kernel `authoring/v1/`. Owns the schema evolution.
2. **CCP `SCHEMA_VERSION`** (consumer) — lives in `validate-skills-schema.py`. MUST declare which kernel version it consumes.
3. **Vendored snapshot version** (cached) — lives in `claude-code-plugins/.kernel-vendor/authoring/v1/index.json`. Must equal a real kernel `$schemaVersion`.

**Ordering invariant:** `vendored.version ≤ CCP.declared_kernel ≤ kernel.latest_published`. Stated mathematically: `V ≤ C ≤ K` where `V` = vendored, `C` = CCP-declared, `K` = kernel latest published.

### 14.15.2 — Eventual consistency, bounded staleness ≤ 7 days

Per F-MK-001 + F-LL-004 remediation:

- Vendored snapshot MAY lag kernel latest by ≤ 7 calendar days
- Beyond 7 days, `kernel-vendor-hash.yml` CI gate fires RED + auto-opens a bump PR
- CCP `SCHEMA_VERSION` declaration MUST be re-evaluated on every kernel bump (PR check)
- Mismatched triple → gate fires RED; PR cannot merge until reconciled

### 14.15.3 — Beads

- `iec-E11-kernel-vendor-consistency-model` (P0) — author the version-coupling spec + CI gates
- `iec-E11-version-ordering-invariant` (P1) — formalize the V ≤ C ≤ K ordering in test corpus

---

## § 14.16 (NEW, closes F-LL-005 + F-WC-004 + F-KB-005) — Prose-schema-coherence machinery

### 14.16.1 — Section-heading parser spec

`prose-anchor-validity.yml` parses 6767-h master spec for section headings. The parser:

- Reads markdown headers (`^#+\s+`)
- Extracts section IDs (numerical hierarchy `§1.2.3` or named `§Skill-Frontmatter`)
- Builds an in-memory section tree
- For each `trace_kind: "anthropic-spec-derived"` entry in coverage map, verifies `6767h_section` is a leaf or intermediate node in the tree

**Stability discipline:** the parser is deterministic given input; no LLM in the loop. Markdown is parsed by a pinned `markdown-it` version (specified in `package.json` of the gate's GitHub Action). Renumbering a 6767-h section requires a coverage-map PR in the same commit.

### 14.16.2 — Liveness bound ≤ 5 business days (F-LL-005)

When prose-schema drift is detected (a coverage-map entry cites a 6767-h section that no longer exists), the gate fires RED. The reconciliation MUST land within 5 business days:

- Day 1: gate fires; auto-PR opens with the drift description
- Day 1-3: editor (per § 14.12 — CTO for kernel, CCP-editorial for prose) resolves
- Day 4: escalation to GC (if 6767-h change has IP implications) or governance triple
- Day 5: ISEDC Class-2 retrospective session triggered IF unresolved
- Day > 5: CI is BLOCKED on the repository until resolved (force-rebase against affected files fails)

### 14.16.3 — Flake budget (F-WC-004)

Cron parsing prose is a known flake source. Mitigation:

- Parser runs daily; flake = parser produces different output for unchanged input
- Flake budget: 1 false-positive per quarter accepted as noise; > 1 = retune
- All parse outputs logged to `.gate-logs/prose-parser-<date>.log` for diff analysis
- Manual re-run available via workflow_dispatch

### 14.16 — Beads

- `iec-E11-prose-anchor-parser` (P0) — implement the parser per § 14.16.1
- `iec-E11-prose-schema-liveness` (P1) — implement the 5-day escalation timer

---

## § 14.17 (NEW, closes F-MK-004 + F-RH-004) — Wave B durability protocol

### 14.17.1 — Per-file branch + atomic commit

Each wave B Refiner attempt operates on a per-file branch:

- Branch name: `refiner/wave-b/<file-hash>`
- Single commit per accepted edit; commit message includes Refiner-run-ID + cost + score-delta
- Failed attempts produce NO commit (rolled back at the working-tree level)
- Successful attempts produce one commit + open PR auto-merged after `validate-plugins.yml` passes

### 14.17.2 — 3-retry + parked queue

For each file:

- Attempt 1: standard Refiner config (Sonnet + default eval set)
- Attempt 2 (if 1 fails): retry with adjusted prompt (clarifies failure mode)
- Attempt 3 (if 2 fails): retry with Opus
- 3 failures: file moved to `audit/wave-b-parked-queue.jsonl` for manual review

### 14.17.3 — Reconciliation queue (F-RH-004)

Wave A residue (files with WARN-level open issues) + Wave B parked queue (files Refiner couldn't migrate) share ONE reconciliation queue. Disposition options:

| Disposition                 | Action                                                                                                |
| --------------------------- | ----------------------------------------------------------------------------------------------------- |
| `keep-as-is`                | File stays valid at lower tier (e.g., open-standard but not IS-marketplace); recorded in coverage map |
| `manual-migrate`            | Engineer manually edits; file lands in next batch                                                     |
| `deprecate-skill`           | Skill marked for removal in next CCP minor; consumers warned                                          |
| `schema-revision-candidate` | Routed to § 14.A.3 queue; schema may need revision                                                    |

Reconciliation queue dispositions are reviewed monthly at SAK cadence (§ 14.13.2 AAR cadence).

### 14.17 — Beads

- `iaj-refiner-wave-b-durability` (P1) — implement per-file-branch + 3-retry + parked-queue
- `iec-E11-reconciliation-queue` (P1) — author queue schema + disposition workflow

---

## § 14.18 (NEW, T1 resolution) — Decompose-first vs test-first ordering

Per audit T1 resolution: "Adopt BOTH in sequence — write the test corpus as Phase 1 sub-deliverable (Beck), then use the test failures to drive decomposition before Phase 2 (Hickey)."

### 14.18.1 — Sequence

| Order | Sub-phase | Deliverable                                                             | Exit gate                                        |
| ----- | --------- | ----------------------------------------------------------------------- | ------------------------------------------------ |
| 1     | Phase 1.0 | 6 schemas shipped with v6 framing (single `$defs.isMarketplace`)        | Schemas exist + lint                             |
| 2     | Phase 1.1 | Test corpus authored (≥ 30 fixtures per schema = ~180 fixtures)         | Fixtures committed                               |
| 3     | Phase 1.2 | Schemas validated against fixtures; failures surface complecting issues | Failure report drafted                           |
| 4     | Phase 1.5 | Schemas DECOMPOSED per § 14.10 REVISED in response to test failures     | 4-fold `$defs` structure in place; fixtures pass |
| 5     | Phase 2   | Validator cutover proceeds against the decomposed schemas               | Per v6 § 14.4 Phase 2                            |

**Beck's "test-first lights the way" and Hickey's "decompose before locking in" both honored in sequence.** Cost: ~2 weeks added to Phase 1 (per audit synthesis estimate). Acceptable.

### 14.18 — Beads

- `iec-E11-fixtures-discipline` (P0, expanded scope) — author the 180-fixture corpus per Phase 1.1
- `iec-E11-decomp-via-failure` (P0) — Phase 1.5 work: use test failures to drive `$defs.isMarketplace` 4-fold decomposition

---

## § 14.19 (NEW, closes F-MK-006) — Conditional-visibility referential integrity

The IS-extras `requires_env: [X]` + `required_environment_variables: [{name: X, ...}]` cross-reference (per CCP schema 3.6.0):

**Referential-integrity rule:** for every value `X` in `requires_env`, there MUST exist exactly one entry in `required_environment_variables` with `name: X`. Missing = ERROR; duplicate = ERROR.

Symmetrically for `requires_tools` ↔ `metadata.intent-solutions.config[*].required_for`.

### 14.19 — Bead

- `iec-E11-conditional-visibility-integrity` (P2) — implement the cross-field check in `$defs.isMarketplace.requiredFields`

---

## § 14.20 REVISED (closes F-CH-005) — Phase 5 explicit risk acknowledgement

v6 § 14.4 Phase 5 (weeks 17-18) ships 5 blocking gates for the remaining authoring contracts. Per F-CH-005, this is an implicit-low-risk assumption — 5 contracts in 2 weeks against the same corpus that needed 6 weeks of Phase 4 work.

**Revised disposition:** Phase 5 is bandwidth-gated. Each of the 5 remaining contracts (plugin-manifest, agent-definition, mcp-config, hook-config, marketplace-catalog) gets its own Phase 5a / 5b / 5c / 5d / 5e mini-phase with the SAME state-machine + shadow + rollback discipline as Phase 4 (per § 14.4 REVISED).

Phase 5 calendar budget: weeks 17-26 (NOT 17-18), assuming 1.5-2 weeks per sub-phase. Total Phase 5 = 10 weeks worst-case.

**Bandwidth coupling:** if Phase 4 stalls (per § 14.4.cost ceiling firing), Phase 5 inherits the stall.

### 14.20 — Bead

- `iec-E11-phase-5-decompose` (P1) — REVISE § 14.4 Phase 5 row to reflect 5a-5e structure; integrate into § 14.13 dashboard

---

## § 14.21 (NEW, closes C2 / F-KB-002) — Phase 1 test corpus discipline

Per audit synthesis: "Add a Phase 1 sub-deliverable: `intent-eval-core/tests/authoring/v1/fixtures/` with golden positive + negative + edge-case corpora for each of the 6 schemas. Minimum 30 fixtures per schema (~180 total)."

### 14.21.1 — Fixture composition (per schema)

| Class                                 | Count  | Purpose                                                                         |
| ------------------------------------- | ------ | ------------------------------------------------------------------------------- |
| Positive (canonical)                  | 10     | Clear-PASS examples; common author shapes                                       |
| Positive (edge)                       | 5      | Pass-but-uncommon shapes (e.g., minimum-required-only)                          |
| Negative (each required field absent) | 8      | Per the 8-required-fields set; one fixture per omission                         |
| Negative (type errors)                | 5      | Wrong type for `version` (number instead of string), etc.                       |
| Negative (constraint violation)       | 5      | `name` with uppercase; `description` > 1024 chars; etc.                         |
| Edge (Anthropic spec ambiguity)       | 5      | Cases where 6767-h is silent; intentional under-spec to surface schema judgment |
| Edge (frontier-model-generated)       | 2      | Real Claude-generated SKILL.md examples; future-proof against frontier shapes   |
| **Total per schema**                  | **40** | (Audit said 30 minimum; rounded up to 40 for headroom)                          |

Total corpus: 240 fixtures. Lives at `intent-eval-core/tests/authoring/v1/fixtures/<schema>/{positive,negative,edge}/`.

### 14.21.2 — Test harness

Each fixture is a YAML or JSON file. Test harness:

- For positive fixtures: `valid_C(fixture, isMarketplace)` MUST return TRUE
- For negative fixtures: `valid_C(fixture, isMarketplace)` MUST return FALSE with the specific predicate sub-conjunct flagged
- For edge fixtures: documented expected behavior; test asserts the documented behavior

### 14.21 — Bead

- `iec-E11-fixtures-discipline` (P0, full scope per § 14.21) — author 240 fixtures + test harness

---

## § 14.22 (NEW, closes F-KB-006) — Kernel-bump propagation to Refiner

When kernel `$schemaVersion` bumps (per § 14.15), the Refiner's accept() predicate may change semantics. Mitigation:

- `@j-rig/refiner-core` declares its consumed kernel version in `package.json` peerDependencies
- Refiner runs emit a `kernel_schema_version_at_run` field in every ScoreRecord
- Kernel-version bumps re-trigger eval-loop runs for any open Refiner work (re-baseline on new kernel)
- Refiner runs that span a kernel bump are MARKED with a `pre-bump-baseline-superseded` flag

### 14.22 — Bead

- `iaj-refiner-kernel-bump-propagation` (P1) — implement kernel-version pinning + re-baseline trigger

---

## § 14.23 (NEW, closes F-CH-004) — Phase A.0 judge change isolation

Phase A.0 (D28-PHASE-A0 baseline per DR-028) uses `/validate-skillmd` as judge. Per F-CH-004, if the judge changes (e.g., D4 patch lands during baseline; future kernel cutover changes validation semantics), the baseline is invalidated.

**Isolation discipline:**

- Phase A.0 pins judge version at baseline start (e.g., `validate-skills-schema.py@SCHEMA-3.7.0`)
- Baseline runs against pinned judge regardless of subsequent judge bumps
- When judge bumps, Phase A.0 results carry the pinned-judge annotation
- A new Phase A.0 (vNext) is initiated for the new judge; old + new compared

### 14.23 — Bead

- `iaj-phase-a0-judge-pin` (P1) — implement judge-version pinning in baseline run config

---

## § 14.24 (NEW, closes F-KB-003) — D4 ↔ kernel duplicate-position reconciliation

The D4 patch (CCP commit ca0ca57bf) adds `disallowed-tools` to `validate-skills-schema.py` BEFORE the kernel exists. Per F-KB-003, this creates a duplicate canonical position: the kernel's eventual `skill-frontmatter.schema.json` will ALSO encode this field.

**Reconciliation in Phase 2 (validator cutover):**

- When Phase 2 cuts CCP validator over to kernel-loaded schema, the CCP-side `SKILL_FIELDS` entry for `disallowed-tools` becomes shadow-only (loaded from kernel, no longer hand-authored)
- D4's hand-authored entry is retained as comment for migration audit trail; actual validation comes from kernel
- CCP `SCHEMA_VERSION` bumps to declare which kernel `$schemaVersion` it consumes (per § 14.15)

### 14.24 — Bead

- `ccp-d4-kernel-cutover` (P1) — implement the Phase 2 D4 cutover; preserve `disallowed-tools` semantics

---

## § 14.25 (NEW, closes F-AK-006) — YAML shell-substitution FP/FN measurement

The validator's YAML shell-substitution security check (one of `$defs.isMarketplace.securityChecks`) currently has no false-positive / false-negative measurement.

**Measurement protocol:**

- Build a curated corpus of 100 SKILL.md fixtures: 50 with legitimate `${VAR}` usage from allow-list; 50 with malicious patterns
- Run the check; measure FP rate (legitimate flagged) + FN rate (malicious missed)
- Target: FP < 2%; FN < 5%; baseline lands at Phase 1.1 fixture authoring
- Quarterly re-measurement per § 14.13.3 CI gate cadence

### 14.25 — Bead

- `iec-E11-shell-sub-measurement` (P2) — author corpus + measurement harness

---

## § 14.26 (NEW, closes F-AK-005) — `_vendor/anthropic/` bump policy

Vendored upstream snapshots at `intent-eval-core/schemas/authoring/v1/_vendor/anthropic/` carry `x-upstream-url` + `x-upstream-fetched-at` + `x-upstream-sha256`.

**Bump policy:**

- Daily cron polls each `x-upstream-url`
- New sha256 detected → opens auto-PR with the new snapshot, diff vs prior, and recommended `$schemaVersion` impact (additive / breaking)
- Auto-PR is human-merged; never auto-merged (per CTO-call discipline)
- PR review by kernel maintainer + (if breaking) governance triple
- Snapshot bump and kernel schema bump may be DECOUPLED — snapshot can refresh without forcing schema bump if the upstream change is purely textual / additive

### 14.26 — Bead

- `iec-E11-vendor-bump-policy` (P2) — implement daily-cron + auto-PR workflow

---

## § 14.27 (NEW, closes F-RH-005) — "Read-only" ambiguity resolution

v6 § 14.4 Phase 1 says "kernel authoring/v1 ships read-only." Per F-RH-005, three distinct invariants are compressed:

| Invariant                         | Statement                                                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Read-only-immutable**           | Kernel `authoring/v1/` schemas are NEVER mutated after publication. Bumps create `authoring/v2/`, not edits to v1.          |
| **Read-only-no-consumer-cutover** | Phase 1 ships schemas but NO consumer cuts over to them. Validators continue using CCP-side `SCHEMA_VERSION` until Phase 2. |
| **Read-only-internal-test**       | Phase 1 schemas may be exercised by internal kernel test harness; not by external consumers.                                |

§ 14.4 Phase 1 text uses these three named invariants explicitly. v6's compressed "read-only" framing is replaced.

### 14.27 — Bead

- `iec-E11-read-only-invariants` (P2) — patch v6 § 14.4 Phase 1 wording

---

## § 14.28 (NEW, closes C5 / F-WC-002 / F-WC-006) — Documentation singularity strategy

Per audit's C5 + Cunningham's repeated reader-cost concern.

### 14.28.1 — Single canonical entry point

`intent-eval-lab/000-docs/SAK-INDEX.md` (NEW, ≤ 2 pages) — the canonical entry. Structure:

````markdown
# SAK Index

## What

Spec Authority Kernel — kernel-canonical authoring schemas for 6 contracts.

## Why

[2-3 sentences. Link to plan 031 § 14.1]

## Status

[Current phase; current state; link to SAK-DASHBOARD.md]

## Where things live

| Concern         | Path                                                          |
| --------------- | ------------------------------------------------------------- |
| Plan amendment  | 031 (v6 intro) + 033 (v7 audit-closure)                       |
| Charter         | 032 (DRAFT — deferred)                                        |
| Audit synthesis | audit/2026-05-28-sak-incremental-audit/synthesis.md           |
| Governance      | NNN-AT-STND-sak-governance-owners.md                          |
| Dashboard       | SAK-DASHBOARD.md (auto-generated)                             |
| Kernel schemas  | intent-eval-core/schemas/authoring/v1/                        |
| Coverage map    | intent-eval-core/schemas/authoring/v1/6767h-coverage-map.json |
| 6767-h prose    | claude-code-plugins/000-docs/6767-h-\*.md                     |
| Beads (filter)  | bd list --label sak --label refiner                           |

## Read order (for engineers)

1. SAK-INDEX.md (this file)
2. SAK-DASHBOARD.md (current state)
3. Plan 031 § 14 (architecture)
4. Plan 033 v7 amendment (this file's sibling-rationale)

## Read order (for ISEDC seats)

1. SAK-INDEX.md
2. 032 charter draft
3. audit synthesis

```text

### 14.28.2 — Dual changelog consolidation (F-WC-006)

v6 § 14.10 said CCP `SCHEMA_CHANGELOG.md` is "DUAL-MAINTAINED" with kernel `schemas/authoring/v1/CHANGELOG.md`. v7 collapses:

- Kernel `CHANGELOG.md` is the canonical changelog for `authoring/v1/`
- CCP `SCHEMA_CHANGELOG.md` retains its CCP-validator-specific entries; for kernel-authored entries, it cites `kernel CHANGELOG.md $sectionRef` instead of duplicating

### 14.28 — Beads

- `iel-sak-summary-doc` (P1) — author `SAK-INDEX.md`
- `iec-E11-changelog-singularity` (P1) — implement the dual→single changelog discipline

---

## § 14.29 (NEW) — Remediation bead inventory (~26 new beads to file)

Per audit remediation map. Filed in companion action with appropriate labels (`refiner`, `sak`, `audit-remediation`, `repo:<short>`):

| #   | Slug                                     | Priority | Repo label | Closes                  |
| --- | ---------------------------------------- | -------- | ---------- | ----------------------- |
| 1   | iec-E11-phase-4-decompose                | P0       | iec        | C1 / F-KB-001           |
| 2   | iec-E11-phase-4b-5-shadow-mode           | P0       | iec        | C1 / F-CH-001           |
| 3   | iec-E11-phase-4-state-machine            | P0       | iec        | C1                      |
| 4   | iec-E11-phase-4-snapshot-rules           | P0       | iec        | F-MK-005                |
| 5   | iec-E11-phase-4c-rollback-protocol       | P0       | iec        | F-KB-004                |
| 6   | iaj-refiner-cost-instrument              | P0       | iaj        | F-AK-004                |
| 7   | iec-E11-fixtures-discipline              | P0       | iec        | C2 / F-KB-002           |
| 8   | iel-schema-policy-eval                   | P0       | iel        | C2                      |
| 9   | iec-E11-valid-predicate-spec             | P0       | iec        | T3 / § 14.A             |
| 10  | iec-E11-cross-schema-invariants          | P0       | iec        | § 14.B / F-LL-002       |
| 11  | iec-E11-coverage-map                     | P0       | iec        | C3 / F-RH-002 / § 14.2  |
| 12  | iec-E11-decomp                           | P0       | iec        | C3 / F-RH-001 / § 14.10 |
| 13  | iec-E11-anthropic-leading-indicators     | P0       | iec        | T2 / F-AK-001           |
| 14  | iec-E11-governance-owners                | P1       | iel        | C4 / § 14.12            |
| 15  | iel-ci-gate-cadence                      | P1       | iel        | F-WC-001                |
| 16  | iel-sak-dashboard                        | P1       | iel        | F-WC-005 / § 14.13      |
| 17  | iel-sak-summary-doc                      | P1       | iel        | C5 / § 14.28            |
| 18  | iec-E11-changelog-singularity            | P1       | iec        | F-WC-006                |
| 19  | iaj-refiner-schema-boundary              | P1       | iaj        | F-AK-003                |
| 20  | iec-E11-kernel-vendor-consistency-model  | P0       | iec        | F-MK-001 / § 14.15      |
| 21  | iaj-refiner-wave-b-durability            | P1       | iaj        | F-MK-004 / § 14.17      |
| 22  | iec-E11-port-not-delete-playbook         | P1       | iec        | T2 / § 14.14            |
| 23  | iec-E11-prose-anchor-parser              | P0       | iec        | F-KB-005 / § 14.16      |
| 24  | iec-E11-prose-schema-liveness            | P1       | iec        | F-LL-005                |
| 25  | iec-E11-reconciliation-queue             | P1       | iec        | F-RH-004                |
| 26  | iaj-refiner-kernel-bump-propagation      | P1       | iaj        | F-KB-006                |
| 27  | iaj-phase-a0-judge-pin                   | P1       | iaj        | F-CH-004                |
| 28  | ccp-d4-kernel-cutover                    | P1       | ccp        | F-KB-003                |
| 29  | iec-E11-shell-sub-measurement            | P2       | iec        | F-AK-006                |
| 30  | iec-E11-vendor-bump-policy               | P2       | iec        | F-AK-005                |
| 31  | iec-E11-read-only-invariants             | P2       | iec        | F-RH-005                |
| 32  | iec-E11-conditional-visibility-integrity | P2       | iec        | F-MK-006                |
| 33  | iec-E11-is-extras-categorize             | P2       | iec        | F-RH-006                |
| 34  | iec-E11-phase-5-decompose                | P1       | iec        | F-CH-005 / § 14.20      |
| 35  | iec-E11-decomp-via-failure               | P0       | iec        | T1 / § 14.18            |
| 36  | iec-E11-version-ordering-invariant       | P1       | iec        | F-MK-003                |

36 total (revised from audit's ~25 estimate — granularity of the C1/C2/C3 remediations expanded). 13 P0, 14 P1, 9 P2. All gated on plan 033 v7 re-audit closing the P0 cluster.

---

## § 14.30 (NEW) — Re-audit gating

v7 re-audit (incremental on v7 deltas only) fires when:

1. v7 is committed + pushed to feat branch (allows panel access)
2. Updated brief pack at `audit/2026-05-28-sak-incremental-audit/brief-pack/` (add `06-plan-033-v7-amendment.md` symlink)
3. 7-seat panel re-runs per same methodology
4. New findings file per seat at `audit/2026-05-28-sak-incremental-audit/findings/<seat>-v7-findings.md`
5. Synthesis appended as `synthesis-v7-addendum.md`
6. STATUS.md updates based on v7 findings:
   - 0 new P0s → RATIFIED-WITH-DELTAS (the original 17 P1 + 13 P2 remain)
   - 1-3 new P0s → NEEDS-AMENDMENT-V8 (plan 034 drafts)
   - > 3 new P0s → STRUCTURAL-REJECT (re-think SAK scope; may revert to single-contract-at-a-time)

### 14.30.1 — Re-audit scope discipline

The re-audit reviews ONLY:

- v7 amendment doc (THIS doc, 033)
- NEW sub-sections (§ 14.A, § 14.B, § 14.12-14.28)
- REVISED sub-sections (§ 14.2, § 14.4, § 14.10, § 14.11, § 14.20)
- NEW remediation bead inventory (§ 14.29)

The re-audit does NOT re-evaluate:

- §§ 1-13 (ratified per DR-028)
- v6 sub-sections that v7 didn't touch
- Findings already closed by v6→v7 deltas (verify closure only)

### 14.30 — No new bead; tracked in `bd_000-projects-8vq0` (charter bead) lifecycle

---

## Bottom line

v7 closes the 12 P0 cluster from the 2026-05-28 incremental audit via:

- **C1 (Phase 4)**: decomposed into 4a/4b/4b.5-shadow/4c with state machine + shadow + rollback + cost ceiling
- **C2 (schemas-as-policy)**: § 14.A formal predicate co-located in `$comment` + § 14.B cross-schema invariants + § 14.21 240-fixture test corpus
- **C3 (bicameral architecture)**: § 14.2 REVISED 3-named-values + § 14.10 REVISED 4-fold `$defs` decomposition + coverage-map artifact
- **C4 (governance + cadence)**: § 14.12 named seat-bound owners + § 14.13 dashboard + 90-day CI cadence
- **C5 (doc sprawl)**: § 14.28 documentation singularity + dual→single changelog
- **T1 (decompose vs test first)**: § 14.18 Phase 1.0 → 1.1 → 1.2 → 1.5 → 2 ordering
- **T2 (bitter-lesson vs invest)**: § 14.11 EXPANDED + § 14.14 port-not-delete
- **T3 (formal predicate vs evolving doc)**: § 14.A co-located in `$comment`
- **T4 (implicit vs explicit upstream-divergence)**: § 14.10.ext IS-extras catalog with triggers

Plus 17 individual P1/P2 patches per § 14 cross-reference index.

36 new remediation beads to file in companion action.

Re-audit on v7 deltas → if 0 new P0s, STATUS flips RATIFIED-WITH-DELTAS → ISEDC Class-1 charter (032) convenes → SAK Phase 1 ships.

## Stopping criteria for v7 itself

- v7 re-audit returns ≥ 1 new P0 → NEEDS-AMENDMENT-V8 (plan 034)
- v7 re-audit returns > 3 new P0s → STRUCTURAL-REJECT; revert to per-contract-at-a-time (skill-frontmatter first; 5 contracts deferred)
- Re-audit reveals v6 sub-section that v7 thought was closed is actually still open → re-fire v7 amendment authoring before re-audit
- Anthropic leading indicator CRITICAL fires during v7 drafting → STOP SAK; defer 032 charter indefinitely; archive v6 + v7 as historical IS contribution

## Status banding

**PROPOSED-FOR-REAUDIT** — pending:

- v7 re-audit per § 14.30
- Outcome flips STATUS to RATIFIED-WITH-DELTAS (success) or NEEDS-AMENDMENT-V8 / STRUCTURAL-REJECT (failure)
- 36 remediation beads filed (companion action; can proceed in parallel with re-audit)
- ISEDC Class-1 charter (032) convenes only after RATIFIED-WITH-DELTAS

— Jeremy Longshore
intentsolutions.io
```
````
