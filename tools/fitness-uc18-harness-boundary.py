#!/usr/bin/env python3
"""UC18 v1 harness doc + hooks.example (P6.4)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_uc18_harness_boundary import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
