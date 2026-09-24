"""SSOT: pending ADR status scan (dashboard, verify, CI)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.adr_scan import *  # noqa: F403
