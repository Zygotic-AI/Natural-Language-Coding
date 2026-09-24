#!/usr/bin/env python3
"""Landmine UC1: verify_fast_blockers refuse missing interview-packet."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_interview_packet_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
