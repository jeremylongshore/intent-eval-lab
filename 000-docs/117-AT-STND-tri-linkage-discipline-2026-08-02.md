<!-- BEGIN BD-SYNC:cross-ref:v1 -->

Beads: `bd_000-projects-pu35.6.1`
GitHub: `jeremylongshore/intent-eval-lab#278`
Projection-SHA256: fab0ae0a95920083edd0a0002d18eceb312bfc9efeb9d622478ed0648df7f668

<!-- END BD-SYNC:cross-ref:v1 -->

# Tri-linkage Discipline Standard

**Date:** 2026-08-02  
**Status:** NORMATIVE for Skill Refiner-scoped artifacts  
**Authority:** Plan 027 § 3.5 PR-1 + § 5.5; DR-028 T3; `bd-sync` projection generator

## 1. Purpose and scope

This standard defines the doc ↔ bead ↔ GitHub-issue topology for Skill Refiner
work. `bd` is the canonical writer. GitHub issues, Plane issues, and document
front-matter are projections and must be updated through `bd-sync` so the same
fact has one writer and verifiable mirrors.

The verifier is label-filtered to `refiner`. Legacy artifacts that predate this
standard are not retroactively swept; new or touched Skill Refiner artifacts
must carry the required peer references.

## 2. D7 — Doc ↔ bead ↔ GH-issue tri-link topology

The canonical Plan 027 D7 rendering is:

```text
              ┌────────────────────────────┐
              │      DOC  (.md in repo)    │
              │ NNN-XX-CCCC-<slug>.md      │
              │ front-matter:              │
              │   Beads: bd_…-0r8m.1       │
              │   Beads: RC-IEC            │
              │   GitHub: owner/repo#42    │
              └────────────┬───────────────┘
                           │                                  cited in
        cites in           │                          ┌──────────────────────┐
        description        │                          │                      │
              ┌────────────┴───────────────┐          ▼                      │
              │     BEAD  (bd issue)       │   ┌────────────────────┐        │
              │ id: bd_…-0r8m.1            │◀──│  GH ISSUE          │        │
              │ description ends with:     │   │  body ends with:   │        │
              │   Doc: iec/000-docs/...    │   │    Bead: bd_…-0r8m.1│       │
              │   GitHub: owner/repo#42    │──▶│    Doc: iec/000-... │       │
              └────────────────────────────┘   └──────────┬─────────┘        │
                           ▲                              │                  │
                           │                              │ comments mirrored│
                           │      bd-sync mirrors         │ via bd-sync      │
                           └──────────────────────────────┴──────────────────┘

   INVARIANT: any new artifact in the triangle must be born with the other two
   references already present. CI gate (validate-trilink.sh in § 5.5) rejects
   merges that violate the invariant for any artifact in 000-docs/ touching
   label 'refiner'.
```

The Plane issue is the parallel work-management projection. `bd-sync link`
records the GitHub and Plane identifiers on the bead; `bd-sync note` mirrors
receipts to both issue systems; `bd-sync project` renders the guarded GitHub
and document blocks; and `bd-sync close` propagates completion when explicitly
requested. The guarded blocks are machine-owned; surrounding prose remains
human-owned.

## 3. Required references

Every newly created or touched refiner artifact must expose the peer references
needed by the verifier:

| Surface      | Required peer references                                         |
| ------------ | ---------------------------------------------------------------- |
| Bead         | `Doc:` and `GitHub:` fields; `Plane:` when a Plane mirror exists |
| GitHub issue | generated `Bead:` and `Doc:` block                               |
| Document     | generated `Beads:` and `GitHub:` block                           |
| Plane issue  | bead and GitHub identifiers in the issue description or receipt  |

Do not edit generated blocks directly. Repair the canonical bead and rerun
`bd-sync project` when a projection drifts.

## 4. Scope boundary

This standard applies to the Skill Refiner label and its explicitly scoped
coordination artifacts. It does not authorize a bulk rewrite of historical
documents, a retroactive GH/Plane migration, or a weakening of the verifier.
