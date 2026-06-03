# Phase A.0 Baseline Results

**Bead:** `bd_000-projects-214c.8` · **Authority:** DR-028 P0-RATIFY-3 · **Status:** RESULTS COLLECTED [SESSION 2]

---

## Executive Summary

| Item                 | Value                                                                     |
| -------------------- | ------------------------------------------------------------------------- |
| Run start            | [DATE]                                                                    |
| Run end              | [DATE]                                                                    |
| Total wall-time      | [HH:MM]                                                                   |
| Total spend          | $[X] / $200 ceiling                                                       |
| Validator commit pin | [SHA8] (must be ≥7b9eb8f)                                                 |
| **Decision verdict** | [**DESCOPE-PHASE-B** / **PROCEED-WITH-PHASE-B**]                          |
| Decision rationale   | [1-sentence: did Arm A naive-Opus lift exceed 70% of Arm B Refiner lift?] |

---

## Primary Decision Metric

The scalar decision hinges on **naive-as-fraction-of-Refiner-lift ratio** against the **70% threshold** (DR-028 P0-RATIFY-3).

### Arm A — Naive Opus In-Context (4 K-levels)

| K                | Mean score delta (pp) | 95% CI            | N specimens |
| ---------------- | --------------------- | ----------------- | ----------- |
| 0                | [X.XX]                | [X.XX – X.XX]     | 60          |
| 3                | [X.XX]                | [X.XX – X.XX]     | 60          |
| 8                | [X.XX]                | [X.XX – X.XX]     | 60          |
| 16               | [X.XX]                | [X.XX – X.XX]     | 60          |
| **Best-K (max)** | **[X.XX]**            | **[X.XX – X.XX]** | —           |

**Sparkline (ASCII):** K=0 → K=3 → K=8 → K=16 (mark best-K with `*`)

---

### Arm B — Refiner Mechanism

| Metric                                                      | Value         |
| ----------------------------------------------------------- | ------------- |
| Mean score delta (pp)                                       | [Y.YY]        |
| 95% CI                                                      | [Y.YY – Y.YY] |
| Acceptance rate (% specimens where final accept succeeded)  | [Z]%          |
| Mean iterations to final accept                             | [N.N]         |
| Rejected-edit-buffer size (max iterations hit per specimen) | [M] specimens |

---

### The Critical Ratio

| Quantity                       | Value                      | Interpretation                         |
| ------------------------------ | -------------------------- | -------------------------------------- |
| **Arm A best-K lift**          | [X.XX]pp                   | Naive Opus, best exemplar count        |
| **Arm B Refiner lift**         | [Y.YY]pp                   | Refiner's propose/accept loop          |
| **Ratio (A/B)**                | [X.XX / Y.YY = R.RR]       | —                                      |
| **70% threshold**              | 0.70 × [Y.YY]pp = [T.TT]pp | Descope cutoff                         |
| **Margin (Ratio - threshold)** | [R.RR - 0.70]              | **✓ PROCEED** if +, **✗ DESCOPE** if − |

---

## Pre-Registered Statistical Tests

**All tests pre-specified per DESIGN.md § 4 + § 6. No p-hacking. No post-hoc selection.**

### Primary Test — One-Sided t-Test (or Wilcoxon if non-normal)

**Name:** Two-sample one-sided t-test (parametric) OR Wilcoxon signed-rank test (nonparametric)

**Hypothesis:**

- **H₀:** Arm A (best-K) lift ≥ 0.70 × Arm B lift _(bitter-lesson null; descope succeeds)_
- **H₁:** Arm A (best-K) lift < 0.70 × Arm B lift _(Refiner mechanism justifies Phase B)_
- **Decision:** Reject H₀ → PROCEED-WITH-PHASE-B. Fail to reject H₀ → DESCOPE-PHASE-B.

**Python function:**

````python
# Normality check first (Shapiro-Wilk or Kolmogorov-Smirnov)
from scipy.stats import shapiro, ttest_ind, wilcoxon

