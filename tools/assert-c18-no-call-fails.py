#!/usr/bin/env python3
"""Known-fail: goal tests never call the goal."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_c18_no_call_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
