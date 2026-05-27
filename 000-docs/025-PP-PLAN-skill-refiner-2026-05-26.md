# Skill Refiner — eval-guided improvement loop for SKILL.md files

| Field | Value |
|---|---|
| Status | DRAFTED 2026-05-26 |
| Owner | Jeremy Longshore (executor: Claude as drafting CTO) |
| Supersedes | Prior 2026-05-26 release-sweep plan (carry-over items folded into § 1). Filename evolved in-PR across 3 brand iterations: `025-PP-PLAN-skillopt-pattern-plugin-ecosystem-2026-05-26.md` (initial draft, borrowed verbiage) → `025-PP-PLAN-j-rig-keeper-pretrip-evidence-2026-05-26.md` (j-rig sub-product naming) → `025-PP-PLAN-skill-refiner-2026-05-26.md` (final, peer-product naming under IS agent-rig stack). |
| Decision basis | User-confirmed via AskUserQuestion rounds 2026-05-26 |
| Scope | ONE new product — **Skill Refiner** — the eval-guided improvement loop that proposes safe, minimal SKILL.md edits and accepts only on strict score improvement. Delivered as a Claude Code plugin with a 3-layer hook architecture (sinker/line/hook); emits signed evidence reports (markdown + HTML) per pass; integrates with the IEP kernel as the 14th canonical entity (SkillVersion) + a new predicate URI (skill-refiner-pass/v1). |
| Status banding | ACTIVE — SUPERSEDED-BY 027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md (this plan is the companion / v3 framing; plan 027 is the v4 enhancement with ecosystem-fold + per-repo bead structure + plan-audit phase) |
| Beads | bd_000-projects-0r8m (product epic — Tier-1 kernel + evidence), bd_000-projects-3zol (product epic — Refiner library), bd_000-projects-jsy3 (product epic — /j-rig plugin + hooks), bd_000-projects-rqwk (RC-IEL), bd_000-projects-brij (RC-IEC), bd_000-projects-214c (RC-IAJ), bd_000-projects-aon3 (RC-IAH), bd_000-projects-r8ir (RC-IAR), bd_000-projects-pu35 (TL-EPIC) |
| GitHub | jeremylongshore/intent-eval-lab#78, jeremylongshore/intent-eval-lab#79, jeremylongshore/intent-eval-core#12, jeremylongshore/j-rig-skill-binary-eval#81, jeremylongshore/intent-audit-harness#42, jeremylongshore/intent-rollout-gate#15 |

## What this is

**Skill Refiner** is the eval-guided improvement loop that proposes safe, minimal changes to a SKILL.md until it passes the rollout gate without regressing sacred tests. It is the **second product in the 3-product Intent Solutions agent-rig stack**:

| Product | What it does |
|---|---|
| **J-Rig Skill Binary Eval** (shipped) | Test harness — evaluates skill behavior across the 7-layer taxonomy |
| **Skill Refiner** (THIS PLAN) | Improvement loop — proposes + accepts bounded SKILL.md edits, gated by eval scores |
| **Rollout Gate** (intent-rollout-gate, in flight at M5) | Final pass/fail release control — consumes Evidence Bundle + policy → ship/no-ship verdict |

Test → improve → ship. Three products, one narrative.

Skill Refiner ships at `@j-rig/refiner` inside the existing j-rig monorepo (`intent-eval-platform/j-rig-binary-eval/`). Engineering structure is 3 epics; consumer-facing surface is ONE product. The 3-layer hook architecture (hook · line · sinker) is Refiner's *delivery mechanism* inside Claude Code; the signed evidence reports (markdown + HTML) are Refiner's *output artifact*. Neither ships as a separately-branded product.

A creator sub-product (would generate NEW skills from scratch) is **DEFERRED**. Public benchmark evidence indicates self-generated skills underperform no-skill baseline; the Refiner does not get a generative sibling until external work demonstrates the bar can be cleared.

## 1. Carry-over from prior plan (release sweep) — incomplete items

The release sweep is COMPLETE. Three items were deferred via the `iep-gist-coverage` follow-up bead; they fold into Phase A here:

| Item | Carry into |
|---|---|
| `/gist-auditor --repo j-rig-binary-eval` on existing gist `d1c4570a8dd54cba6517c56a3dae17f5` | Phase A pre-flight |
| Regenerate j-rig gist with v1.1.0 content (per old plan Step 4 Phase 7.5) | Phase A pre-flight |
| Four missing gists (audit-harness, intent-eval-core, intent-eval-lab, intent-rollout-gate) | Stays under `iep-gist-coverage` bead per CTO call (quality over speed) |

## 2. Product structure

One new product (Skill Refiner), three internal features. Engineering structure stays as 3 epics; consumer-facing surface is ONE brand.