# If both arms normal (p > 0.05 on Shapiro): use ttest_ind
arm_a_deltas = [...]  # 60 per-specimen score deltas
arm_b_deltas = [...]  # 60 per-specimen score deltas
t_stat, p_value_two_tail = ttest_ind(arm_a_deltas, arm_b_deltas)
p_value_one_tail = p_value_two_tail / 2 if t_stat < 0 else 1.0 - p_value_two_tail / 2

# If non-normal: use Wilcoxon signed-rank
# (pairs each Arm A specimen with matched Arm B specimen; if no match, exclude)
z_stat, p_value_one_tail = wilcoxon(arm_a_deltas, arm_b_deltas, alternative='less')
```text

**Significance level:** α = 0.05 (pre-registered DR-028)

**Report:** t-statistic [or Z-statistic], p-value, degrees-of-freedom, effect-size (Cohen's d)

---

### Stratum Interaction — Two-Way ANOVA

**Name:** Two-way ANOVA (arm × stratum)

**Design:**

- **Factor 1 (Arm):** Arm A vs Arm B (between-subjects)
- **Factor 2 (Stratum):** Global (20) vs Marketplace-Pass (20) vs Marketplace-Fail (20) (within subject pool)
- **Outcome:** score delta

**Python function:**

```python
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

# Data: DataFrame with columns [arm, stratum, score_delta]
# arm ∈ {A, B}, stratum ∈ {global, pass, fail}
model = smf.ols('score_delta ~ C(arm) + C(stratum) + C(arm):C(stratum)', data=df).fit()
anova_table = anova_lm(model, typ=2)
````

**Report:** F-statistic (arm main), F-statistic (stratum main), F-statistic (interaction), p-values, effect-size (eta-squared per term)

**Interpretation:** Heterogeneity across strata signals whether Arm A/B lift generalizes equally or is stratum-dependent.

---

### K-Sweep Diminishing Returns — Sequential Contrast (K-levels)

**Name:** Sequential contrasts (or pairwise paired t-tests with Bonferroni correction)

**Design:** Compare adjacent K levels on Arm A

- K=0 vs K=3
- K=3 vs K=8
- K=8 vs K=16

**Python function:**

````python
# Paired t-test: each of 60 specimens has 4 scores (K ∈ {0, 3, 8, 16})
from scipy.stats import ttest_rel

k_pairs = [(0, 3), (3, 8), (8, 16)]
for k1, k2 in k_pairs:
    t_stat, p_val = ttest_rel(arm_a_scores[f'K={k1}'], arm_a_scores[f'K={k2}'])
    # Bonferroni: multiply p_val by 3 (three pairwise tests)
    p_adjusted = min(p_val * 3, 1.0)
    # Report t_stat, p_adjusted, Cohen's d
```text

**Report per contrast:** t-statistic, p-value (Bonferroni-adjusted), Cohen's d

**Interpretation:** Identify the K-level with best ROI; detect if K=16 shows saturation (diminishing marginal return).

---

### Goodhart Multi-Dimensional Audit — Bonferroni-Corrected Paired Tests

**Name:** One-sided paired t-tests per dimension (5 dimensions × 2 arms), Bonferroni α-correction

**Dimensions** (per DESIGN.md § 4):

1. `marketplace_score_pct` (primary, scalar)
2. `field_completeness` (count 0–8)
3. `deprecated_field_count` (count 0–N)
4. `description_chars` (raw count)
5. `is_extras_present` (count 0–11)

**Python function:**

```python
from scipy.stats import ttest_rel
import pandas as pd

# Data: 60 specimens × 2 arms × 5 dimensions
# Flag: dimension regression (Arm A > Arm B) even when scalar ↑

bonferroni_alpha = 0.05 / 5  # α = 0.01 per dimension
results = []

