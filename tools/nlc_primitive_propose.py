#!/usr/bin/env python3
"""UC12: governed primitive expansion — draft ADR before integrity/primitives.md edit."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.primitive_propose import *  # noqa: F403
__all__ = ['ROOT', 'main', 'next_adr_number', 'render_adr']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

