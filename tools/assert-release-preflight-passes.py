#!/usr/bin/env python3
"""Landmine ADR 0014/0022: hub release preflight --check MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_release_preflight_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
