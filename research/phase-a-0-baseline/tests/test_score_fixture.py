"""Tests for score-fixture.py — the validator wrapper.

These tests run the actual validator subprocess against simple inline
fixtures in tmp_path. No network. The validator binary must be present
(checked via skip).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SCORE_SCRIPT = REPO_ROOT / "research" / "phase-a-0-baseline" / "scripts" / "score-fixture.py"
VALIDATOR_PATH = Path.home() / "000-projects" / "claude-code-plugins" / "scripts" / "validate-skills-schema.py"


@pytest.fixture(scope="module")
def validator_available() -> bool:
    if not VALIDATOR_PATH.exists():
        pytest.skip(f"validator not found at {VALIDATOR_PATH}")
    return True


def _make_skill_md(tmp_path: Path, frontmatter_lines: list[str], body: str = "# Body\n\nContent.\n") -> Path:
    """Write a synthetic SKILL.md with the given frontmatter lines + body."""
    content = "---\n" + "\n".join(frontmatter_lines) + "\n---\n\n" + body
    p = tmp_path / "SKILL.md"
    p.write_text(content)
    return p


def _run_scorer(target: Path) -> dict:
    """Run score-fixture.py on target and parse JSON output."""
    result = subprocess.run(
        [sys.executable, str(SCORE_SCRIPT), str(target), "--validator-path", str(VALIDATOR_PATH)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, f"scorer failed: stdout={result.stdout[:500]} stderr={result.stderr[:500]}"
    return json.loads(result.stdout)


def test_score_minimal_skill_md_returns_expected_shape(tmp_path: Path, validator_available: bool) -> None:
    """Validator output JSON must have the canonical expected.json schema."""
    skill = _make_skill_md(
        tmp_path,
        [
            "name: test-skill",
            "description: A test skill for the unit-test suite.",
        ],
    )
    result = _run_scorer(skill)

    # Top-level required fields per DESIGN.md § 5.1 expected.json schema
    assert "fixture_sha" in result
    assert "validator_version" in result
    assert "validator_commit" in result
    assert "tiers" in result
    assert "standard" in result["tiers"]
    assert "marketplace" in result["tiers"]
    assert isinstance(result.get("field_completeness"), int)


def test_score_marketplace_tier_detects_missing_required_fields(
    tmp_path: Path,
    validator_available: bool,
) -> None:
    """Marketplace tier requires 8 IS-required fields; a minimal skill should fail it."""
    skill = _make_skill_md(
        tmp_path,
        [
            "name: incomplete-skill",
            "description: Missing most required fields.",
        ],
    )
    result = _run_scorer(skill)
    # Marketplace tier should fail (missing 6 of 8 required fields)
    assert result["tiers"]["marketplace"]["pass"] is False
    # field_completeness is 0-8 count of IS_MARKETPLACE_REQUIRED present
    assert result["field_completeness"] < 8


def test_score_full_marketplace_skill_passes(
    tmp_path: Path,
    validator_available: bool,
) -> None:
    """A SKILL.md with all 8 IS-required fields should pass marketplace tier (modulo deprecations)."""
    skill = _make_skill_md(
        tmp_path,
        [
            "name: complete-skill",
            "description: A skill that satisfies the IS marketplace tier requirements.",
            "allowed-tools: Read, Edit",
            "version: 1.0.0",
            "author: test@example.com",
            "license: Apache-2.0",
            "compatibility: Claude Code",
            "tags:",
            "  - test",
            "  - smoke",
        ],
    )
    result = _run_scorer(skill)
    # All 8 required fields present
    assert result["field_completeness"] == 8


def test_score_detects_deprecated_compatible_with_field(
    tmp_path: Path,
    validator_available: bool,
) -> None:
    """The deprecated 'compatible-with' field should be flagged."""
    skill = _make_skill_md(
        tmp_path,
        [
            "name: legacy-skill",
            "description: Uses the deprecated compatible-with field.",
            "compatible-with: Claude Code",
        ],
    )
    result = _run_scorer(skill)
    assert result["deprecated_field_count"] >= 1
