"""Strip markdown links for machine parsers (fitness, landmines) after TERMS linking."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.markdown_plain import *  # noqa: F403
