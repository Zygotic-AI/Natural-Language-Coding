#!/usr/bin/env python3
"""UC4 v2 semantic rule runner product boundary (P2 / ADR 0007)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_uc4_semantic_rule_runner_v2 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
