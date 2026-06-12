---
date: 2026-06-12
status: ADJUDICATED — acting-CTO ruling under explicit owner delegation. All 27 tier-3 reconciliation findings dispositioned; implementation lands as kernel authoring/v2 for five contracts.
class: Class-2 acting-CTO adjudication (tier-3 reconciliation queue), NOT a 7-seat ISEDC convening
author: Jeremy Longshore (acting CTO — Claude per explicit owner delegation, "make the decisions, you are CTO", 2026-06-12)
basis: docs 056/058/059/060/061 kernel cross-check findings (the standing tier-3 queue per 061 § program completion); promotion-is-human rule per 052-AT-SPEC; projections at specs/_vendor/upstream/<contract>/projection.json
relates: DR-049 (authoring/v1 read-only-immutable; v2-never-edits-v1), 045-RR-LAND (SSoT declaration), DR-044 D7 (base+overlay walking skeleton)
---

# Tier-3 Reconciliation — authoring/v2 bases mirror the captured projections (DR-062)

## Tri-link block

```text
Beads: <TBA — filed under the SAK epic on implementation kickoff>
GitHub: jeremylongshore/intent-eval-lab#<TBA>
```

## 1. The ruling

> The base layer mirrors the captured projection exactly — documented fields only, upstream's requiredness, upstream's wire forms. Every IS narrowing or extension moves to the overlay with a convergence trigger. Implemented as authoring/v2 for the five contracts (mcp-config, plugin-manifest, agent-definition, hook-config, marketplace-catalog); authoring/v1 stays byte-frozen per DR-049; the skill-frontmatter v1+v2 split is the precedent.

Delegation basis: explicit owner instruction 2026-06-12 ("make the decisions, you are CTO"). This is an acting-CTO adjudication of the queue the deep-capture program produced — not a charter change. The structure ratified by DR-049 (base = upstream, overlay = IS policy, composition = marketplace tier) is untouched; this DR applies that structure honestly to the five contracts whose v1 bases predate their captures.

## 2. Scope

The deep-capture program (056 mcp-config, 058 plugin-manifest, 059 agent-definition, 060 hook-config, 061 marketplace-catalog) cross-checked each committed projection against the kernel's `schemas/authoring/v1/upstream-base/*.v1.json` and exact-match-pinned **27 divergences** (4 + 5 + 6 + 6 + 6). Each is dispositioned below into one of four classes. Per 052-AT-SPEC, every promotion here is a human-adjudicated act; the cross-check harnesses keep each finding pinned until the v2 fixtures supersede them.

Accounting (every finding lands in exactly one class; class totals sum to 27):

