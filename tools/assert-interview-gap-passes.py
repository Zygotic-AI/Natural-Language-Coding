#!/usr/bin/env python3
"""Landmine ADR 0018: ./nlc human gaps are interview-shaped, not NOT_MET-first."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_interview_gap_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
