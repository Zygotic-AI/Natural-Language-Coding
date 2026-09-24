#!/usr/bin/env python3
"""C21 v1: if a proposal/confirm note exists, it must name generated callers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c21 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
