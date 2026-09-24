"""Friendly CLI messages when required arguments are missing (ADR 0018)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.cli_help import *  # noqa: F403
