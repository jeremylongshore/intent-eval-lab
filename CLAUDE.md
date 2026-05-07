# CLAUDE.md — Intent Eval Lab

Guidance for Claude Code when working in `/home/jeremy/000-projects/intent-eval-lab/`.

## What this is

A research umbrella for vendor-neutral evaluation methodology around AI plugins, agents, MCP servers, and skill-discovery systems. Scoped to **measurement and methodology** — not a product, not a marketplace, not a blog. Outputs flow to other surfaces:

- Validated methodology → blog posts on `startaitools.com`
- Productizable harnesses → contributions to `j-rig-binary-eval` (sister project)
- Public reference content → this repo's `000-docs/` (Apache 2.0)

## Where to start Claude Code sessions

The lab and j-rig-binary-eval are **coordinated repos with different scopes**. Open Claude Code in the right one based on what you're doing:

| You're working on | Open Claude Code in |
|---|---|
| Methodology, research, literature review, sandbox experiments, evidence analysis, blog drafts | **`~/000-projects/intent-eval-lab/`** (this dir) |
| Implementing eval harness code (workspace packages, executor adapters per artifact type, CLI surface, schemas) | **`~/000-projects/j-rig-binary-eval/`** |
| A constituent project's own work (semantic-flux internals, audit-harness changes) | That project's own dir |

The lab session has full context for cross-project synthesis. The JRig session has full context for the harness code itself. They reference each other but stay scoped.

**Rule of thumb**: if your output is a markdown doc, a sandbox dir, or a research artifact → lab session. If your output is TypeScript code that ends up in a workspace package → JRig session.

## Constituent projects

`projects/` contains symlinks (gitignored) to constituent project repos at `~/000-projects/<name>/`. Don't move or clone them. Each keeps its own git, README, and CLAUDE.md.

| Symlink | Real path | Public? |
|---|---|---|
| `projects/j-rig-binary-eval` | `~/000-projects/j-rig-binary-eval` | yes — github.com/jeremylongshore/j-rig-binary-eval |
| `projects/audit-harness` | `~/000-projects/audit-harness` | yes — github.com/jeremylongshore/audit-harness |
| (additional projects added by symlink as the lab grows) | | |

When working IN a constituent project (via symlink or direct path), defer to that project's own CLAUDE.md. The lab's CLAUDE.md governs lab-level work only (`000-docs/`, `research/`, `sandboxes/`, `scripts/`, `evidence/`).

## Lab-level conventions

### Doc filing

Numbered + dated + category-coded (the `/doc-filing` standard).

```
000-docs/000-INDEX.md             ← index of all lab docs
000-docs/001-RR-LAND-...md        ← research/landscape report
000-docs/002-RR-LITS-...md        ← research/literature survey
000-docs/003-PP-PLAN-...md        ← planning document
000-docs/004-AA-AACR-...md        ← after-action report
```

Filing-code crib: `RR` = research/recon, `PP` = plan, `AA` = after-action, `DR` = draft, `RA` = ready-to-publish.

### Sandboxes

Per-experiment subdirs under `sandboxes/`. Naming: `YYYY-MM-DD-<short-experiment-id>/`. Each contains its own `REPORT.md`, infrastructure config (`docker-compose.yml` if applicable), `prompts/`, `fixtures/`, and an `evidence/` cross-link to lab-level `evidence/<experiment-id>/`.

Never share state across experiments. Tear down infrastructure after each run unless explicitly continuing. Snapshot evidence to `evidence/<experiment-id>/` with cross-link in REPORT.md.

### Evidence

`evidence/` captures raw telemetry, OTEL traces, screenshots, JSON bundles. Mostly gitignored — ephemeral artifacts. Reference evidence files from `000-docs/<doc>.md` so the path is permanent in the doc record even if the file isn't tracked.

### Scripts

`scripts/` holds REUSABLE test-harness code, OTEL probes, prompt-suite runners, regression-report generators. One-off scripts go in their experiment's sandbox, not here.

## Operational rules

1. **Don't move constituent projects.** They live at `~/000-projects/<name>/`. Symlinks are filesystem view only. Moving would break their git remotes, references, and any in-flight work.
2. **Respect each constituent's CLAUDE.md.** When working inside a sub-project, that project's rules apply.
3. **Don't expose patent-sensitive material.** Private partner-engagement details and any patent-pending work live in `.private/` (gitignored). The public repo is for vendor-neutral, partner-anonymous methodology only.
4. **No premature productization.** Publishable content (blogs, productized SKU pages on intentsolutions.io) flows OUT of validated experiments — not from speculation. If a methodology hasn't been demonstrated empirically in a sandbox here, don't blog about it.
5. **First-mover SEO is real but secondary to rigor.** Don't ship sloppy content for first-mover advantage. Time the publication to land when the methodology is defensible against expert review.

## What this lab is NOT

- Not a plugin marketplace (separate concern)
- Not a consulting practice page (separate site)
- Not a blog (separate site)
- Not a single product (it's a research umbrella; products spin out FROM it)

Keep this scoped. The lab's value is rigor + cross-project synthesis, not building yet another application.

## Internal operational notes

Detailed operational state (active engagements, sock-puppet observations, partner-specific notes, patent-sensitive cross-refs) lives in `.private/CLAUDE-private.md` — gitignored, local-only. Read that file in addition to this one when working in this dir on operational tasks.
