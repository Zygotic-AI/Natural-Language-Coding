#!/usr/bin/env python3
"""ADR 0036 gate: human surface asks for goal + policy only (default-closed scan)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_0036_inference_only import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
