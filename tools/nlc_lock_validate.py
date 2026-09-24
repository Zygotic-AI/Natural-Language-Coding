"""ADR 0015: compiled-system .nlc/lock.json shape."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.lock_validate import *  # noqa: F403
