#!/usr/bin/env python3
"""Landmine ADR 0003: verify-deep extra refuses self-audit produce package."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_deep_role_separation_refused import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
