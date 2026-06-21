---
date: 2026-06-17
authors:
  - Jeremy Longshore (Intent Solutions, acting head of board)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: ISEDC Session — DR-082 (skill-refiner-pass/v1 predicate URI, Class-1, 2026-06-17)
inherits_from: 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B § 7 — the gate-result/v1 normative-fold this section mirrors)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: bd_000-projects-0r8m (refiner evidence reports + Tier-1 kernel)
bead: bd_000-projects-0r8m.3
filing_standard: Document Filing Standard v4.3
related_drs:
  - 082-AT-DECR (skill-refiner-pass/v1 predicate URI — the 5 binding decisions Q1–Q5 this section implements)
  - 081-AT-DECR (SAK Class-1 charter — Q3 no-shared-trust-root; the separate authoring chamber)
  - 028-AT-DECR (Skill Refiner plan ratification — T1 SkillVersion 14th entity; refiner_strategy_id signed; significance threshold normative)
  - 064-AT-DECR (Evidence Bundle predicate-compatibility policy — inherited by DR-082 Q5)
  - 010-AT-DECR (S4 — Q3 unification thesis, Q5 production-Rekor sequencing, staging-first default)
  - 004-AT-DECR (S1 — predicate URI namespace binding; evals.* only, never labs.*)
schema_normative_authority: "@intentsolutions/core/schemas/v1/skill-refiner-pass.schema.json (kernel JSON Schema is the machine-readable authority; this section is the normative prose; on disagreement the kernel schema wins and this section is amended to match — never the reverse)"
production_signing: STAGING (sigstore_staging) — all four DR-082 Q3 production triggers must hold to flip; see § 6
forward_refs:
  - 084-AT-SPEC-authoring-chamber-signing-trust-root-design (DR-082 Q3 trigger 3 — the SEPARATE signing root this section's production posture depends on)
  - PREDICATE-TYPES.md (specs/ registry — this section flips the skill-refiner-pass/v1 row RESERVED→ACTIVE on merge)
---

# `skill-refiner-pass/v1` — Normative Predicate Spec

> **State label: NORMATIVE.** This is the SPEC.md normative section for the
> `skill-refiner-pass/v1` predicate URI. Landing it on `intent-eval-lab` main
> is **DR-082 Q3 trigger 1** — it flips the registry row in
> `specs/PREDICATE-TYPES.md` from `RESERVED` to `ACTIVE`. Landing this section
> does **not** by itself unlock production-Rekor signing; production is gated on
> the **conjunction of all four** DR-082 Q3 triggers (§ 6). Until all four hold,
> `skill-refiner-pass/v1` runs in `sigstore_staging`.
>
> **What this section is.** The normative prose specification of the
> `skill-refiner-pass/v1` in-toto predicate — the signed attestation the Skill
> Refiner emits when a real `SkillVersion` clears the `@j-rig/refiner-core`
> acceptance gate. It mirrors the structure of Blueprint B § 7 (the
> `gate-result/v1` normative fold) deliberately: per DR-082 Q4, this predicate
> MIRRORS `gate-result/v1` EXACTLY on the wire — same in-toto Statement v1
> envelope, same DSSE wrapping, same body-only schema validation, same row
> independence, same no-top-level-bundle-signature rule. The ONLY divergences
> are below the wire: a different signing trust root (DR-081 Q3 / § 6 trigger 3)
> and an independent `$schemaVersion` lane. The chamber boundary is NEVER
> expressed in the URL string or the envelope shape (DR-082 Q1, Q4).
>
> **What this section is NOT.** It is not the kernel schema — the canonical
> machine-readable authority is the kernel JSON Schema at
> `@intentsolutions/core/schemas/v1/skill-refiner-pass.schema.json` (DR-082
> § 13). It is not the acceptance-gate algorithm spec — the `accept()` predicate
> (significant Pareto-dominance on the behavioral dimension + non-regression on
> every named dimension, one-sided z-test at the stated `alpha`) lives in
> `@j-rig/refiner-core` and is ratified by DR-028. It is not the SkillVersion
> entity spec — SkillVersion is the kernel's 14th canonical entity (DR-028 T1),
> referenced here by id/hash, never redefined.
>
> **Authority precedence on conflict.** Where this section's prose tables, the
> kernel JSON Schema at `@intentsolutions/core/schemas/v1/skill-refiner-pass.schema.json`,
> and the kernel TypeScript surface (`@intentsolutions/core/predicates/skill-refiner-pass-v1`)
> disagree, **the kernel JSON Schema wins.** Edits to this section that change
> the predicate body shape require simultaneous edits to the kernel; this
> section is amended to match the kernel, not the reverse. This is the same
> machine-readable-schema-is-canonical precedence Blueprint B § 7.0 / § 7.4 set
> for `gate-result/v1`.

---

## 1. Predicate meaning

A `skill-refiner-pass/v1` row is the signed, third-party-verifiable claim that:

> **A real `SkillVersion` cleared the Skill Refiner acceptance gate** — it
> demonstrated significant Pareto-dominance on the behavioral dimension AND
> non-regression on every named dimension, by a one-sided z-test at the stated
> `alpha`, against a FROZEN eval-set, via a bounded EditProposal, produced by a
> named, traceable RefinerStrategy.

This is the platform thesis applied to authoring: signed, third-party-verifiable
evidence that a skill provably _got better_ — not a score in a dashboard, not a
"trust me, it passed" assertion, but an in-toto attestation a verifier can
re-derive from immutable inputs without trusting Intent Solutions.

The predicate is **emitted on a real verdict**. The closed `verdict` enum carries
`accept | reject`; the URI's category claim ("skill-refiner-pass") is realized
by the determinant set in the body, not by the URI string alone. A row with no
signed deltas, no `alpha`, and no `refiner_strategy_id` would be an unfalsifiable
badge — exactly the failure mode DR-082 Q2 forbids. The body therefore carries
exactly the **accept determinants**: the fields a verifier needs to independently
re-run the one-sided z-test on the named deltas at the stated `alpha`, confirm
the eval-set hash, and confirm the edit-proposal hash. Strip any one determinant
and the PASS becomes unfalsifiable.

**Composable partial attestation.** Like every platform predicate, a
`skill-refiner-pass/v1` row stands alone: silence ≠ failure. The absence of a
row for some skill or some dimension means "no PASS was emitted for that," never
"that failed." Rows are unioned across a bundle, not joined (Blueprint B § 7.1).

---

## 2. In-toto Statement v1 envelope

Per DR-082 Q4 (7–0 MIRROR `gate-result/v1` exactly — no bespoke envelope), every
`skill-refiner-pass/v1` row MUST be a well-formed
[in-toto Statement v1](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md)
document with the following top-level structure:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [ { "name": "<subject-name>", "digest": { "sha256": "<hex>" } } ],
  "predicateType": "https://evals.intentsolutions.io/skill-refiner-pass/v1",
  "predicate": { ... predicate body per § 5 ... }
}
```

The row MUST be wrapped for distribution in a
[DSSE](https://github.com/secure-systems-lab/dsse) (Dead Simple Signing Envelope)
signed envelope, `payloadType` `application/vnd.in-toto+json` — byte-identical
to the `gate-result/v1` wrapping in Blueprint B § 7.1:

```json
{
  "payloadType": "application/vnd.in-toto+json",
  "payload": "<base64-encoded Statement JSON>",
  "signatures": [
    { "keyid": "<cosign keyless OIDC subject + issuer fingerprint>", "sig": "<base64 signature>" }
  ]
}
```

**Row independence.** Each row MUST be independently verifiable. A consumer MUST
NOT require any other row in the same bundle to verify a given row's signature or
schema validity.

**No top-level signature.** A bundle as a whole MUST NOT carry a top-level
"bundle signature." All signatures are row-level (Blueprint B § 7.1). This
preserves row independence and the composable-partial-attestation principle.

**Body-vs-envelope split.** The kernel JSON Schema (§ 5) validates ONLY the
`predicate` body. The enclosing Statement envelope (`_type`, `subject`,
`predicateType`) is validated separately, exactly as for `gate-result/v1`.

---

## 3. Predicate URI registration

The exact predicate URI string is:

```text
https://evals.intentsolutions.io/skill-refiner-pass/v1
```

Per DR-082 Q1 (7–0 FLAT), the URI is a **flat sibling** of `gate-result/v1`,
distinguished only by the type name `skill-refiner-pass`. There is **no
`/authoring/` segment, ever.** The grammar `evals.intentsolutions.io/<predicate-type>/v<version>`
is locked (DR-010 Q2 CTO non-negotiable); inserting a chamber token would
silently mutate the predicate-URI grammar for every consumer's subject-matching
logic and would invite a reader to treat the signed PASS as authoring-lint
output — the exact trust-class confusion DR-081 forbids. The PASS is a
behavioral-gate attestation, runtime-class; it must never wear an `/authoring/`
costume.

**Chamber isolation lives below the wire.** The SAK-charter-Q3 (DR-081)
"distinct predicate-URI namespace" for the authoring chamber is satisfied by
three real, enforceable separations — NONE of them a URL segment:

1. the chamber's **SEPARATE signing trust root** (DR-081 Q3 no-shared-root; the
   design is § 084, and provisioning it is § 6 production trigger 3);
2. the chamber's independent **`$schemaVersion` lane** (so a runtime-driven
   schema bump never drags the authoring lane);
3. the kernel **file path** (`src/predicates/skill-refiner-pass-v1.ts` +
   `schemas/v1/skill-refiner-pass.schema.json`).

**The URI is effectively immutable** once any row referencing it is signed and
pushed to a transparency log (sigstore staging or production Rekor). Per DR-004
Q1 + DR-010 reaffirmation, `evals.intentsolutions.io` is reserved EXCLUSIVELY for
predicate URIs and MUST be DNSSEC-enabled with CAA records pinned before any
signed attestation referencing this URI is pushed to a public transparency log
(§ 6 trigger 2). `labs.intentsolutions.io` is reserved-don't-touch and MUST NOT
host this or any predicate URI (DR-004 CISO binding).

**Predicate-type registry.** The row for this URI in `specs/PREDICATE-TYPES.md`
moves from `RESERVED` to `ACTIVE` when this section lands (this is § 6 trigger 1).
The registry MUST record the first-signed-attestation date within 7 days of the
first signed row going live (Blueprint B § 7.2 GC discipline). Registry drift is
unrecoverable; the registry IS the canonical record of which URIs exist.

---

## 4. Subject naming convention

Per DR-082 Q4 (CISO/CSO authoring-chamber clarification), the in-toto `subject`
field of each `skill-refiner-pass/v1` row MUST contain at least one entry whose
`name` field matches the `gate-result/v1` subject-name grammar (Blueprint B
§ 7.3), specialized to the authoring chamber:

```text
^[a-z0-9][a-z0-9-]*:(client|server|ci|sandbox|local):[a-zA-Z0-9][a-zA-Z0-9.-]*$
```

The recommended authoring-chamber idiom (mirroring `gate-result/v1`'s
`tool:side:gate-id`) is:

```text
skill-refiner:<side>:<skill-version-id>
```

| Segment             | Meaning                                                                                                | Examples                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| **Tool**            | The runner that produced the row. Lowercase, kebab-case.                                               | `skill-refiner`, `j-rig`                                       |
| **Side**            | Which side of the pipeline emitted the row. Closed enum: `client`, `server`, `ci`, `sandbox`, `local`. | `ci` (post-merge refiner run), `local` (developer workstation) |
| **Gate ID segment** | The accepted SkillVersion identity discriminator — the row's `skill_version_id`.                       | a UUIDv7                                                       |

**Subject digest — the load-bearing tamper-evidence binding (DR-082 Q4).** The
in-toto `subject[].digest` map MUST include the `sha256` key, and its value MUST
equal the predicate body's `source_snapshot_hash` **with the `sha256:` prefix
removed**. This is the authoring-chamber analogue of `gate-result/v1`'s
`input_hash` === subject-digest binding (Blueprint B § 7.3): it cryptographically
ties the signed PASS to the exact post-edit `SkillVersion` content. A verifier
MUST reject a row whose subject digest does not equal `source_snapshot_hash`
without the prefix. The subject MUST resolve to a content-addressed artifact —
the digest is the SkillVersion snapshot's identity. This is what stops a refiner
from laundering an unrelated skill snapshot through a forged subject.

---

## 5. `skill-refiner-pass/v1` predicate body — schema

The `predicate` field MUST validate against the canonical JSON Schema published
in the kernel package at `@intentsolutions/core/schemas/v1/skill-refiner-pass.schema.json`
(GH source: [`intent-eval-core/schemas/v1/skill-refiner-pass.schema.json`](https://github.com/jeremylongshore/intent-eval-core/blob/main/schemas/v1/skill-refiner-pass.schema.json)).
This section is the normative **prose** specification; the kernel JSON Schema is
the normative **machine-readable** specification. The two MUST agree; on
disagreement the kernel JSON Schema wins for machine-validation purposes and this
section is amended to match (§ 7.0 / § 7.4 precedence inherited from
Blueprint B). The schema is `additionalProperties: false` — unknown fields are a
validation failure, not silently tolerated.

The body carries exactly the **accept determinants** (DR-082 Q2): the fields a
verifier needs to independently re-derive the accept decision from immutable
inputs. Provenance _bulk_ (raw per-eval-item transcripts, human-readable diff
prose, dashboard-render metadata) is OUT of the signed body — referenced by hash
via the EvidenceBundle side-channel, never inlined. This is the
minimal-signed-surface / complete-provenance reconciliation DR-082 Q2 ratified.

### 5.1 Required fields (the accept determinants)

| Field                    | Type                                            | Normative semantics                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------ | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `verdict`                | enum `accept \| reject`                         | Decision verdict — the accept-record discriminator. CLOSED enum; a row is emitted on a real verdict. Widening this enum is a **/v2** trigger (DR-082 Q5 CISO binding: a consumer that hard-codes the closed set must never silently encounter a third verdict on an immutable row).                                                                                                                                                                                                                                   |
| `reason`                 | array of strings, `minItems: 1`                 | Structured reason entries — non-empty always. Reasons SHOULD be **structured codes, not free prose**, to avoid leaking skill content onto a public transparency log (DR-082 Q2 CISO + GC binding).                                                                                                                                                                                                                                                                                                                    |
| `refiner_strategy_id`    | string, `minLength: 1`                          | Identifier of the `RefinerStrategy` that produced the verdict. **REQUIRED in the signed body** per the DR-028 CISO Session-7 binding: mechanism-swappable must not become mechanism-untraceable. Strategy ids are **append-only-registered** — a retired id is burned forever, never reused for a different mechanism (DR-082 Q5).                                                                                                                                                                                    |
| `skill_version_id`       | UUIDv7 (kernel `$defs/uuidv7`)                  | UUIDv7 of the accepted `SkillVersion` (the 14th kernel entity, DR-028 T1). Referenced by the kernel's EXISTING UUIDv7 primitive — this predicate does NOT define a SkillVersion entity (DR-028 one-way door).                                                                                                                                                                                                                                                                                                         |
| `parent_version_id`      | UUIDv7 (kernel `$defs/uuidv7`)                  | UUIDv7 of the parent `SkillVersion` the accepted version was refined from. Binds **parent → child** so a refiner cannot launder an unrelated skill through a forged lineage (DR-082 Q2 CISO binding).                                                                                                                                                                                                                                                                                                                 |
| `source_snapshot_hash`   | sha256-prefixed (kernel `$defs/sha256Prefixed`) | sha256-prefixed content hash of the **post-edit** SkillVersion source snapshot. The in-toto `subject[].digest.sha256` MUST equal this value **without** the `sha256:` prefix (§ 4 — the tamper-evidence binding, DR-082 Q4). References the SkillSnapshot content by the kernel's EXISTING sha256-prefixed primitive (reference, not FK — DR-028 T1).                                                                                                                                                                 |
| `eval_set_ref`           | object `{ hash, version, lineage_id }`          | Reference to the **FROZEN** eval-set the verdict was derived against — the entire epistemic basis of the claim. `hash` (sha256-prefixed) pins exact content; `version` (string, `minLength: 1`) pins which published eval-set; `lineage_id` (UUIDv7) pins the eval-set lineage. A production PASS over a _mutable_ eval-set is unverifiable by definition (DR-082 Q3 frozen-eval lock). `additionalProperties: false`.                                                                                                |
| `edit_proposal_hash`     | sha256-prefixed (kernel `$defs/sha256Prefixed`) | sha256-prefixed hash of the `EditProposal` (the bounded edit-ops) that earned the pass — binds **WHAT changed**.                                                                                                                                                                                                                                                                                                                                                                                                      |
| `behavioral_delta`       | number                                          | Observed delta on the behavioral dimension the accept gate requires significant Pareto-dominance on. A determinant of the accept decision.                                                                                                                                                                                                                                                                                                                                                                            |
| `named_dimension_deltas` | array of `{ id, delta, non_regressed }`         | Per-named-dimension observed deltas — the **non-regression surface** of the accept gate. Each entry is independently re-checkable: a verifier re-runs the one-sided z-test on these deltas at the stated `alpha`. `id` is a kebab-slug dimension identifier; `delta` is a number; `non_regressed` is a boolean. For an `accept` verdict every entry's `non_regressed` MUST be `true`. MAY be empty when the skill declares no named dimensions beyond the behavioral one. Each item is `additionalProperties: false`. |
| `alpha`                  | number, `(0, 1)` exclusive                      | The significance level (α) the one-sided z-test was evaluated at — the **falsifiability anchor**. A PASS with no published `alpha` is an unfalsifiable assertion (DR-082 Q2).                                                                                                                                                                                                                                                                                                                                         |
| `test_statistic_kind`    | const `one-sided-z`                             | Statistical-test family identifier. CONST for v1 — the acceptance gate is a one-sided z-test (DR-028 + DR-082 Q2). Changing the test family is a SEMANTIC change that mints **/v2** (the same deltas/alpha would no longer mean the same verdict).                                                                                                                                                                                                                                                                    |

### 5.2 Optional fields (descriptive, NOT determinants)

| Field                      | Type                                        | Normative semantics                                                                                                                                                                      |
| -------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cost_record_ref`          | UUIDv7 (kernel `$defs/uuidv7`)              | OPTIONAL reference → `CostRecord.id` for cost attribution of the refiner run. Descriptive — NOT a determinant of accept. Consumers MUST NOT treat its absence as a verification failure. |
| `replay_fidelity_level`    | enum `RF-0 \| RF-1 \| RF-2 \| RF-3 \| RF-4` | OPTIONAL replay-fidelity claim for the refiner run, mirroring `gate-result/v1`'s iel-E11 levels.                                                                                         |
| `signing_downgrade_reason` | string, `minLength: 1`                      | OPTIONAL structured reason recorded ONLY when the `signing_mode` was downgraded for this row (e.g. a production→staging fallback). Absent on a normally-signed row.                      |

