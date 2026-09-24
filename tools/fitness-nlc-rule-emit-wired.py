#!/usr/bin/env python3
"""ADR 0023: hub compiler rule-emit wired to CLI, planit, and CI."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_rule_emit_wired import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
