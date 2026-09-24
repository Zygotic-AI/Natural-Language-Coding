#!/usr/bin/env python3
"""Landmine UC15/0023: brownfield inventory runs and hints goal-scaffold."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_brownfield_inventory_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
