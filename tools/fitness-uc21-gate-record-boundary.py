#!/usr/bin/env python3
"""UC21 v1 gate-record + scope harness (P6.5)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_uc21_gate_record_boundary import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
