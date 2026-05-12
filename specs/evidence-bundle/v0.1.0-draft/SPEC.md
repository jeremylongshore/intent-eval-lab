# Evidence Bundle Spec — v0.1.0-draft

> **Status: NORMATIVE DRAFT.** Phase B Milestone 1 of the build journey (`se-the-council-bubbly-frog.md`)
> elevates this file from Phase A skeleton to normative draft. Subsequent reference implementations
> (`audit-harness` v0.3.0 emission + `j-rig-binary-eval` v0.15.0 emission +
> `intent-rollout-gate` v0.1.0 consumer) inform `v0.1.0-rc` / `v0.1.0` revisions.

## 1. Purpose

An **Evidence Bundle** is a tamper-evident, schema-versioned, signature-verifiable collection of
**in-toto Statement v1 rows** attesting to deterministic gate results and behavioral verdicts
produced anywhere in the agent-native CLI evaluation pipeline.

The bundle's value proposition is independent verifiability. Any party with access to the public
component of the signing key — or with access to the Rekor transparency log — can confirm every
row in a bundle without trusting Intent Solutions, the team that produced the bundle, or the tools
that generated the rows. **No trust in any single party is required to verify an Evidence Bundle
result.**

The bundle is **composable**: partial coverage is explicitly valid. A bundle that contains rows
for three of six failure-mode categories means "these three were tested; the other three were not"
— it does NOT mean "the other three failed." The consumer-facing policy declared in
`tests/TESTING.md` decides whether partial coverage is acceptable; the Evidence Bundle merely
records what was attested.

## 2. Scope

### 2.1 In scope (v0.1.0-draft)

| Concern | Where in this spec |
|---|---|
| Bundle envelope structure (collection of in-toto Statement v1 rows) | § 4 |
| Predicate URI for gate results | § 5 |
| Predicate body schema (`gate_id`, `result`, hashes, timestamp, runner, commit) | § 5, schema file |
| Subject naming convention (pipeline-hop discriminator) | § 6 |
| Signing & verification (cosign-compatible, Rekor anchor) | § 7 |
| Policy consumption — how `tests/TESTING.md` consumes bundles | § 8 |
| Version evolution (`bundle_version` vs `predicateType` URI) | § 9 |
| Conformance reporting | § 10 |

### 2.2 Out of scope (v0.1.0-draft)

- **Domain-specific gate semantics** — what `escape-scan` means, what `MM-3 cooldown` means.
  Those live in the originating tool's documentation (`audit-harness` README,
  `mcp-plugin-observability` spec).
- **Policy as peer spec module.** Policy is consumer-facing config in the consuming repository's
  `tests/TESTING.md` file. § 8 specifies the consumption interface only. A peer-spec policy
  schema module is deferred (`000-docs/FUTURE.md`).
- **Canary / progressive-delivery decisions.** Those live in the `intent-rollout-gate` repo's
  decision logic; the Evidence Bundle is the input, not the policy.
- **Human-readable verdict rendering.** UI concerns are downstream consumers.
- **Gateway / federated-MCP-server attestation composition.** Deferred per ISEDC Session 3 Q3
  (`000-docs/FUTURE.md` — Gateway / Universal MCP Server entry).

## 3. Conformance keywords

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY** are used per
[RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) and
[RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174).

## 4. Bundle envelope structure

### R1 — Bundle is a collection of in-toto Statement v1 rows

An Evidence Bundle **MUST** be representable as a sequence of zero or more
[in-toto Statement v1](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) rows.

Each row **MUST** be a self-contained in-toto Statement v1 document. A bundle producer **MAY**
serialize the bundle as:

- **A directory of files** — one signed Statement per file (recommended for CI artifacts);
- **A JSON Lines (`.jsonl`) file** — one Statement per line;
- **A JSON array** under a top-level `bundle.rows` key — convenient for tooling that wants a
  single-document representation.

The container format **MUST NOT** alter the row contents. Hashing, signing, and verification
operate on each row independently.

### R2 — Row independence

Each row **MUST** be independently verifiable. A consumer **MUST NOT** require the presence of
any other row in the same bundle to verify a given row's signature or schema validity.

