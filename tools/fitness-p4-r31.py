#!/usr/bin/env python3
"""P4 / R31: agent-noun structure AND code-boundary failure modes."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_p4_r31 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
