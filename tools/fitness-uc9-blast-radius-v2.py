#!/usr/bin/env python3
"""UC9 v2 rule-tagged blast radius product boundary (P6.1)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_uc9_blast_radius_v2 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
