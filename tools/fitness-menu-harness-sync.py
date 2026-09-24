#!/usr/bin/env python3
"""ADR 0017/0020: human menu SSOT matches docs/nlc/MENU.md."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_menu_harness_sync import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
