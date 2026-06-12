# 051-AA-AACR — Umbrella Review-and-Fix Wave — 2026-06-11

| Field | Value |
|---|---|
| **Doc** | `051-AA-AACR-umbrella-review-and-fix-wave-2026-06-11.md` |
| **Date** | 2026-06-11 / 2026-06-12 |
| **Status** | FINAL |
| **Scope** | 6 IEP repos · 443 open beads (full docket) · 10 code surfaces |
| **Repos** | intent-eval-core, intent-eval-lab, j-rig-skill-binary-eval, intent-audit-harness, intent-rollout-gate, claude-code-plugins-plus-skills |
| **Companion** | `051a` — machine-readable `final-output.json` (full per-bead dispositions, findings, synthesis), filed alongside this doc |

---

## 1. What ran

Three orchestrated agent workflows, end to end, 2026-06-11 into 2026-06-12:

| Phase | Run id | Shape |
|---|---|---|
| **Review** | `wf_fd40cbff-045` | 24-agent workflow: 19 fan-out agents (10 code reviewers, right-sized per repo hotspot + 9 bead auditors covering all 443 open beads in chunks), a scripted evidence gate (every disposition must cite file/commit/PR evidence), an adversarial verify wave re-checking every P0/P1 claim against origin/main, and a synthesizer. |
| **Wave-1 fixes** | `wf_9412dd87-3c1` | 12 agents: 6 fixer branches (one per repo), each adversarially diff-verified by a paired reviewer before PR. |
| **Wave-2 builders** | `wf_dcb2e355-490`, `wf_c7bd4d6b-dd7` | Rollout-gate decision-logic package extraction + publish; intent-rollout-gate M5 builder consuming it. |

The verify wave was load-bearing: it both confirmed the 9 real P0/P1 findings against exact source lines and killed 3 plausible-looking false claims before any fix work was scheduled (§ 3).

## 2. Findings funnel

```
35 raw findings  →  12 P0/P1 escalated to adversarial verify  →  9 confirmed / 3 refuted
                    23 P2/P3 retained as advisory backlog
```

Zero unverified P0/P1 claims survived into the fix wave.

### 2.1 Confirmed P0/P1 (9)

| ID | Repo | Sev | Location | Finding |
|---|---|---|---|---|
| f-jrig-core-1 | j-rig-skill-binary-eval | **P0** | `packages/core/src/judgment/engine.ts:50` | Judgment engine calls `runCheck()` without forwarding `params`, so the built-in deterministic checks `contains`, `regex_match`, `min_length`, `max_length` resolve to vacuous defaults (`''`, min 0) and **pass on any input** from the engine path. |
| f-jrig-core-2 | j-rig-skill-binary-eval | P1 | `g1-credential-redaction.ts:107-130` (+ g2) | CISO-gate timeout sets a flag but never aborts the awaited `invokeProvider()`; a hung adapter blocks forever and leaves stdout/stderr patched. |
| f-jrig-security-1 | j-rig-skill-binary-eval | P1 | `packages/cli/src/commands/emit-evidence.ts:129-132, 257-261` | Default `--sign` path feeds the FULL in-toto Statement to cosign as the predicate, double-wrapping the attestation; gate-result fields land off `predicate.*`. |
| f-iec-validators-1 | intent-eval-core | P1 | `src/validators/v1/eval-spec.ts:17-23` | `ScoringConfigSchema` is `.strict()` while the JSON Schema leaves `scoring` open — valid tool-extension payloads pass schema validation but are rejected by Zod. |
| f-iec-validators-3 | intent-eval-core | P1 | `src/validators/v1/gate-result-v1.ts` + schema | NORMATIVE Blueprint B § 7.4 invariant (gate_reasons non-empty for fail/advisory/error) lives only in a description string — enforced by neither JSON Schema allOf nor Zod superRefine. A reasonless `fail` produces a valid signed predicate row. |
| f-iah-python-1 | intent-audit-harness | P1 | `scripts/crap-score.py:168` | Test-kind gocyclo invoked with `-ignore '.*\.go$'` — ignores every .go file; Go test CRAP scores permanently empty, gate silently passes. |
| f-iah-python-2 | intent-audit-harness | P1 | `scripts/crap-score.py:180,190-199` | gocyclo relative paths never match go-tool-cover module-qualified paths; every Go method scores at 0% coverage (max CRAP, inflated FAILs). |
| f-iah-python-3 | intent-audit-harness | P1 | `scripts/crap-score.py:231-247` | complexity-report relative paths never match c8 absolute-path keys in coverage-summary.json; every JS/TS method scores at 0% coverage. |
| f-iah-bash-1 | intent-audit-harness | P1 | `.github/workflows/ci.yml:74-79` | Escape-scan CI self-check permanently dark: piping through `tee` without pipefail makes the `if` always test tee's exit 0; the "correctly refused" branch is unreachable. |

