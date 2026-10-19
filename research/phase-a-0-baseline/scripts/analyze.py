#!/usr/bin/env python3
"""Analyze a complete Phase A.0 cohort without overwriting historical evidence.

Retains the implemented estimators: Shapiro on paired differences; paired
one-sided t-test for normal differences, otherwise one-sided signed rank;
pooled effect size; unadjusted K contrasts; independent Welch tests per stratum.
These differ from parts of RESULTS-TEMPLATE.md. The accepted-flag summary is
not a five-dimension Goodhart audit. See README for the unresolved methodology
and historical-baseline review. A threshold result does not ratify those gaps.

The DR-028 mechanical rule remains max(0, mean(A best-K delta)) / 1.5 > 0.70.
Missing, inconsistent or non-finite evidence cannot produce a decision.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parent.parent
ARM_A_DIR = REPO_ROOT / "results" / "arm-a" / "nvidia-llama-70b"
ARM_B_DIR = REPO_ROOT / "results" / "arm-b" / "nvidia-llama-70b"
OUT_DIR = REPO_ROOT / "results" / "aggregated"
MANIFEST = REPO_ROOT / "corpus" / "manifest.json"
K_VALUES = {0, 3, 8, 16}

PROJECTED_REFINER_LIFT_PP = 1.5  # Q1 pre-registered
DESCOPE_THRESHOLD_FRACTION = 0.70  # DR-028 P0-RATIFY-3
ALPHA = 0.05


class AnalysisInputError(ValueError):
    """Inputs cannot support the registered complete-cohort decision."""


def read_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise AnalysisInputError(f"{path}: non-finite JSON number {value}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, item in pairs:
            if key in result:
                raise AnalysisInputError(f"{path}: duplicate JSON key {key}")
            result[key] = item
        return result

    try:
        value = json.loads(path.read_text(), parse_constant=reject_constant, object_pairs_hook=unique_object)
        # Also catches numeric overflow such as 1e999, which parse_constant does not.
        json.dumps(value, allow_nan=False)
        return value
    except (OSError, ValueError) as exc:
        raise AnalysisInputError(f"Cannot read finite JSON from {path}: {exc}") from exc


def number(record: dict[str, Any], key: str) -> float:
    value = record.get(key)
    if isinstance(value, bool) or not isinstance(value, int | float) or abs(value) > 100 or not math.isfinite(value):
        raise AnalysisInputError(f"{key} must be a finite number")
    return float(value)


def measurement(record: Any, final_key: str) -> tuple[float, float, float]:
    if not isinstance(record, dict):
        raise AnalysisInputError("Score record must be an object")
    baseline = number(record, "baseline_marketplace_score_pct")
    final = number(record, final_key)
    delta = number(record, "delta_marketplace_score_pct")
    if not (0 <= baseline <= 100 and 0 <= final <= 100):
        raise AnalysisInputError("Scores must be between 0 and 100")
    if not math.isclose(final - baseline, delta, rel_tol=0, abs_tol=1e-9):
        raise AnalysisInputError("Score delta does not equal final minus baseline")
    return baseline, final, delta


def load_arm_a() -> dict[str, Any]:
    """Return {specimen_sha8: {k: {delta, baseline, candidate, score_dict}}}."""
    data: dict[str, Any] = defaultdict(dict)
    for score_file in sorted(ARM_A_DIR.rglob("score.json")):
        parts = score_file.relative_to(ARM_A_DIR).parts
        if len(parts) != 3 or parts[1] not in {f"k={k}" for k in K_VALUES}:
            raise AnalysisInputError(f"Unexpected Arm A score path: {score_file}")
        sha8, k = parts[0], int(parts[1][2:])
        score = read_json(score_file)
        baseline, candidate, delta = measurement(score, "marketplace_score_pct")
        data[sha8][k] = {
            "delta": delta,
            "baseline": baseline,
            "candidate": candidate,
            "field_completeness": score.get("field_completeness", 0),
            "deprecated_count": score.get("deprecated_field_count", 0),
            "is_extras": score.get("is_extras_present", 0),
            "security_findings": score.get("security_finding_count", 0),
            "marketplace_pass": score.get("marketplace_pass", False),
        }
    return dict(data)


def load_arm_b() -> dict[str, Any]:
    """Return {specimen_sha8: {delta, baseline, final, accepted, stratum}}."""
    summary = read_json(ARM_B_DIR / "_summary.json")
    if not isinstance(summary, dict) or not isinstance(summary.get("per_specimen_results"), list):
        raise AnalysisInputError("Arm B summary must contain per_specimen_results")
    if summary.get("dry_run") is True or summary.get("error_count", 0) != 0:
        raise AnalysisInputError("Arm B summary contains dry-run data or errors")
    out: dict[str, Any] = {}
    for rec in summary.get("per_specimen_results", []):
        baseline, final, delta = measurement(rec, "final_marketplace_score_pct")
        sha8 = rec.get("sha8")
        if not isinstance(sha8, str) or not sha8 or sha8 in out:
            raise AnalysisInputError("Arm B specimen IDs must be present and unique")
        if (
            not isinstance(rec.get("accepted"), bool)
            or not isinstance(rec.get("stratum"), str)
            or rec["stratum"] not in {"A", "B", "C"}
        ):
            raise AnalysisInputError(f"Arm B {sha8} needs an accepted boolean and registered stratum")
        out[sha8] = {
            "delta": delta,
            "baseline": baseline,
            "final": final,
            "accepted": rec["accepted"],
            "stratum": rec["stratum"],
            "iterations_to_accept": rec.get("iterations_to_accept"),
        }
    return out


def validate_cohort(arm_a: dict[str, Any], arm_b: dict[str, Any]) -> None:
    """A decision requires the registered 60 specimens and all four K values.

    DESIGN section 6 permits reporting failed/excluded samples, but exclusions
    cannot silently become a successful complete-experiment decision here.
    """
    manifest = read_json(MANIFEST)
    strata = manifest.get("strata") if isinstance(manifest, dict) else None
    if not isinstance(strata, dict) or set(strata) != {"A", "B", "C"}:
        raise AnalysisInputError("Manifest must declare strata A, B and C")
    expected: dict[str, str] = {}
    for stratum, records in strata.items():
        if not isinstance(records, list) or len(records) != 20:
            raise AnalysisInputError("Registered cohort requires 20 specimens per stratum")
        for record in records:
            sha = record.get("sha256") if isinstance(record, dict) else None
            if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
                raise AnalysisInputError("Manifest requires complete lowercase SHA-256 specimen IDs")
            if sha[:8] in expected:
                raise AnalysisInputError("Manifest specimen prefixes must be unique")
            expected[sha[:8]] = stratum
    for name, arm in (("A", arm_a), ("B", arm_b)):
        if set(arm) != set(expected):
            raise AnalysisInputError(
                f"Arm {name} cohort mismatch: missing {len(set(expected) - set(arm))}, "
                f"unexpected {len(set(arm) - set(expected))}; no decision emitted"
            )
    for sha8, stratum in expected.items():
        if set(arm_a[sha8]) != K_VALUES:
            raise AnalysisInputError(f"Arm A {sha8} lacks the complete registered K sweep")
        if arm_b[sha8]["stratum"] != stratum:
            raise AnalysisInputError(f"Arm B {sha8} stratum differs from the manifest")
        if any(rec["baseline"] != arm_b[sha8]["baseline"] for rec in arm_a[sha8].values()):
            raise AnalysisInputError(f"Incomparable baseline scores for specimen {sha8}")


def cohen_d(a: list[float], b: list[float]) -> float:
    """Welch-style Cohen's d (pooled std with unequal variances)."""
    a_arr = np.array(a)
    b_arr = np.array(b)
    pooled_std = np.sqrt((a_arr.var(ddof=1) + b_arr.var(ddof=1)) / 2)
    if pooled_std == 0:
        return 0.0
    return float((b_arr.mean() - a_arr.mean()) / pooled_std)


