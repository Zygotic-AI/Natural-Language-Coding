#!/usr/bin/env python3
"""Landmine UC16: non-Python source without language-adapters.json."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_non_python_adapter_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