**Determinant rule (DR-082 Q2 / DR-082 Q5 CTO addendum).** A field belongs in the
REQUIRED set iff a verifier needs it to independently re-derive the accept
decision. The optional fields above are purely descriptive and cannot affect the
accept decision. Per the DR-082 Q5 freeze-rule nuance, the §-7.2-style
"optional-additive needs no URI bump" carve-out applies ONLY to such
purely-descriptive optionals — an "optional" field that participates in the
accept decision (a new dimension semantics, a tie-break flag) is NOT a free
additive change; it is at minimum Class-1, because it silently changes what PASS
means across signed rows.

### 5.3 Verdict semantics

- `accept` — the SkillVersion cleared the gate: significant Pareto-dominance on
  the behavioral dimension AND every `named_dimension_deltas[].non_regressed` is
  `true`, by a one-sided z-test at `alpha`. This is the PASS the URI's category
  claim refers to.
- `reject` — the gate evaluated and the SkillVersion did not clear it. The
  `reason[]` MUST document the specific failure (a regressed named dimension, an
  insignificant behavioral delta at the stated `alpha`).

The `reject` verdict is part of the closed enum so the predicate can carry a
real, signed _negative_ result when a refiner run is attested end-to-end — but a
relying party treating the URI as a "this skill got better" badge keys on
`verdict === "accept"`, never on the presence of a row alone.

