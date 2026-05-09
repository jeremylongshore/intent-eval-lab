# Case Study: `kobiton/automate` (in progress)

> **Status: case study in progress.** This file scaffolds the first reference conformance report against the [MCP Plugin Observability Spec v0.1.0-draft](../SPEC.md). Source-of-truth for the underlying audit findings lives in the engagement's private docs (`kobiton/000-docs/`); this file holds only the spec-aligned summary suitable for public reference once the case study is sign-off-ready and the plugin maintainer (Kobiton) has consented to being named the inaugural case study.

## Plugin under test

- Repo: [`kobiton/automate`](https://github.com/kobiton/automate) (canonical upstream)
- Class: MCP plugin for Claude Code (cross-CLI ports for Copilot CLI and Gemini CLI in flight via PRs #10 and #28)
- MCP server: `api.kobiton.com/mcp` (transport: HTTPS)
- Tool surface: 13 tools under the `mcp__plugin_automate_kobiton__*` namespace (device reservation, app upload, session management, artifact retrieval, credential management)
- Snapshot tags: `r1-2026-04-28`, `r2-2026-05-04` (on fork [`jeremylongshore/automate`](https://github.com/jeremylongshore/automate))

## Matcher map (Kobiton-specific instantiation)

The general matcher-map template lives at [`../matcher-map-template.md`](../matcher-map-template.md). The Kobiton instantiation will be filled in here as R3 audit research completes (target 2026-05-25). Structure:

| # | Finding-shape | Generic matcher | Kobiton-specific finding | Hook matcher (`hooks/hooks.json` form) | OTel assertion |
|---|---|---|---|---|---|
| KOB-MM-1 | Async write → stale read-after-write | MM-1 | F25 (confirmAppUpload async race) | (TBD: PostToolUse on `mcp__plugin_automate_kobiton__confirmAppUpload`) | (TBD) |
| KOB-MM-2 | Read-side shape drift | MM-2 | F12 + F13 (listApps ↔ getApp drift) | (TBD: PostToolUse on listApps + getApp) | (TBD) |
| KOB-MM-3 | Cooldown / debounce | MM-3 | F33 (terminateSession cooldown) | (TBD: PreToolUse on `mcp__plugin_automate_kobiton__terminateSession`) | (TBD) |
| KOB-MM-4 | Side-effect completion verification | MM-4 | F18 (per-command session data) | (TBD: PostToolUse on session-creating tools) | (TBD) |
| KOB-MM-5 | Mandatory context augmentation | MM-5 | userIntent enforcement (engagement-internal) | (TBD: PreToolUse on all `mcp__plugin_automate_kobiton__.*` tools) | (TBD) |
| KOB-MM-6 | Strict-mode protocol compliance | MM-6 | F32 (W3C-strict /se/log) | (TBD: PreToolUse on `mcp__plugin_automate_kobiton__getSessionArtifacts`) | (TBD) |

The (TBD) cells get filled in during R3 § 5 prototype work and the post-M3 measurement work tied to the engagement's internal beads.

## Conformance report (skeleton — to be completed)

Per [SPEC.md § Conformance reporting](../SPEC.md#conformance-reporting):

- **Spec version:** `v0.1.0-draft` (this draft)
- **Plugin under test:** `kobiton/automate` @ commit `<TBD>` (R3 close snapshot)
- **Test environment:**
  - Harness: Claude Code v2.1.128+ (May 4 2026 telemetry surface, see [Claude Code GitHub changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
  - OTel gates: `CLAUDE_CODE_ENABLE_TELEMETRY=1`, `OTEL_LOGS_EXPORTER=otlp` (R1, R2, R3 results); `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` + `OTEL_TRACES_EXPORTER=otlp` (additional trace-span results); `ENABLE_BETA_TRACING_DETAILED=1` + `BETA_TRACING_ENDPOINT` only as part of the deeper-beta optional path
  - Collector: (TBD — to be standardized post-M3 under the kobiton-5cj.6 work)
- **Per-requirement results:**
  - **R1 (Tool-call observability):** TBD
  - **R2 (Hook-firing observability):** TBD — gates on whether R3 § 5 hooks bundle ships with the deliverable
  - **R3 (Transport observability):** TBD
  - **R4 (Vendor-neutral test harness):** TBD
  - **R5 (Documented matcher map):** TBD — gates on this case study completing
- **Matcher map (R5 appendix):** above table, when filled in

## Source-of-truth pointers

The underlying audit findings (F1-F35, with F36-F43 candidate findings still in research) are documented in the engagement's private repo at `kobiton/000-docs/`:

- R1 deliverable: `003-AA-AACR-r1-review-deliverable-report.md`
- R2 deliverable: `021-AA-AACR-r2-mid-cycle-deliverable-report.md`
- R3 deliverable: (in progress, target 2026-05-25)
- F-finding catalog: spread across `013-RR-EXPS-...` through `017-RR-EXPS-...`

Public references where the underlying finding is described in non-confidential terms:

- Fork issues `jeremylongshore/automate#20-#25` (R2 bundle issues, labeled `audit:R2`)
- Fork issues `jeremylongshore/automate#1-9, #12` (R1 mirrors of upstream findings; deferred cleanup)

## Next steps

1. R3 audit research (May 11-25) populates the (TBD) cells in the matcher map.
2. R3 § 5 prototype hooks bundle (if it ships) provides the hook-matcher payloads for KOB-MM-1 through KOB-MM-6.
3. Post-M3 (June+) measurement work under engagement bead `kobiton-5cj.6` — local OTel collector standup, representative prompt-set design, before/after capture against the bundle — populates the OTel-assertion cells.
4. When all cells are populated AND conformance-report results are validated against the v0.1.0-draft requirements, this case study is promotion-eligible (with Kobiton's permission) as the public reference implementation against the spec.
