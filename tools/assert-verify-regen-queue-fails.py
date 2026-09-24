#!/usr/bin/env python3
"""Landmine: open delta-regen queue must fail ./nlc verify (ADR 0006 loud prove)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_regen_queue_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
