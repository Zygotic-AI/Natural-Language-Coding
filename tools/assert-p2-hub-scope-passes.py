#!/usr/bin/env python3
"""Landmine ADR 0002: P2 hub scope fitness MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_p2_hub_scope_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
