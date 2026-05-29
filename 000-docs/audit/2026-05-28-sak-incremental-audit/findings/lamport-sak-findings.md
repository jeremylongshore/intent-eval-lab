# Leslie Lamport — § 14 SAK Incremental Audit Findings — 2026-05-28

## Summary

- "Valid SKILL.md" is never formally defined as a predicate. § 14 talks around it for 11 sub-sections but never says: "A SKILL.md is valid iff (∀ field F in required) F is present ∧ (∀ field F) shape(F) ∈ ValueSpace(F) ∧ ...". Without the predicate, every consumer is implementing their own.
- Cross-schema invariants are absent. Six schemas are added — `skill-frontmatter`, `plugin-manifest`, `agent-definition`, `mcp-config`, `hook-config`, `marketplace-catalog`. What are the invariants ACROSS them? E.g., every `agent-definition.tools[i]` ∈ `mcp-config.servers[*].tools[i]`? Every `marketplace-catalog.plugins[i]` ∈ existing plugin-manifest? Unspecified.
- "Advisory → blocking flip" lacks a state-machine description. There are at least 5 reachable states (advisory-clean / advisory-violations-present / shadow-mode / blocking-stable / blocking-rolled-back); the transitions and their guards are described in prose only.

## Findings

### F-LL-001  [P0]  [GAPS]
**Plan section cited:** § 14.2 (the kernel becomes bicameral) + § 14.10 (tier discipline)
**Defect:** The plan never states what `valid(skill)` means as a predicate. § 14.10's tier table says "8 required (ERROR each)" but doesn't compose into a predicate. Is `valid(skill, tier)` ≡ `(∀ F ∈ tier.required) F ∈ skill ∧ schema_check(skill)` ? Or does it include the IS-extras conditional rules (e.g., `requires_env` is checked only if present)? Or the cross-field rules (`when_to_use + description ≤ 1536 chars`)? Prose describes individual rules; no formal definition composes them.
**Why this matters (specifications vs implementations):** "You haven't told me what the system is supposed to do; you've only told me what it does." Every validator now has its own implicit predicate. When two validators disagree on the same SKILL.md, there is no reference predicate to adjudicate. The kernel schema is supposed to BE the reference but it's not stated as a predicate; it's stated as a JSON Schema, which is one implementation of a predicate.
**Proposed remediation:** Add § 14.A "Valid SKILL.md — formal predicate". Define `valid(skill, tier)` as a composed predicate. State all conjuncts. State which conjuncts are deterministic-checkable vs require external context (e.g., `requires_env` checking against actual environment). The JSON Schema is then ONE implementation of the predicate; the predicate itself is the spec. File `iec-E11-valid-predicate-spec` (P0, repo:iec).

