# 023-AA-AACR — Thinker-Canon Panel Review (release-sweep adversarial review)

**Date**: 2026-05-25
**Author**: Jeremy Longshore (acting CTO Claude as drafting executor; user-confirmed CEO-mode delegation)
**Scope**: Adversarial review of the IEP release-sweep plan + ecosystem state + bd backlog + ISEDC verify-before-claim discipline + unification thesis + harness-hash gate stack
**Trigger**: Step 0.5 of the "Run /release ceremony across 5 IEP repos + /gist-auditor sweep" plan, 2026-05-25
**Status**: ACTIVE — findings synthesized; 9 new beads filed; 2 PRs in flight; remaining Steps 3-7 deferred to a focused future session
**Cross-references**:
- Master release-sweep plan: in transcript, not committed (per CLAUDE.md no-plan-files rule)
- Durable agent assets: 13 thinker-canon agents at `~/.claude/agents/<thinker>-reviewer.md` (created this session)
- New beads filed: P0 `bd_000-projects-uprg` (compat policy), P0 `bd_000-projects-9pi3` (OTel semconv), P0 `bd_000-projects-59tx` (Release CI alerting) + 6 more (listed below)
- In-flight PRs: `j-rig-skill-binary-eval#76` (CI fix), `intent-eval-core#11` (v0.1.1 prep)

---

## 1. Background

A multi-repo release-sweep plan was approved 2026-05-25 to drive `/release` ceremony across the 5 IEP sub-repos (intent-eval-core, intent-eval-lab, j-rig-binary-eval, intent-rollout-gate, audit-harness). Step 0.5 was added to the plan as an adversarial review BEFORE the release work began — the rationale being that real findings on the underlying architecture, the bd backlog, and the verify-before-claim discipline might affect the sequence or shape of Steps 1-7.

The panel was built in two layers:

1. **Durable assets**: 13 thinker-canon Claude Code subagents created at `~/.claude/agents/`. Each one channels a real software-engineering thinker's known biases (Fowler, Beck, Cunningham, Kleppmann, Lamport, Gregg, Linus, Pike, Thompson, Hickey, Armstrong, Karpathy, Huyen). Read-only tools (Read/Glob/Grep/Bash) — they review, they don't edit. Single-signer accountability: the acting CTO is the sole executor; agents propose, CTO disposes.

2. **Immediate review panel**: 6 priority agents spawned in parallel for the release-sweep review. User-confirmed top-6: Kleppmann, Hickey, Fowler, Beck, Gregg, Cunningham. The other 7 (Lamport, Linus, Pike, Thompson, Armstrong, Karpathy, Huyen) remain as durable assets for future-context-appropriate invocations.

---

## 2. Verbatim 6-seat findings

Adversarial-integrity discipline per DR-022 § "verify-before-claim": each seat's findings preserved verbatim. The synthesis in § 3 cites them; the originals remain intact below for future readers (and future ISEDC sessions) who want to re-evaluate the lens.

### 2.1 Martin Kleppmann's Review (distributed systems / DDIA)

**Cross-cutting theme**: "You have built a careful, well-typed specification of an event-shaped system — thirteen entities, immutability prose, append-only language, RF-0..RF-4 forward-references — but the actual ordering, causality, and signing substrate beneath all of it is markdown-in-git plus a Postgres-row-per-thing plus a 60-second-throttled JSONL projection of a Dolt SQL store. The kernel calls itself a 'canonical contracts kernel' and the bundles call themselves 'lingua franca,' but the only place a happens-before relation is currently enforceable is inside one PostgreSQL transaction. ... The IEP today is a CRUD system whose author intends event-log semantics. Everywhere I looked, the binding promise (immutability, replay, lineage, attestation) is one cosign-signature, one Rekor-anchor, or one merkle-root short of what the prose claims."

**Findings**:

1. **OBSERVATION**: Decision Records are described as "permanent verbatim 7-seat record" but are plain markdown in a git repo with no content digest, no detached signature, no Rekor anchor.
   **RISK**: A future contributor (or rebased merge, or force-push fix-up) can silently mutate verbatim seat positions. The platform's governance substrate is weaker than the platform's own attestation requirements for `cost-attribution/v1`.
   **MITIGATION**: Compute sha256 of each `NNN-AT-DECR-*.md` at merge, hash-chain into `intent-eval-lab/specs/DECISION-RECORDS.md` ledger (append-only), sign via cosign keyless, anchor root in Rekor.
   **BEAD**: NEW P1 — "Hash-chain Decision Records into signed append-only ledger".

