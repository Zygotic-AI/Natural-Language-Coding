#!/usr/bin/env python3
"""Run one releasable gate or profile (RCA-1). Prefer: ./nlc gate …"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.releasable_gates.releasable_gates import main

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
