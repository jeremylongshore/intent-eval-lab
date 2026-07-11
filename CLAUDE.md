# CLAUDE.md — Intent Eval Lab

Guidance for Claude Code when working in `/home/jeremy/000-projects/intent-eval-platform/intent-eval-lab/`.

## What this is

A research umbrella for vendor-neutral evaluation methodology around AI plugins, agents, MCP servers, and skill-discovery systems. Scoped to **measurement and methodology** — not a product, not a marketplace, not a blog. Outputs flow to other surfaces:

- Validated methodology → blog posts on `startaitools.com`
- Productizable harnesses → contributions to `j-rig-skill-binary-eval` (sister project)
- Public reference content → this repo's `000-docs/` (Apache 2.0)

> **State (updated 2026-07-10):** SAK Class-1 charter RATIFIED (docs 049/081); Skill Refiner PUBLISHED to npm (initial `@intentsolutions/refiner@0.1.0` 2026-06-21; now **`@intentsolutions/refiner`+`refiner-core@0.3.0`** — provider-agnostic `refine score/propose --provider` over free/cheap models — with `@intentsolutions/jrig-cli@0.2.0`, 2026-07-10); the SSoT/spec-compliance machinery (doc 045 + `SAK-INDEX.md` + `scripts/spec-drift-check.sh` / `spec-projection-diff.py` + `.github/workflows/spec-drift-watch.yml`) is the dominant active surface. 000-docs runs through 106+. Any "Skill Refiner" or "Phase B/C gate" block below is a 2026-05-27 snapshot — trust the DRs + `SAK-INDEX.md` + the umbrella CLAUDE.md over them.

## Five-repo convergence (Phase A complete 2026-05-13; intent-rollout-gate added 2026-05-12)

This repo is the **methodology + specs umbrella** in the five-repo convergence vision: the canonical contracts kernel (`intent-eval-core`) + `intent-eval-lab` + `audit-harness` + `j-rig-skill-binary-eval` + `intent-rollout-gate`. The architectural insight: the repos compose via a shared schema (the **Evidence Bundle**), not via package consolidation. Convergence happens at the schema layer. (`intent-eval-dashboard` is the 6th platform repo — the reports hub at `labs.intentsolutions.io` — separate from the 5-repo convergence taxonomy.) See the umbrella `~/000-projects/intent-eval-platform/CLAUDE.md` § "5-repo target" for the full taxonomy.

