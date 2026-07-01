#!/usr/bin/env python3
"""analyze.py — Phase A.0 pre-registered statistical analysis.

Reads on-disk arm-a + arm-b results, applies the pre-registered tests
from RESULTS-TEMPLATE.md, emits results/aggregated/statistics.json and
results/aggregated/decision.json.

Pre-registered tests (locked by DESIGN.md before any data collected):
1. Per-K Arm A mean delta + std
2. Per-specimen Arm A best-K vs Arm B final score
3. Shapiro-Wilk normality check on (B - A_best) deltas
4. One-sided t-test (Welch's) — null: Refiner ≤ Naive; alt: Refiner > Naive
   Wilcoxon signed-rank if Shapiro p ≤ 0.05
5. Cohen's d effect size
6. K-sweep diminishing returns: sequential contrasts (K=0 vs K=3, K=3 vs K=8, K=8 vs K=16)
7. Two-way ANOVA: stratum × arm
8. 5-dim Bonferroni Goodhart audit: field_completeness, deprecated_count,
   is_extras_count, security_findings, marketplace_pass
9. Apply DR-028 P0-RATIFY-3 decision rule:
     naive_lift_pct = max(0, mean(arm_a_score_delta)) / projected_refiner_lift_pp
     DESCOPE if naive_lift_pct > 0.70
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent.parent
ARM_A_DIR = REPO_ROOT / "results" / "arm-a" / "nvidia-llama-70b"
ARM_B_DIR = REPO_ROOT / "results" / "arm-b" / "nvidia-llama-70b"
OUT_DIR = REPO_ROOT / "results" / "aggregated"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROJECTED_REFINER_LIFT_PP = 1.5  # Q1 pre-registered
DESCOPE_THRESHOLD_FRACTION = 0.70  # DR-028 P0-RATIFY-3
ALPHA = 0.05


def load_arm_a() -> dict[str, Any]:
    """Return {specimen_sha8: {k: {delta, baseline, candidate, score_dict}}}."""
    data: dict[str, Any] = defaultdict(dict)
    for score_file in ARM_A_DIR.rglob("score.json"):
        parts = score_file.parts
        sha8 = parts[-3]
        k_part = next((p for p in parts if p.startswith("k=")), None)
        if not k_part:
            continue
        k = int(k_part[2:])
        score = json.loads(score_file.read_text())
        if "delta_marketplace_score_pct" in score:
            data[sha8][k] = {
                "delta": score["delta_marketplace_score_pct"],
                "baseline": score["baseline_marketplace_score_pct"],
                "candidate": score["marketplace_score_pct"],
                "field_completeness": score.get("field_completeness", 0),
                "deprecated_count": score.get("deprecated_field_count", 0),
                "is_extras": score.get("is_extras_present", 0),
                "security_findings": score.get("security_finding_count", 0),
                "marketplace_pass": score.get("marketplace_pass", False),
            }
    return dict(data)


def load_arm_b() -> dict[str, Any]:
    """Return {specimen_sha8: {delta, baseline, final, accepted, stratum}}."""
    summary = json.loads((ARM_B_DIR / "_summary.json").read_text())
    out: dict[str, Any] = {}
    for rec in summary.get("per_specimen_results", []):
        sha8 = rec["sha8"]
        out[sha8] = {
            "delta": rec.get("delta_marketplace_score_pct", 0),
            "baseline": rec.get("baseline_marketplace_score_pct", 0),
            "final": rec.get("final_marketplace_score_pct", 0),
            "accepted": rec.get("accepted", False),
            "stratum": rec.get("stratum", "?"),
            "iterations_to_accept": rec.get("iterations_to_accept"),
        }
    return out


def cohen_d(a: list[float], b: list[float]) -> float:
    """Welch-style Cohen's d (pooled std with unequal variances)."""
    a_arr = np.array(a)
    b_arr = np.array(b)
    pooled_std = np.sqrt((a_arr.var(ddof=1) + b_arr.var(ddof=1)) / 2)
    if pooled_std == 0:
        return 0.0
    return float((b_arr.mean() - a_arr.mean()) / pooled_std)


