#!/usr/bin/env python3
"""JOBS-TO-BE-DONE Blocked/Available vs uc-product-status + TODO."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_jobs_todo_sync import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