for dim in ['marketplace_score_pct', 'field_completeness', 'deprecated_field_count',
            'description_chars', 'is_extras_present']:
    t_stat, p_val = ttest_rel(arm_a[dim], arm_b[dim])
    # Report regression (A higher than B, bad) with one-sided test:
    # H₀: arm_a[dim] ≤ arm_b[dim] vs H₁: arm_a[dim] > arm_b[dim]
    p_one_sided = p_val / 2 if t_stat > 0 else 1.0 - p_val / 2
    results.append({
        'dimension': dim,
        't_stat': t_stat,
        'p_bonf': min(p_one_sided * 5, 1.0),
        'regression_risk': 'YES' if (t_stat > 0 and p_one_sided < bonferroni_alpha) else 'NO'
    })
````

**Report:** Table with all 5 dimensions, t-statistic, p-value (Bonferroni-adjusted), regression-flag

**Interpretation:** Surface any dimension where Arm A regresses (e.g., fewer extras, shorter description) even if marketplace_score_pct↑. Alerts to Goodhart's Law capture.

---

### Held-Out Generalization — Optional Exploratory Test

**Name:** Out-of-sample performance on held-out 20-set (if time/budget permits)

**Design:** Run Arm A (best-K) and Arm B on the reserved 20 specimens NOT seen during training/calibration.

**Python function:**

````python
# Compare held-out-set lift to main-sample lift
# If held-out lift << main-sample lift → fixture-overfitting risk
from scipy.stats import mannwhitneyu

u_stat, p_val = mannwhitneyu(main_sample_deltas, held_out_deltas, alternative='two-sided')
# Report: mean delta main vs held-out, p-value
```text

**Report:** Mean lift on main 60 vs mean lift on held-out 20, Mann-Whitney U p-value

**Interpretation:** If p < 0.05 and held-out << main, flag overfitting risk for Phase B design.

---

## Per-Arm Trajectories

### Arm A — K-Sweep (Naive Opus)

**Score delta by K (all 60 specimens):**

````

K=0: [MEAN]pp ± [SD]pp; range [MIN]–[MAX]
K=3: [MEAN]pp ± [SD]pp; range [MIN]–[MAX]
K=8: [MEAN]pp ± [SD]pp; range [MIN]–[MAX]
K=16: [MEAN]pp ± [SD]pp; range [MIN]–[MAX]

ASCII sparkline (sample deltas):
0────○────○────○────16
3 8

```text

**Per-stratum breakdown (Arm A best-K):**

| Stratum                      | N      | Mean Δ (pp) | Median Δ (pp) | SD      |
| ---------------------------- | ------ | ----------- | ------------- | ------- |
| Global (~/.claude/skills)    | 20     | [X]         | [X]           | [X]     |
| Marketplace-Pass (score ≥80) | 20     | [X]         | [X]           | [X]     |
| Marketplace-Fail (score <80) | 20     | [X]         | [X]           | [X]     |
| **Overall**                  | **60** | **[X]**     | **[X]**       | **[X]** |

---

### Arm B — Refiner Mechanism Behavior

**Acceptance trajectory (first-pass through max 3 iterations):**

| Iteration                  | Acceptance count     | Cumulative accept | Rejection reason (top 3)                             |
| -------------------------- | -------------------- | ----------------- | ---------------------------------------------------- |
| 1 (initial propose)        | [M] of 60            | [M]/60            | `[reason_1]` (N), `[reason_2]` (N), `[reason_3]` (N) |
| 2 (re-propose w/ feedback) | [M] of [N remaining] | [M]/60            | [top 3]                                              |
| 3 (final attempt)          | [M] of [N remaining] | [M]/60            | [top 3]                                              |
| **Never accepted**         | [M] specimens        | [M]/60 total      | [top 3 reasons across all attempts]                  |

**Iterations-to-accept distribution:**

```

1 iteration: [M] specimens (NN%)
2 iterations: [M] specimens (NN%)
3 iterations: [M] specimens (NN%)
Never: [M] specimens (NN%)

```text

**Rejected-edit-buffer utilization:**

| Specimen ID (sample) | Iteration where accept occurred | Reason if rejected (N=3 iterations) | Final score delta (pp) |
| -------------------- | ------------------------------- | ----------------------------------- | ---------------------- |
| [exemplar]           | 2                               | (accepted)                          | [X.XX]                 |
| [exemplar]           | 3                               | Regression in `field_completeness`  | [Y.YY]                 |
| [exemplar]           | Never                           | Reject-buffer exhausted (3/3)       | [0.00]                 |

