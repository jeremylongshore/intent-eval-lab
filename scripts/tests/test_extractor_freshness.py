"""Regression lock for `--check-fresh` on the four deep-capture extractors.

WHAT REGRESSED, AND WHY A SELF-TEST CANNOT CATCH IT
---------------------------------------------------
Each extractor's `--check` and `--self-test` were passing every day while 11 of 16
upstream sources drifted. Neither was wrong: `--check` proves the committed
projection matches the vendored doc it was derived from, `--self-test` proves the
extraction anchors work on fixtures, and both remain sound. The bug was that BOTH
operands of `--check` live in `specs/_vendor/upstream/`, a hand-vendored tree
`fetch-capture.py` cannot write. Frozen vs frozen is green by construction.

So the property under test here is not "does the differ work" — it is "does
`--check-fresh` read from the tree that can actually MOVE, and can it still fire
against real captured bytes". A soundness test cannot express that; only a test
that asserts on the path the extractor really opens can.

THIS FILE IS MUTATION-TESTED
----------------------------
In the equivalent lock for FF#2 (PR #234) the first attempt asserted on the
resolver and passed GREEN under the injected regression — because `cmd_check` could
be repointed straight back at the frozen tree without the resolver noticing. The
fix was to spy on the call the extractor actually makes. Same discipline here:
`test_check_fresh_actually_parses_the_captured_tree` spies on `extract_reference_doc`,
and the injected regression (repointing `--check-fresh` at the frozen doc) was
confirmed to turn this suite RED before it was trusted. A lock nobody has tried to
break is a hope, not a lock.

Offline, fixture-driven, no network.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CAPTURE_TREE = REPO_ROOT / "specs" / "_vendor"
FROZEN_TREE = REPO_ROOT / "specs" / "_vendor" / "upstream"
REGISTRY = REPO_ROOT / "specs" / "upstream-surface-registry.v1.json"

CLEAN, DRIFT, INOPERABLE = 0, 1, 2

# contract -> the registry surface its reference doc is fetched from.
CONTRACT_SURFACE = {
    "agent-definition": "sub-agents",
    "hook-config": "claude-hooks",
    "marketplace-catalog": "plugin-marketplaces",
    "plugin-manifest": "plugins-reference",
}
CONTRACTS = sorted(CONTRACT_SURFACE)


def _vendor_dir(contract: str) -> str:
    return str(FROZEN_TREE / contract)


# ── The regression that actually happened ─────────────────────────────────────


@pytest.mark.parametrize("contract", CONTRACTS)
def test_check_fresh_actually_parses_the_captured_tree(
    extractors: dict[str, ModuleType], contract: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """THE lock: assert on the path `--check-fresh` really opens.

    Deliberately spies on `extract_reference_doc` rather than on the resolver.
    Asserting on the resolver alone locks nothing — `cmd_check_fresh` can be
    repointed back at the frozen doc and a resolver-only assertion stays green.
    (Verified by injecting exactly that regression; see the module docstring.)
    """
    mod = extractors[contract]
    seen: list[str] = []
    real = mod.extract_reference_doc

    def spy(path: str):
        seen.append(path)
        return real(path)

    monkeypatch.setattr(mod, "extract_reference_doc", spy)
    mod.cmd_check_fresh(_vendor_dir(contract))

    assert len(seen) == 1, f"expected exactly one reference-doc extraction, got {seen}"
    used = Path(seen[0])
    assert CAPTURE_TREE in used.parents, (
        f"{contract}: --check-fresh parsed {used}, which is not under the capture tree. "
        "It has regressed to a snapshot the pipeline cannot advance."
    )
    assert FROZEN_TREE not in used.parents, f"{contract}: --check-fresh regressed to the frozen vendored doc"
    assert used.parent.name == CONTRACT_SURFACE[contract]


@pytest.mark.parametrize("contract", CONTRACTS)
def test_check_still_parses_the_frozen_tree(
    extractors: dict[str, ModuleType], contract: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The other half: `--check` must NOT have been repointed.

    The two modes answer different questions and both are wanted. Quietly turning
    `--check` into a freshness check would make every PR fail on upstream edits the
    author never touched.
    """
    mod = extractors[contract]
    seen: list[str] = []
    real = mod.extract_reference_doc

    def spy(path: str):
        seen.append(path)
        return real(path)

    monkeypatch.setattr(mod, "extract_reference_doc", spy)
    assert mod.cmd_check(_vendor_dir(contract)) == CLEAN

    assert len(seen) == 1
    assert FROZEN_TREE in Path(seen[0]).parents, "--check was repointed at the capture tree; it must stay frozen-vs-frozen"


