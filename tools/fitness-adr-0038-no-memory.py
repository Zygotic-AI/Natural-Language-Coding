#!/usr/bin/env python3
"""ADR 0038 v1: operator SSOT must not rely on 'remember' without a linked gate or TODO."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adr_0038_no_memory import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
