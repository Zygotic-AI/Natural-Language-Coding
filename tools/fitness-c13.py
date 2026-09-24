#!/usr/bin/env python3
"""C13 / R16 v1: a one-verb goal with no I/O schemas is a wrapper, not a goal."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c13 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
