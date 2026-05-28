# § 14 SAK Incremental Audit — Synthesis — 2026-05-28

**Panel**: 7 seats (Hickey, Beck, Karpathy, Huyen, Lamport, Cunningham, Kleppmann)
**Scope**: § 14 SAK content of plan 031 v6 amendment (sub-sections 14.1 through 14.11) + companion 032 charter draft
**Method**: each seat reasoned from their canonical lens; findings classified P0/P1/P2/P3/NIT against four categories (GAPS / RISK / RISK_MITIGATION / SCOPE_INTEGRITY).

## Total counts

| Seat | P0 | P1 | P2 | NIT | Total |
|---|---|---|---|---|---|
| Hickey | 2 | 2 | 2 | 0 | 6 |
| Beck | 2 | 2 | 2 | 0 | 6 |
| Karpathy | 2 | 2 | 2 | 0 | 6 |
| Huyen | 2 | 3 | 1 | 0 | 6 |
| Lamport | 2 | 2 | 2 | 0 | 6 |
| Cunningham | 0 | 3 | 3 | 0 | 6 |
| Kleppmann | 2 | 3 | 1 | 0 | 6 |
| **TOTAL** | **12** | **17** | **13** | **0** | **42** |

## Convergent findings (≥ 3 seats raised similar)

### C1 — Phase 4 lacks deployment discipline (P0 convergent)
**Seats:** Beck (F-KB-001 Phase 4 big-bang), Huyen (F-CH-001 no shadow-mode), Lamport (F-LL-003 no state machine), Kleppmann (F-MK-002 + F-MK-005 mid-migration snapshot + rollback semantics), Karpathy (F-AK-004 cost model unspecified)
**Pattern:** Phase 4 — the 6-week corpus migration ending in advisory→blocking flip — is described as one phase with one quorum-pin. Five seats independently surfaced that this is the single highest-blast-radius event in SAK and it lacks: decomposition into sub-phases (4a/4b/4c), shadow-mode discipline before the flip, formal state-machine for the gate states, snapshot semantics for in-flight contributor PRs, rollback semantics for Evidence Bundles emitted during the flip window, and a per-file cost ceiling.
**Severity:** This is the convergent P0. Any single seat's finding here is sufficient; the convergence makes it definitive.

### C2 — Schemas-as-policy ships without evals or formal predicate (P0 convergent)
**Seats:** Karpathy (F-AK-002 no schema-policy eval), Lamport (F-LL-001 no formal valid(skill) predicate + F-LL-002 no cross-schema invariants), Beck (F-KB-002 no Phase 1 test corpus)
**Pattern:** The 6 authoring schemas encode IS-enterprise policy across ~9 IS-extras + 8 required fields. No eval measures whether the policy is *correct*; no formal predicate defines what "valid SKILL.md" means; no test corpus accompanies the schemas at Phase 1 ship. Three seats independently flagged that schemas-as-policy without an eval/predicate/test-corpus is an article of faith at scale.
**Severity:** P0 convergent. Schemas going into 3,044-file production without empirical validation of the policy is the kind of decision that compounds for years.

### C3 — Bicameral kernel architecture has complecting + identity problems (P0 convergent)
**Seats:** Hickey (F-RH-001 `$defs.isMarketplace` complects 4 concerns + F-RH-002 6767-h-as-shadow metaphor collapses), Karpathy (F-AK-001 bitter lesson 6-12mo obsolescence + F-AK-003 deterministic/probabilistic boundary fuzzy), Lamport (F-LL-002 cross-schema invariants missing)
**Pattern:** The "bicameral kernel" framing is doing rhetorical work that masks structural problems. § 14.10's `$defs.isMarketplace` complects required-fields + deprecation registry + security checks + token-economy markers. The "kernel as shadow of 6767-h" metaphor is contradicted by § 14.10's "IS-only extras NOT in any upstream spec". The bitter lesson says hand-curated schema infrastructure may be obsoleted by frontier models within 6-12mo.
**Severity:** P0 convergent on architectural integrity. Each seat sees a different facet of the same underlying problem.

### C4 — Governance owners + AAR cadence undefined (P1 convergent)
**Seats:** Huyen (F-CH-002 no named governance owners), Cunningham (F-WC-001 no CI-gate re-evaluation cadence + F-WC-005 no stopping-criterion dashboard)
**Pattern:** SAK ships 4-5 new CI gates, 6 new schemas, and a 6-week migration with no named seat-bound governance ownership. Stopping criteria are listed but with no current-state indicator. Gates ship with no re-eval cadence.
**Severity:** P1. Operational discipline gap; doesn't block ship but compounds.