@pytest.mark.parametrize("contract", CONTRACTS)
def test_samples_are_never_repointed(extractors: dict[str, ModuleType], contract: str) -> None:
    """Only the parsed reference doc moves.

    Sample corpora are commit-pinned ground truth, and the provenance rule
    (`documented` vs `observed-in-samples`, never promoted) depends on them holding
    still. Repointing them would let a captured page and a moving sample set drift
    into agreement and hide a real change.
    """
    mod = extractors[contract]
    meta = mod.load_vendor_meta(_vendor_dir(contract))
    non_reference = [f for f in meta["files"] if f["role"] != "reference-doc"]
    assert non_reference, "capture has no samples/supporting docs to protect"
    for entry in non_reference:
        assert (FROZEN_TREE / contract / entry["file"]).is_file()


# ── Can it still fire? (a green result must mean agreement, not an unreachable check) ──


@pytest.mark.parametrize("contract", ["hook-config", "plugin-manifest", "agent-definition"])
def test_reconciled_contracts_are_clean(extractors: dict[str, ModuleType], contract: str) -> None:
    """The control. These three were reconciled against the current capture."""
    assert extractors[contract].cmd_check_fresh(_vendor_dir(contract)) == CLEAN


@pytest.mark.parametrize("contract", ["marketplace-catalog"])
def test_undispositioned_contracts_still_report_their_known_drift(
    extractors: dict[str, ModuleType], contract: str
) -> None:
    """Proves --check-fresh is not vacuous on REAL captured content.

    marketplace-catalog carries findings recorded in the registry as awaiting a
    kernel fold-in. If this ever goes green without the registry flipping to
    `failing`, either the finding was silently reconciled or the check went blind.
    """
    assert extractors[contract].cmd_check_fresh(_vendor_dir(contract)) == DRIFT


# ── Open-clause value recording (the permissionMode class of loss) ────────────


def test_open_value_clause_records_every_documented_value(extractors: dict[str, ModuleType]) -> None:
    """`manual` must survive, on the REAL page, not just a fixture.

    Upstream added a 7th permissionMode value phrased as
    "…, `plan`, or {/* min-version: 2.1.200 */}`manual` as an alias for `default`."
    Two independent parse defects each dropped it while still producing a
    plausible-looking list: the clause stop cut INSIDE the version number
    "2.1.200", and the alias phrasing duplicated `default`. A fixture proves the
    rules; this proves they still line up with the page as published.
    """
    mod = extractors["agent-definition"]
    fields = mod.build_projection(_vendor_dir("agent-definition"))["frontmatter"]["fields"]
    pm = fields["permissionMode"]

    assert "enum" not in pm, "the clause is open — `enum` must stay honest about closedness"
    assert pm["enum_clause_open"] is True
    assert pm["enum_candidates"] == [
        "default",
        "acceptEdits",
        "auto",
        "dontAsk",
        "bypassPermissions",
        "plan",
        "manual",
    ], "a documented permission mode was dropped or duplicated by the value-clause parse"


