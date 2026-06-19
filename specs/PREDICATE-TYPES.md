# Predicate-Type Registry

**Status: NORMATIVE.** This file is the canonical record mandated by Blueprint B
(`000-docs/012-AT-ARCH-platform-runtime-blueprint.md`) § 7.2: _"the file
`intent-eval-lab/specs/PREDICATE-TYPES.md` lists every URI subtype, first-signed-attestation
date, and Decision Record link. The registry MUST be updated within 7 days of any new subtype
going live. Drift in this registry is unrecoverable; the registry IS the canonical record of
which URIs exist."_

This registry tracks **what predicate URIs exist and at what lifecycle stage**. The canonical,
machine-readable **schema** for each predicate body lives in the kernel package at
`@intentsolutions/core/schemas/v1/<predicate>.schema.json` (Blueprint B § 7.0; DR-018 Option
α-minus). This registry is the index; the kernel is the schema authority. On any disagreement
about a predicate body's shape, the kernel schema wins.

## Reading the registry

- **Predicate URI** — the immutable `predicateType` string. Grammar (DR-004 Q1, DR-010 § 7 Q3):
  `evals.intentsolutions.io/<predicate-type>/v<version>`. URIs live **only** on `evals.`;
  `labs.intentsolutions.io` is reserved-don't-touch (CISO binding, Blueprint B § 7.2).
- **Stage** — the predicate's lifecycle stage (see the closed vocabulary below). This is the
  per-predicate _scope-element_ label per the State-Labeling Standard
  (`000-docs/069-DR-STND-state-labeling-standard-2026-06-18.md`).
- **First-signed date** — the date the first in-toto Statement carrying this URI was signed
  into a transparency log. `—` means no row has been signed yet (the URI is reserved/declared
  but not yet live). The three-year DEPRECATION clock (DR-064) runs from a successor's
  first-signed date.
- **Schema (kernel)** — the canonical schema path in `@intentsolutions/core`, with the kernel
  version that introduced it.
- **DR / spec** — the Decision Record and/or normative spec section that authorizes the URI.

### Stage vocabulary (closed)

| Stage         | Meaning                                                                                                     | Signing mode                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `ACTIVE`      | SPEC.md normative section landed; eligible for production-Rekor once DNSSEC + CAA verify.                   | `rekor_production` (after pre-flight) / `sigstore_staging` until then. |
| `CONDITIONAL` | In the namespace as a legitimate type; production-Rekor gated on its own SPEC.md normative section landing. | `sigstore_staging`.                                                    |
| `RESERVED`    | Reserved concurrent with a kernel release; SPEC reference fixed; awaiting first signing.                    | `unsigned_experimental` / `sigstore_staging`.                          |
| `DEFERRED`    | Recognized use case; not yet reserved. Naming it here does not reserve it.                                  | none.                                                                  |
| `PROPOSED`    | Proposed by an RFC; one step earlier than `DEFERRED`. Reservation is a Class-1 ISEDC act.                   | none.                                                                  |
| `REJECTED`    | Explicitly disclaimed for v1 pending a precondition (e.g. a sanitization spec).                             | none.                                                                  |

