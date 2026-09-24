#!/usr/bin/env python3
"""R18 v1: retry/compensation orchestration does not live inside the noun."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_r18_noun_retries import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
