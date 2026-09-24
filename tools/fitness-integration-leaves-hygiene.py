#!/usr/bin/env python3
"""integration-leaves.json populated or explicit waive record (F4)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_integration_leaves_hygiene import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
