#!/usr/bin/env python3
"""Gate-set byte receipt confirmation (ADR 0051 SG2; completion only)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.gate_change_receipt import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
