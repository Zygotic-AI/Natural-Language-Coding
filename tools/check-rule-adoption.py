#!/usr/bin/env python3
"""UC14 / ADR 0012: adopt-time check for conflicting rules."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.check_rule_adoption import main  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main(hub_root=HUB_ROOT))
