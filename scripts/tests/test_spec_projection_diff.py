"""Regression lock for Fitness Function #2 — spec-projection-diff.py.

This file exists because of a specific, expensive failure: FF#2 spent six weeks
reporting "NO semantic drift (0 findings)" while 11 of 16 upstream sources had
drifted. It was not a false negative in the diff logic — `--self-test` was passing
the whole time and remains sound. It was that `--check` read a snapshot hand-vendored
on 2026-05-28 that the capture pipeline never writes to, and compared it against a
committed projection. Both operands were frozen, so a clean result was a structural
certainty rather than a finding.

A soundness self-test cannot catch that class of bug: the differ was sound and the
INPUT was dead. So these tests assert on where `--check` reads from and on whether it
can still fire against real captured content — the two properties that actually
regressed.

Offline, fixture-driven, no network.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CAPTURE_TREE = REPO_ROOT / "specs" / "_vendor"
LEGACY_TREE = REPO_ROOT / "_vendor" / "upstream" / "skill-frontmatter"


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture()
def captured_snapshot_text(spd: ModuleType) -> str:
    return Path(spd.resolve_captured_snapshot()).read_text(encoding="utf-8")


def _perturb(text: str, *, add_field: bool = False, flip_required: bool = False) -> str:
    """Mutate the real captured table the way upstream actually would.

    Anchored on the live column widths so a silently reformatted table fails these
    tests loudly instead of quietly producing an unperturbed control.
    """
    out = text
    if flip_required:
        assert "| `license`       | No       |" in out, "captured table shape changed; update this fixture"
        out = out.replace("| `license`       | No       |", "| `license`       | Yes      |")
    if add_field:
        assert "| `metadata`      | No       |" in out, "captured table shape changed; update this fixture"
        out = out.replace(
            "| `metadata`      | No       |",
            "| `icon`          | No       | Optional display glyph. |\n| `metadata`      | No       |",
        )
    return out


# ── The regression that actually happened ─────────────────────────────────────


def test_resolver_points_at_the_capture_tree(spd: ModuleType) -> None:
    resolved = Path(spd.resolve_captured_snapshot())
    assert CAPTURE_TREE in resolved.parents, f"{resolved} is not under the capture tree {CAPTURE_TREE}"
    assert LEGACY_TREE not in resolved.parents
    assert resolved.is_file()


def test_cmd_check_actually_extracts_from_the_capture_tree(spd: ModuleType, monkeypatch: pytest.MonkeyPatch) -> None:
    """THE regression lock: assert on the path `cmd_check` really reads.

    Deliberately spies on the call rather than on the resolver. Testing the resolver
    alone does not lock anything — `cmd_check` can be repointed straight back at the
    frozen legacy snapshot and a resolver-only assertion still passes green. (Checked:
    it does. That is why this test is written this way.)
    """
    seen: list[str] = []
    real_extract = spd.extract_projection

    def spy(path: str):
        seen.append(path)
        return real_extract(path)

    monkeypatch.setattr(spd, "extract_projection", spy)
    spd.cmd_check(str(LEGACY_TREE))

    assert len(seen) == 1, f"expected exactly one extraction, got {seen}"
    used = Path(seen[0])
    assert CAPTURE_TREE in used.parents, (
        f"cmd_check extracted from {used}, which is not under the capture tree. "
        "FF#2 has regressed to diffing a snapshot the pipeline cannot advance."
    )
    assert LEGACY_TREE not in used.parents, "cmd_check regressed to the frozen legacy snapshot"


def test_capture_tree_snapshot_is_newer_than_the_frozen_legacy_one(spd: ModuleType) -> None:
    """The point of the repoint: the side being diffed must be able to move.

    The legacy snapshot is pinned at 2026-05-28 by its own header and cannot advance;
    the captured one carries a vendor-meta timestamp that the pipeline updates.
    """
    meta = json.loads((CAPTURE_TREE / "agentskills-spec" / "vendor-meta.json").read_text(encoding="utf-8"))
    assert meta["updated_at"] > "2026-05-28", "captured snapshot is no fresher than the frozen legacy one"
    assert meta["sha256"], "captured snapshot has no content hash — provenance is broken"


def test_check_fires_on_a_real_perturbation_of_the_captured_snapshot(spd: ModuleType, captured_snapshot_text: str, tmp_path: Path) -> None:
    """Detects drift in the CAPTURED table format, not just in synthetic dicts.

    --self-test already proves the diff algebra. This proves the extractor and the
    real snapshot still line up, which is what makes the algebra reachable.
    """
    perturbed = tmp_path / "snapshot.md"
    perturbed.write_text(_perturb(captured_snapshot_text, add_field=True, flip_required=True), encoding="utf-8")

    rc = spd.cmd_check(str(LEGACY_TREE), str(perturbed))
    assert rc == 1, "perturbed upstream shape did not produce a drift exit code"

    base = json.loads((LEGACY_TREE / "projection.v1.json").read_text(encoding="utf-8"))
    findings = spd.diff_projections(base, spd.extract_projection(str(perturbed)))
    assert any(f.startswith("ADDED_FIELD") and "icon" in f for f in findings)
    assert any(f.startswith("REQUIRED_CHANGED") and "license" in f for f in findings)


def test_check_is_clean_on_the_unperturbed_captured_snapshot(spd: ModuleType) -> None:
    """The control. A green result must mean agreement, not an unreachable comparison.

    Paired with the perturbation test above, this is what separates "we checked and
    it matches" from "we cannot check".
    """
    assert spd.cmd_check(str(LEGACY_TREE)) == 0


# ── No silent fallbacks ───────────────────────────────────────────────────────


def test_missing_captured_snapshot_exits_2_rather_than_falling_back(spd: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """A missing capture must be loud. Falling back to a frozen snapshot is the bug."""
    monkeypatch.setattr(spd, "CAPTURE_VENDOR_ROOT", str(tmp_path / "nonexistent"))
    with pytest.raises(SystemExit) as exc:
        spd.resolve_captured_snapshot()
    assert exc.value.code == 2


def test_surface_declaring_a_different_contract_is_rejected(spd: ModuleType) -> None:
    """Guards the 1:many contract->surface relation.

    `platform-skills-overview` and `skills-releases` also declare contract
    `skill-frontmatter`, and `mcp-schema-ts` declares `mcp-config`. Silently
    projecting the wrong surface with this extractor would produce confident
    nonsense.
    """
    with pytest.raises(SystemExit) as exc:
        spd.resolve_captured_snapshot("mcp-schema-ts")
    assert exc.value.code == 2


def test_unknown_surface_is_rejected(spd: ModuleType) -> None:
    with pytest.raises(SystemExit) as exc:
        spd.resolve_captured_snapshot("no-such-surface")
    assert exc.value.code == 2


def test_default_surface_is_monitored_in_the_registry(spd: ModuleType) -> None:
    """An unmonitored default would mean a snapshot that never advances — the bug again."""
    registry = json.loads((REPO_ROOT / "specs" / "upstream-surface-registry.v1.json").read_text(encoding="utf-8"))
    surface = next(s for s in registry["surfaces"] if s["name"] == spd.DEFAULT_SURFACE)
    assert surface["monitored"] is True
    assert surface["contract"] == spd.CONTRACT


# ── Differ soundness (unchanged behaviour, kept under test) ───────────────────


def test_self_test_still_passes(spd: ModuleType) -> None:
    assert spd.cmd_self_test() == 0


def test_identical_projections_report_no_drift(spd: ModuleType) -> None:
    base = {"fields": {"name": {"required": True, "experimental": False}}, "deprecations": []}
    assert spd.diff_projections(base, json.loads(json.dumps(base))) == []


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        ({"fields": {"name": {"required": True, "experimental": False}, "new": {"required": False}}}, "ADDED_FIELD"),
        ({"fields": {}}, "REMOVED_FIELD"),
        ({"fields": {"name": {"required": False, "experimental": False}}}, "REQUIRED_CHANGED"),
        ({"fields": {"name": {"required": True, "experimental": True}}}, "EXPERIMENTAL_CHANGED"),
    ],
)
def test_each_drift_class_is_detected(spd: ModuleType, mutation: dict, expected: str) -> None:
    base = {"fields": {"name": {"required": True, "experimental": False}}, "deprecations": []}
    fresh = {"deprecations": [], **mutation}
    assert any(f.startswith(expected) for f in spd.diff_projections(base, fresh))


def test_extract_on_a_table_less_file_exits_2(spd: ModuleType, tmp_path: Path) -> None:
    empty = tmp_path / "no-table.md"
    empty.write_text("# Not a spec page\n\nProse only.\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        spd.extract_projection(str(empty))
    assert exc.value.code == 2
