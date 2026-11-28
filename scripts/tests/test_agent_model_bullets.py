"""Frozen sub-agent docs have two equivalent spellings for the model list."""
import runpy
from pathlib import Path

import pytest


model_facts = runpy.run_path(str(Path(__file__).resolve().parents[1] / "extract-agent-definition-projection.py"))["_model_facts"]


def test_compact_alias_and_inherit_bullets():
    facts = model_facts(["* **Model alias**: `sonnet`, `opus`, or `fable`", "* **`inherit`**: parent model"])
    assert facts == {"model_aliases_documented": ["sonnet", "opus", "fable"], "model_inherit_documented": True}


@pytest.mark.parametrize("bullets", [[], ["* **Model alias**: for example `opus`"], ["* **Model alias**: `opus`"] * 2])
def test_ambiguous_alias_list_requires_review(bullets):
    with pytest.raises(ValueError):
        model_facts(bullets)
