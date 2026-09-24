#!/usr/bin/env python3
"""Human command surface for Natural Language Coding (ADR 0017)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.nlc_hub_cli import main  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
