# SkillOpt-Pattern Plugin Ecosystem for the Intent Eval Platform

| Field | Value |
|---|---|
| Status | DRAFTED 2026-05-26 |
| Owner | Jeremy Longshore (executor: Claude as drafting CTO) |
| Supersedes | Prior 2026-05-26 release-sweep plan (carry-over items folded into § 1) |
| Decision basis | User-confirmed via 4-question AskUserQuestion 2026-05-26 |
| Scope | Two-plugin ecosystem (refiner + creator) + Tier-1 IEP integration + dual md/HTML report shape |
| Status banding | ACTIVE |

## Context — why this plan exists

The 2026-05-22 SkillOpt arXiv paper (`2605.23904`) proposes a text-space optimizer for agent skills: separate optimizer model → bounded add/delete/replace edits on a skill doc → edit accepted only if held-out validation score strictly improves. Anthropic's security-guidance plugin (`code.claude.com/docs/en/security-guidance`, released ~2026-05) is the canonical hook-based template for "spawn separate model call from a hook, feed findings back to session" — Anthropic explicitly publishes its source as the reference implementation for this pattern.

The two compose. SkillOpt's mechanism + security-guidance's hook architecture = a Claude Code plugin that performs evals-gated skill edits in-session. The user owns `claude-code-plugins` (2000+ stars, 30+ human-curated skills, ~45k npm downloads), the IEP ecosystem (kernel + lab + audit-harness + j-rig + rollout-gate), and j-rig is the canonical 7-layer skill evaluator that already produces `gate-result/v1` Evidence Bundle rows with scores. **Every piece needed to build a SkillOpt-pattern plugin already exists; the work is composition, not new infrastructure.**

### Frontier landscape (Phase 1 deep-dive, May 2026)

| Paper | Date | Mechanism | Relevance |
|---|---|---|---|
| **SkillOpt** (arXiv 2605.23904) | 2026-05-22 | Text-space SGD-style optimizer; bounded edits + held-out-strict-improvement gate; rejected-edit buffer | Primary subject |
| **Skill-R1** (arXiv 2605.09359) | 2026-05-10 | RL bi-level GRPO; intra+inter-generation advantage; lightweight skill generator conditions frozen task LLM | Direct competitor — different optimizer technique (RL vs text-space SGD); same "frozen agent + external state" thesis |
| **SHARP** (arXiv 2605.06822) | 2026-05-07 | Self-Evolving Human-Auditable Rubric Policy; bounded symbolic rule edits + walk-forward validation | Architectural analog in finance domain; identical "policy drift → bounded structured edits" pattern |
| **Learning to Self-Evolve (LSE)** (arXiv 2603.18620) | 2026-03-19 | RL trains 4B model to evolve its own contexts; beats GPT-5 + Sonnet 4.5 + GEPA + TextGrad on prompt-opt benchmarks | Direct competitor; **4B beats Sonnet 4.5** is a bitter-lesson alarm |
| **Skill-CMIB** (arXiv 2605.08526) | 2026-05-08 | Multimodal skill construction via Conditional Multimodal Information Bottleneck | Adjacent — multimodal generalization vector |
| **Skill-Pro** (arXiv 2602.01869) | ~2026-02 | Non-Parametric PPO + PPO Gate + Semantic Gradients | Adjacent — "PPO Gate Pass Rate" is the same idea as held-out-strict-improvement |
| **CUA-Skill** (Microsoft, arXiv 2601.21123) | 2026-01 | Computer-use agent skill library; 57.5% on WindowsAgentArena | Industry investment |
| **EvoFSM** (arXiv 2601.09465) | 2026-01-14 | Self-evolving via Finite State Machine (constrained) instead of free-form rewriting | Adjacent — same "unconstrained = drift" problem, different shape |
| **AgenticRecTune** (arXiv 2604.26969) | 2026-04-21 | Multi-agent + Self-Evolving Skillhub for recommendation systems | Adjacent industry application |
| **SkillsBench** (Microsoft + 40 authors, arXiv 2602.12670) | ~2026-02 | Benchmark: how well do agent skills work across tasks | **CRITICAL — see below** |
| **Generate-Filter-Control-Replay** survey (arXiv 2605.02913) | 2026-05-08 | 23-author survey framing the rollout-strategy space | Field-mapping document |

