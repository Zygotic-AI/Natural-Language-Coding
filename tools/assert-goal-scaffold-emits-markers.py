#!/usr/bin/env python3
"""Landmine ADR 0023: goal-scaffold emits nlc:rule= lines for adopted rules."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_goal_scaffold_emits_markers import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
