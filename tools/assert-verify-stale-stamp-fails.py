#!/usr/bin/env python3
"""Landmine: product newer than before-generate stamp must fail verify."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_stale_stamp_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
