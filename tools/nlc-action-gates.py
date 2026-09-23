#!/usr/bin/env python3
"""X6: run the default-closed gates of ADRs bound to an action (ADR 0024 / 0030).

Input: JSON list of {"adr_id", "gate_cmd", "args": [...]}.
Each gate_cmd is executed; non-zero exit or RESULT:NOT_MET fails the stage.
Default-closed: an empty list fails (no bound gates means nothing was bound).
"""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.action_gates import *  # noqa: F403
__all__ = ['main']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

