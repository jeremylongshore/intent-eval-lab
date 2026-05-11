# Conformance Test Suite — placeholder

This directory will hold the reference test suite for [SPEC.md v0.1.0-draft](../SPEC.md). It's currently a placeholder; the test harness lands as part of the work tied to the first case-study implementation (engagement-private until the plugin maintainer consents to public release).

## Planned shape

The reference test runner is planned in **Go**. Single static binary distribution (`curl + chmod +x + run`, no interpreter or virtualenv ritual), fast cold start, native integration with the OTel ecosystem (Collector, Tempo, Honeycomb, Grafana stack are all Go), and an official Anthropic `mcp-go` SDK for MCP-aware test harnesses. The choice mirrors the precedent set by [`j-rig-binary-eval`](https://github.com/jeremylongshore/j-rig-binary-eval), the sibling 7-layer binary-criteria evaluation harness in the same author's portfolio.

- **`runner/`** (Go) — drives `claude -p` against a labeled prompt set via `os/exec`, captures the OTel signal stream (in-process via `go.opentelemetry.io/otel` exporters or via a sidecar Collector), runs assertions against the Intentional Mapping rows.
- **`fixtures/`** — labeled prompt sets per finding-shape (one prompt set per Intentional Mapping row).
- **`assertions/`** (Go) — per-requirement assertion modules (R1-R5 of the spec).
- **`collector-config/`** — minimal OTel Collector configuration (~10-line Docker compose) for local testing without an external observability backend.

### Important: spec artifacts stay language-neutral

The choice of Go for the test runner is a **runner-implementation decision**, not a spec-implementation decision. The normative artifacts in this module — [`SPEC.md`](../SPEC.md), the [Intentional Mapping template](../intentional-mapping-template.md), the case-study schema — stay language-neutral so a plugin author writing in Python, TypeScript, Rust, or any other runtime can author a conformant Intentional Mapping and submit a conformance report without first installing a Go toolchain. Conformance is measured against the spec, not against this reference runner.

If a Python-first or TypeScript-first runner reference is later useful for the contributor pool (e.g., a Python adapter that generates Intentional Mapping YAML and shells out to the Go binary, or a pure-TS port targeting Node-native CI), it lives alongside this Go runner under `runner-py/` or `runner-ts/`. Multiple reference implementations are welcome; the spec is the source of truth that all of them target.

## Why it's not here yet

A test suite asserting on `claude_code.hook` spans (deeper-beta) requires an OTel collector to be standing up. Collector standup is engagement-private work; pre-public-release, the spans are referenced as architectural primitives, not as a measurement claim — no published numbers without the collector standup having actually happened.

When the collector standup lands, the test suite lands here, and at least one case-study conformance report has its results validated against this suite, the spec is promotion-eligible from `v0.1.0-draft` to `v0.1.0-rc`.

## RFC

If you have an existing OTel collector standup pattern that would be a good fit for the reference test suite, file a GitHub issue on [`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) with `[mcp-plugin-observability]` in the title.
