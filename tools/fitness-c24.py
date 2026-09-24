#!/usr/bin/env python3
"""C24: classes A/B/D/E/F need Ratified-by: a human, not the agent."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c24 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
