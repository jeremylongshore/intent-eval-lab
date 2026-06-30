# AAR — Make the Intent Eval Platform demonstrably work end-to-end on real skills

- **Code**: AA-AACR (After-Action / Accomplishment Capture Report)
- **Date**: 2026-06-29
- **Author**: Jeremy Longshore (intentsolutions.io)
- **Epic (bd)**: `bd_000-projects-h08j` — "Make the Intent Eval Platform demonstrably work end-to-end on real skills and publish real results"
- **Status**: Phases 0–2 landed (PRs open, CI green); Phase 3 partially executed + boundary documented; Phases 3 (full batch) / 4 (publish) / 5 (hardening) = follow-on.

---

## 1. Objective

Prove — not assume — that the platform works: take a real skill, grade it with our
own tooling end-to-end, and have a real, signed result land where it can be shown.
The starting belief was "the suites are green but the thing doesn't actually work,"
and a ground-truth read of all six repos confirmed that in three specific places:

1. **No real Evidence Bundle flowed end-to-end** — `j-rig eval` computed a verdict
   but never emitted a `gate-result/v1` bundle; every downstream seam was simulated.
2. **Grading couldn't scale** — `j-rig eval` required a hand-authored spec per skill
   and there was no generator. ~2 of ~3,192 SKILL.md files were eval-ready.
3. **The `/skills/` page on the site was 100% no-data** (`NO_SIGNALS` resolver).

Plus trust gaps: docs claimed capabilities the code didn't have.

## 2. What shipped

