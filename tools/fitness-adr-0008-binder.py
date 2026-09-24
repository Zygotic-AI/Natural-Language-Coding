#!/usr/bin/env python3
"""ADR 0008: noun-inheritance scan + landmine + planit/reviewer cite."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adr_0008_binder import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
