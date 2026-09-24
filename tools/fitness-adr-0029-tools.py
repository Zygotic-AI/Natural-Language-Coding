#!/usr/bin/env python3
"""Fitness: ADR 0029 lineage check + bind snapshot round-trip + freshness."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adr_0029_tools import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
