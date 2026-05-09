# MCP Plugin Observability Spec — v0.1.0-draft

> **Status: DRAFT.** This is a request for comment, not a finalized specification. Normative requirements are subject to change. No implementation has been independently certified yet. The first reference implementation case study is in progress against [`kobiton/automate`](./case-studies/kobiton-automate.md).

## Purpose

This spec codifies what it means for an **MCP plugin** to be *operationally observable* — i.e., for a third party (a regression suite, a partner, an auditor, an operator) to assert on the plugin's behavior at the protocol level without modifying the plugin's MCP server.

The spec is **vendor-neutral**. It applies to any MCP plugin published for any agentic-CLI runtime that emits OpenTelemetry signals (today: Claude Code; in the future: any harness that adopts equivalent telemetry primitives).

The spec is **non-prescriptive about the plugin's internal architecture.** It does not require the plugin to be written in any particular language, ship any particular file layout, or use any particular MCP transport. It only requires that **specific classes of plugin behavior are observable through the standard signal stream emitted by the harness.**

## Scope

In scope:

- Tool-call sequencing and step-count assertions
- Hook-firing presence/absence assertions (deterministic enforcement layer)
- MCP transport reliability assertions
- Skill / plugin discovery rate assertions

Out of scope:

- MCP server-internal behavior (response shape correctness, server-side cooldown enforcement, OAuth flow correctness — covered by the [MCP spec itself](https://modelcontextprotocol.io/specification))
- Latency / cost / throughput SLOs (orthogonal to observability)
- Functional correctness of the plugin's domain (e.g., "did the device test actually run on a real iPhone")

## Anchoring

Every normative requirement in this spec cites the canonical Anthropic source it codifies:

- [Claude Code monitoring (OTel surface)](https://code.claude.com/docs/en/monitoring-usage) — log events vs trace spans split, env-var gates
- [Claude Code hooks](https://code.claude.com/docs/en/hooks) — PreToolUse / PostToolUse / PostToolBatch surface, MCP tool matcher syntax
- [Claude Code plugins](https://code.claude.com/docs/en/plugins) — plugin manifest layout
- [Claude Code GitHub changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) — version-anchored rollout history

This spec does not invent telemetry primitives. It codifies how existing primitives compose into testable assertions.

## Normative requirements (v0.1.0-draft)

The keywords MUST, SHOULD, MAY are used per [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

### R1 — Tool-call observability

A conformant plugin MUST be observable via the harness's `tool_decision` log event for every tool the plugin exposes via its MCP server. The event MUST include the tool name in the form `mcp__<server-name>__<tool-name>`.

*(This requirement is automatically satisfied by Claude Code v2.1.x with `CLAUDE_CODE_ENABLE_TELEMETRY=1` and `OTEL_LOGS_EXPORTER=otlp`. The plugin needs to do nothing.)*

### R2 — Hook-firing observability

A conformant plugin SHOULD ship a `hooks/hooks.json` bundle declaring its deterministic-enforcement matchers using the `mcp__<server-name>__.*` matcher syntax. When such a bundle is present, every hook execution MUST be observable via `claude_code.hook_execution_start` and `claude_code.hook_execution_complete` log events on the standard logs pipeline.

A conformant plugin MAY additionally expect its hook executions to be observable as `claude_code.hook` trace spans under the deeper beta gate (`ENABLE_BETA_TRACING_DETAILED=1` + `BETA_TRACING_ENDPOINT`). Plugins MUST NOT require this deeper-beta gate for their primary regression-test path.

### R3 — Transport observability

A conformant plugin's MCP server MUST be observable via the harness's `mcp_server_connection` log event for every transport setup and teardown. Plugins MAY emit additional server-side telemetry to their own observability stack but MUST NOT require that telemetry for the harness-side regression suite to function.

### R4 — Vendor-neutral test harness

A regression suite asserting against a conformant plugin MUST be runnable from `claude -p` (the non-interactive harness) or equivalent SDK invocation, without requiring interactive CLI session allowlisting. This allows the suite to run in CI without organizational gating.

### R5 — Documented matcher map

A conformant plugin SHOULD publish a **matcher map** (see [`matcher-map-template.md`](./matcher-map-template.md)) — a vendor-neutral 3-column document mapping each finding-shape (race condition, state inconsistency, contract violation, etc.) to the hook matcher that addresses it and the OTel signal that observes whether the matcher fired. The matcher map is the artifact that makes the plugin's deterministic-enforcement layer testable, reviewable, and reusable.

## Conformance reporting

A claim of conformance against this spec at version `vN.M.K-draft` requires a **conformance report** that:

1. Cites the spec version explicitly.
2. Names the plugin under test (repo + commit SHA + tag).
3. Documents the test environment (harness version, env-var gate set, OTel collector configuration).
4. Reports per-requirement results: PASS / PARTIAL / FAIL / N/A — with PARTIAL and FAIL annotated with finding evidence.
5. Includes the plugin's matcher map (R5) as an appendix.

The first reference conformance report against this draft is the [`kobiton/automate` case study](./case-studies/kobiton-automate.md), in progress.

## Versioning

- `v0.1.0-draft` — initial scaffold + first case study in progress (this version).
- `v0.1.0-rc` — when the first case study reaches conformance-report-ready state and incorporates feedback.
- `v0.1.0` — when at least one independent implementation (a plugin not authored by this spec's maintainer) ships a conformance report against the spec.
- `v0.2.0+` — minor versions add new normative requirements; major versions break compatibility.

## RFC

Comments, corrections, and counter-proposals welcome via GitHub issues on [`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) with `[mcp-plugin-observability]` in the title.

This spec is in draft. Sharper challenges to the requirement set, the anchoring, the conformance-report shape, and the scope boundaries are explicitly invited.

## License

Apache 2.0 — see [LICENSE](../../../LICENSE) at repo root.
