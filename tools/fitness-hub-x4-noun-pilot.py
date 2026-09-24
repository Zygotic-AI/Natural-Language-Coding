#!/usr/bin/env python3
"""X4 noun pilots: every tools/nouns/<slug>/ package has shape + CLI adapter import."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_x4_noun_pilot import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
