# Anchoring the Decision Records ledger HEAD (cosign keyless → STAGING Rekor)

This procedure anchors the [`specs/DECISION-RECORDS.md`](../specs/DECISION-RECORDS.md)
ledger **HEAD** in Sigstore's **STAGING** transparency log, giving the hash chain
an external, time-stamped, third-party witness. With the ledger committed _and_
its HEAD anchored, silently mutating a verbatim 7-seat Decision Record requires
forging both the in-repo chain (caught by `--verify` in CI) **and** a staging
Rekor inclusion proof (cryptographically infeasible).

> **STAGING ONLY.** This ledger anchors to `rekor.sigstage.dev` /
> `fulcio.sigstage.dev` — the Sigstore **staging** instances. Staging entries are
> periodically wiped and carry **no** durability guarantee; they are for
> dogfooding the pipeline, not for production attestation. **Never** anchor the
> DR ledger to production `rekor.sigstore.dev`. Production-Rekor predicate
> declaration for this platform is gated on `evals.intentsolutions.io` DNSSEC +
> CAA + SPEC.md normative clearance (DR-018, DR-010 Q3) — which have not cleared.
> The production evidence-bundle signing path lives in a separate workflow and is
> deliberately manual-dispatch-only.

## Why this is "anchor the HEAD", not "sign every DR"

The ledger is a Certificate-Transparency-style hash chain: every entry commits to
its predecessor, so the single HEAD value transitively commits to every DR and
every prior entry. Anchoring the **HEAD** anchors the entire chain. Re-anchor
whenever a new DR lands (the HEAD changes); each anchor is a point-in-time witness
that the chain held that exact shape at that time.

## What gets signed

A `cosign sign-blob` over the raw bytes of `specs/DECISION-RECORDS.md`. The blob
signature attests **file integrity + signer identity + time** — it declares **no**
predicate URI (`cosign sign-blob` makes no predicate claim, by design, consistent
with the existing evidence-bundle signing path). The HEAD inside the file is the
load-bearing value; signing the whole file is simply the cheapest way to bind it.

## One-time local dogfication (interactive — needs a browser for OIDC)

Keyless signing needs an OIDC identity. Locally this is an interactive browser
flow; in CI it is the workflow's GitHub OIDC token (preferred — see below).

```bash
# 1. Make sure the ledger is current and self-consistent.
scripts/build-dr-ledger.sh --verify

# 2. Point cosign at the STAGING Sigstore deployment.
export SIGSTORE_FULCIO_URL="https://fulcio.sigstage.dev"
export SIGSTORE_REKOR_URL="https://rekor.sigstage.dev"
export SIGSTORE_OIDC_ISSUER="https://oauth2.sigstage.dev/auth"

# 3. Sign the ledger blob (opens a browser for the staging OIDC flow).
cosign sign-blob \
  --yes \
  --new-bundle-format \
  --bundle specs/DECISION-RECORDS.sigstore.json \
  specs/DECISION-RECORDS.md
```

The resulting `specs/DECISION-RECORDS.sigstore.json` carries the staging-Fulcio
cert chain plus the staging-Rekor inclusion proof. Do **not** commit it as a
durable artifact (staging is ephemeral); treat it as a dogfooding receipt.

## Preferred: anchor from CI under the workflow's OIDC identity

A reusable, manual-dispatch-only workflow is the durable home for this — it mirrors
`.github/workflows/sign-evidence-bundle.yml` but swaps the production Sigstore
endpoints for staging. Drop the following at
`.github/workflows/anchor-dr-ledger.yml` to wire it (left as a follow-on so the
ledger + procedure can land first):