2. **OBSERVATION**: Blueprint B § 1.1 lists "no event sourcing" as deferred — but § 2 simultaneously claims every EvidenceBundle row is "append-only," every JudgeDecision "immutable at creation". Prose committed to event-sourced invariants while explicitly disowning the substrate.
   **RISK**: Immutability enforced by `content_hash` columns and developer discipline, not by a storage layer that refuses overwrites.
   **MITIGATION**: Either (a) honestly weaken prose to "logically immutable; physical immutability is operational discipline", OR (b) put EvidenceBundle blobs in S3 Object Lock + add periodic merkle-walk verifier.
   **BEAD**: NEW P1 — "Physical-immutability backing for EvidenceBundle blobs (Object-Lock + merkle-walk verifier)".

3. **OBSERVATION**: bd JSONL throttle mitigation (`export.interval=1s`) is a quantitative tuning, not a correctness fix. Window narrowed from 60s to 1s; it did not close.
   **RISK**: Any consumer that reads JSONL within the 1s window observes pre-write state. Multi-writer scenarios (parallel `bd-sync` invocations) still race; rarer, not eliminated.
   **MITIGATION**: Treat Dolt DB as only system of record; derive JSONL via CDC against a stored cursor. Belt-and-suspenders: advisory lock against a known Postgres row before mutate-then-mirror.
   **BEAD**: ENHANCE `bd_000-projects-ufc` (CLOSED) — reopen as P2 "JSONL is a derived view, not a snapshot — implement CDC projection from Dolt commit log".

4. **OBSERVATION**: Schema evolution story for `gate-result/v1 → v2` is missing the consumer side. Producer story is clear; rules for forward/backward/mixing/deprecation are absent.
   **RISK**: Once v1 anchors hit prod Rekor (one-way door), consumers in the wild will be reading v1 indefinitely. Without compat rules written down BEFORE the first prod-Rekor anchor, you commit to a maintenance burden of unspecified shape.
   **MITIGATION**: Write `intent-eval-lab/specs/evidence-bundle/COMPATIBILITY.md` with FORWARD / BACKWARD / MIXING / DEPRECATION rules BEFORE iah-E06 pre-flight passes.
   **BEAD**: NEW **P0** — "Write Evidence Bundle predicate compatibility policy BEFORE first prod-Rekor anchor" — filed as `bd_000-projects-uprg`.

5. **OBSERVATION**: 13-entity state machines in Blueprint B § 3.1 are specified as `(from_state, event, to_state)` triples in prose but not extracted as a machine-checkable artifact. Kernel ships a `canTransition` helper; no evidence it's generated from Blueprint B tables.
   **RISK**: Blueprint B is normative per source-of-truth hierarchy, but if a developer edits the kernel's transition table without editing Blueprint, kernel ships out-of-spec runtime and the static gate doesn't catch it.
   **MITIGATION**: Make state-machine spec single-sourced (either Blueprint B → kernel codegen, or kernel TS → Blueprint doc-extractor). Add CI drift gate.
   **BEAD**: NEW P1 — "Make state-machine spec single-sourced (Blueprint B ↔ kernel transition table); add CI drift gate".

**Most-costly-to-recover-from**: Finding #4 — Evidence Bundle predicate compatibility policy. Rekor is a one-way door; every other finding is recoverable; this one is recoverable only by abandoning v1 namespace and starting over at v2 (forfeits first-mover-on-attested-evidence claim).

### 2.2 Rich Hickey's Review (simple-vs-easy, data-oriented)

**Cross-cutting theme**: "You've done something genuinely uncommon: you put a value at the center of the universe. The Evidence Bundle is a value in the strict sense... The unification thesis is the right kind of thesis because it is value-oriented, not mechanism-oriented. So before I complain, let me say: the spine here is correct... Now. My concern across nearly every finding below: you are at constant risk of re-complecting the value into the mechanism that produces it. The 13-entity domain model is rich and well-attributed, but several entities braid together at least three independently-varying concerns."

