"""Offline analysis contracts over synthetic measurements, never experiment results.

Use the real NumPy/SciPy calculations and temporary result trees. These tests
verify loading, specimen pairing, best-K selection and the recorded decision
rule; they do not establish statistical validity or authorize Phase B.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest


@pytest.fixture
def analysis(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "scripts" / "analyze.py"
    spec = importlib.util.spec_from_file_location("phase_a0_analysis", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in ("ARM_A_DIR", "ARM_B_DIR", "OUT_DIR"):
        target = tmp_path / name
        target.mkdir()
        monkeypatch.setattr(module, name, target)
    return module


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_loaders_preserve_measurements_and_ignore_unscored_candidates(analysis: ModuleType) -> None:
    write_json(
        analysis.ARM_A_DIR / "first" / "k=3" / "score.json",
        {
            "delta_marketplace_score_pct": 4,
            "baseline_marketplace_score_pct": 80,
            "marketplace_score_pct": 84,
            "field_completeness": 8,
            "deprecated_field_count": 1,
            "is_extras_present": 2,
            "security_finding_count": 3,
            "marketplace_pass": True,
        },
    )
    write_json(analysis.ARM_A_DIR / "unscored" / "k=0" / "score.json", {})
    write_json(analysis.ARM_A_DIR / "no-k" / "score.json", {})
    assert analysis.load_arm_a() == {
        "first": {
            3: {
                "delta": 4,
                "baseline": 80,
                "candidate": 84,
                "field_completeness": 8,
                "deprecated_count": 1,
                "is_extras": 2,
                "security_findings": 3,
                "marketplace_pass": True,
            }
        }
    }
    write_json(analysis.ARM_B_DIR / "_summary.json", {"per_specimen_results": [{"sha8": "first"}]})
    assert analysis.load_arm_b() == {
        "first": {
            "delta": 0,
            "baseline": 0,
            "final": 0,
            "accepted": False,
            "stratum": "?",
            "iterations_to_accept": None,
        }
    }


def seed_pairs(analysis: ModuleType, best: list[float], improvements: list[float]) -> None:
    records = []
    for i, (a, improvement) in enumerate(zip(best, improvements, strict=True)):
        for position, k in enumerate((0, 3, 8, 16)):
            delta = a - (3 - position) * (0.2 + i * 0.01)
            write_json(
                analysis.ARM_A_DIR / f"specimen-{i}" / f"k={k}" / "score.json",
                {
                    "delta_marketplace_score_pct": delta,
                    "baseline_marketplace_score_pct": 80,
                    "marketplace_score_pct": 80 + delta,
                },
            )
        records.append(
            {
                "sha8": f"specimen-{i}",
                "delta_marketplace_score_pct": a + improvement,
                "accepted": i % 2 == 0,
                "stratum": "A" if i % 2 == 0 else "B",
            }
        )
    # An unmatched B specimen must not affect paired tests, means or decisions.
    records.append({"sha8": "unmatched", "delta_marketplace_score_pct": 1000})
    write_json(analysis.ARM_B_DIR / "_summary.json", {"per_specimen_results": records})


@pytest.mark.parametrize(
    ("offset", "outcome", "lift"), [(-2, "PROCEED", 0), (0, "PROCEED", 0.625), (1, "DESCOPE", 1.625)]
)
def test_analysis_pairs_best_k_and_emits_decision(
    analysis: ModuleType, offset: float, outcome: str, lift: float
) -> None:
    seed_pairs(analysis, [offset + i / 4 for i in range(6)], [0.2, 0.5, 0.3, 0.7, 0.4, 0.6])
    assert analysis.main() == 0
    stats = json.loads((analysis.OUT_DIR / "statistics.json").read_text())
    decision = json.loads((analysis.OUT_DIR / "decision.json").read_text())
    assert stats["n_specimens_paired"] == 6
    assert stats["raw_means"] == pytest.approx(
        {"arm_a_best_k_mean": offset + 0.625, "arm_b_mean": offset + 1.075, "b_minus_a_mean": 0.45}
    )
    assert decision == stats["decision"]
    assert decision["outcome"] == outcome
    assert decision["naive_lift_pp"] == pytest.approx(lift)
    assert decision["naive_lift_as_fraction_of_projected"] == pytest.approx(lift / 1.5)
    assert stats["per_k_arm_a"]["16"]["n"] == 6
    assert stats["per_k_arm_a"]["16"]["mean"] == pytest.approx(offset + 0.625)
    assert set(stats["k_sweep_contrasts"]) == {"K3-K0", "K8-K3", "K16-K8"}
    for contrast in stats["k_sweep_contrasts"].values():
        assert contrast["n"] == 6
        assert contrast["mean_diff"] == pytest.approx(0.225)
    assert set(stats["per_stratum_test"]) == {"A", "B"}
    assert stats["goodhart_audit"]["accepted_specimens"] == 3
    assert stats["goodhart_audit"]["accepted_rate"] == 0.5
    assert stats["primary_paired_test"]["shapiro_normal"] is True
    assert decision["primary_significant_at_alpha_0_05"] is True


def test_non_normal_differences_use_real_signed_rank_test(analysis: ModuleType) -> None:
    seed_pairs(analysis, [i / 100 for i in range(20)], [0.1] * 19 + [10])
    assert analysis.main() == 0
    stats = json.loads((analysis.OUT_DIR / "statistics.json").read_text())
    test = stats["primary_paired_test"]
    assert test["shapiro_normal"] is False
    assert test["test_name"] == "Wilcoxon signed-rank one-sided (B > A)"
    assert test["statistic"] == 210
    assert test["p_value"] < 0.05


def test_cohen_d_preserves_direction_and_scale(analysis: ModuleType) -> None:
    assert analysis.cohen_d([1, 2, 3], [2, 3, 4]) == pytest.approx(1)
    assert analysis.cohen_d([2, 3, 4], [1, 2, 3]) == pytest.approx(-1)
