#!/usr/bin/env python3
"""Adapter for nouns.gate_stage.gate_stage."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.gate_stage.gate_stage import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
