#!/usr/bin/env python3
"""Prove the loaded Planit skill matches the registry."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.planit_identity import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
