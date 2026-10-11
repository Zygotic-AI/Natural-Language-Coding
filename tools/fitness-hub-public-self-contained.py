#!/usr/bin/env python3
"""O6: hub in-force surfaces must be self-contained."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_public_self_contained import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
