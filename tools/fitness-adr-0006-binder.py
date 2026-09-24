#!/usr/bin/env python3
"""ADR 0006: contract-change fitness + landmines wired in CI."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adr_0006_binder import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
