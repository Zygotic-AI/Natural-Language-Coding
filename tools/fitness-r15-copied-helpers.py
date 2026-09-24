#!/usr/bin/env python3
"""R15: the same helper must not be copied or imported into two goals."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_r15_copied_helpers import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