| Feature | Role | Lifecycle moment | Engineering epic |
|---|---|---|---|
| **Refiner core loop** | The bounded-edit propose+accept loop; pure value-oriented library | After N rollouts on a skill: propose + accept edits | Epic 1 (Refiner library) |
| **3-layer hooks (hook · line · sinker)** | The delivery mechanism — runs the Refiner loop inside Claude Code at three lifecycle moments | Sinker on every Edit/Write; Line on every Stop; Hook on every git commit/push | Epic 2 (Plugin + hooks) |
| **Signed evidence reports** | The output artifact — markdown AAR + HTML projection per Refiner pass; signed Evidence Bundle row | After each accepted (or rejected) edit | Epic 3 (Evidence reports + Tier-1 kernel integration) |

**Plugin shape**: single `/j-rig` plugin in `claude-code-plugins` with subcommands (`/j-rig refine`, `/j-rig status`, `/j-rig promote`). One marketplace entry, one hook config. The plugin path stays at `/j-rig` because the Refiner is delivered through j-rig's existing engineering home; the user-facing brand is "Skill Refiner" even though the plugin command lives under `/j-rig`.

**Creator sub-product (would generate NEW skills from scratch)**: DEFERRED at P3. Filed bead stays open with deferral note; trigger to re-open = public benchmark evidence that self-generated skills can clear the no-skill baseline AND a partner ask for the capability.

## 3. Architectural commitments

Non-negotiables for any Skill Refiner / 3-layer hooks / Evidence implementation. These are IS-native commitments; prior art informed the design space but does not dictate the architecture.

1. **Tier-1 IEP integration**: `SkillVersion` entity in `intent-eval-core` kernel + `skill-refiner-pass/v1` predicate URI on `evals.intentsolutions.io`. 14th canonical entity. Blocks on existing P0 beads (`uprg` Evidence Bundle compat policy + `9pi3` OTel semconv pin).
2. **Append-only event log**: never in-place SKILL.md mutation. Every accepted edit produces a content-addressed `SkillVersion` value; "current best" is a separate mutable pointer. If `bd_000-projects-uprg` policy locks in immutable artifact semantics, this layer satisfies it.
3. **Multi-dimensional score records**: `(skill_hash, eval_set_hash, behavioral_score, readability_score, adversarial_pass_rate, ...)`. Never collapsed to a scalar. Single-score refinement invites the variant that games the metric.
4. **Promotion ladder**: shadow → canary → promote. Refiner proposes candidate edits; humans review + promote. **No auto-write to SKILL.md on main.** This is a hard floor, not a defaultable setting.
5. **Tiered model routing**: Haiku for rollout scoring, Sonnet for the refiner, Opus only for final validation. Hard budget cap per skill + alert at 80%. Naive Opus-everywhere costs roughly $11K/mo for 30 skills; tiered routing delivers an order-of-magnitude reduction.
6. **Eval-set bootstrap is first-class**: every skill being Kept needs a held-out set. Three sources: (a) synthetic from SKILL.md, (b) j-rig Binary Eval rollout harvest, (c) human-nominated golden traces. Bootstrap is a CLI command, not a manual step.
7. **The acceptance gate is the durable contribution; the refiner mechanism is swappable.** When frontier-native skill refinement arrives, keep the harness + gate + Evidence pipeline; throw away the refiner internals.
8. **3-layer hooks = three hooks at three lifecycle moments at three cost tiers.** Hook, line, sinker — three layers of inspection before the rig leaves the dock:
   - **Sinker (L1)** — `PostToolUse:Edit/Write` on SKILL.md. Deterministic `validate-skillmd` Tier 2 check. $0 (no model call). Drops fast, anchors the rig.
   - **Line (L2)** — `Stop` hook. End-of-turn rollout capture; fires refiner in background after N rollouts. $ (Sonnet refiner model; Haiku scoring). The line tells you the bite is real.
   - **Hook (L3)** — `PostToolUse:Bash` matcher `git commit`/`git push` on staged SKILL.md diff. Agentic gate: check against rejected-edit buffer + shadow-validation against held-out set. $$ (Opus, rate-limited). Sets the catch.
9. **Single-signer audit trail**: Refiner proposes; humans + acting CTO dispose. Read-only roles preserved through the chain. Every accepted edit cites the actor identity in its `SkillVersion` record.
10. **Position: evals-gated edits, not automated refinement.** Every Evidence report shows the rejected-edits buffer alongside the accepted ones. Trust comes from showing the work, not hiding it. Marketing surface stays consistent: "j-rig — the rig for agentic software. Evaluate skills. Gate changes. Ship with evidence."

## 4. Phased roadmap

Five phases (A, B, C, E, F). Phase D deferred per § 2. Each phase ships independently. Each later phase consumes earlier-phase value artifacts.