```yaml
name: Anchor DR ledger HEAD (STAGING Rekor)

# Anchors specs/DECISION-RECORDS.md in Sigstore STAGING (fulcio.sigstage.dev +
# rekor.sigstage.dev), keyless, under this workflow's GitHub OIDC identity.
# STAGING ONLY — staging entries are ephemeral; never point this at production.
# Manual trigger: re-run whenever a new AT-DECR lands and the HEAD changes.

on:
  workflow_dispatch: {}

permissions:
  contents: read
  id-token: write # REQUIRED: Fulcio keyless signing via GitHub OIDC

jobs:
  anchor:
    name: Verify ledger + anchor HEAD (staging Rekor)
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Verify the ledger matches the live DRs (refuse to anchor if stale)
        run: bash scripts/build-dr-ledger.sh --verify

      - name: Install cosign
        uses: sigstore/cosign-installer@v3

      - name: Sign ledger blob (keyless, STAGING Sigstore + Rekor)
        env:
          SIGSTORE_FULCIO_URL: https://fulcio.sigstage.dev
          SIGSTORE_REKOR_URL: https://rekor.sigstage.dev
          SIGSTORE_OIDC_ISSUER: https://token.actions.githubusercontent.com
        run: |
          set -euo pipefail
          HEAD="$(bash scripts/build-dr-ledger.sh --head)"
          echo "Anchoring DR ledger HEAD: ${HEAD}"
          cosign sign-blob \
            --yes \
            --new-bundle-format \
            --fulcio-url "$SIGSTORE_FULCIO_URL" \
            --rekor-url "$SIGSTORE_REKOR_URL" \
            --bundle /tmp/dr-ledger.sigstore.json \
            specs/DECISION-RECORDS.md

      - name: Verify the signature we just made (staging)
        env:
          SIGSTORE_REKOR_URL: https://rekor.sigstage.dev
        run: |
          set -euo pipefail
          EXPECTED_IDENTITY="https://github.com/${GITHUB_REPOSITORY}/.github/workflows/anchor-dr-ledger.yml@${GITHUB_REF}"
          cosign verify-blob \
            --new-bundle-format \
            --rekor-url "$SIGSTORE_REKOR_URL" \
            --bundle /tmp/dr-ledger.sigstore.json \
            --certificate-identity "${EXPECTED_IDENTITY}" \
            --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
            specs/DECISION-RECORDS.md

      - name: Upload staging anchor receipt
        uses: actions/upload-artifact@v4
        with:
          name: dr-ledger-staging-anchor
          path: /tmp/dr-ledger.sigstore.json
```

## Verifying an existing staging anchor

```bash
export SIGSTORE_REKOR_URL="https://rekor.sigstage.dev"
cosign verify-blob \
  --new-bundle-format \
  --rekor-url "$SIGSTORE_REKOR_URL" \
  --bundle specs/DECISION-RECORDS.sigstore.json \
  --certificate-identity '<the OIDC identity that signed it>' \
  --certificate-oidc-issuer '<the OIDC issuer>' \
  specs/DECISION-RECORDS.md
```

A successful verify proves the ledger bytes (and therefore the HEAD and the whole
chain) match what was witnessed in staging Rekor at signing time. A staging-log
wipe makes the _inclusion proof_ unverifiable, but the in-repo chain
(`--verify`) remains the always-available tamper signal; the staging anchor is the
external corroborating witness, not the sole line of defense.

## Status / scope

- ✅ Ledger + generator + `--verify` gate: shipped.
- ✅ Anchoring procedure + ready-to-paste staging workflow: this document.
- ⏳ Wiring `.github/workflows/anchor-dr-ledger.yml` + capturing a first staging
  Rekor entry: follow-on. The live `cosign sign-blob` step needs a CI OIDC
  identity (or an interactive browser locally) and a reachable staging Sigstore;
  it cannot run from a non-interactive build sandbox. Per the bead's rescope
  clause, the anchor step is split out from the ledger authoring.

## Authority

- Bead: "Hash-chain Decision Records into signed append-only ledger".
- `000-docs/023-AA-AACR-thinker-panel-review-2026-05-25.md` § 2.1 finding #1.
- DR-010 Q3 GC binding (Decision Records are the permanent verbatim 7-seat
  record); DR-018 (production predicate declaration gating).
- Existing production-path reference: `.github/workflows/sign-evidence-bundle.yml`.
