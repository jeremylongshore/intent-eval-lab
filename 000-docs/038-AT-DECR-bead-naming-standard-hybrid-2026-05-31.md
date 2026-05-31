# DR-038 — IS Bead Naming Standard: HYBRID (title-codes + minimal-prefix IDs + KB labels)

**Date:** 2026-05-31
**Type:** AT-DECR (architectural decision record)
**Acting head:** Jeremy Longshore (CEO-mode delegation; ratification enacted 2026-05-31 by Claude in autonomous-CTO mode per `/goal` directive)
**Status:** RATIFIED 2026-05-31 (proposed standard; no retroactive renames — applies to NEW beads after ratification)
**Authority:** Research epic `bd_000-projects-lmiy` — investigation of upstream `gastownhall/beads` naming docs + IS internal divergence
**Pre-flight basis:** `gastownhall/beads/docs/{ADAPTIVE_IDS,COLLISION_MATH,CONTRIBUTOR_NAMESPACE_ISOLATION}.md` + IS umbrella CLAUDE.md plain-English-titles SOP + `/doc-filing` standard precedent

---

## 0. Executive summary

Adopt a **HYBRID** standard for IS bead naming that combines:

1. **Upstream-compatible system IDs** — short hex prefix following gastownhall/beads adaptive-ID convention (e.g., `bd-7f3a`, `iel-a9c1`, `iep-puxu`). Per-knowledge-base prefix chosen per workspace (NOT embedded in title).
2. **Plain-English titles** — current IS SOP (full-sentence imperative-mood) PRESERVED. Optionally prefixed with a categorical code from a controlled vocabulary (mirrors `/doc-filing`).
3. **Knowledge-base labels** — `kb:ics`, `kb:qmd`, `kb:iep`, `kb:partner-portals`, etc. as labels on every bead. Enables cross-KB queries without polluting IDs.
4. **Cross-KB external_refs** — `external:<kb>:<id>` linking semantics for beads that reference work in another knowledge base.

This standard:
- Aligns with gastownhall/beads upstream conventions (no breaking changes if we ever push to that ecosystem)
- Preserves the 2026-05-22 plain-English-titles SOP (no regression)
- Mirrors `/doc-filing`'s discipline (optional title-prefix codes for searchability + categorization)
- Adds cross-KB navigation that doesn't exist today
- No retroactive renames (existing beads keep their current IDs + titles)

---

## 1. The standard (binding for new beads from 2026-06-01)

### 1.1 System IDs

| Knowledge base | Workspace prefix | Example ID |
|---|---|---|
| `intent-eval-platform` (IEP umbrella) | `iep-` (proposed) — current `bd_000-projects-` retained for legacy compatibility | `iep-7f3a`, legacy `bd_000-projects-puxu` |
| `intentional-cognition-os` (ICOS) | `ics-` (proposed) — current `intentional-cognition-os-` retained for legacy | `ics-a9c1` |
| `qmd-team-intent-kb` (QMD) | `qmd-` | `qmd-2bef` |
| `partner-portals` | `pp-` | `pp-4d5e` |
| Future knowledge bases | One-word kebab-case prefix, 3-5 chars | — |

**Sub-bead notation** (parent.N) per gastownhall/beads upstream — PRESERVED. `iep-puxu.3`, `ics-a9c1.2`, etc.

**Adaptive length** per upstream `COLLISION_MATH.md` — let bd choose 4/5/6-char hex per workspace size. Don't manually pin.

### 1.2 Title structure

```
[<CODE>: ] <imperative-mood sentence describing the work>
```

Where `<CODE>` is OPTIONAL and drawn from this controlled vocabulary (mirrors `/doc-filing` code semantics):

| Code | Use for |
|---|---|
| `RR` | Research / recon (landscape survey, literature review) |
| `PP` | Planning (multi-step plan authoring) |
| `IMPL` | Implementation (code, infra, deploy) |
| `AUDIT` | Audit / review (post-hoc inspection of existing work) |
| `DR` | Decision-related (drafting an AT-DECR doc) |
| `REFINE` | Iteration on existing work (refactor, polish) |
| `OPS` | Operational (one-off ops task, no code or doc deliverable) |
| `RELS` | Release / version cut |
| `TEST` | Testing infrastructure or specific test work |
| `DEFER` | Marked as deferred — usually short-lived in OPEN state |

