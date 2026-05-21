# Schema Repoint — Lab → Kernel (Priority 5 closeout)

**Filing**: 019-AA-AACR-schema-repoint-iel-link-schemas-2026-05-21.md
**Date**: 2026-05-21
**Author**: Jeremy Longshore (CTO + beads work; executed by Claude per CEO-mode delegation)
**Beads closed by this AAR**: `iel-link-schemas-to-kernel` (`bd_000-projects-i4jh`, P1), `iel-link-schemas-blueprint-b` (`bd_000-projects-v1ao`, P1), `iel-link-schemas-glossary` (`bd_000-projects-7vvz`, P2), `iel-link-schemas-drift-ci` (`bd_000-projects-1zr1`, P1)
**Cluster**: IEP Convergence Debt Plan Priority 5 — lab schema repoint
**Authority**: ISEDC Session 5 DR 018 § 6.4 (Option α-minus); Blueprint B § 7.0 (new schema-authority sub-section landing in this PR)

---

## 1. What this AAR records

Priority 5 of the IEP Convergence Debt Plan is the lab-side schema migration: replace the duplicated `gate-result/v1` JSON Schema content at `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/` with a redirect to the kernel's canonical schema at `@intentsolutions/core/schemas/v1/gate-result.schema.json`. The migration is independent of the j-rig P1 unblocking work (ISEDC Session 5 ratified Q2 for the j-rig schema upgrade; Priority 5 implements the lab side of the same architectural principle for the lab's own copy of the schema).

## 2. What changed

| # | Change | File | Reason |
|---|---|---|---|
| 1 | Replaced normative schema content with redirect stub (valid JSON Schema 2020-12; `$ref` to kernel; `x-redirect` marker; description-as-comment block) | `specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` | Kernel is canonical per DR 018 Option α-minus; lab MUST NOT host normative schema content |
| 2 | Rewrote README to describe the redirect + cross-link the canonical sources + migration history | `specs/evidence-bundle/v0.1.0-draft/schema/README.md` | Discoverability for consumers following old links |
| 3 | Added "Schema-authority notice" block at top of SPEC | `specs/evidence-bundle/v0.1.0-draft/SPEC.md` | The lab spec page remains the public-facing mirror but explicitly cedes normative authority to the kernel |
| 4 | Added new § 7.0 "Schema authority (effective 2026-05-21)" to Blueprint B; updated § 7.4 + § 7.6 + versioning-policy references to point to the kernel as canonical | `000-docs/012-AT-ARCH-platform-runtime-blueprint.md` | Reverses the 2026-05-11 "lab JSON Schema file wins" framing; the kernel schema now wins |
| 5 | Updated `EvidenceBundle` entry + `Predicate URI` entry + `Active predicate types` entry to cite kernel canonical surface | `000-docs/014-DR-GLOS-canonical-glossary.md` | Glossary is the platform's single source of truth for term canonical sites |
| 6 | NEW: schema-drift CI workflow that fails any PR re-introducing normative schema content under `specs/evidence-bundle/*/schema/` | `.github/workflows/schema-drift.yml` | Structural enforcement of DR 018 Option α-minus; allowlist for redirect stubs via `x-redirect` marker |
| 7 | Filed this AAR | `000-docs/019-AA-AACR-schema-repoint-iel-link-schemas-2026-05-21.md` | Closeout per IEP Convergence Debt Plan Priority 5 acceptance criteria |
| 8 | Updated `000-INDEX.md` | `000-docs/000-INDEX.md` | New entry 019; new mention of Priority 5 work |

## 3. What did NOT change

- **Predicate URI namespace** `https://evals.intentsolutions.io/gate-result/v1`: unchanged, immutable per Blueprint B § 7.2.
- **Normative predicate body shape**: unchanged; Blueprint B § 7.4 already locked it via the 5-PR Phase A foundation merge on 2026-05-15.
- **Sigstore staging vs production-Rekor unlock posture**: unchanged; still gated on iah-E06 DNSSEC + CAA pre-flight per DR-010 Q3 CISO non-negotiable.
- **Lab `SPEC.md` prose tables in § 5**: the § 5 prose tables in `SPEC.md` still describe the v0.1.0-draft shape (`result` / `timestamp` / fewer required fields). They were authored before Blueprint B § 7.4 normative-fold landed. **Updating those § 5 tables to mirror the kernel's normative shape is out of scope for Priority 5 work** — that's a separate documentation-cleanup track (will be filed as a P2 follow-up bead). The new schema-authority notice at the top of SPEC.md tells readers explicitly that the kernel wins on conflict, which prevents the now-stale § 5 tables from being treated as canonical.

## 4. Verification

- **JSON validity**: `python3 -c "import json; json.load(open('specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json'))"` returns clean.
- **Redirect stub conformance** (matches schema-drift CI gate locally): file has top-level `x-redirect`; declares zero canonical predicate-field properties; `$ref` forwards to `https://raw.githubusercontent.com/jeremylongshore/intent-eval-core/main/schemas/v1/gate-result.schema.json`.
- **Partner-name guard**: `.github/workflows/partner-name-guard.yml` returns clean against this AAR + the updated docs (zero hits; pattern sourced from private umbrella per DR-004 S1Q2).
- **Blueprint B § 7.0 + § 7.4 + § 7.6**: the path references to the lab schema have been updated to point at the kernel for normative validation; the lab stub is referenced only as a redirect.
- **Glossary § 2.4 + Predicate URI + Active predicate types**: each cites the kernel canonical surface.
- **CI workflow**: `.github/workflows/schema-drift.yml` is YAML-valid and runs on PR + push to main.

