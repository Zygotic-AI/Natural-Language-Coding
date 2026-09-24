#!/usr/bin/env python3
"""C16 v1: each adjectives.txt token appears in the noun's tests."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c16 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
