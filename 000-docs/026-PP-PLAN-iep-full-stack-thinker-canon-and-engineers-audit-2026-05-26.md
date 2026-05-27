# IEP Full-Stack Audit: Thinker Canon + Engineers Panel Review of Entire Epic + Bead Buildout

| Field | Value |
|---|---|
| Status | DRAFTED 2026-05-26 |
| Owner | Jeremy Longshore (executor: Claude as drafting CTO) |
| Type | Audit-orchestration plan (the plan IS the input; the audit is the output) |
| Trigger | User direction 2026-05-26: "make a /plan to have a team of experts engineers and thought leaders thinker canon audit the entire epic bead build out we have so far to ensure everything is in line — this is a parfe project lots of wires to keep straight" |
| Companion plan | `025-PP-PLAN-j-rig-keeper-pretrip-evidence-2026-05-26.md` (the buildout being audited) |
| Status banding | ACTIVE |

## Why this audit, why now

The IEP has grown into a multi-repo, multi-epic, multi-priority structure with cross-cutting dependency edges. Right now it carries:

- 5 repos (intent-eval-lab, intent-eval-core, intent-audit-harness, intent-rollout-gate, j-rig-binary-eval)
- 56+ epics across the repos (some closed, many open)
- ~600+ beads in the umbrella workspace
- 8+ ratified Decision Records (DR-004 through DR-018+ series, with the j-rig + Keeper brand canon as the most recent)
- 1 newly-restructured 3-epic-26-child cluster (j-rig Keeper + Pre-Trip + Evidence — see companion plan)
- Multiple P0 dependency chains crossing repo boundaries (uprg → kernel v0.3.0; 9pi3 → kernel v0.2.0; bj5m → release tag pattern)
- 5 deferred standalone beads (j-rig MLOps Phase F + creator product)

User framing: "lots of wires to keep straight." The risk is structural drift — beads filed against old branding, dependency edges that no longer match the kernel-shadow inventory, brand-canon violations in older specs, abandoned epics still showing as in_progress, P0 chains gated on closed pre-conditions, etc. A full-stack audit before the next sprint catches drift before it compounds.

## Scope — what gets audited

**Everything currently live in the IEP**, across 5 audit lanes:

| Lane | Subject | Source-of-truth layer |
|---|---|---|
| **Lane 1 — Brand canon** | All public-facing artifacts (READMEs, specs, plan docs, repo names, package names, CLI names, blog drafts, gists) checked against the j-rig + intent-audit-harness brand canon decisions of 2026-05-26 | DR-010 § 13.6, plan 025, this plan |
| **Lane 2 — Bead structure** | All open epics + children: titles plain-English (post-2026-05-22 rule), parent-child graph correct, dependency edges valid, labels sane, no orphaned in_progress, no P0 chains gated on closed pre-conditions, no duplicate beads from race conditions | bd workspace (canonical SoT) |
| **Lane 3 — Cross-repo dependency graph** | Inter-repo edges across the 5 IEP repos: who consumes what, who emits what, schema-authority direction (kernel → consumers, never reverse), Evidence Bundle compat policy honored at every emitter+consumer pair | Blueprint A, Blueprint B § 7, kernel-shadow inventory (`intent-eval-lab/000-docs/016-RR-LAND`), DR-018 |
| **Lane 4 — Decision Record consistency** | Every ratified DR is still load-bearing OR explicitly marked superseded; § 13.5 + § 13.6 overrides still apply; ISEDC sessions traceable from binding rule → source DR; no contradictions between active DRs | intent-eval-lab/000-docs/0*-AT-DECR-* + DR-010 master |
| **Lane 5 — CI + governance gates** | Every repo's CI matches its claimed governance; partner-name-guard active everywhere it claims to be; harness-hash policy hash-pinned + verified; release.yml present for any package claiming an npm release; schema-drift.yml enforced where Blueprint B § 7.0 authority applies | per-repo .github/workflows/ + tests/TESTING.md + claimed posture |

