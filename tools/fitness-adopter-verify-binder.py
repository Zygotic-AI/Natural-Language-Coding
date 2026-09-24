#!/usr/bin/env python3
"""ADR 0021/0023: adopter verify-fast green specimen + landmine in CI."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adopter_verify_binder import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