Reserving or activating a predicate URI is a **Class-1 ISEDC act** ("new predicate URI subtype
reservation," DR-010 § 7 Q6). Naming a `DEFERRED` / `PROPOSED` / `REJECTED` type in this registry
does **not** reserve it, declare a normative SPEC, or emit any `predicateType`.

---

## Registry

### ACTIVE

| Predicate URI                                     | Stage    | First-signed             | Schema (kernel)                                                       | DR / spec                                                                          |
| ------------------------------------------------- | -------- | ------------------------ | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `https://evals.intentsolutions.io/gate-result/v1` | `ACTIVE` | — (staging only to date) | `@intentsolutions/core/schemas/v1/gate-result.schema.json` (`@0.1.0`) | Blueprint B § 7 (normative); DR-010 § 7 Q3; DR-018 § 6.4 (kernel schema authority) |

`gate-result/v1` is the **first** predicate URI with SPEC.md normative content landed (Blueprint
B § 7). Production-Rekor signing is unlocked once Blueprint B § 7 merged (done) **and** the
`iah-E06` pre-flight (DNSSEC + CAA on `evals.intentsolutions.io` + the compatibility policy
DR-064) passes. Until then it anchors to `sigstore_staging` per DR-010 § 7 Q5.

### CONDITIONAL (per DR-010 § 7 Q3)

| Predicate URI                                           | Stage         | First-signed | Schema (kernel)                                          | DR / spec                                                 |
| ------------------------------------------------------- | ------------- | ------------ | -------------------------------------------------------- | --------------------------------------------------------- |
| `https://evals.intentsolutions.io/validation-result/v1` | `CONDITIONAL` | —            | (kernel schema lands with its SPEC.md normative section) | DR-010 § 7 Q3                                             |
| `https://evals.intentsolutions.io/eval-verdict/v1`      | `CONDITIONAL` | —            | (kernel schema lands with its SPEC.md normative section) | DR-010 § 7 Q3                                             |
| `https://evals.intentsolutions.io/cost-attribution/v1`  | `CONDITIONAL` | —            | (kernel schema lands with its SPEC.md normative section) | DR-010 § 7 Q3                                             |
| `https://evals.intentsolutions.io/runtime-receipt/v1`   | `CONDITIONAL` | —            | (kernel schema lands with its SPEC.md normative section) | Blueprint B § 7.2 (OTel `must emit` table); DR-010 § 7 Q3 |

Each enters the namespace as a legitimate type but its production-Rekor signing is gated on that
predicate's own SPEC.md normative section landing first. Until then, attestations carrying these
URIs run in `sigstore_staging` mode.

### RESERVED

| Predicate URI                                                 | Stage      | First-signed                                                               | Schema (kernel)                                                                                                          | DR / spec                                                                                                                                              |
| ------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `https://evals.intentsolutions.io/evidence-bundle-payload/v1` | `RESERVED` | — (reserved concurrent with `@intentsolutions/core@0.2.0`; not yet signed) | `@intentsolutions/core` `EvidenceBundlePayload` + `schemas/v1/evidence-bundle-payload.schema.json` (`@0.2.0`, `iec-E12`) | Blueprint B § 7 (parent spec); DR-018 (`000-docs/018-AT-DECR-isedc-council-session-5-jrig-reconciliation-2026-05-21.md`) § 6.4 binding precondition #3 |
| `https://evals.intentsolutions.io/skill-refiner-pass/v1`      | `RESERVED` | —                                                                          | (kernel schema lands with Skill Refiner integration)                                                                     | DR-028 (`000-docs/028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md`)                                                  |

#### `evidence-bundle-payload/v1` — entry detail (im30)

| Field                     | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Predicate URI**         | `https://evals.intentsolutions.io/evidence-bundle-payload/v1`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Stage**                 | `RESERVED` — reserved concurrent with the kernel `@intentsolutions/core@0.2.0` release per DR-018 § 6.4 binding precondition #3; no row signed yet.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **Date reserved**         | 2026-06-18 (registry entry filed). First-signed date to be recorded here within 7 days of the kernel v0.2.0 release per the Blueprint B § 7.2 / DR-010 § 7 Q3 GC discipline.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **Kernel version**        | `@intentsolutions/core@0.2.0` (the minor, additive release that introduces the `EvidenceBundlePayload` type — `iec-E12`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Co-author attribution** | The `EvidenceBundlePayload` wire-format shape folds the `EvidenceStatement` row shape originally implemented in `j-rig-skill-binary-eval` (`@j-rig/*`), adopted into the kernel under DR-018 Option α-minus. The cross-field invariants (`subject[0].name === predicate.gate_id`; `subject[0].digest.sha256` === `predicate.input_hash`, prefix-stripped) were co-authored by the CISO seat per DR-018 § 6.4 binding precondition #2. j-rig retains a behavioral secondary check for one major-version cycle, then removes it once kernel enforcement is CI-proven across all five consumer repos. |
| **Parent spec**           | Blueprint B (`000-docs/012-AT-ARCH-platform-runtime-blueprint.md`) § 7 (Evidence Bundle predicate contracts). The kernel schema is the machine-readable authority (Blueprint B § 7.0).                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Authorizing DR**        | DR-018 § 6.4 (Option α-minus + the three binding preconditions, the third of which mandates this registry entry).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Compatibility**         | Bound by the four compatibility rules in DR-064 (`000-docs/064-AT-DECR-evidence-bundle-predicate-compatibility-policy-2026-06-12.md`): FORWARD, BACKWARD, MIXING, three-year DEPRECATION window.                                                                                                                                                                                                                                                                                                                                                                                                   |

### PROPOSED (NOT reserved)

| Predicate URI                                      | Stage      | First-signed | Schema (kernel) | DR / spec                                                                                                  |
| -------------------------------------------------- | ---------- | ------------ | --------------- | ---------------------------------------------------------------------------------------------------------- |
| `https://evals.intentsolutions.io/prompt-eval/v1`  | `PROPOSED` | —            | n/a             | 043-DR-RFC (`000-docs/043-DR-RFC-intent-eval-target-generalization-2026-06-06.md`) § 6; DR-010 § 7 Q3 + Q6 |
| `https://evals.intentsolutions.io/context-eval/v1` | `PROPOSED` | —            | n/a             | 043-DR-RFC § 6; DR-010 § 7 Q3 + Q6                                                                         |

Proposed by the prompt+context-eval landscape RFC as the eventual signed-evidence surface for the
proposed `prompt` / `context-template` eval targets. Their use case is _proposed_, not yet accepted.
Reservation is a Class-1 ISEDC act; naming them here does not reserve them. Host, if ever admitted,
is `evals.intentsolutions.io` only — never `labs.`.

### DEFERRED (Phase B+)

| Predicate URI                                            | Stage      | First-signed | Schema (kernel) | DR / spec     |
| -------------------------------------------------------- | ---------- | ------------ | --------------- | ------------- |
| `https://evals.intentsolutions.io/harness-experiment/v1` | `DEFERRED` | —            | n/a             | DR-010 § 7 Q3 |
| `https://evals.intentsolutions.io/cache-decision/v1`     | `DEFERRED` | —            | n/a             | DR-010 § 7 Q3 |

Use cases recognized but not yet ready for namespace reservation.

### REJECTED

| Predicate URI                                          | Stage               | First-signed | Schema (kernel) | DR / spec               |
| ------------------------------------------------------ | ------------------- | ------------ | --------------- | ----------------------- |
| `https://evals.intentsolutions.io/agent-loop-trace/v1` | `REJECTED` (for v1) | —            | n/a             | DR-010 § 7 Q3 CISO veto |

`REJECTED for v1` pending a sanitization specification. Agent-loop traces carry credential-shaped
substrings and tool-output payloads whose redaction discipline is not yet specified; admitting the
URI before the sanitization spec lands risks a credential leak into a transparency log.

The gating sanitization spec is now authored at
[`specs/sanitization/v0.1.0-draft/SPEC.md`](sanitization/v0.1.0-draft/SPEC.md) (iel-E10) — it
defines the prompt-redaction (§ 4), tool-call-arg sanitization (§ 5), and agent-reasoning
summarization (§ 6) rules plus the CISO PASS/FAIL fixture suite (§ 7). **Authoring the spec does
NOT un-reject the URI.** Per DR-010 § 7 Q3 the revisit trigger is: the sanitization spec authored
AND its fixture suite green in CI. Even then, un-rejecting and reserving `agent-loop-trace/v1` is a
**Class-1 ISEDC act** — moving this row out of REJECTED is a separate council decision, not a
consequence of the spec landing (sanitization SPEC § 7 R15).

---

## Maintenance discipline

- **7-day rule.** Any new subtype going live (first row signed) MUST be recorded here within 7 days
  (Blueprint B § 7.2; DR-010 § 7 Q3 GC discipline). Record the **first-signed date** the moment a
  row referencing the URI is pushed to a transparency log (staging or production).
- **Reservation is Class-1.** Adding a row in `ACTIVE` / `CONDITIONAL` / `RESERVED` (i.e., reserving
  a URI) is a Class-1 ISEDC act. Adding a `DEFERRED` / `PROPOSED` / `REJECTED` row (recording a type
  that is _not_ reserved) is a registry-hygiene act that cites the authorizing RFC/DR.
- **Compatibility.** Every URI listed here is bound by the four compatibility rules in DR-064.
- **Schema authority.** This registry never carries a predicate body schema; the kernel does
  (Blueprint B § 7.0). This file is the index of _which URIs exist_, not _what they contain_.

## Cross-references

- Predicate URI registration + grammar: Blueprint B (`000-docs/012-AT-ARCH-platform-runtime-blueprint.md`) § 7.2.
- Schema authority (kernel wins): Blueprint B § 7.0; DR-018 § 6.4.
- Compatibility rules: DR-064 (`000-docs/064-AT-DECR-evidence-bundle-predicate-compatibility-policy-2026-06-12.md`).
- Predicate-type taxonomy in prose: Canonical Glossary (`000-docs/014-DR-GLOS-canonical-glossary.md`) § 6.
- Scope-element labels: State-Labeling Standard (`000-docs/069-DR-STND-state-labeling-standard-2026-06-18.md`).