### 5.4 Hash format

`source_snapshot_hash`, `edit_proposal_hash`, and `eval_set_ref.hash` MUST be
prefixed `sha256:` followed by 64 lowercase hexadecimal characters (the kernel
`$defs/sha256Prefixed` primitive). The in-toto `subject[].digest.sha256` value is
the prefix-stripped form of `source_snapshot_hash` (§ 4). Consumers MUST treat an
unknown algorithm prefix as a verification failure for the **row**, not the
bundle.

---

## 6. Staging → production posture (DR-082 Q3 — the four triggers)

Per DR-082 Q3 (7–0 staging-first), `skill-refiner-pass/v1` ships in
`sigstore_staging` and becomes **production-Rekor-signable ONLY when ALL FOUR
triggers hold, AND-gated**. The kernel `SigningMode` flip is the _effect_ of the
four triggers holding, never a trigger itself. (The kernel comment refers to the
staging posture by the shorthand `ln`; the kernel `SigningMode` enum value is
`sigstore_staging` — `'sigstore_staging' | 'rekor_production' | 'unsigned_experimental'`.)

| #     | Trigger                                                                                                                                                   | Status as of this section                                                                                                                      | Owner                      |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **1** | The `skill-refiner-pass/v1` SPEC.md **normative section lands** (RESERVED→ACTIVE in `PREDICATE-TYPES.md`).                                                | **ADVANCED by this document** — landing this section on `intent-eval-lab` main satisfies trigger 1.                                            | this PR                    |
| **2** | **DNSSEC + CAA pre-flight green** on `evals.intentsolutions.io` (iah-E06-class).                                                                          | Already green for `gate-result/v1`; this is **verify-still-green**, not rebuild — the host posture is shared.                                  | maintainer (verify)        |
| **3** | The authoring chamber's **SEPARATE signing trust root is provisioned-and-live** (DR-081 no-shared-root — the NEW gating step `gate-result/v1` never had). | **DESIGN ADVANCED** by § 084; **PROVISIONING is maintainer-run infra** — not satisfiable by a doc.                                             | maintainer (infra)         |
| **4** | **≥1 REAL SkillVersion clears the behavioral gate on a FROZEN, signed eval-set** (a green row, not a synthetic fixture).                                  | **BLOCKED** — requires `@intentsolutions/core` published with this predicate + the SkillVersion entity, then a real `@j-rig/refiner-core` run. | maintainer (release + run) |

