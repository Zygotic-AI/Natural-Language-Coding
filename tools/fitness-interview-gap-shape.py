#!/usr/bin/env python3
"""ADR 0018: human-facing hub tools use interview-shaped gaps (not NOT_MET-first)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_interview_gap_shape import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
