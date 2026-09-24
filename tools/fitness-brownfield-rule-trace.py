#!/usr/bin/env python3
"""ADR 0023 / UC15: brownfield inventory points at rule-trace + goal-scaffold."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_brownfield_rule_trace import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
