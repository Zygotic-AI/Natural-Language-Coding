#!/usr/bin/env python3
"""Landmine: verify-deep extra blockers refuse incomplete produce package."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_deep_produce_refused import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
