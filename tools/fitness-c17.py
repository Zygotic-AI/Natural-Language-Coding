#!/usr/bin/env python3
"""C17: each verb has success, precondition failure, and adjective preservation."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_c17 import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
