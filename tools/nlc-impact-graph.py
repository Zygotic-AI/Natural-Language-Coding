#!/usr/bin/env python3
"""Emit or persist the R21 impact graph for an adopter repo."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.impact_graph import *  # noqa: F403
__all__ = ['ROOT', '_build', 'main']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

