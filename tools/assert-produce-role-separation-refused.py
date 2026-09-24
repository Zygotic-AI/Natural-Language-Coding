#!/usr/bin/env python3
"""Landmine ADR 0003: produce package cannot self-audit (same producer and auditor role)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_produce_role_separation_refused import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
