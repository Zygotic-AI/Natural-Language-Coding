#!/usr/bin/env python3
"""C18: a goal with code has a use-case test that *calls* the goal."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c18 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