### The strategically critical SkillsBench finding

> *"Skills provide substantial but variable benefit. Skills improve performance by +16.2pp on average across 7 model-harness configurations… Self-generated Skills provide negligible or negative benefit. When prompted to generate their own procedural knowledge before solving tasks, models achieve −1.3pp on average compared to the no-Skills baseline… effective Skills require human-curated domain expertise that models cannot reliably self-generate."*

**This is the IP-defense argument for `claude-code-plugins`'s 30+ human-curated skills.** Human-curated skills give +16.2pp; self-generated give −1.3pp (NEGATIVE). The role of a SkillOpt-pattern optimizer is **NOT to replace human curation but to refine it via evals-gated edits**. SkillsBench provides the empirical baseline that justifies the user's two-product split: a refiner (anchored on the +16.2pp curated baseline) + a creator (which must beat the −1.3pp self-generated baseline before it ships anything).

## 1. Carry-over from prior plan (release sweep) — incomplete items

The release sweep (steps 0–7 of prior plan) is COMPLETE. Three items were explicitly deferred via the `iep-gist-coverage` follow-up bead. They are folded into Phase A of this new plan:

| Item | Status | Carry into |
|---|---|---|
| `/gist-auditor --repo j-rig-binary-eval` on existing gist `d1c4570a8dd54cba6517c56a3dae17f5` | DEFERRED | Phase A pre-flight |
| Regenerate j-rig gist with v1.1.0 content (per old plan Step 4 Phase 7.5) | DEFERRED | Phase A pre-flight |
| `iep-gist-coverage` bead's 4 missing gists (audit-harness, intent-eval-core, intent-eval-lab, intent-rollout-gate) | DEFERRED | Phase E — Reports/Brand surface (quality-over-speed per CTO call) |

## 2. Naming + product structure

Two products, anchored on the SkillsBench empirical bifurcation:

| Plugin | Role | Anchor | Confidence | Status |
|---|---|---|---|---|
| **`/skill-improve`** (working name; final TBD) | **REFINER** — applies SkillOpt-pattern optimization to existing human-curated skills | Built on +16.2pp curated baseline (SkillsBench) | HIGH — SkillsBench validates the substrate | Primary product; ships first |
| **`/<NEW-NAME>`** (placeholder) | **CREATOR** — generates new skills from scratch with eval-gated discipline | Must beat the −1.3pp self-generated baseline before ANY skill ships | LOWER — must prove it beats SkillsBench's negative baseline | Secondary product; ships after refiner |

**Creator-name candidates** (user to pick later): `SkillSmith`, `SkillMint`, `SkillCraft`, `SkillSpawn`. **AVOID**: `SkillForge` (conflicts with `/skill-creator --forge` mode). **Recommended placeholder**: `SkillSmith`.

The refiner is **infrastructure** (Phases A→C). The creator is **product** (Phase D onward). They share Phase A's library, score-record values, and IEP integration.

## 3. Architectural commitments

Non-negotiable design constraints synthesized from thinker-canon panel + ratified by user decisions:

