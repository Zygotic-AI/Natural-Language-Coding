#!/usr/bin/env python3
"""Landmine: release infer planning rules."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_release_infer_passes import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
