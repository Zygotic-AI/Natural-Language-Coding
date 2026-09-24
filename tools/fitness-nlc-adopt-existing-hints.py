#!/usr/bin/env python3
"""ADR 0023/UC15: ./nlc adopt-existing points at goal-scaffold + RULE-TRACE."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_adopt_existing_hints import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
