# Intentional Mapping Template — vendor-neutral 3-column form

The Intentional Mapping is the highest-leverage artifact in this spec. It maps each **finding-shape** (a class of plugin failure mode) to the **hook matcher** that addresses it and the **OTel signal** that observes whether the matcher fired.

The map is **vendor-neutral**. The first column describes the failure mode in generic terms; the second column gives the hook matcher pattern; the third column names the OTel signals to assert against. Vendor-specific instantiations live in case studies.

## Template

| # | Finding-shape (vendor-neutral) | Hook matcher pattern | OTel signal to assert against |
|---|---|---|---|
| MM-1 | Asynchronous tool returns success but a downstream tool sees stale state (race condition between async write and read-after-write) | `PostToolUse` on the upstream tool, with reconciliation / retry-with-backoff in the hook handler | `claude_code.hook_execution_complete` log event correlated with the upstream `tool_decision` event; `claude_code.tool_result` event on the downstream tool reflecting reconciled state |
| MM-2 | Tool's read-side response shape drifts across consecutive calls (e.g., list-shape vs detail-shape inconsistency) | `PostToolUse` on the read-side tools, with shape-normalization in the hook handler | `claude_code.tool_result` events for both list and detail tools; assertion on shape parity via `tool_input_size_bytes` and (optionally with `OTEL_LOG_TOOL_CONTENT=1`) content shape |
| MM-3 | Operation requires a cooldown / debouncing window before the next equivalent operation can succeed | `PreToolUse` on the affected tool, with cooldown-enforcement (block + retry-after) in the hook handler | `claude_code.hook_execution_complete` log event with handler-emitted `decision: block` semantics; `claude_code.tool_decision` showing the retry attempt |
| MM-4 | Operation requires verification of side-effect completion before downstream tools can rely on it | `PostToolUse` on the operation, with poll-until-verified in the hook handler (potentially `async` + `asyncRewake`) | `claude_code.hook_execution_start` followed by `claude_code.hook_execution_complete` with verified side-effect; downstream `tool_decision` events parented under the same trace |
| MM-5 | Tool inputs need to carry mandatory context (caller identity, intent string, policy tag) that the model isn't reliably providing | `PreToolUse` on the tool, with input-augmentation in the hook handler — set `hookSpecificOutput.updatedToolInput` | `claude_code.hook_execution_complete` log event; `claude_code.tool_decision` with the augmented inputs visible (under `OTEL_LOG_TOOL_DETAILS=1`) |
| MM-6 | Server-side endpoint requires strict-mode protocol (W3C, RFC) compliance that the model's default tool input doesn't enforce | `PreToolUse` on the affected tool, with strict-mode payload reformat in the hook handler | `claude_code.hook_execution_complete` log event; `claude_code.tool_result` showing the server accepted (rather than rejected) the call |

## Authoring guide

When authoring a Intentional Mapping for a specific plugin:

1. **Start from the finding catalog.** Walk every audit finding (or every known reliability hazard) in the plugin and check which finding-shape pattern in the template above it matches. Most plugin findings collapse to one of MM-1 through MM-6; novel patterns get added rows.
2. **Keep the first column generic.** "Confirmation API returns 200 but device-status API still shows pending for 8 seconds" is too specific. The generic shape is "asynchronous write returns success but read-after-write sees stale state" (MM-1). The plugin-specific instance goes in the case study.
3. **Cite the matcher syntax verbatim.** The Claude Code hook matcher format is `mcp__<server-name>__<tool-name>` (or `mcp__<server-name>__.*` for all-tools-on-a-server). The trailing `.*` is significant — without it the matcher is an exact-string match and matches nothing. This footgun is the #1 reason hook bundles silently fail.
4. **Name the OTel signal precisely.** Distinguish log events (no allowlist gate, `OTEL_LOGS_EXPORTER`) from trace spans (`CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`) from deeper-beta hook spans (`ENABLE_BETA_TRACING_DETAILED=1` + `BETA_TRACING_ENDPOINT`). Conflating these causes regression suites to silently fail to observe what they think they're observing.
5. **Test it.** Every Intentional Mapping row implies an assertion. Before declaring a row "covers" a finding, run `claude -p` against a representative prompt that exercises the finding, capture the OTel stream, and confirm the asserted signal actually fires (and the finding is actually addressed). Untested rows are aspirational, not normative.

## What this is not

The Intentional Mapping is **not** a list of bugs. It's a list of *patterns the plugin is hardened against* via its hook bundle, with the *observability that proves the hardening fired*. Findings get fixed; Intentional Mappings endure across versions.

The Intentional Mapping is **not** a substitute for the MCP server's own internal observability. Server-side metrics belong in the server's own telemetry stack. The Intentional Mapping covers what's observable from the harness side.

The Intentional Mapping is **not** a regression test suite by itself. The test suite is in [`conformance-test-suite/`](./conformance-test-suite/) and uses the Intentional Mapping as input.