def test_closed_clauses_still_produce_enums_and_no_candidates(extractors: dict[str, ModuleType]) -> None:
    """The change must not loosen the closed-set rule it sits beside.

    `enum` and `enum_candidates` are mutually exclusive by construction; a field
    carrying both would mean the projection is asserting a set is closed AND open.
    """
    mod = extractors["agent-definition"]
    fields = mod.build_projection(_vendor_dir("agent-definition"))["frontmatter"]["fields"]
    assert fields["color"]["enum"] == [
        "red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan",
    ]
    for name, entry in fields.items():
        assert not ("enum" in entry and "enum_candidates" in entry), f"{name} claims both closed and open"
        if "enum_candidates" in entry:
            assert entry.get("enum_clause_open") is True, f"{name} has candidates without the openness marker"


def test_mdx_version_comments_never_reach_the_projection(extractors: dict[str, ModuleType]) -> None:
    """MDX markup is doc-SOURCE noise, not a value. It must not leak into a token."""
    mod = extractors["agent-definition"]
    rendered = mod.render(mod.build_projection(_vendor_dir("agent-definition")))
    assert "{/*" not in rendered and "min-version" not in rendered


@pytest.mark.parametrize("contract", CONTRACTS)
def test_check_fresh_fires_on_a_perturbed_capture(
    extractors: dict[str, ModuleType], contract: str, tmp_path: Path
) -> None:
    """Injected drift in the CAPTURED page must be detected for every contract.

    Perturbation is the crudest one that is guaranteed semantic for all four
    extractors: delete the reference doc's field/lifecycle tables wholesale by
    stripping every table row. A contract whose projection survives that unchanged
    is not reading the doc at all.
    """
    mod = extractors[contract]
    surface = CONTRACT_SURFACE[contract]
    original = (CAPTURE_TREE / surface / "snapshot.md").read_text(encoding="utf-8")
    gutted = "\n".join(ln for ln in original.splitlines() if not ln.lstrip().startswith("|"))

    snapshot_dir = tmp_path / surface
    snapshot_dir.mkdir()
    (snapshot_dir / "snapshot.md").write_text(gutted, encoding="utf-8")

    mod.captured_source.CAPTURE_VENDOR_ROOT = str(tmp_path)
    try:
        # Removing every table breaks a required anchor in some extractors (exit 2,
        # loud) and produces a different projection in others (exit 1). Both are
        # "detected"; silently returning 0 is the failure this asserts against.
        try:
            rc = mod.cmd_check_fresh(_vendor_dir(contract))
        except SystemExit as exc:
            rc = exc.code
        assert rc in (DRIFT, INOPERABLE), f"{contract}: a gutted captured page went undetected (rc={rc})"
    finally:
        mod.captured_source.CAPTURE_VENDOR_ROOT = str(CAPTURE_TREE)


# ── Inoperable is distinguishable from drift, and never from clean ────────────


@pytest.mark.parametrize("contract", CONTRACTS)
def test_unknown_surface_is_inoperable_not_clean(extractors: dict[str, ModuleType], contract: str) -> None:
    assert extractors[contract].cmd_check_fresh(_vendor_dir(contract), surface="no-such-surface") == INOPERABLE


def test_wrong_contract_surface_is_rejected(extractors: dict[str, ModuleType]) -> None:
    """Guards the 1:many contract->surface relation.

    Several surfaces share a contract, and several contracts share a page family.
    Projecting the wrong surface with the wrong extractor produces confident
    nonsense, which is worse than no signal.
    """
    assert extractors["agent-definition"].cmd_check_fresh(_vendor_dir("agent-definition"), surface="claude-hooks") == (
        INOPERABLE
    )


