#!/usr/bin/env python3
"""BBP fitness check: noun modules must not import goal/workflow modules (C6, R7)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_noun_imports import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
