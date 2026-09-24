#!/usr/bin/env python3
"""ADR 0007/0009: gaps documented — no fake binders claiming MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adr_gap_parked import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