@pytest.mark.parametrize("contract", CONTRACTS)
def test_missing_capture_is_inoperable_never_a_silent_fallback(
    extractors: dict[str, ModuleType], contract: str, tmp_path: Path
) -> None:
    """A missing capture must be loud. Falling back to the frozen doc IS the bug."""
    mod = extractors[contract]
    mod.captured_source.CAPTURE_VENDOR_ROOT = str(tmp_path / "nonexistent")
    try:
        assert mod.cmd_check_fresh(_vendor_dir(contract)) == INOPERABLE
    finally:
        mod.captured_source.CAPTURE_VENDOR_ROOT = str(CAPTURE_TREE)


def test_unmonitored_surface_is_rejected(captured_source: ModuleType) -> None:
    """An unmonitored surface's snapshot never advances — frozen-vs-frozen again."""
    registry = {"surfaces": [{"name": "frozen-thing", "contract": "hook-config", "monitored": False}]}
    with pytest.raises(captured_source.InoperableError, match="not monitored"):
        captured_source.resolve_captured_snapshot("frozen-thing", registry=registry)


def test_reference_doc_without_a_registered_surface_is_rejected(captured_source: ModuleType) -> None:
    """mcp-config's claude-code-mcp.md is exactly this case: surface null, so it
    cannot be repointed. It must raise, not quietly resolve to something else."""
    meta = {"files": [{"file": "claude-code-mcp.md", "role": "reference-doc", "surface": None}]}
    with pytest.raises(captured_source.InoperableError, match="registered as a surface"):
        captured_source.reference_doc_surface(meta)


# ── The generic projection diff ───────────────────────────────────────────────


def test_identical_projections_report_no_drift(captured_source: ModuleType) -> None:
    doc = {"a": {"b": [1, 2], "c": "x"}}
    assert captured_source.diff_projections(doc, json.loads(json.dumps(doc))) == []


@pytest.mark.parametrize(
    ("base", "fresh", "expected"),
    [
        ({"a": 1}, {"a": 1, "b": 2}, "ADDED_KEY: b"),
        ({"a": 1, "b": 2}, {"a": 1}, "REMOVED_KEY: b"),
        ({"a": {"n": 1}}, {"a": {"n": 2}}, "CHANGED_VALUE: a.n"),
        ({"a": ["x"]}, {"a": ["x", "y"]}, "CHANGED_VALUE: a"),
        ({"a": {"b": {"c": 1}}}, {"a": {"b": {}}}, "REMOVED_KEY: a.b.c"),
    ],
)
def test_each_diff_class_is_detected(captured_source: ModuleType, base: dict, fresh: dict, expected: str) -> None:
    findings = captured_source.diff_projections(base, fresh)
    assert any(f.startswith(expected) for f in findings), findings


def test_long_values_are_truncated_but_flagged(captured_source: ModuleType) -> None:
    """A 30-entry enum must not bury the finding it is attached to."""
    findings = captured_source.diff_projections({"e": ["v"] * 200}, {"e": ["w"] * 200})
    assert len(findings) == 1
    assert "truncated" in findings[0]


# ── The registry-driven driver ────────────────────────────────────────────────


def test_every_monitored_surface_states_its_coverage(freshness: ModuleType) -> None:
    """No surface may be silent about whether it is semantically covered.

    An unstated coverage level is how "no extractor" gets mistaken for "not covered
    by design" — the exact confusion that let a 7th contract (slash-commands) sit at
    zero coverage unnoticed.
    """
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    monitored = [s for s in registry["surfaces"] if s.get("monitored")]
    assert monitored
    for surface in monitored:
        cov = surface.get("semantic_coverage")
        assert cov, f"{surface['name']} states no semantic_coverage"
        assert cov["status"] in ("field-level", "byte-hash-only")


def test_field_level_surfaces_name_a_checker_that_exists(freshness: ModuleType) -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    covered = freshness.field_level_surfaces(registry)
    assert len(covered) >= 4, "the four deep-capture contracts must all be field-level covered"
    for surface in covered:
        checker = surface["semantic_coverage"]["checker"]
        assert (REPO_ROOT / checker[0]).is_file(), checker
        assert surface["semantic_coverage"]["enforcement"] in ("failing", "report-only")