**Convergence umbrella epic:** [`#4`](https://github.com/jeremylongshore/intent-eval-lab/issues/4) (`IEL-CONV-1`) — 8 umbrella + 10 work issues filed in this repo, plus 8 in `audit-harness`, plus 3 in `j-rig-skill-binary-eval`

### Phase A landed (this repo)

- **Evidence Bundle spec module** at `specs/evidence-bundle/v0.1.0-draft/` — the Phase A skeleton has since been elevated to a **NORMATIVE DRAFT** (`SPEC.md` self-declares `Status: NORMATIVE DRAFT` at Phase B Milestone 1). The canonical `gate-result/v1` JSON Schema now lives in the kernel `@intentsolutions/core`; this module's schema file is a redirect stub.
- **Phase B spec-module stubs** live under `specs/` (e.g. `validator-contract-reliability/`, `forecasting-drift-detection/`, `decentralized-crypto-evaluation/`) — placeholders for Phase B work per `IEL-5`. (The originally-planned `cross-cli-discovery/` module was never created under that name.)
- **OpenTelemetry RFC draft** at `000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` — full RFC text proposing `agent.rollout.gate.*` and `agent.evidence_bundle.*` signal conventions. **Drafted, NOT filed.** Filing is a Phase B deliverable per `IEL-CONV-7`.
- **Partner-consent discipline** enforced (see § Brand-name policy below)

### Phase B/C gate

Phase A is documentation + skeleton ONLY. **Phase B is bandwidth-gated, not customer-signal-gated** — the customer-signal gate was REMOVED per DR-010 § 13.5 (acting-head-of-board override; see `000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md`). When Phase B work is scheduled, next-session entry point: `bd-sync status` across the convergence repos → begin `IEL-3` SPEC.md normative content. (Note: end-to-end platform operation was demonstrated 2026-06-29 per `000-docs/105-AA-AACR-iep-demonstrably-works-end-to-end-2026-06-29.md`; the "documentation + skeleton only" framing predates that.)

### Brand-name policy (partner-consent discipline)

**A partner is not named in any public repo content (specs, READMEs, GitHub issues, blog drafts) until they have explicitly consented in writing to being named.** The first reference case study against `mcp-plugin-observability/v0.1.0-draft/` is engagement-private; the brand-named scaffold file was removed from the public repo on 2026-05-10 and the case study now lives only in the engagement's private docs. When the partner consents, the case study can be re-instantiated with their name in `case-studies/`.

This rule applies even to negative-affirmation phrasings ("we don't mention X, Y, Z"). Use generic terms like "an enterprise partner engagement" or "the inaugural case study (engagement-private)" until written consent is on file.

Run the partner-name grep guard against `specs/`, `000-docs/`, `README.md`, and this `CLAUDE.md` before any commit touching public artifacts. The active pattern is maintained in the PRIVATE umbrella `~/000-projects/CLAUDE.md` and is **not enumerated here** — inlining it would defeat the discipline. The `.github/workflows/partner-name-guard.yml` CI workflow also enforces this gate automatically on every PR and push to main. Expected output: zero hits.

## Where to start Claude Code sessions

The lab and j-rig-skill-binary-eval are **coordinated repos with different scopes**. Open Claude Code in the right one based on what you're doing:

| You're working on                                                                                              | Open Claude Code in                                                   |
| -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Methodology, research, literature review, sandbox experiments, evidence analysis, blog drafts                  | **`~/000-projects/intent-eval-platform/intent-eval-lab/`** (this dir) |
| Implementing eval harness code (workspace packages, executor adapters per artifact type, CLI surface, schemas) | **`~/000-projects/intent-eval-platform/j-rig-binary-eval/`**          |
| A constituent project's own work (semantic-flux internals, audit-harness changes)                              | That project's own dir                                                |

The lab session has full context for cross-project synthesis. The JRig session has full context for the harness code itself. They reference each other but stay scoped.

**Rule of thumb**: if your output is a markdown doc, a sandbox dir, or a research artifact → lab session. If your output is TypeScript code that ends up in a workspace package → JRig session.

## Constituent projects (two tiers)

`projects/` contains symlinks (gitignored) to two kinds of constituent project. **The tier-1 vs tier-2 distinction is load-bearing — don't lump them together.**

### Tier 1 — Testing-platform convergence (sibling under `intent-eval-platform/`)

Repos that **compose into one evaluation platform via the Evidence Bundle schema** (per LAB-6 / `IEL-CONV-1`). They share architectural coupling and live as siblings under the same umbrella dir.

| Symlink                        | Real path                                                                                                                                                              | Convergence role                                                                                                                                                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `projects/audit-harness`       | `~/000-projects/intent-eval-platform/audit-harness` (sibling)                                                                                                          | Deterministic gates — emits Evidence Bundle gate-result rows                                                                                                                                                      |
| `projects/j-rig-binary-eval`   | `~/000-projects/intent-eval-platform/j-rig-binary-eval` (sibling; GH-canonical repo name is `j-rig-skill-binary-eval`, local FS dir name retained for backward-compat) | 7-layer judgment harness — consumes + emits Evidence Bundle rows                                                                                                                                                  |
| `projects/intent-rollout-gate` | `~/000-projects/intent-eval-platform/intent-rollout-gate` (sibling)                                                                                                    | GitHub Action — consumes a bundle + a `tests/TESTING.md` policy → ship/no-ship decision (LIVE at v0.3.0, signed to production Rekor; delegates decision logic to published `@intentsolutions/rollout-gate@2.0.0`) |

### Tier 2 — Independent lab research projects (outside the umbrella)

Research-stage work the lab oversees **methodologically** but that runs on its own architecturally. Often patent-sensitive. Lives at `~/000-projects/<name>/` (NOT inside `intent-eval-platform/`).

| Symlink                                                          | Real path                      | Why it's outside the umbrella                                                                                                                                       |
| ---------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `projects/semantic-flux`                                         | `~/000-projects/semantic-flux` | Query-Compiled Semantic Scan (QCSS), patent provisional clock 2026-06-12. No Evidence Bundle dependency. Has its own Plane project (SFX), separate from LAB + JRIG. |
| (additional research projects added by symlink as the lab grows) |                                |                                                                                                                                                                     |

### Rules

- **Don't move tier-2 projects into the platform umbrella.** Patent isolation + architectural honesty + Plane parity. The lab oversees them methodologically; they don't share architecture with the testing platform.
- **When working IN a constituent project** (via symlink or direct path), defer to that project's own CLAUDE.md. The lab's CLAUDE.md governs lab-level work only (`000-docs/`, `research/`, `sandboxes/`, `scripts/`, `evidence/`).
- **New constituent project?** Decide its tier first: does it compose via Evidence Bundle (→ tier 1, lives under `intent-eval-platform/`) or is it independent research the lab covers (→ tier 2, lives at `~/000-projects/<name>/`)?

## Lab-level conventions

### Doc filing

Numbered + dated + category-coded (the `/doc-filing` standard).

```text
000-docs/000-INDEX.md             ← index of all lab docs
000-docs/001-RR-LAND-...md        ← research/landscape report
000-docs/002-RR-LITS-...md        ← research/literature survey
000-docs/003-PP-PLAN-...md        ← planning document
000-docs/004-AA-AACR-...md        ← after-action report
```

Filing-code crib: `RR` = research/recon, `PP` = plan, `AA` = after-action, `DR` = draft, `RA` = ready-to-publish.

Key normative anchors added since Phase A: doc 045 (SSoT + continuous spec-compliance), `SAK-INDEX.md` (Spec Authority Kernel index), docs 049/081 (ISEDC Class-1 SAK charter ratifications), doc 076 (state-machine single-source + drift gate).

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

## Skill Refiner — plan + audit + ratification (2026-05-27)

Skill Refiner is RATIFIED (DR-028, 2026-05-27) and PUBLISHED to npm (initial `@intentsolutions/refiner-core` + `@intentsolutions/refiner@0.1.0` 2026-06-21, SLSA provenance; now at **`0.3.0`** — provider-agnostic `refine score/propose --provider` over free/cheap OpenAI-compatible models — shipped in `@intentsolutions/jrig-cli@0.2.0`, 2026-07-10). The docs below are the ratification-era record; for current SAK/charter state see docs 044/049/081 + `SAK-INDEX.md`.

**Canonical docs (read in order):**

| Order | Doc                                                                                          | Purpose                                                                                                                                            |
| ----- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | `000-docs/027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md`                | THE PLAN (v5 inline; ~1700 lines). DR-028 Amendments Index block at top is the v5 delta digest.                                                    |
| 2     | `000-docs/028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md` | ISEDC Session 7 Decision Record — 10 ratified decisions (T1-T4 tensions + P0-RATIFY-1..6). Verbatim seat positions + binding minority constraints. |
| 3     | `000-docs/029-DR-BAND-skill-refiner-bandwidth-model-2026-05-27.md`                           | FTE-week budget per phase (8.8 FTE-weeks total ≈ ~3 calendar months bandwidth-gated + external blockers). Critical-path beads. Pre-mortem.         |
| 4     | `000-docs/025-PP-PLAN-skill-refiner-2026-05-26.md`                                           | Companion plan (v3 framing); SUPERSEDED-BY 027.                                                                                                    |
| 5     | `000-docs/audit/2026-05-26-plan-audit/STATUS.md`                                             | Current state: **RATIFIED** as of 2026-05-27                                                                                                       |
| 6     | `000-docs/audit/2026-05-26-plan-audit/synthesis.md`                                          | 7-seat Plan Audit panel synthesis (Hickey/Beck/Karpathy/Huyen/Lamport/Cunningham/Kleppmann); 6 convergent P0s; 4 tensions                          |
| 7     | `000-docs/audit/2026-05-26-plan-audit/findings/*-findings.md`                                | 7 individual Plan Audit seat reports + 6 thinker tension arbitrations                                                                              |
| 8     | `000-docs/audit/2026-05-26-plan-audit/remediation-map.md`                                    | Finding → plan-section / bead-ID action map                                                                                                        |
| 9     | `000-docs/audit/2026-05-26-plan-audit/internal-review-2026-05-27.md`                         | Pre-flight 4-reviewer pass (article-consistency + architect + code + fact-checker) that produced v4.1 P0 patches                                   |

**Headline decisions (DR-028 ratified):**

- **T1 SkillVersion entity:** DISCRIMINATOR — separate entity from SkillSnapshot, `version_kind` + `parent_version_id` + `source_snapshot_hash` (reference, NOT FK) (6 vs 5 vs 2 vs 2)
- **T2 Phase D:** ANTI-GOAL — removed from plan; Blueprint A § 3.X amendment carries the explicit non-commitment (12 of 14 voices)
- **T3 Process discipline:** COLLAPSE — bd is canonical writer; GH/Plane are projections; `bd-sync` becomes generator (20/20 consensus)
- **T4 Brand:** KEEP Skill Refiner as named product (CMO/CFO/VP DevRel business-axis trio overrode thinker-majority on brand-instability + dev-mental-model grounds); AC-7 + new AC-13 RefinerStrategy interface are the engineering hedge

**Enforcement (machine, not honor):** `intent-eval-lab/scripts/bd-claim-precheck.sh` reads `000-docs/audit/2026-05-26-plan-audit/STATUS.md`; blocks `bd claim` against refiner-labeled beads unless STATUS=RATIFIED (or RATIFIED-WITH-DELTAS for explicitly-authorized work). Tested + working.

**Tri-link verifier:** `intent-eval-lab/scripts/validate-trilink.sh` enforces bead↔doc↔GH-issue cross-refs for refiner-labeled artifacts. Runs in CI per repo (planned). Currently PASS.

**Bead workspace:** ALL Skill Refiner beads (50 open as of 2026-05-27) live in the umbrella `~/000-projects/.beads/` (NOT per-repo workspaces). Per-repo distinguishability via mandatory `repo:<short>` labels (`repo:iel`, `repo:iec`, `repo:iaj`, `repo:iah`, `repo:iar`, `repo:iep`). Query example: `bd list --label repo:iec --label refiner --status open`.

**Open external blockers (sole-prop-owned):**

- `bd_000-projects-uprg` — Evidence Bundle compat policy → blocks Phase C SkillVersion in `@intentsolutions/core@0.3.0`
- `bd_000-projects-9pi3` — OTel semconv pin → blocks kernel v0.3.0 release
- Both amended with DR-028 dependency notes pointing to 029-DR-BAND

**Plan Audit pattern (reusable):** the 4-reviewer pre-flight → 7-seat thinker-canon panel → 6-thinker tension arbitration → 7-seat ISEDC ratification sequence is reusable for any future high-stakes plan (any plan with multiple convergent P0s + cross-seat tensions). See `~/.claude/skills/exec-decision-council/sessions/2026-05-27-skill-refiner-plan-ratification/` for the canonical run.

## Internal operational notes

Detailed operational state (active engagements, sock-puppet observations, partner-specific notes, patent-sensitive cross-refs) lives in `.private/CLAUDE-private.md` — gitignored, local-only. Read that file in addition to this one when working in this dir on operational tasks.

## AI code review (Greptile + Gemini)

Two AI reviewers run on PRs here, **both advisory** — neither is a branch-protection
required check. The deterministic merge gate is this repo's own CI (the partner-name guard + schema-drift gate + doc gates) plus CodeQL.

- **Gemini Code Assist** (`.gemini/config.yaml` + `.gemini/styleguide.md`) is the
  **active** reviewer. Re-instated 2026-06-24 as the fallback after the Greptile
  review quota was exhausted. Workhorse for design / logic / correctness /
  cross-artifact consistency; CodeQL owns security.
- **Greptile** (`.greptile/config.json` + `rules.md` + `files.json`) is configured to
  the platform-unified schema (`strictness: 3`, `commentTypes: ["logic","syntax"]`,
  `statusCheck: false`, a universal `no-gate-weakening` rule, plus this repo's scoped
  invariant rules). It stays in place and resumes when the Greptile quota resets.

Read either review when present; the required gate is CI. Re-installing/uninstalling
the GitHub Apps is an admin (UI) action — the in-repo config here does not install them.

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
