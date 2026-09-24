#!/usr/bin/env python3
"""ADR 0010/0023: HARNESS.md lists gate + rule trace maintainer commands."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_harness_gate_binder_sync import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