def test_known_uncovered_surfaces_carry_a_named_reason(freshness: ModuleType) -> None:
    """`slash-commands`, `mcp-config` and `platform-skills-overview` are the named
    gaps. Recording WHY is what keeps them from reading as deliberate coverage."""
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    byte_only = {s["name"]: s["semantic_coverage"]["reason"] for s in freshness.byte_only_surfaces(registry)}
    for name in ("claude-slash-commands", "mcp-schema-ts", "platform-skills-overview"):
        assert name in byte_only, f"{name} is expected to be a recorded byte-hash-only gap"
        assert len(byte_only[name]) > 20


def test_driver_exit_code_is_the_worst_enforced_verdict(freshness: ModuleType, monkeypatch: pytest.MonkeyPatch) -> None:
    """Report-only surfaces must not colour the exit code, and enforced ones must.

    Both halves matter: without the first this lane goes permanently red and gets
    ignored; without the second the whole gate is decorative.
    """
    registry = {
        "surfaces": [
            {"name": "enforced-clean", "contract": "c", "semantic_coverage": {"status": "field-level", "enforcement": "failing", "checker": ["x"]}},
            {"name": "reporting-drift", "contract": "c", "semantic_coverage": {"status": "field-level", "enforcement": "report-only", "checker": ["y"]}},
        ]
    }
    verdicts = {"enforced-clean": CLEAN, "reporting-drift": DRIFT}
    monkeypatch.setattr(freshness.captured_source, "load_registry", lambda *a, **k: registry)
    monkeypatch.setattr(freshness, "run_checker", lambda s: (verdicts[s["name"]], "stub"))
    monkeypatch.setattr("sys.argv", ["projection-freshness.py"])
    assert freshness.main() == CLEAN

    # …and --strict promotes the report-only drift to a failure.
    monkeypatch.setattr("sys.argv", ["projection-freshness.py", "--strict"])
    assert freshness.main() == DRIFT


def test_driver_treats_an_inoperable_enforced_checker_as_red(
    freshness: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A gate that could not run is not a gate that passed."""
    registry = {
        "surfaces": [
            {"name": "broken", "contract": "c", "semantic_coverage": {"status": "field-level", "enforcement": "failing", "checker": ["z"]}}
        ]
    }
    monkeypatch.setattr(freshness.captured_source, "load_registry", lambda *a, **k: registry)
    monkeypatch.setattr(freshness, "run_checker", lambda s: (INOPERABLE, "boom"))
    monkeypatch.setattr("sys.argv", ["projection-freshness.py"])
    assert freshness.main() == INOPERABLE


def test_driver_treats_an_unexpected_exit_code_as_inoperable(
    freshness: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A checker that dies with 127 or is OOM-killed must not read as clean."""

    class FakeProc:
        returncode = 127
        stdout = "command not found"
        stderr = ""

    monkeypatch.setattr(freshness.subprocess, "run", lambda *a, **k: FakeProc())
    code, _ = freshness.run_checker(
        {"name": "s", "semantic_coverage": {"checker": ["nope.py", "--check-fresh"]}}
    )
    assert code == INOPERABLE


def test_the_real_coverage_map_runs_and_agrees_with_the_registry(freshness: ModuleType) -> None:
    """End-to-end: every declared checker actually executes, and every surface the
    registry marks `failing` really is clean right now. That pairing is what makes
    `failing` a promise rather than an aspiration."""
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for surface in freshness.field_level_surfaces(registry):
        code, output = freshness.run_checker(surface)
        assert code in (CLEAN, DRIFT), f"{surface['name']} checker is inoperable: {output}"
        if surface["semantic_coverage"]["enforcement"] == "failing":
            assert code == CLEAN, (
                f"{surface['name']} is enforced but drifted — flip it back to report-only with a "
                f"disposition note, or reconcile it:\n{output}"
            )
