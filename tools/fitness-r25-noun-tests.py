#!/usr/bin/env python3
"""R25 v1: a noun with declared fields/adjectives has tests next to it."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_r25_noun_tests import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
