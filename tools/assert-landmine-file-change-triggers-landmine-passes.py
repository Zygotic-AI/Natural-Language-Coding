#!/usr/bin/env python3
"""Hub landmine adapter for assert_landmine_file_change_triggers_landmine_passes."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_landmine_file_change_triggers_landmine_passes import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
