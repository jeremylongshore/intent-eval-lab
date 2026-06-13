---
date: 2026-06-12
status: RATIFIED — acting-CTO ruling under explicit owner delegation. The superseding-event protocol below is the normative rollback semantics for production-Rekor-anchored Evidence Bundles; binding before the first production-Rekor anchor.
class: Class-2 acting-CTO ratification (one-way-door pre-Rekor gate), NOT a 7-seat ISEDC convening
author: Jeremy Longshore (acting CTO — Claude per explicit owner delegation, "make the decisions, you are CTO", 2026-06-12)
basis: bead 3ptb (Rekor superseding-event protocol, P0); plan 033-PP-PLAN § 14.4.rollback (the preserve-not-mutate rule + rolled-back-superseded marker); Rekor append-only transparency-log guarantee
relates: 064-AT-DECR (predicate compatibility policy — sibling pre-Rekor gate), Blueprint B § 2.4 (EvidenceBundle SigningMode enum), Blueprint B § 7 (gate-result/v1), DR-010 Q5 (production-Rekor signing gated on SPEC.md normative section landing)
---

# Rekor superseding-event protocol (DR-065)

## Tri-link block

```text
Beads: 3ptb (Rekor superseding-event protocol, P0)
GitHub: jeremylongshore/intent-eval-lab#<TBA>
```

## 1. The ruling

> A rollback of a production-Rekor-anchored attestation NEVER mutates the original Rekor entries. Rekor is append-only; original rows are byte-frozen forever. Downstream consumers learn that a window of attestations is no-longer-binding via a separate SUPERSEDING event appended to the log, not by any retraction, deletion, or rewrite of the originals. In-flight Evidence Bundles emitted during the shadow→blocking→rollback window are preserved and marked `signing_mode='rolled-back-superseded'`.

Delegation basis: explicit owner instruction 2026-06-12 ("make the decisions, you are CTO"). This is an acting-CTO ratification of the rollback semantics plan 033 § 14.4.rollback fixed for the Skill Refiner Phase-4 flip; this DR generalizes that rule to every production-Rekor-anchored predicate and pins the wire shape of the superseding event. It is the second one-way-door gate (sibling to DR-064) that must be ratified before the first production-Rekor anchor.

## 2. Why a superseding event, not a retraction

Production Rekor is an append-only transparency log. Three consequences fix the design:

1. **Originals are immutable.** A signed in-toto Statement pushed to production Rekor has a permanent log index. It cannot be edited or deleted. "Rolling back" cannot mean "removing the row."
2. **The signature is still valid.** The rolled-back rows were genuinely emitted and genuinely signed — they are real attestations of what the gate actually decided at emission time. Their cryptographic validity is not in question; their **binding force on downstream ship/no-ship decisions** is what the rollback revokes.
3. **Consumers are uncoordinated.** There is no callback to every consumer that already read a now-superseded row. The only durable channel is the same append-only log: append a new event that consumers resolve against.

Therefore a rollback appends a SUPERSEDING event. The original rows stay; the superseding event tells a consumer "treat the referenced rows as advisory-not-binding from here forward."

## 3. The shadow→blocking→rollback window

The rollback applies to attestations emitted in a bounded window, per the plan 033 § 14.4 state machine:

| Phase | What is emitted | Binding force |
| --- | --- | --- |
| **shadow** | Evidence Bundle rows emitted while the gate runs in advisory/shadow mode | non-blocking by construction |
| **blocking** | rows emitted after the advisory→blocking flip; these gate real PRs | binding |
| **rollback** | the governance-authorized revert of the blocking flip | the trigger that mints the superseding event |

Any Evidence Bundle rows emitted between SHADOW-MODE entry and the BLOCKING flip — and the BLOCKING-window rows themselves — are PRESERVED. They are real attestations. The rollback does not pretend they never happened; it records that the BLOCKING-window attestations are advisory-not-binding via the superseding event.

## 4. The `rolled-back-superseded` marker

