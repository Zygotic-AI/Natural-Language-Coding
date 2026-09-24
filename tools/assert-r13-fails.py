#!/usr/bin/env python3
"""Known-fail fixture gate for R13 v1 (one entrypoint per goal)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_r13_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
