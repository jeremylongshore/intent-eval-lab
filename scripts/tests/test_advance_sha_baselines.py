from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("advance_sha_baselines", REPO / "scripts" / "advance-sha-baselines.py")
assert _spec and _spec.loader
asb = importlib.util.module_from_spec(_spec)
sys.modules["advance_sha_baselines"] = asb
_spec.loader.exec_module(asb)

H1 = "a" * 64
H2 = "b" * 64


def _report(path: Path, rows: list[dict]) -> Path:
    path.write_text(json.dumps({"checked_at": "2026-10-03T09:00:00Z", "sources": rows}), encoding="utf-8")
    return path


def test_writes_the_observed_hash_for_drift_rows_only(tmp_path: Path) -> None:
    sha = tmp_path / ".sha"
    sha.mkdir()
    (sha / "steady.sha").write_text(H2 + "\n")
    report = _report(
        tmp_path / "r.json",
        [
            {"source": "moved", "status": "drift", "baseline": H2, "current": H1},
            {"source": "steady", "status": "ok", "hash": H2},
            {"source": "down", "status": "fetch_error"},
        ],
    )
    assert asb.advance(str(report), str(sha)) == ["moved"]
    assert (sha / "moved.sha").read_text() == H1 + "\n"
    assert (sha / "steady.sha").read_text() == H2 + "\n"
    assert not (sha / "down.sha").exists()


def test_no_drift_changes_nothing(tmp_path: Path) -> None:
    report = _report(tmp_path / "r.json", [{"source": "steady", "status": "ok", "hash": H2}])
    assert asb.advance(str(report), str(tmp_path / ".sha")) == []
    assert not (tmp_path / ".sha").exists()


@pytest.mark.parametrize(
    "row",
    [
        {"source": "x", "status": "drift", "current": "not-a-hash"},
        {"source": "x", "status": "drift"},
        {"source": "../escape", "status": "drift", "current": H1},
    ],
)
def test_malformed_drift_row_fails_closed(tmp_path: Path, row: dict) -> None:
    report = _report(tmp_path / "r.json", [row])
    with pytest.raises(ValueError):
        asb.advance(str(report), str(tmp_path / ".sha"))
    assert not list((tmp_path).glob(".sha/*"))


def test_cli_exit_codes(tmp_path: Path, monkeypatch) -> None:
    good = _report(tmp_path / "r.json", [{"source": "moved", "status": "drift", "current": H1}])
    monkeypatch.setattr(sys, "argv", ["x", "--report", str(good), "--sha-dir", str(tmp_path / ".sha")])
    assert asb.main() == 0
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    monkeypatch.setattr(sys, "argv", ["x", "--report", str(bad), "--sha-dir", str(tmp_path / ".sha")])
    assert asb.main() == 2
