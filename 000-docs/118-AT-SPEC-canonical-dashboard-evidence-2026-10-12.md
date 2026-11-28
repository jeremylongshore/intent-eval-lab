# Canonical Dashboard Evidence

**Date:** 2026-10-12

**Bead:** `bd_000-projects-0s2a`

**Scope:** Private `iel` release evidence producer; implementation guidance.

## Producer and Dependency Boundary

`ci/emit-evidence.ts` measures the existing harness-hash and snapshot-currency
meta-gates. These describe repository integrity, not product evaluation quality.
Their measurements, outcomes and source identity remain unchanged.

The private `ci/` package pins kernel 0.10.0 and its transitive dependencies in
`ci/package-lock.json`. This deliberately replaces the release job's unlocked
0.2.0 install for canonical payload production and tested dashboard compatibility.
It is not a kernel-currency policy: older consumer pins remain conformant under
[doc 111](111-AT-SPEC-kernel-version-skew-is-by-design-2026-07-22.md).
The lab still has no root Node package, application build or npm publication.

## Payload Contract

Each predicate becomes one kernel-validated in-toto statement in an
`EvidenceBundlePayload` array. The signed bundle binds the entire canonical
array through `storage_key`; subject set, predicate types and row count derive
from the same validated payload. The manifest transports that payload and a
checked `gateResults` projection.

Assembly rejects missing or invalid payloads, inconsistent signed metadata and
conflicting projections. Hashing includes every transported field, including
allowed extensions. Real signature verification remains the workflow/dashboard
boundary; an assembler transport fixture does not establish provenance.

## Verification

Use Node 22.6 or newer from the repository root:

```bash
npm ci --prefix ci --ignore-scripts
npm test --prefix ci
node --experimental-strip-types ci/emit-evidence.ts --self-check
scripts/audit-harness verify
```

Twelve offline contracts cover independently calculated synthetic bytes,
pass/fail/advisory/error preservation, source/signing identity, payload and
metadata mutations, projection mismatch and missing signature files. PR CI runs
these checks; release CI repeats the contracts before signing. Emitter sources,
fixture, tests and dependency files are hash-pinned. Run `scripts/audit-harness init` after an intentional edit and review the
updated pin manifest.

## Live Transition

Tag-only publication and the existing OIDC workflow identity are preserved.
After an approved release, verify source SHA, canonical digest, signed metadata,
real signature, dashboard ingest and rendered rows. Record receipts on the bead.
Synthetic fixtures are never signed or substituted for measured outcomes.
Retain legacy consumer compatibility until all producers and retained caches
have a verified transition disposition; source merge alone is not live proof.
