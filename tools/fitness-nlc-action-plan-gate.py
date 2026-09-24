#!/usr/bin/env python3
"""Fitness: X1 action-plan gate — ok specimen MET, bad specimen stays red."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_action_plan_gate import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
