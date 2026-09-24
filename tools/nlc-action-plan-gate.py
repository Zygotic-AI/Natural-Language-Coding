#!/usr/bin/env python3
"""X1: action-plan gate (NLC-0024-04)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.action_plan_gate import main  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
