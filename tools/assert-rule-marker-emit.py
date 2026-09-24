#!/usr/bin/env python3
"""Landmine: nlc_rule_marker.py emits stable ADR 0023 lines."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_rule_marker_emit import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