**Code OPTIONAL — plain-English-no-code titles remain valid.** Don't force a code if it doesn't fit. Codes are for searchability + filtering, not gatekeeping.

**Examples:**

```
✓ Build the daily-cron regenerator that auto-refreshes eval-set pages
✓ IMPL: Build the daily-cron regenerator that auto-refreshes eval-set pages
✓ RR: Survey NVIDIA SkillSpector + adjacent skill-evaluation projects
✓ DR: File ISEDC decision record on Phase A.0 PROCEED outcome
✓ Phase A.0 baseline experiment naive-Opus-in-context vs Refiner stub
```

### 1.3 Labels

**Mandatory `kb:<knowledge-base>` label** on every bead from 2026-06-01:

```
kb:ics    bead in intentional-cognition-os workspace
kb:qmd    bead in qmd-team-intent-kb workspace
kb:iep    bead in intent-eval-platform workspace
kb:pp     bead in partner-portals workspace
```

This enables cross-KB queries via `bd list --label kb:iep` from any context.

**Topic labels** (1-3 plain-English words) PRESERVED per current SOP. Examples: `dashboard`, `phase-a-0`, `ingest`, `refiner`, `automation`.

**Anti-labels** (forbidden, per current SOP): no `epic:N`, no `type:X`, no `E#-B##` codes.

### 1.4 Cross-knowledge-base references

When a bead in one KB references work in another KB:

```
bd dep add <local-id> --depends-on "external:<kb>:<remote-id>"
```

Example: a Skill Refiner blog draft in QMD that references the Phase A.0 result in IEP:

```
bd dep add qmd-blog-skillref --depends-on "external:iep:bd_000-projects-214c.8"
```

This follows the existing `external_refs` mechanism in bd (per ADAPTIVE_IDS.md upstream).

---

## 2. What changes vs status quo

| Element | Status quo | New standard | Migration |
|---|---|---|---|
| System ID prefix | `bd_000-projects-<3char>` (IEP); `intentional-cognition-os-<3char>` (ICOS); `qmd-team-intent-kb-<3char>` (QMD) | Short prefix `iep-`, `ics-`, `qmd-` (NEW) | Legacy IDs retained; new beads use new prefix. No retroactive rename. |
| Title | Plain-English imperative sentence | Same + OPTIONAL leading code (RR/PP/IMPL/...) | Existing beads not renamed; new beads may add codes |
| `kb:` label | Not present | Mandatory on new beads | Existing beads grandfathered |
| Topic labels | Plain-English 1-3 words | Same — unchanged | n/a |
| Cross-KB linking | Inconsistent (manual mention in notes) | `external:<kb>:<id>` formal external_refs | Optional retrofit for important cross-refs |
| Plain-English-title SOP | Binding from 2026-05-22 | Preserved (codes additive, not replacing) | n/a |

**Migration policy:** Grandfather-and-go-forward. NO retroactive renames. Existing 781 IEP beads + ICOS + QMD beads keep their current IDs + titles. New beads from 2026-06-01 follow this standard.

---

## 3. Upstream-compatibility analysis

`gastownhall/beads` upstream conventions (per `docs/ADAPTIVE_IDS.md` + `docs/COLLISION_MATH.md`):

| Convention | Upstream default | IS new standard | Compatible? |
|---|---|---|---|
| ID format | `<prefix>-<4to8 hex>` | `<prefix>-<4to8 hex>` | ✓ matches |
| Default prefix | `bd-` (customizable per workspace) | Per-KB prefix (`iep-`, `ics-`, etc.) | ✓ — custom prefix is upstream-supported |
| Adaptive length | Birthday-paradox auto-scaling | Inherits upstream behavior | ✓ matches |
| Sub-bead notation | `parent.N` | `parent.N` | ✓ matches |
| Title shape | Free-form `"Title"` | Plain-English + optional code prefix | ✓ — codes are still free-form within upstream's rules |
| Labels | Free-form | Plain-English + mandatory `kb:` | ✓ matches |
| External refs | `external:<project>:<capability>` | `external:<kb>:<id>` | ✓ matches |

**Result:** the IS standard is a SUPERSET of upstream conventions with no breaking divergence. If we ever migrate to a shared bd registry across organizations, the IS standard plays clean.

---

## 4. Why this layered approach

