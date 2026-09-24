#!/usr/bin/env python3
"""BBP fitness check: no hand-authored dependency/execution graphs (R19, R21)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_no_hand_authored_graphs import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