### C5 — Doc / changelog sprawl creating compounded reader cost (P1-P2 convergent)
**Seats:** Cunningham (F-WC-002 plan doc sprawl + F-WC-006 dual-maintained changelogs), Hickey (F-RH-002 prose/schema as distinct values)
**Pattern:** The plan + DR + bandwidth + brief-pack ecosystem is 5,000+ lines for SAK alone; dual-maintained CCP/kernel changelogs; 6-doc read order. Reader cost is rising faster than artifact value.
**Severity:** P1-P2 mixed.

## Divergent findings (1-2 seats)

| ID | Seat(s) | Severity | Plan section | Finding |
|---|---|---|---|---|
| F-KB-003 | Beck | P1 | § 14.8 dir 1 | D4 hand-codes before kernel exists → duplicate canonical position |
| F-AK-005 | Karpathy | P2 | § 14.2 | `_vendor/anthropic/` no bump policy |
| F-AK-006 | Karpathy | P2 | § 14.10 | YAML shell-substitution check has no FP/FN measurement |
| F-CH-004 | Huyen | P1 | § 14.9 | Phase A.0 judge change mid-flight invalidates baseline |
| F-CH-005 | Huyen | P1 | § 14.4 Phase 5 | Phase 5 (5 contracts in 2 weeks) is implicit-low-risk assumption |
| F-LL-004 | Lamport | P1 | § 14.10 | Version-coupling invariant CCP↔kernel unstated |
| F-LL-005 | Lamport | P2 | § 14.5 + 14.7A | Prose↔schema reconciliation liveness bound missing |
| F-WC-003 | Cunningham | P1 | § 14.10 | IS extras "upstream-convergence trigger" implicit debt |
| F-WC-004 | Cunningham | P2 | § 14.5 | Nightly cron parsing prose = flaky-gate hazard |
| F-MK-003 | Kleppmann | P1 | § 14.10 | Three version identities, no stated ordering |
| F-MK-006 | Kleppmann | P2 | § 14.10 | Conditional-visibility fields have no referential-integrity rule |
| F-RH-004 | Hickey | P1 | § 14.7B | Wave A/B reconciliation rule absent |
| F-RH-005 | Hickey | P2 | § 14.4 | "Read-only" ambiguous (3 distinct invariants compressed) |
| F-RH-006 | Hickey | P2 | § 14.10 | 9 IS extras flat-listed across 3 categories |
| F-KB-004 | Beck | P1 | § 14.4 Phase 4c | Rollback protocol unspecified |
| F-KB-005 | Beck | P2 | § 14.5 | prose-schema-coherence parsing mechanism hand-waved |
| F-KB-006 | Beck | P2 | § 14.9 | Kernel-bump propagation to Refiner unspecified |

## Cross-seat tensions

### T1 — Decompose first vs test-drive first (Hickey vs Beck)
**Hickey (F-RH-001):** Decompose `$defs.isMarketplace` into 4 composable `$defs` BEFORE shipping. Tests against the wrong shape lock in the wrong shape.
**Beck (F-KB-002):** Ship the test corpus FIRST; the failing test exposes the complecting and drives the decomposition.
**Resolution recommendation:** Adopt BOTH in sequence — write the test corpus as Phase 1 sub-deliverable (Beck), then use the test failures to drive decomposition before Phase 2 (Hickey). Cost: ~2 weeks added to Phase 1. Avoids both fault modes.

### T2 — Bitter-lesson stop vs invest-and-ship (Karpathy vs Huyen/Kleppmann)
**Karpathy (F-AK-001):** Anthropic-eats-this within 6-12mo is plausible; add leading indicators to STOP early.
**Huyen / Kleppmann implicit:** The production-governance + consistency-model investment pays off regardless of whether kernel is canonical — even if Anthropic ships upstream, the discipline transfers.
**Resolution recommendation:** Both right; not actually mutually exclusive. Adopt Karpathy's leading-indicators (cheap to add); structure SAK so that if a leading indicator fires, the discipline (governance owners, consistency model, snapshot rules) ports to the upstream-canonical world rather than getting deleted.

### T3 — Formal predicate vs evolving-doc (Lamport vs Cunningham)
**Lamport (F-LL-001):** Define `valid(skill)` as a formal composed predicate; the JSON Schema is one implementation.
**Cunningham (F-WC-002 + meta):** Beautiful precise specs that nobody reads are debt of a different kind.
**Resolution recommendation:** Define the predicate IN the schema's `$comment` as a structured comment block, not in a separate doc. The predicate lives where the schema lives; consumers reading the schema see it; no separate doc to go stale.

