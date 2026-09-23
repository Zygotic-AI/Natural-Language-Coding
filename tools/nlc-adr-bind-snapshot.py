#!/usr/bin/env python3
"""ADR 0029: snapshot ACTIVE set at bind time for reproducibility."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.adr_bind_snapshot import *  # noqa: F403
__all__ = ['ROOT', 'main']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

