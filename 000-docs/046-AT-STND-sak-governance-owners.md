---
title: SAK Governance Owners — seat-bound decision-authority taxonomy
date: 2026-06-10
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
binding_authority: iec-E11-governance-owners (plan 033 § 14.12, closes audit finding C4)
inherits_from:
  - 031-PP-PLAN-skill-refiner-sak-amendment-v6-2026-05-28.md (v6 amendment intro)
  - 033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md (v7 audit-closure § 14.12)
related_drs:
  - 032-AT-DECR-isedc-class-1-charter-spec-authority-kernel-draft-2026-05-28.md (SAK charter)
  - 044-AT-DECR-isedc-council-session-8-sak-charter-2026-06-09.md (SAK charter ratification)
filing_standard: Document Filing Standard v4.3
---

# SAK Governance Owners

**Beads:** `bd_000-projects-kp30`

The Spec Authority Kernel (SAK) carries cross-consumer, immutable-surface, and
supply-chain-security concerns. Each concern has exactly one **named owner seat**
in the Intent Solutions Executive Decision Council (ISEDC) so that no SAK change
lands without a clearly-accountable sign-off. This document lifts the
decision-authority taxonomy verbatim from plan 033 (`033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md`)
§ 14.12 and is the canonical standalone reference for "who owns what" on the SAK.

It closes audit finding **C4** (governance + cadence — named seat-bound owners).

## Owner-seat map

| Concern                                               | Owner seat | Responsibility                                                                   |
| ----------------------------------------------------- | ---------- | -------------------------------------------------------------------------------- |
| Kernel schema versioning + breaking-change discipline | CTO        | Sign-off on `$schemaVersion` major bumps; co-sign Phase 4c flip                  |
| IS-marketplace policy floor (anti-realignment)        | CTO + CISO | Veto on `$defs.isMarketplace.requiredFields` changes per NON-NEGOTIABLES         |
| Supply-chain hardening (security checks)              | CISO       | Own `$defs.isMarketplace.securityChecks` evolution; co-sign Phase 4c flip        |
| External adopter relations + brand promise            | VP DevRel  | Co-sign Phase 4c flip; field cross-vendor distribution conversations per Phase F |
| Cost-budget enforcement (Refiner / SAK aggregate)     | CFO        | Sign-off on Phase 4b cost ceiling exceedances; audit wave B cost ledger          |
| Legal IP review on 6767-h / kernel coupling           | GC         | Sign-off on 6767-h ↔ kernel-map ADR amendments (per plan 033 § 14.16)            |
| Brand positioning + naming (Skill Refiner, SAK)       | CMO        | Veto on brand-canon changes; review external-facing dashboard copy               |

## Decision-authority taxonomy

- **CTO + CISO + VP DevRel triple** = required for the Phase 4c advisory→blocking
  flip + any kernel `$schemaVersion` major bump (NON-NEGOTIABLES item 7).
- **CTO alone** = minor/patch kernel bumps; validator patches at IS marketplace tier.
- **CFO** = cost-ceiling exceedance authorization (Phase 4b).
- **GC** = 6767-h ↔ kernel coverage-map ADR sign-off.
- **CISO veto** = any change to `$defs.isMarketplace.securityChecks`.

## Phase 4c rollback authority

Phase 4c is the advisory→blocking flip on `validate-plugins.yml`. Per plan 033
§ 14.12 + the rollback protocol described in plan 033, the **CTO + CISO + VP DevRel
triple** is also the authorizing body for a post-flip rollback. When BLOCKING mode
breaks real PRs at a high rate, the triple authorizes a single command —
`kernel-gate-revert <reason>` — which:

1. flips `validate-plugins.yml` back to `mode: advisory`;
2. records a Decision Record (`AT-DECR-phase-4c-rollback-NNN`);
3. emits a kernel-side Evidence Bundle row marking BLOCKING attestations from the
   affected window as `signing_mode: rolled-back-superseded`;
4. opens an ISEDC Class-2 retrospective session within 7 calendar days.

No single seat may authorize the rollback alone — the same triple that gates the
flip gates its reversal, so the authority surface is symmetric.

## Cross-references

- **Plan source:** `033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md` § 14.12.
- **SAK charter:** `032-AT-DECR-isedc-class-1-charter-spec-authority-kernel-draft-2026-05-28.md`
  (DRAFT) → ratified at `044-AT-DECR-isedc-council-session-8-sak-charter-2026-06-09.md`.
- **CCP CLAUDE.md** references this seat-bound taxonomy for the validator/spec
  NON-NEGOTIABLES (the IS 8-field marketplace required-set + error-vs-warning
  semantics) — the CTO + CISO veto on `requiredFields` and `securityChecks`
  enumerated above is the governance backing for those non-negotiables.
