#!/usr/bin/env python3
"""Adapter for nouns.mandated_paths.mandated_paths."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.mandated_paths.mandated_paths import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
