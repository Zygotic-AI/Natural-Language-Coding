#!/usr/bin/env python3
"""Thin adapter for fitness-landmine-self-contained."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_landmine_self_contained import *  # noqa: F403

if __name__ == "__main__":
    sys.exit(main())