## 5. Sequencing notes

This work landed BEFORE `iec-E12` (the kernel v0.2.0 EvidenceBundlePayload epic) ships. That's fine and intended: the kernel's existing `gate-result.schema.json` at v0.1.0 is already the canonical source for the predicate body (which is what this AAR migrates to). The forthcoming `iec-E12` work adds the `EvidenceBundlePayload` wire-format envelope around the predicate; it does not change the predicate body shape, which is already locked.

When `iec-E12` lands kernel v0.2.0, the lab will optionally:

1. Add a redirect stub at `specs/evidence-bundle/v0.1.0-draft/schema/evidence-bundle.schema.json` (or similar path) per the same pattern this AAR establishes.
2. Update the glossary `EvidenceBundle` entry to reference `EvidenceBundlePayload` once it ships.
3. Update Blueprint B with a § 7.8 (or similar) for the bundle-envelope contract.

Those are follow-on items NOT in Priority 5 scope and will be tracked via the `iec-E12` child cluster + `iel-predicate-types-evidence-bundle-payload` (`bd_000-projects-im30`).

## 6. Dependencies + linkages

- **Authority chain**: DR 018 § 6.4 (Option α-minus ratification) → Blueprint B § 7.0 (new schema-authority sub-section, landing in this PR) → this AAR (closeout)
- **Bead lineage**:
  - `iep-P5-lab-schema-repoint` (`bd_000-projects-xxx` — to be filed when Plane-LAB-95 mirror lands; treated as closed-by-this-AAR per Plane catch-up workflow)
  - `iel-link-schemas-to-kernel` (`bd_000-projects-i4jh`) — schema file replacement: COMPLETE
  - `iel-link-schemas-blueprint-b` (`bd_000-projects-v1ao`) — Blueprint B § 7 update: COMPLETE
  - `iel-link-schemas-glossary` (`bd_000-projects-7vvz`) — Canonical Glossary kernel pointers: COMPLETE
  - `iel-link-schemas-drift-ci` (`bd_000-projects-1zr1`) — CI drift-check gate: COMPLETE
- **Downstream beads NOT closed here** (deferred to other tracks):
  - `iec-E12` cluster — kernel v0.2.0 `EvidenceBundlePayload` (gated on CISO invariant enumeration + audit-harness 2nd-emitter sketch per DR 018 § 6.4 binding precondition)
  - `iaj-E02` cluster — j-rig schema upgrade to kernel-normative shape (gated on `iec-E12` release)
  - `iel-predicate-types-evidence-bundle-payload` — PREDICATE-TYPES.md registry entry (gated on `iec-E12` release)
  - SPEC.md § 5 prose-table cleanup — separate P2 follow-up bead to be filed

## 7. Risks + open issues

| Risk | Likelihood | Mitigation |
|---|---|---|
| SPEC.md § 5 prose tables remain stale (encode old shape) and a reader treats them as canonical | Medium | New schema-authority notice at top of SPEC.md tells readers "kernel wins on conflict"; § 5 tables are flagged for follow-up cleanup. |
| Future contributor edits the lab schema redirect stub thinking they're editing the canonical | Low | CI drift-check guard catches normative-field reintroduction; README in `schema/` explicitly forbids edits. |
| Cross-origin `$ref` resolution fails for some JSON Schema validators (e.g. validators that don't follow remote refs) | Low | The README directs implementers to fetch the kernel schema directly; the `$ref` is a discoverability nicety, not a load-bearing validation path. |
| Drift-check CI workflow fires false positives on a future, legitimate predicate-URI schema landing in lab `specs/` | Low | The workflow allowlists `x-redirect` stubs; any future predicate schema landing in lab `specs/` SHOULD be a redirect stub anyway per Blueprint B § 7.0. |

## 8. References

- DR 018 — ISEDC Session 5 — `000-docs/018-AT-DECR-isedc-council-session-5-jrig-reconciliation-2026-05-21.md`
- 017-RR-LAND shape reconciliation addendum — `000-docs/017-RR-LAND-shape-reconciliation-addendum-2026-05-21.md`
- 016-RR-LAND kernel shadow inventory — `000-docs/016-RR-LAND-kernel-shadow-inventory-2026-05-20.md`
- Blueprint B § 7.0 (new) — `000-docs/012-AT-ARCH-platform-runtime-blueprint.md`
- Canonical Glossary § 2.4 + Predicate URI + Active predicate types — `000-docs/014-DR-GLOS-canonical-glossary.md`
- DR-010 § 7 Q3 (unification thesis BINDING) — `000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md`
- Kernel canonical schema — https://github.com/jeremylongshore/intent-eval-core/blob/main/schemas/v1/gate-result.schema.json
- Kernel npm package — https://www.npmjs.com/package/@intentsolutions/core

— Jeremy Longshore
intentsolutions.io