### T4 — Implicit vs explicit upstream-divergence (Cunningham vs Karpathy)
**Cunningham (F-WC-003):** Name the IS-extras-vs-upstream divergence as deliberate debt with convergence triggers.
**Karpathy (F-AK-001 leading indicators):** Same intent — early-warning signals for when to align with upstream.
**Resolution recommendation:** Unify as one § 14.11 expansion: name each IS-extra divergence + the upstream-convergence trigger + the leading-indicator that says "Anthropic is heading toward this shape, prepare to converge."

## Remediation map

| Finding ID | Severity | Remediation type | Action |
|---|---|---|---|
| C1 (Phase 4 deployment discipline) | P0 | plan amendment | Decompose § 14.4 Phase 4 into 4a/4b/4b.5-shadow/4c; add state machine; add snapshot+rollback semantics; add cost ceiling. New beads: `iec-E11-phase-4-decompose`, `iec-E11-phase-4b-5-shadow-mode`, `iec-E11-phase-4-state-machine`, `iec-E11-phase-4-snapshot-rules`, `iec-E11-phase-4c-rollback-protocol`, `iaj-refiner-cost-instrument` |
| C2 (schemas-as-policy without evals) | P0 | plan amendment | Add Phase 1 test corpus + Phase 1.5 schema-policy eval + § 14.A formal valid(skill) predicate + § 14.B cross-schema invariants. New beads: `iec-E11-fixtures-discipline`, `iel-schema-policy-eval`, `iec-E11-valid-predicate-spec`, `iec-E11-cross-schema-invariants` |
| C3 (bicameral architecture integrity) | P0 | plan amendment | Decompose `$defs.isMarketplace`; clarify 6767-h-as-shadow vs IS-only-policy distinction with 3 named artifacts (prose / IS-policy / coverage-map); add Anthropic leading indicators. New beads: `iec-E11-decomp`, `iec-E11-coverage-map`, `iec-E11-anthropic-leading-indicators` |
| C4 (governance + cadence) | P1 | plan amendment | Add § 14.12 governance owners (4 seat-bound roles); add § 14.5.1 CI gate re-eval cadence (90-day); add `SAK-DASHBOARD.md`. New beads: `iec-E11-governance-owners`, `iel-ci-gate-cadence`, `iel-sak-dashboard` |
| C5 (doc sprawl) | P1 | doc + plan amendment | Author `031-SUMMARY.md` ≤ 2 pages; consolidate dual changelogs (pick kernel as canonical). New beads: `iel-sak-summary-doc`, `iec-E11-changelog-singularity` |
| F-AK-003 (det/prob boundary) | P1 | plan amendment | Specify the 4-quadrant accept/reject matrix in § 14.9 row 2. New bead: `iaj-refiner-schema-boundary` |
| F-MK-001 (kernel-npm vs vendored consistency) | P0 | plan amendment | Specify eventual consistency, bounded staleness ≤ 7d. New bead: `iec-E11-kernel-vendor-consistency-model` |
| F-MK-004 (wave B durability) | P1 | plan amendment | Side-branch-per-file + atomic commit + 3-retry + parked queue. New bead: `iaj-refiner-wave-b-durability` |
| Divergent P1s (F-KB-003, F-CH-003, F-CH-004, F-CH-005, F-LL-004, F-WC-003, F-MK-003, F-RH-004) | P1 | plan amendment | Each gets a one-line patch to plan 031 + a new bead per finding |
| Divergent P2s + NIT-adjacent | P2 | plan amendment OR existing-bead-update | Some fold into existing beads (e.g., F-AK-005 → enhance `iec-E11-vendor-bump-policy`); others get new low-priority beads |

## Recommended status disposition

**NEEDS-AMENDMENT** — 12 P0 findings across all 7 seats with strong convergence on 3 themes (Phase 4 deployment discipline, schemas-as-policy without evals, bicameral architecture integrity). The plan as drafted is too far from RATIFIED to ship with deltas; the P0 cluster requires substantive rework before the ISEDC Class-1 charter convenes.

This is the *expected* outcome for an incremental audit on widely-scoped new work — 7 seats finding zero P0s would have been the suspicious result. The convergence on Phase 4 from 5 independent seats is the strongest signal: this is the load-bearing decision and it's under-specified.

**Recommended next steps:**
1. Acting-CTO drafts plan 031 v7 amendment folding the C1/C2/C3 remediations (estimated ~3 days of work).
2. ISEDC Class-1 charter session deferred until v7 lands; charter scope unchanged (the 6 decisions in 032 don't go away, they just gate on a better-specified plan).
3. New beads filed per remediation map (~25 new beads total).
4. Re-audit incrementally on v7's § 14 deltas only; if v7 closes all P0s, STATUS flips to RATIFIED-WITH-DELTAS for the remaining P1/P2 work.

## Total counts

- **P0**: 12
- **P1**: 17
- **P2**: 13
- **NIT**: 0
- **TOTAL**: 42
