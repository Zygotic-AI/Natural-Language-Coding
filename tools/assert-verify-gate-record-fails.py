#!/usr/bin/env python3
"""Landmine: app tree with goals/implementation.py must fail verify without gate records."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_gate_record_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
