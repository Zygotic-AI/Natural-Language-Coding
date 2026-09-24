#!/usr/bin/env python3
"""UC16 reference adapter fixture + pass landmine (P3)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_uc16_reference_adapter import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