| Contract            | Source doc | Findings | C1 adopt       | C2 widen   | C3 relocate | C4 do-not-adopt |
| ------------------- | ---------- | -------- | -------------- | ---------- | ----------- | --------------- |
| mcp-config          | 056        | 4        | 3 (#2, #3, #4) | 1 (#1)     | —           | —               |
| plugin-manifest     | 058        | 5        | 2 (#1, #3)     | 1 (#2)     | 2 (#4, #5)  | —               |
| agent-definition    | 059        | 6        | 1 (#1)         | 2 (#3, #4) | 2 (#2, #5)  | 1 (#6)          |
| hook-config         | 060        | 6        | 3 (#1, #3, #5) | 1 (#2)     | 1 (#4)      | 1 (#6)          |
| marketplace-catalog | 061        | 6        | 3 (#2, #3, #4) | —          | 2 (#1, #5)  | 1 (#6)          |
| **Total**           |            | **27**   | **12**         | **5**      | **7**       | **3**           |

## 3. Disposition classes

### Class 1 — ADOPT-INTO-V2-BASE (12 findings)

Documented upstream fields and shapes the v1 base lacks. The v2 base adopts them verbatim from the projection.

- **agent-definition** (059 #1): the 11 unmodeled documented fields — `background`, `disallowedTools`, `effort`, `hooks`, `initialPrompt`, `isolation`, `maxTurns`, `mcpServers`, `memory`, `permissionMode`, `skills` — with the projection's types, enums, and per-field requiredness.
- **hook-config** (060 #1, #3, #5): the documented 3-level nesting replaces the flattened single-hook shape; 16 of 18 documented handler fields adopted (`allowedEnvVars`, `args`, `async`, `asyncRewake`, `headers`, `if`, `input`, `model`, `once`, `prompt`, `server`, `shell`, `statusMessage`, `timeout`, `tool`, `url`); per-type required fields modeled for all five handler types (`url`, `server`, `tool`, `prompt` requireds, not just `command`).
- **marketplace-catalog** (061 #2, #3, #4): the 4 documented top-level optionals (`$schema`, `allowCrossMarketplaceDependenciesOn`, `description`, `version`); all 18 documented plugin-entry optionals; the 5 documented source forms (relative-path string + github/url/git-subdir/npm object types with their per-type required/optional sets and the `source` discriminator); base states no `minItems` on `plugins`, matching the doc.
- **plugin-manifest** (058 #1, #3): the 11 unmodeled component-path fields (`agents`, `channels`, `dependencies`, `experimental.monitors`, `experimental.themes`, `hooks`, `lspServers`, `mcpServers`, `outputStyles`, `skills`, `userConfig`); the documented metadata fields `$schema`, `defaultEnabled`, `displayName`.
- **mcp-config** (056 #2, #3, #4): the transport selector takes upstream's wire name `type` (not `transport`); the `streamable-http` alias is accepted; per-transport shapes replace the flat shape (stdio's `command`/`args`/`env` vs URL-bearing transports). The base `$comment` re-attributes enum provenance to the Claude Code page per 056 finding 4 — the machine-readable schema defines neither the enum nor the server-config shape, and `ws` is Claude-Code-only.

### Class 2 — WIDEN-BASE-MOVE-NARROWING-TO-OVERLAY (5 findings)

The v1 base encoded an IS projection choice narrower than the documented surface. The v2 base widens to upstream's form; the narrowing relocates to the overlay with a convergence trigger.

- **agent-definition `tools`** (059 #3): base accepts the documented comma-separated string AND the array form; array-only narrowing → overlay.
- **agent-definition `model`** (059 #4): base admits the documented full-model-ID latitude alongside the alias enum + `inherit`; closed-enum narrowing → overlay.
- **plugin-manifest `commands`** (058 #2): base accepts `string|array` per the documented union; array-only narrowing → overlay.
- **mcp-config required-set** (056 #1): base makes `type` optional with the stdio default, matching upstream's own standardized-format example; the flat all-required projection choice → overlay.
- **hook-config `matcher`** (060 #2): base accepts the documented match-all forms (omitted / `""` / `"*"`); the explicit-non-empty-matcher requirement → overlay.

### Class 3 — RELOCATE-IS-EXTENSION-TO-OVERLAY (7 findings)

Kernel-only inventions with zero upstream provenance. Each moves to `is-overlay/<contract>.v2.json`, carrying a per-field convergence trigger in the walking-skeleton format (`is-overlay/skill-frontmatter.v1.json` precedent: `CONVERGENCE TRIGGER: if <upstream condition>, move it to upstream-base` — a mechanical move, not a re-edit).

- **`metadata` extension objects** (058 #4, 059 #2, 060 #4; 061 #2 notes the generic `metadata` modeling): the kernel-only `metadata` object on every contract → overlay. Trigger: upstream documents a top-level `metadata` field for the contract.
- **64-char name caps + kebab regexes** (058 #5, 059 #5, 061 #5): where upstream documents kebab-case in prose only or no length cap at all, the structural encoding → overlay. Trigger: upstream publishes a machine-readable length cap or pattern. Carve-out within 061 #5: the doc's **14 reserved names** are documented upstream and therefore adopt into the v2 base, not the overlay.
- **marketplace `plugins` `minItems: 1`** (061 #1): the corpus-rationalized minimum → overlay. Trigger: upstream documents a minimum entry count.

### Class 4 — DO-NOT-ADOPT (3 findings; provenance rule)

Sample-only tolerances — observed in official samples or catalogs but on no documented table. Per the conservative documented-vs-observed provenance rule (never promote observed to documented), these enter neither base nor overlay. They are recorded as upstream-documentation-bug findings; reporting optionals upstream is out of scope for this DR.

- **agent-definition** (059 #6): official sample uses `color: magenta` outside the documented 8-value enum.
- **hook-config** (060 #6): `rewakeMessage`, `rewakeSummary` used by one official plugin, documented nowhere.
- **marketplace-catalog** (061 #6): `commit` on github sources, `path` on url sources, the non-kebab plugin name `wordpress.com` in the official catalog.

## 4. Seat notes (consultative, not votes — no convening was held)

- **CISO:** widening bases does NOT weaken IS enforcement — the marketplace tier binds via overlays + composition, and v2 strict forks remain available. Demand: the monotonicity property (overlay is additive/narrowing on base, never loosening) must hold in v2 CI, same as v1.
- **GC:** the Class-4 upstream-documentation-bug findings are observations on the record, not commitments to report anything upstream.
- **CMO / VP DevRel:** no public-surface changes until consumers opt into v2; v1 untouched, so no author-facing migration event fires from this DR alone.
- **Hickey (panel canon):** this restores base=THEM purity — the projections are now the regeneration source for the bases, closing the loop the SSoT declaration (doc 045) demanded.

## 5. Implementation directive

1. Kernel `schemas/authoring/v2/` family for the five contracts, bases derived from the captured projections at `specs/_vendor/upstream/<contract>/projection.json` — the projection is the regeneration source, not a reference.
2. Codegen per the skill-frontmatter v2 pattern: upstream-base + is-overlay + composed marketplace tier + generated Zod validators, fold-agreement tested.
3. CHANGELOG entries per the changelog-observance gate (intent-eval-core PR #38) for every observable v2 surface.
4. Lineage `adopt`/`diverge` events appended in the lab ledger (054-AT-SPEC) when v2 lands, one per dispositioned finding class per contract; coverage map regenerates in the same append.
5. `authoring/v1` stays byte-frozen per DR-049; v1 consumers are unaffected; the per-contract cross-check fixtures repoint to v2 expectations only when each v2 base ships.

— Jeremy Longshore
intentsolutions.io
