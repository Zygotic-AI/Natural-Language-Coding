#!/usr/bin/env python3
"""Landmine: skill-author checklist must NOT_MET on the broken fixture."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_skill_author_check_fails import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
