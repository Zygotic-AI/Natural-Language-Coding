#!/usr/bin/env python3
"""Landmine ADR 0017–0020: human-surface binder fitness MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_human_surface_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
