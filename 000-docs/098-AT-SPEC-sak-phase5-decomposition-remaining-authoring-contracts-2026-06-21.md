---
title: SAK Phase-5 decomposition — 5a / 5b / 5c / 5d / 5e, one per remaining authoring contract (funding-gated)
category: AT-SPEC
status: NORMATIVE (decomposition + sequencing only — NOT authorization to build)
date: 2026-06-21
authority: plan 033 v7 § 14.20 REVISED + § 14.B; plan 048 v8; DR-044 D7 / ID-8; DR-049 (CFO binding)
bead: bd_000-projects-bt75
epic: bd_000-projects-3kye (SAK)
---

# SAK Phase-5 decomposition — the five remaining authoring contracts

**Status: NORMATIVE — but this is a DECOMPOSITION + SEQUENCING plan, NOT authorization to
build.** This doc decomposes SAK Phase-5 (the rollout of the **five remaining authoring
contracts** beyond the `skill-frontmatter` walking skeleton) into its five named sub-phases —
**5a** (plugin-manifest) / **5b** (agent-definition) / **5c** (mcp-config) / **5d**
(hook-config) / **5e** (marketplace-catalog) — per plan 033 v7 § 14.20 REVISED, with the
cross-schema dependency edges of plan 033 § 14.B and the lifecycle + flip discipline of plan
048 v8 + doc 097.

It is the structural counterpart to doc 097 (the Phase-4 decomposition → implementation map):
where 097 mapped four **already-built** sub-phases to the machinery that landed this sprint,
this doc decomposes five sub-phases that are **NOT built and NOT authorized to build** — each
one is **FUNDING-GATED** on its own per-contract CFO sign-off (DR-044 D7 / ID-8, re-bound by
DR-049) before any bead under it may be claimed.

## The charter constraint — read this before anything else

**The six authoring contracts do NOT ship as one capital outlay.** Only contract #1
(`skill-frontmatter`, the walking skeleton) is funded to `PUBLISHED`. Contracts 2–6 — the five
this doc decomposes — are sequenced **on-demand, each behind its own lightweight CFO bandwidth
sign-off**, not a single batch authorization and not a new ISEDC convening per contract.

| Binding                      | Source                                                         | What it says                                                                                                                                                                                                                                                                                                                                     |
| ---------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **DR-044 D7**                | `044-AT-DECR-...session-8-sak-charter-2026-06-09.md`           | RATIFY the composition model; **"authoring is sequenced — skill-frontmatter first, the remaining five on-demand behind a lightweight CFO bandwidth sign-off (not a new ISEDC convening)."**                                                                                                                                                      |
| **DR-044 ID-8**              | same                                                           | Action item: "Author the 6 per-contract schemas — skill-frontmatter first; **the other 5 on-demand behind a lightweight CFO sign-off** (D7)." Owners: CTO + CFO. The six per-contract beads are unblocked **for sequencing**, NOT for simultaneous authoring.                                                                                    |
| **DR-049 (CFO binding)**     | `049-AT-DECR-isedc-class-1-charter-ratification-2026-06-10.md` | "only skill-frontmatter is funded to PUBLISHED now; **contracts 2-6 stay in DRAFT/SHIPPED-INTERNAL and each one's promotion requires my per-contract FTE-day estimate + sign-off per DR-044 ID-8**, with the estimate logged against the bandwidth model before any bead is claimed. No contract crosses into PUBLISHED without that line item." |
| **plan 033 § 14.20 REVISED** | `033-PP-PLAN-...v7-2026-05-28.md`                              | Phase 5 is **bandwidth-gated**. Each of the five remaining contracts gets its own 5a–5e mini-phase "with the SAME state-machine + shadow + rollback discipline as Phase 4." Bandwidth coupling: if Phase 4 stalls (§ 14.4.cost ceiling firing), Phase 5 inherits the stall.                                                                      |

