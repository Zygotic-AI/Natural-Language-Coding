#!/usr/bin/env python3
"""R24 v1: named adjectives and field math stay under domain/<noun>/."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adjective_locality import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
