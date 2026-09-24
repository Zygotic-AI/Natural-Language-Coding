#!/usr/bin/env python3
"""A11 permanence: CHARTER.md first H1 must open as NLC roof (not BBP-only)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_charter_nlc_door import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
