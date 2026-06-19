"""Pure-logic tests for _arm_common.py — aligned to actual signatures."""

from __future__ import annotations

import json
from pathlib import Path

import _arm_common as ac  # noqa: E402
import pytest

# --- get_provider factory ----------------------------------------------------


@pytest.mark.parametrize("name", ac.ALL_PROVIDER_NAMES)
def test_get_provider_returns_instance_for_every_name(name: str) -> None:
    p = ac.get_provider(name, dry_run=True)
    assert p is not None
    assert hasattr(p, "complete")
    assert hasattr(p, "model")
    assert isinstance(p.model, str) and len(p.model) > 0


def test_get_provider_rejects_unknown_name() -> None:
    with pytest.raises(ValueError, match="Unknown provider"):
        ac.get_provider("not-a-real-provider", dry_run=True)


@pytest.mark.parametrize(
    "name,expected_class_substring",
    [
        ("anthropic-opus", "Anthropic"),
        ("anthropic-haiku", "Anthropic"),
        ("nvidia-llama-405b", "NVIDIA"),
        ("nvidia-nemotron", "NVIDIA"),
        ("groq-llama-70b", "Groq"),
        ("groq-mixtral", "Groq"),
    ],
)
def test_get_provider_routes_to_correct_class(name: str, expected_class_substring: str) -> None:
    p = ac.get_provider(name, dry_run=True)
    assert expected_class_substring in type(p).__name__


# --- is_free_provider --------------------------------------------------------


@pytest.mark.parametrize(
    "name,expected_free",
    [
        ("anthropic-opus", False),
        ("anthropic-sonnet", False),
        ("anthropic-haiku", False),
        ("nvidia-llama-405b", True),
        ("nvidia-llama-70b", True),
        ("nvidia-nemotron", True),
        ("groq-llama-70b", True),
        ("groq-llama-70b-specdec", True),
        ("groq-mixtral", True),
    ],
)
def test_is_free_provider(name: str, expected_free: bool) -> None:
    assert ac.is_free_provider(name) is expected_free


# --- CostMeter (uses UsageRecord) --------------------------------------------


def _usage(cost_usd: float, input_tokens: int = 100, output_tokens: int = 50) -> ac.UsageRecord:
    return ac.UsageRecord(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=cost_usd,
    )


def test_cost_meter_accumulates() -> None:
    cm = ac.CostMeter(ceiling_usd=10.0)
    cm.record(_usage(1.50))
    cm.record(_usage(2.25))
    assert cm.spent_usd == pytest.approx(3.75)
    assert cm.calls == 2


def test_cost_meter_raises_when_paid_call_exceeds_ceiling() -> None:
    cm = ac.CostMeter(ceiling_usd=5.0)
    cm.record(_usage(3.0))
    with pytest.raises(ac.BudgetExceeded):
        cm.record(_usage(2.5))  # 5.5 > 5.0


def test_cost_meter_zero_cost_does_not_raise_at_zero_ceiling() -> None:
    """Free-tier providers record $0 cost; ceiling 0 must not block them."""
    cm = ac.CostMeter(ceiling_usd=0.0)
    for _ in range(100):
        cm.record(_usage(0.0))
    assert cm.spent_usd == 0.0
    assert cm.calls == 100


# --- ResultPersister idempotency --------------------------------------------


def test_result_persister_creates_provider_scoped_subtree(tmp_path: Path) -> None:
    ac.ResultPersister(
        out_dir=tmp_path,
        arm="arm-a",
        provider="nvidia-llama-405b",
    )
    expected = tmp_path / "arm-a" / "nvidia-llama-405b"
    assert expected.is_dir()


def test_result_persister_writes_then_skips_on_rerun(tmp_path: Path) -> None:
    rp = ac.ResultPersister(
        out_dir=tmp_path,
        arm="arm-a",
        provider="nvidia-llama-405b",
    )
    payload = {"hello": "world", "n": 42}
    sha = "abc12345deadbeef"

    target1 = rp.write_json(sha, "response.json", payload)
    assert target1.exists()
    original = json.loads(target1.read_text())

    # Re-write with different payload but no force — should NOT overwrite
    rp.write_json(sha, "response.json", {"different": "data"})
    after = json.loads(target1.read_text())
    assert after == original  # idempotent skip preserved original


