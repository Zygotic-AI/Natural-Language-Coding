#!/usr/bin/env python3
"""Landmine ADR 0006: diff-scoped C21 MET when missing caller is outside CHANGED."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_c21_changed_scoped_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
