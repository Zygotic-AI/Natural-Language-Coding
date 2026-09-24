#!/usr/bin/env python3
"""C15: retrying goals call an idempotent verb that *honors* a key."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c15_idempotent import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
