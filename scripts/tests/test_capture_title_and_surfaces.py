"""Regression tests for the two holes that let a replaced page read as healthy.

1. `expect_title` — every surface's `expect_regex` is effectively "any heading",
   so a page upstream REPLACES wholesale still classifies FETCH_OK and still
   gets promoted as the last-good snapshot. That is what happened to
   slash-commands.md: it was replaced by a document titled "Extend Claude with
   skills" and nothing anywhere went red.

2. registered-surface linkage — a vendored file with a spec-bearing role that
   names no surface is a normative input nothing re-fetches, diffs, or notices
   changing. claude-code-mcp.md has been in exactly that state.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    # Registered before exec so dataclass field resolution can find the module.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fc = _load("fetch_capture_under_test", "fetch-capture.py")
integrity = _load("vendor_meta_under_test", "check-vendor-meta-integrity.py")

_BODY = "# Extend Claude with skills\n\n## Frontmatter reference\n\n" + ("filler line\n" * 500)


def _raw(body: str, url: str = "https://code.claude.com/docs/en/slash-commands.md"):
    return fc.RawFetch(requested_url=url, http_code=200, body=body.encode(), error=None, redirects=[])


def _capture(**overrides) -> dict:
    base = {"kind": "http", "urls": [], "expect_regex": r"(?m)^#{1,3} ", "min_bytes": 128, "ext": ".md"}
    base.update(overrides)
    return base


# ── expect_title ────────────────────────────────────────────────────────────


def test_matching_title_is_fetch_ok():
    cap = _capture(expect_title=r"(?i)^Extend Claude with skills$")
    assert fc.classify_fetch(_raw(_BODY), cap) == fc.FETCH_OK


def test_replaced_page_is_shape_changed():
    """The real case: the registry expects the old title, upstream served a new page."""
    cap = _capture(expect_title=r"(?i)^Slash commands$")
    assert fc.classify_fetch(_raw(_BODY), cap) == fc.SHAPE_CHANGED


def test_without_expect_title_a_replaced_page_still_reads_healthy():
    """Pins the hole itself, so removing expect_title cannot go unnoticed."""
    assert fc.classify_fetch(_raw(_BODY), _capture()) == fc.FETCH_OK


def test_missing_h1_with_expect_title_is_shape_changed():
    body = "## Only a subheading\n\n" + ("filler line\n" * 500)
    cap = _capture(expect_title=r"(?i)^Anything$")
    assert fc.classify_fetch(_raw(body), cap) == fc.SHAPE_CHANGED


def test_expect_title_does_not_override_earlier_taxonomy_rules():
    """First rule wins: a 404 stays MOVED even when the title would mismatch."""
    raw = fc.RawFetch(
        requested_url="https://example.invalid/x.md", http_code=404, body=b"", error=None, redirects=[]
    )
    assert fc.classify_fetch(raw, _capture(expect_title=r"^Nope$")) == fc.MOVED


def test_every_registered_expect_title_compiles_and_matches_its_snapshot():
    """Guards against a title pattern that can never match the captured page."""
    import re

    registry = json.loads((REPO_ROOT / "specs" / "upstream-surface-registry.v1.json").read_text())
    checked = 0
    for surface in registry["surfaces"]:
        pattern = (surface.get("capture") or {}).get("expect_title")
        if not pattern:
            continue
        re.compile(pattern)  # must not raise
        snapshot = REPO_ROOT / "specs" / "_vendor" / surface["name"] / f"snapshot{surface['capture']['ext']}"
        if not snapshot.exists():
            continue
        h1 = next((l for l in snapshot.read_text(errors="replace").splitlines() if l.startswith("# ")), None)
        assert h1 is not None, f"{surface['name']}: expect_title set but snapshot has no H1"
        assert re.search(pattern, h1[2:].strip()), f"{surface['name']}: expect_title never matches its own snapshot"
        checked += 1
    assert checked >= 8, f"expected to check the markdown surfaces, only checked {checked}"


# ── registered-surface linkage ──────────────────────────────────────────────


def test_spec_bearing_input_without_a_surface_is_reported(tmp_path):
    meta = {
        "contract": "demo",
        "spec_version": "v1",
        "files": [{"file": "doc.md", "role": "claude-code-doc", "source_url": "https://example.test/doc.md"}],
    }
    (tmp_path / "vendor-meta.json").write_text(json.dumps(meta))
    found: list[str] = []
    integrity.check_registered_surfaces(str(tmp_path), found, {"some-surface"})
    assert len(found) == 1, found
    assert "declares NO surface" in found[0]


def test_sample_roles_are_exempt(tmp_path):
    """Samples are commit-pinned corroboration; monitoring them is meaningless."""
    meta = {
        "contract": "demo",
        "spec_version": "v1",
        "files": [{"file": "s.json", "role": "sample-manifest", "source_url": "https://example.test/s.json"}],
    }
    (tmp_path / "vendor-meta.json").write_text(json.dumps(meta))
    found: list[str] = []
    integrity.check_registered_surfaces(str(tmp_path), found, {"some-surface"})
    assert found == []


def test_unknown_surface_name_is_reported(tmp_path):
    meta = {
        "contract": "demo",
        "spec_version": "v1",
        "files": [{"file": "d.md", "role": "reference-doc", "surface": "ghost", "source_url": "https://x.test/d"}],
    }
    (tmp_path / "vendor-meta.json").write_text(json.dumps(meta))
    found: list[str] = []
    integrity.check_registered_surfaces(str(tmp_path), found, {"real-surface"})
    assert len(found) == 1 and "ghost" in found[0], found


def test_known_surface_is_clean(tmp_path):
    meta = {
        "contract": "demo",
        "spec_version": "v1",
        "files": [{"file": "d.md", "role": "reference-doc", "surface": "real", "source_url": "https://x.test/d"}],
    }
    (tmp_path / "vendor-meta.json").write_text(json.dumps(meta))
    found: list[str] = []
    integrity.check_registered_surfaces(str(tmp_path), found, {"real"})
    assert found == []