Until all four hold, every `skill-refiner-pass/v1` row carries
`signing_mode = "sigstore_staging"` and `rekor_log_index = null`, per the DR-028
cross-field invariant ("`rekor_log_index` iff `signing_mode = production`"). Per
DR-018 STAGING-STAYS-STAGING, any draft attestation signed in staging STAYS
staging forever — it is never retro-promoted to production.

**Trigger 3 is the charter-Q3-mandated addition.** `skill-refiner-pass/v1` is the
FIRST authoring-chamber predicate to head toward production. It CANNOT free-ride
`gate-result/v1`'s production unlock the way the runtime CONDITIONAL predicates
do, because DR-081 Q3 permits NO shared signing trust root: the authoring chamber
must stand up its own Fulcio identity + Rekor posture (§ 084) before its first
production signature, or trust domains silently fuse on the first signature — the
one un-rollback-able mistake (DR-082 Q3 CISO most-costly).

**Trigger 4 is the non-vacuity lock.** A production-Rekor row for a predicate that
has never once fired on real data — over a _frozen, signed_ eval-set whose hash is
the one written into the body — would be the worst possible founding row: an
empty badge immortalized in a public append-only log. Prove it fires on real
data, then mint it forever.

---

## 7. Signing and verification

**Signing.** Each row MUST be wrapped in DSSE and signed via
[cosign](https://docs.sigstore.dev/cosign/overview/) keyless mode (OIDC-backed
Fulcio short-lived certificates), exactly as `gate-result/v1` (Blueprint B § 7.5).
The OIDC identity proves who emitted the row. **The cosign keyless OIDC identity
MUST resolve to the AUTHORING chamber's Fulcio identity, distinct from the
runtime chamber's** (DR-081 Q3; DR-082 Q4 CISO divergence-b). A
`skill-refiner-pass/v1` row signed by a runtime-chamber keyid is INVALID — the
authoring/runtime chamber boundary is enforced **cryptographically at the
keyid**, not structurally in the envelope or URL. The trust-root design + the
maintainer provisioning steps are § 084.

