#!/usr/bin/env python3
"""ADR 0023: planit generate step prescribes goal-scaffold + rule-marker emit."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_planit_generate_markers import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