**Out of scope** (explicitly):

- Code review of individual implementations (covered by /pr-review and /code-reviewer per-PR)
- Performance benchmarking
- Security pentest (covered by /security-review + dedicated security audits)
- Partner-engagement private content (lives in `.private/` per partner-consent discipline)
- Tier-2 research projects (semantic-flux etc. — separate methodology layer)

## The panel — who audits

A **7-9 seat panel** composed of two cohorts. **Each cohort's findings are kept distinct in the deliverable** — the engineers see the system as it is; the thinker canon sees the system through their canonical biases. Disagreements between cohorts are the highest-signal output.

### Cohort A — Engineers (4-5 seats)

Real-world engineering personas evaluating the system as a working system. Each is implementable as a Claude subagent or as a prompt invocation. The list:

| Seat | Persona | Audit focus |
|---|---|---|
| **A1 — Backend architect** | Senior backend engineer with 10+y experience across schema-evolution / multi-service systems | Cross-repo dependency graph (Lane 3); kernel-shadow inventory drift; schema authority direction |
| **A2 — Distributed-systems engineer** | Engineer who's debugged production incidents in multi-repo systems where releases ship out of order | Bead dep chain (Lane 2); P0 chain validity; release-tag-pattern adoption; one-way-door Rekor anchoring |
| **A3 — Release engineer** | Engineer who owns release ceremonies, CI gates, supply-chain attestation | Lane 5 (CI + governance gates); sigstore provenance posture; npm publish gap (iah-npm-publish-gap); release-failure alerting (59tx) |
| **A4 — DX engineer / API designer** | Engineer who writes SDKs + cares about the consumer ergonomics of every public surface | Brand canon (Lane 1); CLI surface coherence (j-rig keeper * vs /j-rig refine *); plugin shape ergonomics |
| **A5 — Site reliability engineer** | SRE who runs production for live customer-facing systems | VPS-as-the-home posture verification; alert routing; backup discipline; bd dolt server contention (the issue we just hit) |

**Cohort A method**: each seat reads the canonical SoT artifacts in their lane, identifies findings (severity-tagged: BLOCKER / MAJOR / MINOR / NIT), and reports in a 5-section template (scope, what they read, findings, recommendations, deferred-to-other-seat handoffs).

### Cohort B — Thinker canon reviewers (4-5 seats)

The existing 13 thinker-canon reviewer agents at `~/.claude/agents/<thinker>-reviewer.md` (created 2026-05-25 per bd-remember entry). They channel canonical biases of named thinkers; positions are verifiable against documented thinker writing/canon.

| Seat | Thinker | Audit focus |
|---|---|---|
| **B1 — Martin Fowler** | Pragmatic refactoring; bounded-context architecture; ubiquitous-language coherence | Whether the brand canon (j-rig Keeper / Pre-Trip / Evidence / Binary Eval) forms a coherent ubiquitous language across all artifacts |
| **B2 — Rich Hickey** | Value-orientation; complexity-vs-simplicity; "complecting" detection | Whether the bead restructure (3 epics × children) is genuinely simpler or just rearranged complexity; whether the Pre-Trip layers complect cost+lifecycle+depth |
| **B3 — Chip Huyen** | ML production practice; MLOps lifecycle; cost discipline; eval-set governance | Whether the Keeper tiered model routing (Haiku/Sonnet/Opus) is actually cost-disciplined; whether Phase F MLOps deferral is wise; eval-set bootstrap soundness |
| **B4 — Brendan Gregg** | Observability; flame graphs; "if you can't measure it, you can't fix it" | Whether OTel semconv (9pi3) actually pins what consumers need; whether Pre-Trip layers emit enough signal to debug a regression |
| **B5 — Martin Kleppmann** | Data systems; append-only logs; eventual consistency; one-way doors | Whether append-only event log + content-addressed store actually delivers replay; whether SkillVersion lineage is reconstructible from Rekor evidence alone |

