#!/usr/bin/env python3
"""Landmine: synthetic TODO/product SSOT mismatch must be detected."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_todo_use_cases_ssot_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