Two signing modes are supported:

1. **sigstore staging** (`rekor.sigstage.dev`) — the default until ALL FOUR § 6
   triggers hold. Rows carry `signing_mode = sigstore_staging`.
2. **production Rekor** (`rekor.sigstore.dev`) — unlocked ONLY when all four § 6
   triggers hold, including the SEPARATE authoring trust root being live.

**Transparency-log anchoring.** A signed row SHOULD be pushed to the
[Rekor](https://docs.sigstore.dev/rekor/overview/) log (staging or production per
signing mode). Once anchored, the row's verdict is permanently and publicly
verifiable without contacting Intent Solutions — the platform's load-bearing
audit guarantee.

**Verification.** A conforming verifier:

1. MUST validate each row's DSSE signature against the signing identity (cosign
   keyless OIDC subject + issuer match for the **authoring chamber** identity, OR
   cosign keyref).
2. MUST validate the predicate body against the kernel JSON Schema at
   `@intentsolutions/core/schemas/v1/skill-refiner-pass.schema.json` (canonical
   per § 5).
3. MUST confirm `subject[].digest.sha256` equals `predicate.source_snapshot_hash`
   with the `sha256:` prefix removed (§ 4).
4. MUST, for an `accept` verdict, be able to re-run the one-sided z-test on
   `behavioral_delta` + `named_dimension_deltas[]` at `alpha` and confirm every
   `named_dimension_deltas[].non_regressed` is `true`.
