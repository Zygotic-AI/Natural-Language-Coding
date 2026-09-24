#!/usr/bin/env python3
"""BBP fitness check: goal modules must not import other goals' internals (C12, R14)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_goal_imports import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
