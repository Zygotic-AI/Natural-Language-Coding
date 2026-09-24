#!/usr/bin/env python3
"""Fitness: nlc-action-gates.py exists and refuses empty input (default-closed)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_action_gates import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
