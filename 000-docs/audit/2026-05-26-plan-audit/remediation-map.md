# Remediation Map — Plan Audit Findings → Plan Section / Bead

Maps every P0/P1 finding to one of:

- **(A) Plan amendment** — edit plan 027 in v5
- **(B) New bead** — file a bead to track the work
- **(C) Existing bead update** — add notes / dependencies to an open bead

## Convergent P0s (6 — must amend before any `bd claim`)

| ID     | Finding                                                                           | Action                      | Target                                                                                                                                      |
| ------ | --------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| CONV-1 | Acceptance gate strict-on-all is broken (5 seats)                                 | (A)                         | Plan § 3 AC-3 + § 4 Phase A `accept()` spec + new normative subsection "Acceptance gate predicate definition"                               |
| CONV-2 | Append-only + Rekor consistency missing (Lamport + Kleppmann)                     | (A) + (B)                   | Plan AC-2 + § 4 Phase C SkillVersion schema (add `version_kind` field) + new bead for "Define consistency model for refiner-core event log" |
| CONV-3 | SkillVersion/SkillSnapshot semantic clash (3 seats)                               | requires ISEDC ratification | TENSION-1 → ISEDC Session 7                                                                                                                 |
| CONV-4 | AC-12 tri-link 3-system consistency model missing (Hickey + Kleppmann)            | (A)                         | Plan AC-12 + § 5.5 tri-link spec; pick "bd-as-linearizable-writer" OR "projections-not-mirrors"                                             |
| CONV-5 | Phase D "defer indefinitely" wrong-shape re-open triggers (Karpathy + Cunningham) | requires ISEDC ratification | TENSION-2 → ISEDC Session 7                                                                                                                 |
| CONV-6 | Null-hypothesis baseline missing from Phase A (Karpathy + Beck)                   | (A)                         | Plan § 4 Phase A — insert Phase A.0 "Bitter-lesson baseline"; gate Phase A on result                                                        |

## Divergent P0s (5 — amend or ISEDC)

| ID       | Finding                                                  | Action    | Target                                                                                                                                     |
| -------- | -------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| F-KB-001 | Phase budgets without bandwidth model (Beck)             | (A)       | Plan § 4 Phase budgets — replace "~1 week" with FTE-week budget + critical-path bead callouts                                              |
| F-KB-003 | Hard gate is honor-system (Beck)                         | (A) + (B) | Plan § 13 Step 7 — add `bd config set` enforcement via a hook OR a `bd claim` pre-check script; file new bead for the enforcement script   |
| F-AK-002 | AC-7 "mechanism swappable" un-operationalized (Karpathy) | (A)       | Plan § 4 Phase A — define `RefinerStrategy` interface + ship 2 strategies (NaiveInContext + SkillOptStyle)                                 |
| F-RH-003 | Sample findings prime the panel (Hickey)                 | (A)       | Plan § 12 — remove "Sample findings" section OR fence with "DO NOT TREAT AS REAL FINDINGS" warning                                         |
| F-CH-001 | Eval-set governance absent from Phase A (Huyen)          | (A)       | Plan § 4 Phase A — add EvalSet versioning (`eval_set_version`, `lineage_parent`, `refresh_due_at`) to bootstrap surface; move from Phase F |

## Other P0s (per individual seat)

| ID       | Finding                                             | Action                          | Target                                                                                                                                   |
| -------- | --------------------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| F-RH-001 | SkillVersion/Snapshot duplication (Hickey)          | (covered by CONV-3)             | TENSION-1                                                                                                                                |
| F-RH-002 | Tri-link place-oriented (Hickey)                    | (covered by CONV-4)             | —                                                                                                                                        |
| F-CH-002 | Strict-all gate vs SkillsBench 16/84 (Huyen)        | (covered by CONV-1)             | —                                                                                                                                        |
| F-WC-003 | Phase D unmanaged debt (Cunningham)                 | (covered by CONV-5)             | TENSION-2                                                                                                                                |
| F-MK-1   | Rollback breaks append-only causality (Kleppmann)   | (covered by CONV-2 + TENSION-1) | —                                                                                                                                        |
| F-MK-2   | Sigstore Rekor unavailability undefined (Kleppmann) | (A) + (B)                       | Plan § 8 risks + § 4 Phase C — add `pending_production` state to SkillVersion; file new bead for "Outbox + reconciler for Rekor outages" |
| F-MK-3   | AC-12 tri-link consistency (Kleppmann)              | (covered by CONV-4)             | —                                                                                                                                        |

## P1 CRITICALs (15 — amend before affected Phase begins)

