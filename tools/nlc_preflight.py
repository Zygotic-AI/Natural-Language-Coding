"""Install / hub preflight for human ./nlc (ADR 0017–0018)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.preflight import *  # noqa: F403