This is the **composable partial attestation** principle: bundles are unioned, not joined.
Producers in different CI stages, in different processes, on different machines, **MAY** emit
their rows without coordination beyond agreeing on the bundle's destination filesystem path.

### R3 — No top-level signature

A bundle as a whole **MUST NOT** carry a top-level "bundle signature." All signatures are
row-level (§ 7). This preserves R2 and prevents partial-bundle verification failures when a
bundle is split or merged across pipeline stages.

## 5. The `gate-result/v1` predicate

### R4 — Predicate URI

A row attesting to a deterministic gate result **MUST** set
`predicateType` to the exact URI:

```
https://evals.intentsolutions.io/gate-result/v1
```

The URI is **immutable** once published. Any breaking change to the predicate body **MUST** mint
a new URI at the next major version (§ 9). Per ISEDC v1 Q1 binding constraint (2026-05-10), the
namespace `evals.intentsolutions.io` is reserved exclusively for predicate URIs and **MUST** be
DNSSEC-enabled with CAA records pinned to a single Certificate Authority before any signed
attestation referencing the URI is pushed to a public transparency log.

### R5 — Predicate body schema

The `predicate` field **MUST** validate against the JSON Schema at
[`schema/gate-result.schema.json`](./schema/gate-result.schema.json).

Required fields:

| Field | Type | Description |
|---|---|---|
| `gate_id` | string | Pipeline-hop-qualified gate identifier (see § 6). |
| `result` | enum: `PASS` / `FAIL` / `ADVISORY` / `NOT_APPLICABLE` | Verdict for this gate execution. |
| `policy_hash` | string (sha256 prefix) | SHA-256 of the policy file the gate evaluated against, prefixed `sha256:`. |
| `input_hash` | string (sha256 prefix) | SHA-256 of the input artifact the gate evaluated, prefixed `sha256:`. |
| `timestamp` | string (RFC 3339 UTC) | Moment the gate emitted the result. |
| `runner` | string | Identifier of the tool + version that produced the row, e.g. `audit-harness@0.3.0`. |
| `commit_sha` | string | Git commit SHA the gate evaluated against (full 40-hex or short 7-hex acceptable). |

Optional fields:

| Field | Type | Description |
|---|---|---|
| `metadata` | object | Free-form tool-specific metadata. Consumers **MUST NOT** rely on metadata fields for ship/no-ship decisions; metadata is informative only. |
| `failure_mode` | string | When `result` is `FAIL`, an identifier classifying the failure shape (e.g. `MM-4`). Refer to the originating tool's documentation for the value space. |
| `advisory_severity` | enum: `info` / `warn` / `error` | When `result` is `ADVISORY`, the severity tier. |

### R6 — Result semantics

- `PASS` — the gate evaluated and the input met the policy.
- `FAIL` — the gate evaluated and the input did not meet the policy. The bundle row **MUST**
  populate `failure_mode` where the originating tool defines one.
- `ADVISORY` — the gate evaluated and emits a non-blocking signal. Consumers **MAY** treat
  `ADVISORY` as informational. Policies in `tests/TESTING.md` **MAY** elevate advisories to
  blocking via the consumer-side policy interface.
- `NOT_APPLICABLE` — the gate determined the input is outside its evaluation scope (e.g.
  `MM-3 cooldown` checks against a repo that ships no MCP server). A `NOT_APPLICABLE` verdict
  **MUST NOT** be interpreted as `FAIL`. It is an accurate statement that the dimension was
  not evaluated.

### R7 — Hash format

`policy_hash` and `input_hash` values **MUST** be prefixed with `sha256:` followed by 64 hexadecimal
characters in lowercase. Other hash algorithms **MAY** be added in a future minor version of this
predicate URI; consumers **MUST** treat unknown algorithm prefixes as causing a verification failure
for the row, not the bundle.

## 6. Subject naming convention

### R8 — Subject form

The in-toto `subject` field of each row **MUST** contain at least one entry whose `name` matches
the regular expression:

```
^[a-z0-9][a-z0-9-]*:(client|server|ci|sandbox|local):[a-zA-Z0-9][a-zA-Z0-9.-]*$
```

The three colon-separated segments are:

