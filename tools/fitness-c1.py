#!/usr/bin/env python3
"""C1: product trees have a note; class letter matches the change set."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c1 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
