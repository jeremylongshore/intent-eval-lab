# Plan — CI/CD + j-rig cross-repo remediation (intent-eval-lab ↔ claude-code-plugins-plus)

- **Code**: PP-PLAN
- **Date**: 2026-07-01
- **Author**: Jeremy Longshore (intentsolutions.io)
- **Status**: DRAFT — Track D (beads + changelog) and Track C proceed on merge; Track A (npm publish + production pin bump) and Track B (cc-plugins PRs) are approval-gated (outward-facing).
- **Related**: AAR [`105-AA-AACR`](./105-AA-AACR-iep-demonstrably-works-end-to-end-2026-06-29.md); cc-plugins docs `693-AA-AACR` (j-rig bug record), `691-AT-AUDT` (sync-external audit), `6768`/`6769` (releases).

---

## 1. Context — the core finding

This session hardened intent-eval-lab CI and fixed real j-rig bugs, but they are **stranded in `main`, unpublished**. j-rig `main` carries five merged PRs the published CLI does not:

| PR       | Fix                                                                                                          |
| -------- | ------------------------------------------------------------------------------------------------------------ |
| #172     | `eval --emit-bundle` — real `gate-result/v1` in-toto Statement                                               |
| **#173** | **reasoning-model `max_tokens`** (execution 8192, judge/trigger 2048) — the false-BLOCK / false-"unsure" fix |
| #174     | `scaffold-spec` — baseline eval-spec generator                                                               |
| **#175** | **judge verdict recovery** from truncated / fenced JSON (`extractVerdict` regex fallback)                    |

