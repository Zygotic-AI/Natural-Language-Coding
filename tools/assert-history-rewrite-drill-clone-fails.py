#!/usr/bin/env python3
"""Known-bad: history drill clone stderr and fail-closed preflight."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_history_rewrite_drill_clone_fails import *  # noqa: F403

if __name__ == "__main__":
    sys.exit(main())
