"""Forensic audit contracts; synthetic fixtures are not experiment evidence."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "audit-phase-a0-history.py"
spec = importlib.util.spec_from_file_location("phase_a0_history_audit", SCRIPT)
assert spec and spec.loader
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def test_reconstruct_input_preserves_original_frontmatter_and_body() -> None:
    original = '---\nname: original\ndescription: "before"\n---\n\n# Body\nExact body.\n'
    final = '---\nname: original\ndescription: "after"\n---\n\n# Body\nExact body.\n'
    proposal = {"prompt": "Instructions\n<input>\n" + original.split("\n\n# Body")[0] + "\n</input>"}
    assert audit.recover_input(final, True, proposal) == original
    assert audit.recover_input(original, False, None) == original


@pytest.mark.parametrize("proposal", [None, {"prompt": "no bounded input"}])
def test_ambiguous_reconstruction_is_refused(proposal: dict[str, str] | None) -> None:
    with pytest.raises(ValueError):
        audit.recover_input("---\nname: example\n---\nbody\n", True, proposal)


def test_cli_refuses_wrong_judge_without_executing_it(tmp_path: Path) -> None:
    validator = tmp_path / "validator.py"
    marker = tmp_path / "executed"
    validator.write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
    output = tmp_path / "audit.json"
    run = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--research-root",
            str(tmp_path),
            "--validator",
            str(validator),
            "--out",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 2
    assert "Validator bytes differ" in run.stderr
    assert not marker.exists()
    assert not output.exists()


@pytest.mark.parametrize("stdout", ["no grade", "GRADE: A (90/100)\nGRADE: B (80/100)"])
def test_replay_refuses_missing_or_ambiguous_grades(tmp_path: Path, stdout: str) -> None:
    validator = tmp_path / "validator.py"
    validator.write_text(f"print({stdout!r})\n")
    with pytest.raises(ValueError, match="exactly one grade"):
        audit.replay_score(validator, "---\nname: specimen\n---\n", tmp_path)


def test_existing_report_is_preserved(tmp_path: Path) -> None:
    output = tmp_path / "audit.json"
    output.write_bytes(b"prior audit\n")
    run = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--research-root",
            str(tmp_path),
            "--validator",
            str(tmp_path / "absent"),
            "--out",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 2
    assert "Output exists" in run.stderr
    assert output.read_bytes() == b"prior audit\n"
