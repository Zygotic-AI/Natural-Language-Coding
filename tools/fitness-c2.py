#!/usr/bin/env python3
"""C2 v1: adjectives.txt / fields.txt do not live under goals/."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c2 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
