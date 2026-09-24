#!/usr/bin/env python3
"""Known-fail fixture gate for P4/R31 v1 (code boundaries)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_boundary_io_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
