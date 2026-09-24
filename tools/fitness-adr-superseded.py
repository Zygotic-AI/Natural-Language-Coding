#!/usr/bin/env python3
"""BBP fitness check: superseded ADRs are marked, not deleted (R22)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adr_superseded import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
