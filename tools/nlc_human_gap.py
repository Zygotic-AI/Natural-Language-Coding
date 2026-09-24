"""ADR 0018 interview-shaped CLI gaps (human stderr; optional machine line last)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.human_gap import *  # noqa: F403