### Phase A — Skill Refiner discipline library — ~1 week

**Goal**: Ship the value-oriented core of Refiner. NO hooks. NO new kernel entity. NO plugin shape. Pure library + thin CLI inside the j-rig monorepo.

**Deliverables**:

- New package: `@j-rig/refiner` (in `j-rig-binary-eval/packages/refiner/`)
- API surface (illustrative — final shape lands in the package):

```typescript
type SkillDocHash = Sha256;
type EvalSetHash = Sha256;
type ScoreRecord = {
  skill: SkillDocHash;
  evalSet: EvalSetHash;
  behavioral: number;
  readability: number;
  [dimension: string]: unknown;
};
type EditProposal = {
  parent: SkillDocHash;
  ops: Array<AddOp | DeleteOp | ReplaceOp>;
  proposer_model: string;
  rationale: string;
};

declare function bootstrap(skillDoc: SkillDoc): EvalSet;
declare function score(skillDoc: SkillDoc, evalSet: EvalSet, modelTier?: 'haiku' | 'sonnet' | 'opus'): ScoreRecord;
declare function propose(skillDoc: SkillDoc, scoredRollouts: ScoredRollout[], refinerModel?: string): EditProposal;
declare function apply(skillDoc: SkillDoc, edit: EditProposal): SkillDocV2;
declare function accept(scoreV1: ScoreRecord, scoreV2: ScoreRecord): boolean;
```

- Append-only event log at `.j-rig/refiner/log.jsonl`
- Content-addressed store at `.j-rig/refiner/store/<hash>`
- Single mutable pointer file: `.j-rig/refiner/pointers/<skill>/best`
- CLI: `j-rig refine bootstrap <skill>`, `j-rig refine score <skill>`, `j-rig refine propose <skill>`, `j-rig refine apply <proposal>`, `j-rig refine status <skill>`
- **Phase A pre-flight**: complete deferred old-plan items — `/gist-auditor --repo j-rig-binary-eval` and regenerate j-rig gist `d1c4570a8...` to v1.1.0 content.

**Reuses existing IEP infrastructure**:

- `j-rig Binary Eval` (`packages/cli/src/commands/{eval,optimize}.ts`) — Refiner DELEGATES scoring to Binary Eval; no new evaluator
- `j-rig` optimizer types (`ChangeProposal`, `Experiment`, `OptimizerProvider`) — Refiner wraps these with value-oriented hash-chaining discipline
- `validate-skillmd` Tier 2 — reusable as pre-acceptance gate
- `audit-harness emit-evidence` — Refiner shells out for in-toto Statement v1 emission

**Exit criteria**: ship `@j-rig/refiner@0.1.0` to npm with sigstore provenance. Demo: `j-rig refine bootstrap /release` produces a valid eval set; `j-rig refine score /release` returns a ScoreRecord; `j-rig refine propose /release` returns an EditProposal; `j-rig refine apply` produces a SkillDocV2 value.

### Phase B — /j-rig plugin v0.1.0 (Refiner + 3-layer hooks together) — ~2 weeks

**Goal**: Wrap Phase A library in a Claude Code plugin and install 3-layer hooks's three hooks. User-visible product lives in `claude-code-plugins`.

**3-layer hooks three-hook layout**:

```
plugins/productivity/j-rig/
├── .claude-plugin/
│   ├── plugin.json
│   └── hooks/hooks.json
└── hooks/
    ├── sinker.sh           # L1 — PostToolUse:Edit/Write on SKILL.md
    ├── line.sh             # L2 — Stop hook (end-of-turn rollout capture)
    └── hook.sh             # L3 — PostToolUse:Bash on git commit/push
```

| Hook | Event | Mechanism | Cost |
|---|---|---|---|
| **Sinker (L1)** | `PostToolUse:Edit/Write` on `SKILL.md` files | Run `validate-skillmd` Tier 2 deterministic check; append warning to context if fails | $0 |
| **Line (L2)** | `Stop` hook | If a skill was invoked AND Binary Eval scored its rollouts: append to `.j-rig/refiner/log.jsonl`. After N rollouts on a skill: fire Refiner in background; surface candidate in next-turn context | $ (Sonnet refiner model; Haiku scoring) |
| **Hook (L3)** | `PostToolUse:Bash` matcher `git commit`/`git push` | If staged diff modifies a SKILL.md: agentic gate that reads surrounding skills + checks regression-against-rejected-buffer + (optional) shadow-validation against held-out set | $$ (Opus; rate-limited) |

**Plugin CLI surface**:

