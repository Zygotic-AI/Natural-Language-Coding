#!/usr/bin/env python3
"""Hub adapter for derive_adr_0051_0052_rules."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.derive_adr_0051_0052_rules import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
