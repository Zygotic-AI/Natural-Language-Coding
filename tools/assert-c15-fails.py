#!/usr/bin/env python3
"""Known-fail fixture gate for C15 missing idempotent flag."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_c15_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
