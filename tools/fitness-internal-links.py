#!/usr/bin/env python3
"""Broken internal markdown link gate (O6)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_internal_links import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
