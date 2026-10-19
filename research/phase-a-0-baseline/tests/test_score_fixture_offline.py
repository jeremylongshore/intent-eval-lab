"""Scorer adapter contracts with a synthetic validator process, not real grades.

The separate test_score_fixture.py retains the actual marketplace integration.
Here deterministic stdout/stderr exercise parsing, tier routing and provenance
without depending on a developer's checkout or provider credentials.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "score-fixture.py"


def test_scorer_routes_tiers_and_preserves_findings(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        "---\nname: sample\ndescription: test\ncompatible-with: old\nrequires_env: TEST\nmetadata:\n  version: nested\n---\n# Body\n"
    )
    validator = tmp_path / "validator.py"
    validator.write_text(
        "import sys\n"
        "from pathlib import Path\n"
        "assert Path(sys.argv[2]).name == 'SKILL.md'\n"
        "if sys.argv[1] == '--standard':\n"
        "    print('GRADE: A (100/100)')\n"
        "    print('INFO: retained message')\n"
        "elif sys.argv[1] == '--marketplace':\n"
        "    print('GRADE: C (72/100)')\n"
        "    print('WARN: [security-policy] fixture warning')\n"
        "    print('ERROR: required field absent', file=sys.stderr)\n"
        "    sys.exit(1)\n"
        "else: raise AssertionError(sys.argv)\n"
    )
    run = subprocess.run(
        [sys.executable, str(SCRIPT), str(skill), "--validator-path", str(validator), "--commit", "fixture-commit"],
        capture_output=True,
        text=True,
        timeout=20,
        check=True,
    )
    result = json.loads(run.stdout)
    assert result["fixture_sha"] == hashlib.sha256(skill.read_bytes()).hexdigest()
    assert result["validator_commit"] == "fixture-commit"
    assert result["field_completeness"] == 2  # Nested version is not a top-level field.
    assert result["deprecated_field_count"] == 1
    assert result["is_extras_present"] == 1
    assert result["security_finding_count"] == 1
    assert result["tiers"]["standard"] == {
        "pass": True,
        "score_pct": 100,
        "grade": "A",
        "findings": [{"severity": "INFO", "section": None, "message": "retained message"}],
    }
    assert result["tiers"]["marketplace"] == {
        "pass": False,
        "score_pct": 72,
        "grade": "C",
        "findings": [
            {"severity": "WARN", "section": "security-policy", "message": "fixture warning"},
            {"severity": "ERROR", "section": None, "message": "required field absent"},
        ],
    }


@pytest.mark.parametrize("missing", ["skill", "validator"])
def test_scorer_missing_input_fails_without_a_grade(tmp_path: Path, missing: str) -> None:
    skill = tmp_path / "SKILL.md"
    validator = tmp_path / "validator.py"
    if missing != "skill":
        skill.write_text("# No frontmatter\n")
    run = subprocess.run(
        [sys.executable, str(SCRIPT), str(skill), "--validator-path", str(validator)],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert run.returncode == 2
    assert run.stdout == ""
    assert "not found" in run.stderr
