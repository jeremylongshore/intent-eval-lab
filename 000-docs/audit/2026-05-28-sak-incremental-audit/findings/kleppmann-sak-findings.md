# Martin Kleppmann — § 14 SAK Incremental Audit Findings — 2026-05-28

## Summary

- The kernel-npm vs CCP-vendored copy is a two-writer system in disguise. Kernel npm publishing is one write path; vendored-copy hand-bumps are a second. The consistency model is asserted ("must match"), never specified. What happens during the window between npm publish and vendor bump?
- "Schema version" is treated as a monotonic counter but has at least three independent identities — `SCHEMA_VERSION` in CCP validator, `$schemaVersion` in kernel index.json, semver of npm package. Three counters, no stated ordering rule.
- The 3,044-file Phase 4 migration writes to 3,044 different files. Mid-migration snapshot semantics are unspecified: if Phase 4 is partway through wave A and someone authors a new SKILL.md, what version of the schema does it target?

## Findings

### F-MK-001  [P0]  [GAPS]
**Plan section cited:** § 14.6 Q3 (vendored kernel copy) + § 14.5 `kernel-vendor-hash.yml`
**Defect:** The kernel-npm package and the CCP `.kernel-vendor/authoring/v1/` copy form a two-replica system with no stated consistency model. When kernel npm publishes v0.4.1, when does the vendored copy update? In the same PR? In a follow-up PR? Within N days? The plan says "single one-line PR" to bump but doesn't specify the *window* during which the two are allowed to diverge. Asserting "must match" is not a consistency model — it's a hope.
**Why this matters (consistency model):** Strong consistency would require atomic npm-publish + vendor-bump (impossible across repos). Eventual consistency requires a stated bound on the inconsistency window. Without one, "must match" is interpreted differently by different operators.
**Proposed remediation:** Specify the consistency model: "(eventual consistency, bounded staleness ≤ 7 calendar days). When kernel npm v.X publishes, CCP CI's `kernel-pin-drift-cron.yml` (per Huyen F-CH-006) detects + files a [vendor-bump] issue within 24h. The vendored copy MUST be bumped within 7 calendar days OR the CCP `KERNEL_VERSION` pin must be explicitly held with an ADR explaining why." File `iec-E11-kernel-vendor-consistency-model` (P0, repo:iec).

### F-MK-002  [P0]  [GAPS]
**Plan section cited:** § 14.4 Phase 4 (corpus migration) + § 14.10 (Schema version sequencing)
**Defect:** Phase 4 takes 6 weeks (weeks 10-16). During those 6 weeks, SKILL.md files are being modified by Phase 4 wave A AND new SKILL.md files are being authored by plugin contributors AND existing skills are being modified for unrelated reasons. The plan doesn't specify the snapshot semantics: which kernel schema version do new authors target? Does wave A migrate the file in flight if a contributor PR touches it?
**Why this matters (mid-migration write semantics):** This is classic schema-migration territory. Without explicit snapshot rules, you get split-brain: contributor authors against kernel v0.4.0 advisory schema; wave A migrates the file to comply with kernel v0.4.1; conflict on merge. Resolution is bespoke each time.
**Proposed remediation:** State Phase 4 snapshot rules: (a) all new authoring during Phase 4 targets kernel `LATEST_PHASE_4_VERSION` (pinned at Phase 4 start; bumps only at phase-c flip). (b) wave A is sequenced BEFORE merging any in-flight PR that touches the same file; if conflict, wave A wins and contributor rebases. (c) wave B (eval-loop) NEVER runs on a file with an open PR. File `iec-E11-phase-4-snapshot-rules` (P0, repo:iec).

### F-MK-003  [P1]  [GAPS]
**Plan section cited:** § 14.10 (three version identities: CCP `SCHEMA_VERSION`, kernel `$schemaVersion`, npm semver)
**Defect:** Three independent version identities are introduced. Their ordering relationship isn't stated. Can the kernel `$schemaVersion` advance without the npm semver advancing (e.g., during pre-publish testing)? Can CCP `SCHEMA_VERSION` advance without the kernel pin advancing? Each is plausible; each implies different semantics.
**Why this matters (identity vs value vs time — Hickey would agree):** Three identities tracking related-but-distinct values over time. Without specified relations, "which version are we on?" has three answers and they can drift.
**Proposed remediation:** Specify the version-identity relations: (a) npm semver is *monotonic*; (b) kernel `$schemaVersion` advances atomically with npm publish (same git tag); (c) CCP `SCHEMA_VERSION` declares which kernel `$schemaVersion` it pinned and advances on every meaningful CCP-side validator change (semantic check tightening, etc.). Document as a versioning-discipline ADR. File `iec-E11-version-identity-relations` (P1, repo:iec).