**Therefore: NO sub-phase in this doc is authorized to build.** Each is `FUNDING-GATED` — its
"authorized to start" precondition is a per-contract CFO FTE-day estimate + sign-off logged
against the bandwidth model (`029-DR-BAND-...md`). This doc plants the decomposition and the
sequence so that, when a contract's sign-off lands, its build inherits a ready plan — it does
**not** itself unblock any bead.

## Source-of-truth pointers

| Layer                                                              | Where                                                                                                                           |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Phase-5 5a–5e definition + bandwidth gate                          | plan 033 v7 § 14.20 REVISED (`033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md`)                                        |
| Cross-schema dependency edges + invariant catalog                  | plan 033 v7 § 14.B (`033-...v7...md`)                                                                                           |
| Funding gate (per-contract CFO sign-off)                           | DR-044 D7 / ID-8 (`044-...session-8-sak-charter...md`); DR-049 CFO binding (`049-...charter-ratification...md`)                 |
| Lifecycle states (DRAFT / SHIPPED-INTERNAL / PUBLISHED)            | plan 048 v8 § 14.31 (`048-PP-PLAN-skill-refiner-sak-amendment-v8-2026-06-10.md`)                                                |
| State-machine / shadow / rollback discipline (inherited)           | doc 097 + the built machinery: 092 (flip state machine) / 093 (rollback) / 094 (reconciliation queue) / 095 (Wave-B durability) |
| Bandwidth model (where each sign-off's FTE-day estimate is logged) | `029-DR-BAND-skill-refiner-bandwidth-model-2026-05-27.md`                                                                       |

## Sub-phase → contract → depends-on → gate-status summary

The ordering below is plan 033 § 14.20 REVISED's enumeration. **Build sequencing** (the
`Depends on` column) is NOT that enumeration order — it is the cross-schema dependency graph of
§ 14.B: a contract that another contract's invariants descend into should ship first so the
descent target exists. Every sub-phase is `FUNDING-GATED`.

