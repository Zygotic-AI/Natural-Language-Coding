#!/usr/bin/env python3
"""ADR-ENFORCEMENT gap rows must not contradict FINDINGS done/bound (F3)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adr_enforcement_table_sync import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
