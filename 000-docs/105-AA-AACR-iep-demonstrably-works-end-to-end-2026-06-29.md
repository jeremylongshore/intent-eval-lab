# AAR — Make the Intent Eval Platform demonstrably work end-to-end on real skills

- **Code**: AA-AACR (After-Action / Accomplishment Capture Report)
- **Date**: 2026-06-29
- **Author**: Jeremy Longshore (intentsolutions.io)
- **Epic (bd)**: `bd_000-projects-h08j` — "Make the Intent Eval Platform demonstrably work end-to-end on real skills and publish real results"
- **Status**: Phases 0–2 + reasoning-model fixes landed and **merged** to main; Phase 3 partially executed + boundary documented. Continuation (§ 8, 2026-06-30 → 07-01): **13 PRs merged ecosystem-wide**, lab CI hardened, a per-repo GitHub Actions outage weathered + reported. Phases 3 (full batch) / 4 (publish) / 5 (per-repo hardening) = follow-on.

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

| Phase      | Deliverable                                                                                                 | PR                                                                                       | CI    |
| ---------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----- |
| 0 (truth)  | `intent-rollout-gate` SECURITY.md de-lied to actual v0.3.0 behavior + version drift                         | [intent-rollout-gate#46](https://github.com/jeremylongshore/intent-rollout-gate/pull/46) | green |
| 0 (truth)  | j-rig CLAUDE.md stale "auto-bump" release claim corrected                                                   | [j-rig#171](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/171)         | green |
| 0 (truth)  | `@intentsolutions/core` README v0.8.0 → v0.9.0                                                              | [intent-eval-core#75](https://github.com/jeremylongshore/intent-eval-core/pull/75)       | green |
| 0 (truth)  | `validate-skillmd/SKILL.md` false "auto-generates a spec" claim corrected (local `~/.claude` skill)         | —                                                                                        | n/a   |
| 1 (chain)  | `j-rig eval --emit-bundle`: real kernel-validated `gate-result/v1` Statement + committed e2e self-eval test | [j-rig#172](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/172)         | green |
| 2 (scale)  | `j-rig scaffold-spec`: generate a baseline eval-spec from a SKILL.md                                        | [j-rig#174](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/174)         | green |
| 3 (prereq) | Reasoning-model `max_tokens` fix across execution + trigger + judge providers                               | [j-rig#173](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/173)         | green |

## 3. The proof (end-to-end, real components, no placeholders)

`j-rig eval` now emits a real, kernel-validated `gate-result/v1` in-toto Statement
(`--emit-bundle`). Verified locally, both directions of the gate:

```text
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
  own skill and asserts a kernel-valid bundle with non-placeholder hashes — _the
  tool that evaluates skills, tested evaluating a skill_ (071 P1 #6).
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

| Layer     | Old budget | Symptom                                                  | Fix                          |
| --------- | ---------- | -------------------------------------------------------- | ---------------------------- |
| Execution | 1024       | empty `content`, `finish_reason=length` → false BLOCK    | 8192 + throw on empty+length |
| Judge     | 256        | empty verdict → `parseJsonObject(null)` → false "unsure" | 2048                         |
| Trigger   | 256        | truncated routing → missed triggers                      | 2048                         |

Empirically verified against DeepSeek (2026-06-29): complex task @400 → 0 chars,
@8000 → 5792 chars. After the fix on a real eval: **trigger recall 0.75 → 1.00**;
**judge "unsure" 7 → 2** with real yes/no verdicts (including a genuine PASS on
`checks-grant-chain-upfront`).

### 4.3 Residual eval-coverage boundary (documented, not faked)

After the fixes, `databricks-cost-leak-hunter`'s functional **execution** still
returns empty for the cost-question prompts specifically, while producing real
output for the grant-chain case. The most likely cause is that this skill is
**tool/script-dependent** (it ships a `scripts/` dir and is designed to _run_
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
   content must budget for hidden reasoning; a too-small budget fails _silently_ as
   empty content, which downstream code charitably interprets (empty output → "the
   skill produced nothing" → BLOCK; empty verdict → "unsure"). Surface truncation as
   an error; don't let it masquerade as a real result.
4. **Honest boundaries beat fake depth.** A generated baseline spec grades trigger +
   safety; tool-dependent skills aren't fully gradeable by single-turn completion —
   say so rather than ship a confident-but-meaningless grade.

## 8. Continuation — merge, CI hardening, and a GitHub Actions outage (2026-06-30 → 07-01)

The Phase 0–2 PRs above were merged (with every AI-reviewer comment addressed in code
first), and the effort widened into repo-health + CI hardening. Net: **13 PRs merged
across the ecosystem; every repo's `main` is green.**

### 8.1 Merging the six PRs — reviewer comments addressed, not waved through

Before merge, 8 Gemini comments + 2 CodeQL alerts were resolved in-place:

- **j-rig#172 (HIGH):** `gate_id` sanitized the model but not the skill name — a
  non-kebab SKILL.md `name` could make `composeStatement` throw. Generalized to
  `sanitizeSegment(raw, fallback)` for both segments.
- **j-rig#174 (2 CodeQL):** TOCTOU file race (`existsSync`→`writeFileSync`) → atomic
  `wx` write; polynomial-ReDoS trim → linear; plus cross-platform `basename`, an
  explicit `models` field, and a kernel-safe `skill_name`.
- **j-rig#173:** execution `max_tokens` made overridable via `JRIG_MAX_OUTPUT_TOKENS`.
- **rollout-gate#46:** corrected the de-lie text itself (the action's `predicate-uri`
  _input_ blocks; a bundle row's differing `predicateType` is skipped, not rejected).
- **core#75:** entity count 15→16 (added `HumanReview`) to match the v0.9.0 CHANGELOG.
- **j-rig#171:** clarified which `package.json` each release flow uses.

### 8.2 A per-repo GitHub Actions event-delivery outage

For 3+ hours, `intent-eval-lab` stopped delivering `push`/`pull_request` events to
Actions while **cron and `workflow_dispatch` kept firing**. Config was healthy
(Actions enabled, workflows active, no path filters, no stuck queue). Every
client-side remedy was exhausted: 6 force-pushes, close/reopen, a fresh branch, an
**API** Actions toggle, and a **UI** toggle. A controlled empty-commit probe in a
sibling repo (`intent-rollout-gate`) fired instantly — proving the fault was
**isolated to one repo and GitHub-side**, not account-wide. Reported officially at
GitHub Community Discussions
[#200604](https://github.com/orgs/community/discussions/200604) (there is no support
email, and Free-tier support tickets exclude Actions). Delivery recovered on its own
hours later; the queued PRs were then finished the normal way (real CI, no bypass).

### 8.3 Repo-health fixes surfaced along the way (#211)

A `[skip ci]` capture commit had left `main` red on three gates once a PR re-ran them:

- **SAK dashboard** was stale vs `coverage-map.json` → regenerated (the generator
  owns the bytes; `--check` + `--self-test` pass).
- **typos** tripped on captured external content (an Anthropic web-page snapshot plus
  Claude Code changelog/release bodies) → excluded `**/_vendor/**` + `archive/raw/**`
  (captured HTML is not ours to spell-fix).
- **markdownlint MD026** flagged the `104-RR-LAND` doc's `?`-ending section heading →
  rephrased to statement form (**not** by loosening the rule); the doc was also
  prettier-formatted with the pinned CI version (3.8.4).
- Doc-number collision resolved: `104-RR-LAND` keeps 104; this AAR renumbered to
  **105** ([#210](https://github.com/jeremylongshore/intent-eval-lab/pull/210),
  [#211](https://github.com/jeremylongshore/intent-eval-lab/pull/211)).

### 8.4 The two advisory Python gates (mypy, pytest)

- **mypy 64 → 0** — real type fixes: an `LLMProvider` Protocol instead of bare
  `object`, an accurate `EditProposal | None` return type, and 10 stale `# type:
ignore` removed. Now green in CI.
  ([#212](https://github.com/jeremylongshore/intent-eval-lab/pull/212))
- **pytest coverage 59.5% → 66.1% (local)** via real smoke tests (`build-fixtures.py`
  0%→97.4%, driven with a stub-injected `--score-script`) — no threshold lowering, no
  exclusions.
- **Root cause of the CI-vs-local coverage gap** (the code comment guessed "subprocess
  timing" — wrong): **CI lacks the external dependencies the integration tests need.**
  `score-fixture.py` shells out to a validator that lives in another repo not checked
  out in CI (0% there), and `run-arm-b`'s deep paths need real model keys. CI runs
  only the hermetic subset (42%) while the dev box runs the full suite (66%), so the
  gate is **correctly advisory** (`continue-on-error`) and the tests — the real signal
  — all pass. Forcing 60% would mean mocking out the real validator + providers, a
  different kind of shortcut.
- **A HIGH review finding fixed**
  ([#213](https://github.com/jeremylongshore/intent-eval-lab/pull/213)): `json.loads`
  accepts `null`/arrays/scalars without raising, so a `null` model response crashed
  `run-arm-b`'s dry-run path. Extracted a testable `_extract_json_object` (requires a
  JSON object), replaced a fragile `assert` with a defensive check, and added **9
  regression tests** (importlib-loaded so the hyphenated script is testable
  in-process). 79 tests pass.

### 8.5 Lessons from the continuation

Three more, continuing § 7:

1. **A single `[skip ci]` capture commit can rot `main` invisibly.** It looks green
   because CI never ran on it; the next PR inherits the breakage. Derived/generated
   artifacts (the SAK dashboard) and captured external content (typos/prettier scope)
   both need explicit CI-scope discipline.
2. **"No shortcuts" cuts both ways.** Fixing a lint failure means fixing the artifact,
   not loosening the rule; making a coverage gate green means adding real tests, not
   lowering the floor or excluding files — _and_ it means being honest when a gate is
   correctly advisory rather than mocking reality to hit a number.
3. **Diagnose the platform, don't trust the comment.** The pytest coverage comment
   blamed subprocess timing; the real cause was missing external deps. A controlled
   cross-repo probe (an empty-commit PR) is what proved the Actions outage was
   per-repo and GitHub-side.

---

- Jeremy Longshore
  intentsolutions.io
