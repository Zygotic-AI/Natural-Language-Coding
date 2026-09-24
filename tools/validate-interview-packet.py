#!/usr/bin/env python3
"""UC1: validate .nlc/interview-packet.json against integrity schema (minimal)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.interview_packet import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