**Cohort B method**: each seat reads the canonical SoT artifacts AND grounds findings in 3-5 verifiable citations to their thinker's actual writing. Findings preserve dissent — no consensus-forming pressure. Read-only roles per existing 13-agent precedent (per bd-remember: "Pattern: read-only reviewers propose; acting CTO executes. Single-signer audit trail").

### Why two cohorts (not one larger panel)

Engineers and thinker-canon reviewers disagree productively. Engineer finding ("this won't scale past 100 partners") + thinker finding ("this complects three concerns into one type") often land on the same root issue from different angles — the overlap is signal; the divergence is signal; both are visible only by keeping them separate.

## Methodology — how the audit runs

5 phases. Each ships an artifact before moving to the next.

### Phase 1 — Brief pack assembly (1 session)

Acting CTO (Claude) assembles the canonical brief pack the panel reads. Includes:

- Companion plan (`025-PP-PLAN-j-rig-keeper-pretrip-evidence-2026-05-26.md`)
- All 8 active Decision Records (010-018 series, j-rig brand canon)
- Blueprint A + Blueprint B + canonical glossary
- Kernel-shadow inventory (`016-RR-LAND`) + shape reconciliation addendum (`017-RR-LAND`)
- Current bd state snapshot: `bd export --filter status=open > brief-pack/bd-open-snapshot.jsonl`
- Per-repo CI workflow snapshot
- Current state section from umbrella `CLAUDE.md`

Brief pack lives at `intent-eval-lab/000-docs/audit/2026-MM-DD-brief-pack/` (date pinned at kickoff).

### Phase 2 — Cohort A engineering audit (parallel, ~1 session per seat)

Each engineering seat reads the brief pack, runs lane-specific tools (e.g., `bd doctor`, `gh repo view` across all 5 repos, `jq` over schemas), writes findings into `intent-eval-lab/000-docs/audit/2026-MM-DD-engineering-findings-A<N>.md`.

Findings format:

```markdown
| ID | Severity | Lane | Finding | Evidence | Recommendation |
|---|---|---|---|---|---|
| A1-1 | MAJOR | 3 | <one-sentence finding> | <link/quote> | <suggested fix> |
```

### Phase 3 — Cohort B thinker-canon audit (parallel, ~1 session per seat)

Same brief pack; each thinker-canon seat applies their bias. Each finding cites the thinker canon source (page/paper/talk timestamp). Findings format identical to Phase 2 + a `Canonical citation` column.

### Phase 4 — Synthesis + ISEDC ratification (1 session)

Acting CTO reads both cohorts' findings, identifies:

- **High-signal overlap**: same root finding from engineer + thinker. These are the highest-priority remediation items.
- **High-signal divergence**: engineer says A; thinker says B. These reveal a hidden tradeoff worth surfacing to user.
- **Single-source findings**: only one cohort flagged. Tagged by severity; lower confidence but still tracked.

Synthesis doc at `intent-eval-lab/000-docs/audit/2026-MM-DD-audit-synthesis.md`. Convene ISEDC Session 8 (or whatever the next number is) to ratify the remediation plan. DR filed per existing pattern.

### Phase 5 — Remediation epic + beads filed (1 session)

Each ratified remediation becomes a bead under a new "j-rig + IEP audit remediation" epic. Severity-tagged priority (BLOCKER=P0, MAJOR=P1, MINOR=P2, NIT=P3). Dependencies linked. The remediation epic gets its own brief pack so it can be audited later (recursive auditability — see Phase F triggers).

## Tooling options — what runs the panel

