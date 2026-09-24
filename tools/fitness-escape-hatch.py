#!/usr/bin/env python3
"""R33 / C26: reflection, ORM, and SQL escape hatches in goal/adapter trees."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_escape_hatch import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
