#!/usr/bin/env python3
"""R9/R10/C7/C8 v2: public entrypoints have schema files."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_contract_presence import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
