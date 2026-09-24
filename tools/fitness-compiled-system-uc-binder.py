#!/usr/bin/env python3
"""Binder: Build a compiled system — UC dependency tools wired in hub CI."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_compiled_system_uc_binder import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
