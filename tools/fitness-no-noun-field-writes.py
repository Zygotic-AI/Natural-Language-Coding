#!/usr/bin/env python3
"""Fitness check 1: no noun field writes from outside the noun (charter §12.1)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_no_noun_field_writes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
