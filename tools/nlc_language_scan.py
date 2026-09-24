#!/usr/bin/env python3
"""UC16 v0: list implementation languages under domain/ and goals/."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.language_scan import *  # noqa: F403

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
