#!/usr/bin/env python3
"""R32: tainted values do not leave the consuming unit."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_taint_lifetime import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
