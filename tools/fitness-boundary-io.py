#!/usr/bin/env python3
"""P4 / R31 v1 for code boundaries: failure mode declared."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_boundary_io import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
