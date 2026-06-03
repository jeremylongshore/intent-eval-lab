# Kent Beck — § 14 SAK Incremental Audit Findings — 2026-05-28

## Summary

- Phase 4 is a big-bang disguised as a phase. 3,044 files migrated, two waves, two mechanisms, ending in advisory→blocking flip — six weeks of work landing on one moment. That's not small steps.
- No test drives the schemas yet. Phase 1 ships "read-only" kernel authoring schemas with no companion test corpus that demonstrates they accept-the-good and reject-the-bad. The feedback loop is missing.
- "Tidy first?" applies to Phase 0. The D4 patch is the right small structural cleanup, but it ships before the kernel schema exists — so D4 is being made hard by its absence of kernel context.

## Findings

### F-KB-001 [P0] [GAPS]

**Plan section cited:** § 14.4 Phase 4 (corpus migration, weeks 10-16)
**Defect:** Phase 4 is described as "6 weeks, two waves, ending in advisory→blocking flip". That is not a phase. That is six phases pretending to be one because the table needs six rows and Phase 4 was the budget slot. The "deliverable" line lists three things: deterministic remediation, eval-guided remediation, AND gate-flip. Each is its own end-state.
**Why this matters (small steps + Tidy First?):** The whole point of phasing is that each phase has a working end-state you can ship and live with. "Wave A landed; we're between waves" is a working state. "Wave A + wave B landed but gate is still advisory" is a working state. "Gate is blocking" is a working state. Lumping all three into "Phase 4" means a stall in any sub-state stalls the whole phase, AND it means the post-mortem if anything goes wrong has to reason across all three boundaries at once.
**Proposed remediation:** Decompose Phase 4 into 4a (wave A deterministic batch), 4b (wave B eval-loop), 4c (advisory→blocking flip). Each ships independently. Phase 4a's exit doesn't gate on Phase 4b starting; Phase 4c is its own ship/no-ship moment with its own quorum + ceiling check. Rewrite § 14.4 Phase 4 row as three rows. File `iec-E11-phase-4-decompose` (P0, repo:iec).

### F-KB-002 [P0] [GAPS]

**Plan section cited:** § 14.4 Phase 1 (kernel authoring/v1 ships read-only) + § 14.5 CI gates
**Defect:** Phase 1 ships 6 schemas + `_vendor/anthropic/` snapshots + `index.json`. No companion test corpus. There is no fixture set that says "these 50 SKILL.md examples MUST pass `$defs.isMarketplace`; these 50 MUST fail; these 50 are intentional edge cases." Without that, kernel v0.4.0 ships with schemas that have never been tested against the corpus they're supposed to validate.
**Why this matters (red-green-refactor + four rules of simple design):** The first rule of simple design is "passes its tests". A schema with no test corpus passes no tests; it just exists. Phase 4 (the migration) then becomes the first time anyone runs the schema at scale, which means Phase 4 becomes the test phase for Phase 1's deliverable. That's test-after, six weeks late, against 3,044 files in production. Feedback loop measured in weeks.
**Proposed remediation:** Add a Phase 1 sub-deliverable: `intent-eval-core/tests/authoring/v1/fixtures/` with golden positive + negative + edge-case corpora for each of the 6 schemas. Minimum 30 fixtures per schema (~180 total). Phase 1's exit gate becomes "schema correctly classifies all fixtures". `iec-E11b..g` epic per-schema beads each get a `-fixtures` child. File `iec-E11-fixtures-discipline` (P0, repo:iec).

### F-KB-003 [P1] [RISK]

**Plan section cited:** § 14.8 directive 1 (D4 patch ships in Phase 0, BEFORE kernel exists)
**Defect:** D4 adds `disallowed-tools` to the CCP validator at SCHEMA 3.7.0. The kernel doesn't exist yet. So D4 hand-codes the canonical position in `validate-skills-schema.py`. When kernel v0.4.0 ships, D4's hand-coded rule will need to be removed and re-implemented as a kernel-schema reference. That's the kind of work that doesn't get cleaned up — it stays as "we did this for Phase 0; we'll remove it later".
**Why this matters (Tidy First?):** This is the canonical "make the change easy, then make the easy change" violation. The kernel schema is the easy place to add `disallowed-tools`. D4 makes the change hard by adding it twice (validator now, kernel later). Tidy first would mean: ship the kernel schema stub first (even if just the skeleton with one field), then D4 adds `disallowed-tools` to the kernel, and the validator imports it. Two PRs instead of one, but no double-coded canonical position.
**Proposed remediation:** Either (a) restructure Phase 0 so the kernel stub ships before D4 and D4 lands in the kernel directly, or (b) explicitly mark D4's hand-coding as TECH DEBT in the validator with a code comment pointing at the kernel removal bead. Don't pretend the duplication isn't there. File `ccp-d4-debt-marker` (P1, repo:ccp).