def test_result_persister_force_overwrites(tmp_path: Path) -> None:
    rp = ac.ResultPersister(
        out_dir=tmp_path,
        arm="arm-a",
        provider="nvidia-llama-405b",
        force=True,
    )
    sha = "abc12345"
    rp.write_json(sha, "response.json", {"original": True})
    rp.write_json(sha, "response.json", {"updated": True})
    loaded = json.loads((tmp_path / "arm-a" / "nvidia-llama-405b" / sha[:8] / "response.json").read_text())
    assert loaded == {"updated": True}


# --- frontmatter extraction --------------------------------------------------


def test_extract_frontmatter_normal_case() -> None:
    md = """---
name: example
version: 1.0.0
---

# Body

Some content.
"""
    fm = ac.extract_frontmatter(md)
    assert "name: example" in fm
    assert "version: 1.0.0" in fm
    assert "# Body" not in fm


def test_extract_frontmatter_no_frontmatter_returns_full_text() -> None:
    """Per actual impl: returns full text if not starting with ---."""
    md = "# Just a body\n\nNo frontmatter.\n"
    fm = ac.extract_frontmatter(md)
    assert fm == md


def test_extract_frontmatter_unclosed_returns_full_text() -> None:
    """Pathological input: --- but no closing delimiter → returns full text."""
    md = "---\nname: unclosed\n\nBody.\n"
    fm = ac.extract_frontmatter(md)
    assert fm == md  # unclosed → fallback


# --- _make_synthetic_response (dry-run shape) -------------------------------


def test_synthetic_response_returns_completion_result() -> None:
    result = ac._make_synthetic_response(
        prompt="You are improving a SKILL.md frontmatter file...",
        model="meta/llama-3.1-405b-instruct",
        provider_name="nvidia-llama-405b",
    )
    assert isinstance(result, ac.CompletionResult)
    assert result.provider == "nvidia-llama-405b"
    assert result.text and len(result.text) > 0


def test_synthetic_response_for_arm_b_returns_valid_proposal_json() -> None:
    """Dry-run for arm-b-style prompt must return valid arm-b-proposal/v1 JSON."""
    result = ac._make_synthetic_response(
        prompt="Return arm-b-proposal/v1 with bounded edit ops...",
        model="meta/llama-3.1-405b-instruct",
        provider_name="nvidia-llama-405b",
    )
    payload = json.loads(result.text)
    assert payload.get("schema_version") == "arm-b-proposal/v1"
    assert "ops" in payload
    assert isinstance(payload["ops"], list)


def test_synthetic_response_zero_cost_for_free_provider_inputs() -> None:
    """Default per-MTok rates = 0.0 → usage.cost_usd = 0.0 for synthetic."""
    result = ac._make_synthetic_response(
        prompt="anything",
        model="meta/llama-3.1-405b-instruct",
        provider_name="nvidia-llama-405b",
    )
    assert result.usage.cost_usd == 0.0


def test_synthetic_response_nonzero_cost_for_paid_provider_inputs() -> None:
    """Pass per-MTok rates → usage.cost_usd > 0.0."""
    result = ac._make_synthetic_response(
        prompt="anything " * 100,
        model="claude-haiku-4-5",
        provider_name="anthropic-haiku",
        input_usd_per_mtok=1.0,
        output_usd_per_mtok=5.0,
    )
    assert result.usage.cost_usd > 0.0


# --- Known CostMeter bug (filed as follow-up) -------------------------------


@pytest.mark.xfail(
    reason=(
        "CostMeter.record() raises BudgetExceeded when cumulative reaches ceiling "
        "even if the NEW UsageRecord has cost_usd=0.0. Free-tier calls should "
        "always be allowed when enforce_paid_only=True. Filed as follow-up; "
        "fix: check usage.cost_usd > 0 before raising."
    ),
    strict=True,
)
def test_cost_meter_enforce_paid_only_lets_free_calls_through_paid_ceiling() -> None:
    cm = ac.CostMeter(ceiling_usd=5.0, enforce_paid_only=True)
    cm.record(_usage(5.0))  # at ceiling exactly
    cm.record(_usage(0.0))  # currently raises — should not
    assert cm.spent_usd == pytest.approx(5.0)
