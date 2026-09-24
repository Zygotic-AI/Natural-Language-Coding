#!/usr/bin/env python3
"""Git semver tags for hub release (shipped baseline). Not integrity/nlc-version.json."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.release_tags import *  # noqa: F403
