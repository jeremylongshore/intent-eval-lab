"""Shared pytest fixtures for Phase A.0 runner tests."""

from __future__ import annotations

import sys
from pathlib import Path

# Make `_arm_common` importable from sibling scripts/
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
