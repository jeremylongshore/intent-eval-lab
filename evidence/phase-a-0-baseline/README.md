# Phase A.0 Evidence Bundle — signed, publicly verifiable

This directory holds the signed Evidence Bundle for the **Skill Refiner Phase A.0**
null-hypothesis baseline result (DR-036, PROCEED).

## What is here

> **SIGNED 2026-06-01.** Rekor log index **1689291334** — [view the raw transparency-log entry](https://rekor.sigstore.dev/api/v1/log/entries?logIndex=1689291334). Signer identity: `github.com/jeremylongshore/intent-eval-lab/.github/workflows/sign-evidence-bundle.yml@refs/heads/main`. Verified `Verified OK` against production sigstore.
>
> **Annotation note (post-signing, 2026-06-01).** After signing, `RESULTS.md` and the
> DR-036 decision record were annotated with a **frontmatter-only scope caveat** (disclosing
> that both arms edited only the SKILL.md frontmatter while the judge scores the whole skill).
> This added **disclosure only — no result or number changed.** The signed bundle therefore
> attests the *pre-annotation* bytes of those two files (digests `35caf7e3…` for RESULTS.md and
> `1af9e9be…` for DR-036), which is correct: a signature freezes exact bytes at sign-time.
> Per the kernel's append-only Evidence Bundle discipline, a correction is a *new* bundle
> referencing the prior one — never an in-place re-sign — so v1 stands as the honest historical
> attestation and the next signature is produced at the next substantive result (Phase A.1).


| File | What it is |
|---|---|
| `evidence-bundle.json` | The canonical Evidence Bundle. Names the four Phase A.0 result artifacts by their SHA-256 digests. Conforms to [`@intentsolutions/core` `schemas/v1/evidence-bundle.schema.json`](https://github.com/jeremylongshore/intent-eval-core/blob/main/schemas/v1/evidence-bundle.schema.json). |
| `evidence-bundle.sigstore.json` | The sigstore bundle (`--new-bundle-format`): Fulcio certificate chain + signature + Rekor inclusion proof. Produced by the `Sign Evidence Bundle (Phase A.0)` GitHub Actions workflow. *(present after the signing run)* |

## What the signature attests — and what it does not

**Attests:** the exact bytes of the four Phase A.0 result artifacts — `decision.json`,
`statistics.json`, `RESULTS.md`, and the DR-036 decision record — existed and were
signed at a specific time, under the GitHub Actions **workflow identity**
`github.com/jeremylongshore/intent-eval-lab/.github/workflows/sign-evidence-bundle.yml`,
anchored in the **public production Rekor transparency log** (`rekor.sigstore.dev`).
This is keyless signing: no long-lived private key exists; the signer is the
reproducible CI identity, not a person's laptop.

**Does NOT attest:**

1. **It declares no predicate URI.** `cosign sign-blob` signs raw bytes. The
   `predicate_uri_set` in the bundle is **empty by design**. The
   `evals.intentsolutions.io/skill-binary-eval/v1` predicate is **reserved, not
   declared** — production-Rekor *predicate declaration* is gated (per DR-018 and
   DR-010 Q3) on a normative SPEC.md + DNSSEC + CAA clearing for
   `evals.intentsolutions.io`, none of which have. A blob signature attests file
   integrity + identity + time; it is **not** a predicate-conformance claim.
2. **It does not claim the statistics are "correct."** A signature proves the
   artifacts are authentic and unaltered. The validity of the result stands on
   the pre-registered analysis in `RESULTS.md` and DR-036 — not on the signature.

This distinction is the whole point of an audit-first posture: we sign what we can
honestly attest (integrity + provenance), and we do **not** dress a signature up as
a claim it cannot support.

## Verify it yourself

You need [`cosign`](https://docs.sigstore.dev/cosign/installation/) (no account, no
keys). From this directory:

```bash
cosign verify-blob \
  --new-bundle-format \
  --bundle evidence-bundle.sigstore.json \
  --certificate-identity 'https://github.com/jeremylongshore/intent-eval-lab/.github/workflows/sign-evidence-bundle.yml@refs/heads/main' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  evidence-bundle.json
```

A `Verified OK` result proves: the bundle was signed by that exact workflow
identity, and its Rekor inclusion proof checks against the public transparency log.

You can also confirm the artifact digests independently:

```bash
# from the repo root — these must match the subject_set digests in evidence-bundle.json
sha256sum research/phase-a-0-baseline/results/aggregated/decision.json
sha256sum research/phase-a-0-baseline/results/aggregated/statistics.json
sha256sum research/phase-a-0-baseline/RESULTS.md
sha256sum 000-docs/036-AT-DECR-phase-a0-result-proceed-2026-05-31.md
```

## How it was produced (reproducible)

1. `scripts/build-evidence-bundle.py` constructs `evidence-bundle.json`
   deterministically — all time-varying inputs are passed as arguments, so a clean
   checkout reproduces byte-identical output (and therefore an identical signed
   digest).
2. The `Sign Evidence Bundle (Phase A.0)` workflow rebuilds the bundle in CI,
   checks it byte-matches the committed copy, signs it keyless against production
   sigstore, and **verifies its own signature** before the run is allowed to
   succeed.

Bead: `bd_000-projects-tr08.24`. Plan: `~/.claude/plans/snoopy-fluttering-comet.md`
§ Move 1.
