"""ADR 0006: loud prove for breaking published contract changes."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.contract_change import *  # noqa: F403
