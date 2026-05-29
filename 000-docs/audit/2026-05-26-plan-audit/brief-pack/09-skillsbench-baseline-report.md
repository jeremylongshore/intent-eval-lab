# SkillsBench — Baseline Finding Digest (Brief Pack Doc 09)

**Paper:** "SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks"
**arXiv ID:** 2602.12670 (v3)
**Submitted:** 2026-02-13 (final: 2026-03-13)
**Authors:** Xiangyi Li, Wenbo Chen, Yimin Liu, Shenghan Zheng, Xiaokun Chen + 36 collaborators
**Verification:** WebFetched 2026-05-27 against `arxiv.org/abs/2602.12670` — abstract and key findings extracted

## Why this doc is in the brief pack

Plan 027 § 2 + Phase D ("defer indefinitely") + the entire IP-defense argument for `claude-code-plugins`'s 30+ human-curated skills are anchored on the SkillsBench finding. Panel seats need access to the actual finding to evaluate whether the Phase D deferral is sound.

## Verbatim findings (from abstract)

| Claim | Source |
|---|---|
| "Curated Skills raise average pass rate by **+16.2 percentage points**" | Abstract |
| Effects range from **+4.5pp (Software Engineering) to +51.9pp (Healthcare)** | Abstract — domain variability |
| **16 of 84 tasks demonstrated performance decrements** with Skills | Abstract — negative outcomes per task |
| "Self-generated Skills **provide no benefit on average**, indicating models struggle authoring procedural knowledge they would benefit from using" | Abstract |
| 7 agent-model configurations × 7,308 trajectories × 86 tasks × 11 domains | Methodology |

## Methodology shape

Three conditions tested:
1. Baseline (no Skills)
2. Curated Skills
3. Self-generated Skills

Skills package size finding: "focused Skills packages (2-3 modules) outperformed comprehensive documentation."

Cross-scale finding: "smaller models equipped with Skills matched larger models without them."

## Discrepancy with Plan 027

| Plan 027 claim | SkillsBench finding | Verdict |
|---|---|---|
| "+16.2pp on average across 7 model-harness configurations" | "+16.2 percentage points" + "7 agent-model configurations" | ✅ verbatim |
| "Self-generated Skills … −1.3pp on average compared to the no-Skills baseline" | "Self-generated Skills provide **no benefit on average**" | ⚠️ over-specific — plan cites −1.3pp; paper abstract says "no benefit." The −1.3pp figure may be in the paper body (not extracted in this digest), but the plan's load-bearing framing should soften to "no benefit on average" if the −1.3pp cannot be substantiated post-full-PDF-fetch. |
| "human-curated domain expertise that models cannot reliably self-generate" | Implicit in "no benefit" finding | ✅ defensible |

## What this means for Plan 027 Phase D ("defer indefinitely")

The SkillsBench finding **does substantiate** the high-level Phase D rationale: self-generated skills underperform vs human-curated. The IP-defense argument for `claude-code-plugins`'s 30+ human-curated skills holds.

But the **specific −1.3pp figure** quoted in the plan is not in the abstract. Either:
- (a) the −1.3pp figure is in the paper body (likely — abstract typically omits magnitudes), and the plan can keep it after a full-PDF fetch confirms
- (b) the −1.3pp was extrapolated by the plan author and should be softened to "no benefit on average per the abstract"

CTO call deferred to the panel — likely a Huyen seat finding.

## Caveats per the paper

- Significant variability in how Skills transfer across domains
- Domain-blanket applications may prove ineffective
- 16/84 tasks regressed (~19% — non-trivial failure rate even with curated Skills)

## Action items for Plan Audit panel

1. Huyen seat — evaluate whether "+16.2pp average" with "16/84 regressing" is a sound basis for the Phase A acceptance gate design (strict-improvement-on-all-dimensions). The regression rate suggests strict-on-all may be too strict.
2. Karpathy seat — the "self-generated provides no benefit" finding is a bitter-lesson alarm for Phase D timing. Phase D deferral should be re-evaluated each frontier-model release.
3. Lamport seat — verify the −1.3pp specific claim survives a full-PDF read; if not, amend plan AC-driving language.