---

## Cost Accounting

### Spend Breakdown

| Arm       | Component                                  | Per-specimen | N specimens | Subtotal   |
| --------- | ------------------------------------------ | ------------ | ----------- | ---------- |
| **A**     | Prompt + Opus-4.7 call (K=0)               | $[X]         | 60          | $[X]       |
| **A**     | Prompt + Opus-4.7 call (K=3)               | $[X]         | 60          | $[X]       |
| **A**     | Prompt + Opus-4.7 call (K=8)               | $[X]         | 60          | $[X]       |
| **A**     | Prompt + Opus-4.7 call (K=16)              | $[X]         | 60          | $[X]       |
| **A**     | Validator runs (4 K-values × 60)           | $[X]         | 240         | $[X]       |
| **B**     | Refiner propose/accept loop (avg 1.8 iter) | $[X]         | 60          | $[X]       |
| **B**     | Validator runs (1 final)                   | $[X]         | 60          | $[X]       |
| —         | —                                          | —            | —           | —          |
| **TOTAL** | —                                          | —            | —           | **$[XXX]** |

### Cost-Efficiency Frontier

| Metric                                            | Value                   |
| ------------------------------------------------- | ----------------------- |
| Cost per percentage-point of lift (Arm A best-K)  | $[X]/pp                 |
| Cost per percentage-point of lift (Arm B Refiner) | $[Y]/pp                 |
| Arm A cost-efficiency ratio (A/B)                 | [ratio]                 |
| Remaining budget vs spend                         | $[200 - spend] headroom |

---

## Goodhart Audit — Per-Dimension Regression Report

**Bonferroni α = 0.01 per dimension (5-way correction of 0.05)**

| Dimension                | Arm A mean | Arm B mean | Δ (A−B) | t-stat | p-Bonf | Regression? |
| ------------------------ | ---------- | ---------- | ------- | ------ | ------ | ----------- |
| `marketplace_score_pct`  | [XX]       | [YY]       | [ΔZ]    | [t]    | [p]    | **PRIMARY** |
| `field_completeness`     | [X]        | [Y]        | [Δ]     | [t]    | [p]    | [YES/NO]    |
| `deprecated_field_count` | [X]        | [Y]        | [Δ]     | [t]    | [p]    | [YES/NO]    |
| `description_chars`      | [X]        | [Y]        | [Δ]     | [t]    | [p]    | [YES/NO]    |
| `is_extras_present`      | [X]        | [Y]        | [Δ]     | [t]    | [p]    | [YES/NO]    |

**Regressions flagged:** [List any dimension where Arm A is WORSE than Arm B and p < 0.01]

**Interpretation:** A regression in a single dimension (e.g., "fewer IS-extras added") that is masked by a gain in marketplace_score_pct is a Goodhart's Law warning. Itemize each one.

---

## Threats to Validity (Pre-Registered per DESIGN.md § 8)

1. **Single judge (validator-only):** No evaluation against live Claude Code user rollouts. Generalization to real human behavior TBD. _Future work: user studies post-Phase B ship._

2. **Static eval set:** No user behavior dynamics (skill popularity trends, evolving marketplace standards, seasonal demand shifts). _Future work: rolling-window re-evaluation quarterly._

3. **Single skill demo:** Generalization to other plugin types (`/plugin-manifest`, `/agent-definition`, `/mcp-config`, `/hook-config`) unproven. _Future work: Phase B.2 multi-skill sweep._

4. **Bitter-lesson risk (AC-7):** Frontier self-generation (e.g., Claude 4.8 or later) may obviate this mechanism entirely by the time Phase B ships (nominal Q4 2026). _Mitigation: Phase B is bandwidth-gated, not time-gated; re-evaluate monthly against frontier release notes._

5. **Exemplar pool static:** K ∈ {0, 3, 8, 16} exemplars are fixed throughout. In-distribution exemplar drift (if marketplace evolves) not captured. _Future work: continuous exemplar refresh policy._

