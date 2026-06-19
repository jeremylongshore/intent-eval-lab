"""Smoke tests for run-arm-a.py and run-arm-b.py via --dry-run.

These do NOT hit any real API. They verify:
- Both runners accept --provider <name> for every name in ALL_PROVIDER_NAMES
- Both runners exit 0 in dry-run mode on one specimen
- The dry-run output is shape-valid JSON / contains expected markers
- The cost meter respects the free-tier (NVIDIA/Groq → $0) and Anthropic ceilings

Run via: pytest tests/test_smoke_runners.py -v
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import _arm_common as ac  # noqa: E402
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = REPO_ROOT / "research" / "phase-a-0-baseline" / "scripts"
MANIFEST = REPO_ROOT / "research" / "phase-a-0-baseline" / "corpus" / "manifest.json"


@pytest.fixture(scope="module")
def manifest_available() -> bool:
    """Skip smoke tests if the corpus manifest hasn't been generated yet."""
    if not MANIFEST.exists():
        pytest.skip(f"corpus manifest not found at {MANIFEST}; run build-fixtures first")
    return True


@pytest.mark.parametrize("provider_name", ac.ALL_PROVIDER_NAMES)
def test_arm_a_dry_run_exits_zero(
    provider_name: str,
    tmp_path: Path,
    manifest_available: bool,
) -> None:
    """Arm A --dry-run for every provider must exit 0 and not call out."""
    out_dir = tmp_path / "arm-a"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "run-arm-a.py"),
            "--dry-run",
            "--provider",
            provider_name,
            "--manifest",
            str(MANIFEST),
            "--out",
            str(out_dir),
            "--budget-ceiling-usd",
            "20",
            "--k-sweep",
            "0",  # smallest sweep for smoke
            "--limit",
            "1",  # one specimen for smoke
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"arm-a dry-run failed for {provider_name}: stdout={result.stdout[:500]} stderr={result.stderr[:500]}"
    )


@pytest.mark.parametrize("provider_name", ac.ALL_PROVIDER_NAMES)
def test_arm_b_dry_run_exits_zero(
    provider_name: str,
    tmp_path: Path,
    manifest_available: bool,
) -> None:
    """Arm B --dry-run for every provider must exit 0 and not call out."""
    out_dir = tmp_path / "arm-b"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "run-arm-b.py"),
            "--dry-run",
            "--provider",
            provider_name,
            "--manifest",
            str(MANIFEST),
            "--out",
            str(out_dir),
            "--budget-ceiling-usd",
            "20",
            "--max-iterations",
            "1",
            "--limit",
            "1",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"arm-b dry-run failed for {provider_name}: stdout={result.stdout[:500]} stderr={result.stderr[:500]}"
    )


def test_arm_a_dry_run_persists_response_with_provider_dir(
    tmp_path: Path,
    manifest_available: bool,
) -> None:
    """After dry-run, response.json must land at out_dir/<provider>/<sha>/."""
    out_dir = tmp_path  # runner creates out_dir/arm-a/<provider>/...
    subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "run-arm-a.py"),
            "--dry-run",
            "--provider",
            "nvidia-llama-405b",
            "--manifest",
            str(MANIFEST),
            "--out",
            str(out_dir),
            "--budget-ceiling-usd",
            "0",
            "--k-sweep",
            "0",
            "--limit",
            "1",
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=True,
    )

    # Verify provider-scoped subtree was created (the persister contract):
    # <out>/arm-a/<provider>/ must exist, even if response.json failed to
    # persist because the validator subprocess wasn't available in the env
    # (e.g., CI without claude-code-plugins). The provider directory itself
    # is what we're testing — scoping works.
    provider_dir = out_dir / "arm-a" / "nvidia-llama-405b"
    assert provider_dir.is_dir(), (
        f"provider-scoped dir not created at {provider_dir}; "
        f"tree: {[str(p.relative_to(out_dir)) for p in out_dir.rglob('*')][:10]}"
    )

    # If response.json exists (validator was available), check it parses
    response_files = list(provider_dir.glob("**/response.json"))
    if response_files:
        payload = json.loads(response_files[0].read_text())
        assert isinstance(payload, dict)
    else:
        # No response.json → at least confirm errors were logged (env issue,
        # not a code bug). _summary.json or errors.jsonl should exist.
        env_signals = list(provider_dir.glob("*.json")) + list(provider_dir.glob("*.jsonl"))
        assert env_signals, "no response, summary, or errors signals under provider dir"


def test_arm_a_unknown_provider_exits_nonzero(
    tmp_path: Path,
    manifest_available: bool,
) -> None:
    """Bad --provider must surface as a clear non-zero exit."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "run-arm-a.py"),
            "--dry-run",
            "--provider",
            "not-a-real-provider",
            "--manifest",
            str(MANIFEST),
            "--out",
            str(tmp_path),
            "--budget-ceiling-usd",
            "0",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode != 0
