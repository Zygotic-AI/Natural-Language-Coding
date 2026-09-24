#!/usr/bin/env python3
"""X4 v2: hub tools/ emit-path modules carry BBA boundary markers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_bba_interior_slice import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
