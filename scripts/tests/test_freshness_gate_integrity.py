"""Regression locks for the nine defects an adversarial review found in the freshness gate.

The gate shipped in #237 green, with a mutation-tested lock, and still carried two
P1s. Both were the SAME failure class the gate exists to end, re-entering by a door
the lock did not watch:

  F1  the registry can name a checker in the WRONG MODE (`--check` instead of
      `--check-fresh`), which compares frozen against frozen and prints an
      authoritative all-green board — for surfaces with real outstanding findings.
      Every gate blessed it, because they validated that `checker[0]` was a FILE
      and never what the argv MEANS.

  F2  `plugin-manifest` asserted a silently TRUNCATED closed enum. Its two siblings
      decline on the same input; only it produced confident nonsense. A short enum
      is worse than an absence: the projection is the field-diff baseline, so the
      next report reads as a legitimate value REMOVAL and sends a human to
      reconcile a phantom.

The lesson generalises, and these tests encode it: **a gate that validates the
EXISTENCE of its machinery has not validated the BEHAVIOUR of it.**

Every test here corresponds to a defect that was reproduced first, then fixed.
Offline, fixture-driven, no network.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY = REPO_ROOT / "specs" / "upstream-surface-registry.v1.json"
REGISTRY_GATE = REPO_ROOT / "scripts" / "check-surface-registry.py"
FRESHNESS = REPO_ROOT / "scripts" / "projection-freshness.py"
PROVENANCE_GATE = REPO_ROOT / "scripts" / "check-vendor-meta-integrity.py"

CLEAN, DRIFT, INOPERABLE = 0, 1, 2


def _field_level_count() -> int:
    """How many surfaces are field-level right now.

    Deliberately derived, not hard-coded: a literal would silently under-mutate
    the moment a surface is promoted, leaving this test passing while no longer
    exercising the empty-map path it exists for.
    """
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return sum(
        1 for s in registry["surfaces"] if (s.get("semantic_coverage") or {}).get("status") == "field-level"
    )


def _run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(script), *args], cwd=REPO_ROOT, capture_output=True, text=True)


@pytest.fixture()
def registry_text() -> str:
    return REGISTRY.read_text(encoding="utf-8")


@pytest.fixture()
def mutate_registry(registry_text: str):
    """Apply a text mutation to the committed registry, restore it afterwards."""
    original = registry_text

    def _apply(old: str, new: str, count: int = 1) -> None:
        assert original.count(old) >= count, f"registry shape changed; fixture is stale: {old!r}"
        REGISTRY.write_text(original.replace(old, new, count), encoding="utf-8")

    try:
        yield _apply
    finally:
        REGISTRY.write_text(original, encoding="utf-8")


# ── F1: the checker's MODE, not just its existence ───────────────────────────


def test_registry_gate_rejects_a_checker_in_self_consistency_mode(mutate_registry) -> None:
    """THE P1. `--check-fresh` -> `--check` re-arms frozen-vs-frozen everywhere.

    Before the fix this passed check-surface-registry.py AND the test suite, and
    the driver then reported five CLEAN enforced surfaces including one with three
    real findings.
    """
    mutate_registry(
        '"scripts/extract-agent-definition-projection.py",\n          "--check-fresh"',
        '"scripts/extract-agent-definition-projection.py",\n          "--check"',
    )
    result = _run(REGISTRY_GATE)
    assert result.returncode == 1
    assert "freshness mode" in result.stdout


def test_registry_gate_rejects_a_checker_with_no_mode_flag(mutate_registry) -> None:
    mutate_registry(
        '"scripts/extract-hook-config-projection.py",\n          "--check-fresh"',
        '"scripts/extract-hook-config-projection.py"',
    )
    assert _run(REGISTRY_GATE).returncode == 1


def test_registry_gate_rejects_a_mutating_mode_flag(mutate_registry) -> None:
    """`--write` would have the gate MUTATE the baseline it exists to guard."""
    mutate_registry(
        '"scripts/extract-plugin-manifest-projection.py",\n          "--check-fresh"',
        '"scripts/extract-plugin-manifest-projection.py",\n          "--write"',
    )
    assert _run(REGISTRY_GATE).returncode == 1


def test_registry_gate_rejects_an_unregistered_checker(mutate_registry) -> None:
    """A checker whose fresh mode is unpinned could be anything at all."""
    mutate_registry('"scripts/spec-projection-diff.py"', '"scripts/fetch-capture.py"')
    result = _run(REGISTRY_GATE)
    assert result.returncode == 1
    assert "not a registered freshness checker" in result.stdout


@pytest.mark.parametrize(
    "contract",
    ["agent-definition", "hook-config", "marketplace-catalog", "plugin-manifest"],
)
def test_surface_is_rejected_outside_check_fresh(contract: str) -> None:
    """Defence in depth: the silently-IGNORED argument was the enabling condition.

    `--surface` is a top-level parser arg, so the wrong mode accepted it and threw
    it away. Nothing objected — which is what made a one-token registry edit
    invisible end-to-end.
    """
    script = REPO_ROOT / "scripts" / f"extract-{contract}-projection.py"
    result = _run(script, "--check", "--surface", "anything")
    assert result.returncode == 2
    assert "only to --check-fresh" in result.stderr


# ── F2: a truncated closed enum is worse than no enum ────────────────────────


@pytest.mark.parametrize(
    ("desc", "expect_enum", "expect_candidates"),
    [
        # Unchanged behaviour: a genuinely closed set stays a closed set.
        (
            "One of `string`, `number`, `boolean`, `directory`, or `file`.",
            ["string", "number", "boolean", "directory", "file"],
            None,
        ),
        # Was ['command'] asserted as CLOSED — the P1. Now open, and complete.
        (
            "One of `command` (Claude Code v2.1.200+), `http`, or `mcp_tool`.",
            None,
            ["command", "http", "mcp_tool"],
        ),
        # Was ['command', 'http'] asserted as CLOSED. MDX is markup, not prose.
        (
            "One of `command`, `http`, or {/* min-version: 2.1.200 */}`mcp_tool`.",
            ["command", "http", "mcp_tool"],
            None,
        ),
    ],
)
def test_plugin_manifest_never_asserts_a_truncated_enum(
    extractors: dict[str, ModuleType], desc: str, expect_enum: list[str] | None, expect_candidates: list[str] | None
) -> None:
    enum, candidates = extractors["plugin-manifest"]._enum_from_description(desc)
    assert enum == expect_enum, f"closed-enum mismatch for {desc!r}"
    assert candidates == expect_candidates, f"open-candidate mismatch for {desc!r}"


def test_a_version_number_period_is_not_a_sentence_end(captured_source: ModuleType) -> None:
    """The shared root cause of both the wrong answer and the silent one.

    Upstream writes version-gated values inline. Stopping a value clause at the
    first bare '.' truncated it inside `2.1.200`, which one extractor asserted as
    a closed enum and another discarded entirely.
    """
    assert captured_source.clause_end("`a`, `b` (v2.1.200+), or `c`. Then prose") == len("`a`, `b` (v2.1.200+), or `c`")
    assert captured_source.clause_end("no period here") == -1
    assert captured_source.clause_end("ends here. and more") == len("ends here")


@pytest.mark.parametrize("contract", ["agent-definition", "plugin-manifest"])
def test_enum_and_candidates_stay_mutually_exclusive(extractors: dict[str, ModuleType], contract: str) -> None:
    """A field carrying both would assert a set is closed AND open at once."""
    vendor_dir = str(REPO_ROOT / "specs" / "_vendor" / "upstream" / contract)
    rendered = json.loads(extractors[contract].render(extractors[contract].build_projection(vendor_dir)))

    def walk(node: object, path: str = "") -> None:
        if isinstance(node, dict):
            assert not ("enum" in node and "enum_candidates" in node), f"{path} claims both closed and open"
            if "enum_candidates" in node:
                assert node.get("enum_clause_open") is True, f"{path} has candidates without the openness marker"
            for key, value in node.items():
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for i, value in enumerate(node):
                walk(value, f"{path}[{i}]")

    walk(rendered)


# ── F3 / F9: an empty or shrunken map is not a clean map ─────────────────────


def test_zero_field_level_surfaces_is_inoperable(mutate_registry) -> None:
    """Was: "CLEAN (exit 0) over 0 field-level surface(s)" — green, having
    compared nothing, in a module whose own docstring forbids exactly that."""
    mutate_registry('"status": "field-level"', '"status": "byte-hash-only"', count=_field_level_count())
    result = _run(FRESHNESS)
    assert result.returncode == INOPERABLE
    assert "ZERO field-level surfaces" in result.stderr


def test_coverage_shrinking_below_the_floor_is_inoperable(mutate_registry) -> None:
    """"The map got smaller" and "the map is clean" must not be the same green."""
    mutate_registry('"status": "field-level"', '"status": "byte-hash-only"', count=2)
    result = _run(FRESHNESS)
    assert result.returncode == INOPERABLE
    assert "below the registry's declared floor" in result.stderr


def test_the_declared_floor_matches_reality(mutate_registry) -> None:
    """A floor above actual coverage would make the gate permanently inoperable;
    a floor of zero would make it decorative."""
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    floor = registry["semantic_coverage_floor"]["field_level"]
    actual = sum(1 for s in registry["surfaces"] if (s.get("semantic_coverage") or {}).get("status") == "field-level")
    assert isinstance(floor, int) and floor >= 1
    assert actual >= floor
    assert _run(FRESHNESS).returncode in (CLEAN, DRIFT)


# ── F4: a parser breakage is INOPERABLE, never DRIFT ─────────────────────────


def test_an_unparseable_capture_is_inoperable_not_drift(
    extractors: dict[str, ModuleType], tmp_path: Path
) -> None:
    """Bare next()/json.loads raise StopIteration/JSONDecodeError on a malformed
    capture. Uncaught, python exits 1 — which the driver reads as DRIFT, so the
    watcher opens a RECONCILIATION issue for a PARSER breakage. Reconciling a
    phantom drift is worse than no signal.
    """
    mod = extractors["agent-definition"]
    real = (REPO_ROOT / "specs" / "_vendor" / "sub-agents" / "snapshot.md").read_text(encoding="utf-8")
    lines = real.splitlines(True)
    start = next(i for i, ln in enumerate(lines) if ln.startswith("### Write subagent files"))
    fence = next(j for j in range(start + 4, len(lines)) if lines[j].strip() == "```")
    del lines[fence]

    surface_dir = tmp_path / "sub-agents"
    surface_dir.mkdir()
    (surface_dir / "snapshot.md").write_text("".join(lines), encoding="utf-8")

    mod.captured_source.CAPTURE_VENDOR_ROOT = str(tmp_path)
    try:
        try:
            rc = mod.cmd_check_fresh(str(REPO_ROOT / "specs" / "_vendor" / "upstream" / "agent-definition"))
        except SystemExit as exc:
            rc = exc.code
        assert rc == INOPERABLE, f"a malformed capture reported {rc}; DRIFT would send a human to reconcile a phantom"
    finally:
        mod.captured_source.CAPTURE_VENDOR_ROOT = str(REPO_ROOT / "specs" / "_vendor")


# ── F5 / F6: the differ must render a finding a human can act on ─────────────


def test_a_one_member_change_in_a_long_enum_is_legible(captured_source: ModuleType) -> None:
    """Was: both sides truncated at 400 chars and byte-identical for every visible
    character, so the reader saw a differing byte COUNT and nothing else.

    A new hook event landing in the 30-entry `events.enum` is the single most
    likely real drift on `claude-hooks`, an ENFORCED surface — i.e. the case most
    likely to be unreadable exactly when it mattered.
    """
    events = [f"Event{i:02d}" for i in range(30)]
    findings = captured_source.diff_projections({"events": {"enum": events}}, {"events": {"enum": [*events, "New"]}})
    assert len(findings) == 1
    assert "New" in findings[0], findings[0]
    assert "truncated" not in findings[0]


def test_removals_and_reorderings_are_distinguished(captured_source: ModuleType) -> None:
    removed = captured_source.diff_projections({"e": ["a", "b", "c"]}, {"e": ["a", "c"]})
    assert any(f.startswith("LIST_CHANGED") and '-["b"]' in f for f in removed), removed
    reordered = captured_source.diff_projections({"e": ["a", "b"]}, {"e": ["b", "a"]})
    assert any(f.startswith("LIST_REORDERED") for f in reordered), reordered


@pytest.mark.parametrize(("base", "fresh"), [(True, 1), (False, 0), (1, 1.0)])
def test_a_type_change_is_a_finding_even_when_python_calls_them_equal(
    captured_source: ModuleType, base: object, fresh: object
) -> None:
    """`True == 1` and `1 == 1.0`, so a bool silently becoming an int — exactly
    what a schema-shape change looks like — used to diff to nothing."""
    findings = captured_source.diff_projections({"required": base}, {"required": fresh})
    assert any(f.startswith("TYPE_CHANGED") for f in findings), findings


def test_the_differ_still_reports_nothing_for_identical_documents(captured_source: ModuleType) -> None:
    doc = {"a": {"b": [1, 2], "c": "x", "d": True, "e": None}}
    assert captured_source.diff_projections(doc, json.loads(json.dumps(doc))) == []


# ── F7: the registry gate must report, not crash ─────────────────────────────


def test_an_unhashable_enforcement_is_reported_not_a_traceback(mutate_registry) -> None:
    """`x in {…}` raises TypeError on a list. The gate died with a traceback
    instead of naming the problem — still red, but useless to the reader."""
    mutate_registry('"enforcement": "failing",', '"enforcement": ["failing"],')
    result = _run(REGISTRY_GATE)
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "enforcement" in result.stdout


# ── F8: the MDX stripper must stay line-bounded ──────────────────────────────


def test_mdx_stripper_cannot_swallow_a_multiline_block(extractors: dict[str, ModuleType]) -> None:
    """An unbalanced `{/*` opening a 16-line commented-out section exists in the
    wild (specs/_vendor/upstream/mcp-config/claude-code-mcp.md). With re.DOTALL
    and a non-greedy match, lifting this regex to document scope would silently
    swallow real content between two unrelated markers."""
    pattern = extractors["agent-definition"]._MDX_COMMENT
    text = "{/* open\nline two\nline three */} kept"
    assert pattern.sub("", text) == text, "the stripper crossed a newline"
    assert pattern.sub("", "a{/* min-version: 2.1.200 */}b") == "ab"


# ── Provenance: the record must describe the bytes on disk ───────────────────


def test_every_vendored_capture_records_its_real_bytes() -> None:
    result = _run(PROVENANCE_GATE)
    assert result.returncode == 0, result.stdout


def test_a_wrong_recorded_sha_is_caught_by_nothing_else(tmp_path: Path) -> None:
    """Three reference docs were re-vendored BY HAND, each editing sha256 and
    bytes in a text editor. `--check` proves the projection derives from the
    FILES and never reads sha256 at all, so a mistyped hash passed every gate
    while the provenance quietly described a file that was not there.
    """
    meta = REPO_ROOT / "specs" / "_vendor" / "upstream" / "agent-definition" / "vendor-meta.json"
    original = meta.read_text(encoding="utf-8")
    payload = json.loads(original)
    entry = next(f for f in payload["files"] if f["role"] == "reference-doc")
    corrupted = original.replace(entry["sha256"], "deadbeef" + entry["sha256"][8:], 1)
    assert corrupted != original

    try:
        meta.write_text(corrupted, encoding="utf-8")
        assert _run(PROVENANCE_GATE).returncode == 1
        # The gate that people believe covers this does not.
        blind = _run(REPO_ROOT / "scripts" / "extract-agent-definition-projection.py", "--check")
        assert blind.returncode == 0, "if --check now catches it, this test's premise needs revisiting"
    finally:
        meta.write_text(original, encoding="utf-8")


def test_an_empty_capture_sweep_is_not_a_pass(tmp_path: Path) -> None:
    """A gate that verified nothing must not print success — the same rule as the
    freshness driver's empty-map check."""
    result = _run(PROVENANCE_GATE, "--vendor-root", str(tmp_path))
    assert result.returncode == 2
    assert "verified NOTHING" in result.stderr