| Sub-phase | Contract              | Depends on (build-sequencing rationale)                                                                                                                                                                                              | Gate status                            |
| --------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| **5a**    | `plugin-manifest`     | `skill-frontmatter` (contract #1, PUBLISHED) — INV-PLUGIN-SKILL descends `plugin-manifest` → `skill-frontmatter`. Recommended **first of the five**: it is the container three other contracts and the catalog all reference.        | **FUNDING-GATED** — not yet authorized |
| **5b**    | `agent-definition`    | `plugin-manifest` (5a) — INV-PLUGIN-AGENT descends `plugin-manifest` → `agent-definition`; the per-agent descent needs the container contract present.                                                                               | **FUNDING-GATED** — not yet authorized |
| **5c**    | `mcp-config`          | `plugin-manifest` (5a) — INV-PLUGIN-MCP descends `plugin-manifest` → `mcp-config`. Independent of 5b (agents and MCP servers are sibling descents).                                                                                  | **FUNDING-GATED** — not yet authorized |
| **5d**    | `hook-config`         | `mcp-config` (5c) for INV-MCP-HOOK (`mcp-config` with hook-bindings → `hook-config`); also referenced by `skill-frontmatter` (INV-SKILL-HOOK, contract #1) and `plugin-manifest` (§ 14.B.1 "refers-to via plugin.json hooks block"). | **FUNDING-GATED** — not yet authorized |
| **5e**    | `marketplace-catalog` | `plugin-manifest` (5a) — INV-CAT-PLUGIN descends `marketplace-catalog` → `plugin-manifest`. Recommended **last of the five**: it is the top of the cross-reference graph (`--deep` walks every plugin source).                       | **FUNDING-GATED** — not yet authorized |

**Reading the two orderings.** The plan's 5a–5e _labels_ are fixed (§ 14.20 REVISED names them
in that order, and this doc preserves that mapping verbatim). The _build dependency_ graph is a
DAG, not a line: `5a` (plugin-manifest) is the keystone — `5b`, `5c`, and `5e` all descend into
it, so it builds first; `5d` (hook-config) sits below `5c` (mcp-config) via INV-MCP-HOOK; `5e`
(marketplace-catalog) sits at the top via INV-CAT-PLUGIN, so it builds last. A topological
build order consistent with both is **5a → {5b, 5c} → 5d → 5e**. The label order and the build
order are NOT in conflict — the labels are a naming convention; the dependency edges are the
sequencing constraint. **All of it is moot until each contract's funding gate clears.**

---

## 5a — plugin-manifest

### Contract it ships

The `plugin-manifest` authoring contract: the formal predicate `valid_plugin-manifest(artifact,
tier)` for `plugin.json` — the IS-marketplace-tier composition over the universal folds (§ 14.10
4-fold decomposition: `requiredFields` / `deprecationRegistry` / `securityChecks` /
`disclosureMarkers`) with `plugin-manifest`-specific `requiredFields` overriding the
parameterizable base (DR-044 D7: each contract **overrides** `requiredFields`, **inherits** the
three universal folds).

### Dependency / sequencing

- **Depends on:** `skill-frontmatter` (contract #1, PUBLISHED). INV-PLUGIN-SKILL (§ 14.B.2):
  `∀ p ∈ plugin-manifest, ∀ s ∈ p.skills, valid_skill_frontmatter(s, isMarketplace)` — the
  per-skill descent target must already exist.
- **Recommended first of the five.** `plugin-manifest` is the container that `agent-definition`
  (5b), `mcp-config` (5c), and `marketplace-catalog` (5e) all reference; shipping it first means
  every later descent has its parent contract in place. The codegen pipeline is a **hard
  precondition** of contract #2 per DR-044 D8/ID-7 (contract #1 grandfathered; the factory is
  built for the second unit), so 5a is the sub-phase that first exercises the generated-validator
  path.

### State-machine discipline inherited (per plan 033 § 14.20 + doc 097)

Same as Phase-4: an advisory → shadow → ready-to-flip → blocking lifecycle with a rollback
off-ramp. Concretely, `plugin-manifest` re-uses the built machinery 1:1: the 092 flip state
machine (its `ADVISORY → … → SHADOW-MODE → READY-TO-FLIP → BLOCKING` graph with the (c)
zero-open-P0 + (d) governance-triple HARD gates and the (a) coverage calendar-dispositionable
gate), the 093 `kernel-gate-revert` rollback, the 094 reconciliation queue for residue, and the
095 Wave-B durability protocol. **No new state-machine is authored for Phase 5** — each contract
instantiates the Phase-4 control plane against its own corpus slice.

### Funding-gate status

**FUNDING-GATED — not yet authorized.** Build of 5a is blocked on a per-contract CFO FTE-day
estimate + sign-off (DR-044 ID-8 / DR-049), logged against the bandwidth model
(`029-DR-BAND`), before any 5a bead may be claimed. The composition spec is binding for all six
contracts (DR-044 D7), but authorization is per-contract. This doc does NOT supply that sign-off.

---

## 5b — agent-definition

### Contract it ships

The `agent-definition` authoring contract: `valid_agent-definition(artifact, tier)` for an
`agents/NAME.md` subagent file — the IS-marketplace 8-field overlay (the kernel-strict agent
contract: `name` / `description` / `tools` / `model` / `color` / `version` / `author` / `tags`,
plus the banned-field set) composed over the three universal folds with `agent-definition`-specific
`requiredFields`.

### Dependency / sequencing

- **Depends on:** `plugin-manifest` (5a). INV-PLUGIN-AGENT (§ 14.B.2): `∀ p ∈ plugin-manifest,
∀ a ∈ p.agents, valid_agent_definition(a, isMarketplace)` — the per-agent descent runs from
  the container contract, so 5a's contract must exist first.
- **Sibling of 5c.** Agents and MCP servers are parallel descents from `plugin-manifest`; 5b and
  5c have no edge between them and may be sequenced in either order (or in parallel) once 5a is
  funded and built.

### State-machine discipline inherited

Identical to 5a — the Phase-4 control plane (092 / 093 / 094 / 095) instantiated against the
agent-definition corpus slice. Advisory → shadow → ready-to-flip → blocking, with the
zero-open-P0 + governance-triple hard gates and the `kernel-gate-revert` rollback off-ramp.

### Funding-gate status

**FUNDING-GATED — not yet authorized.** Per-contract CFO sign-off (DR-044 ID-8 / DR-049)
required before any 5b bead may be claimed.

---

## 5c — mcp-config

### Contract it ships

The `mcp-config` authoring contract: `valid_mcp-config(artifact, tier)` for a `.mcp.json` (or a
`plugin.json` `mcpServers` block) — transport-specific required fields (stdio → `command`;
http/sse/ws → `url`), server-name uniqueness + kebab-case convention, and plaintext-credential
hygiene — composed over the universal folds with `mcp-config`-specific `requiredFields`.

### Dependency / sequencing

- **Depends on:** `plugin-manifest` (5a). INV-PLUGIN-MCP (§ 14.B.2): `∀ p ∈ plugin-manifest,
p.mcpServers[*] ⊨ valid_mcp_config` — the MCP descent runs from the container contract.
- **Precedes 5d.** INV-MCP-HOOK (§ 14.B.2): `∀ m ∈ mcp-config with hook-bindings,
valid_hook_config(m.hooks)` — `mcp-config`'s hook-binding descent needs `hook-config` (5d) to
  exist as a _target_, so the **invariant edge points 5c → 5d** and 5d should ship after 5c is in
  place. (5d also has independent referrers — see 5d below.)

### State-machine discipline inherited

Identical to 5a / 5b — Phase-4 control plane instantiated against the mcp-config corpus slice.
`securityChecks` is the universal-immutable fold here too: per DR-044 / DR-049 the
`securityChecks` conjuncts (e.g. plaintext-credential / `$(...)`-injection-adjacent patterns)
**block day-0, exempt from the shadow window** — RCE-adjacent checks do not get a grace period.

### Funding-gate status

**FUNDING-GATED — not yet authorized.** Per-contract CFO sign-off (DR-044 ID-8 / DR-049)
required before any 5c bead may be claimed.

---

## 5d — hook-config

### Contract it ships

The `hook-config` authoring contract: `valid_hook-config(artifact, tier)` for a `hooks/hooks.json`
(or hooks declared inline in `settings.json` / skill / agent frontmatter) — JSON validity, the
3-level event nesting, the event allowlist (PreToolUse, PostToolUse, SessionStart, Stop,
SubagentStop, PreCompact, UserPromptSubmit, …), per-handler required fields by handler type, and
matcher-regex validity (every matcher must compile) — composed over the universal folds with
`hook-config`-specific `requiredFields`.

### Dependency / sequencing

- **Depends on:** `mcp-config` (5c) via INV-MCP-HOOK (the edge points 5c → 5d). `hook-config` is
  also the descent target of **two contract-#1 / 5a referrers**: INV-SKILL-HOOK (§ 14.B.2,
  `∀ s ∈ skill-frontmatter with hooks block, valid_hook_config(s.hooks)` — already PUBLISHED) and
  the § 14.B.1 "`plugin-manifest` refers-to `hook-config` via plugin.json hooks block" edge. So
  `hook-config` has the most inbound invariant edges of the five and should ship after its
  referrers' container contracts (5a, 5c) are in place.
