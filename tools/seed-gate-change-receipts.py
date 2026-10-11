#!/usr/bin/env python3
"""Maintainer: seed integrity/gate-change-receipts.json (ADR 0051 SG2)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.seed_gate_change_receipts import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
