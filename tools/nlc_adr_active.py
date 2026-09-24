"""Shared ACTIVE.md parsing + hash for ADR 0029 tools."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.adr_active import *  # noqa: F403
