#!/usr/bin/env python3
"""P8.2: USE-CASES EXPANSION-ONLY rows align with uc-product-status expansion SSOT."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_use_cases_expansion_sync import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
