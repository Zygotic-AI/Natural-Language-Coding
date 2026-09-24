#!/usr/bin/env python3
"""C21 diff-scoped (ADR 0006): impact callers only for CHANGED goal units."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c21_changed import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
