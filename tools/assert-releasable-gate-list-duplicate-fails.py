#!/usr/bin/env python3
"""Landmine: second releasable gate profile home must fail SSOT fitness."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_releasable_gate_list_duplicate_fails import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
