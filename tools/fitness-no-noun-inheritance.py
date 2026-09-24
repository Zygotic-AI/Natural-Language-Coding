#!/usr/bin/env python3
"""ADR 0008 v1: nouns must not inherit other nouns (domain/ class bases)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_no_noun_inheritance import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
