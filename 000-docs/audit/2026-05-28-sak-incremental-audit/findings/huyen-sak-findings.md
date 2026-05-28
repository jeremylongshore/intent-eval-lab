# Chip Huyen — § 14 SAK Incremental Audit Findings — 2026-05-28

## Summary

- The Phase 4c "advisory → blocking flip" is the production deployment moment but it's described as a single discrete event with no shadow-mode, no canary, no progressive-rollout. 99.5% pass-rate is the gate, not a deployment discipline.
- The 3,044-file CCP corpus is the production traffic. The eval set for the schemas and for Refiner wave B is unspecified. Eval set drawn from same distribution as production traffic? The plan doesn't say.
- Governance gaps: who owns rollback if Phase 4c breaks? Who pages who when schema-validation false-positives spike during Phase 4 wave A? No rollback runbook, no on-call story, no SLA on resolution.

## Findings

### F-CH-001  [P0]  [GAPS]
**Plan section cited:** § 14.4 Phase 4c exit + § 14.6 Q4 quorum-pin
**Defect:** The 99.5%-pass + 30-day-ceiling discipline is a gate-flip rule, not a deployment discipline. In production-ML terms, this is going from 0% to 100% of traffic in one PR merge. No shadow-mode (the schema runs but its decision is logged, not enforced), no canary (the schema runs blocking on a subset of plugins first), no progressive rollout (gradual exposure expansion).
**Why this matters (production-ML governance):** Phase 4c is the single highest-blast-radius event per the plan's own framing. Skipping shadow-mode here means the first time the blocking gate sees a regression is in production CI, where it blocks a real PR. Recovery is "revert the workflow PR" but the social cost — a real contributor being told their PR is broken by infrastructure — is high and accumulates trust debt.
**Proposed remediation:** Insert a Phase 4b.5 between wave B and Phase 4c: SHADOW-MODE. For 7 calendar days, the kernel schema runs in `validate-plugins.yml` and emits its verdict as a PR comment (not a check failure). Measure FP rate (would-have-blocked-but-author-correct) and TP rate (would-have-blocked-author-actually-wrong) on real PR traffic. Phase 4c only fires if shadow-mode FP rate < 1%. File `iec-E11-phase-4b-5-shadow-mode` (P0, repo:iec).

### F-CH-002  [P0]  [GAPS]
**Plan section cited:** § 14.7 Risk A (kernel disagrees with 6767-h at edges) + § 14.10 (schemas-as-policy)
**Defect:** No governance owner is named for ANY of the failure modes. When the kernel schema rejects a SKILL.md that 6767-h ostensibly permits (Risk A), who decides? When Phase 4 wave B Refiner produces an edit a plugin author disputes, who arbitrates? When the schema policy needs to change, who proposes, who reviews, who approves?
**Why this matters (production-ML governance):** "The team" is not a governance answer. In production AI we name owners because incidents don't wait for committees. Without named ownership, every incident becomes a coordination problem on top of the technical problem.
**Proposed remediation:** Add § 14.12 "Governance owners" with named roles (not people — but seat-bound): (a) Schema Owner (CISO seat — owns IS-marketplace `$defs.required` set + anti-realignment guard), (b) Migration Owner (CTO seat — owns Phase 4 wave A/B execution + rollback decisions), (c) Drift Owner (VP DevRel seat — owns prose ↔ schema reconciliation ADRs), (d) Cost Owner (CFO seat — owns Phase 4 wave B inference-budget ceiling). Each Decision Record in CCP ties to one of these. File `iec-E11-governance-owners` (P0, repo:iel).

### F-CH-003  [P1]  [RISK]
**Plan section cited:** § 14.7 Risk B (Phase 4 stall mitigation) + § 14.4 Phase 4 wave B
**Defect:** "Eval loop handles only ambiguous tail (~20%)". The ~20% figure is asserted, not measured. What's the basis? The eval set used to estimate the deterministic-vs-ambiguous split is unspecified. If the true split is 50/50 (which is plausible for a corpus that's grown organically across 449 plugin dirs), Phase 4 wave B cost and time double.
**Why this matters (eval set / production distribution match):** This is the classic ML mistake — extrapolating from a small annotated sample to a 3,044-file corpus without confidence intervals. Production distribution may not match the assumption.
**Proposed remediation:** Phase 1 (or Phase 2) ships a `corpus-classification` deliverable: random sample 300 SKILL.md from the 3,044 corpus; classify each as deterministic-fixable vs eval-loop-required; report 95% CI on the percentage. If the lower CI bound is below 70% deterministic, Phase 4 cost model triggers; reallocate budget. File `iec-E11-corpus-classification-sample` (P1, repo:iec).

