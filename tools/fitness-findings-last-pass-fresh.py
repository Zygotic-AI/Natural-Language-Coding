#!/usr/bin/env python3
"""FINDINGS last_pass_sha must match current HEAD short SHA (F2)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_findings_last_pass_fresh import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
