#!/usr/bin/env python3
"""UC13 v2 engine.runtime tag strict product boundary (P6.2)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_uc13_engine_runtime_strict import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
