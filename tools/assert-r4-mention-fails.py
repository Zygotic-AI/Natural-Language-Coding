#!/usr/bin/env python3
"""Known-fail: verb mentions fields in a string, never reads/writes them."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_r4_mention_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
