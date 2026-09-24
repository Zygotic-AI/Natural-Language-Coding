#!/usr/bin/env python3
"""P5.6 x4-t2-assert-batch-a: inventory + assert noun pilot progress (default-closed)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_x4_tranche_t2 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
