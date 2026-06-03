# DR-039 — Evidence Bench: public scorecard direction (ratified)

**Date:** 2026-06-02
**Type:** AT-DECR (architectural decision record)
**Acting head:** Jeremy Longshore (CEO-mode delegation; enacted by Claude in autonomous-CTO mode)
**Status:** RATIFIED 2026-06-02
**Authority:** DR-035 (ISEDC Session 8 — labs dashboard architecture); DR-010 Q3 + § 5 (predicate-URI scoping, CISO binding); DR-018 (STAGING-STAYS-STAGING / per-predicate production-Rekor gate); snoopy-fluttering-comet plan § Move 1
**Bead:** `bd_000-projects-tr08.2` — CLOSED with this DR. Epic: `bd_000-projects-tr08`.
**Basis:** the scorecard, the signed result, and the supporting infrastructure described below are already SHIPPED and LIVE as of 2026-06-01. This DR ratifies the direction and records the binding constraints the implementation already honors.

---

## 0. Executive summary

The Intent Eval Platform now publishes a **public Evidence Bench scorecard** at
`labs.intentsolutions.io/eval-sets/j-rig-bench/`. Its first row — the Skill Refiner
Phase A.0 baseline (DR-036, PROCEED) — is rendered with a **signed, publicly
verifiable Evidence Bundle** anchored in the production sigstore transparency log
(Rekor log index `1689291334`). This DR ratifies that direction and locks the
constraints that keep it honest and on the right side of prior governance.

The scorecard exists to do one thing competitors selling unverifiable numbers cannot:
let any reader **cryptographically confirm a result was not altered after the fact**,
and trace it — in plain English — back to what was done and how. Reproducibility via
_signature_, on top of reproducibility via _transparency_.

---

## 1. Decision

**The public Evidence Bench scorecard is the ratified Move 1 surface.** It ships at
`labs.intentsolutions.io/eval-sets/j-rig-bench/` with a plain-English walkthrough at
`/eval-sets/j-rig-bench/phase-a0/`, and every published row links to a verifiable
public Rekor entry plus a self-serve `cosign verify-blob` command.

---

## 2. Ratified constraints (binding on every current + future scorecard row)

These are not aspirational — the live implementation already satisfies all of them.

1. **Different dimension, not a re-run of others.** The scorecard measures dimensions
   adjacent eval boards do not — provenance / attestability / (for memory systems)
   citation integrity. It **links to** peer boards (e.g. `gbrain-evals`) and does **not**
   restate or claim-to-beat their numbers. This is the anti-derivative guard from the
   2026-05-31 ground-truth review (HIGH-risk item): "signed" is the differentiator only
   if the _measured dimension_ is also distinct.

2. **No predicate URI declared at `labs.*`.** Published bundles are signed as **blobs**;
   `predicate_uri_set` is empty. The `skill-binary-eval/v1` predicate stays **reserved,
   not declared** — production-Rekor _predicate declaration_ remains gated (per DR-010 Q3
   - DR-018) on a normative SPEC.md + DNSSEC + CAA clearing for
     `evals.intentsolutions.io`, none of which have. (Verified 2026-06-01: `evals.*` has no
     DNSSEC and serves no TLS.) Predicate URIs live ONLY at `evals.*`, never `labs.*`.

3. **No aggregate PASS%** across heterogeneous predicates (inherits DR-035 C3). Enforced
   in CI by `scripts/regenerate.py` refusal regex + `deploy.yml` gate.

4. **Append-only signatures.** Evidence Bundles are signed once against the exact bytes at
   sign time; corrections are a _new_ bundle referencing the prior — never an in-place
   re-sign (kernel `evidence-bundle.schema.json` discipline). When a signed result's
   source docs are later annotated (e.g. the Phase A.0 frontmatter-only scope caveat added
   2026-06-01), the v1 signature stands as honest history and the annotation is disclosed,
   not hidden.

5. **Honest scope, stated on-artifact.** Every signed row states what the signature
   attests (artifact integrity + signer identity + time) and what it does NOT (it is not a
   claim the underlying result is "correct," and — where applicable — discloses the exact
   measurement scope). The Phase A.0 page carries the frontmatter-only-edit caveat publicly.

6. **Public deploy is GC-pre-pub gated.** Merging a scorecard change to `main` deploys it
   live; the flip-to-public on any named-technique comparative claim is gated on acting-head
   sign-off per the DR-035 GC pre-publication binding.

---

## 3. What is already live under this direction (as of 2026-06-01)

| Artifact                                                        | State                                                                                                                                                                                        |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scorecard page `labs.intentsolutions.io/eval-sets/j-rig-bench/` | LIVE (HTTP 200)                                                                                                                                                                              |
| Plain-English walkthrough `/eval-sets/j-rig-bench/phase-a0/`    | LIVE — question / method / 60-skill list / worked example / proof / honest scope                                                                                                             |
| Phase A.0 signed Evidence Bundle                                | Rekor log index `1689291334`, `cosign verify-blob ... Verified OK`                                                                                                                           |
| Signing workflow                                                | `intent-eval-lab/.github/workflows/sign-evidence-bundle.yml` (GitHub OIDC → Fulcio keyless → cosign sign-blob → production Rekor, self-verifying, deterministic + commit-independent bundle) |
| Source-doc consistency                                          | RESULTS.md + DR-036 annotated with the frontmatter-only scope caveat (PR #95)                                                                                                                |

Bead trail: `tr08.1` (scorecard, CLOSED), `tr08.24` (signing, CLOSED), `tr08.3` (repo
topics/homepage, CLOSED), this DR closes `tr08.2`.

---

## 4. Anti-goals (what this scorecard is NOT)

- Not a leaderboard of aggregate scores (DR-035 C3).
- Not a predicate-URI declaration surface (DR-010 § 5 CISO binding).
- Not a marketing board — the board may not claim provenance it does not hold; a row reads
  `pending` until its signature is real.
- Not a re-implementation of any peer eval board's dimension.

---

## 5. Cross-references

- DR-035 — ISEDC Session 8, labs dashboard architecture (the parent binding)
- DR-036 — Phase A.0 PROCEED result (the first scorecard row's underlying result)
- DR-010 / DR-018 — predicate-URI scoping + production-Rekor per-predicate gate
- Plan: `~/.claude/plans/snoopy-fluttering-comet.md` § Move 1
- Evidence: `intent-eval-lab/evidence/phase-a-0-baseline/` (bundle + signature + verification guide)
