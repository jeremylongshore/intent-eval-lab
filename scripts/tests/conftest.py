"""Pytest fixtures for the top-level scripts/ unit tests.

The scripts in scripts/ are named with hyphens (e.g. sak-state-machine.py) so
they are not importable as modules by name. This conftest loads the module
under test by file path via importlib and exposes it as a session fixture.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def _load_by_path(filename: str, module_name: str) -> ModuleType:
    path = SCRIPTS_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:  # pragma: no cover - import guard
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    # Register before exec_module so dataclass machinery (which resolves
    # cls.__module__ via sys.modules) can find the module while it executes.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def ssm() -> ModuleType:
    """The sak-state-machine module (loaded by path)."""
    return _load_by_path("sak-state-machine.py", "sak_state_machine")


@pytest.fixture(scope="session")
def gate_revert() -> ModuleType:
    """The sak-kernel-gate-revert module (loaded by path)."""
    return _load_by_path("sak-kernel-gate-revert.py", "sak_kernel_gate_revert")


@pytest.fixture(scope="session")
def srq() -> ModuleType:
    """The sak-reconciliation-queue module (loaded by path)."""
    return _load_by_path("sak-reconciliation-queue.py", "sak_reconciliation_queue")


@pytest.fixture(scope="session")
def wb() -> ModuleType:
    """The sak-wave-b-durability module (loaded by path)."""
    return _load_by_path("sak-wave-b-durability.py", "sak_wave_b_durability")


@pytest.fixture(scope="session")
def spd() -> ModuleType:
    """The spec-projection-diff module — Fitness Function #2 (loaded by path)."""
    return _load_by_path("spec-projection-diff.py", "spec_projection_diff")


# The four deep-capture extractors that carry --check-fresh. Loaded by path for the
# same reason as the others (hyphenated filenames); each puts scripts/ on sys.path
# itself so `from lib import captured_source` resolves under pytest too.


@pytest.fixture(scope="session")
def extractors() -> dict[str, ModuleType]:
    """contract -> extractor module, for the four contracts with a captured surface."""
    return {
        contract: _load_by_path(
            f"extract-{contract}-projection.py", f"extract_{contract.replace('-', '_')}_projection"
        )
        for contract in ("agent-definition", "hook-config", "marketplace-catalog", "plugin-manifest")
    }


@pytest.fixture(scope="session")
def captured_source(extractors: dict[str, ModuleType]) -> ModuleType:
    """The shared captured-snapshot resolver (scripts/lib/captured_source.py).

    Deliberately reached THROUGH an extractor rather than loaded by path again:
    a second load would be a distinct module object, so monkeypatching it would
    not affect the copy the extractors actually call.
    """
    return extractors["hook-config"].captured_source


@pytest.fixture(scope="session")
def freshness() -> ModuleType:
    """The projection-freshness driver (loaded by path)."""
    return _load_by_path("projection-freshness.py", "projection_freshness")