| ID       | Finding                                                                  | Action               | Target                                                                                                                  | Defers-to-phase |
| -------- | ------------------------------------------------------------------------ | -------------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------- |
| F-RH-004 | best-pointer mutable file no consistency semantics                       | (A)                  | Plan § 4 Phase A — specify pointer atomicity rule                                                                       | Phase A         |
| F-RH-005 | AC-11 two spec-version strings still place-oriented                      | (A)                  | Plan AC-11 — consider single sha256 of merged snapshot                                                                  | Phase A         |
| F-KB-004 | Phase A "hidden iep-P3 sigstore dependency"                              | (A)                  | Plan § 4.5 ecosystem fold — make iep-P3 explicit blocker for Phase A                                                    | Phase A         |
| F-KB-005 | Phase A+B/Phase C predicate-shape hand-waving                            | (A)                  | Plan § 4 Phase B exit — name the bridge step                                                                            | Phase B         |
| F-KB-006 | Bitter-lesson baseline missing                                           | (covered by CONV-6)  | —                                                                                                                       | —               |
| F-AK-004 | "Mechanism is product" vs AC-7 "mechanism swappable" contradiction       | requires ISEDC       | TENSION (new) → ISEDC                                                                                                   | Brand           |
| F-AK-005 | No eval of the eval set itself                                           | (A)                  | Plan § 4 Phase A — add eval-set quality metrics (coverage, leakage, calibration)                                        | Phase A         |
| F-CH-003 | Low-volume-skill bootstrap fallback undefined                            | (A)                  | Plan § 4 Phase A — define 3-tier policy per sample-finding F-CH-001 (was in plan as illustrative; now binding)          | Phase A         |
| F-CH-004 | Shadow → canary ladder not operationalized                               | (A)                  | Plan § 4 Phase B — name what "shadow" actually is in MVP (offline-eval vs traffic-routed)                               | Phase B         |
| F-CH-005 | $9.30/pass unit-economics derivation missing                             | (A)                  | Plan § 3 AC-5 — derive the number OR remove the claim                                                                   | Phase A         |
| F-LL-03  | rekor_log_index iff signing_mode invariant has no relying-party contract | (A)                  | Plan § 4 Phase C SkillVersion schema — add producer-vs-consumer obligation table                                        | Phase C         |
| F-MK-4   | 13→14 entity migration story missing                                     | (A)                  | Plan § 4 Phase C — define forward-compatibility test against existing 13-entity consumers                               | Phase C         |
| F-WC-001 | No AAR cadence in plan                                                   | (A)                  | Plan § 4 — add AAR cadence per phase (post-phase-exit + quarterly + post-incident)                                      | All phases      |
| F-WC-002 | 7 process disciplines without unifying abstraction                       | (A)                  | Plan § 3.5 — collapse PR-1..5 + verifier + spec-refresh into a single "Skill Refiner process discipline" with sub-rules | Phase A         |
| F-WC-005 | Cross-repo dependencies not negotiated with owners                       | requires bd outreach | bd notes on uprg, 9pi3 + ISEDC Session 7 ratification of dependency direction                                           | Phase C         |

## P2 / P3 / NIT (14 — backlog)

Filed in remediation-map but not gating. See individual seat findings files for verbatim text.

## New beads to file

These are surfaced by the audit as needing first-class tracking:

| Title                                                                                      | Parent epic                   | Severity |
| ------------------------------------------------------------------------------------------ | ----------------------------- | -------- |
| Define consistency model for refiner-core event log (linearizable? eventually consistent?) | RC-IAJ (bd_000-projects-214c) | P0       |
| Bitter-lesson baseline — Phase A.0 — naive-Opus-in-context vs proposed Refiner             | RC-IAJ                        | P0       |
| Hard-gate enforcement — `bd claim` pre-check honoring Plan Audit STATUS                    | RC-IEC (bd_000-projects-brij) | P0       |
| `RefinerStrategy` swap interface + 2 reference impls                                       | RC-IAJ                        | P0       |
| EvalSet versioning + lineage + refresh-cadence in Phase A                                  | RC-IAJ                        | P0       |
| Sigstore Rekor outbox + reconciler (handles outages)                                       | RC-IAH (bd_000-projects-aon3) | P0       |
| Document SkillVersion state machine + version_kind discriminator                           | RC-IEC                        | P1       |
| AAR cadence schedule per phase + quarterly                                                 | RC-IEL (bd_000-projects-rqwk) | P1       |
| Eval-set quality eval (coverage / leakage / calibration)                                   | RC-IAJ                        | P1       |

(These will be filed in § 13 Step 5 remediation only after the user authorizes amendment scope.)

## Tensions requiring ISEDC ratification

| #               | Tension                                                                                             | Seats                                          |
| --------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| TENSION-1       | SkillVersion/SkillSnapshot resolution path (merge / orthogonal-no-FK / state-machine-discriminator) | Hickey, Lamport, Kleppmann, internal-architect |
| TENSION-2       | Phase D resolution (quarterly trigger OR Blueprint A anti-goal)                                     | Karpathy, Cunningham                           |
| TENSION-3       | Process discipline weight (simplify to 1-2 abstractions OR eliminate AC-12)                         | Cunningham, Hickey                             |
| TENSION-4 (new) | "Mechanism is product" vs AC-7 "mechanism swappable" — what does IS sell?                           | Karpathy                                       |

— Claude (acting CTO)
2026-05-27
