#!/usr/bin/env python3
"""C23 v2: open findings in FINDINGS.md *or* confirmer FAIL lines."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c23 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