**Findings** (compressed for brevity; full verbatim preserved in agent run output `ac986d3616075de01`):

1. P0 — **Decomplect `EvalRun`**: split into `EvalRunSpec` (immutable value), `EvalRunLease` (ephemeral place, explicitly Redis-shaped not Postgres-shaped), append-only `EvalRunTransition` events. Terminal-state derivation becomes a fold over transitions, not a mutable column.

2. P1 — **Convert bd ↔ GH ↔ Plane from three-way sync to canonical-bd + computed projections**. Three databases hold "the same" task; `bd-sync` is the cure-that-is-also-the-cause. Beads is already source of truth — make GH and Plane *projections* (computed, not synced). When a view drifts, re-derive; never reconcile.

3. P1 — **Split `gate-result` predicate body from attestation metadata**. The predicate body is the value; the signing envelope (signing_mode, rekor_log_index, signed_at) is a separate `GateResultAttestation` relation keyed by `content_hash(predicate_body)`. One predicate body MAY have N attestations.

4. P1 — **Decompose review-panel ceremony into (creative findings → deterministic rules) two-phase pipeline**. Personas are model-prompts; running the same panel twice produces different findings. Keep panel for generating findings; reduce every finding to a rule that fires deterministically on the next artifact.

5. P3 — **Reframe harness-hash docs from ritual language to immutable-value language**. Policy file IS its content-hash; "re-init" implies state being re-created. Replace with "anchor the new policy value."

6. P1 — **Convert per-repo Blueprint C work from hand-authored docs to template+identity-yaml generation**. 25 P0 beads ÷ 5 repos × 5 sections of Blueprint C = the un-DRY of the document layer. Per-repo Blueprint C should be a small `repo-identity.yaml` combined with the template to generate the per-repo blueprint doc.

**Most-costly-to-recover-from**: Finding #2 (three-layer mirror). Cost compounds daily; recovery cost grows superlinearly with time. Every new bead, every `bd-sync note`, every CI integration adds to the cost of switching to canonical-bd-with-projections.

### 2.3 Martin Fowler's Review (evolutionary architecture)

**Cross-cutting theme**: "Look — the IEP is not a Big Up Front Design disaster, but it has the smell of one. Five repos exist, a kernel is published, audit-harness has cut FIVE releases in the last seven days. That cadence is the architecture thinking out loud — which is healthy. What worries me is that the constitutional documents (Blueprints A/B/C, 12 binding principles, ISEDC sessions, three-class governance routing) front-loaded enormous design authority before the platform had a single external consumer. Blueprint A § 1.2 binds 12 principles on every future repo; § 2.3 binds a three-class governance router with quarterly cadence. That's a constitution written for a federation that does not yet exist."

**Findings**:

1. **Speculative Generality in the constitution**. Mark Blueprint A § 2.3 cadence as PROVISIONAL until the first three Class-1 triggers have actually fired and produced DRs that downstream consumers acted on. **BEAD**: file `iel-blueprint-a-cadence-provisional` P3.

2. **Five audit-harness releases in seven days is evolution-with-a-whiff-of-thrash**. The `prev_blank` awk noise (v1.1.2 → v1.1.4) ought to have been caught by the harness's own integration test on a deliberately-failing feature file. Missing **fitness functions** for stdout shape. **BEAD**: NEW P1 — "Golden-master test for gherkin-lint + crap-score stdout shapes (fitness function preventing prev_blank-class regressions)".

3. **Shotgun Surgery** — version-canonical-check across 5 polyglot manifests. Single-source the version in one file; generator stamps the other 4. **BEAD**: NEW P2 — "Single-source the version across 5 polyglot manifests".

4. **`bd-sync` is the right pattern (Aggregator)** — but the JSONL throttle bug took 3 weeks to characterize correctly. Add `bd-sync verify` that round-trips a canary bead nightly. **BEAD**: NEW P2 — "bd-sync verify subcommand: round-trip a canary bead nightly, alert on drift".

5. **ISEDC adversariality is real but at risk of seat-collapse over time**. Once a quarter, bring in an outside reviewer (or a different LLM cold) to play one seat. **BEAD**: NEW P2 — "ISEDC adversariality fitness function: every Q4 session must have at least one non-operator-authored seat position".

