#!/usr/bin/env python3
"""ADR 0008: planit generate step cites noun-inheritance fitness."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_planit_noun_shape import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
