---
title: State-Labeling Standard — normative-doc lifecycle labels for the Intent Eval Platform
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: Blueprint A § 2.3 (DR-010 three-class governance routing)
inherits_from:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E13
bead: bd_000-projects-njw9
filing_standard: Document Filing Standard v4.3
related_docs:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — labels applied)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — labels applied)
  - 013-AT-SPEC-repo-blueprint-template.md (Blueprint C — labels applied)
  - 014-DR-GLOS-canonical-glossary.md (canonical glossary — labels applied)
  - 068-AT-STND-core-repo-boundaries-2026-06-18.md (uses CURRENT/PLANNED/EXPERIMENTAL/DEFERRED/REJECTED scope labels)
related_drs:
  - 010-AT-DECR (DR-010 — three-class governance routing; phase lifecycle)
---

> **State label: NORMATIVE.** This standard is binding on every numbered document in
> `intent-eval-lab/000-docs/`. Its own lifecycle is governed by the labels it defines.
> Authoring lifecycle defined here; amendments route per Blueprint A § 2.3.

# State-Labeling Standard

**Beads:** `bd_000-projects-njw9` (iel-E13b) under epic `bd_000-projects-7gs` (iel-E13).

## 1. Purpose

A reader who opens any document in this repository must be able to tell, from the
top of the file alone, **how much weight it carries and whether it is still in force**.
Without an explicit label, a draft RFC reads identically to a binding architectural
lock, and a superseded plan reads identically to the plan that replaced it. This
standard fixes a small, closed vocabulary of **lifecycle labels** and the rules for
applying, displaying, and transitioning them.

This standard governs the **document lifecycle** — the maturity and in-force status
of a whole document. It is distinct from, and complementary to, the **scope-element
labels** (`CURRENT` / `PLANNED` / `EXPERIMENTAL` / `DEFERRED` / `REJECTED`) defined in
`068-AT-STND-core-repo-boundaries-2026-06-18.md`, which classify individual capabilities,
predicate types, and repo responsibilities _inside_ a document. A document is `NORMATIVE`
(its lifecycle label) while it describes a feature that is `PLANNED` (a scope-element
label). The two vocabularies never collide because they label different things.

Per the Canonical Glossary (`014-DR-GLOS-canonical-glossary.md`), "Decision Record,"
"ratification," "override," and the Phase A/B/C lifecycle are defined terms; this
standard cites them and does not redefine them.

## 2. The lifecycle labels

Exactly seven labels exist. The set is closed: a document MUST carry exactly one of
them, and no document may invent a new label without amending this standard.

| Label         | Meaning                                                                                                                                                                           | In force?        | Amendment path                                                        |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | --------------------------------------------------------------------- |
| `DRAFT`       | Work in progress. Content is not yet ready to bind anything; tables and decisions may still change materially.                                                                    | No               | Edit freely until promoted.                                           |
| `NORMATIVE`   | Binding specification or standard. Downstream documents, code, and CI inherit from it. Conflicts are resolved in this document's favor until amended.                             | Yes              | Decision Record per Blueprint A § 2.3 routing.                        |
| `RATIFIED`    | A decision that has been adjudicated and locked by a governance body (an ISEDC session, an acting-CTO ruling, or a pair Decision Record). Verbatim positions, if any, are frozen. | Yes              | A subsequent ratifying Decision Record (re-ratification or revision). |
| `INFORMATIVE` | Reference, landscape, research, or after-action content. Carries no binding force; cited for context, not inherited from.                                                         | No (non-binding) | Edit or supersede; no governance gate.                                |
| `SUPERSEDED`  | Replaced by a later document. Retained for the audit trail. MUST name its successor.                                                                                              | No               | None — terminal. The successor carries the live content.              |
| `DEPRECATED`  | Still technically in force but scheduled for removal; consumers should migrate. Distinct from `SUPERSEDED` (which is already replaced).                                           | Yes, with sunset | A removal Decision Record at end of the deprecation window.           |
| `WITHDRAWN`   | Pulled before it ever bound anything (a proposal that was rejected at intake, or a draft abandoned). Distinct from `SUPERSEDED` (which was once in force).                        | No               | None — terminal.                                                      |

### 2.1 Why these seven and not more

- `DRAFT` → `NORMATIVE`/`RATIFIED` is the normal promotion path for a specification
  or a decision.
- `INFORMATIVE` exists because the majority of `000-docs/` content (RR-LAND landscape
  surveys, AA-AACR after-action records, DR-BRIEF system briefs) is reference material
  that must never be mistaken for a binding spec.
- `SUPERSEDED` vs `WITHDRAWN` vs `DEPRECATED` are kept distinct because they answer
  three different reader questions: "what replaced this?" (`SUPERSEDED`), "did this
  ever bind?" (`WITHDRAWN` = no), and "is this on a clock?" (`DEPRECATED`).

Anything that does not fit one of the seven is a signal that the document's purpose is
unclear — resolve the purpose, do not add a label.

## 3. Label-to-category-code correspondence (advisory)

The Document Filing Standard v4.3 category code (the `CC-ABCD` segment of the filename)
correlates with, but does not determine, the lifecycle label. The label is authoritative;
the filename category is a filing aid. Typical pairings:

| Category code                              | Typical lifecycle label(s)                                                      |
| ------------------------------------------ | ------------------------------------------------------------------------------- |
| `AT-ARCH`, `AT-SPEC`, `AT-STND`            | `NORMATIVE` (or `DRAFT` while authoring)                                        |
| `AT-DECR`                                  | `RATIFIED` (or `DRAFT` pre-session)                                             |
| `DR-STND`, `DR-GLOS`                       | `NORMATIVE`                                                                     |
| `DR-RFC`, `DR-BRIEF`, `DR-GAPS`, `DR-BAND` | `INFORMATIVE` or `DRAFT`                                                        |
| `RR-LAND`, `RR-INTL`, `RR-LITS`            | `INFORMATIVE`                                                                   |
| `AA-AACR`, `AA-AUDT`                       | `INFORMATIVE`                                                                   |
| `PP-PLAN`                                  | `INFORMATIVE` (planning), or `SUPERSEDED` when a later plan version replaces it |

