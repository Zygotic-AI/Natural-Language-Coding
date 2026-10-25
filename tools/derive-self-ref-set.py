#!/usr/bin/env python3
"""Adapter for nouns.self_ref_set.self_ref_set."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.self_ref_set.self_ref_set import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