- **Precedes 5e only indirectly** (no direct catalog→hook edge; the catalog reaches hooks
  transitively through plugin-manifest).

### State-machine discipline inherited

Identical to the others — Phase-4 control plane instantiated against the hook-config corpus
slice, with the advisory → shadow → ready-to-flip → blocking lifecycle and the `kernel-gate-revert`
rollback. Hook matcher-regex validity and the PreToolUse exit-2 blocking-behavior contract
are deterministic checks (100% fold agreement required, no 0.5% tolerance band, per DR-049 CTO
binding).

### Funding-gate status

**FUNDING-GATED — not yet authorized.** Per-contract CFO sign-off (DR-044 ID-8 / DR-049)
required before any 5d bead may be claimed.

---

## 5e — marketplace-catalog

### Contract it ships

The `marketplace-catalog` authoring contract: `valid_marketplace-catalog(artifact, tier)` for a
`.claude-plugin/marketplace.json` — required top-level fields (`name` / `owner` / `plugins`
array), owner shape, per-plugin entries (required `name` + `source`; optional `description` /
`version` / `category` / `keywords` / `author`), and source-type handling (relative path /
github shorthand / full URL) — composed over the universal folds with
`marketplace-catalog`-specific `requiredFields`.

### Dependency / sequencing

- **Depends on:** `plugin-manifest` (5a). INV-CAT-PLUGIN (§ 14.B.2): `∀ catalog entry
e ∈ marketplace-catalog.plugins, plugin_manifest_resolves(e.source) ∧
valid_plugin_manifest(content_of(e.source), isMarketplace)` — the `validate-marketplace --deep`
  descent resolves each plugin source and validates it against `plugin-manifest`, so 5a's contract
  must be in place.
