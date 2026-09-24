#!/usr/bin/env python3
"""Landmine ADR 0014: hub version must sit on a complete migration catalog."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_migration_catalog_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