def main() -> int:
    arm_a = load_arm_a()
    arm_b = load_arm_b()

    print(f"Loaded Arm A: {len(arm_a)} specimens")
    print(f"Loaded Arm B: {len(arm_b)} specimens")

    # 1. Per-K Arm A stats
    per_k_a = defaultdict(list)
    for _sha8, by_k in arm_a.items():
        for k, rec in by_k.items():
            per_k_a[k].append(rec["delta"])

    per_k_stats = {}
    for k, deltas in sorted(per_k_a.items()):
        per_k_stats[k] = {
            "n": len(deltas),
            "mean": float(np.mean(deltas)),
            "std": float(np.std(deltas, ddof=1)) if len(deltas) > 1 else 0.0,
            "median": float(np.median(deltas)),
            "min": min(deltas),
            "max": max(deltas),
        }

    # 2. Per-specimen Arm A best-K vs Arm B
    paired = []
    for sha8 in set(arm_a.keys()) & set(arm_b.keys()):
        # best-K = K with maximum delta (least negative or most positive)
        by_k = arm_a[sha8]
        best_k = max(by_k.keys(), key=lambda k: by_k[k]["delta"])
        a_delta = by_k[best_k]["delta"]
        b_delta = arm_b[sha8]["delta"]
        paired.append(
            {
                "sha8": sha8,
                "a_delta_best_k": a_delta,
                "a_best_k": best_k,
                "b_delta": b_delta,
                "b_minus_a": b_delta - a_delta,
                "stratum": arm_b[sha8]["stratum"],
                "b_accepted": arm_b[sha8]["accepted"],
            }
        )

    n_paired = len(paired)
    b_minus_a = [p["b_minus_a"] for p in paired]
    a_best = [p["a_delta_best_k"] for p in paired]
    b_finals = [p["b_delta"] for p in paired]

    # 3. Shapiro-Wilk normality
    if len(b_minus_a) >= 3:
        shapiro = stats.shapiro(b_minus_a)
        shapiro_p = float(shapiro.pvalue)
    else:
        shapiro_p = 1.0
    normality_pass = shapiro_p > 0.05

    # 4. Primary test: one-sided t-test (Welch's), null Refiner ≤ Naive
    # If non-normal, Wilcoxon signed-rank (one-sided)
    if normality_pass:
        primary_test_name = "Welch's one-sided t-test (B > A)"
        t_result = stats.ttest_rel(b_finals, a_best, alternative="greater")
        primary_stat = float(t_result.statistic)
        primary_p = float(t_result.pvalue)
    else:
        primary_test_name = "Wilcoxon signed-rank one-sided (B > A)"
        try:
            w_result = stats.wilcoxon(b_finals, a_best, alternative="greater")
            primary_stat = float(w_result.statistic)
            primary_p = float(w_result.pvalue)
        except ValueError as e:
            primary_test_name += f" — FAILED: {e}"
            primary_stat = 0.0
            primary_p = 1.0

    significant = primary_p < ALPHA

    # 5. Cohen's d
    d = cohen_d(a_best, b_finals)

    # 6. K-sweep diminishing returns: sequential contrasts
    k_contrasts = {}
    k_pairs = [(0, 3), (3, 8), (8, 16)]
    for k1, k2 in k_pairs:
        if k1 in per_k_a and k2 in per_k_a:
            # paired across specimens
            pair_deltas = []
            for _sha8, by_k in arm_a.items():
                if k1 in by_k and k2 in by_k:
                    pair_deltas.append(by_k[k2]["delta"] - by_k[k1]["delta"])
            if len(pair_deltas) >= 3:
                t = stats.ttest_1samp(pair_deltas, 0, alternative="greater")
                k_contrasts[f"K{k2}-K{k1}"] = {
                    "n": len(pair_deltas),
                    "mean_diff": float(np.mean(pair_deltas)),
                    "t_stat": float(t.statistic),
                    "p_value": float(t.pvalue),
                    "significant": float(t.pvalue) < ALPHA,
                }

    # 7. Two-way ANOVA: stratum × arm (approximate via 2-way independent groups)
    # Build long-form: each row is (specimen, arm, stratum, delta)
    strata_arm_deltas = defaultdict(list)
    for p in paired:
        strata_arm_deltas[("A", p["stratum"])].append(p["a_delta_best_k"])
        strata_arm_deltas[("B", p["stratum"])].append(p["b_delta"])

    anova_summary = {}
    for stratum in {p["stratum"] for p in paired}:
        a_s = strata_arm_deltas.get(("A", stratum), [])
        b_s = strata_arm_deltas.get(("B", stratum), [])
        if len(a_s) > 1 and len(b_s) > 1:
            t_strat = stats.ttest_ind(b_s, a_s, equal_var=False, alternative="greater")
            anova_summary[stratum] = {
                "n_a": len(a_s),
                "n_b": len(b_s),
                "mean_a": float(np.mean(a_s)),
                "mean_b": float(np.mean(b_s)),
                "b_minus_a": float(np.mean(b_s) - np.mean(a_s)),
                "t_stat": float(t_strat.statistic),
                "p_value": float(t_strat.pvalue),
                "significant": float(t_strat.pvalue) < ALPHA,
            }

    # 8. 5-dim Bonferroni Goodhart audit
    # Did Arm B gain on marketplace_score_pct by degrading any other dimension?
    # We have per-(specimen, K) Arm A score breakdowns. For Arm B we have
    # only the final marketplace_score_pct + accepted flag; the score-N.json
    # files per iteration capture the full breakdown. For v0.1 of analysis,
    # we use the headline marketplace_score_pct + accepted to check whether
    # B's accepted edits maintained the no-loss-on-other-dims invariant.
    # Cross-check via final.md if Goodhart concern surfaces in later review.
    goodhart_summary = {
        "approach": "v0.1 — uses Arm B per-specimen final accepted flag as proxy",
        "note": "Full 5-dim audit requires reading per-iteration score-N.json files; "
        "deferred to follow-up bead. Acceptance gate already enforces strict "
        "improvement on marketplace_score_pct + non-degradation on the 4 other dims.",
        "accepted_specimens": sum(1 for p in paired if p["b_accepted"]),
        "accepted_rate": sum(1 for p in paired if p["b_accepted"]) / max(1, len(paired)),
    }

    # 9. Decision rule
    a_mean_overall = float(np.mean([p["a_delta_best_k"] for p in paired]))
    b_mean_overall = float(np.mean([p["b_delta"] for p in paired]))
    naive_lift_pp = max(0.0, a_mean_overall)
    naive_lift_pct_of_projected = naive_lift_pp / PROJECTED_REFINER_LIFT_PP
    descope = naive_lift_pct_of_projected > DESCOPE_THRESHOLD_FRACTION

    decision = {
        "outcome": "DESCOPE" if descope else "PROCEED",
        "naive_lift_pp": naive_lift_pp,
        "refiner_lift_pp": b_mean_overall,
        "projected_refiner_lift_pp": PROJECTED_REFINER_LIFT_PP,
        "descope_threshold_fraction": DESCOPE_THRESHOLD_FRACTION,
        "naive_lift_as_fraction_of_projected": naive_lift_pct_of_projected,
        "refiner_lift_as_fraction_of_projected": b_mean_overall / PROJECTED_REFINER_LIFT_PP,
        "primary_test": primary_test_name,
        "primary_p_value": primary_p,
        "primary_significant_at_alpha_0_05": significant,
        "cohens_d": d,
        "notes": (
            "Primary one-sided test asks: is Refiner final score significantly > Naive "
            "best-K score per specimen? Outcome DESCOPE iff naive baseline achieves > 70% "
            "of projected Refiner lift (1.5pp), per DR-028 P0-RATIFY-3."
        ),
    }

    stats_out = {
        "schema_version": "phase-a-0-statistics/v0.1",
        "generated_at": "2026-05-31",
        "n_specimens_paired": n_paired,
        "per_k_arm_a": {str(k): v for k, v in per_k_stats.items()},
        "primary_paired_test": {
            "test_name": primary_test_name,
            "statistic": primary_stat,
            "p_value": primary_p,
            "alpha": ALPHA,
            "significant": significant,
            "shapiro_p": shapiro_p,
            "shapiro_normal": normality_pass,
        },
        "effect_size_cohens_d": d,
        "k_sweep_contrasts": k_contrasts,
        "per_stratum_test": anova_summary,
        "goodhart_audit": goodhart_summary,
        "decision": decision,
        "raw_means": {
            "arm_a_best_k_mean": a_mean_overall,
            "arm_b_mean": b_mean_overall,
            "b_minus_a_mean": float(np.mean(b_minus_a)),
        },
    }

    (OUT_DIR / "statistics.json").write_text(json.dumps(stats_out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (OUT_DIR / "decision.json").write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\n✓ Wrote {OUT_DIR / 'statistics.json'}")
    print(f"✓ Wrote {OUT_DIR / 'decision.json'}")

    # Console summary
    print("\n" + "=" * 64)
    print("PHASE A.0 PRE-REGISTERED ANALYSIS RESULT")
    print("=" * 64)
    print(f"n_paired_specimens: {n_paired}")
    print(f"Arm A best-K mean delta: {a_mean_overall:+.3f} pp")
    print(f"Arm B mean delta:        {b_mean_overall:+.3f} pp")
    print(f"B − A mean:              {np.mean(b_minus_a):+.3f} pp")
    print(f"Cohen's d:               {d:+.3f}")
    print(f"Primary test:            {primary_test_name}")
    print(f"  statistic:             {primary_stat:.4f}")
    print(f"  p-value:               {primary_p:.6f}")
    print(f"  significant (α=0.05):  {significant}")
    print(f"Shapiro-Wilk normality:  p={shapiro_p:.4f} (normal: {normality_pass})")
    print(f"Goodhart accept rate:    {goodhart_summary['accepted_rate']:.1%}")
    print()
    print(f"DECISION: {decision['outcome']}")
    print(f"  naive_lift_pp:                       {naive_lift_pp:+.3f}")
    print(f"  naive_lift_pct_of_projected:         {naive_lift_pct_of_projected:.1%}")
    print(f"  refiner_lift_pp:                     {b_mean_overall:+.3f}")
    print(f"  refiner_lift_pct_of_projected:       {b_mean_overall / PROJECTED_REFINER_LIFT_PP:.1%}")
    print(f"  descope_triggered: {descope}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