- **Recommended last of the five.** `marketplace-catalog` is the top of the § 14.B.1
  cross-reference graph (`marketplace-catalog ──cites──▶ plugin-manifest ──contains──▶
{skill-frontmatter, agent-definition, mcp-config} …`). Shipping it last means its `--deep` walk
  has every descent target already authored, and the full invariant chain is enforceable end-to-end.

### State-machine discipline inherited

Identical to the others — Phase-4 control plane instantiated against the marketplace-catalog
corpus slice. Because 5e's `--deep` mode is the integration point that exercises every other
contract's invariants transitively, its shadow-mode dual-validator window is where cross-contract
deviation (a catalog that passes but whose descended plugin/skill/agent fails) surfaces.

### Funding-gate status

**FUNDING-GATED — not yet authorized.** Per-contract CFO sign-off (DR-044 ID-8 / DR-049)
required before any 5e bead may be claimed.

---

## End-to-end flow (5a → 5e) with the shared state-machine discipline + per-contract funding gate

The diagram below shows the two layers that govern Phase-5: (1) the **build-dependency DAG**
(the § 14.B invariant edges — what must precede what) and (2) the **per-contract funding gate**
that sits in front of EVERY sub-phase before its shared Phase-4 state-machine even begins.
`[GATED]` = not authorized to build; the CFO sign-off in front of each sub-phase is the
authorization precondition. The state-machine lane (advisory → shadow → ready-to-flip →
blocking + rollback) is the SAME machinery for all five — it is drawn once and inherited
per-sub-phase.

