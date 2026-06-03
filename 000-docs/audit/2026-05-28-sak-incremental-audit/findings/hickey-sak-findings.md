# Rich Hickey — § 14 SAK Incremental Audit Findings — 2026-05-28

## Summary

- The bicameral kernel framing reads "easy" (mirror runtime/, add authoring/) but complects three distinct things: spec-floor compliance, IS-marketplace policy, and prose-source-of-truth citation. Three folds dressed as one.
- § 14.10's nine-cell tier-binding table is a classic complecting move — required-fields, deprecation surface, security checks, and progressive-disclosure markers all live in the same `$defs.isMarketplace`. These are different concepts and they will need different versioning over time.
- The 6767-h ↔ kernel relationship treats _prose-as-canonical, schema-as-shadow_ as if it's a clean derivation. It isn't. Prose and schema have different invariants. Calling one a "shadow" of the other is the easy move; the simple move is to treat each as a value with its own identity, and make the mapping a third value.

## Findings

### F-RH-001 [P0] [GAPS]

**Plan section cited:** § 14.10 (the nine IS-extras table)
**Defect:** `$defs.isMarketplace` complects FOUR orthogonal concerns into one schema fold: (a) required-fields-policy, (b) deprecation registry (`DEPRECATED_FIELDS` + migration suggestions), (c) supply-chain security checks (YAML shell-substitution), (d) token-economy markers (L0/L1/L2 progressive disclosure). Each will evolve at a different cadence under different ratification regimes. Stuffing them into one `$defs` means any bump to one forces consumers to re-evaluate all four.
**Why this matters (Simple-vs-Easy):** This is the canonical Hickey failure mode. "Marketplace tier" is the easy noun — familiar, at-hand from existing CCP discourse. But under it sit four independent identities. When the deprecation registry adds `compatible-with` → `compatibility` (a tactical migration concern), every consumer of `$defs.isMarketplace` is forced to redeploy. When the security-check rule for `$(...)` tightens (a CISO concern), same. When progressive-disclosure tokenomics shift (a Karpathy-axis concern), same. _Simple Made Easy_: complecting is the source of pain.
**Proposed remediation:** Decompose `$defs.isMarketplace` into FOUR composable `$defs`: `isMarketplace.requiredFields`, `isMarketplace.deprecationRegistry`, `isMarketplace.securityChecks`, `isMarketplace.disclosureMarkers`. Consumers compose the ones they need. Each evolves independently with its own changelog. The "marketplace tier" becomes the composition, not a primitive. File `iec-E11-decomp` (P0, repo:iec).

### F-RH-002 [P0] [SCOPE_INTEGRITY]

