#!/usr/bin/env python3
"""Landmine ADR 0011: consumer-facing docs MET fitness-nlc-naming."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_nlc_naming_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
