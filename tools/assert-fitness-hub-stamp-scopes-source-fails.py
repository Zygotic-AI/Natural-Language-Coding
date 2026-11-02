#!/usr/bin/env python3
"""Landmine: fitness hub stamp scope SSOT missing or unreadable sources fail closed."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_fitness_hub_stamp_scopes_source_fails import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
