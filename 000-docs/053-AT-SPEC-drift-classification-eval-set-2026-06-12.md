# 053-AT-SPEC — drift-classification/v1 frozen eval set

**Date:** 2026-06-12
**Status:** NORMATIVE (governs the LLM drift-classifier write gate)
**Artifacts:** `evals/drift-classification/v1/` · `scripts/drift-eval-runner.py` · CI step in `.github/workflows/ci.yml` ("Validate specs and docs")
**Companions:** 050-AT-SPEC (upstream surface registry) · 045-RR-LAND (SSoT + continuous spec compliance) · `scripts/spec-drift-check.sh` / `scripts/spec-projection-diff.py` (the machinery this extends)

## Purpose

The byte-hash watcher says "a surface changed"; FF#2 says "the skill-frontmatter shape changed". The next stage — an LLM classifier that triages raw upstream diffs into material vs immaterial in advisory-comment mode — must not be trusted by default. This eval set is the **write gate**: the classifier writes nothing (no auto-refresh, no auto-triage labels treated as authoritative) until it clears a recall floor of **1.0 on material cases** against a frozen, human-labeled set of real upstream-snapshot diffs. Missing a material change is the unrecoverable failure (a stale kernel contract); a false positive only costs one human review.

## Contents

15 cases at `evals/drift-classification/v1/cases/<id>/{before,after,meta.json}`:

- **3 real** (`real-0001..0003`) — every real before/after diff of an upstream snapshot file in this repo's git history (the `0f56bfc → 8ade071` doc-lint pass over `research/agentskills-spec-v1.0-snapshot.md`, `research/agentskills-spec-v1.0.0.md`, `research/claude-docs-spec-tree-2026-05-27.md`; verified formatting-only by normalized token comparison). The `.sha` baselines have never been refreshed (seed-only history), so no further real diffs exist yet.
- **12 synthetic** (`syn-0001..0012`, marked `"synthetic": true`) — perturbations of real snapshot material (`_vendor/upstream/skill-frontmatter/agentskills-spec-v1.0.md`, `research/claude-docs-spec-tree-2026-05-27.md`) covering: field added, field removed, required flag flipped, constraint value changed, experimental marker dropped, field moved between standard/extension layers, hook event removed, MCP schema revision re-pinned, prose-only edit, whitespace/formatting-only edit, anchor renumbering, version-signal-only bump.

## Label rubric

`meta.json` per case: `{id, surface_id, source: real|synthetic, label, expected_contract_owner, rationale, provenance}`.

- **material** — the change would require a kernel base/overlay edit (`@intentsolutions/core` `schemas/authoring/v1`) or a consumer-visible validation-behavior change. Examples: field added/removed, required/experimental flag flipped, constraint or enum value changed, hook event added/removed, protocol revision re-pinned, field moved between spec layers.
- **immaterial** — formatting, prose rewording, ordering, anchor renumbering, or a version signal with no contract-surface change. Byte hash fires; no kernel edit follows.
- **expected_contract_owner** — one of the 6 kernel authoring contracts (`skill-frontmatter`, `plugin-manifest`, `agent-definition`, `mcp-config`, `hook-config`, `marketplace-catalog`) or `none`. Immaterial cases are always `none`.
- **surface_id** — a `name` from `specs/upstream-surface-registry.v1.json`, or `multi` for snapshots spanning several surfaces.

## Freeze / extension protocol

`manifest.json` carries `{version, frozen_at, model_pin, recall_floor: 1.0, case_count, case_files, cases.<id>.sha256.<file>}`.

1. **Existing cases are NEVER edited** — not even typo fixes. A wrong label is corrected by appending a superseding case and recording the defect here.
2. **New cases append via PR**: add `cases/<id>/{before,after,meta.json}`, add the case's hash entry to `manifest.json`, bump `case_count`. Future labels bootstrap from advisory-comment-mode overrides (a human overriding the classifier's advisory call is a labeled case by construction).
3. **CI enforces the freeze**: every PR re-hashes all case files via `drift-eval-runner.py --verify-manifest` in the "Validate specs and docs" job; any divergence (edited file, unmanifested dir, missing case) hard-fails.
4. **`model_pin` is `null` until a classifier registers.** When one does, its pinned model/version string is recorded in `manifest.json` in the same PR that publishes its eval result; changing the pin re-runs the full gate.

## The recall-floor write-gate contract

A classifier earns write privileges only by a published run of:

```bash
python3 scripts/drift-eval-runner.py --score PREDICTIONS.jsonl
```

where `PREDICTIONS.jsonl` has one `{"case_id", "label", "contract_owner"}` object per line. The runner verifies manifest integrity first (scores against a drifted set are meaningless), computes recall on material / precision / per-case table / contract-owner accuracy (informational), and **exits nonzero when recall < `recall_floor`**. A missing prediction for a material case is a miss — abstention does not clear the floor. The runner only scores; LLM invocation lives outside this repo. `--self-test` proves the gate is not vacuous (perfect fixture passes, missed-material fixture fails, a tampered case fails integrity) and runs in CI.

— Jeremy Longshore
intentsolutions.io
