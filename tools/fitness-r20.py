#!/usr/bin/env python3
"""R20: verbs.schema.json required fields are named and typed in the verb."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_r20 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
