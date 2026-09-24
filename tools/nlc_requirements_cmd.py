"""Agent/CI requirements sync (ADR 0019–0020). Humans use /interview."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.requirements_cmd import *  # noqa: F403