### F-MK-004  [P1]  [RISK]
**Plan section cited:** § 14.7 Risk B (Phase 4 stall) + § 14.4 Phase 4 wave B (eval-loop edits)
**Defect:** Wave B uses the Refiner eval loop to edit SKILL.md files. Each edit is a write. If an eval-loop iteration fails partway (model timeout, judge disagreement, retry exhausted), what's the durability story? Is the partial edit committed? Rolled back? Logged for retry?
**Why this matters (durability under partial failure):** Distributed systems don't fail cleanly; they fail in the middle. The plan's wave-B latency model assumes happy-path completion. The partial-failure path isn't specified.
**Proposed remediation:** Specify the durability semantics for wave B: (a) edits are written to a side branch per-file (not main branch), (b) committed atomically (one commit per file) only after judge accept, (c) rollback = abandon the side branch (no main-branch impact). (d) Retry budget per file = 3; after exhaustion, file is parked in a `wave-b-failed/` queue for human triage. File `iaj-refiner-wave-b-durability` (P1, repo:iaj).

### F-MK-005  [P1]  [GAPS]
**Plan section cited:** § 14.4 Phase 4 + § 14.4 Phase 4c exit (advisory → blocking flip)
**Defect:** Phase 4c is described as a single flip. But the flip is a write to a workflow file (`validate-plugins.yml`). What's the rollback semantics? If the flip is reverted within 1h, were there PRs that landed during that hour against the blocking gate? Are their gate-results valid retroactively?
**Why this matters (snapshot freshness mid-migration):** Rollback isn't free in a system that's emitting Evidence Bundle gate-results. If a PR's gate-result was recorded against "schema blocking at 10:00" and the flip is reverted at 10:30, what does the Evidence Bundle for that PR say at 11:00?
**Proposed remediation:** Specify the rollback semantics: (a) flip lands as a commit with explicit pre-prepared revert PR template; (b) any gate-results emitted during the flip-window are tagged `phase-4c-window` in the Evidence Bundle; (c) on revert, those gate-results remain valid (they're records of what happened, not predictions). File `iec-E11-phase-4c-rollback-semantics` (P1, repo:iec).

### F-MK-006  [P2]  [GAPS]
**Plan section cited:** § 14.10 (the IS extras — visibility fields, fallback chains)
**Defect:** Fields like `requires_env`, `fallback_for_env`, `fallback_for_tools` declare conditional behavior. The conditional itself can drift — env can change, tools can change. The IS extras say a skill's visibility depends on these conditionals but don't say what happens when the conditional becomes obsolete (e.g., a tool is renamed).
**Why this matters (referential integrity over time):** The fallback chain is a referential structure. Renames break it silently.
**Proposed remediation:** State the referential-integrity invariant: every `requires_tools`/`fallback_for_tools` reference must resolve at validator-run-time against the current tool registry. Unresolved references → WARN (not ERROR — backward-compat) + log to a `tool-rename-debt.json` queue. File as NIT amendment to § 14.10.

## Where I disagree with named other seats

- **Lamport**: Leslie wants formal predicates. I want the consistency model spelled out before the predicate — predicate-against-the-wrong-consistency-model is wrong with confidence. Get the substrate right first.
- **Huyen**: Chip's shadow-mode for Phase 4c is right. I'd add: the shadow-mode itself is a parallel-write system (real verdict + shadow verdict per PR); the comparison data is itself a substrate that needs durability and consistency rules.
- **Karpathy**: Andrej is right that 6-12mo Anthropic-eats-this is a real risk. I'd note: the vendor-bump protocol I'm proposing in F-MK-001 is also the mechanism for graceful obsolescence — if Anthropic ships canonical spec, we point the vendor at upstream and migrate.

## Most-costly-to-recover-from

F-MK-002 (mid-migration snapshot semantics). Phase 4 runs for 6 weeks against a 3,044-file corpus that is itself being modified by contributors. Without snapshot rules, you get write-write conflicts that resolve in 3,044 different ways. Worse: gate-result Evidence Bundles emitted during the migration record which schema version they were checked against; if that's ambiguous, the audit-trail loses meaning. Once silent corruption is in the Evidence Bundle log, recovery is forensic — you have to retroactively re-verify every record. The cost of specifying snapshot rules is one page of plan; the cost of not specifying them is months of Evidence Bundle archaeology.