1. **Tier-1 IEP integration** (user choice): new `SkillVersion` entity in `intent-eval-core` kernel + new `skill-optimization-step/v1` predicate URI. The 14th canonical entity. Blocks on `iec-E12` v0.2.0 release (gated by P0 beads `uprg` Evidence Bundle compat policy + `9pi3` OTel semconv).
2. **Append-only event log; never in-place SKILL.md mutation** (Hickey #1). Each accepted edit produces a content-addressed `SkillVersion` value; "current best" is a separate mutable pointer.
3. **Multi-dimensional score records** (Hickey #5 — Goodhart in prose). Score is `(skill_hash, eval_set_hash, behavioral_score, readability_score, ...)` — never collapsed to a scalar.
4. **Shadow → canary → promote ladder, human-gated promotion** (Huyen Ch. 9). Plugin NEVER auto-writes SKILL.md on main; produces candidate values that humans review + promote.
5. **Default Haiku/Sonnet for scoring + Opus only for final validation** (Huyen economics: $9.30/pass naive, ~$370/epoch/skill — order-of-magnitude reduction by tiered routing).
6. **Eval-set bootstrap is non-optional** (Karpathy — every new skill needs a held-out set; `bootstrap` is a first-class command). Sources: (a) synthetic from SKILL.md, (b) j-rig rollout harvest, (c) human-nominated golden traces.
7. **The acceptance gate is the durable contribution; the optimizer is swappable** (Karpathy bitter-lesson check). When frontier-native skill refinement arrives, you keep the harness + gate; throw away the SkillOpt mechanism.
8. **Three-layer hook architecture from security-guidance** (Anthropic-canonical pattern). Per-edit deterministic check (no model call) + end-of-turn background review (with finding-feedback) + commit-time deeper agentic gate.
9. **Single-signer audit trail** (ISEDC pattern). Plugin proposes; human + acting CTO disposes. Read-only roles preserved.
10. **Marketing as "evals-gated skill edits" not "automated skill optimization"** (Karpathy verdict — durable framing when frontier-native lands).

## 4. Phased roadmap — MVP through full-scale

Five phases. Each ships independently. Each later phase consumes earlier-phase value artifacts.

### Phase A — Discipline library (Foundation) — ~1 week

**Goal**: Ship the value-oriented core that everything else builds on. NO hooks. NO new entity. NO plugin shape. Pure library + thin CLI.

**Deliverables**:
- New package: `@intentsolutions/skillopt-core` (npm-publish under same scope as `@intentsolutions/core`)
- API surface (8–10 functions, all pure-ish over values):

```typescript
// Value types
type SkillDocHash = Sha256
type EvalSetHash = Sha256
type ScoreRecord = { skill: SkillDocHash; evalSet: EvalSetHash;
                     behavioral: number; readability: number; ... }
type EditProposal = { parent: SkillDocHash; ops: Array<AddOp|DeleteOp|ReplaceOp>;
                      proposer_model: string; rationale: string }

// Pure operations
bootstrap(skillDoc): EvalSet
score(skillDoc, evalSet, modelTier='haiku'): ScoreRecord
propose(skillDoc, scoredRollouts, optimizerModel='sonnet'): EditProposal
apply(skillDoc, edit): SkillDocV2
accept(scoreV1, scoreV2): boolean
```

- Append-only event log at `.skillopt/log.jsonl`
- Content-addressed store at `.skillopt/store/<hash>`
- Single mutable pointer file: `.skillopt/pointers/<skill>/best`
- CLI: `skillopt bootstrap <skill>`, `skillopt score <skill> --eval-set <path>`, `skillopt propose <skill>`, `skillopt apply <proposal>`, `skillopt status <skill>`
- **Phase A pre-flight**: complete deferred old-plan items — `/gist-auditor --repo j-rig-binary-eval` and update existing j-rig gist `d1c4570a8...` to v1.1.0 content.

**Reuses existing infrastructure**:
- `j-rig score` and `j-rig optimize` already exist (`packages/cli/src/commands/{eval,optimize}.ts`); Phase A library DELEGATES scoring to j-rig
- `j-rig` `ChangeProposal` and `Experiment` types already exist; Phase A library wraps them with the value-oriented hash-chaining discipline
- `validate-skillmd` Tier 2 deterministic checks are reusable as a pre-acceptance gate
- `audit-harness emit-evidence` is the existing wrapper for in-toto Statement v1 emission; Phase A library uses it via shell-out

**Exit criteria**: ship `@intentsolutions/skillopt-core@0.1.0` to npm with sigstore provenance. Demo: `skillopt bootstrap /release` produces a valid eval set; `skillopt score /release` returns a ScoreRecord; `skillopt propose /release` returns an EditProposal; `skillopt apply` produces a SkillDocV2 value.

### Phase B — `/skill-improve` plugin v0.1.0 (refiner, hook-shaped) — ~2 weeks

**Goal**: Wrap Phase A library in a 3-layer Claude Code plugin matching the security-guidance shape. User-visible product that lives in `claude-code-plugins`.

**3-layer architecture (mirroring security-guidance)**:

```
plugins/productivity/skill-improve/
├── .claude-plugin/
│   ├── plugin.json
│   └── hooks/hooks.json
└── hooks/
    ├── pre-edit-validate.sh
    ├── end-of-turn-capture.sh
    └── commit-skill-gate.sh
```

| Layer | Hook event | Mechanism | Cost |
|---|---|---|---|
| **L1 — per-edit validation** | `PostToolUse:Edit/Write` on `SKILL.md` files | Run `validate-skillmd` Tier 2; append warning to context if fails | $0 (no model call) |
| **L2 — end-of-turn rollout-capture** | `Stop` hook | If a skill was invoked AND j-rig has scored its rollouts: append to `.skillopt/log.jsonl`. After N rollouts: fire optimizer in background, surface candidate in next-turn context | $ (Sonnet proposer; Haiku scoring) |
| **L3 — commit-time skill-readiness gate** | `PostToolUse:Bash` matcher `git commit`/`git push` | If staged diff modifies a SKILL.md: run agentic gate that reads surrounding skills + checks regression-against-rejected-buffer + (optional) shadow-validation | $$ (Opus; rate-limited per security-guidance pattern) |

**Plugin CLI surface**:
- `/skill-improve bootstrap <skill>` — create initial eval set
- `/skill-improve propose <skill>` — manual optimizer pass
- `/skill-improve shadow <skill>` — run candidate in shadow mode
- `/skill-improve promote <skill>` — promote candidate → main (human-gated)
- `/skill-improve status <skill>` — show trajectory + budget + rejected log

**MVP demo**: pick ONE existing skill (recommended: `/audit-tests` or `/validate-skillmd`); run full bootstrap → score → propose → shadow → promote cycle; produce Phase E report (md + HTML); publish as case-study blog post.

**Exit criteria**:
- Plugin published to `claude-code-plugins` marketplace at `plugins/productivity/skill-improve/`
- One real skill improved end-to-end with shipped score-delta evidence
- Phase E report (markdown + HTML) generated and published as blog post

### Phase C — Tier-1 IEP integration (kernel) — ~3–4 weeks

**Goal**: Promote `SkillVersion` to the 14th canonical entity in `intent-eval-core`. Mint `skill-optimization-step/v1` predicate URI. j-rig becomes an emitter of skill-optimization rows; intent-rollout-gate becomes a consumer.

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
  "score_record": { ... },
  "accepted_by": "actor-identity",
  "accepted_at": "rfc3339",
  "signing_mode": "staging | production",
  "rekor_log_index": "int64 | null"
}
```

- New predicate URI `https://evals.intentsolutions.io/skill-optimization-step/v1`
- Blueprint B § 7 extension documenting the new predicate body
- Companion governance: P0 bead `uprg` (Evidence Bundle compat policy) MUST land before this predicate URI is signed into production Rekor. **Phase C cannot complete until `uprg` is closed.**

**j-rig changes**:
- New CLI command `j-rig emit-skill-step` parallel to existing `j-rig emit-evidence` — emits `skill-optimization-step/v1` rows
- Existing `optimizer/` module extended to use `@intentsolutions/skillopt-core` value types

**intent-rollout-gate changes**:
- M5 substantive runtime consumes `skill-optimization-step/v1` rows as enrichment (not blocking advisory by default)

**Companion P0 dependencies**:
- `bd_000-projects-uprg` — Evidence Bundle predicate compatibility policy (BLOCKS this phase)
- `bd_000-projects-9pi3` — OTel semconv pin (BLOCKS kernel v0.3.0 ship)
- `bd_000-projects-59tx` — Release workflow failure alerting (CROSS-CUTTING)

**Exit criteria**:
- `@intentsolutions/core@0.3.0` published with `SkillVersion` entity
- `j-rig-binary-eval` ships `j-rig emit-skill-step` command
- intent-eval-lab Blueprint B § 7 extended with new predicate spec
- ISEDC Session 7 ratifies the URI namespace addition (CISO binding: must be on `evals.intentsolutions.io` not `labs.`)

### Phase D — `SkillSmith` (or final-name) creator product — ~6–8 weeks

**Goal**: Second plugin — generates NEW skills from scratch with the discipline Phase A library enforces. Must clear the SkillsBench −1.3pp negative baseline before any generated skill ships.

**Architecture**:
- Uses Phase A library as foundation
- Generation entry point: `/<NEW-NAME> create <description> --domain <area> --seed <reference-skill>?`
- Two-phase generation:
  1. **Spec phase**: generate draft SKILL.md + initial eval set from user description + optional seed skill
  2. **Train phase**: run Phase A loop (score → propose → accept) until convergence OR budget exhausted OR no improvement over N passes
- **Hard floor**: generated skill must beat `+0pp` (no-skill baseline) by ≥ 5pp on held-out before shipping

**Risk mitigations**:
- Generated skills get `confidence_tier` field (alpha/beta/stable) based on optimization passes + held-out delta
- All generated skills start as `alpha`; promotion requires real-world rollout evidence (via j-rig)
- The plugin REFUSES to ship a generated skill that fails the SkillsBench negative-baseline check

**Open product question**: separate plugin (`/skillsmith create`) or `--create` mode inside `/skill-improve`? CTO recommendation: separate plugin (easier to deprecate if SkillsBench's warning holds).

**Exit criteria**:
- 10+ test skills generated, ≥50% clearing SkillsBench positive-baseline threshold (+5pp over no-skill)
- ISEDC Session 8 ratifies marketplace publication
- Blog-post case study of one generated skill that beat the bar

### Phase E — Report production / proof-of-work deliverable spec — ongoing

**Goal**: Define the per-run deliverable shape so consumers SEE the eval ran and produced something defensible.

#### E.1 — Markdown AAR (canonical, git-versioned, machine-parseable)

Filename: `<repo>/000-docs/NNN-RL-REPT-skillopt-<skill>-<date>.md`

Template (REQUIRED sections):

```markdown
# Report — SkillOpt-Pattern Optimization of `<skill-id>`

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Skill | <skill-id> |
| Skill version (input) | sha256(...) (8-char prefix) |
| Skill version (output) | sha256(...) (8-char prefix) |
| Eval set | sha256(...) (8-char prefix) |
| Score delta | behavioral +N.Mpp; readability +N.Mpp |
| Optimization passes | N (M accepted, K rejected) |
| Compute cost | $X.XX (Haiku $X.XX; Sonnet $X.XX; Opus $X.XX) |
| Wall-clock | HH:MM:SS |
| Confidence tier | alpha | beta | stable |

## 1. Context
## 2. Eval set composition
## 3. Score trajectory
## 4. Accepted edits (replayable)
## 5. Rejected edits (audit trail)
## 6. Acceptance gate evidence (per pass)
## 7. Signed Evidence Bundle (in-toto Statement v1)
## 8. Architectural bindings
## 9. Limitations + risks
## 10. Status banding
```

#### E.2 — HTML projection (derived from markdown AAR per Hickey value-oriented projection rule)

Generated deterministically from the markdown source. Single source of truth; HTML is a view. Hosted at `evals.intentsolutions.io/reports/<skill-id>/<sha-prefix>/`. Static HTML via Hugo template (mirrors partner-portal pattern).

#### E.3 — Storage spec

| Artifact | Storage | Retention |
|---|---|---|
| Markdown AAR | `<repo>/000-docs/NNN-RL-REPT-*.md` (committed to git) | Forever |
| Signed Evidence Bundle | `<repo>/.skillopt/evidence/<sha>.json` (gitignored if signed-prod, committed if signed-staging) | Indexed by sha; orphaned GC'd after 90 days |
| HTML render | `evals.intentsolutions.io/reports/<skill-id>/<sha-prefix>/` | Pinned per version; never overwritten |
| Rekor log entry | Public sigstore Rekor | Permanent (by design) |

**Phase E exit criteria**:
- Markdown template committed to `intent-eval-lab/specs/skill-optimization-report/v1.0.0-draft/SPEC.md`
- HTML renderer shipped as part of partner-portal infrastructure
- ISEDC Session 7 ratifies the predicate URI carrying the report's canonical sha
- One real report generated end-to-end (Phase B exit-criteria demo skill)

### Phase F — MLOps scale-up (long-term, ~Q3 2026)

| Layer | Mechanism | Filed bead |
|---|---|---|
| Skill registry | SkillVersion + lineage graph | Phase C extends |
| Eval-set governance | Versioned + reviewed quarterly + adversarial-append | `iep-eval-set-governance` |
| Canary rollouts | Per-partner traffic routing | `iep-canary-rollouts` |
| A/B at partner layer | Partner pins skill version | `iep-partner-skill-pins` |
| Promotion graph | Shadow → canary-10% → canary-50% → 100% | Phase C SkillVersion + DR per transition |
| Drift policy | Weekly re-validation; event-triggered on model bump | `iep-drift-policy` |
| Cost dashboard | OTel spans + per-skill cost trajectory + alerts | Subsumes `iel-E12-attributes-pinned` (already P0 in `9pi3`) |

**Phase F triggers**: when ≥5 partners actively consume optimized skills OR ≥100 active SkillVersion records OR drift incident causes the first rollback. Until then, Phases A→E are sufficient.

## 5. Critical files to be created / modified

### NEW package (Phase A)
- `@intentsolutions/skillopt-core` — separate repo `intent-eval-platform/skillopt-core/` OR new package in j-rig monorepo (see § 7)

### `intent-eval-core/` (Phase C)
- `schemas/v1/skill-version.schema.json` — NEW entity
- `src/validators/v1/skill-version.ts` — NEW Zod validator
- `schemas/v1/skill-optimization-step.schema.json` — NEW predicate
- `schemas/v1/index.json` — register new entity + predicate
- `CHANGELOG.md` — `[0.3.0]` entry
- `package.json` — version 0.1.1 → 0.3.0 (MINOR — additive Parallel Change per `xcs4`)

### `intent-eval-lab/` (Phase C + E)
- `000-docs/012-AT-ARCH-platform-runtime-blueprint.md` — extend § 7 with `skill-optimization-step/v1`
- `000-docs/014-DR-GLOS-canonical-glossary.md` — add SkillVersion + SkillOpt-pattern + ScoreRecord + EditProposal
- `specs/skill-optimization-report/v1.0.0-draft/SPEC.md` — NEW report template spec
- `000-docs/NNN-AT-DECR-isedc-session-7-skillopt-tier1.md` — DR ratifying predicate URI + entity addition

### `j-rig-binary-eval/` (Phase C)
- `packages/cli/src/commands/emit-skill-step.ts` — NEW command
- `packages/core/src/optimizer/index.ts` — extend to use `@intentsolutions/skillopt-core`
- `CHANGELOG.md` — `[v1.2.0]` MINOR

### `claude-code-plugins/` (Phase B)
- `plugins/productivity/skill-improve/.claude-plugin/{plugin.json,hooks/hooks.json}`
- `plugins/productivity/skill-improve/hooks/{pre-edit-validate.sh,end-of-turn-capture.sh,commit-skill-gate.sh}`
- `plugins/productivity/skill-improve/skills/skill-improve/SKILL.md`
- `plugins/productivity/skill-improve/scripts/optimize-loop.ts`

### `claude-code-plugins/` (Phase D)
- `plugins/productivity/<final-creator-name>/...` — mirrors Phase B structure

## 6. Reused infrastructure (per Plan Mode discipline)

| Component | Location | Reused for |
|---|---|---|
| `/skill-creator` skill | `~/.claude/skills/skill-creator/SKILL.md` | Phase D scaffold (its `--forge` mode is prior-art) |
| `/validate-skillmd` skill | `~/.claude/skills/validate-skillmd/SKILL.md` | Phase B L1 deterministic gate (Tier 2 checks) |
| `/audit-tests` + `/implement-tests` | `~/.claude/skills/` | Phase A bootstrap (7-layer taxonomy approach) |
| `/appaudit` skill | `~/.claude/skills/appaudit/SKILL.md` | Phase E HTML render (partner-grade PDF reports) |
| `/release` skill | `~/.claude/skills/release/SKILL.md` | Phase B + D plugin releases (8-phase ceremony) |
| `/branch-protection` skill | `~/.claude/skills/branch-protection/SKILL.md` | Phase C kernel v0.3.0 protected-main push |
| `/gist-auditor` skill | `~/.claude/skills/gist-auditor/SKILL.md` | Phase A pre-flight (j-rig gist carry-over) |
| `j-rig optimizer/types.ts` | `j-rig-binary-eval/packages/core/src/optimizer/` | Phase A wraps with value-oriented hash-chains |
| `j-rig eval`/`optimize`/`check`/`emit-evidence` CLI | `j-rig-binary-eval/packages/cli/src/commands/` | Phase A DELEGATES scoring |
| `audit-harness emit-evidence` | `audit-harness/scripts/emit-evidence.sh` | in-toto Statement v1 emission |
| `SkillSnapshot` entity | `intent-eval-core/schemas/v1/skill-snapshot.schema.json` | Phase C SkillVersion extends/references (NOT duplicate) |
| `gate-result/v1` predicate | `intent-eval-core/schemas/v1/gate-result.schema.json` + Blueprint B § 7 | Phase A emits from optimization passes |
| Anthropic security-guidance | github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance | Phase B reference implementation |
| Partner-portal infrastructure | `~/000-projects/partner-portals/` | Phase E HTML hosting (new section `evals.intentsolutions.io/reports/`) |
| bd-sync three-layer mirror | `~/bin/bd-sync` | All new beads filed per discipline |
| Doc Filing Standard v4.x | `intent-eval-lab/000-docs/` + `/doc-filing` skill | Phase E markdown template |

## 7. Open questions for user (deferred to Phase A kickoff)

1. **`@intentsolutions/skillopt-core` packaging**: separate repo or new package in j-rig monorepo? **CTO recommendation: SEPARATE REPO** — independent release cadence and different audience (power-users of the IEP, not just j-rig consumers).
2. **Creator-product name**: SkillSmith / SkillMint / SkillCraft / SkillSpawn / other?
3. **Phase A target host**: same `@intentsolutions/` scope? **Recommendation: SAME SCOPE** — aligns with `@intentsolutions/core` and `@intentsolutions/audit-harness`.
4. **Phase B target skill for end-to-end demo**: `/audit-tests` (rich invocation history) or `/validate-skillmd` (meta-recursive)? **Recommendation: `/audit-tests`** for cleaner blog post; `/validate-skillmd` is the sharper IP-defense story.
5. **Phase C kernel version**: v0.2.0 (per `iec-E12`) or v0.3.0 (skip v0.2.0)? **Recommendation: v0.2.0 ships `EvidenceBundlePayload`; SkillVersion lands in v0.3.0**. Honors expand-contract Parallel Change (`xcs4`).

## 8. Risks + mitigations

| Risk | Mitigation |
|---|---|
| Frontier moves faster — SkillOpt eaten by frontier-native skill refinement in 6-12mo (Karpathy bitter-lesson) | Phase A library exposes pure-function value API; SkillOpt-specific mechanism is a pluggable strategy. When frontier-native arrives: swap strategy, keep harness. |
| Self-generated skills (Phase D) bomb in the wild — Goodhart (SkillsBench + Hickey #5) | Multi-dimensional score records. `confidence_tier` field gates marketplace publication. Hard refuse on SkillsBench negative-baseline check failure. |
| Cost runaway — naive Opus-everywhere = $11K/mo for 30 skills | Tiered routing: Haiku scoring, Sonnet proposer, Opus only validation. Hard budget cap + alert at 80%. |
| Phase C blocks on `uprg`+`9pi3` indefinitely | Phases A+B NOT blocked on Phase C — they use existing `gate-result/v1` and `SkillSnapshot` + emit via j-rig. Phase C is the polish/first-class layer. |
| Branch-protection failures on Phase C kernel release (`bj5m` pattern) | Already mitigated — j-rig adopted tag-trigger pattern (PR #80). Phase C uses same pattern in intent-eval-core release.yml. |
| Eval-set bootstrap is the unsexy 80% (Huyen) and Phase A skips it = no usable plugin | Phase A bootstrap is FIRST-CLASS. Three sources: synthetic + j-rig harvest + human-golden. All three implemented in Phase A. |
| Two-product split doubles maintenance | Phase A library is SHARED. Both plugins are thin shells over the same value API. Maintenance burden = library + 2 shells, not 2 stacks. |
| `iah-npm-publish-gap` (audit-harness git v1.1.4 vs npm v0.1.0) blocks consumer reach | Phase C must close this — audit-harness needs release.yml + first npm publish from v1.1.4 OR Phase C explicitly notes the gap. |
| Reports become brand-surface explosion if every run gets public HTML | Markdown is canonical (in git); HTML is OPT-IN per-report (defaults internal-only). Public reports gated by quality + human approval. |
| Plugin (Phase B) marketed as "automated skill optimization" → consumer expects auto-magic → trust failure | Marketing position is "evals-gated skill edits" (Karpathy). Every report shows rejected-edits buffer alongside accepted. Trust comes from showing the work. |

## 9. Verification (end-to-end exit criteria)

1. **Phase A**: `npm view @intentsolutions/skillopt-core` returns v0.1.0+ with sigstore provenance
2. **Phase B**: `/skill-improve` plugin in claude-code-plugins marketplace; ONE real skill improved end-to-end; blog post published
3. **Phase C** (gated on `uprg`+`9pi3`): `@intentsolutions/core@0.3.0` published with SkillVersion; `skill-optimization-step/v1` URI live (test signed via cosign + Rekor staging); ISEDC Session 7 DR filed
4. **Phase D**: `<creator-name>` plugin available with 10+ test-generated skills; ≥50% clear SkillsBench positive-baseline; ISEDC Session 8 DR filed
5. **Phase E**: report template at `intent-eval-lab/specs/skill-optimization-report/v1.0.0-draft/SPEC.md`; HTML renderer live at `evals.intentsolutions.io/reports/`; one real report generated end-to-end
6. **Phase F** triggers (NOT ships): when ≥5 partners consume optimized skills OR ≥100 active SkillVersion records OR first rollback incident

If any phase exit-criterion fails > 2 weeks past target: pause, file an ISEDC session, re-plan.

## 10. Stopping criteria

- Frontier ships frontier-native skill-refinement subsuming Phase A → archive Phases A–D; keep Phase E (reports) as durable interface
- Phase B end-to-end demo fails meaningful score-delta on ANY real skill → DO NOT ship Phase D
- SkillsBench negative-baseline finding REPLICATES on our skills → Phase D cancelled outright; Phase B continues
- Phase C `uprg` or `9pi3` cannot be closed → Phase C stays deferred; Phases A+B continue without first-class kernel integration

## 11. What this plan does NOT do

- Does not advance any current bead beyond the ones already filed (uprg, 9pi3, 59tx, tyck, uop6, 5qcy, 9yhe, xcs4, bj5m, q9vn, iah-npm-publish-gap, iep-gist-coverage). Phase A–F bead filing happens POST-plan-approval.
- Does not write any code. Plan mode is design-only. Implementation begins at Phase A kickoff.
- Does not name the creator product (Phase D).
- Does not commit to Phase A package location (separate repo vs monorepo).
- Does not pick Phase B demo skill (`/audit-tests` vs `/validate-skillmd`).
- Does not address broader gist-coverage work (4 missing gists) — stays under `iep-gist-coverage`.
- Does not address P6 Phase A3+ linting infrastructure.
- Does not advance the Plane / GH / bd projection inversion (`q9vn` design spike).

---

- Jeremy Longshore
intentsolutions.io
