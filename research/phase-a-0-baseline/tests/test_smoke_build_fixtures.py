"""Smoke tests for build-fixtures.py.

build-fixtures.py orchestrates fixture materialization: for each skill in a
manifest it runs a `--score-script` (injectable) and stages an
input/expected/label/provenance fixture directory. Because the score-script is
a parameter, we drive the full main() path with a trivial STUB scorer — no real
scoring toolchain, no network — and assert the staging behavior + summary.

Covers: manifest parse, stratum/held_out selection, run_scorer, stage_fixture
(new + skip-existing), label_for (A/B/C/held_out branches), and the summary.

Run via: pytest tests/test_smoke_build_fixtures.py -v
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = REPO_ROOT / "research" / "phase-a-0-baseline" / "scripts"
BUILD_FIXTURES = SCRIPTS / "build-fixtures.py"

# A trivial stand-in for score-fixture.py: reads the skill path arg and emits a
# shape-valid scoring JSON (the only field build-fixtures inspects is
# tiers.marketplace.pass, used by label_for).
STUB_SCORER = (
    "import sys, json\n"
    "print(json.dumps({'skill': sys.argv[1], 'tiers': {'marketplace': {'pass': True}}, 'score': 100}))\n"
)


def _write_skill(path: Path, tag: str = "smoke") -> str:
    """Write a minimal, content-unique SKILL.md; return its sha256 hex digest.

    `tag` varies the body so distinct skills hash to distinct sha256 (build-
    fixtures dedupes staged fixtures by sha8, so identical content collapses).
    """
    path.write_text(
        f"---\nname: {tag}-skill\ndescription: Minimal {tag} skill for the build-fixtures smoke test.\n---\n\n# {tag} Skill\n",
        encoding="utf-8",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(manifest: Path, out: Path, scorer: Path, strata: str, force: bool = False) -> subprocess.CompletedProcess[str]:
    args = [
        sys.executable,
        str(BUILD_FIXTURES),
        "--manifest",
        str(manifest),
        "--out",
        str(out),
        "--score-script",
        str(scorer),
        "--strata",
        strata,
    ]
    if force:
        args.append("--force")
    return subprocess.run(args, capture_output=True, text=True, check=False)


def _build_manifest(skill: Path, sha: str) -> dict[str, object]:
    """Single-item manifest (stratum A only) for the skip/error tests.

    held_out is empty: build-fixtures selects by letter, so a held_out group
    keyed "A" would ALSO match `--strata A` and double-count. Keeping it empty
    isolates a single processed item. (The all-strata test builds its own
    multi-skill manifest to exercise every branch.)
    """
    item = {"path": str(skill), "sha256": sha}
    return {
        "pre_registration": {"seed": 1234, "validator_commit": "smoke-test"},
        "strata": {"A": [item]},
        "held_out": {},
    }


def test_build_fixtures_stages_all_strata(tmp_path: Path) -> None:
    # Distinct skills per stratum so each hashes to a distinct sha8 (identical
    # content would dedupe to a single staged fixture).
    def mk(tag: str) -> dict[str, str]:
        p = tmp_path / f"{tag}.md"
        sha = _write_skill(p, tag)
        return {"path": str(p), "sha256": sha}

    a, b, c, h = mk("a"), mk("b"), mk("c"), mk("held")
    manifest_obj: dict[str, object] = {
        "pre_registration": {"seed": 1234, "validator_commit": "smoke-test"},
        "strata": {"A": [a], "B": [b], "C": [c]},
        "held_out": {"A": [h]},
    }
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps(manifest_obj), encoding="utf-8")
    scorer = tmp_path / "stub_scorer.py"
    scorer.write_text(STUB_SCORER, encoding="utf-8")
    out = tmp_path / "fixtures"

    r = _run(manifest, out, scorer, strata="A,B,C,held_out")
    assert r.returncode == 0, f"stderr: {r.stderr}\nstdout: {r.stdout}"

    summary = json.loads(r.stdout)
    # 3 strata items + 1 held_out item, all distinct → all newly staged.
    assert summary["staged"] == 4
    assert summary["skipped_existing"] == 0
    assert summary["errors"] == []
    assert summary["fixture_count_total"] == 4

    # Per-stratum label_for branches (A / B / C) are exercised.
    def label(sha: str) -> str:
        return (out / sha[:8] / "label.txt").read_text().strip()

    assert label(a["sha256"]) == "global-pass-marketplace"
    assert label(b["sha256"]) == "marketplace-corpus-pass"
    assert label(c["sha256"]) == "marketplace-corpus-fail"
    # held_out group is keyed by letter "A", so build-fixtures calls
    # label_for("A", ...) for it -> the same global-pass label as stratum A.
    assert label(h["sha256"]) == "global-pass-marketplace"

    # A staged fixture carries the four expected artifacts + provenance.
    fixture_dir = out / a["sha256"][:8]
    assert (fixture_dir / "input.md").exists()
    expected = json.loads((fixture_dir / "expected.json").read_text())
    assert expected["tiers"]["marketplace"]["pass"] is True
    prov = json.loads((fixture_dir / "provenance.json").read_text())
    assert prov["source_sha256"] == a["sha256"]
    assert prov["manifest_seed"] == 1234


def test_build_fixtures_skips_existing_without_force(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    sha = _write_skill(skill)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps(_build_manifest(skill, sha)), encoding="utf-8")
    scorer = tmp_path / "stub_scorer.py"
    scorer.write_text(STUB_SCORER, encoding="utf-8")
    out = tmp_path / "fixtures"

    first = _run(manifest, out, scorer, strata="A")
    assert first.returncode == 0
    assert json.loads(first.stdout)["staged"] == 1

    # Second run over the same out dir without --force → the existing fixture
    # is skipped, not restaged.
    second = _run(manifest, out, scorer, strata="A")
    assert second.returncode == 0
    s2 = json.loads(second.stdout)
    assert s2["staged"] == 0
    assert s2["skipped_existing"] == 1


def test_build_fixtures_reports_scorer_errors(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    sha = _write_skill(skill)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps(_build_manifest(skill, sha)), encoding="utf-8")
    # A scorer that exits non-zero → run_scorer raises → recorded as an error,
    # nothing staged, and main() returns exit 1.
    scorer = tmp_path / "bad_scorer.py"
    scorer.write_text("import sys\nsys.exit(3)\n", encoding="utf-8")
    out = tmp_path / "fixtures"

    r = _run(manifest, out, scorer, strata="A")
    assert r.returncode == 1
    summary = json.loads(r.stdout)
    assert summary["staged"] == 0
    assert len(summary["errors"]) == 1
    assert "scorer exit 3" in summary["errors"][0]["error"]
