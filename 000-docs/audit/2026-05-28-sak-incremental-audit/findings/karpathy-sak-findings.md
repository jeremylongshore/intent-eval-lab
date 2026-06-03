# Andrej Karpathy — § 14 SAK Incremental Audit Findings — 2026-05-28

## Summary

- The bitter lesson bites here. SAK proposes a hand-curated schema-authority kernel right when frontier models are getting good enough at SKILL.md inference that the schema's edge cases might be handled by the model itself. Are we building a 2026 scaffold that 2027-Q1 obsoletes?
- The plan treats schema validation as deterministic (good) and Refiner edits as LLM-driven (good) but the BOUNDARY between them is fuzzy — § 14.9 says Refiner `accept()` depends on kernel schema validity, but doesn't say what happens when the model proposes an edit that's schema-valid but semantically wrong, or schema-invalid but semantically clearly better.
- 6 new authoring schemas are being added to the kernel without an eval that measures whether the schemas themselves are _correct_. The schemas are policy. Policy needs an eval too.

## Findings

### F-AK-001 [P0] [RISK]

**Plan section cited:** § 14.11 stopping criteria (Anthropic ships first-party spec)
**Defect:** The stopping criterion "Anthropic ships a first-party SKILL.md spec authority" is listed as a re-plan trigger but the probability isn't estimated and no early-warning signal is named. Given Anthropic's velocity on plugin/agent/skill surfaces (2.1.X cadence, agentskills.io is already published as v1.0), the realistic probability of an Anthropic-canonical machine-readable spec landing in 6-12 months is moderate-to-high. SAK invests Phases 1-5 (12-18 weeks per § 14.4) before that re-plan trigger fires.
**Why this matters (bitter lesson):** The bitter lesson is that methods which scale with compute beat methods that don't. A hand-curated schema-authority kernel scales with our maintenance, not with compute. If a frontier model can ingest 6767-h prose + agentskills.io spec + a few hundred SKILL.md examples and produce a validator function that matches our hand-built one, then our work was a 2026-era scaffold. The plan should at least name the early-warning signal so we know when to STOP, not just when something has already shipped.
**Proposed remediation:** Add a "leading indicators" sub-bullet to § 14.11 stopping criteria: (a) Anthropic publishes a public roadmap that includes machine-readable spec; (b) `claude` CLI begins ingesting a `.claude/schema/` directory at the project level; (c) `claude doctor` adds plugin-format validation. Any one of these = pause SAK Phase 1+, re-plan. File `iec-E11-anthropic-leading-indicators` (P0, repo:iec).

### F-AK-002 [P0] [GAPS]

**Plan section cited:** § 14.10 (the schemas as policy) — no companion eval mentioned
**Defect:** The 6 authoring schemas encode IS-enterprise policy. § 14.10 says "the kernel encodes the IS enterprise position". But there is NO eval that measures whether the schemas themselves correctly express the policy. Is `tags` actually a required field that improves outcomes? Is `version` semver-strict required because we have evidence semver-loose causes failures, or because it feels right? Where's the eval that says "skills with these 8 required fields perform better on judge-score-X than skills with only 2 required fields"?
**Why this matters (evals are the source code):** The schemas ARE prompts of a kind — they constrain what a skill author can write, which shapes what Claude can invoke. If the constraints are wrong, every downstream consumer pays. We don't ship prompts without evals; why are we shipping schemas without evals? The Refiner has an eval. The schema doesn't.
**Proposed remediation:** Add a Phase 1.5 deliverable: a "schema policy eval" that takes a corpus of N+ historical SKILL.md (pre-tagged with a quality score from `/validate-skillmd --thorough` or human-rated) and measures whether `$defs.isMarketplace` correctly classifies high-quality vs low-quality SKILL.md. Failure modes named: false-rejects (a high-quality skill that fails the schema) and false-accepts (a low-quality skill that passes). Pin a precision/recall floor. File `iel-schema-policy-eval` (P0, repo:iel).

### F-AK-003 [P1] [GAPS]

