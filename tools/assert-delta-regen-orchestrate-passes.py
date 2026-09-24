#!/usr/bin/env python3
"""Landmine UC9 v2: delta-regen --orchestrate --write-queue emits v2 plan + queue."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_delta_regen_orchestrate_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