The published CLI is still **`@intentsolutions/jrig-cli@0.1.1`** (cut by #163, before all of the above). **`claude-code-plugins-plus-skills` pins `0.1.1` exactly** (root `package.json` line 51), so its skill evals still hit the judge-truncation + reasoning-model bugs that inflate false NO-SHIP — exactly what the Xquik-dev dogfood surfaced in cc-plugins doc `693-AA-AACR`. **The work done here translates there via one release + one pin bump.** j-rig is NOT a CI gate in cc-plugins; it is a build-time enrichment step (`marketplace/scripts/enrich-jrig-data.mjs`) + a manual maintainer `j-rig eval` command, so the blast radius is the verification badges and manual evals, not the PR gate.

## 2. Track A — j-rig release → propagate (the core fix)

Approval-gated: an npm publish and a production-marketplace pin bump.

- **A1 — cut `jrig-cli@0.1.2`.** Bump `packages/cli/package.json` `0.1.1 → 0.1.2` + a CHANGELOG entry, open a PR, merge, then tag `jrig-cli-v0.1.2` from main HEAD so `publish-jrig-cli.yml` publishes #172–#175. Verify: `npm view @intentsolutions/jrig-cli version` reports `0.1.2` with sigstore provenance; `cli-test.yml` green.
- **A2 — bump the cc-plugins pin `0.1.1 → 0.1.2`** (a `#925`-style PR on `claude-code-plugins-plus-skills`). This lands the judge-parity (#173) + verdict-recovery (#175) fixes in its evals. Verify: `validate-plugins` green; a re-run of `j-rig eval` on the Xquik skills no longer false-blocks on off-topic control prompts / truncated verdicts.
- **A3 — populate `forge_proofs` + harden the silent-failure mode.** Run `j-rig eval` (new CLI) on one plugin to write the first `tier3-jrig` row (today `jrig-data.json` is `{}` → every "JRig-Verified" badge renders "pending"). Separately, make `enrich-jrig-data.mjs` fail loudly (or emit a CI warning) when the DB/table is missing — currently a failed enrich degrades to `{}` and every badge silently disappears.

## 3. Track B — claude-code-plugins-plus CI hardening

From the repo's own audit docs; approval-gated per PR.

- **B1 — revert the `#604` mitigation.** `validate-plugins.yml:564` `node packages/cli/dist/index.js validate --strict || true` must return to `|| exit 1` once the frontmatter campaign clears its last error (171 remaining; 177 agents missing `capabilities`). Track the campaign; add a deadline gate via the existing `check-ci-deadlines.py` forcing function so it cannot rot silently.
- **B2 — the 8 `sync-external` follow-ups** (`691-AT-AUDT`). Most urgent: the markdownlint + ruff synced-dir exclusion drift (2 blockers — needs `scripts/sync-lint-ignores.mjs` with a `--check` CI drift gate; blocks un-vendoring `beads-dolt`) and `synced-gitignored-files-dropped` (high — `git add -A` silently drops files like a synced `.npmrc`). Remainder: orphan-prune on upstream removal, mode-only-change correction, partial-sync-shipped-as-clean, `matchesPattern` extglob no-op.
- **B3 — npm-audit discipline.** `validate-plugins.yml:284` `npm audit --production || true` is non-blocking, and `npm audit` was skipped entirely in the v4.31.0 release. Decide a policy (blocking on high/critical, or a tracked report-only with a deadline).

## 4. Track C — intent-eval-lab / j-rig follow-ups (this session)

Proceeds on approval of this plan; not outward-facing.

- **C1 — residual empty-output boundary** (`bd_000-projects-h08j.4`). Add in-eval instrumentation (log `result.text` / `finishReason` per test case) to characterize tool/script-dependent skills that a single-turn completion eval cannot fully grade.
- **C2 — `analyze.py` coverage.** Either make the research suite CI-hermetic (stub the external validator + model providers so CI measures the real ~66% instead of the external-dep-limited 42%) or formally accept the pytest-coverage gate as advisory and document why (it needs a validator from another repo + real model keys, absent in CI). The tests themselves all pass.
- **C3 — original-plan Phases 3/4/5.** Phase 3 (batch-grade the ~10-skill shortlist — gated on C1's boundary call), Phase 4 (publish real grades to `labs.intentsolutions.io`), Phase 5 (per-repo verification hardening + the walkthrough doc).

## 5. Track D — beads + changelog (immediate)

- **D1 — beads.** One umbrella epic + children for every A/B/C item, three-layer-mirrored (bd ↔ GitHub issue ↔ Plane) where a code deliverable applies. Cross-repo items (A2, B1–B3) get `claude-code-plugins-plus-skills` GitHub issues.
- **D2 — changelog.** Update the intent-eval-lab `CHANGELOG` (and/or a changelog doc) with this session's CI-hardening arc + the pending j-rig `0.1.2` release.

## 6. Sequencing

1. **Track D** — beads + changelog (now; cheap, recoverable).
2. **Track A** — `A1 → A2 → A3` (the release chain; each step approval-gated and CI-verified before the next).
3. **Tracks B and C** — parallel follow-ons once A lands.

## 7. Verification (how we know it is real, not green-theater)

- **A1**: `npm view @intentsolutions/jrig-cli version` = `0.1.2`; the published tarball contains the #173 + #175 provider code; `cli-test.yml` green on the release tag.
- **A2**: cc-plugins `validate-plugins` green on the bump PR; a manual `j-rig eval` on a control-prompt-heavy skill no longer NO-SHIPs on off-topic criteria or truncated verdicts.
- **B/C**: every PR CI-green with the required gates; no rule-loosening, no threshold-lowering, no coverage exclusions — fixes land on the artifact, or a gate is honestly reclassified with a documented reason.

## 8. Risks + approval gates

- **Outward-facing, hard to reverse**: the npm publish (A1) and the cc-plugins production pin bump (A2) ship to a public marketplace's tooling — both wait on explicit go-ahead.
- **Version-line confusion**: `jrig-cli 0.1.x` is the published consumer CLI; the j-rig eval **engine** repo tracks its own `v0.14.0`-style line. The release is the CLI line (`0.1.2`), not the engine line.
- **cc-plugins doc drift**: docs `174` / `187` / `189` / `211` describe a stale Dec-2025 GitHub-Pages world; treat `693`, `691`, `6769`, and the live workflow files as ground truth.

---

- Jeremy Longshore
  intentsolutions.io