User direction 2026-05-26: surveys vLLM (https://github.com/vllm-project/vllm) and Hugging Face ml-intern (https://github.com/huggingface/ml-intern) as candidate substrates. Plus survey the broader market for similar agent-orchestration tools.

| Option | What it is | Fit for this audit | Cost | Sovereignty |
|---|---|---|---|---|
| **Anthropic Claude (current default)** | The Claude API + Claude Code subagents we already use | HIGH — 13 thinker-canon reviewer agents already exist at `~/.claude/agents/`; Claude Code subagent invocation is the proven path | $$$ per token (Opus/Sonnet for the panel work) | Anthropic-hosted; data does not leave Anthropic |
| **vLLM + open model (Llama 3.1 70B, Qwen 2.5 72B, DeepSeek-V3, etc.)** | Self-hosted high-throughput LLM inference server. Runs OSS models locally/on-prem | MEDIUM — the engineering audit lanes (1, 3, 5) are content-grounded enough that a strong OSS model could plausibly produce comparable findings. The thinker-canon biases (B1-B5) need careful prompting to channel the persona faithfully; OSS models may default to generic critique rather than thinker-grounded critique. Requires local GPU (24GB+ VRAM for 70B-class quantized; A100/H100 for full-precision) | $ infrastructure-only; no per-token costs | Self-hosted; full data sovereignty |
| **Hugging Face ml-intern** | Autonomous research agent from HF (per user link; specific capability needs investigation in Phase 1 brief pack assembly) | UNKNOWN until investigated — could be a fit for the parallelization (each seat runs concurrently) but specific orchestration pattern not yet confirmed | Unknown | Likely HF-hosted; check posture |
| **Anthropic Computer Use / Agent SDK alternatives** | OpenAI Operator, Devin, Cognition, etc. | LOW — these tools optimize for browser/computer-using agents, not for structured-document audit. Mismatch for this use case. | Varies | Provider-hosted |
| **Hybrid (Anthropic for thinker canon + vLLM for engineering lanes)** | Use Claude for B1-B5 (where persona fidelity matters most) + self-hosted OSS model for A1-A5 (where the work is grounded in artifact-reading + finding-format-filling) | HIGH if the GPU infrastructure exists | $$ ($ for OSS hosting + $$ for Anthropic thinker calls) | Mixed; thinker findings touch Anthropic, engineer findings stay local |

**Phase 1 brief-pack assembly must include**: investigation of ml-intern's actual orchestration model (read its README + look for example use cases) so the Phase 2/3 cohorts can be wired up correctly if the hybrid model is chosen.

**Recommendation (CTO read)**: start with Anthropic-only for first audit (proven path; the 13 thinker-canon agents already exist; no GPU procurement). Re-evaluate hybrid after first audit's cost data lands.

## Deliverable shape

After Phase 5, the durable artifacts are:

1. `intent-eval-lab/000-docs/audit/2026-MM-DD-brief-pack/` — what the panel read
2. `intent-eval-lab/000-docs/audit/2026-MM-DD-engineering-findings-A{1..5}.md` — Cohort A findings
3. `intent-eval-lab/000-docs/audit/2026-MM-DD-thinker-findings-B{1..5}.md` — Cohort B findings (with citations)
4. `intent-eval-lab/000-docs/audit/2026-MM-DD-audit-synthesis.md` — overlap + divergence analysis
5. `intent-eval-lab/000-docs/NNN-AT-DECR-isedc-session-N-audit-remediation-2026-MM-DD.md` — ratified remediation
6. bd workspace: new "j-rig + IEP audit remediation" epic + children, severity-tagged

The audit doc cluster lives in `audit/<date>/` so subsequent audits don't overwrite. Each audit gets its own date-pinned folder.

## Cadence

- **First audit**: triggered by this plan (immediate; tactically blocks on the j-rig Keeper Epic 1 closing OR on Phase 1 brief-pack being readable, whichever comes first)
- **Recurring audits**: quarterly (every 12 weeks) OR event-triggered when (a) a new repo joins the IEP, (b) a new DR ratifies an architecturally-rippling change, (c) ≥3 BLOCKER findings accumulate without remediation, (d) a partner reports a structural concern
- **Lightweight micro-audits**: per-PR Gemini reviews + per-release /release ceremony validate ongoing state; full audits catch what micro-audits cannot see

## Risks + mitigations

| Risk | Mitigation |
|---|---|
| Panel finds so much drift that remediation becomes its own quarter-long project | Sever findings by severity. BLOCKER + MAJOR ship inside 2 weeks (firefighting). MINOR + NIT get filed but live in the backlog. Audit doesn't expand scope; it surfaces. |
| Thinker-canon reviewers parrot generic critique instead of channeling their thinker | Each finding REQUIRES a canonical citation column. Findings without verifiable citation get rejected at Phase 4 synthesis. The 13 existing thinker-reviewer agents have proven this constraint works (bd-remember entry references 9+ P0/P1 surfaced from 6-seat panel on 2026-05-26). |
| Panel disagreements paralyze decisions | ISEDC Session at Phase 4 has acting head of board who decides. Verbatim positions preserved. No consensus-forming pressure during cohort phases. |
| User runs out of patience reading 10 finding docs + a synthesis | Synthesis doc is the user-facing artifact. Individual seat findings are appendix. One synthesis page → one decision page → action. |
| Audit cost runs away on Anthropic API | Use Haiku for the bulk Phase 2/3 reading; Sonnet for the synthesis; Opus only if a specific finding demands the deeper read. Budget cap: ~$50 per full audit cycle (estimate; first audit will produce real number). |
| Audit becomes performative — finds nothing because nothing was wrong | OK outcome. Audit produces a "ratified-clean" DR. The point of audits is the option value; finding nothing IS a finding. |

## Exit criteria

1. Phase 1 brief pack assembled and readable by both cohorts
2. Phase 2 + 3 produce findings docs from all 4-5 seats per cohort (parallel sessions)
3. Phase 4 synthesis doc identifies overlap + divergence + recommendations
4. Phase 5 ISEDC Session N ratifies the remediation plan; DR filed
5. Remediation epic + children filed in bd with severity-mapped priorities; cross-linked to PR(s) when remediation work ships

## Stopping criteria

- Brief-pack assembly reveals the system is too small to warrant a panel audit → skip to a single CTO-led review (would be surprising given current size)
- Phase 2 + 3 produce zero findings across all 9-10 seats → audit pauses; defer next audit to next quarter
- A remediation BLOCKER is found that's actually a bug, not a structural issue → bypass the rest of the audit, file urgent bead, fix immediately, resume audit afterward

## What this plan does NOT do

- Does not execute the audit. Plan mode. Execution begins at Phase 1 brief-pack assembly (separate session).
- Does not pick the tooling substrate (Anthropic-only vs hybrid). Recommendation in § Tooling but final call deferred to Phase 1 kickoff.
- Does not define the specific GPU/infra needed for vLLM if hybrid chosen. That's Phase 1 prereq.
- Does not commit to a recurring cadence beyond the first audit. Cadence decision happens after the first audit's value is observed.
- Does not enumerate every finding template field. The 5-section format above is a starting point; refine in Phase 1.
- Does not address Tier-2 research projects (semantic-flux, future research). Their methodology oversight is separate.

## Companion artifacts

- Plan being audited: `025-PP-PLAN-j-rig-keeper-pretrip-evidence-2026-05-26.md`
- Existing thinker-canon reviewer agents: `~/.claude/agents/<thinker>-reviewer.md` (13 agents per bd-remember)
- Recent precedent panel: "AA-AACR-thinker-panel-review-2026-05-25" (`023-AA-AACR-thinker-panel-review-2026-05-25.md`) — surfaced 9+ P0/P1 findings + Beck #1 j-rig CI root cause + Gregg #2 OTel semconv gap that gates v0.2.0 kernel
- ISEDC pattern: `/exec-decision-council` skill at `~/.claude/skills/exec-decision-council/`

---

- Jeremy Longshore
intentsolutions.io
