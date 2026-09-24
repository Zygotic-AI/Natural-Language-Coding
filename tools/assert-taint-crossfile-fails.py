#!/usr/bin/env python3
"""Known-fail: taint returned through a helper in another file."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_taint_crossfile_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