- `/j-rig refine bootstrap <skill>` — create initial eval set
- `/j-rig refine propose <skill>` — manual Refiner pass
- `/j-rig refine shadow <skill>` — run candidate in shadow mode
- `/j-rig refine promote <skill>` — human-gated promote candidate → main
- `/j-rig status <skill>` — show trajectory + budget + rejected log

**MVP demo**: pick ONE existing skill (recommended `/audit-tests` for cleaner blog post, OR `/validate-skillmd` for sharper IP-defense story — § 7 open question). Run full bootstrap → score → propose → shadow → promote cycle; produce Phase E Evidence report (md + HTML); publish as case-study blog post.

**Exit criteria**:

- Plugin published to `claude-code-plugins` marketplace at `plugins/productivity/j-rig/`
- One real skill refined end-to-end with shipped score-delta evidence
- Phase E Evidence report (markdown + HTML) generated and published as blog post

### Phase C — Tier-1 IEP integration (kernel) — ~3–4 weeks

**Goal**: Promote `SkillVersion` to the 14th canonical entity in `intent-eval-core`. Mint `skill-refiner-pass/v1` predicate URI. j-rig becomes an emitter of skill-refiner-pass rows; `intent-rollout-gate` becomes a consumer.

**Architectural commits**:

New entity `SkillVersion` in `intent-eval-core/schemas/v1/skill-version.schema.json`:

```jsonc
{
  "id": "uuidv7",
  "skill_id": "kebab-slug",
  "skill_doc_hash": "sha256",
  "parent_version_id": "uuidv7 | null",
  "edit_proposal_hash": "sha256 | null",
  "eval_set_hash": "sha256",
  "score_record": { "behavioral": "number", "readability": "number" },
  "accepted_by": "actor-identity",
  "accepted_at": "rfc3339",
  "signing_mode": "staging | production",
  "rekor_log_index": "int64 | null"
}
```

- New predicate URI: `https://evals.intentsolutions.io/skill-refiner-pass/v1`
- Blueprint B § 7 extension documenting the new predicate body
- Companion governance: P0 bead `bd_000-projects-uprg` (Evidence Bundle compat policy) MUST land before this predicate URI is signed into production Rekor. **Phase C cannot complete until `uprg` is closed.**

**j-rig changes**:

- New CLI command `j-rig emit-skill-step` parallel to existing `j-rig emit-evidence` — emits `skill-refiner-pass/v1` rows
- Refiner's `optimizer/` module extended to use `@j-rig/refiner` value types (Phase A becomes a transitive dep within the monorepo)

**intent-rollout-gate changes**:

- M5 substantive runtime consumes `skill-refiner-pass/v1` rows as enrichment (not blocking advisory by default)

**Companion P0 bead dependencies**:

- `bd_000-projects-uprg` — Evidence Bundle predicate compatibility policy (BLOCKS this phase)
- `bd_000-projects-9pi3` — OTel semconv pin (BLOCKS kernel v0.3.0 ship)
- `bd_000-projects-59tx` — Release workflow failure alerting (CROSS-CUTTING)

**Exit criteria**:

- `@intentsolutions/core@0.3.0` published with `SkillVersion` entity
- `j-rig-binary-eval` ships `j-rig emit-skill-step` command
- intent-eval-lab Blueprint B § 7 extended with new predicate spec
- ISEDC Session 7 ratifies the URI namespace addition (CISO binding: must be on `evals.intentsolutions.io`, not `labs.`)

### Phase D — DEFERRED (creator sub-product)

Originally scoped as a fourth j-rig sub-product (working placeholder name dropped per IS brand canon). Public benchmark evidence indicates self-generated skills underperform no-skill baseline. j-rig does not ship a creator until either:

(a) External work demonstrates the bar can be cleared on agent-skill generation OR
(b) A partner explicitly asks for the capability AND accepts the risk profile.

Bead stays open at P3 with deferral note. No code, no design, no marketplace listing until the trigger fires.

### Phase E — Skill Refiner evidence (report production + storage spec) — ongoing

**Goal**: Define the per-Refiner-pass deliverable shape. Consumers SEE the eval ran and produced something defensible. The evidence pipeline is the brand surface where the rig's work becomes auditable artifact.

#### E.1 — Markdown AAR (canonical, git-versioned, machine-parseable)

Filename per Doc Filing Standard v4.3:
`<repo>/000-docs/NNN-RL-REPT-skill-refiner-<skill>-<date>.md`

Template (each section REQUIRED; missing sections fail the BLOCKING gate):

