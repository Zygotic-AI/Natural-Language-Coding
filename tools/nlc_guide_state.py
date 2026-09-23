#!/usr/bin/env python3
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.guide_state import *  # noqa: F403
__all__ = ['_nlc', '_write_json', 'before_generate_ok', 'before_generate_stamp_valid', 'end_planit', 'handoff_build', 'policy_change', 'requirements_dirty', 'start_planit']