### F-LL-002  [P0]  [GAPS]
**Plan section cited:** § 14.2 (the 6 schemas) + § 14.10 (tier discipline applied to all 6)
**Defect:** Six schemas, treated as independent. But they are part of one bigger system — a plugin is a bundle of (manifest + agents + skills + MCP configs + hooks); a marketplace is a catalog of plugins. Cross-schema invariants are absent. Examples: every agent `tools` allowlist entry must reference a tool exposed by some MCP server in the same plugin; every `marketplace-catalog.plugins[].source.path` must point at an existing `plugin-manifest`; every hook event in `hooks.json` must be in the 30-event allowlist (§ 14.2 mentions this as a `hook-config` rule but doesn't cross-check against `agent-definition.permissionMode`).
**Why this matters (safety properties):** These are `[]` (always) properties on the plugin bundle. Without stating them, two independently-valid schemas can compose into an invalid plugin bundle. Test-and-pray won't find these; only formal invariants will.
**Proposed remediation:** Add § 14.B "Cross-schema bundle invariants". Enumerate the cross-schema `[]` properties. At minimum: (a) tools-consistency (agent.tools ⊆ ⋃ mcp.servers.tools), (b) marketplace-coverage (every catalog entry resolves to a valid manifest), (c) hook-allowlist (every hook.event ∈ allowlist), (d) plugin-bundle-completeness (manifest claims match physical files). File `iec-E11-cross-schema-invariants` (P0, repo:iec).

### F-LL-003  [P1]  [GAPS]
**Plan section cited:** § 14.4 Phase 4 + § 14.6 Q4 (quorum-pin) + § 14.4 Phase 4c exit
**Defect:** The advisory→blocking gate is described informally. There is no state machine specifying the reachable states, the guards on transitions, or the liveness property. Is there an "advisory but stalled at 95%" state? Is it the same as "advisory, healthy, still under 30-day ceiling"? Can a Phase 4 wave A regression move the system backward from "advisory-99%" to "advisory-95%"?
**Why this matters (state machines):** State machine reasoning catches the bugs that linear prose hides. "We flip at 99.5%" sounds clear but doesn't answer "do we un-flip at 98% post-flip?" The lack of unflip-state is itself a state.
**Proposed remediation:** Draw the Phase 4 state machine. States: ADVISORY, ADVISORY_QUORUM_PRE, ADVISORY_QUORUM_MET, SHADOW_MODE (per Huyen F-CH-001), BLOCKING, BLOCKING_ROLLED_BACK. Transitions with guards: ADVISORY → ADVISORY_QUORUM_MET iff pass-rate ≥ 99.5% AND days-elapsed ≥ 30; ADVISORY_QUORUM_MET → SHADOW_MODE on manual signoff; SHADOW_MODE → BLOCKING iff FP-rate < 1% over 7d; BLOCKING → BLOCKING_ROLLED_BACK on emergency revert; BLOCKING_ROLLED_BACK terminal until human re-plan. Spec the state machine in a `phase-4-state-machine.md` doc. File `iec-E11-phase-4-state-machine` (P1, repo:iel).

### F-LL-004  [P1]  [GAPS]
**Plan section cited:** § 14.10 (Schema version sequencing through migration) — the table at lines 261-269
**Defect:** The table shows CCP `SCHEMA_VERSION` and kernel `$schemaVersion` evolving in lockstep but the coupling invariant isn't stated. Is it `CCP_SCHEMA_VERSION.minor + 1 = KERNEL_SCHEMA_VERSION.minor` post-Phase-1? Or some other relation? Or is the coupling itself only sometimes enforced?
**Why this matters (specifications vs examples):** A table of examples is not a specification of the invariant. The table shows Phase 1 = (CCP 3.7.0, kernel 1.0.0). What's the invariant that says CCP 3.8.0 maps to kernel 1.0.x and not 1.1.0?
**Proposed remediation:** State the version-coupling invariant explicitly: "(safety) CCP `SCHEMA_VERSION` declares which kernel `$schemaVersion` it pinned via a field `KERNEL_SCHEMA_PIN`. (safety) `kernel-vendor-hash.yml` verifies this pin. (liveness) every kernel minor bump is followed within N days by a CCP `SCHEMA_VERSION` patch bumping the pin or an explicit decision-record declining." File `iec-E11-version-coupling-invariant` (P1, repo:iec).

### F-LL-005  [P2]  [GAPS]
**Plan section cited:** § 14.5 (`prose-schema-coherence.yml`) + § 14.7 Risk A (prose↔schema disagreement)
**Defect:** The "ADR amends both" reconciliation mechanism is described but not specified as an invariant. When can prose ↔ schema disagree, and for how long? Is there a liveness property that says "any disagreement is reconciled within N days"?
**Why this matters (liveness properties):** "Disagreements get reconciled eventually" is a liveness claim. Without an upper bound, "eventually" is never.
**Proposed remediation:** State the prose↔schema reconciliation liveness invariant: "(liveness) any prose↔schema disagreement detected by `prose-schema-coherence.yml` MUST be reconciled by an ADR within 14 calendar days OR escalated to ISEDC Class-1. (safety) at most 3 unresolved disagreements at any time (matches § 14.11 stopping criterion)." File `iec-E11-reconciliation-liveness` (P2, repo:iec).

### F-LL-006  [P2]  [GAPS]
**Plan section cited:** § 14.6 Q3 (CCP vendored at `.kernel-vendor/`) + § 14.5 `kernel-vendor-hash.yml`
**Defect:** The vendored copy and the kernel npm package are two values that must agree. Their relationship is described informally ("vendored copy hash equals npm-shipped hash"). What's the invariant when they disagree? Build fails, but what's the recovery? Is the vendored copy authoritative for the CCP CI run that detected the disagreement, or is the npm package?
**Why this matters (safety):** Disagreement IS the bug. The recovery semantics determine whether the bug is benign or compounds.
**Proposed remediation:** Specify the invariant: "vendored.hash = npm.hash, always. If detected unequal, CI fails red AND the vendored copy is treated as authoritative for the in-flight PR (no schema check skipped). Recovery: manual PR bumping the vendored copy to match the new npm." File as NIT amendment to § 14.5.

## Where I disagree with named other seats

- **Kleppmann**: Martin will (correctly) want consistency model spelled out for the kernel-npm vs vendored relationship. I want it as an invariant pair (safety + liveness), not as prose.
- **Beck**: Kent wants the failing test that exercises the schema. I want the predicate the test is checking. Same artifact at different abstraction levels — but if the predicate isn't written down, neither is the test, and neither knows what it's checking.
- **Hickey**: Rich wants decomposition. I want the predicate that the decomposition preserves. Decomposing without an invariant means you can't tell whether decomposition broke anything.

## Most-costly-to-recover-from

F-LL-001 (no formal `valid(skill)` predicate). Every validator implementation will diverge in subtle edge cases — null vs missing, empty array vs absent, normalization rules. Three years later you discover that the kernel says "valid" and the global-skills git-remote pre-commit says "invalid" on the same file and there's no reference predicate to break the tie. Recovery is impossible without retroactively defining the predicate, by which point thousands of skills have been authored against the implicit-predicate-each-validator-encoded.
