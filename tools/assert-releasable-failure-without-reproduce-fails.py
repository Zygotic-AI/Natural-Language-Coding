#!/usr/bin/env python3
"""Landmine: gate failures must include a Reproduce command."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_releasable_failure_without_reproduce_fails import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
