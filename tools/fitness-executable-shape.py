#!/usr/bin/env python3
"""Classify every executable file into one shape."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.executable_shape import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