| Segment | Meaning | Examples |
|---|---|---|
| **Tool** | The runner that produced the row. Lowercase, kebab-case. | `audit-harness`, `j-rig`, `intent-rollout-gate` |
| **Side** | Which side of the pipeline emitted the row. Closed enum. | `client` (pre-commit, local), `server` (CI pipeline), `ci` (post-merge CI), `sandbox` (experimental), `local` (developer workstation, ad-hoc) |
| **Gate ID** | Tool-specific gate or check identifier. Either lowercase kebab-case or the originating tool's documented identifier (e.g. `MM-1`..`MM-6` from the Intentional Mapping vocabulary). Mixed case is permitted; the originating tool's documentation defines the value space. | `escape-scan`, `crap-score`, `MM-3`, `harness-hash` |

A subject `name` **MUST** match `gate_id` in the predicate body. Bundle producers **MAY** include
additional `subject` entries (e.g. file-level digests of evaluated inputs) but **MUST** include the
pipeline-hop-discriminator entry per this rule.

### R9 — Digest

The in-toto `subject[].digest` map **MUST** include at least the `sha256` key matching the value of
`predicate.input_hash` for the same row. Consumers **MUST** reject a row whose subject digest does
not match its predicate `input_hash`.

## 7. Signing & verification

### R10 — Signature wrapping

Each row **MUST** be wrapped for distribution as an in-toto/sigstore-compatible signed envelope.
The recommended wrapping is [DSSE](https://github.com/secure-systems-lab/dsse) (Dead Simple
Signing Envelope), which is what `cosign attest` and `cosign sign-blob` emit by default.

### R11 — Signing identity

