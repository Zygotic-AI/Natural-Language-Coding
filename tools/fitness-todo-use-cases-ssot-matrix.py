#!/usr/bin/env python3
"""Matrix tests for nlc_todo_ssot (negative + positive scenarios)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_todo_use_cases_ssot_matrix import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