**Plan section cited:** § 14.2 ("the kernel becomes bicameral") + § 14.10 (6767-h as upstream)
**Defect:** § 14.2 says the schemas are "machine-readable shadow" of 6767-h. § 14.10 then makes them ALSO encode IS-marketplace policy that has no prose home in 6767-h (the IS extras explicitly described as "NOT in any upstream spec — pure IS-enterprise additions"). The kernel cannot simultaneously be a shadow of 6767-h AND carry IS-only policy that 6767-h doesn't contain. The metaphor collapses on inspection.
**Why this matters (Simple-vs-Easy):** This is identity/value/time confusion (_The Value of Values_). "6767-h" is one value (the prose authority). "Kernel marketplace policy" is another value (the IS enterprise position). They have different identities. The plan treats them as one identity (kernel = shadow of prose) and one value (the schema). Two values masquerading as one will mean any prose change implies a schema change, and any schema change implies a prose change — neither implication is actually true.
**Proposed remediation:** Make the three values explicit: (1) 6767-h prose authority, (2) IS-marketplace-policy authority (the kernel's `$defs.isMarketplace`), (3) a third standalone artifact `intent-eval-core/schemas/authoring/v1/6767h-coverage-map.json` that records which schema fields trace to which 6767-h sections AND which fields are IS-only with no 6767-h trace. `prose-schema-coherence.yml` then checks the _map_, not the schemas directly. File `iec-E11-coverage-map` (P0, repo:iec).

### F-RH-003 [P1] [RISK]

**Plan section cited:** § 14.5 (CI gate strategy) + § 14.6 Q3 (vendored consumption)
**Defect:** The CCP-side vendoring (`.kernel-vendor/authoring/v1/`) is described as "matches `audit-harness` vendor pattern". But audit-harness vendoring is a deterministic-script substrate (you vendor a shell script; it runs the same forever). Schema vendoring carries an additional concern: _which version of the schema validated which artifact when_. The vendored copy is a value; the validation that ran against it is also a value; the kernel npm version is a third. Three values, one filesystem path.
**Why this matters (Simple-vs-Easy):** Borrowing a familiar pattern (vendoring) without checking whether the underlying primitive matches. Audit-harness is a deterministic substrate; kernel schema is a _policy_ substrate. The pattern is easy to copy; the semantics aren't the same.
**Proposed remediation:** Vendored schema files MUST carry a `$id` that includes the kernel version + a vendor-pinned-at timestamp. Validation results that get emitted into Evidence Bundles must record BOTH the vendored `$id` AND the kernel npm version it was supposed to mirror. `kernel-vendor-hash.yml` then checks the equality. File `iec-E11-vendor-id-discipline` (P1, repo:iec).

### F-RH-004 [P1] [RISK_MITIGATION]

**Plan section cited:** § 14.7 Risk B (Phase 4 stall mitigation)
**Defect:** The "wave A deterministic + wave B eval-loop" split is described as if "deterministic" and "eval-guided" are non-overlapping. They are overlapping in subtle ways: `batch-remediate.py` runs deterministic migrations against ambiguous frontmatter (e.g., `author` field that lacks `@`), and the Skill Refiner eval loop will also touch those. Wave A and wave B can produce conflicting edits to the same SKILL.md if not gated.
**Why this matters (Simple-vs-Easy):** Two mechanisms editing the same artifact with no explicit reconciliation rule is the easy framing ("wave A then wave B"). The simple framing requires answering: when wave A and wave B disagree on the same file, who wins? Is it last-write-wins (a time-based answer)? Is it eval-loop-wins (a quality-based answer)? Neither is stated.
**Proposed remediation:** State the conflict rule explicitly in § 14.4 Phase 4: wave A runs to completion AND emits a per-file `wave-a-applied` marker into the file (or a sidecar); wave B treats wave-a-marked files as immutable unless wave-A's emit failed validation. File `iec-E11-wave-reconciliation-rule` (P1, repo:iec).

### F-RH-005 [P2] [GAPS]

**Plan section cited:** § 14.4 Phase 1 ("kernel ships read-only")
**Defect:** "Read-only" is ambiguous. Does it mean (a) no consumer cuts over yet, (b) the schema file is immutable until Phase 2, or (c) the schema accepts no breaking changes during the phase window?
**Why this matters (Simple-vs-Easy):** Three distinct invariants compressed into one word. Hammock work that wasn't done.
**Proposed remediation:** Replace "read-only" with three explicit invariants: "no-consumer-cutover", "no-breaking-changes", "patch-bumps-allowed". File as a NIT amendment to § 14.4 Phase 1.

### F-RH-006 [P2] [SCOPE_INTEGRITY]

**Plan section cited:** § 14.10 ("IS extras beyond the 8-field set" table)
**Defect:** The nine IS-extras are listed as one flat table but they fall into at least three different categories — _visibility/runtime_ (requires*env, fallback_for), \_self-declared config surface* (required*environment_variables, metadata.intent-solutions.config), and \_authoring discipline* (semver, deprecation, author@-rule, shell enum, when_to_use cap, YAML security). These shouldn't sit in one schema.
**Why this matters (Simple-vs-Easy):** Same complecting failure as F-RH-001 at the sub-table level. Visibility-rules and authoring-discipline-rules are different concerns.
**Proposed remediation:** Mark each IS-extra with a category label in the schema (`x-is-extras-category`). When `$defs.isMarketplace` is decomposed per F-RH-001, the categories pre-define the decomposition. File `iec-E11-is-extras-categorize` (P2).

## Where I disagree with named other seats

- **Beck**: Kent will probably want a test for each of the 9 IS-extras. I want the schema decomposed first; tests-against-the-wrong-shape just lock in the wrong shape. Tidy before testing.
- **Karpathy**: Andrej is going to ask whether the kernel architecture survives a frontier-model-eats-everything event. I'd answer: a complected schema survives worse than a decomposed one, so the answer hinges on decomposition first.
- **Lamport**: Leslie will demand a formal predicate for "valid SKILL.md". I agree, but the predicate needs to compose from the decomposed `$defs`, not be defined against the complecting one.

## Most-costly-to-recover-from

F-RH-001 + F-RH-002 together. If `$defs.isMarketplace` ships complecting four concerns AND ships pretending to be a 6767-h shadow when it isn't, every downstream consumer (16 validators, 6 creators, 3,044 SKILL.md, plus future external adopters) inherits both confusions forever. Decomposing later is a years-long migration with breaking-change pain across all consumers. Decomposing now is one PR.
