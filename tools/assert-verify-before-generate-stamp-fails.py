#!/usr/bin/env python3
"""Landmine: product without before-generate stamp must fail verify (UC18 / ADR 0010)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_before_generate_stamp_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
