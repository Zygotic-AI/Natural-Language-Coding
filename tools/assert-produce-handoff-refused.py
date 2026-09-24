#!/usr/bin/env python3
"""Landmine ADR 0004/0005: produce package without SSOT evidence must handoff_refused."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_produce_handoff_refused import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
