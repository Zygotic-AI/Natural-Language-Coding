#!/usr/bin/env python3
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.plan_audit import *  # noqa: F403
__all__ = ['_validate_q2', 'install_audit', 'main']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

