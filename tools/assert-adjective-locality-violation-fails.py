#!/usr/bin/env python3
"""Known-fail fixture gate for R24 v1 (adjective locality)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_adjective_locality_violation_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
