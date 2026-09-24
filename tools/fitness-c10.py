#!/usr/bin/env python3
"""C10: a breaking schema change needs an ADR, even at version 1."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c10 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