**Plan section cited:** § 14.9 (Refiner-SAK interlock, row 2 — Phase A library)
**Defect:** "Refiner's `accept()` predicate evaluates 'is the post-edit SKILL.md kernel-schema-valid'". What happens when the model proposes an edit that's schema-VALID but a clear regression (semantic deterioration) vs an edit that's schema-INVALID but a clear improvement (the schema is over-strict)? The boundary between deterministic gate (schema) and probabilistic judge (Refiner eval loop) isn't defined.
**Why this matters (deterministic/probabilistic boundary):** This is the load-bearing boundary in the whole AI-native architecture. Schema validity is deterministic; semantic quality is probabilistic. The plan implies schema validity is a _precondition_ to acceptance — but what if the schema is wrong about a specific case? The Refiner has no mechanism to overrule the schema; the schema has no mechanism to learn from Refiner-judged-better-but-invalid edits.
**Proposed remediation:** In § 14.9 row 2, specify the boundary explicitly: (a) schema-valid + judge-improved = ACCEPT, (b) schema-valid + judge-regression = REJECT (schema didn't catch the real problem), (c) schema-INVALID + judge-improved = LOG AS SCHEMA-DEFECT, do not auto-accept, but do route to SAK schema-bump consideration via a `schema-revision-candidates` queue, (d) schema-invalid + judge-regression = REJECT (both gates agree). File `iaj-refiner-schema-boundary` (P1, repo:iaj).

### F-AK-004 [P1] [RISK]

**Plan section cited:** § 14.4 Phase 4 wave B (eval-loop for ~20% ambiguous tail)
**Defect:** "Skill Refiner's eval-guided edit loop has unknown per-file latency; 24-hour budget at scale could mean weeks." This is named as Risk B but the mitigation ("eval loop handles only ambiguous tail") doesn't actually address the cost question. ~20% of 3,044 = ~609 files. At even 10 minutes per file (model latency + judge + retry), that's 100+ hours. At cost-per-file, that's real money. No estimate is provided.
**Why this matters (inference economics):** Bitter lesson cuts both ways — methods that scale beat methods that don't, but ECONOMICS scales with usage. If Phase 4 wave B costs $X dollars and Y hours, we should know that before authorizing it.
**Proposed remediation:** Add to § 14.7 Risk B mitigation: per-file cost model (input tokens × output tokens × provider rate × expected retry rate). Pin a dollar ceiling on Phase 4 wave B (e.g., $500); if exceeded, pause and re-plan. Pin a time ceiling (e.g., 7 calendar days). Cost instrumentation lands as Phase 4 sub-deliverable. File `iaj-refiner-cost-instrument` (P1, repo:iaj).

### F-AK-005 [P2] [GAPS]

**Plan section cited:** § 14.2 architecture (the `_vendor/anthropic/` snapshots)
**Defect:** "Snapshotted upstream specs (read-only)" — the vendoring is described as a single-version pin. But Claude Code is on a 2.1.X cadence. What's the bump policy? When 2.2.0 ships, who decides whether to bump the vendor? On what signal?
**Why this matters (model/spec drift):** This is the same drift problem as model drift, applied to spec drift. Without a defined bump policy, the kernel will lag upstream by some unbounded amount, and we'll discover the gap when something breaks.
**Proposed remediation:** Vendor-bump policy in § 14.5: `spec-drift-watch.yml` already polls upstream; extend it to file a `[vendor-bump-candidate]` GH issue when upstream diverges from vendored. Ratification gate: at least one human review confirms the bump is non-breaking before merging. File `iec-E11-vendor-bump-policy` (P2, repo:iec).

### F-AK-006 [P2] [RISK_MITIGATION]

**Plan section cited:** § 14.10 (the YAML shell-substitution security check)
**Defect:** "YAML shell-substitution security check (`$(...)`, backticks, ungated `${VAR}` outside allow-list)" — listed as IS-extra at 3.3.x. But what's the eval that says this check is correct? What's the false-positive rate on legitimate skills that use `$(...)` in a description for documentation purposes?
**Why this matters (LLM-as-primitive vs feature):** This is a security check applied to text that flows into model context. False positives waste author time; false negatives are supply-chain attacks. Both should have measured rates.
**Proposed remediation:** Add a `tests/security/yaml-shell-substitution/` corpus to kernel Phase 1 fixtures: known-malicious + known-benign + known-edge. Measure FP/FN rate. Document expected rates in `$defs` `$comment`. File `iec-E11-security-corpus` (P2, repo:iec).

## Where I disagree with named other seats

- **Hickey**: Rich wants the schema decomposed. I want an eval that measures whether the decomposed schema produces better outcomes than the complecting one — otherwise it's a refactor based on taste, which doesn't survive frontier-model-eats-everything.
- **Huyen**: Chip will (correctly) want shadow-mode for the Phase 4c flip. I'd extend it: shadow-mode on the SCHEMAS themselves — run them advisory for a full Phase 4 against a calibration corpus and measure drift between expected-pass and actual-pass before flipping anything.
- **Lamport**: Leslie wants a formal predicate. I want the predicate AND an eval that says the predicate corresponds to what real users would call valid.

## Most-costly-to-recover-from

F-AK-001 (Anthropic ships first-party). If 6-12 months from now Anthropic publishes a machine-readable spec that subsumes 6767-h + agentskills.io, every Phase 1-5 deliverable becomes legacy IS-bespoke infra. The 3,044 SKILL.md corpus migration to a now-obsolete kernel is sunk cost. The plan needs leading indicators that say "stop building this layer; cut over to upstream" BEFORE the wasted effort accumulates, not after.