```text
                       ┌──────────────────────────────────────────────────────────┐
                       │  PER-CONTRACT FUNDING GATE (DR-044 D7/ID-8 · DR-049)       │
                       │  CFO FTE-day estimate + sign-off, logged vs 029-DR-BAND,   │
                       │  REQUIRED before ANY bead under a sub-phase may be claimed. │
                       │  NOT a new ISEDC convening — a lightweight per-contract     │
                       │  bandwidth line item. One gate per sub-phase below.        │
                       └──────────────────────────────────────────────────────────┘
                                              │ (each sub-phase passes its own gate)
                                              ▼
  contract #1: skill-frontmatter  ── PUBLISHED (walking skeleton; the only funded-to-PUBLISHED contract)
       │  INV-PLUGIN-SKILL descends into it
       ▼
  ┌───────────────────────┐
  │ 5a  plugin-manifest   │ [GATED]  ◀── keystone: 5b, 5c, 5e all descend into it
  │  (container contract) │
  └───────┬───────┬───────┘
   INV-   │       │  INV-CAT-PLUGIN
   PLUGIN-│       └──────────────────────────────────┐
   AGENT  │  INV-PLUGIN-MCP                           │
          ▼       ▼                                   │
  ┌───────────────┐  ┌───────────────┐                │
  │ 5b agent-     │  │ 5c mcp-config │ [GATED]        │
  │   definition  │  │  (sibling of  │                │
  │   [GATED]     │  │   5b)         │                │
  └───────────────┘  └───────┬───────┘                │
                     INV-MCP-HOOK                      │
                             ▼                         │
                     ┌───────────────┐                 │
                     │ 5d hook-config│ [GATED]         │
                     │ (also referred│                 │
                     │  by #1 + 5a)  │                 │
                     └───────────────┘                 │
                                                       ▼
                                              ┌──────────────────────┐
                                              │ 5e marketplace-      │ [GATED]
                                              │    catalog           │  ◀── top of graph;
                                              │ (--deep walks all)   │      ships last
                                              └──────────────────────┘

  topological build order (consistent with all edges):  5a → {5b, 5c} → 5d → 5e
  (plan 033 § 14.20 label order is 5a/5b/5c/5d/5e — preserved verbatim above)

  ── inherited per sub-phase, once its funding gate clears (the SAME Phase-4 machinery, docs 092–095/097) ──

   ADVISORY ──▶ ADVISORY-W-A ──▶ ADVISORY-W-AB ──▶ SHADOW-MODE ──▶ READY-TO-FLIP ──▶ BLOCKING
   (advisory)   (Wave A)         (both waves)      (dual-          [HARD: (c)         (flip
        │                                           validator)      zero-open-P0 +     complete)
        │                                              │            (d) gov-triple;        │
        │                                              ▼            (a) coverage           │
        │                                          HOLDING          calendar-              │
        │                                          (audit;          dispositionable]       │
        │                                           never flips                            │
        │                                           direct to                              │
        │                                           BLOCKING)                              │
        ▼                                                                                  ▼
   ROLLED-BACK ◀──────────────────── regression-detected (kernel-gate-revert, gov-triple, +7d ISEDC Class-2)
   (back-to-shadow re-try)           ── plus Wave-A class-1 / Wave-B class-2 rollbacks per § 14.4.rollback
```

**Two gates, in series.** Each sub-phase passes TWO gates before it can flip to `BLOCKING`:
first the **per-contract funding gate** (CFO sign-off — the authorization to build at all),
then, after build, the **Phase-4 flip gate** (the (c) zero-open-P0 + (d) governance-triple HARD
gates inherited from 092). The funding gate is what makes Phase-5 a _plan_ and not a build:
none of the five has passed it.

## Honest bottom line

- **This doc DECOMPOSES; it does NOT authorize.** The 5a–5e → contract mapping, the cross-schema
  build-dependency DAG, and the inherited state-machine discipline are now on the record so that
  when a contract's CFO sign-off lands, its build starts from a ready plan. **No bead under any
  sub-phase is unblocked by this doc.**
- **Every sub-phase is FUNDING-GATED.** Contracts 2–6 stay in DRAFT / SHIPPED-INTERNAL until a
  per-contract CFO FTE-day estimate + sign-off (DR-044 D7 / ID-8, DR-049) is logged against the
  bandwidth model. No contract crosses into PUBLISHED without that line item, and authorization is
  per-contract — never a batch, never a new ISEDC convening per contract.
- **No new control plane is built for Phase-5.** Each sub-phase instantiates the Phase-4 state
  machine + rollback + reconciliation-queue + Wave-B durability (docs 092–095, mapped in 097)
  against its own corpus slice. Phase-5 reuses the control plane; it does not re-author it.
- **Bandwidth coupling stands (§ 14.20):** if Phase-4 stalls (the § 14.4.cost ceiling firing),
  Phase-5 inherits the stall — another reason the gate is per-contract and on-demand, not a
  committed roadmap clock.

The Phase-5 _decomposition_ exists; the Phase-5 _authorization_ does not. Each sub-phase waits on
its own CFO sign-off before a single bead is claimed.

— Jeremy Longshore
intentsolutions.io
