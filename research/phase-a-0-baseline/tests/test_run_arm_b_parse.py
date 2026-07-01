"""Unit tests for run-arm-b.py's proposal-parsing guard (_extract_json_object).

Regression coverage for the null/non-object response bug: `json.loads` accepts
`null` (-> None), arrays, and bare scalars WITHOUT raising, so those responses
must be reported as parse errors rather than slipping through as a "valid"
proposal (which previously crashed the dry-run assert / _validate_proposal.get()).

run-arm-b.py has a hyphenated filename, so it is loaded via importlib rather than
imported. conftest.py puts scripts/ on sys.path so its `_arm_common` import
resolves.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
RUN_ARM_B = REPO_ROOT / "research" / "phase-a-0-baseline" / "scripts" / "run-arm-b.py"


@pytest.fixture(scope="module")
def arm_b() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_arm_b_mod", RUN_ARM_B)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    # run-arm-b.py has module-level code that does sys.modules.get(cls.__module__)
    # — register before exec so that lookup resolves (standard importlib pattern).
    sys.modules[spec.name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    return mod


@pytest.mark.parametrize(
    "response",
    ["null", "[1, 2, 3]", "42", '"a bare string"', "true"],
)
def test_non_object_responses_are_parse_errors(arm_b: ModuleType, response: str) -> None:
    obj, err = arm_b._extract_json_object(response)
    assert obj is None
    assert err is not None and "not a JSON object" in err


def test_invalid_json_reports_decode_error(arm_b: ModuleType) -> None:
    obj, err = arm_b._extract_json_object("not json {")
    assert obj is None
    assert err is not None and "JSON decode error" in err


def test_object_in_code_fence_is_extracted(arm_b: ModuleType) -> None:
    obj, err = arm_b._extract_json_object('```json\n{"rationale": "x", "ops": []}\n```')
    assert err is None
    assert obj == {"rationale": "x", "ops": []}


def test_plain_object_is_extracted(arm_b: ModuleType) -> None:
    obj, err = arm_b._extract_json_object('{"rationale": "y", "ops": []}')
    assert err is None
    assert obj == {"rationale": "y", "ops": []}


def test_null_response_never_yields_a_proposal(arm_b: ModuleType) -> None:
    """The end-to-end guard the bug violated: a `null` response produces an
    error + no proposal, never an EditProposal."""
    obj, err = arm_b._extract_json_object("null")
    proposal, verr = (None, err)
    if obj is not None:  # not taken for a null response
        proposal, verr = arm_b._validate_proposal(obj)
    assert proposal is None
    assert verr is not None