### F-CH-004  [P1]  [RISK_MITIGATION]
**Plan section cited:** § 14.9 (Refiner-SAK interlock, Phase A.0 baseline)
**Defect:** "Phase A.0 baseline (judge: `/validate-skillmd`)" — the eval-set bootstrap (DR-030 / D28-PHASE-A0) was authored before the kernel schema existed. After kernel ships, the judge changes (from CCP validator to kernel-loaded schema). Does Phase A.0 re-run on the new judge? If so, the baseline number could shift and invalidate downstream comparisons.
**Why this matters (training/eval/serving consistency):** The eval data path needs to be the same path as serving — same judge in both. Changing the judge mid-Refiner means baseline-N and post-edit-N are scored differently. Apples and oranges.
**Proposed remediation:** Pin Phase A.0 to a specific judge version (CCP validator at SCHEMA 3.7.0). When kernel cutover lands in Phase 2, run a PARALLEL Phase A.0' baseline on the kernel-loaded judge. Compare. Document the delta. If delta > 5%, pause Refiner work and reconcile. File `iaj-refiner-judge-version-pin` (P1, repo:iaj).

### F-CH-005  [P1]  [GAPS]
**Plan section cited:** § 14.4 Phase 4 + § 14.7 Risk B + § 14.4 Phase 5 (hook/MCP/agent/marketplace gating)
**Defect:** Phase 4 ships the SKILL.md migration; Phase 5 ships the other 5 contract gates. Same advisory→blocking flip mechanic, same risks. But Phase 5 ships in weeks 17-18 (2 weeks total) for FIVE contracts. There's no per-contract corpus classification, no per-contract quorum-pin, no per-contract shadow mode. Phase 5 is implicitly assumed to be lower-risk than Phase 4 with no justification.
**Why this matters (production-ML pipeline view):** Phase 5 covers plugin.json (449 files), agent definitions (variable count, growing), MCP configs (variable, growing), hooks.json (variable, security-critical), and marketplace.json (one file but high-signal). Each is its own distribution; each could surface its own ambiguity tail. Lumping them into 2 weeks reads like budget-driven optimism.
**Proposed remediation:** Either (a) decompose Phase 5 into 5 phases (one per contract, each with its own quorum-pin + shadow-mode), or (b) reduce Phase 5 scope to plugin.json + marketplace.json only (the two high-leverage low-cardinality contracts), defer agent/MCP/hooks to Phase 6+. File `iec-E11-phase-5-decompose` (P1, repo:iec).

### F-CH-006  [P2]  [RISK]
**Plan section cited:** § 14.7 Risk C (consumer repos pin different kernel versions)
**Defect:** Mitigation = "`/sync-kernel-pin` skill". But the skill is a tool; it requires someone to run it. What's the alerting story? When CCP pins v0.4.0 and global skills pin v0.4.1, who notices, and when?
**Why this matters (monitoring discipline):** A drift problem without a monitoring story is just a drift problem you'll discover after it bites.
**Proposed remediation:** Add a `kernel-pin-drift-cron.yml` workflow (weekly cron in `intent-eval-lab/`) that scans all consumer repos for kernel-version pins; emits a `[kernel-pin-drift]` issue when drift > 1 minor version. Auto-assigns to whoever last bumped. File `iec-E11-pin-drift-cron` (P2, repo:iel).

## Where I disagree with named other seats

- **Karpathy**: Andrej will (correctly) want schema-policy evals. I'd add: those evals need the SAME data-pipeline discipline as the Refiner evals — drawn from production distribution, tracked for drift, owned by a named role.
- **Beck**: Kent's "Phase 4 is a big-bang disguised as a phase" is right. Shadow-mode is the small-step decomposition.
- **Kleppmann**: Martin will (correctly) want consistency invariants on the kernel npm bumping. I want the deployment discipline that catches violations BEFORE they manifest as Evidence Bundle ambiguity.

## Most-costly-to-recover-from

F-CH-001 + F-CH-002. Phase 4c going from 0%→100% with no shadow-mode AND no named governance owner means the first incident — a real plugin author blocked by a schema rule that's a false-positive — becomes a triage scramble in real time. The accumulated trust debt with CCP plugin contributors is much harder to recover from than the technical revert. Shadow-mode + named owner together cost ~7 days. Trust recovery costs months.
