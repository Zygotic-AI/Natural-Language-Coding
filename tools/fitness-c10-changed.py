#!/usr/bin/env python3
"""C10 diff-scoped (ADR 0006): breaking schema / version≠1 only in CHANGED units."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c10_changed import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