def analyze() -> int:
    if any((OUT_DIR / name).exists() for name in ("statistics.json", "decision.json")):
        raise AnalysisInputError("Output already exists; use a fresh output directory, never overwrite evidence")
    arm_a = load_arm_a()
    arm_b = load_arm_b()
    validate_cohort(arm_a, arm_b)

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
    for sha8 in sorted(arm_a):
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

    # Preserve the implemented estimator; correct its label, not its method.
    # The normal branch differs from the independent-sample template; see README.
    if normality_pass:
        primary_test_name = "Paired one-sided t-test (B > A)"
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
            raise AnalysisInputError(f"Primary signed-rank test could not be computed: {e}") from e

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

    # 7. Independent Welch tests within strata; this is NOT a two-way ANOVA.
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

    # 8. Accepted-flag summary only. No dimension-level Goodhart test is run.
    goodhart_summary = {
        "status": "not_performed",
        "approach": "v0.1 — uses Arm B per-specimen final accepted flag as proxy",
        "note": "Full 5-dim audit requires dimension-level evidence and remains pending "
        "in bd_000-projects-436s. Accepted flags alone do not establish non-degradation.",
        "accepted_specimens": sum(1 for p in paired if p["b_accepted"]),
        "accepted_rate": sum(1 for p in paired if p["b_accepted"]) / max(1, len(paired)),
    }

    # 9. Decision rule
    a_mean_overall = float(np.mean([p["a_delta_best_k"] for p in paired]))
    b_mean_overall = float(np.mean([p["b_delta"] for p in paired]))
    # Compare the recorded decimal observations exactly at the strict threshold;
    # binary floating-point rounding must not turn equality into DESCOPE.
    exact_a_mean = sum(Fraction(str(value)) for value in a_best) / len(a_best)
    naive_lift_pp = float(max(Fraction(0), exact_a_mean))
    naive_lift_pct_of_projected = float(max(Fraction(0), exact_a_mean) / Fraction(str(PROJECTED_REFINER_LIFT_PP)))
    descope = max(Fraction(0), exact_a_mean) > Fraction(str(PROJECTED_REFINER_LIFT_PP)) * Fraction(
        str(DESCOPE_THRESHOLD_FRACTION)
    )

    decision = {
        "outcome": "DESCOPE" if descope else "PROCEED",
        "methodology_status": "unreconciled — see statistics.methodology_limits; not authorization",
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
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
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
        "methodology_limits": {
            "normal_branch": "Implemented paired t-test retained; independent-sample template differs; adjudication pending",
            "stratum_tests": "Independent Welch tests, not the template's two-way ANOVA",
            "k_contrasts": "Unadjusted one-sided p-values, not the template's Bonferroni-adjusted comparisons",
            "goodhart": "Accepted-flag summary only; five-dimension audit not performed",
            "authority": "Mechanical threshold result is not methodology ratification or Phase B authorization",
        },
        "raw_means": {
            "arm_a_best_k_mean": a_mean_overall,
            "arm_b_mean": b_mean_overall,
            "b_minus_a_mean": float(np.mean(b_minus_a)),
        },
    }

    # Serialize both before writing either; non-finite results never become evidence.
    statistics_json = json.dumps(stats_out, indent=2, sort_keys=True, allow_nan=False) + "\n"
    decision_json = json.dumps(decision, indent=2, sort_keys=True, allow_nan=False) + "\n"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in (("statistics.json", statistics_json), ("decision.json", decision_json)):
        with (OUT_DIR / name).open("x", encoding="utf-8") as handle:
            handle.write(content)
    print(f"\n✓ Wrote {OUT_DIR / 'statistics.json'}")
    print(f"✓ Wrote {OUT_DIR / 'decision.json'}")

    # Console summary
    print("\n" + "=" * 64)
    print("PHASE A.0 ANALYSIS RESULT — METHODOLOGY UNRECONCILED")
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
    print(f"Accepted-flag rate:      {goodhart_summary['accepted_rate']:.1%} (Goodhart audit not performed)")
    print()
    print(f"DECISION: {decision['outcome']}")
    print(f"  methodology_status: {decision['methodology_status']}")
    print(f"  naive_lift_pp:                       {naive_lift_pp:+.3f}")
    print(f"  naive_lift_pct_of_projected:         {naive_lift_pct_of_projected:.1%}")
    print(f"  refiner_lift_pp:                     {b_mean_overall:+.3f}")
    print(f"  refiner_lift_pct_of_projected:       {b_mean_overall / PROJECTED_REFINER_LIFT_PP:.1%}")
    print(f"  descope_triggered: {descope}")
    return 0


def main() -> int:
    try:
        return analyze()
    except (AnalysisInputError, OSError, ValueError) as exc:
        print(f"Analysis refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a complete Phase A.0 cohort without overwriting evidence")
    parser.add_argument("--arm-a", type=Path, default=ARM_A_DIR)
    parser.add_argument("--arm-b", type=Path, default=ARM_B_DIR)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--out", type=Path, required=True, help="Fresh output directory; existing evidence is refused")
    args = parser.parse_args()
    ARM_A_DIR, ARM_B_DIR, MANIFEST, OUT_DIR = args.arm_a, args.arm_b, args.manifest, args.out
    raise SystemExit(main())