```markdown
# Skill Refiner evidence Report — Refiner run on `<skill-id>`

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Skill | <skill-id> |
| Skill version (input) | sha256(...) (8-char prefix) |
| Skill version (output) | sha256(...) (8-char prefix) |
| Eval set | sha256(...) (8-char prefix) |
| Score delta | behavioral +N.Mpp; readability +N.Mpp |
| Refinement passes | N (M accepted, K rejected) |
| Compute cost | $X.XX (Haiku $X.XX; Sonnet $X.XX; Opus $X.XX) |
| Wall-clock | HH:MM:SS |
| Confidence tier | `alpha` \| `beta` \| `stable` |

## 1. Context
## 2. Eval set composition
## 3. Score trajectory
## 4. Accepted edits (replayable)
## 5. Rejected edits (audit trail)
## 6. 3-layer hooks gate evidence (per pass)
## 7. Signed Evidence Bundle (in-toto Statement v1)
## 8. Architectural bindings
## 9. Limitations + risks
## 10. Status banding
```

#### E.2 — HTML projection (derived from markdown AAR)

Generated deterministically from markdown source via Hugo template. **Single source of truth; HTML is a view.** Hosted at `evals.intentsolutions.io/reports/<skill-id>/<sha-prefix>/`. Mirrors the existing `partner-portals` Hugo infrastructure.

Sections rendered: hero (skill + delta + cost + wall-clock); score-trajectory chart; side-by-side diff browser; rejected-edits collapsible table; verification panel with cosign-verify command + Rekor log indices; architectural-bindings footer links.

#### E.3 — Storage spec

| Artifact | Storage | Retention |
|---|---|---|
| Markdown AAR | `<repo>/000-docs/NNN-RL-REPT-*.md` (committed to git) | Forever |
| Signed Evidence Bundle | `<repo>/.j-rig/evidence/<sha>.json` (gitignored if signed-prod, committed if signed-staging) | Indexed by sha; orphaned bundles GC'd after 90 days |
| HTML render | `evals.intentsolutions.io/reports/<skill-id>/<sha-prefix>/` (Hugo build artifact) | Pinned per version; never overwritten |
| Rekor log entry | Public sigstore Rekor | Permanent (by design) |

**Phase E exit criteria**:

- Markdown template committed to `intent-eval-lab/specs/skill-refiner-evidence-report/v1.0.0-draft/SPEC.md`
- HTML renderer (~200 LOC Hugo template + recharts JS) shipped as part of partner-portal infrastructure
- ISEDC Session 7 ratifies the predicate URI carrying the report's canonical sha
- One real report generated end-to-end (Phase B exit-criteria demo skill)

### Phase F — MLOps scale-up (long-term, ~Q3 2026) — beyond MVP

| Layer | Mechanism | Filed bead |
|---|---|---|
| Skill registry | SkillVersion + lineage graph | Phase C extends |
| Eval-set governance | Versioned + reviewed quarterly + rolling-production + adversarial-append | bd_000-projects-6qyw.6 |
| Canary rollouts | Per-partner traffic routing of skill versions | bd_000-projects-6qyw.7 |
| Partner skill pins | Partner pins skill version; promotion is per-partner | bd_000-projects-6qyw.8 |
| Drift policy | Weekly re-validation; event-triggered on upstream model bump; auto-refine on persistent drift | bd_000-projects-6qyw.9 |
| Promotion graph | Shadow → canary-10% → canary-50% → 100% → archived | Phase C SkillVersion + DR per transition |
| Cost dashboard | OTel-spans + per-skill cost trajectory + hard alerts at 80% budget | Subsumes `iel-E12-attributes-pinned` (already P0 in `9pi3`) |

**Phase F triggers**: when (a) ≥5 partners actively consume Kept skills OR (b) ≥100 active `SkillVersion` records OR (c) drift incident in production causes the first rollback. Until then, Phases A→C+E are sufficient.

## 5. Critical files to be created / modified

### NEW packages (Phase A + Phase E)

- `@j-rig/refiner` — new package inside j-rig monorepo at `j-rig-binary-eval/packages/refiner/`
- `@j-rig/evidence` (optional Phase E) — Hugo template + renderer; could ship as part of partner-portals infrastructure instead

### `intent-eval-core/` (Phase C)

- `schemas/v1/skill-version.schema.json` — NEW entity schema
- `src/validators/v1/skill-version.ts` — NEW Zod validator (regenerated via `pnpm run codegen:validators`)
- `src/validators/v1/index.ts` — export new validator
- `schemas/v1/skill-refiner-pass.schema.json` — NEW predicate schema
- `schemas/v1/index.json` — register new entity + predicate
- `CHANGELOG.md` — `[0.3.0]` entry per Keep-a-Changelog 1.1.0 (hyphen, not em-dash)
- `package.json` — version 0.1.1 → 0.3.0 (MINOR — additive Parallel Change per `bd_000-projects-xcs4`)
- `000-docs/NNN-RL-REPT-release-v0.3.0-<date>.md`

### `intent-eval-lab/` (Phase C + E)