A document whose category code and lifecycle label imply different weights (e.g., an
`AT-ARCH` marked `INFORMATIVE`) MUST state why in its purpose section.

## 4. How a label is applied

Every numbered document MUST carry its lifecycle label in **two places**:

1. **Frontmatter** — a `state_label:` key in the YAML frontmatter block, carrying the
   bare label string. Documents authored before this standard already carry a
   `status:` field; where present, `state_label:` is the authoritative lifecycle label
   and `status:` is retained for backward compatibility. When the two disagree,
   `state_label:` wins.
2. **Visible banner** — a single blockquote line immediately below the frontmatter,
   beginning `> **State label: <LABEL>.**`, so the label is readable in any rendered
   or plaintext view without parsing YAML.

The banner MAY add a one-clause qualifier after the label (e.g., a successor reference
for `SUPERSEDED`, or a sunset date for `DEPRECATED`). Example banners:

```text
> **State label: NORMATIVE.** Binding on every IEP repo per Blueprint A § 2.3.
> **State label: SUPERSEDED.** Replaced by 027-PP-PLAN-... (v5). Retained for audit trail.
> **State label: DEPRECATED.** Sunset 2026-09-01; migrate to 070-AT-ARCH-... .
```

## 5. Transition rules

Lifecycle transitions are not free-form. The permitted transitions are:

| From                     | To           | Trigger                                                                                                                     |
| ------------------------ | ------------ | --------------------------------------------------------------------------------------------------------------------------- |
| `DRAFT`                  | `NORMATIVE`  | Author promotes; for an `AT-*` doc this is a Class-2 or Class-1 act per Blueprint A § 2.3 depending on the surface touched. |
| `DRAFT`                  | `RATIFIED`   | A governance session adjudicates and locks the decision.                                                                    |
| `DRAFT`                  | `WITHDRAWN`  | The proposal is abandoned or rejected at intake.                                                                            |
| `NORMATIVE`              | `DEPRECATED` | A successor is in flight; consumers are put on a migration clock.                                                           |
| `NORMATIVE` / `RATIFIED` | `SUPERSEDED` | A successor document lands and takes over the live content.                                                                 |
| `DEPRECATED`             | `SUPERSEDED` | The successor lands and the deprecation window closes.                                                                      |
| `RATIFIED`               | `RATIFIED`   | Re-ratification by a later session (the later session's record carries the live decision).                                  |

Forbidden: re-promoting a `SUPERSEDED` or `WITHDRAWN` document back to `NORMATIVE`. To
re-introduce withdrawn content, author a **new** document — the audit trail of the
terminal state stays intact.

When a document transitions to `SUPERSEDED` or `DEPRECATED`, its banner MUST be updated
to name the successor, and the successor's frontmatter SHOULD list the predecessor in
`supersedes:`.

## 6. The 000-INDEX `Status` column

The `000-INDEX.md` table already carries a free-text `Status` column. That column is a
human summary; this standard's `state_label` is the machine-checkable lifecycle label.
The index `Status` cell for each document SHOULD lead with the lifecycle label in bold
(e.g., `**NORMATIVE** — Blueprint A, the constitution`) so the index and the document
agree at a glance. Index drift (a document labeled `NORMATIVE` whose index cell says
otherwise) is a documentation defect, fixable as a Class-3 solo edit.

## 7. Application to the foundation documents (skrs)

Per bead `bd_000-projects-skrs` (iel-E13d), the four Phase A foundation documents are
labeled retroactively under this standard. All four were authored as binding artifacts
under ISEDC Session 4 (DR-010) and are in force; each receives the `NORMATIVE` label:

| Document                                                  | Lifecycle label |
| --------------------------------------------------------- | --------------- |
| `011-AT-ARCH-ecosystem-master-blueprint.md` (Blueprint A) | `NORMATIVE`     |
| `012-AT-ARCH-platform-runtime-blueprint.md` (Blueprint B) | `NORMATIVE`     |
| `013-AT-SPEC-repo-blueprint-template.md` (Blueprint C)    | `NORMATIVE`     |
| `014-DR-GLOS-canonical-glossary.md` (Canonical Glossary)  | `NORMATIVE`     |

The retroactive application adds the `state_label:` frontmatter key and the visible
banner to each; no body content of those documents changes. This is a Class-3 solo
documentation act (label application, no semantic change), recorded here for the
audit trail.

## 8. Scope and authority

This standard is `NORMATIVE` and binds the `intent-eval-lab` documentation surface. It
does not govern code, schemas, or per-repo CLAUDE.md files — those carry their own
versioning. Amendments to this standard route per Blueprint A § 2.3: adding or removing
a lifecycle label is a Class-2 act (CTO + VP DevRel pair) because it changes how the
entire documentation corpus is read; clarifying prose is a Class-3 solo act.

## 9. Cross-references

- Lifecycle labels for individual scope elements (capabilities, predicate types):
  `068-AT-STND-core-repo-boundaries-2026-06-18.md` § scope labels.
- Governance routing for label transitions: Blueprint A (`011-AT-ARCH`) § 2.3.
- Phase A/B/C lifecycle and "ratification" / "override" definitions:
  Canonical Glossary (`014-DR-GLOS`) §§ 4, 7.
- Filing convention (`NNN-CC-ABCD-<title>-<date>.md`): Document Filing Standard v4.3.
