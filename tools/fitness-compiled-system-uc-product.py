#!/usr/bin/env python3
"""Product slice: UC tools wired and green specimen commands MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_compiled_system_uc_product import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
