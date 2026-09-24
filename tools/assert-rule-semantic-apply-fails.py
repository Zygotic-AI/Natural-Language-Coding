#!/usr/bin/env python3
"""Landmine UC5 v2: semantic apply NOT_MET when obligation receipt missing."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_rule_semantic_apply_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
