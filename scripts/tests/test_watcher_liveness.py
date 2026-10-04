"""Unit tests for scripts/watcher-liveness.py — fetch-error + baseline-stale streaks."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
MOD_PATH = REPO / "scripts" / "watcher-liveness.py"

_spec = importlib.util.spec_from_file_location("watcher_liveness", MOD_PATH)
assert _spec and _spec.loader
wl = importlib.util.module_from_spec(_spec)
sys.modules["watcher_liveness"] = wl
_spec.loader.exec_module(wl)


def _write_drift(path: Path, rows: list[dict], checked_at: str = "2026-07-23T12:00:00Z") -> None:
    path.write_text(
        json.dumps({"checked_at": checked_at, "sources": rows}, indent=2) + "\n",
        encoding="utf-8",
    )


def test_fetch_error_streak_trips_at_threshold(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    drift = tmp_path / "drift.json"
    # threshold defaults to 3 via empty state
    for i in range(2):
        _write_drift(drift, [{"source": "s1", "status": "fetch_error"}])
        assert wl.cmd_record_run(str(state), str(drift), f"2026-07-2{i}T12:00:00Z") == 0
    _write_drift(drift, [{"source": "s1", "status": "fetch_error"}])
    assert wl.cmd_record_run(str(state), str(drift), "2026-07-23T12:00:00Z") == 1
    st = json.loads(state.read_text())
    assert st["surfaces"]["s1"]["fetch_error_streak"] == 3


def test_ok_status_resets_fetch_error_streak(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    drift = tmp_path / "drift.json"
    _write_drift(drift, [{"source": "s1", "status": "fetch_error"}])
    wl.cmd_record_run(str(state), str(drift), "2026-07-21T12:00:00Z")
    _write_drift(drift, [{"source": "s1", "status": "ok"}])
    assert wl.cmd_record_run(str(state), str(drift), "2026-07-22T12:00:00Z") == 0
    st = json.loads(state.read_text())
    assert st["surfaces"]["s1"]["fetch_error_streak"] == 0


def test_baseline_stale_streak_increments_on_drift_only(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    drift = tmp_path / "drift.json"
    for i in range(2):
        _write_drift(drift, [{"source": "s1", "status": "drift"}])
        assert wl.cmd_record_run(str(state), str(drift), f"2026-07-2{i}T12:00:00Z") == 0
    st = json.loads(state.read_text())
    assert st["surfaces"]["s1"]["baseline_stale_streak"] == 2
    assert st["surfaces"]["s1"]["fetch_error_streak"] == 0


def test_baseline_stale_streak_trips_at_threshold(tmp_path: Path) -> None:
    # baseline-stale has its own threshold (default 7: "merge the promotion PR at
    # least weekly"), separate from the fetch-error streak's 3. "s1" is not in the
    # registry, so it is treated as enforced (fail-safe).
    state = tmp_path / "state.json"
    drift = tmp_path / "drift.json"
    for i in range(7):
        _write_drift(drift, [{"source": "s1", "status": "drift"}])
        rc = wl.cmd_record_run(str(state), str(drift), f"2026-07-2{i}T12:00:00Z")
        if i < 6:
            assert rc == 0
        else:
            assert rc == 1
    st = json.loads(state.read_text())
    assert st["surfaces"]["s1"]["baseline_stale_streak"] == 7


def _registry(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "surfaces": [
                    {"name": "signal", "semantic_coverage": {"status": "byte-hash-only"}},
                    {"name": "normative", "semantic_coverage": {"status": "field-level"}},
                ]
            }
        ),
        encoding="utf-8",
    )
    return path


def test_signal_only_source_is_advisory_and_never_trips(tmp_path: Path, capsys) -> None:
    state = tmp_path / "state.json"
    drift = tmp_path / "drift.json"
    reg = _registry(tmp_path / "registry.json")
    for i in range(10):
        _write_drift(drift, [{"source": "signal", "status": "drift"}])
        assert wl.cmd_record_run(str(state), str(drift), f"2026-07-{10 + i}T12:00:00Z", str(reg)) == 0
    st = json.loads(state.read_text())
    assert st["surfaces"]["signal"]["baseline_stale_streak"] == 10  # still tracked
    assert "advisory" in capsys.readouterr().out


def test_field_level_source_still_trips(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    drift = tmp_path / "drift.json"
    reg = _registry(tmp_path / "registry.json")
    rcs = []
    for i in range(7):
        _write_drift(drift, [{"source": "normative", "status": "drift"}, {"source": "signal", "status": "drift"}])
        rcs.append(wl.cmd_record_run(str(state), str(drift), f"2026-07-{10 + i}T12:00:00Z", str(reg)))
    assert rcs == [0, 0, 0, 0, 0, 0, 1]


def test_signal_only_classification_reads_the_real_registry() -> None:
    signal = wl.signal_only_surfaces(wl.DEFAULT_REGISTRY)
    assert {"claude-code-changelog", "claude-code-npm", "platform-skills-overview"} <= signal
    assert not {"claude-hooks", "plugins-reference", "sub-agents", "plugin-marketplaces", "agentskills-spec"} & signal


def test_missing_registry_treats_everything_as_enforced(tmp_path: Path) -> None:
    assert wl.signal_only_surfaces(str(tmp_path / "absent.json")) == set()


def test_baseline_advance_resets_stale_streak(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    drift = tmp_path / "drift.json"
    for i in range(2):
        _write_drift(drift, [{"source": "s1", "status": "drift"}])
        wl.cmd_record_run(str(state), str(drift), f"2026-07-2{i}T12:00:00Z")
    # Promotion / refresh advances baseline
    _write_drift(drift, [{"source": "s1", "status": "refreshed"}])
    assert wl.cmd_record_run(str(state), str(drift), "2026-07-23T12:00:00Z") == 0
    st = json.loads(state.read_text())
    assert st["surfaces"]["s1"]["baseline_stale_streak"] == 0


def test_fetch_error_does_not_increment_baseline_stale(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    drift = tmp_path / "drift.json"
    _write_drift(drift, [{"source": "s1", "status": "drift"}])
    wl.cmd_record_run(str(state), str(drift), "2026-07-21T12:00:00Z")
    _write_drift(drift, [{"source": "s1", "status": "fetch_error"}])
    wl.cmd_record_run(str(state), str(drift), "2026-07-22T12:00:00Z")
    st = json.loads(state.read_text())
    assert st["surfaces"]["s1"]["baseline_stale_streak"] == 1
    assert st["surfaces"]["s1"]["fetch_error_streak"] == 1


def test_backfills_baseline_stale_key_on_legacy_state(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    state.write_text(
        json.dumps(
            {
                "state_version": "watcher-liveness/v1",
                "streak_threshold": 3,
                "surfaces": {"s1": {"fetch_error_streak": 0, "last_ok_utc": None}},
            }
        )
    )
    drift = tmp_path / "drift.json"
    _write_drift(drift, [{"source": "s1", "status": "drift"}])
    assert wl.cmd_record_run(str(state), str(drift), "2026-07-23T12:00:00Z") == 0
    st = json.loads(state.read_text())
    assert st["surfaces"]["s1"]["baseline_stale_streak"] == 1