| Phase | Deliverable | PR | CI |
|---|---|---|---|
| 0 (truth) | `intent-rollout-gate` SECURITY.md de-lied to actual v0.3.0 behavior + version drift | [intent-rollout-gate#46](https://github.com/jeremylongshore/intent-rollout-gate/pull/46) | green |
| 0 (truth) | j-rig CLAUDE.md stale "auto-bump" release claim corrected | [j-rig#171](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/171) | green |
| 0 (truth) | `@intentsolutions/core` README v0.8.0 → v0.9.0 | [intent-eval-core#75](https://github.com/jeremylongshore/intent-eval-core/pull/75) | green |
| 0 (truth) | `validate-skillmd/SKILL.md` false "auto-generates a spec" claim corrected (local `~/.claude` skill) | — | n/a |
| 1 (chain) | `j-rig eval --emit-bundle`: real kernel-validated `gate-result/v1` Statement + committed e2e self-eval test | [j-rig#172](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/172) | green |
| 2 (scale) | `j-rig scaffold-spec`: generate a baseline eval-spec from a SKILL.md | [j-rig#174](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/174) | green |
| 3 (prereq) | Reasoning-model `max_tokens` fix across execution + trigger + judge providers | [j-rig#173](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/173) | green |

## 3. The proof (end-to-end, real components, no placeholders)

`j-rig eval` now emits a real, kernel-validated `gate-result/v1` in-toto Statement
(`--emit-bundle`). Verified locally, both directions of the gate:

```
# SHIP path (stub provider, deterministic):
j-rig eval ./skill --provider stub --emit-bundle bundle.json   → gate_decision: pass
intent-rollout-gate (policy j-rig:local:*)                      → decision: allow

# NO-SHIP path (REAL DeepSeek, ground_truth: true):
j-rig eval databricks-cost-leak-hunter --provider deepseek --emit-bundle b.json
  → gate_decision: fail   (real input_hash, real git commit_sha, NO 1111… placeholders)
intent-rollout-gate (policy j-rig:local:*)
  → decision: block, reason "required gate 'j-rig:local:*' present but not passing"
```

- The bundle shape is exactly what `intent-rollout-gate` consumes (in-toto Statement
  array). `commit_sha` is resolved honestly (env → skill-dir git HEAD →
  content-derived slice, with the source recorded in `metadata.commit_sha_source`).
- A committed e2e test (`eval.e2e.test.ts`) spawns the built CLI evaluating j-rig's
  own skill and asserts a kernel-valid bundle with non-placeholder hashes — *the
  tool that evaluates skills, tested evaluating a skill* (071 P1 #6).
- Signing (cosign → Rekor) is the only un-exercised step; it is dispatch-only /
  DNSSEC-gated and flows through release CI per DR-002 § 6.3.

`scaffold-spec` was verified on a real skill (`~/.claude/skills/doc-filing`):
extracted real trigger phrases ("organize docs", "file documents") and produced a
kernel-valid spec — turning "grade the hand-spec'd skills" into "grade the library."

## 4. Findings

### 4.1 Plan claims corrected by ground-truth verification (verify-before-claim earned its keep)

1. j-rig CLAUDE.md was **already** Apache-2.0 (the plan's "fix MIT→Apache" was stale);
   the real drift was the auto-bump release line.
2. `intent-rollout-gate` already had a **real** self-generated dogfood
   (`scripts/dogfood-bundle.mjs`), not the `1111…` static fixture the plan described.
   The genuine gap was only on the j-rig emit side.
3. The rollout-gate fixtures live at `tests/fixtures/evidence/`, not
   `tests/dogfood/bundle.json`.

### 4.2 Reasoning-model `max_tokens` exhaustion (the real Phase-3 blocker)

`deepseek-v4-flash` is a reasoning model: hidden chain-of-thought tokens count
against `max_tokens` but never appear in `content`. The OpenAI-compat providers sent
small budgets, so reasoning exhausted them and returned empty/truncated output that
silently became garbage grades:

| Layer | Old budget | Symptom | Fix |
|---|---|---|---|
| Execution | 1024 | empty `content`, `finish_reason=length` → false BLOCK | 8192 + throw on empty+length |
| Judge | 256 | empty verdict → `parseJsonObject(null)` → false "unsure" | 2048 |
| Trigger | 256 | truncated routing → missed triggers | 2048 |

Empirically verified against DeepSeek (2026-06-29): complex task @400 → 0 chars,
@8000 → 5792 chars. After the fix on a real eval: **trigger recall 0.75 → 1.00**;
**judge "unsure" 7 → 2** with real yes/no verdicts (including a genuine PASS on
`checks-grant-chain-upfront`).

### 4.3 Residual eval-coverage boundary (documented, not faked)

After the fixes, `databricks-cost-leak-hunter`'s functional **execution** still
returns empty for the cost-question prompts specifically, while producing real
output for the grant-chain case. The most likely cause is that this skill is
**tool/script-dependent** (it ships a `scripts/` dir and is designed to *run*
queries, not answer in a single completion turn) — so a single-turn completion eval
cannot fully grade it. This is an eval-coverage boundary, not a wiring bug, and
matches the plan's directive to "document the boundary rather than fake depth." It is
tracked on `bd_000-projects-h08j.4`; fully characterizing it needs in-eval response
instrumentation (log `result.text`/`finishReason` per test case).

**Consequence for Phase 3**: do not scale the ~10-skill batch on reasoning-model
DeepSeek until per-skill execution output is spot-checked; tool-dependent skills need
either a different provider, a tool-enabled harness, or an explicit "not gradeable by
completion" classification.

## 5. Verification posture

- Every code PR is CI-green (Test / Lint / Typecheck / CodeQL / dogfood). j-rig full
  gate `pnpm run check`: 1215 → 1224 tests as new tests landed (e2e self-eval +2
  execution guard +2 judge/trigger headroom +7 scaffold-spec).
- All real DeepSeek runs used `ground_truth: true`; the key was decrypted in-process
  from SOPS to `/dev/shm`-equivalent (never written to disk).
- No placeholder hashes in any emitted bundle; `commit_sha` provenance is labeled.

## 6. Tracking

- Epic `bd_000-projects-h08j` + 7 phase children (`h08j.1`–`.7`).
- `h08j.1` (Phase 0) and `h08j.2` (Phase 1) marked `in_progress` with full evidence
  notes; `h08j.3` (Phase 2) delivered; `h08j.4` (Phase 3) carries the empty-output /
  reasoning-model diagnosis and the documented boundary.
- Follow-on: GH-issue + Plane mirror for the epic/phases (PRs + bead notes currently
  carry recovery context); merge the 6 PRs; resolve the residual execution boundary;
  complete Phase 3 batch + Phase 4 publish + Phase 5 hardening.

## 7. Lessons

1. **Verify the plan against the code before executing.** Three plan claims were
   stale; acting on them blindly would have produced churn or wrong fixes.
2. **A green suite is not a working system.** The make-or-break gap (no bundle ever
   emitted) sat under 1200+ passing tests.
3. **Reasoning models break naïve `max_tokens`.** Any provider call that expects
   content must budget for hidden reasoning; a too-small budget fails *silently* as
   empty content, which downstream code charitably interprets (empty output → "the
   skill produced nothing" → BLOCK; empty verdict → "unsure"). Surface truncation as
   an error; don't let it masquerade as a real result.
4. **Honest boundaries beat fake depth.** A generated baseline spec grades trigger +
   safety; tool-dependent skills aren't fully gradeable by single-turn completion —
   say so rather than ship a confident-but-meaningless grade.

---

- Jeremy Longshore
intentsolutions.io
