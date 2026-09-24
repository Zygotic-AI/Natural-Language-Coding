#!/usr/bin/env python3
"""Landmine ADR 0015: nlc-init writes a valid .nlc/lock.json."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_project_lock_schema_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
