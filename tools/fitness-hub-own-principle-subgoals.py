#!/usr/bin/env python3
"""Hub material property leaf goals (ADR 0051 SG1)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_own_principle_subgoals import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
