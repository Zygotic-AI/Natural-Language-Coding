#!/usr/bin/env python3
"""BBP fitness check: stand-alone branding, no foreign brand imports (P1)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_branding import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
