# `conformance-test-suite/` — placeholder

The reference test suite for [SPEC.md](../SPEC.md) lands in Phase B alongside `IEL-7` (Evidence Bundle CLI in Go).

## Planned shape (mirrors `mcp-plugin-observability` test-suite design)

- **`runner/`** (Go) — drives the CLI against fixture bundles, runs assertions
- **`fixtures/`** — labeled bundles per requirement (positive + negative)
- **`assertions/`** (Go) — per-requirement assertion modules (R1..R6 per spec)
- **`schema-validation/`** — round-trip tests against the JSON Schema files (per `IEL-4`)

## Important

The test runner is implemented in Go for the same reasons as the `mcp-plugin-observability` runner (single static binary, native OTel ecosystem). The **spec itself stays language-neutral** — implementers in Python, TypeScript, Rust, or any other runtime can author conformant tooling without first installing a Go toolchain. Conformance is measured against the spec, not against this reference runner.
