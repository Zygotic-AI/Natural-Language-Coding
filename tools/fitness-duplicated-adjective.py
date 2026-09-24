#!/usr/bin/env python3
"""C19 v1: the same adjective is implemented in two files of one noun."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_duplicated_adjective import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
