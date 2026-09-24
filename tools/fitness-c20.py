#!/usr/bin/env python3
"""C20: R23 field-writes AND R24 adjective-locality both MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c20 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
