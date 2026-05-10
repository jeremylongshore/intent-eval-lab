# CLAUDE.md — Intent Eval Lab

Guidance for Claude Code when working in `/home/jeremy/000-projects/intent-eval-platform/intent-eval-lab/`.

## What this is

A research umbrella for vendor-neutral evaluation methodology around AI plugins, agents, MCP servers, and skill-discovery systems. Scoped to **measurement and methodology** — not a product, not a marketplace, not a blog. Outputs flow to other surfaces:

- Validated methodology → blog posts on `startaitools.com`
- Productizable harnesses → contributions to `j-rig-binary-eval` (sister project)
- Public reference content → this repo's `000-docs/` (Apache 2.0)

## Three-repo convergence (Phase A complete 2026-05-10)

This repo is the **methodology + specs umbrella** in the three-repo convergence vision (`intent-eval-lab` + `audit-harness` + `j-rig-binary-eval`). The architectural insight: the three repos compose via a shared schema (the **Evidence Bundle**), not via package consolidation. Convergence happens at the schema layer.

**Master plan (local-only):** `~/.claude/plans/please-take-your-time-glimmering-stardust.md`
**ID mapping artifact:** `~/.claude/plans/please-take-your-time-glimmering-stardust-id-map.md` (29 issues × 4 layers each — beads + GH + Plane + bd-sync link)
**Convergence umbrella epic:** [`#4`](https://github.com/jeremylongshore/intent-eval-lab/issues/4) (`IEL-CONV-1`) — 8 umbrella + 10 work issues filed in this repo, plus 8 in `audit-harness`, plus 3 in `j-rig-binary-eval`

### Phase A landed (this repo)

- **Evidence Bundle spec module** at `specs/evidence-bundle/v0.1.0-draft/` (skeleton — `SPEC.md` section headers only; normative content gates to Phase B per `IEL-3`)
- **Cross-CLI discovery module** stub at `specs/cross-cli-discovery/v0.1.0-draft/` (Phase B per `IEL-5`)
- **OpenTelemetry RFC draft** at `000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` — full RFC text proposing `agent.rollout.gate.*` and `agent.evidence_bundle.*` signal conventions. **Drafted, NOT filed.** Filing is a Phase B deliverable per `IEL-CONV-7`.
- **Partner-consent discipline** enforced (see § Brand-name policy below)

### Phase B/C gate

Phase A is documentation + skeleton ONLY. **No feature code commits to this repo's spec modules until first paying-customer signal** per master plan § Risks. When that signal arrives, next-session entry point: `bd-sync status` across the three repos → re-read mapping artifact → update meta-bead `OPS-nfx` (in home `~/.beads/`) with Phase B kickoff note → begin `IEL-3` SPEC.md normative content.

### Brand-name policy (partner-consent discipline)

**A partner is not named in any public repo content (specs, READMEs, GitHub issues, blog drafts) until they have explicitly consented in writing to being named.** The first reference case study against `mcp-plugin-observability/v0.1.0-draft/` is engagement-private; the brand-named scaffold file was removed from the public repo on 2026-05-10 and the case study now lives only in the engagement's private docs. When the partner consents, the case study can be re-instantiated with their name in `case-studies/`.

This rule applies even to negative-affirmation phrasings ("we don't mention X, Y, Z"). Use generic terms like "an enterprise partner engagement" or "the inaugural case study (engagement-private)" until written consent is on file.

`grep -ri "Kobiton\|Polygon\|Nixtla\|Lit Protocol\|Mudit Gupta" specs/` should return zero hits at all times. Run before commits touching `specs/`.

## Where to start Claude Code sessions

The lab and j-rig-binary-eval are **coordinated repos with different scopes**. Open Claude Code in the right one based on what you're doing:

| You're working on | Open Claude Code in |
|---|---|
| Methodology, research, literature review, sandbox experiments, evidence analysis, blog drafts | **`~/000-projects/intent-eval-platform/intent-eval-lab/`** (this dir) |
| Implementing eval harness code (workspace packages, executor adapters per artifact type, CLI surface, schemas) | **`~/000-projects/intent-eval-platform/j-rig-binary-eval/`** |
| A constituent project's own work (semantic-flux internals, audit-harness changes) | That project's own dir |

The lab session has full context for cross-project synthesis. The JRig session has full context for the harness code itself. They reference each other but stay scoped.

**Rule of thumb**: if your output is a markdown doc, a sandbox dir, or a research artifact → lab session. If your output is TypeScript code that ends up in a workspace package → JRig session.

## Constituent projects (two tiers)

`projects/` contains symlinks (gitignored) to two kinds of constituent project. **The tier-1 vs tier-2 distinction is load-bearing — don't lump them together.**

### Tier 1 — Testing-platform convergence (sibling under `intent-eval-platform/`)

Repos that **compose into one evaluation platform via the Evidence Bundle schema** (per LAB-6 / `IEL-CONV-1`). They share architectural coupling and live as siblings under the same umbrella dir.

| Symlink | Real path | Convergence role |
|---|---|---|
| `projects/audit-harness` | `~/000-projects/intent-eval-platform/audit-harness` (sibling) | Deterministic gates — emits Evidence Bundle gate-result rows |
| `projects/j-rig-binary-eval` | `~/000-projects/intent-eval-platform/j-rig-binary-eval` (sibling) | 7-layer judgment harness — consumes + emits Evidence Bundle rows |

### Tier 2 — Independent lab research projects (outside the umbrella)

Research-stage work the lab oversees **methodologically** but that runs on its own architecturally. Often patent-sensitive. Lives at `~/000-projects/<name>/` (NOT inside `intent-eval-platform/`).

| Symlink | Real path | Why it's outside the umbrella |
|---|---|---|
| `projects/semantic-flux` | `~/000-projects/semantic-flux` | Query-Compiled Semantic Scan (QCSS), patent provisional clock 2026-06-12. No Evidence Bundle dependency. Has its own Plane project (SFX), separate from LAB + JRIG. |
| (additional research projects added by symlink as the lab grows) | | |

### Rules

- **Don't move tier-2 projects into the platform umbrella.** Patent isolation + architectural honesty + Plane parity. The lab oversees them methodologically; they don't share architecture with the testing platform.
- **When working IN a constituent project** (via symlink or direct path), defer to that project's own CLAUDE.md. The lab's CLAUDE.md governs lab-level work only (`000-docs/`, `research/`, `sandboxes/`, `scripts/`, `evidence/`).
- **New constituent project?** Decide its tier first: does it compose via Evidence Bundle (→ tier 1, lives under `intent-eval-platform/`) or is it independent research the lab covers (→ tier 2, lives at `~/000-projects/<name>/`)?

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


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
