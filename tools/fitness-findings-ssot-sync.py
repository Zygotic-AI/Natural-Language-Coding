#!/usr/bin/env python3
"""Umbrella: FINDINGS vs tags + ADR-ENFORCEMENT table (F1 + F3)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_findings_ssot_sync import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
