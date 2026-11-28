"""Offline integrity of the frozen synthetic document corpus; never render input."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pytest

CORPUS = Path(__file__).resolve().parents[2] / "evals/adversarial-documents/v1"
MANIFEST_BYTES = (CORPUS / "manifest.json").read_bytes()
MANIFEST = json.loads(MANIFEST_BYTES)
FROZEN_MANIFEST_SHA256 = "864cac10a75dd57f678e8ee56d3b29b6dbe4c3d201e8e1c394ae71770c2f0b03"


def test_manifest_is_frozen_including_provenance_and_labels():
    assert hashlib.sha256(MANIFEST_BYTES).hexdigest() == FROZEN_MANIFEST_SHA256
    assert MANIFEST["corpus_version"] == "adversarial-documents/v1"
    assert MANIFEST["status"] == "seed-unmeasured"
    assert re.fullmatch(r"[0-9a-f]{40}", MANIFEST["source"]["commit"])
    assert MANIFEST["case_count"] == len(MANIFEST["cases"]) == 10


def test_case_inventory_and_required_families():
    cases = MANIFEST["cases"]
    ids = [case["id"] for case in cases]
    documents = [case["document"] for case in cases]
    assert len(set(ids)) == len(ids)
    assert len(set(documents)) == len(documents)
    actual = {p.relative_to(CORPUS).as_posix() for p in (CORPUS / "cases").rglob("*")}
    assert actual == set(documents)
    assert {case["family"] for case in cases} == {
        "instruction-injection",
        "raw-latex",
        "remote-fetch",
        "tex-file-read",
        "benign-control",
    }


@pytest.mark.parametrize("case", MANIFEST["cases"], ids=lambda case: case["id"])
def test_document_bytes_and_metadata(case):
    assert re.fullmatch(r"[a-z][a-z0-9-]+", case["id"])
    assert case["document"] == f"cases/{case['id']}.md"
    path = CORPUS / case["document"]
    assert not path.is_symlink()
    assert path.resolve().is_relative_to(CORPUS.resolve())
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == case["sha256"]
    text = raw.decode("utf-8")
    assert text.startswith("---\n") and text.endswith("\n")
    assert MANIFEST["setup"]["canary_text"].strip() not in text
    assert case["synthetic"] is True
    source = case["source"]
    assert re.fullmatch(r"[0-9a-f]{64}", source["sha256"])
    assert source["path"].startswith(("tests/", "evals/scenarios/"))
    assert source["selector"] and source["transformation"]
    expected = case["expected"]
    assert expected["outcome"] in {
        "refuse",
        "deliver-literal",
        "refuse-or-render-without-leak",
    }
    assert expected["invariants"]
    if case["family"] == "benign-control":
        assert expected["outcome"] == "deliver-literal"
    if MANIFEST["setup"]["path_placeholder"] in text:
        assert "no-canary-in-any-rendered-artifact" in expected["invariants"]
    if case["family"] in {"remote-fetch", "instruction-injection"}:
        assert "no-network" in expected["invariants"]
