#!/usr/bin/env python3
"""Landmine ADR 0015: release smoke (local store + init + install-verify)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_release_smoke_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
