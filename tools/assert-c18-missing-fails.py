#!/usr/bin/env python3
"""Known-fail fixture gate for C18 v2 missing goal test."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_c18_missing_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
