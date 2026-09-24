"""CLI handlers for ./nlc maintainer guide (durable .nlc/ state)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.guide_cmd import *  # noqa: F403
