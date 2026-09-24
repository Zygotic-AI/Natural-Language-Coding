"""UC9 goal ↔ rule/tag bindings for blast-radius (shared)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.uc9_bindings import *  # noqa: F403
