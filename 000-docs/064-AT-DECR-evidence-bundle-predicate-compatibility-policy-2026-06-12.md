---
date: 2026-06-12
status: RATIFIED — acting-CTO ruling under explicit owner delegation. The four predicate-compatibility rules below are binding before the first production-Rekor anchor; iah-E06 prod-Rekor pre-flight is GATED on this policy being ratified (it now is).
class: Class-2 acting-CTO ratification (one-way-door pre-Rekor gate), NOT a 7-seat ISEDC convening
author: Jeremy Longshore (acting CTO — Claude per explicit owner delegation, "make the decisions, you are CTO", 2026-06-12)
basis: bead uprg (Evidence Bundle predicate compatibility policy, P0); Kleppmann "Designing Data-Intensive Applications" ch. 4 forward/backward compatibility; Fowler "most-costly mistakes" schema-evolution discipline; gate-result/v1 predicate (Blueprint B § 7) + SigningMode/EvidenceBundle (Blueprint B § 2.4)
relates: DR-010 Q3 (predicate URI grammar locked before first prod-Rekor attestation), Blueprint B § 7.2 (URI versioning policy — URI-level; this DR is the row-level field-compat complement), 062-AT-DECR (acting-CTO ruling format precedent)
---

# Evidence Bundle predicate compatibility policy (DR-064)

## Tri-link block

```text
Beads: uprg (Evidence Bundle predicate compatibility policy, P0)
GitHub: jeremylongshore/intent-eval-lab#<TBA>
```

## 1. The ruling

> Every Evidence Bundle predicate (`gate-result/v1` and every URI minted after it) obeys four compatibility rules — FORWARD, BACKWARD, MIXING, DEPRECATION — fixed below. These rules are binding before the first production-Rekor anchor, because the `gate-result/v1` URI namespace is permanent the moment any row referencing it is signed and pushed to a transparency log. There is no errata path on a one-way door; the policy precedes the door.

Delegation basis: explicit owner instruction 2026-06-12 ("make the decisions, you are CTO"). This is an acting-CTO ratification of a one-way-door gate the prod-Rekor cutover produced — not a charter change. It complements, and does not alter, the URI-level versioning policy already locked in Blueprint B § 7.2: that policy governs **when a new URI is minted**; this DR governs **how rows of a given URI version evolve and interoperate** at the field level.

## 2. Why this is a one-way door

Production-Rekor anchoring is append-only and public. Once the first in-toto Statement carrying `predicateType: https://evals.intentsolutions.io/gate-result/v1` is signed and pushed to production Rekor, three facts become immutable:

1. The URI string is permanent — it can never be un-published from the transparency log (Blueprint B § 7.2).
2. The set of consumers that learned to read v1 rows is unbounded and uncoordinated — there is no central registry to migrate.
3. Any future v2 of the predicate body must coexist with v1 rows that are already signed into the log forever.

A compatibility policy authored **after** the first anchor cannot retroactively constrain rows already signed. Therefore the four rules are ratified now, as the gate on `iah-E06`.

## 3. The four rules (binding)

These rules borrow the forward/backward terminology from Kleppmann's compatibility framing (the writer/reader-version distinction) and Fowler's most-costly-mistake discipline (never break a deployed reader). They bind every predicate URI on `evals.intentsolutions.io`, not only `gate-result/v1`.

### Rule (a) — FORWARD compatibility

A consumer written against predicate version `vN` MUST ignore unknown fields when reading a `v(N+1)` row of the same URI major version. Concretely: a `gate-result/v1` consumer that encounters a field added in a later minor revision of the v1 body MUST process the fields it knows and MUST NOT reject the row on account of the unknown field. Producers MAY add new optional fields within a URI major version without coordinating with existing consumers.

This is the load-bearing rule for incremental kernel releases: `@intentsolutions/core` minor bumps add optional predicate-body fields (Blueprint B § 7.2 already commits the kernel schema to backward-compatibility across minor revisions); FORWARD compatibility is the consumer-side guarantee that makes those additions safe.

### Rule (b) — BACKWARD compatibility