### Why not just adopt upstream `bd-` everywhere?
Loses cross-KB disambiguation in IDs. If both ICOS and IEP use `bd-`, then `bd-7f3a` is ambiguous without context. The per-KB prefix solves this without breaking upstream compatibility.

### Why not use `/doc-filing` codes mandatorily?
Most beads don't fit cleanly into a single category. Forcing codes creates classification ambiguity ("is this IMPL or REFINE?"). Making codes optional captures the discipline benefits without imposing classification overhead.

### Why preserve plain-English titles?
The 2026-05-22 SOP was deliberate — beads that say "v0.2 metrics: paraphrase_robustness in verify.py + render-summary.py" become unparseable two days later. Plain English self-documents. Codes are additive search aids, not replacements.

### Why mandatory `kb:` labels?
Currently the workspace prefix IS the cross-KB disambiguator (`bd_000-projects-` vs `intentional-cognition-os-`). When we shorten prefixes to `iep-` / `ics-`, the disambiguator becomes shorter and easier to miss. The `kb:` label gives an explicit filtering surface (`bd list --label kb:iep`) and survives prefix renames in the future.

### Why grandfather instead of retroactive rename?
The CLAUDE.md rule from 2026-05-22 explicitly says "Old beads from numbered execution plans remain historically valid under their old titles. Do not retroactively rename." Same principle applies to IDs — the audit trail benefits from stable identifiers over time.

---

## 5. Implementation directives

1. **Document this standard in the IS umbrella `CLAUDE.md`** (`~/000-projects/CLAUDE.md` — PRIVATE) under a new "Bead naming standard (HYBRID v1)" section. Reference DR-038 for the binding rationale.
2. **Per-KB workspace prefix config updates** (when convenient — not blocking):
   - IEP: configure new bd workspace prefix `iep-` in `~/000-projects/.beads/config.yaml`
   - ICOS: configure `ics-` in `intentional-cognition-os/.beads/config.yaml`
   - QMD: configure `qmd-` in `qmd-team-intent-kb/.beads/config.yaml`
   - Document the workspace-prefix change as a per-workspace bead with a `OPS: workspace-prefix-rename` title for audit trail
3. **Update bd-sync tooling** (if needed) to handle short prefixes — confirm `~/bin/bd-sync` works without change (suspect: it does, since it operates by ID string match)
4. **Future bead authoring** (new beads from 2026-06-01) follows this standard. No retroactive work.
5. **Close research epic `bd_000-projects-lmiy`** with this DR as evidence.

---

## 6. What this DOES NOT change

- Existing 781+ IEP/ICOS/QMD bead titles + IDs remain unchanged. No retroactive churn.
- `bd-sync` 3-layer mirror discipline (bd ↔ GH ↔ Plane) preserved.
- Plain-English title SOP from 2026-05-22 preserved (codes are additive).
- The "every bead has a parent epic OR is a <15-min standalone chore" rule preserved.
- `/doc-filing` standard for documents is INDEPENDENT of this; not affected.

---

## 7. Hard refusals

- **No retroactive rename of existing beads.** Audit trail discipline.
- **No mandatory title codes.** Plain-English titles remain valid.
- **No abandoning the `kb:` label** once instituted. The cross-KB query surface is the whole point of the label discipline.
- **No prefix duplication across KBs.** Each KB picks one prefix, locked.

---

## 8. Open follow-ups (filed after this DR ships)

| Item | Priority |
|---|---|
| Update IS umbrella `~/000-projects/CLAUDE.md` (PRIVATE) with HYBRID standard summary | P2 |
| Configure new workspace prefix in IEP `.beads/config.yaml` | P3 |
| Configure new workspace prefix in ICOS `.beads/config.yaml` | P3 |
| Configure new workspace prefix in QMD `.beads/config.yaml` | P3 |
| Audit existing labels for compliance + add `kb:<name>` to in-flight beads | P3 |

These follow-ups are operational; not blocking. The standard is BINDING from 2026-06-01 regardless of when the operational follow-ups land.

---

## 9. Signature

Acting head: **Jeremy Longshore** (CEO-mode delegation; ratification enacted 2026-05-31 by Claude in autonomous-CTO mode per `/goal` directive)
Research epic closed with this DR: `bd_000-projects-lmiy`
Adversarial-integrity protocol: not formally invoked (organizational standard; no architectural binding affected; outcome preserves existing 2026-05-22 plain-English-titles SOP).