Signing **SHOULD** use [Sigstore cosign keyless](https://docs.sigstore.dev/cosign/signing/overview/)
mode (OIDC-backed Fulcio short-lived certificates) for v0.x bundles. Operators who require key-based
signing **MAY** use cosign key-based mode; in that case, the public key **MUST** be discoverable
via a deterministic mechanism (cosign keyref, repo-anchored `cosign.pub`, or sigstore key
discovery).

### R12 — Transparency log anchoring

A signed row **SHOULD** be pushed to the [Rekor](https://docs.sigstore.dev/rekor/overview/)
transparency log. Once Rekor-anchored, the row's verdict is permanently and publicly verifiable.

Operators **MAY** omit Rekor anchoring for private bundles (engagement-internal evaluation results
that have not yet received partner consent for public emission). When omitted, the row's
verifiability is reduced to whoever holds the signing key's public component — Rekor cannot be
substituted by claim.

### R13 — Verification

A conforming verifier:

1. **MUST** validate each row's DSSE signature against the signing identity (cosign keyless OIDC
   subject + issuer match, OR cosign keyref).
2. **MUST** validate the predicate body against this spec's JSON Schema for the `predicateType`.
3. **MUST** confirm `subject.digest.sha256` matches `predicate.input_hash`.
4. **SHOULD** confirm Rekor entry exists when the row claims Rekor anchoring (via
   `cosign verify-attestation --rekor-url`).
5. **MUST NOT** treat the absence of optional fields (metadata, failure_mode, advisory_severity)
   as a verification failure.

`cosign verify-attestation --type 'https://evals.intentsolutions.io/gate-result/v1' …` is the
reference verifier for v0.x.

## 8. Policy consumption — `tests/TESTING.md`

### R14 — Policy is NOT part of this spec

The Evidence Bundle attests to what was evaluated. A separate, consumer-facing policy decides
whether what was evaluated is sufficient to ship. **That policy is NOT a peer spec module under
this URI.** It lives as consumer-facing configuration in the consuming repository's
`tests/TESTING.md` file.

The decision to keep policy out of the predicate URI is explicit:

- The predicate URI is immutable once signed (R4). Policy evolves with every team's threshold
  adjustment.
- Coupling policy to the attestation surface would force every threshold change to mint a new URI.
- Policy schema across language ecosystems is heterogeneous; codifying it as a peer module is
  premature absent ≥2 independent implementations needing a shared format (deferred to
  `000-docs/FUTURE.md`).

### R15 — Consumption interface

A consumer of an Evidence Bundle (e.g. the `intent-rollout-gate` GitHub Action) **MUST**:

1. Read the bundle (any container form per R1).
2. Verify each row per R13.
3. Read the repository's `tests/TESTING.md` policy.
4. Evaluate the verified rows against the policy.
5. Emit a ship / no-ship / advisory decision.

The consumer **MUST NOT** modify the bundle. Decisions are themselves emittable as new in-toto
rows under a different `predicateType` (Phase C work, deferred).

### R16 — Example policy shape

[`examples/policy.yaml`](./examples/policy.yaml) is an **informative** example of a
`tests/TESTING.md` policy block. It is **not** normative. Tooling consuming a policy file
**MUST** define its own schema (e.g. `intent-rollout-gate`'s `action.yml` declares its expected
inputs); this spec does not pin a policy schema.

## 9. Version evolution

### R17 — URI immutability

The exact string `https://evals.intentsolutions.io/gate-result/v1` is permanent once any row
referencing it is signed and pushed to Rekor. Breaking changes (removing a required field,
narrowing an enum, changing semantics of an existing field) **MUST** mint a new URI:
`https://evals.intentsolutions.io/gate-result/v2`. Both URIs **MAY** coexist; consumers that
support only v1 **MUST** reject v2 rows rather than mis-interpreting them.

### R18 — Additive minor versions

Adding new optional fields, adding new enum values to optional enums, and clarifying prose
**MUST NOT** require a URI bump. The JSON Schema at `schema/gate-result.schema.json` **MUST**
remain backward-compatible across minor revisions of this draft.

### R19 — Draft → RC → stable

- `v0.1.0-draft` — this document; normative requirements are subject to revision pending
  reference implementations.
- `v0.1.0-rc` — first reference implementation (`audit-harness` v0.3.0) emits against this spec;
  any required revisions land here.
- `v0.1.0` — at least one **non-Intent-Solutions** party emits a row against this URI and the
  row verifies. The URI is then frozen permanently.

## 10. Conformance reporting

A claim of conformance against this spec at version `v0.1.0` (or later) **MUST** be substantiated
by a conformance report linking to:

1. At least one publicly verifiable Rekor entry whose `predicateType` matches R4.
2. The signing-identity public component (cosign public key or OIDC subject + issuer pair).
3. The commit SHA of the codebase that emitted the row.
4. A `tests/TESTING.md` (or equivalent) policy file the producer evaluated against, if any.

Conformance reports for reference implementations land under
`specs/evidence-bundle/v0.1.0-draft/conformance-reports/`.

## 11. Examples

| File | What it is |
|---|---|
| [`examples/in-toto-statement.json`](./examples/in-toto-statement.json) | One well-formed in-toto Statement v1 row attesting a passing `audit-harness:client:escape-scan` gate. |
| [`examples/evidence-bundle.json`](./examples/evidence-bundle.json) | A multi-row bundle (audit-harness static gates + j-rig behavioral gates + an MM-3 NOT_APPLICABLE row) in JSON-array form. |
| [`examples/policy.yaml`](./examples/policy.yaml) | An informative `tests/TESTING.md` policy block illustrating coverage + pass-rate thresholds. **NOT normative.** |

## 12. Anchoring — primary sources this spec composes

This spec invents no primitives. It composes:

- [in-toto Statement v1](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) — envelope structure
- [DSSE](https://github.com/secure-systems-lab/dsse) — signature wrapping
- [Sigstore cosign](https://docs.sigstore.dev/cosign/overview/) — signing primitives
- [Rekor](https://docs.sigstore.dev/rekor/overview/) — transparency log anchor
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html) — predicate schema definition
- [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) / [RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174) — conformance keyword semantics
- [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) — timestamp format
- [OpenTelemetry semantic conventions](https://github.com/open-telemetry/semantic-conventions) — observability vocabulary (`agent.rollout.gate.*` events fire alongside row emission, per `000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`)

## 13. RFC

Comments, corrections, and counter-proposals are welcome via GitHub issues on
[`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) with
`[evidence-bundle]` in the title. Per `intent-eval-lab/CLAUDE.md` § "Brand-name policy", do not
file issues that name partner engagements absent written consent.

## 14. License

Apache 2.0 — see [LICENSE](../../../LICENSE) at repo root.
