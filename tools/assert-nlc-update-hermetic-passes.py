#!/usr/bin/env python3
"""Landmine ADR 0014/0015: hermetic store upgrade 0.1.0 → 0.1.1 via nlc-update."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_nlc_update_hermetic_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
