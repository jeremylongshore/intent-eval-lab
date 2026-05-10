# Evidence Bundle Spec — v0.1.0-draft

> **Status: SKELETON.** Section headers only. No normative content yet. This file's Phase A deliverable is the structural skeleton; Phase B fills in normative requirements once the audit-harness side (`AH-4` envelope design notes) and the j-rig side (`JR-EPIC-03a` validator) inform the final shape. Per master plan `~/.claude/plans/please-take-your-time-glimmering-stardust.md` § "Phase A".

## Purpose

*(To be authored in Phase B. Anchor: this section will state what an Evidence Bundle is — a tamper-evident, schema-versioned, signature-verifiable container for gate results and verdicts produced by deterministic-gate runners and judgment harnesses across the agent-native CLI ecosystem.)*

## Scope

### In scope (Phase B)

- Bundle envelope structure
- Gate-result row shape (audit-harness emission target)
- Verdict row shape (j-rig emission target)
- Version-evolution rules (`bundle_version` vs `schema_version`)
- Signature-embedding semantics (cosign-compatible)

### Out of scope (Phase B)

- Domain-specific gate semantics (those live in the originating tool's docs)
- Canary / progressive-delivery decisions (those live in `IEL-CONV-6` Rollout Gate GHA)
- Human-readable verdict rendering (UI concerns are downstream)

## Anchoring

Every normative requirement in this spec will cite the canonical source it codifies:

- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html) — envelope schema definition
- [Sigstore cosign](https://docs.sigstore.dev/) — signing primitives
- [OpenTelemetry semantic conventions](https://github.com/open-telemetry/semantic-conventions) — observability signals (post-`IEL-CONV-7` RFC)
- [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) — keyword semantics (MUST / SHOULD / MAY)
- [RFC 8949 (CBOR)](https://datatracker.ietf.org/doc/html/rfc8949) — optional binary encoding for compact bundles

This spec does not invent primitives. It composes existing primitives into a testable, signable, diffable evidence record.

## Normative requirements (v0.1.0-draft — Phase B placeholders)

The keywords MUST, SHOULD, MAY are used per RFC 2119.

### R1 — Envelope structure

*(To be authored in Phase B. Will define the top-level envelope shape: manifest, signature, payload.)*

### R2 — Gate-result row shape

*(To be authored in Phase B. Will define `gate_id`, `result`, `timestamp`, `metadata`, `schema_version` fields. Co-developed with `AH-4` envelope design notes.)*

### R3 — Verdict row shape

*(To be authored in Phase B. Will define j-rig verdict emission shape. Co-developed with `JR-EPIC-04a` adapters.)*

### R4 — Version-evolution rules

*(To be authored in Phase B. Will define `bundle_version` semver semantics, `schema_version` semantics, and forward/backward compatibility rules.)*

### R5 — Signature integrity

*(To be authored in Phase B. Will define signing semantics: cosign-compatible, in-bundle vs out-of-bundle signature embedding, verification process.)*

### R6 — Tamper evidence

*(To be authored in Phase B. Will define hash-chain semantics across rows so that row-level tampering is detectable independently of envelope signature.)*

## Conformance reporting

A claim of conformance against this spec at version `vN.M.K-draft` will require a **conformance report** that:

1. *(To be authored in Phase B. Will mirror the conformance-reporting structure in [`mcp-plugin-observability/v0.1.0-draft/SPEC.md` § Conformance reporting](../../mcp-plugin-observability/v0.1.0-draft/SPEC.md#conformance-reporting).)*

## Versioning

- `v0.1.0-draft` — initial structural skeleton (this version, Phase A)
- `v0.1.0-rc` — first reference implementation in flight (Phase B)
- `v0.1.0` — at least one independent implementation ships a conformance report against the spec
- `v0.2.0+` — minor versions add new normative requirements; major versions break compatibility

## RFC

Comments, corrections, and counter-proposals welcome via GitHub issues on [`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) with `[evidence-bundle]` in the title.

This spec is in **structural skeleton** state during Phase A. Sharper challenges to the planned requirement set, the envelope shape, the signature embedding semantics, and the version-evolution rules are explicitly invited.

## License

Apache 2.0 — see [LICENSE](../../../LICENSE) at repo root.