### F-KB-004 [P1] [RISK_MITIGATION]

**Plan section cited:** § 14.4 Phase 4c exit ("advisory → blocking flip")
**Defect:** The 99.5% quorum + 30-day ceiling is a discrete event — one PR flips the workflow. The feedback loop from "advisory looks healthy" → "blocking actually works in CI" → "we caught the regression" → "we rolled back" is unspecified. If the flip breaks something, what's the rollback path? Reverting the PR? How long does that take? Who pages who?
**Why this matters (feedback-loop length):** This is the single highest-blast-radius moment per the plan's own framing. The feedback loop on "did the flip work?" needs to be minutes, not days. Right now it's unstated.
**Proposed remediation:** Add a Phase 4c sub-section to § 14.4 specifying: (a) the flip lands as a single revertible commit with explicit revert-PR template prepared in advance, (b) on-call rotation owns the first 72h post-flip with explicit alert thresholds, (c) any PR failing the new blocking gate within first 72h triggers immediate review and decides revert-or-amend within 1h. Mirror this in the Phase 4 risk table. File `iec-E11-phase-4c-rollback-protocol` (P1, repo:iel).

### F-KB-005 [P2] [GAPS]

**Plan section cited:** § 14.5 (`prose-schema-coherence.yml` NEW)
**Defect:** "Nightly. Parses 6767-h section headings; asserts every `$comment` in authoring schemas cites a currently-existing 6767-h section." How does it parse 6767-h section headings? That's not a trivial regex on a real markdown doc with renumbering. The mechanism is hand-waved.
**Why this matters (feedback-loop discipline):** A nightly gate that flakes on section renumbering is worse than no gate — it teaches people to ignore the red.
**Proposed remediation:** Pin the parsing implementation: list 6767-h section headings as a versioned `6767-h-sections.txt` snapshot, committed alongside 6767-h. The coherence workflow diffs this against actual 6767-h headings and against schema `$comment` citations. Three-way coherence, all three artifacts pinned. File `ccp-6767h-section-index` (P2, repo:ccp).

### F-KB-006 [P2] [SCOPE_INTEGRITY]

**Plan section cited:** § 14.9 (How SAK + Refiner interlock — 5 rows)
**Defect:** The interlock table lists 5 dependencies but doesn't say which direction the change-pressure flows. If the Refiner's `accept()` predicate depends on the kernel schema, what happens when the kernel schema bumps mid-flight? Does the Refiner re-run all past acceptance decisions? Re-eval the calibration set?
**Why this matters (make the change easy):** The interlock is described statically. The dynamic question — what does the next kernel-schema bump do to in-flight Refiner work — isn't answered.
**Proposed remediation:** Add a "kernel bump propagation" sub-section to § 14.9 specifying: minor bumps require Refiner calibration-set re-validation only; major bumps require full Phase A.0 baseline re-run. File `iel-refiner-kernel-bump-protocol` (P2, repo:iel).

## Where I disagree with named other seats

- **Hickey**: Rich will (correctly) demand the schema be decomposed before any test corpus is built. I want both — but I won't accept "we'll write the tests after we decompose". The tests drive the decomposition. Write a failing test that exposes the complecting; the schema separation falls out.
- **Lamport**: Leslie will (correctly) want a formal predicate for "valid SKILL.md". I want the failing test first; the predicate emerges from staring at why the test failed.
- **Cunningham**: Ward will (correctly) point out that the plan doc itself is becoming a tome. I agree, but I want the test corpus shipped before I worry about doc-shape. Living docs trump tidy specs that nobody runs.

## Most-costly-to-recover-from

F-KB-001 + F-KB-002 together. Phase 4 as a single phase + Phase 1 shipping with no test corpus means the corpus migration IS the test. 3,044 files in production are not a fixture set. When the schema rejects a SKILL.md that the author thinks should pass, the resolution PR will involve everyone — plan author, validator author, schema author, plugin author — because no one has prior agreement on what the schema actually does. Tests drive design; design tests after the fact and the design is accidental.
