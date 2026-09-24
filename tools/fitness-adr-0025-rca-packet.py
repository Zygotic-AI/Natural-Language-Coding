#!/usr/bin/env python3
"""ADR 0025 expansion: RCA packet schema + validator wired."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_adr_0025_rca_packet import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