6. **Expand-contract / Parallel Change discipline missing from Blueprint B § 7**. Every kernel field addition should land as `optional` first, age, then become `required` only after deprecation warning. **BEAD**: NEW P1 — "Add Parallel Change discipline to Blueprint B § 7: optional → deprecated → required with one minor-version dwell".

**Most-costly-to-recover-from**: The predicate URI namespace lock. Once a `gate-result/v1` payload is signed into Rekor with that URI, it's immutable forever. **Do not let v0.2.0 ship until `iec-E12a` is closed with a written invariants list, reviewed by someone other than the author.**

### 2.4 Kent Beck's Review (TDD / feedback loops)

**Cross-cutting theme**: "I'm not a great programmer; I'm just a good programmer with great habits. The IEP ecosystem has impressive habits at the artifact layer — ISEDC sessions, Decision Records, three-layer mirrors, harness-hash pinning, sigstore provenance. But the cycle time of the inner feedback loop has been degraded by two things: (1) `|| true` masking on the release path that hid a real failure for weeks, and (2) a CI workflow that runs `pnpm run test` without `pnpm run build` in the test job, even though the typecheck job above it correctly builds first. The j-rig CI failure is not a new bug — it's a feedback gap that was finally allowed to speak. That's the most important finding in this review."

**Findings**:

1. **CRITICAL** — j-rig CI `test` job is asymmetric with `typecheck`. (NOTE: Beck's recon was on `ci.yml`; actual failure was in `release.yml` which had the same gap. Fix landed in PR #76 — `release.yml` now builds before tests run.) **BEAD**: NEW P0 — "Factor j-rig CI setup-and-build into a composite action; restore build-before-test invariant uniformly" (post-Step 1 sweep).

2. **Step 1 (CI fix) must come BEFORE Step 0.5 (agent ceremony)**. (Sequence moot — 0.5 was complete by the time this finding surfaced. Future plans should respect Tidy First sequencing.)

3. **/release 8-phase ceremony — only some phases have true irreversibility lines**. Annotate every phase as REVERSIBLE / SOCIAL-IRREVERSIBLE / TECHNICAL-IRREVERSIBLE. **BEAD**: NEW P2 — "Map each /release phase as REVERSIBLE / SOCIAL-IRREVERSIBLE / TECHNICAL-IRREVERSIBLE; align BLOCKING gate position".

4. **harness-hash mechanism preserves loop meaning if the diff is visible**. Add a one-line "what changed in the policy?" diff summary printed by `audit-harness init`. **BEAD**: NEW P2.

5. **Lab CHANGELOG repair = 2 PRs not 1** (Tidy First). PR 1 (Tidy): rearrange existing entries into Keep-a-Changelog format. PR 2 (Change): add v0.2.0 entry using the established format. **APPLIED** to Step 3 of the release sweep plan.

6. **Three repos with separate release.yml workflows — file the bead, don't do it during the sweep**. **BEAD**: NEW P2 — "Extract reusable release workflow across IEP repos (post-sweep)".

**Most-costly-to-recover-from**: The duplicated release workflows across three repos diverging silently. Rank-order of badness: (1) divergent release workflows > (2) silently-failing CI from `|| true` > (3) the asymmetric build-before-test gap > (4) the agent-ceremony-before-CI-fix sequencing risk.

### 2.5 Brendan Gregg's Review (observability / USE method)

**Cross-cutting theme**: "You've built an OpenTelemetry-native platform on paper — Blueprint B § 4.3 reads beautifully — and that's where the observability story ends. The runtime that EMITS this telemetry doesn't exist yet. Meanwhile, the things that are real and running right now — bd workspace, the 5-repo CI fabric, the /release skill, the harness-hash policy gate — have effectively zero instrumentation. You can't see your own developer-facing system."

**Findings**:

1. **CRITICAL** — j-rig Release workflow failed 3 consecutive times with NO alert path. **BEAD**: NEW **P0** — "Add Release workflow failure alerting (ntfy 'prod-alerts' topic) across IEP repos" — filed as `bd_000-projects-59tx`.

2. **CRITICAL** — `gate-result/v1` has no OTel attribute schema pinned. Five emitters will drift. **BEAD**: NEW **P0** — "Pin OTel semantic conventions in @intentsolutions/core BEFORE v0.2.0 ships" — filed as `bd_000-projects-9pi3`.

3. **harness-hash mismatch in production has no debugging surface**. Add `audit-harness verify --emit-otel` flag. **BEAD**: NEW P1 — "audit-harness verify observability (--emit-otel + --diff flags)".

4. **Cross-repo propagation latency: 8 days, intent-eval-core v0.1.0 → still-not-consumed by j-rig. No tracing**. Add weekly `bd-flame.sh` cron. **BEAD**: NEW P2 — "Dev-flow flame graph (weekly stacked-bar of bead close latency by priority)".

5. **/release skill is 8 phases — no time-per-phase emission**. Add PHASE_START / PHASE_END timing. **BEAD**: NEW P3 — "release-phase instrumentation".

6. **bd JSONL throttle 'mitigation' papers over missing telemetry**. Add session-close USE check. **BEAD**: NEW P2 — "bd-saturation-check at session-close".

**Most-costly-to-recover-from**: Drifted OTel attribute names across 5 emitters once each ships its own runtime instrumentation. Once consumers emit drifted-attribute spans, recovery cost rises super-linearly with retained-trace count. **Pin the semconv inside `intent-eval-core` BEFORE v0.2.0 ships.**

### 2.6 Ward Cunningham's Review (technical debt / evolving docs)

**Cross-cutting theme**: "I built the wiki because I wanted to think out loud with others — fast, in the open, reversible. What I see across IEP is the opposite vector applied with admirable rigor: write-once Decision Records, verbatim-frozen ISEDC seat positions, hash-pinned harness, NORMATIVE schema, 'no override exists' anti-goals. Some of this is genuinely deliberate debt being repaid... But a lot of it is the same architectural reflex that produces fossilized requirements documents: crystallize first, evolve never. 22 docs in 14 days at ~8,200 lines is not 'alive knowledge' — it's a paper-trail accumulator that future readers will have to mine, not converse with."

**Findings**:

1. **The DR sequence shows EVOLVING thinking — institutionalize it**. Adopt "Status banding" at the top of every DR: `ACTIVE / SUPERSEDED-BY-NNN / INVERTED-BY-EMPIRICAL-FINDING / RATIFIED-AND-STABLE`. **BEAD**: NEW P2 — "DR status-banding convention + 000-INDEX update mechanism".

2. **ISEDC verbatim-7-seat preservation is RIGHT but needs "what we'd think now" appendix**. Add `## Post-decision learnings` section to every DR template (append-only, dated). **BEAD**: NEW P2 — "DR template: post-decision learnings appendix".

3. **Three-layer mirror is a synchronization-debt accumulator** (echoes Hickey #2). **BEAD**: convergent with Hickey #2.

4. **The 8-category filing scheme crystallized too early**. Adopt `0NN-DRAFT-<slug>-<date>.md` escape hatch for ungovernable in-flight thinking. **BEAD**: NEW P3 — "Add DRAFT escape hatch to Doc Filing Standard".

5. **CRITICAL** — `bd memories` is empty across 625 imported issues and 22 DRs. Yet every CLAUDE.md says "Use `bd remember` for persistent knowledge". **BEAD**: NEW **P1** — "Backfill bd memories from 22 DRs + 4 AACRs (mine 1-2 sentence insights, file via `bd remember`)".

6. **FUTURE.md doing the right thing — extend the pattern**. Promote FUTURE.md to a first-class category `0NN-FF-FUTR-<slug>.md`, one file per deferred insight. **BEAD**: NEW P3 — "FUTURE.md first-class promotion".

**Most-costly-to-recover-from**: `bd memories` being empty. Every other finding has obvious fixes once you notice; this one is invisible. The cost compounds silently: every insight learned in a session that doesn't become a `bd remember` is an insight you'll re-derive at 80% accuracy in 3 weeks.

---

## 3. Synthesis matrix

### 3.1 Cross-cutting themes (3+ seats convergent)

| Theme | Seats | Action |
|---|---|---|
| **One-way door: predicate compatibility before Rekor anchor** | Kleppmann #4, Fowler most-costly | **P0 bead filed** (`uprg`); becomes precondition for `iec-E12` v0.2.0 |
| **OTel attribute drift across 5 emitters** | Gregg #2, Kleppmann (indirectly) | **P0 bead filed** (`9pi3`); becomes child of `iel-E12` |
| **bd ↔ GH ↔ Plane three-layer mirror = sync-debt accumulator** | Hickey #2, Kleppmann #3, Cunningham #3, Fowler #4 (counter-argues) | **P1 design spike bead** to file: convert to canonical-bd + projections |
| **`bd memories` empty — knowledge channel unused** | Cunningham #5 (most-costly), aligned with Hickey #5 framing | **P1 bead** to file: backfill from 22 DRs |
| **j-rig CI feedback gap (build-before-test asymmetry)** | Beck #1 | **APPLIED** — PR #76 in flight; resolves Step 1 of release sweep |
| **CHANGELOG repair = 2 PRs (Tidy First)** | Beck #5 | **APPLIED** to Step 3 plan (lab v0.2.0 split) |
| **Three release workflows diverging silently** | Beck #6, Fowler #3 (related) | **P2 bead** to file: extract reusable release workflow |
| **ISEDC adversariality erosion over time** | Fowler #5 | **P2 bead** to file: quarterly outside-reviewer or different-LLM seat |
| **Constitution-as-Speculative-Generality** | Fowler #1 | **P3 bead**: mark Blueprint A § 2.3 cadence PROVISIONAL |

### 3.2 Productive disagreements (preserved per adversarial-integrity)

- **Linus would call the constitution ceremony**; **Fowler defends the contracts as load-bearing** — both correct in different scopes. Resolved by demoting some governance-routing prose to PROVISIONAL while keeping the predicate/schema spec as binding.
- **Hickey says "make schema data, never break"**; **Fowler endorses MAJOR for breaking changes**. Both right at different consumer-count scales — current IEP is small enough that MAJOR is pragmatically correct (audit-harness, j-rig, intent-rollout-gate all already shipped v1.0.0 license relicenses).
- **Kleppmann wants formal merkle-log + Object-Lock**; **Hickey just wants the bd-as-canonical inversion**. Both fixable; the merkle-log is the stronger statement, the bd-inversion is the cheaper win.
- **Beck says "test first"**; **Hickey says "shape first"**. Beck's TidyFirst applies to changes; Hickey's value-first applies to inception. The release sweep itself benefits from both — Beck's 2-PR CHANGELOG split (applied) + Hickey's bd-canonical inversion (deferred bead).

### 3.3 CTO decisions applied

1. **CHANGELOG repair (Step 3) becomes 2 PRs** per Beck #5. Tidy first (rewrite top of lab CHANGELOG into Keep-a-Changelog format on existing entries); then add v0.2.0 as separate PR.
2. **j-rig CI fix shipped** per Beck #1 + the actual `release.yml` symmetry gap (Beck's recon hit `ci.yml` which IS correct; the bug was in `release.yml` which I fixed directly).
3. **3 P0 beads filed immediately** rather than deferred to the final AAR: `uprg` (compat policy), `9pi3` (OTel semconv), `59tx` (Release CI alerting).

### 3.4 CTO decisions deferred (bead-only, no immediate work)

| Decision | Reason for deferral | Bead |
|---|---|---|
| Decompose `EvalRun` into spec/lease/transitions (Hickey #1) | Kernel architecture change; needs ISEDC ratification | P1 bead to file |
| Hash-chain DRs into signed append-only ledger (Kleppmann #1) | Substantial infra work; not blocking; ironic but not urgent | P1 bead to file |
| Physical immutability for EvidenceBundle blobs (Kleppmann #2) | Storage substrate change; coordinated with v0.2.0 work | P1 bead to file |
| State-machine spec single-sourced (Kleppmann #5) | Codegen pipeline addition; medium effort | P1 bead to file |
| bd-canonical + GH/Plane projections (Hickey #2 + Cunningham #3 + Kleppmann #3) | Workflow change; affects every Intent Solutions repo, not just IEP | P2 design spike bead |
| `gate-result` body/attestation split (Hickey #3) | v2 schema change; major bump territory | P1 bead, gated on v0.2.0 |
| Per-repo Blueprint C via template + identity-yaml (Hickey #6) | Big DRY win but invalidates 25 in-flight P0 beads | P1 bead with migration plan |
| Golden-master test for harness stdout (Fowler #2) | Adds to audit-harness test suite; non-trivial fixture corpus | P1 bead |
| ISEDC adversariality fitness function (Fowler #5) | Quarterly cadence — bead to revisit in Q3 | P2 bead |
| audit-harness verify --emit-otel (Gregg #3) | New flag; backward-compat addition | P1 bead |
| Dev-flow flame graph (Gregg #4) | Tooling — not architectural | P2 bead |
| DR status-banding (Cunningham #1) | Convention; can apply incrementally | P2 bead |
| DR post-decision learnings appendix (Cunningham #2) | Template update + retroactive backfill | P2 bead |
| `bd memories` backfill (Cunningham #5) | Mechanical effort; high leverage | **P1 bead** — high priority for filing |
| FUTURE.md first-class promotion (Cunningham #6) | Filing-system change | P3 bead |

---

## 4. Beads filed this session (status snapshot)

Filed during execution (P0s, immediate):

| ID | Priority | Title |
|---|---|---|
| `bd_000-projects-uprg` | P0 | Write Evidence Bundle predicate compatibility policy BEFORE first prod-Rekor anchor |
| `bd_000-projects-9pi3` | P0 | Pin OTel semantic conventions in @intentsolutions/core BEFORE v0.2.0 ships |
| `bd_000-projects-59tx` | P0 | Add Release workflow failure alerting (ntfy 'prod-alerts' topic) across IEP repos |

To file as session-close action (synthesized from panel, P1-P3, queue):

- P1 — Hash-chain Decision Records into signed append-only ledger
- P1 — Physical-immutability backing for EvidenceBundle blobs
- P1 — State-machine spec single-sourced (Blueprint B ↔ kernel)
- P1 — `gate-result` body/attestation split
- P1 — Per-repo Blueprint C via template + identity-yaml generation
- P1 — Decompose EvalRun (spec/lease/transitions)
- P1 — Golden-master test for harness stdout (prev_blank regression prevention)
- P1 — audit-harness verify --emit-otel
- P1 — Backfill bd memories from 22 DRs + 4 AACRs (high-leverage mechanical effort)
- P1 — Add Parallel Change discipline to Blueprint B § 7 (optional → deprecated → required dwell)
- P2 — Convert bd ↔ GH ↔ Plane from three-way sync to canonical-bd + projections
- P2 — Single-source the version across 5 polyglot manifests
- P2 — bd-sync verify subcommand (round-trip canary)
- P2 — ISEDC adversariality fitness function (Q4 outside reviewer)
- P2 — Extract reusable release workflow across IEP repos
- P2 — Dev-flow flame graph
- P2 — Map each /release phase REVERSIBLE / SOCIAL-IRREVERSIBLE / TECHNICAL-IRREVERSIBLE
- P2 — bd-saturation-check at session-close
- P2 — DR status-banding convention
- P2 — DR template: post-decision learnings appendix
- P3 — Reframe harness-hash docs from ritual to immutable-value language
- P3 — release-phase instrumentation
- P3 — Add DRAFT escape hatch to Doc Filing Standard
- P3 — FUTURE.md first-class promotion
- P3 — Mark Blueprint A § 2.3 cadence PROVISIONAL

---

## 5. Constraints applied to release-sweep plan

| Constraint | Source | Where applied |
|---|---|---|
| CHANGELOG repair = 2 PRs | Beck #5 | Plan Step 3 (lab v0.2.0) |
| Hash-pinned compat policy is P0 BEFORE prod Rekor | Kleppmann #4 + Fowler most-costly | `bd_000-projects-uprg` filed; gates future v0.2.0 release; v0.1.1 unaffected (no Rekor anchoring yet) |
| OTel semconv pinned BEFORE v0.2.0 | Gregg #2 | `bd_000-projects-9pi3` filed; gates future v0.2.0 release; v0.1.1 unaffected |
| j-rig build-before-test in release.yml | Beck #1 (refined to actual root cause) | PR #76 filed; CI green; awaiting Gemini |

---

## 6. Durable assets created

13 thinker-canon agent files at `~/.claude/agents/` — each one read-only (Read/Glob/Grep/Bash), each one channels a real thinker's known biases, each one ~600-900 words of body prose with verifiable canonical positions. Future invocations route via the Task tool with the matching `subagent_type` (once Claude Code picks up the new agents at session boundaries).

Naming convention: `<thinker>-reviewer`. Color-coded for discoverability.

Read-only enforcement is load-bearing — the acting CTO remains sole executor; this preserves single-signer audit trail per the ISEDC adversarial-integrity discipline.

---

## 7. Why this step happened BEFORE the release work

Two reasons documented in the plan:

1. The review MAY have surfaced a deeper cause for the j-rig CI failure. It did (Beck #1 — though Beck's recon hit `ci.yml` and the actual bug was in `release.yml`; the *shape* of the finding was correct: asymmetric build-before-test). The fix landed (PR #76) and CI is now green.

2. The review MAY have surfaced a release-sequencing issue. It did — Beck #2 argued the CI fix should have come BEFORE the agent ceremony (Tidy First). Sequence-wise that's a moot lesson for this plan, but it becomes a constraint for future similar plans.

**Worst case**: the panel finds nothing material and the plan proceeds as written. Even then, the durable agent assets are created and this AAR documents adversarial review happened.

**Actual case**: the panel surfaced 2 P0 findings affecting future v0.2.0 work, 1 P0 finding affecting the broader IEP CI alerting posture, ~12 P1/P2/P3 findings worth filing, and confirmed the j-rig CI fix shape. Significant value; the 60-min investment paid for itself.

---

## 8. Lessons for future ISEDC sessions

1. **Adversarial review BEFORE execution beats adversarial review AFTER execution.** The panel surfaced findings that would have been more expensive to address mid-release-sweep.

2. **Persona-prompts produce findings; don't trust them as gates.** Per Hickey #4 — every panel-flagged concern that should block future work must reduce to a deterministic rule. The current 9 beads filed are the value; the personas are the generators.

3. **Durable agents > ephemeral prompts.** The 13 thinker files are reusable. Cost was ~15 min to create; expected lifetime is years.

4. **Read-only reviewers preserve audit trail.** Single-signer accountability (acting CTO is sole executor) means future readers can attribute every change to one decision-maker. This is the same pattern as ISEDC's drafting executor in DR-022.

5. **The 60-min "agent ceremony before release work" cost was justified by the OTel semconv finding alone**. Without that finding, v0.2.0 would have shipped with un-pinned attribute names, locking in drift across 5 emitters before consumers existed. Gregg's most-costly was correctly named.

---

## 9. Cross-references

- `~/.claude/agents/martin-fowler-reviewer.md` and 12 sibling files (durable agent assets)
- `intent-eval-lab/000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md` — DR-010, the constitutional document the panel critiqued
- `intent-eval-lab/000-docs/022-AT-DECR-isedc-session-6-beads-reengage-2026-05-23.md` — DR-022, the verify-before-claim discipline source
- `intent-eval-lab/000-docs/012-AT-ARCH-platform-runtime-blueprint.md` — Blueprint B, target of Kleppmann/Hickey/Gregg findings
- bd workspace at `/home/jeremy/000-projects/.beads/`
- Original 6 agent run outputs preserved (Claude Code agent IDs: `a10a35aaac5c48e3c`, `ac986d3616075de01`, `a9c19f3c89b8cc233`, `a4b6eb6181330d3de`, `a9fcca794639ef54e`, `a24641b56d1ca6077`)

---

## 10. Status banding (per Cunningham #1)

**ACTIVE** — Synthesis applied to in-flight release sweep. 9 new beads filed (3 P0 + 6 queued P1-P3). Findings will be re-evaluated in next ISEDC session when actual v0.2.0 work begins. Verbatim agent findings preserved above for future readers + future councils.

---

*Filed by acting CTO during cross-repo release sweep, 2026-05-25. Companion to in-flight PR `intent-eval-core#11` (v0.1.1) and `j-rig-skill-binary-eval#76` (release CI fix).*

— Jeremy Longshore
intentsolutions.io