5. SHOULD confirm a Rekor entry exists when the row claims Rekor anchoring (via
   `cosign verify-attestation --rekor-url`), against the **production** Rekor URL
   only when `signing_mode = rekor_production`.
6. MUST NOT treat the absence of optional fields (`cost_record_ref`,
   `replay_fidelity_level`, `signing_downgrade_reason`) as a verification failure.

The reference verifier command (staging shown; swap `--rekor-url` for production
only against a `rekor_production` row):

```bash
cosign verify-attestation \
  --type 'https://evals.intentsolutions.io/skill-refiner-pass/v1' \
  --certificate-identity-regexp '<authoring-chamber OIDC identity regexp — see § 084>' \
  --certificate-oidc-issuer '<authoring-chamber OIDC issuer — see § 084>' \
  --rekor-url https://rekor.sigstage.dev \
  oci://<bundle-blob-reference>
```

The `--certificate-identity-regexp` and `--certificate-oidc-issuer` for the
authoring chamber are defined by the trust-root design in § 084 and MUST be
distinct from the runtime chamber's identity. A verifier MUST NOT accept a
`skill-refiner-pass/v1` row whose certificate identity resolves to the runtime
chamber.

---

## 8. Versioning + immutability (DR-082 Q5, inheriting DR-064)

This is a **net-new** predicate URI — ADDITIVE per Blueprint B § 7.2 backward-compat.
No existing v1 contract is changed by minting it.

