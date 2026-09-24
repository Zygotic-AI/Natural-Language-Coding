#!/usr/bin/env python3
"""Known-fail: two goals import the same helper."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_r15_import_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
