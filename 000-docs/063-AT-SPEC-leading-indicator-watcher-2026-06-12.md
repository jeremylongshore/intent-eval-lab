# 063 — Anthropic leading-indicator watcher (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 033-PP-PLAN § 14.11 (the 12 indicators + matrix + polling mechanism), 052-AT-SPEC (the typed fetch-failure posture this reuses) · **Bead:** 06qk

The normative reference for the leading-indicator watcher — the **bitter-lesson trigger** for the Spec Authority Kernel (SAK). It answers a strategic question distinct from the spec-drift watcher's "did an upstream contract page change?": **has Anthropic shipped something that signals the SAK should stop investing and cut over to upstream?** Implementation: `scripts/leading-indicator-watch.py`, driven by `specs/leading-indicators.v1.json`; daily cron in `.github/workflows/leading-indicator-watch.yml`; self-test wired into `ci.yml`'s `Validate specs and docs` job.

## Why (the bitter-lesson rationale)

Rich Sutton's bitter lesson: general methods that scale with compute eventually beat hand-engineered structure. The SAK is hand-engineered structure (curated schemas + an IS-marketplace policy floor). If a frontier model can derive a schema-validator's verdicts from prose + examples — or if Anthropic ships first-party machine-readable spec authority — then continuing to invest in the SAK is paddling against the current. This watcher makes that moment **observable** rather than something we notice too late. Per plan 033 § 14.14, a STOP verdict routes to the port-not-delete playbook so the investment (governance owners, consistency model, snapshot rules) transfers upstream rather than evaporating.

## The 12 indicators (§ 14.11.1)

| #   | Indicator                                                                    | Source kind     | Severity                               |
| --- | ---------------------------------------------------------------------------- | --------------- | -------------------------------------- |
| 1   | Anthropic publishes public roadmap including machine-readable spec           | prose           | High                                   |
| 2   | `claude` CLI begins ingesting `.claude/schema/` directory                    | rss (changelog) | High                                   |
| 3   | `claude doctor` adds plugin-format validation                                | rss (changelog) | High                                   |
| 4   | agentskills.io v2 RFC published                                              | rss (spec)      | High                                   |
| 5   | Anthropic publishes machine-readable agentskills.io v2 schemas               | github-release  | **CRITICAL**                           |
| 6   | Anthropic ships skill-author-onboarding doc citing field validation          | prose           | Medium                                 |
| 7   | `claude-codemod` or equivalent field-migration tool ships                    | github-release  | Medium                                 |
| 8   | Anthropic ships skill-shell-validation                                       | rss (changelog) | Medium                                 |
| 9   | Anthropic ships skill-security-audit                                         | rss (changelog) | Medium                                 |
| 10  | agentskills.io spec adds vendor-namespacing section                          | rss (spec)      | Low                                    |
| 11  | Vercel skills.sh adopts kernel-schema-compatible format                      | github-release  | Low                                    |
| 12  | Frontier model demonstrates schema-validator equivalence from prose+examples | github-release  | **CRITICAL** — bitter-lesson triggered |

## Disposition matrix (§ 14.11.2)

The watcher counts FIRING indicators by severity → one verdict:

| Indicators firing    | Verdict    | Action                                                                      |
| -------------------- | ---------- | --------------------------------------------------------------------------- |
| 0-2 Low-severity     | `CONTINUE` | Continue per plan                                                           |
| 1 Medium             | `NOTE`     | Note in next AAR; no plan change                                            |
| 2-3 Medium OR 1 High | `RETRO`    | ISEDC Class-2 retrospective; consider pausing Phase >= 3                    |
| 1 CRITICAL           | `PAUSE`    | PAUSE all SAK phases; ISEDC Class-1 re-charter to evaluate upstream cutover |
| 2 CRITICAL           | `STOP`     | STOP SAK; archive as historical contribution; cut over to upstream          |

## Deterministic detection + typed-fetch-failure posture (reused from 052-AT-SPEC)

The watcher mirrors the spec-drift machinery's discipline exactly: **only a clean fetch (FETCH_OK) feeds disposition.** A fetch failure is classified `UNREACHABLE | MOVED | RATELIMITED | SHAPE_CHANGED`, alerted via ntfy (`prod-health`), and recorded — but is **NEVER a hit**. A bad fetch cannot masquerade as an Anthropic signal, and never opens an issue. Structured sources (GitHub releases atom, RSS entry ids, JSON/TS schema presence) parse to a stable token and diff against the last-known snapshot.

## Flake budget (§ 14.11.3 — <5% false positives)

- **Structured sources** (10 of 12) parse exactly and escalate IMMEDIATELY on a parsed change — no flake surface.
- **The 2 prose sources** (#1 Anthropic blog, #6 skills overview) are the only flake risk. A prose change is held PENDING for a **7-day disposition window** before it counts as an escalating hit. While PENDING the watcher deliberately holds the OLD baseline so the change keeps being detected daily; only after 7 days of persistence does it fire. A prose page that reverts inside the window clears PENDING with no hit. This keeps the prose false-positive rate under the 5% budget.

## Side effects (scheduled run only)

On a new escalating hit: (1) the workflow fails (red X), (2) an ntfy push fires, (3) a deduped `[leading-indicator]` GH issue opens carrying the disposition verdict. A PR/push event runs the offline self-test only — it never hits the network and never reds on a genuine upstream signal it didn't cause.

## CI

`ci.yml` `Validate specs and docs` runs `leading-indicator-watch.py --self-test` (offline, deterministic: new-hit, no-change, fetch-failure, prose-window, and full-matrix fixtures). The registry ↔ script ↔ workflow contract is hash-pinned via `.harness-hash` (the `.github/workflows/*.yml` pattern); a silent edit to the workflow blocks the PR via `harness-hash --verify`.