- `000-docs/012-AT-ARCH-platform-runtime-blueprint.md` — extend § 7 with `skill-refiner-pass/v1` normative spec
- `000-docs/014-DR-GLOS-canonical-glossary.md` — add SkillVersion + Skill Refiner + Skill Refiner's 3-layer hooks + Skill Refiner evidence + ScoreRecord + EditProposal terminology
- `specs/skill-refiner-evidence-report/v1.0.0-draft/SPEC.md` — NEW report template spec (Phase E.1)
- `000-docs/NNN-AT-DECR-isedc-session-7-jrig-tier1.md` — DR ratifying the predicate URI + entity addition

### `j-rig-binary-eval/` (Phase A + Phase C)

- `packages/refiner/` — new package directory (Phase A)
- `packages/cli/src/commands/emit-skill-step.ts` — NEW command parallel to `emit-evidence.ts` (Phase C)
- `packages/core/src/optimizer/index.ts` — extend to use `@j-rig/refiner` types (Phase C)
- `CHANGELOG.md` — `[v1.2.0]` MINOR entry

### `claude-code-plugins/` (Phase B)

- `plugins/productivity/j-rig/.claude-plugin/plugin.json`
- `plugins/productivity/j-rig/.claude-plugin/hooks/hooks.json`
- `plugins/productivity/j-rig/hooks/{sinker.sh,line.sh,hook.sh}`
- `plugins/productivity/j-rig/skills/j-rig/SKILL.md`
- `plugins/productivity/j-rig/scripts/refiner-loop.ts`

### bd workspace (`~/000-projects/.beads/`)

**Restructured 2026-05-26 per user direction: 3 epics × 7–10 children each (replaces prior 1-epic-9-child structure).** Old beads `bd_000-projects-6qyw` + `.1`–`.9` closed as superseded with forward-pointing notes; new structure below.

**Three new epics**:

- **`bd_000-projects-3zol`** (P1) — Ship Skill Refiner — the eval-gated skill refinement discipline library + CLI at `@j-rig/refiner` v0.1.0
  - 8 task-level children: package scaffold + value types · `bootstrap()` · `score()` · `propose()` · `apply()`+`accept()` · event log + content-addressed store · CLI (5 commands) · release ceremony
- **`bd_000-projects-jsy3`** (P1, deps: `3zol`) — Ship `/j-rig` Claude Code plugin — Refiner subcommands wired together with 3-layer hooks 3-layer hook architecture (sinker/line/hook)
  - 8 task-level children: plugin scaffold + hooks.json · Sinker (L1) · Line (L2) · Hook (L3) · CLI subcommand wiring · target-skill decision · end-to-end MVP demo + Evidence report + blog post · marketplace publish
- **`bd_000-projects-0r8m`** (P0, deps: `3zol`, `uprg`, `9pi3`) — Ship Skill Refiner evidence + Tier-1 IEP kernel integration — SkillVersion entity (14th canonical) + skill-refiner-pass/v1 predicate URI + signed evidence reports
  - 10 task-level children: SkillVersion schema · Zod validator · predicate schema · Blueprint B § 7 extension · glossary update · `j-rig emit-skill-step` CLI · ISEDC Session 7 ratification · kernel v0.3.0 release · skill-refiner-evidence-report SPEC.md template · HTML renderer

**Deferred standalone beads** (P3, not children of any epic): Phase D creator product + 4 Phase F MLOps scale-up items (eval-set governance, canary rollouts, partner skill pins, drift policy). Trigger conditions documented per bead.

**Companion P0 dependency beads** (already filed, unchanged):

- `bd_000-projects-uprg` — Evidence Bundle compat policy (BLOCKS Epic 3)
- `bd_000-projects-9pi3` — OTel semconv pin (BLOCKS Epic 3 kernel ship)
- `bd_000-projects-59tx` — Release workflow failure alerting (CROSS-CUTTING for Epic 1 + Epic 3 release ceremonies)

Companion action executed in this PR: GH repo `jeremylongshore/audit-harness` renamed to `jeremylongshore/intent-audit-harness`. GH auto-redirects old URLs; local git remotes updated. npm package + CLI binary + local FS directory all stay as `audit-harness` (per user scope clarification 2026-05-26).

## 6. Reused infrastructure

