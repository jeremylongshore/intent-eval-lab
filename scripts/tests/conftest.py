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