**P0 hand-verification note.** The judgment-engine P0 was hand-verified before any fix was scheduled: a human read `engine.ts:50` on an origin/main worktree and confirmed the call is exactly `runCheck(criterion.deterministic_check, outcome.output.text)` — two arguments against a three-argument `runCheck(checkName, input, params?)` signature — and confirmed the vacuous defaults in `deterministic-registry.ts`. This is a silent false-pass in the exact code the product sells as its trust anchor; it gated the v2.0.0 release until fixed (j-rig-skill-binary-eval#104, merged before the #103/#105 release train).

### 2.2 Refuted P0/P1 (3) — what the verify layer caught

| ID | Repo | Refuted claim | Why refuted |
|---|---|---|---|
| f-iar-fused-1 | intent-rollout-gate | "`actions/checkout@v6` / `setup-node@v6` do not exist; latest stable is v4; CI fails to resolve on every run." | Factually wrong on every count: GitHub API shows `actions/checkout` latest release `v6.0.3` and `actions/setup-node` latest `v6.x`. The cited lines exist; the conclusion did not. A confident, specific, checkable claim — and false. |
| f-jrig-core-3 | j-rig-skill-binary-eval | Evidence-writer `array` format contradicts the CHANGELOG wire-format doc. | The finding's two evidence halves came from **different branches**; no CHANGELOG on main contains the quoted text (the related line is in a pending-v2.0.0 section). No mismatch exists on main. |
| f-iel-scripts-1 | intent-eval-lab | Drift extractors silently hash empty grep output, producing a stable empty-input hash that masks upstream changes forever. | Defeated by `set -euo pipefail`: a grep no-match propagates as the pipeline's exit status, the extractor returns non-zero, and the caller's fetch-error trap fires before any seed/compare in every mode. |

Recording these matters: all three were severity-tagged, plausibly written, and would have consumed fixer time (or worse, "fixed" working code). The adversarial verify wave is the reason machine findings were treated as actionable.

## 3. Repo health (synthesis grades)

| Repo | Grade | Summary |
|---|---|---|
| intent-eval-core | B+ | Validators and gate-chain tight, codegen deterministic, SAK shipped through v0.5.0 on schedule. Held off an A by four parity defects (strict/open scoring, unenforced gate_reasons invariant, missing minLength on 4 fields, unregistered Evidence schemas) and two gate-coverage gaps (authoring/v2 outside the namespace gate; byte-freeze omits 5 of 7 validator files). |
| j-rig-skill-binary-eval | C | One confirmed P0 in the judgment engine plus a hangable CISO-gate timeout, a double-wrapping default sign path, and an over-matching coverage-floor regex. Shipped surface otherwise solid (MM-1..6, G-1/G-2, stub discipline); 15 beads verified done. Grade reflects pre-fix state — all P0/P1s landed in #104 before release. |
| intent-eval-lab | B- | Spec-drift machinery (16 surfaces, daily cron, field-diff, liveness) is the most advanced continuity infrastructure in the ecosystem; weakened by a claim-precheck gate that prints its own bypass and a retired ntfy topic silently dropping drift alerts. Heavy rescope debt in the docket (stolen doc-number slots, superseded quarterly asks). |
| intent-audit-harness | C- | Three of four CRAP language backends systematically wrong in production (Go test scores empty, Go/JS coverage always 0%, Rust hardcoded 0.0) and the golden suite was deliberately built around the no-provider path so CI could not catch it. Dispatcher, bash layer, npm pipeline well-built — a correctness failure in the scoring core of a measurement tool. |
| intent-rollout-gate | B- | Honest v0.0.0 stub, injection-hardened (env + `jq --arg`); 59-bead docket uniformly consistent with reality, all legitimately blocked on the rollout-gate 2.0.0 release. Small real defect: three declared inputs never wired into the env block. (The headline CI claim against this repo was the refuted one.) |
| claude-code-plugins-plus-skills | B- | Validator honors the SCHEMA_CHANGELOG non-negotiables; 30 of 31 workflows properly hardened including the pull_request_target path. But `validate_tool_permission` always returned True (malformed allowed-tools passed at every tier), missing `name` at standard tier emitted zero diagnostics, and sync-external.yml carried a live repository_dispatch template injection. |

Headline from synthesis: **both of the platform's measurement engines were lying in production** (j-rig vacuous-pass P0; harness CRAP backends), and every failure mode was silent — both repos looked healthy from the outside.

## 4. Bead outcomes

All 443 open beads dispositioned; 0 unaudited; 0 evidence-gate downgrades; 0 unknown IDs dropped.

| Disposition | Count | Outcome |
|---|---|---|
| keep | 331 | The honest remaining roadmap — survives audit as-is. |
| re-scope | 62 | Description notes applied (blown version anchors, doc-number slots taken by later files, partially-landed epics, asks superseded by daily crons). |
| close-now | 39 | Verified done with file/commit/PR evidence; closed in Wave-0. |
| duplicate | 6 | Closed against named survivors with cross-ref notes. |
| lands-with-PR-103 | 5 | Re-judged after j-rig #103 merged; closed with merge-commit evidence. |

**Wave-0 execution detail** (45 closes = 39 close-now + 6 duplicates): 24 closed clean on the first pass; **21 were refused by bd's dependency check** ("blocked by open issues") because stale blocking edges pointed at beads that were themselves verified-done or out of scope. The batch-close verify step caught all 21 (count-and-grep against the JSONL after each group), and they were re-issued individually with `--force` after the blocking edges were confirmed stale. Final state: all 45 verified CLOSED in the exported JSONL. Per-bead IDs and evidence lines live in the 051a companion, not here.

## 5. Ships (PR ledger)

| Repo | PR | What landed |
|---|---|---|
| claude-code-plugins-plus-skills | #858 | Sponsor de-branding (a former sponsor's name removed from repo surfaces) + 4 pre-existing CI repairs picked up in-flight. |
| claude-code-plugins-plus-skills | #860 | Validator fixes: real `validate_tool_permission` enforcement, standard-tier missing-name diagnostic, stale warnings-only docstrings refreshed. |
| claude-code-plugins-plus-skills | #861 | 75-finding actionlint cleanup across the workflow fleet (incl. the sync-external.yml injection route through `env:`). |
| intent-eval-lab | #121 | Watcher hardening: claim-precheck bypass text removed, retired ntfy topic retargeted, extractor robustness. |
| j-rig-skill-binary-eval | #104 | **The P0** (params threaded through the engine path, regression tests proving checks fail on bad input) + 6 companion P1/P2 fixes (timeout race, sign default, coverage-floor regex, etc.). |
| j-rig-skill-binary-eval | #103 | v2.0.0 kernel migration (pre-existing branch, conflict-resolved post-#104). |
| j-rig-skill-binary-eval | #105 | v2.0.0 release prep. |
| j-rig-skill-binary-eval | #106 | Rollout-gate decision-logic package extraction. |
| j-rig-skill-binary-eval | #107 | Publish workflow fix (build-before-typecheck; see lesson 8d). |
| intent-audit-harness | #66 | CRAP backend corrections (gocyclo test pattern, Go/JS path normalization, Rust coverage honesty) + bash fixes (escape-scan self-check unmasked, SHA256_CMD, OTEL JSON escaping). |
| intent-eval-core | #36 | Validator parity (scoring open-world, minLength) + gate_reasons non-empty enforced in BOTH JSON Schema allOf and Zod superRefine. |

**Releases:** j-rig **v2.0.0** (GitHub release, post P0-fix); **`@intentsolutions/rollout-gate@2.0.0`** published to npm with sigstore provenance (transparency log index 1798629513).

## 6. Decisions made under delegated authority

1. **Branch protection — required checks wired** on j-rig-skill-binary-eval (`Lint`, `Test`, `Typecheck`), intent-eval-lab (`Validate specs and docs`, `harness-hash --verify`), and intent-audit-harness (13 contexts: manifest version+license alignment, SemVer contract suite, the audit/classify/conform/scan golden suites, crap-score join-regression, golden-master stdout suite, layer-applicability projection drift, py_compile, ruff, shellcheck). Advisory lanes (CISO gates, coverage advisories) and matrix-expanded lanes were deliberately excluded: advisory lanes are non-blocking by design, and matrix job names churn with matrix edits, which would brick merges on a rename rather than on a regression.
2. **intent-audit-harness stays npm-canonical.** PyPI (`intent-audit-harness`) and crates.io legs deferred to a post-fix release — publishing polyglot mirrors of a scorer with known-wrong backends was the wrong order of operations.
3. **DR-028 T3 satisfied by the GH projection.** The spec-drift watcher's auto-filed GitHub issue + bd projection satisfies the original "issue auto-filed on drift" ask; no separate Plane automation is built (bd is the canonical writer, GH/Plane are projections).
4. **The publishable decision-logic package ships as `@intentsolutions/rollout-gate`**, not `@j-rig/rollout-gate`: the `@j-rig` npm scope is inaccessible to the org account. `@j-rig/*` stays internal-private; the substance of DR-018 (decision logic published as a consumable 2.0.0 package that unblocks intent-rollout-gate) is preserved under the reachable scope.
5. **Lost doc numbers are never reclaimed.** The four lab standards docs whose planned 000-docs numbers were taken by later files get next-free numbers when authored; this AAR itself files at 051 under that rule.

## 7. Process lessons

1. **Evidence gate + adversarial verify + hand spot-checks made machine dispositions trustworthy.** Every close-now required citable evidence; every P0/P1 was re-verified against origin/main; 5 of 5 hand spot-checks of machine dispositions passed. The 3 refuted findings (§ 2.2) are the proof the verify layer pays for itself — including a confidently-stated "this action version doesn't exist" claim that was wrong against the live GitHub API.
2. **bd batch closes abort on dependency edges — verify-after-write is mandatory.** 21 of 45 closes were silently absent after the batch pass (bd refuses per-bead and continues); the post-write JSONL grep caught every one. Never trust a batch mutation's exit chatter; count terminal states.
3. **Auto-bump bot ping-pong.** The de-brand PR (#858) entered a rebase loop with the repo's version auto-bump bot; the `[skip auto-bump]` commit-message escape hatch is the documented exit. Use it on any PR that touches files the bot also touches.
4. **Publish workflows must build before typecheck on fresh clones.** Workspace `dist/` artifacts don't exist on a clean CI checkout, so typecheck-first fails on imports of sibling packages (fixed in j-rig #107).
5. **Private workspace deps must be bundled into published artifacts.** `@intentsolutions/rollout-gate` depends on private `@j-rig/*` workspace packages; publishing requires tsup `noExternal` bundling + dts resolution so the tarball is self-contained.

## 8. Pointers

- **This doc:** `000-docs/051-AA-AACR-umbrella-review-and-fix-wave-2026-06-11.md` (intent-eval-lab).
- **Companion 051a:** the full machine-readable review output (`final-output.json` — stats, 10 surface summaries, all 35 findings with verify reasoning, 443 per-bead dispositions, synthesis) files alongside this doc; both commit together.
- **Run artifacts** (chunk inputs, wave plans, close logs, fixer briefs) are archived with the companion; bead-level forensics resolve through the umbrella bd workspace per the three-layer mirror discipline.
- **Open follow-ons** ride the surviving docket: the 23 advisory P2/P3 findings, the 62 re-scoped beads, and the intent-rollout-gate M5 docket now unblocked by `@intentsolutions/rollout-gate@2.0.0`.
