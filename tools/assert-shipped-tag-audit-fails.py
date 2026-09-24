#!/usr/bin/env python3
"""Landmine ADR 0040: shipped tag audit refuses unprepared v0.2.0 merge."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_shipped_tag_audit_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
