#!/usr/bin/env python3
"""Known-fail fixture gate for R6/C5 v1 (persistence escapes)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verb_path_violation_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
