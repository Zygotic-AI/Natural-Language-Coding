#!/usr/bin/env python3
"""ADR 0049: the release planner owns every intentional stop."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_release_planner_ownership import *  # noqa: E402,F403


if __name__ == "__main__":
    raise SystemExit(main())