Every Evidence Bundle row in the affected window is marked `signing_mode='rolled-back-superseded'` in a **separate envelope event**, NOT by mutating the original Rekor entries. This is a fourth value in the SigningMode space (Blueprint B § 2.4 enumerates `sigstore_staging`, `rekor_production`, `unsigned_experimental`; `rolled-back-superseded` is the rollback-state marker carried on the superseding event's references, not on the originals).

Critical constraint: the marker lives on the **superseding event's reference to** each original row, never as an edit to the original row's stored bytes. A verifier fetching the original Rekor entry sees its true emission-time `signing_mode` (`rekor_production`); a verifier resolving current-binding-state via the superseding event sees the rows marked `rolled-back-superseded`.

## 5. The superseding-event shape

A superseding event is itself an appended attestation — a new in-toto Statement, signed and pushed like any other row, carrying a rollback predicate body. It references the superseded rows; it never carries the originals' bytes.

What it MUST reference:

- **`superseded_window`** — the bounded set of original rows being superseded, identified by their content-addressed subject digests (`sha256:`) and, where known, their production-Rekor `log_index` values. Identification is by immutable content hash + log index, never by mutable position.
- **`superseded_signing_mode`** — the constant `rolled-back-superseded` (the new binding-state the referenced rows take on).
- **`original_signing_mode`** — `rekor_production` (recording what the superseded rows were, so a consumer sees both the genuine emission mode and the new binding state).
- **`rollback_reason`** — a structured string; the same reason recorded in the governing Decision Record.
- **`rollback_decision_ref`** — a reference to the authorizing Decision Record (per plan 033 § 14.4.rollback, the `kernel-gate-revert <reason>` command records an `AT-DECR-phase-4c-rollback-NNN`). The superseding event cites that DR so the audit trail is closed.
- **`superseded_at`** — RFC 3339 UTC moment the rollback was authorized.

How a consumer resolves current-vs-superseded:

1. Fetch the original row by its Rekor `log_index` / subject digest. Verify its signature — it is and remains valid.
2. Query the log for any superseding event whose `superseded_window` references that row's subject digest.
3. If a superseding event exists, the row's **binding state** is `rolled-back-superseded` — treat it as advisory-not-binding for ship/no-ship purposes; its historical fact (the gate decided X at time T) is unchanged.
4. If no superseding event references it, the row is current and binding at its emission-time `signing_mode`.

Resolution is last-writer-wins by `superseded_at` among superseding events referencing the same row, but in practice a row is superseded at most once (a re-flip after rollback emits new rows under a new window, it does not un-supersede old ones).

## 6. The append-only guarantee (invariant)

The load-bearing invariant, stated once and unconditionally:

> **A rollback MUST NOT mutate, edit, delete, or rewrite any original Rekor entry. Every rollback is expressed exclusively as one or more newly-appended superseding events. The transparency log only ever grows.**

Corollaries:

- An auditor replaying the log at any historical timestamp sees the world as it was at that timestamp — including BLOCKING-window rows that were binding then and are superseded now. History is not rewritten.
- A consumer that read a now-superseded row before the superseding event was appended is not "wrong" — it acted on the binding state of record at its read time. The superseding event changes binding state going forward, not retroactively.
- There is no top-level "bundle retraction" — consistent with Blueprint B § 7.1's no-top-level-bundle-signature rule, supersession operates at the row-reference granularity, never as a whole-bundle erase.

## 7. Seat notes (consultative, not votes — no convening was held)

- **CISO:** the separate-envelope rule is the security-critical one — marking the originals in place would be indistinguishable from log tampering and would void the transparency guarantee. The marker MUST live on the appended event. Demand: the superseding event cites the authorizing DR (`rollback_decision_ref`) so the revoke is provably governance-authorized, not a unilateral act.
- **GC:** "advisory-not-binding" is the precise legal posture — the rolled-back rows are not retracted (they happened, they were signed) and not warranted as binding; the superseding event is the record of that posture change.
- **Gregg (panel canon):** resolution is observable — a consumer can compute current-vs-superseded purely from the log (fetch original + query for superseding references), no out-of-band state. If you can't measure the binding state from the log alone, the protocol failed; this one you can.

## 8. Gate status

This protocol is the rollback-semantics precondition for production-Rekor anchoring. With this DR RATIFIED alongside DR-064 (predicate compatibility policy), the two one-way-door governance gates that must precede the first production-Rekor anchor are both closed. The remaining `iah-E06` preconditions (DNSSEC + CAA pinning) are independent and tracked separately.

— Jeremy Longshore
intentsolutions.io
