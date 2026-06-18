---
title: DR-082 Erratum — skill-refiner-pass/v1 freeze-point doctrine + amend-in-place
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: DR-085 D2 (Q2, 7-0) — amend skill-refiner-pass/v1 in place; freeze = first production-Rekor signature
amends: 082-AT-DECR-isedc-skill-refiner-pass-v1-predicate-uri-2026-06-17.md
issued_under: ISEDC Corrective Council — IEP Kernel One-Way-Door Correction (DR-085)
filing_standard: Document Filing Standard v4.3
related_docs:
  - 082-AT-DECR-isedc-skill-refiner-pass-v1-predicate-uri-2026-06-17.md (the record this erratum amends)
  - 085-AT-DECR-isedc-kernel-onewaydoor-correction-2026-06-17.md (DR-085 — the corrective council; D2 is the source decision)
  - 087-AT-STND-ratified-clause-conflict-halt-gate-2026-06-18.md (sibling D1 standard)
related_drs:
  - 082-AT-DECR (DR-082 — minted the URI; Q3 staging-first; Q5 originally froze v1 at SPEC.md-landing)
  - 085-AT-DECR (DR-085 — D2 corrects the freeze point + authorizes amend-in-place)
state_element_status: CURRENT
---

> **State label: NORMATIVE.** This is a recorded erratum to DR-082 (a Class-1
> immutable-artifact record), issued under the authority of DR-085 D2. It does not
> re-open DR-082's ratified decisions; it corrects DR-082's Q5 freeze-point wording,
> records the no-prior-signature attestation that makes amend-in-place legitimate, and
> notes the verbatim body-shape changes applied per DR-085 D2–D5.

# DR-082 Erratum — `skill-refiner-pass/v1` Freeze-Point Doctrine + Amend-in-Place

**Beads:** filed under the refiner/kernel epics per DR-085 § 11.4; mirrored via `bd-sync`.
**Amends:** DR-082 (`082-AT-DECR-isedc-skill-refiner-pass-v1-predicate-uri-2026-06-17.md`).
**Issued under:** DR-085 D2 (`085-AT-DECR-isedc-kernel-onewaydoor-correction-2026-06-17.md`).

## 0. Why this erratum exists

A 3-reviewer adversarial glance (code-reviewer + `martin-kleppmann-reviewer` +
`rich-hickey-reviewer`) on the **merged-but-unpublished** kernel PRs #56 (the
`skill-refiner-pass/v1` predicate) and #57 (the `SkillVersion` 14th entity) found
one-way-door defects in the body shape DR-082 ratified. The corrective ISEDC council
(DR-085) ruled **7-0 (D2, Q2)** to **amend `skill-refiner-pass/v1` in place** rather than
mint `/v2`, because nothing had ever been signed into the **production** Rekor
transparency log — the immutability cost had not yet been incurred.

DR-082 § 6 Q5 had written the freeze event as attaching **at SPEC.md-landing** (CISO Q5
position, line 140: *"v1 is FROZEN at SPEC.md-landing"*). DR-085 D2 supersedes that wording.
This erratum records the corrected doctrine, the attestation that legitimizes the
amend-in-place, and the body changes that were applied.

## 1. (a) The FREEZE-POINT DOCTRINE (binding on all staging-first predicates)

DR-085 D2 establishes, and this erratum records as NORMATIVE doctrine binding **every**
staging-first predicate on `evals.intentsolutions.io`:

1. **"Frozen" attaches at the first production-Rekor signature — NOT at ratification, and
   NOT at SPEC.md-landing.** The transparency log is the only real freeze; everything
   upstream of a production signature is correction surface (DR-085 CSO memo:
   *"The transparency log is the only real freeze; everything upstream of a production
   signature is correction surface."*).
2. **Amend-in-place is permitted ONLY while `signing_mode = sigstore_staging` (the canonical
   staging label per DR-085 D4; legacy alias `ln`) AND zero production-Rekor entries exist**
   for the predicate. Under those two conditions the body shape may be corrected without a
   URI bump.
3. **The first production-Rekor signature is the irrevocable freeze.** After it fires, the
   body is frozen by the append-only physics of the log, not by policy. From that instant
   forward, every correction follows DR-082 Q5 unchanged: any add/loosen → Class-1 ISEDC;
   any breaking change → a NEW URI `skill-refiner-pass/v2` on its own `$schemaVersion` lane;
   v1 rows in the wild remain valid forever and are never reinterpreted in place.
4. **This doctrine binds ALL staging-first predicates**, not only `skill-refiner-pass/v1`.
   It reconciles DR-082's strict immutability discipline (Q5) with the operational reality
   that a staging predicate which has never been production-signed has incurred no
   immutability cost and is therefore still correctable.

**Net effect on DR-082 Q5:** the Q5 *evolution* rule (add/loosen = Class-1, breaking =
`/v2`, v1 never mutates in place) stands unchanged **as of the first production signature**.
The only correction is *when the clock starts*: the freeze attaches at first
production-Rekor signature, not at SPEC.md-landing. The CISO Q5 phrasing
("FROZEN at SPEC.md-landing", DR-082 line 140) and the CTO Q5 phrasing
("the freeze event is named at FIRST PRODUCTION-SIGNED ROW", DR-082 line 135) were in latent
tension inside DR-082 itself; DR-085 D2 resolves it in favor of the first-production-signature
reading.

## 2. (b) Attestation — NO production-Rekor signature ever existed for the pre-amendment shape

Issued per the GC/CISO binding in DR-085 D2 ("an auditable 'no production signature ever
existed for the pre-amendment shape' attestation"):

> **ATTESTATION (auditable).** As of the date of this erratum (2026-06-18), **no
> production-Rekor signature has ever existed** for the pre-amendment `skill-refiner-pass/v1`
> body shape. Specifically:
>
> - The predicate ran exclusively at `signing_mode = ln` / `sigstore_staging`
>   (sigstore staging only). Per DR-082 Q3, `skill-refiner-pass/v1` ships staging-first and
>   becomes production-signable ONLY when all four AND-gated triggers hold (SPEC.md normative
>   section lands; DNSSEC+CAA pre-flight green on `evals.intentsolutions.io`; the authoring
>   chamber's SEPARATE signing trust root is provisioned-and-live; ≥1 real SkillVersion clears
>   the behavioral gate on a frozen, signed eval-set). Those triggers have **not** all been
>   met — in particular the authoring chamber's separate signing trust root is **not yet
>   provisioned** (DR-085 holds intent-eval-lab PR #171, the SPEC.md + authoring signing-root,
>   until D1–D5 land).
> - PRs **#56 and #57 were merged but unpublished**; they were **not ancestors of the
>   published `@intentsolutions/core` v0.7.0 tag**. No `@intentsolutions/core` tag carrying the
>   pre-amendment shape was ever published, so no consumer ever signed a production row against
>   it.
> - There is therefore **zero production logIndex** referencing the pre-amendment shape. The
>   amend-in-place precondition in § 1.2 (`signing_mode = staging` AND zero production-Rekor
>   entries) is satisfied by construction.

This attestation is the auditable basis on which the amend-in-place is legitimate rather than
a retroactive edit of a frozen artifact: there was nothing frozen to edit.

## 3. (c) Body-shape amendments applied in place (per DR-085 D2–D5)

The `skill-refiner-pass/v1` body shape DR-082 Q2 ratified was amended in place — URI string
**unchanged** (`https://evals.intentsolutions.io/skill-refiner-pass/v1`, the flat sibling of
`gate-result/v1` confirmed in DR-082 Q1) — per the structural-integrity decisions of DR-085:

| Change | Source decision | What changed (verbatim intent) |
|---|---|---|
| **Nullable parent** | DR-085 D3 (Q3, 7-0) | The predicate's `parent_version_id` becomes **nullable** to match the entity, so a root attests without forging a parent; root emission is provably zero-forgery (`null parent_version_id` + `null parent_content_hash`). |
| **`result_snapshot_hash`** | DR-085 D4 (Q4, 7-0) | A distinct `result_snapshot_hash` (post-edit output) is added to the predicate; `source_snapshot_hash` now means **pre-edit input** consistently across entity + predicate (name retained, not renamed on both sides — CISO minimize-diff). |
| **`sigstore_staging` label** | DR-085 D4 (Q4, 7-0) | Canonical staging `signing_mode` = **`sigstore_staging`** across all predicates; `ln` is retired with a changelog alias + a canonical-label registry entry. |
| **Three-layer enforcement** | DR-085 D5 (Q5, 7-0) | Every signed cross-field invariant is machine-enforced at all three layers (JSON-Schema `if/then` + Zod `superRefine` + Pydantic `model_validator`) before v0.8.0: `accept ⇒ every named_dimension_delta.non_regressed = true`; `version_kind ∈ {revert,restore} ⇒ parent_version_id ≠ null`; Python optional-not-nullable parity. A standing kernel CI gate ("no unenforced invariant on a signed row," scoped to predicate/entity schemas) is established. |

These amendments are the body-shape corrections; the kernel-side implementation (schema +
Zod + Pydantic + tests) lands on the same `@intentsolutions/core` v0.8.0 tag per DR-085
§ 11.2 ("BLOCK any `@intentsolutions/core` tag/publish until D1–D5 land; the next tag is
`v0.8.0` carrying the corrections").

## 4. What this erratum does NOT change

- **The URI string.** Unchanged: `https://evals.intentsolutions.io/skill-refiner-pass/v1`,
  flat (DR-082 Q1, 7-0).
- **The staging-first / four-trigger production gate.** Unchanged (DR-082 Q3, 7-0).
- **The in-toto alignment.** Unchanged — mirror `gate-result/v1` exactly (DR-082 Q4, 7-0).
- **The Q5 evolution rule once production signing unlocks.** Unchanged: add/loosen =
  Class-1 ISEDC, breaking = `/v2`, v1 never mutates in place. The only correction is the
  *freeze-point* (§ 1): the rule attaches at first production-Rekor signature.

## 5. References

- DR-082: `082-AT-DECR-isedc-skill-refiner-pass-v1-predicate-uri-2026-06-17.md` — the Class-1
  record minting the URI; Q3 staging-first; Q5 originally froze v1 at SPEC.md-landing.
- DR-085: `085-AT-DECR-isedc-kernel-onewaydoor-correction-2026-06-17.md` — the corrective
  council; D2 (Q2, 7-0) is the source decision authorizing this erratum.
- Sibling standard (D1): `087-AT-STND-ratified-clause-conflict-halt-gate-2026-06-18.md`.
- Glance input: code-reviewer + `martin-kleppmann-reviewer` + `rich-hickey-reviewer`
  adversarial second-look on PRs #56 / #57 (DR-085 § 14).
