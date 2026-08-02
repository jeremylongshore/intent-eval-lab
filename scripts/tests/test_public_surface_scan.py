"""Tests for the deterministic public-surface PII/secret scrub gate."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO / "scripts" / "public-surface-scan.py"
SPEC = importlib.util.spec_from_file_location("public_surface_scan", MODULE_PATH)
assert SPEC and SPEC.loader
scan = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scan
SPEC.loader.exec_module(scan)


def test_public_literals_and_pii_are_reported_without_content() -> None:
    policy = scan.load_policy()
    findings = scan.scan_lines(
        "README.md",
        [
            (1, "A synthetic example only."),
            (2, "Jeremy Longshore <person@example.test>"),
            (3, "record 123-45-6789"),
        ],
        policy,
    )
    assert {(finding.line, finding.detector_id) for finding in findings} == {
        (2, "personal-name"),
        (2, "email-address"),
        (3, "us-social-security-number"),
    }
    assert all(not hasattr(finding, "matched_text") for finding in findings)


def test_private_brain_literals_are_public_scope_only() -> None:
    policy = scan.load_policy()
    public = scan.scan_lines("docs/example.md", [(1, "qmd://x uses ~/.teamkb")], policy)
    source = scan.scan_lines("src/example.py", [(1, "path = '~/.teamkb'")], policy)
    assert [finding.detector_id for finding in public] == ["private-brain-path"]
    assert source == []


def test_credentials_are_blocked_in_any_non_exempt_path() -> None:
    policy = scan.load_policy()
    findings = scan.scan_lines("src/client.py", [(7, 'token = "ghp_123456789012345678901234567890"')], policy)
    assert (7, "github-token") in [(finding.line, finding.detector_id) for finding in findings]


def test_ignored_vendor_and_test_paths_are_not_scanned() -> None:
    policy = scan.load_policy()
    assert scan.scan_lines("specs/_vendor/upstream/example.md", [(1, "Jeremy Longshore")], policy) == []
    assert scan.scan_lines("scripts/tests/test_fixture.py", [(1, "sk-123456789012345678901234")], policy) == []


def test_invalid_policy_fails_closed(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"public_roots": [], "ignored_prefixes": [], "detectors": []}))
    with pytest.raises(scan.PolicyError):
        scan.load_policy(bad)


def test_staged_mode_scans_only_added_lines(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "--quiet", "-b", "main"], cwd=repo, check=True)
    (repo / "README.md").write_text("Historical Jeremy Longshore line\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.test", "commit", "--quiet", "-m", "seed"], cwd=repo, check=True)
    (repo / "README.md").write_text("Historical Jeremy Longshore line\nNew synthetic line\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    policy = scan.load_policy()
    assert scan.scan_diff(repo, ["--cached"], policy) == []
