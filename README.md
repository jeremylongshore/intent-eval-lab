# Intent Eval Lab

A research umbrella for measuring AI plugin, agent, and MCP server quality across CLI runtimes — Claude Code, Gemini CLI, GitHub Copilot CLI, and OpenAI Codex CLI.

The agentic-CLI ecosystem is converging on a small set of cross-tool conventions (`AGENTS.md`, MCP, `SKILL.md`) but the empirical question — *does my plugin actually get discovered and invoked correctly when the agent decides on its own?* — has no vendor-neutral answer. The vendors won't publish opinionated cross-CLI invocation-measurement frameworks because they're competing across the stack. That niche is structurally available to a third party.

This repo is the working surface for that work.

## What's here

```
intent-eval-lab/
├── 000-docs/        ← numbered docs (research summaries, methodology, plans, AAR)
├── specs/           ← normative methodology output — versioned, testable specs
│                       per class of inference system, with case studies
├── research/        ← literature surveys, paper notes, competitive landscape
├── sandboxes/       ← per-experiment dirs (one dated subdir per run)
├── evidence/        ← captured telemetry, OTEL traces, JSON evidence (mostly gitignored)
├── scripts/         ← reusable test harness, OTEL probes, prompt-suite runners
└── projects/        ← symlinks to constituent project repos (gitignored — see below)
```

`specs/` is the **normative output** of the lab — currently shipping module 1 ([`mcp-plugin-observability/`](./specs/mcp-plugin-observability/)) at `v0.1.0-draft`, with placeholder modules for `validator-contract-reliability/`, `forecasting-drift-detection/`, and `decentralized-crypto-evaluation/` reserving the structural slots for future engagements. See [`specs/README.md`](./specs/README.md) for the module index and authoring conventions.

`projects/` is filesystem-only — the constituent projects keep their own GitHub remotes. The lab is a research umbrella over them, not a monorepo.

## Topics in scope

- Cross-CLI plugin invocation rate measurement (Claude Code / Gemini CLI / Copilot CLI / Codex CLI)
- Skill auto-discovery vs explicit invocation — when does each pattern win
- Eager-vs-lazy skill loading tradeoffs (eager via `contextFileName` arrays vs lazy via auto-discovery)
- OpenTelemetry-instrumented agent evaluation — using `claude_code.skill_activated` and similar primitives
- Plugin metadata quality and its effect on agent decision rates
- MCP server contract conformance and tool-allowlist tradeoffs
- Cross-tool plugin pattern (`AGENTS.md` + `SKILL.md` + `mcpServers`) at scale

## Adjacent projects

| Project | Role |
|---|---|
| [`jeremylongshore/j-rig-skill-binary-eval`](https://github.com/jeremylongshore/j-rig-skill-binary-eval) | 7-layer binary-criteria evaluation harness for SKILL.md artifacts. Natural extension target — the layers are artifact-type-polymorphic; specializing executor + judgment for plugin/agent/MCP is the core build axis. |
| [`jeremylongshore/audit-harness`](https://github.com/jeremylongshore/audit-harness) | `@intentsolutions/audit-harness` — source-code test-policy containment. Composes with the lab's L4-L7 sandbox work. JRig vendors it via a copied `.audit-harness/` directory for self-validation in its own CI (not an npm dep). The three-repo convergence integrates these at the shared Evidence Bundle schema layer rather than via package coupling — see [`000-docs/003-PP-PLAN-phase-b-scope-refinement.md`](./000-docs/003-PP-PLAN-phase-b-scope-refinement.md). |

## Working pattern

1. **Research first.** File a numbered doc in `000-docs/` from a literature survey or competitive scan before scaffolding anything. Methodology decisions get a permanent canonical filename.
2. **One experiment per sandbox.** Every experiment gets its own dated subdir under `sandboxes/`, isolated infrastructure, isolated state. Never share state across experiments.
3. **Evidence as JSON + screenshots.** Captures go to `evidence/<experiment-id>/` with cross-link in the experiment's `REPORT.md`.
4. **Reusable code in `scripts/`.** One-off scripts stay in their experiment's sandbox; only promote to `scripts/` when used twice.

## Status

Early-stage. Scaffolding + initial research underway. Public so the methodology can be reviewed and the work can be discoverable. **No published harness yet** — when output is ready it will land here as either a tagged release or as a PR to `j-rig-skill-binary-eval`.

## License

Apache 2.0 — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution model and conventions. The repo accepts PRs but is currently maintained by a single author; expect slower review cycles than a multi-maintainer project.

## Author

Jeremy Longshore — [intentsolutions.io](https://intentsolutions.io) · [startaitools.com](https://startaitools.com)
