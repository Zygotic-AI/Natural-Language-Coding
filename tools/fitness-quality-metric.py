#!/usr/bin/env python3
"""BBP fitness check: quality metric validation (Q1-Q5, CS9-CS10)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_quality_metric import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