Once the first row referencing this URI is signed to production Rekor, the body is
frozen by the medium (append-only, externally replicated). The freeze rule
(DR-082 Q5, inheriting DR-064):

1. At v1, **NO** required field is ever removed, and **NO** field's
   type / semantics / enum-value / constraint is ever changed or loosened.
2. Adding OR loosening **ANY** field in the signed body requires a fresh
   **Class-1 ISEDC** convening. (Per DR-082 Q5 the strict default is
   convene-always on an immutable medium; purely-descriptive optional-additive
   fields are the only carve-out, and even those are a recorded, convened act.)
3. A **breaking** change mints a NEW URI `skill-refiner-pass/v2` on its OWN
   `$schemaVersion` lane and its OWN authoring-chamber body file — **v1 is NEVER
   edited in place.** v1 rows in the wild remain valid forever and are never
   reinterpreted.
4. **Enum widening is a /v2 trigger, not an additive change** (DR-082 Q5 CISO):
   widening `verdict` (or any closed enum) in place is a downgrade-confusion
   vector — a consumer that hard-codes `accept | reject` must never silently
   encounter a third value on an immutable row.
5. **`refiner_strategy_id` cannot be quietly weakened within v1** (DR-082 Q5 CSO):
   relaxing it from REQUIRED, or admitting a sentinel/null, is a SEMANTIC
   loosening → a /v2 event. Strategy ids are append-only-registered, never reused
   for a different mechanism.