A consumer written against `v(N+1)` MUST read a `vN` row unmodified — without rewriting, upgrading, or normalizing the on-the-wire row. The newer consumer fills in absent-because-newer fields from its own defaults; it MUST NOT mutate the original row to do so, and it MUST NOT require fields that did not exist in `vN`. A v2 consumer reading a v1 row treats the v1 row as authoritative for the fields v1 defined.

The append-only transparency log makes this non-negotiable: a `vN` row signed into Rekor is byte-frozen forever. A `v(N+1)` consumer that cannot read it has lost the ability to verify history.

### Rule (c) — MIXING (mixed-version bundles)

A single Evidence Bundle MAY contain rows of different predicate versions. Consumers MUST process each row independently — per the row-independence principle already in Blueprint B § 7.1 ("bundles are unioned, not joined; each row is independently verifiable"). A consumer MUST NOT assume every row in a bundle shares one predicate version, MUST NOT fail the whole bundle because one row is a version it does not support, and MUST NOT require version homogeneity as a precondition for verifying any row.

The correct posture for an unsupported row version is to skip that row (record it as not-covered in the consumer's coverage accounting), never to reject the bundle. This is the bundle-level corollary of FORWARD compatibility.

### Rule (d) — DEPRECATION window

A predicate URI version `vN` MUST remain supported for at least **three years** after `v(N+1)` is first published (first-signed-attestation date of `v(N+1)`, per the predicate-type registry in Blueprint B § 7.2). "Supported" means: the kernel keeps the `vN` JSON Schema published and validating; first-party consumers (audit-harness, j-rig, intent-rollout-gate) keep reading `vN` rows; the `vN` URI is never un-published from the registry. Retirement of a `vN` URI before its three-year floor expires requires its own Decision Record recording the exception and the migration evidence.

Three years is the floor, not the target: because Rekor entries are permanent, a `vN` row signed on the last day of support is still a permanent historical artifact that a verifier may need to read indefinitely. The three-year window bounds **producer** support, never **reader** capability.

## 4. Tie to the kernel + SigningMode

- The canonical machine-readable body for `gate-result/v1` is the kernel schema at `@intentsolutions/core/schemas/v1/gate-result.schema.json` (Blueprint B § 7.0). These four rules are the kernel's evolution contract: the kernel's "backward-compatible across minor revisions" commitment (§ 7.2) is the producer side; FORWARD/BACKWARD here are the consumer side.
- The four rules apply identically across SigningMode tiers (`unsigned_experimental`, `sigstore_staging`, `rekor_production` — Blueprint B § 2.4). They are not relaxed for staging: a row signed in staging today may be re-anchored or referenced in prod tomorrow, so it must already obey the compatibility rules.
- MIXING (rule c) is the bundle-index corollary of `predicate_uri_set` (Blueprint B § 2.4): a bundle's index row already enumerates the set of predicate URIs its rows represent, which presupposes a bundle may carry more than one.

## 5. Seat notes (consultative, not votes — no convening was held)

- **CISO:** the three-year DEPRECATION floor is the security-relevant rule — a verifier auditing a historical incident must be able to read the rows that were live at incident time; un-publishing a URI early would blind forensic replay. Demand: the predicate-type registry (Blueprint B § 7.2) records the `v(N+1)` first-signed date so the three-year clock is computable from the record, not from memory.
- **GC:** FORWARD/BACKWARD are stated as MUST on consumers, which binds first-party consumers we control; third-party consumers are bound by published contract, not by us. The DR records the contract; it does not warrant third-party conformance.
- **Hickey (panel canon):** these rules are the "don't break callers" growth discipline — new information is additive (new optional fields, new URIs), never a relaxation or removal within a version. Accretion, not mutation.

## 6. Gate status

`iah-E06` (audit-harness production-Rekor pre-flight) lists this compatibility policy as a precondition. With this DR RATIFIED, that precondition is satisfied. The remaining `iah-E06` preconditions (DNSSEC + CAA pinning on `evals.intentsolutions.io` per DR-004 Q1 + DR-010 Q3 CISO binding) are independent and tracked separately; this DR closes only the compatibility-policy gate.

— Jeremy Longshore
intentsolutions.io