| Component | Location | Reused for |
|---|---|---|
| `/skill-creator` skill | `~/.claude/skills/skill-creator/SKILL.md` | (was Phase D scaffold; Phase D deferred) |
| `/validate-skillmd` skill | `~/.claude/skills/validate-skillmd/SKILL.md` | Phase B Sinker (L1) deterministic gate (Tier 2 checks) |
| `/audit-tests` + `/implement-tests` | `~/.claude/skills/` | Phase A bootstrap (7-layer taxonomy approach) |
| `/appaudit` skill | `~/.claude/skills/appaudit/SKILL.md` | Phase E HTML render (partner-grade PDF reports) |
| `/release` skill | `~/.claude/skills/release/SKILL.md` | Phase B plugin release (8-phase ceremony) |
| `/branch-protection` skill | `~/.claude/skills/branch-protection/SKILL.md` | Phase C kernel v0.3.0 protected-main push pattern |
| `/gist-auditor` skill | `~/.claude/skills/gist-auditor/SKILL.md` | Phase A pre-flight: run against j-rig gist (carry-over from old plan) |
| `j-rig` optimizer types (`ChangeProposal`, `Experiment`, `OptimizerProvider`) | `j-rig-binary-eval/packages/core/src/optimizer/` | Phase A Refiner library extends these |
| `j-rig` Binary Eval CLIs (`eval`/`optimize`/`check`/`emit-evidence`) | `j-rig-binary-eval/packages/cli/src/commands/` | Phase A Refiner DELEGATES scoring |
| `audit-harness emit-evidence` subcommand | `audit-harness/scripts/emit-evidence.sh` | Phase A Refiner uses for in-toto Statement v1 emission |
| `SkillSnapshot` entity (existing) | `intent-eval-core/schemas/v1/skill-snapshot.schema.json` | Phase C SkillVersion extends/references this (NOT duplicate — SkillSnapshot pins source state; SkillVersion captures refinement lineage) |
| `gate-result/v1` predicate | `intent-eval-core/schemas/v1/gate-result.schema.json` + Blueprint B § 7 | Phase A Refiner emits these from refinement passes via j-rig Binary Eval |
| Partner-portal infrastructure (Hugo) | `~/000-projects/partner-portals/` | Phase E HTML render hosting (new section `evals.intentsolutions.io/reports/`) |
| bd-sync three-layer mirror | `~/bin/bd-sync` | All new beads filed per the discipline |
| Doc Filing Standard v4.x | `intent-eval-lab/000-docs/` + `/doc-filing` skill | Phase E markdown template numbering |

## 7. Open questions

**Resolved in this rebrand**:

- ~~§ 7.1 packaging (separate repo vs monorepo)~~ — **RESOLVED**: j-rig monorepo, `@j-rig/*` scope, new package `@j-rig/refiner`
- ~~§ 7.2 creator-product name~~ — **RESOLVED**: deferred per § 2 (no creator product ships)
- ~~§ 7.3 npm scope~~ — **RESOLVED**: `@j-rig/*` (not `@intentsolutions/*`)

**Still open** (Phase A claim should resolve):

1. **Phase B target skill for end-to-end demo**: `/audit-tests` (rich invocation history, cleaner blog post) OR `/validate-skillmd` (meta-recursive, sharper IP-defense story)?
2. **Phase C kernel version sequencing**: v0.2.0 ships `EvidenceBundlePayload` per existing `iec-E12`; SkillVersion lands in v0.3.0. Honors expand-contract Parallel Change (`bd_000-projects-xcs4`). Confirm.

## 8. Risks + mitigations