---

## Decision Audit Trail

**DR-028 P0-RATIFY-3 citation:** ["If naive-Opus-in-context achieves > 70% of projected Refiner lift on `/validate-skillmd`, DESCOPE Phase B mechanism. Result is PUBLISHED as a blog post REGARDLESS of outcome."]

**Projected lift (pre-registered):** 1.5pp marketplace_score_pct (acting CTO decision 2026-05-28; filed in DR-028 amendment addendum)

**Descope threshold (derived):** 0.70 × 1.5pp = 1.05pp

**Verdict date:** [DATE DECISION MADE]

**VP DevRel binding (2026-05-27):** Publish blog post regardless of DESCOPE or PROCEED outcome. _Two blog-post drafts required: one for each outcome (see § Blog Post Hooks below)._

**Plane issue track:** LAB-6 (IEL-CONV-1 umbrella) + LAB-82 (Decision Record for outcome)

**GitHub issue:** `intent-eval-lab#81` (bead `bd_000-projects-214c.8` mirror)

---

## Blog Post Hooks (VP DevRel Binding — Publish Regardless)

### Outcome A: DESCOPE-PHASE-B

**Framing:** "The bitter-lesson check that saved us 3 months of engineering"

**Draft headline options:**

1. "We built an eval-gated skill refiner. Then Opus in-context did 70% of the work."
2. "Frontier models are catching up faster than we build for them."
3. "Why we killed Phase B of a $35k evaluation platform."

**1-page outline:**

- Hook: "We ran a pre-registered null-hypothesis test. The null won."
- Setup: Refiner mechanism was justified by projected 1.5pp lift. Opus-in-context achieved 1.0pp+ (70%) solo.
- Insight: The bitter-lesson pattern from scaling (Karpathy et al., openai.com/research) predicts this. Frontier models compress the innovation curve.
- Action: Pivoted the Phase B FTE-weeks to the durable contribution (acceptance gate, AC-7).
- Lesson: Pre-register. Run null-hypothesis tests. Let data kill ideas fast.

---

### Outcome B: PROCEED-WITH-PHASE-B

**Framing:** "Why eval-gated SKILL.md edits actually matter — empirical proof"

**Draft headline options:**

1. "Naive models can't close the gap. Here's why the Refiner mechanism works."
2. "70% isn't enough. The last 30% is where the engineering lives."
3. "Evidence-bundle gating unlocked a 1.5pp lift we couldn't get any other way."

**1-page outline:**

- Hook: "We tested the null hypothesis. It failed spectacularly."
- Setup: Opus-in-context (best-K) achieved X pp; Refiner mechanism achieved Y pp. Y − X > 1.05pp.
- Insight: The gap is systematic: propose/accept gates enforce strict improvement; rejected-buffer iterations compound corrections.
- Spotlight: Goodhart audit shows Refiner doesn't game the metric — gains are real across all 5 dimensions.
- Action: Phase B ships on schedule; roadmap includes multi-skill validation (QSSS, agents, MCPs).
- Lesson: Simple baseline tests prevent false confidence. This mechanism is real.

---

## Next Steps (Session 3 preparation)

1. **AAR:** File `005-AA-AACR-phase-a0-baseline-aar-<date>.md` documenting execution, surprises, and recommendations for Phase B.
2. **Bead closure:** `bd-sync close bd_000-projects-214c.8 -r "RESULTS.md complete; decision verdict [DESCOPE/PROCEED]"`.
3. **ISEDC Session 8 (outcome-specific):**
   - If DESCOPE: file ISEDC Session 8 decision record on Phase B retirement + FTE reallocation.
   - If PROCEED: file ISEDC Session 8 decision record on Phase B go-live + timeline.
4. **Blog draft:** Use the headline + outline from § Blog Post Hooks; expand to 1000 words; land on `startaitools.com` or `jeremylongshore.com` per VP DevRel direction.
5. **Plan 030 (follow-on):** Update master plan or file addendum based on outcome.

---

— Jeremy Longshore
intentsolutions.io
```
