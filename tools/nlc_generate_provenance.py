#!/usr/bin/env python3
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.generate_provenance import *  # noqa: F403
__all__ = ['PROVENANCE_FILE', '_utc_now', 'provenance_for', 'record_generate']

