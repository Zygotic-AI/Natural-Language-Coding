#!/usr/bin/env python3
"""Landmine: adopter-verify-fast-green has no verify_fast_blockers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_adopter_verify_fast_green_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
