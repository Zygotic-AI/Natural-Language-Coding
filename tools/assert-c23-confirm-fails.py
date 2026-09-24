#!/usr/bin/env python3
"""Known-fail: confirmer Cx — FAIL with no rebuttal."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_c23_confirm_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
