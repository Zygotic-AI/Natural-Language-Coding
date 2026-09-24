#!/usr/bin/env python3
"""C3 / R3 v1: a noun must not call another noun's verb."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c3 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
