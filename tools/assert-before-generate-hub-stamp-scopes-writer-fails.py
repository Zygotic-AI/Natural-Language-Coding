#!/usr/bin/env python3
"""Landmine: hub before-generate writer refuses partial scope lists."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_before_generate_hub_stamp_scopes_writer_fails import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
