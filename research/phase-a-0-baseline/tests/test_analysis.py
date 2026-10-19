"""Offline analysis contracts over synthetic measurements, never experiment results.

Use the real NumPy/SciPy calculations and temporary result trees. These tests
verify loading, specimen pairing, best-K selection and the recorded decision
rule; they do not establish statistical validity or authorize Phase B.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
from scipy import stats as scipy_stats


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
    manifest = tmp_path / "manifest.json"
    write_json(
        manifest,
        {
            "strata": {
                stratum: [{"sha256": f"{i:08x}" + "0" * 56} for i in range(60) if "ABC"[i % 3] == stratum]
                for stratum in "ABC"
            }
        },
    )
    monkeypatch.setattr(module, "MANIFEST", manifest)
    return module


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_loaders_preserve_measurements(analysis: ModuleType) -> None:
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
    write_json(
        analysis.ARM_B_DIR / "_summary.json",
        {
            "per_specimen_results": [
                {
                    "sha8": "first",
                    "delta_marketplace_score_pct": 0,
                    "baseline_marketplace_score_pct": 80,
                    "final_marketplace_score_pct": 80,
                    "accepted": False,
                    "stratum": "A",
                }
            ]
        },
    )
    assert analysis.load_arm_b() == {
        "first": {
            "delta": 0,
            "baseline": 80,
            "final": 80,
            "accepted": False,
            "stratum": "A",
            "iterations_to_accept": None,
        }
    }


def seed_pairs(analysis: ModuleType, best: list[float], improvements: list[float]) -> None:
    records = []
    for i, (a, improvement) in enumerate(zip(best, improvements, strict=True)):
        for position, k in enumerate((0, 3, 8, 16)):
            delta = a - (3 - position) * (0.2 + (i % 6) * 0.01)
            write_json(analysis.ARM_A_DIR / f"{i:08x}" / f"k={k}" / "response.json", {"dry_run": False})
            write_json(
                analysis.ARM_A_DIR / f"{i:08x}" / f"k={k}" / "score.json",
                {
                    "delta_marketplace_score_pct": delta,
                    "baseline_marketplace_score_pct": 80,
                    "marketplace_score_pct": 80 + delta,
                },
            )
        write_json(analysis.ARM_B_DIR / f"{i:08x}" / "proposal-0.json", {"dry_run": False})
        records.append(
            {
                "sha8": f"{i:08x}",
                "delta_marketplace_score_pct": a + improvement,
                "baseline_marketplace_score_pct": 80,
                "final_marketplace_score_pct": 80 + a + improvement,
                "accepted": i % 2 == 0,
                "stratum": "ABC"[i % 3],
            }
        )
    write_json(analysis.ARM_B_DIR / "_summary.json", {"per_specimen_results": records})


@pytest.mark.parametrize(
    ("offset", "outcome", "lift"), [(-2, "PROCEED", 0), (0, "PROCEED", 0.625), (1, "DESCOPE", 1.625)]
)
def test_analysis_pairs_best_k_and_emits_decision(
    analysis: ModuleType, offset: float, outcome: str, lift: float
) -> None:
    seed_pairs(
        analysis,
        [offset + i * 1.25 / 59 for i in range(60)],
        [0.45 + 0.1 * float(scipy_stats.norm.ppf((i + 0.5) / 60)) for i in range(60)],
    )
    assert analysis.main() == 0
    stats = json.loads((analysis.OUT_DIR / "statistics.json").read_text())
    decision = json.loads((analysis.OUT_DIR / "decision.json").read_text())
    assert stats["n_specimens_paired"] == 60
    assert stats["raw_means"] == pytest.approx(
        {"arm_a_best_k_mean": offset + 0.625, "arm_b_mean": offset + 1.075, "b_minus_a_mean": 0.45}
    )
    assert decision == stats["decision"]
    assert decision["outcome"] == outcome
    assert decision["naive_lift_pp"] == pytest.approx(lift)
    assert decision["naive_lift_as_fraction_of_projected"] == pytest.approx(lift / 1.5)
    assert stats["per_k_arm_a"]["16"]["n"] == 60
    assert stats["per_k_arm_a"]["16"]["mean"] == pytest.approx(offset + 0.625)
    assert set(stats["k_sweep_contrasts"]) == {"K3-K0", "K8-K3", "K16-K8"}
    for contrast in stats["k_sweep_contrasts"].values():
        assert contrast["n"] == 60
        assert contrast["mean_diff"] == pytest.approx(0.225)
    assert set(stats["per_stratum_test"]) == {"A", "B", "C"}
    assert stats["goodhart_audit"]["accepted_specimens"] == 30
    assert stats["goodhart_audit"]["accepted_rate"] == 0.5
    assert stats["primary_paired_test"]["shapiro_normal"] is True
    assert decision["primary_significant_at_alpha_0_05"] is True
    assert stats["primary_paired_test"]["test_name"] == "Paired one-sided t-test (B > A)"
    assert stats["goodhart_audit"]["status"] == "not_performed"
    assert "unreconciled" in decision["methodology_status"]
    assert "not the template's two-way ANOVA" in stats["methodology_limits"]["stratum_tests"]
    # Python's default JSON parser accepts NaN; explicitly refuse it here.
    json.dumps(stats, allow_nan=False)


def test_non_normal_differences_use_real_signed_rank_test(analysis: ModuleType) -> None:
    seed_pairs(analysis, [i / 100 for i in range(60)], [0.1] * 59 + [10])
    assert analysis.main() == 0
    stats = json.loads((analysis.OUT_DIR / "statistics.json").read_text())
    test = stats["primary_paired_test"]
    assert test["shapiro_normal"] is False
    assert test["test_name"] == "Wilcoxon signed-rank one-sided (B > A)"
    assert test["statistic"] == 1830
    assert test["p_value"] < 0.05


def test_cohen_d_preserves_direction_and_scale(analysis: ModuleType) -> None:
    assert analysis.cohen_d([1, 2, 3], [2, 3, 4]) == pytest.approx(1)
    assert analysis.cohen_d([2, 3, 4], [1, 2, 3]) == pytest.approx(-1)


def assert_refused(analysis: ModuleType) -> None:
    assert analysis.main() == 2
    assert not (analysis.OUT_DIR / "decision.json").exists()
    assert not (analysis.OUT_DIR / "statistics.json").exists()


@pytest.mark.parametrize("count", [0, 1, 2, 59])
def test_incomplete_registered_cohort_cannot_decide(analysis: ModuleType, count: int) -> None:
    seed_pairs(analysis, [i / 100 for i in range(count)], [0.2] * count)
    assert_refused(analysis)


@pytest.mark.parametrize(
    "defect",
    [
        "unmatched",
        "duplicate",
        "missing-delta",
        "wrong-stratum",
        "missing-accepted",
        "string-accepted",
        "missing-final",
        "baseline-mismatch",
        "inconsistent-delta",
        "dry-run",
        "errors",
    ],
)
def test_invalid_arm_b_evidence_cannot_decide(analysis: ModuleType, defect: str) -> None:
    seed_pairs(analysis, [i / 100 for i in range(60)], [0.1] * 59 + [10])
    path = analysis.ARM_B_DIR / "_summary.json"
    summary = json.loads(path.read_text())
    rec = summary["per_specimen_results"][0]
    if defect == "unmatched":
        for item in summary["per_specimen_results"]:
            item["sha8"] = "unmatched-" + item["sha8"]
    elif defect == "duplicate":
        summary["per_specimen_results"].append(rec)
    elif defect == "missing-delta":
        del rec["delta_marketplace_score_pct"]
    elif defect == "wrong-stratum":
        rec["stratum"] = "C"
    elif defect == "missing-accepted":
        del rec["accepted"]
    elif defect == "string-accepted":
        rec["accepted"] = "false"
    elif defect == "missing-final":
        del rec["final_marketplace_score_pct"]
    elif defect == "baseline-mismatch":
        rec["baseline_marketplace_score_pct"] -= 1
        rec["final_marketplace_score_pct"] -= 1  # Internally consistent, but a different baseline.
    elif defect == "inconsistent-delta":
        rec["delta_marketplace_score_pct"] += 1
    elif defect == "dry-run":
        summary["dry_run"] = True
    else:
        summary["error_count"] = 1
    write_json(path, summary)
    assert_refused(analysis)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), True, "1", None, 101, 10**400])
def test_invalid_arm_a_numbers_cannot_decide(analysis: ModuleType, value: object) -> None:
    seed_pairs(analysis, [i / 100 for i in range(60)], [0.1] * 59 + [10])
    path = analysis.ARM_A_DIR / "00000000" / "k=0" / "score.json"
    record = json.loads(path.read_text())
    record["marketplace_score_pct"] = value
    write_json(path, record)
    assert_refused(analysis)


@pytest.mark.parametrize(
    "defect",
    [
        "missing-k",
        "missing-delta",
        "duplicate-json-key",
        "overflow",
        "missing-summary",
        "malformed-summary",
        "manifest-count",
        "manifest-duplicate",
        "manifest-stratum",
    ],
)
def test_incomplete_or_ambiguous_files_cannot_decide(analysis: ModuleType, defect: str) -> None:
    seed_pairs(analysis, [i / 100 for i in range(60)], [0.1] * 59 + [10])
    score = analysis.ARM_A_DIR / "00000000" / "k=0" / "score.json"
    summary = analysis.ARM_B_DIR / "_summary.json"
    if defect == "missing-k":
        score.unlink()
    elif defect == "missing-delta":
        data = json.loads(score.read_text())
        del data["delta_marketplace_score_pct"]
        write_json(score, data)
    elif defect == "duplicate-json-key":
        score.write_text('{"delta_marketplace_score_pct": 1, "delta_marketplace_score_pct": 2}')
    elif defect == "overflow":
        score.write_text('{"marketplace_score_pct": 1e999}')
    elif defect == "missing-summary":
        summary.unlink()
    elif defect == "malformed-summary":
        summary.write_text("{broken")
    else:
        manifest = json.loads(analysis.MANIFEST.read_text())
        if defect == "manifest-count":
            manifest["strata"]["A"].pop()
        elif defect == "manifest-duplicate":
            manifest["strata"]["B"][0] = manifest["strata"]["A"][0]
        else:
            manifest["strata"]["D"] = manifest["strata"].pop("A")
        write_json(analysis.MANIFEST, manifest)
    assert_refused(analysis)


def test_non_finite_calculation_is_refused_before_either_output(analysis: ModuleType) -> None:
    # Both groups are constant: the real statistical routines yield undefined or
    # infinite statistics. Do not sanitize these into invented successful evidence.
    seed_pairs(analysis, [1] * 60, [1] * 60)
    with pytest.warns((RuntimeWarning, UserWarning)):
        assert_refused(analysis)


@pytest.mark.parametrize(("delta", "outcome"), [(1.049, "PROCEED"), (1.05, "PROCEED"), (1.051, "DESCOPE")])
def test_strict_descope_threshold_does_not_round_equality_up(analysis: ModuleType, delta: float, outcome: str) -> None:
    seed_pairs(analysis, [delta] * 60, [0.45 + 0.1 * float(scipy_stats.norm.ppf((i + 0.5) / 60)) for i in range(60)])
    assert analysis.main() == 0
    assert json.loads((analysis.OUT_DIR / "decision.json").read_text())["outcome"] == outcome


@pytest.mark.parametrize("name", ["statistics.json", "decision.json"])
def test_existing_evidence_is_preserved_byte_for_byte(analysis: ModuleType, name: str) -> None:
    existing = analysis.OUT_DIR / name
    existing.write_bytes(b"historical evidence\n")
    assert analysis.main() == 2
    assert existing.read_bytes() == b"historical evidence\n"
    assert len(list(analysis.OUT_DIR.iterdir())) == 1


def test_cli_refuses_empty_input_without_an_output(analysis: ModuleType, tmp_path: Path) -> None:
    write_json(analysis.ARM_B_DIR / "_summary.json", {"per_specimen_results": []})
    script = Path(analysis.__file__)
    run = subprocess.run(
        [
            sys.executable,
            str(script),
            "--arm-a",
            str(analysis.ARM_A_DIR),
            "--arm-b",
            str(analysis.ARM_B_DIR),
            "--manifest",
            str(analysis.MANIFEST),
            "--out",
            str(tmp_path / "cli-output"),
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert run.returncode == 2
    assert "cohort mismatch" in run.stderr
    assert not (tmp_path / "cli-output").exists()


@pytest.mark.parametrize("arm", ["A", "B"])
@pytest.mark.parametrize("defect", ["simulated", "missing-file", "missing-flag", "string-flag", "non-object"])
def test_per_record_provenance_refuses_resumed_simulation(analysis: ModuleType, arm: str, defect: str) -> None:
    seed_pairs(analysis, [i / 100 for i in range(60)], [0.1] * 59 + [10])
    # A later real run's summary does not change saved per-record provenance.
    write_json(analysis.ARM_A_DIR / "_summary.json", {"dry_run": False})
    summary_path = analysis.ARM_B_DIR / "_summary.json"
    summary = json.loads(summary_path.read_text())
    summary["dry_run"] = False
    write_json(summary_path, summary)
    path = (
        analysis.ARM_A_DIR / "00000000" / "k=0" / "response.json"
        if arm == "A"
        else analysis.ARM_B_DIR / "00000000" / "proposal-0.json"
    )
    if defect == "missing-file":
        path.unlink()
    else:
        content = {
            "simulated": {"dry_run": True},
            "missing-flag": {},
            "string-flag": {"dry_run": "false"},
            "non-object": [],
        }[defect]
        write_json(path, content)
    assert_refused(analysis)


def test_later_simulated_arm_b_proposal_is_refused(analysis: ModuleType) -> None:
    seed_pairs(analysis, [i / 100 for i in range(60)], [0.1] * 59 + [10])
    write_json(analysis.ARM_B_DIR / "00000000" / "proposal-3.json", {"dry_run": True})
    assert_refused(analysis)