6. The authoring chamber versions on an **independent `$schemaVersion` lane and an
   independent evolution clock** (DR-081 Q3 / DR-082 Q5 CSO) — a runtime-chamber
   schema bump never drags the authoring lane.

---

## 9. References

- Minting ADR (the 5 binding decisions Q1–Q5): `082-AT-DECR-isedc-skill-refiner-pass-v1-predicate-uri-2026-06-17.md`
- SAK Class-1 charter (Q3 no-shared-trust-root mandate): `081-AT-DECR-isedc-sak-class-1-charter-ratification-2026-06-17.md`
- The separate authoring signing-root DESIGN (§ 6 trigger 3): `084-AT-SPEC-authoring-chamber-signing-trust-root-design-2026-06-17.md`
- The mirrored precedent (`gate-result/v1` normative fold): Blueprint B `012-AT-ARCH-platform-runtime-blueprint.md` § 7
- Payload bindings (refiner_strategy_id signed; significance threshold normative; SkillVersion 14th entity): `028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md`
- Predicate-compat policy (inherited by DR-082 Q5): `064-AT-DECR-evidence-bundle-predicate-compatibility-policy-2026-06-12.md`
- Kernel JSON Schema (machine-readable authority): `@intentsolutions/core/schemas/v1/skill-refiner-pass.schema.json`
- Kernel TypeScript surface: `@intentsolutions/core/predicates/skill-refiner-pass-v1`
- Registry: `specs/PREDICATE-TYPES.md` (this section flips the row RESERVED→ACTIVE)
