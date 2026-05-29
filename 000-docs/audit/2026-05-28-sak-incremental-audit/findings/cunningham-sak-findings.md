# Ward Cunningham — § 14 SAK Incremental Audit Findings — 2026-05-28

## Summary

- Four NEW CI gates are being added (`kernel-vendor-hash.yml`, `prose-schema-coherence.yml`, `kernel-rubric-floor-guard.yml`, extended `schema-drift.yml`) plus a fifth implied (`kernel-pin-drift-cron.yml` per Huyen F-CH-006). Five gates around one schema family. Each gate is debt the team has to maintain. No AAR cadence specifies when we check whether they're still earning their keep.
- The § 14 doc itself has grown to 354 lines as a sub-section of a plan. "Read order: Plan 027 v5 → this doc → DR-028 → 029 → 030 → THIS file → DR-032." That's 6 docs to read before understanding what's being decided. The conversation cost is rising faster than the value.
- "Technical debt" is used to mean "thing we haven't paid back yet" — that's fine. But § 14 introduces several pieces of *implicit* debt that aren't named: the IS extras "we'll align to upstream eventually", the vendored snapshot "we'll re-sync periodically", the prose-schema map "we'll keep current". Implicit debt is the worst kind because no one tracks it.

## Findings

### F-WC-001  [P1]  [RISK_MITIGATION]
**Plan section cited:** § 14.5 CI gate strategy (5 gates total, 4 new + 1 extended)
**Defect:** Five CI gates land in 18 weeks. No re-evaluation cadence is specified. "When do we check whether these are still useful?" — unanswered. Some of them are likely to become flaky over time (e.g., `prose-schema-coherence.yml` parsing 6767-h section headings); some will become stale signal once Phase 5 ships; some will catch only what they were designed for and nothing else.
**Why this matters (technical debt as I meant it):** Debt only works as a metaphor when it's tracked deliberately. CI gates are debt — they're an ongoing maintenance commitment. Adding 5 gates with no re-evaluation cadence means the team has tacitly committed to maintaining all 5 forever, on top of whatever already exists.
**Proposed remediation:** Add § 14.5.1 "CI gate re-evaluation cadence". Every 90 days, owner reviews: (a) firing rate, (b) FP rate, (c) signal value (did it catch something a human wouldn't have?), (d) maintenance burden. Gates that score poorly across all 4 dimensions get a `[deprecate-candidate]` issue; deprecation requires ADR. File `iel-ci-gate-cadence` (P1, repo:iel).

### F-WC-002  [P1]  [RISK]
**Plan section cited:** § 14 overall (the doc itself, 354 lines)
**Defect:** The plan doc is at 354 lines as one § 14 sub-section. To understand a single decision (say, why D4 ships before ISEDC), the next reader needs Plan 027 v5 (~1700 lines) + DR-028 + 029 + 030 + THIS file + 032-DR (forthcoming) + the brief-pack 5 docs + 6767-h. That's a multi-thousand-line read for one decision. The artifact is becoming a tome.
**Why this matters (collaborative gradient):** The wiki principle: the artifact should lower the cost of the next conversation. Right now the artifact is raising it. The next person joining will spend two days reading before they can talk.
**Proposed remediation:** Carve § 14 SAK into a separate `031-PP-PLAN-skill-refiner-sak-amendment-v6...` doc (already so — good), AND author a `031-SUMMARY.md` companion that's ≤ 2 pages and tells someone-who-doesn't-know what the SAK is, why it exists, what it changes, where to look for detail. Treat it as the README for § 14. File `iel-sak-summary-doc` (P1, repo:iel).

### F-WC-003  [P1]  [GAPS]
**Plan section cited:** § 14.10 (IS extras + IS-only language + "we'll align eventually" implication)
**Defect:** § 14.10 describes IS extras as "NOT in any upstream spec — pure IS-enterprise additions". This is fine as an authoring choice, but it's implicit debt: someday agentskills.io or Anthropic will publish their own version of one or more of these (e.g., `requires_env` style conditional visibility is a natural feature for them to add). When that happens, IS has either to (a) adopt upstream's shape and migrate, or (b) maintain the divergence forever. Neither path is named, neither has a trigger.
**Why this matters (debt deliberately tracked):** Implicit debt compounds silently. Naming it costs nothing now and saves the eventual reconciliation argument.
**Proposed remediation:** Add to § 14.10 a "Future upstream-convergence" sub-section explicitly listing each IS-extra and the upstream-convergence trigger. Example: "If agentskills.io v2 adds `requires_env`, we adopt their shape and migrate kernel `$defs.isMarketplace.required` to match. If we choose to maintain divergence, requires ISEDC Class-1." File `iec-E11-upstream-convergence-policy` (P1, repo:iec).

### F-WC-004  [P2]  [RISK]
**Plan section cited:** § 14.5 (`prose-schema-coherence.yml`) + Beck F-KB-005 (parsing 6767-h headings)
**Defect:** Nightly cron that parses prose. The minute 6767-h gets a renumbering or a heading format change, this gate flakes. Flaky gates become tuned-out gates. Tuned-out gates are no gates.
**Why this matters (tools fit situation):** A nightly cron parsing prose is the wrong tool for the situation. The situation calls for stable cross-references; the tool is a fragile parser.
**Proposed remediation:** Replace nightly cron with: each PR that touches `6767-h-*.md` OR any `authoring/v1/*.schema.json` triggers `prose-schema-coherence.yml` synchronously. No background cron; only on-PR. Gate becomes a real check, not a noisy background notification. File `ccp-prose-schema-coherence-on-pr` (P2, repo:ccp).

### F-WC-005  [P2]  [RISK_MITIGATION]
**Plan section cited:** § 14.11 stopping criteria
**Defect:** Four stopping criteria are listed. None of them have a current-state indicator. How would the team know they're approaching trigger 2 (Phase 4 wave B stall)? Trigger 4 (drift exceeds 3 unresolved ADRs)?
**Why this matters (evolving documentation):** Stopping criteria are only useful if someone can tell you're approaching them. Right now they're aspirational.
**Proposed remediation:** Add a `SAK-DASHBOARD.md` in `intent-eval-lab/000-docs/` that tracks: (a) Anthropic indicator status (per Karpathy F-AK-001), (b) Phase 4 wave B file-count + ETA, (c) unresolved prose↔schema ADR count, (d) kernel-pin drift status across consumer repos. Updated weekly. File `iel-sak-dashboard` (P2, repo:iel).

### F-WC-006  [P2]  [SCOPE_INTEGRITY]
**Plan section cited:** § 14.10 ("DUAL-MAINTAINED — kernel ships its own CHANGELOG + the CCP one cross-references")
**Defect:** Two changelogs for the same logical schema. CCP's `SCHEMA_CHANGELOG.md` AND kernel's `schemas/authoring/v1/CHANGELOG.md`. Cross-references between them. Reader has to maintain a mental sync. This is exactly the kind of debt I named in 1992 — shipped knowing we'd come back to it.
**Why this matters (debt deliberately tracked):** If it's debt, name it. If it's permanent, justify it.
**Proposed remediation:** Pick one. Either kernel changelog is canonical and CCP cites kernel by hash, or CCP changelog is canonical (with kernel cross-referencing). Don't dual-maintain. File `iec-E11-changelog-singularity` (P2, repo:iec).

## Where I disagree with named other seats

- **Hickey**: Rich's decomposition is right but it lands more artifacts on the maintainer's desk before the team has shown it can maintain what's already on it. Decomposition first, then prove the discipline at the smaller scale, then build outward.
- **Beck**: Kent will want the failing test. I want to know who reads the test result and whether they can act on it. Test failures that no one reads are debt of a different kind.
- **Lamport**: Leslie's formal predicate is correct. But the team has to USE the predicate. A predicate doc that nobody opens after week 1 is a beautifully precise piece of debt.

## Most-costly-to-recover-from

F-WC-002 (doc-sprawl). The plan + audit + DR + bandwidth + brief-pack ecosystem is approaching 10,000+ lines for a single coherent initiative. The cost of bringing a new contributor up to speed is no longer "read the README"; it's "set aside two days". That cost compounds with every new initiative until the team's working knowledge becomes oral tradition supplemented by archaeology. A 2-page `SAK-SUMMARY.md` is the smallest thing that could possibly work.
