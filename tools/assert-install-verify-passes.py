#!/usr/bin/env python3
"""Landmine ADR 0015: hub install hash manifest must MET on checkout."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_install_verify_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
