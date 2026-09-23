#!/usr/bin/env python3
"""UC15 beta: inventory non-NLC product paths in an existing repo."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.brownfield_inventory import *  # noqa: F403
__all__ = ['NLC_MARKERS', 'SKIP', 'main']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