| Risk | Mitigation |
|---|---|
| Frontier ships skill-refinement that subsumes Refiner's mechanism in 6–12mo | Phase A library exposes pure-function value API; the proposer mechanism is a pluggable strategy behind the gate, not the core contract. When frontier-native arrives: swap proposer, keep harness + 3-layer hooks + Evidence |
| Single-score Goodhart corner gaming | Multi-dimensional score records (behavioral + readability + adversarial-pass-rate). Per-skill kind extension via index signature on ScoreRecord |
| Cost runaway — naive Opus-everywhere ≈ $11K/mo for 30 skills | Tiered routing: Haiku scoring, Sonnet proposer, Opus only validation. Hard budget cap at workflow level + alert at 80% |
| Phase C blocks on `uprg`+`9pi3` indefinitely | Phases A+B NOT blocked on Phase C — they use existing `gate-result/v1` and `SkillSnapshot` + emit via j-rig Binary Eval. Phase C is the polish/first-class layer. Plan can ship A+B without C |
| Branch-protection failures on Phase C kernel release | Already mitigated — j-rig adopted tag-trigger pattern (PR #80, 2026-05-26). Phase C uses same pattern in intent-eval-core release.yml (already canonical) |
| Eval-set bootstrap deferred → no usable Refiner | Phase A bootstrap is FIRST-CLASS, not deferred. Three sources: synthetic + Binary Eval rollout-harvest + human-nominated golden. All three implemented in Phase A |
| 3-layer hooks hooks become disabled-by-default if they're noisy | Each hook has independent enable/disable. Sinker is cheap and on-by-default. Line is opt-in per skill (only fires after bootstrap). Hook is opt-in per repo (only fires on repos that have run bootstrap) |
| `iah-npm-publish-gap` (audit-harness git v1.1.4 vs npm v0.1.0) blocks consumer reach | Phase C must close this — audit-harness needs release.yml + first npm publish from v1.1.4 OR Phase C explicitly notes the gap. Filed as bead `iah-npm-publish-gap`; tracked separately |
| Reports become a brand-surface explosion if every run gets a public HTML page | Markdown is canonical (in git); HTML is OPT-IN per-report (defaults internal-only). Public reports gated by quality + human approval (mirrors `iep-gist-coverage` policy) |
| Plugin marketed as "automated skill refinement" → consumer expects auto-magic → trust failure on first bad edit | Marketing position is "evals-gated edits, not automated refinement". Every Evidence report shows the rejected-edits buffer alongside accepted ones. Trust comes from showing the work, not hiding it |

## 9. Verification (end-to-end exit criteria)

1. **Phase A ships**: `npm view @j-rig/refiner` returns v0.1.0+ with sigstore provenance
2. **Phase B ships**: `/j-rig` plugin in claude-code-plugins marketplace; ONE real skill Kept end-to-end with shipped score-delta evidence; blog post published
3. **Phase C ships** (gated on `uprg`+`9pi3`): `@intentsolutions/core@0.3.0` published with `SkillVersion`; `skill-refiner-pass/v1` URI live (test signed via cosign + Rekor staging); ISEDC Session 7 DR filed
4. **Phase D**: stays DEFERRED until external trigger fires
5. **Phase E ships**: report template at `intent-eval-lab/specs/skill-refiner-evidence-report/v1.0.0-draft/SPEC.md`; HTML renderer live at `evals.intentsolutions.io/reports/`; one real report generated end-to-end (Phase B demo)
6. **Phase F triggers** (NOT ship — trigger): when ≥5 partners consume Kept skills OR ≥100 active SkillVersion records OR first rollback incident

If any phase exit-criterion fails > 2 weeks past target: pause, file an ISEDC session, re-plan.

## 10. Stopping criteria

- Frontier ships native skill-refinement subsuming Refiner's proposer mechanism → archive Phases A–C as historical IS contribution; keep Phase E (Evidence) as durable interface; Phase F may still be relevant
- Phase B end-to-end demo fails meaningful score-delta on ANY real skill → DO NOT promote to wider rollout; the discipline didn't work in this codebase
- External benchmark evidence shows our skills hit the same negative-baseline pattern that gates Phase D → keep Phases A+B as internal-only tooling; do not market externally
- Phase C `uprg` or `9pi3` cannot be closed (e.g., compat policy can't be agreed) → Phase C stays deferred; Phases A+B continue without first-class kernel integration

## 11. What this plan does NOT do

- Does not advance any current bead beyond the ones already filed (`uprg`, `9pi3`, `59tx`, `tyck`, `uop6`, `5qcy`, `9yhe`, `xcs4`, `bj5m`, `q9vn`, `iah-npm-publish-gap`, `iep-gist-coverage`). Phase A–F bead filing happened POST-plan-approval.
- Does not write any code. Plan mode is design-only. Implementation begins at Phase A kickoff.
- Does not commit to a Phase B demo skill (`/audit-tests` vs `/validate-skillmd`) — open question.
- Does not address the broader gist-coverage work (4 missing gists across audit-harness, intent-eval-core, intent-eval-lab, intent-rollout-gate). Those stay under `iep-gist-coverage`.
- Does not address P6 Phase A3+ linting infrastructure (separate workstream).
- Does not advance the Plane / GH / bd projection inversion (`q9vn` design spike) — separate workstream.
- Executes the GH repo rename `jeremylongshore/audit-harness` → `jeremylongshore/intent-audit-harness` as part of this PR (GH auto-redirects old URLs; local remote URLs updated). Does NOT rename the npm package, the CLI binary, or the local FS directory — those stay as `audit-harness` and `@intentsolutions/audit-harness`. Per user scope clarification 2026-05-26: "just change the public-facing repo name on GitHub."

## Prior art (cited for reproducibility, not borrowed for branding)

Public work on text-space agent-skill refinement (arXiv 2605.23904), 3-layer in-session hook architectures (Anthropic published a reference implementation around mid-2026), and skill benchmark measurement (arXiv 2602.12670, 40-author multi-org study) informed the design space. Skill Refiner, 3-layer hooks, and Evidence are IS-native products; the cited work is referenced for reproducibility and design-context, not borrowed for branding or framing. Per DR-010 § 13.6 (external-pattern non-borrow), our sub-product names, architectural framing, and positioning are forward-deployed from first principles within the j-rig ecosystem.

---

- Jeremy Longshore
intentsolutions.io
