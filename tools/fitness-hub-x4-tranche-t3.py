#!/usr/bin/env python3
"""P5.7 x4-t3-assert-batch-b: all assert landmines noun-backed (default-closed)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_x4_tranche_t3 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
