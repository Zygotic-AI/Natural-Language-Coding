"""Single source for human menu labels (ADR 0017, 0020)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.menu_data import *  # noqa: F403
