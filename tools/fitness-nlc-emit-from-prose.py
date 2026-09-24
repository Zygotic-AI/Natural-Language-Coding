#!/usr/bin/env python3
"""Fitness: nlc-emit-from-prose.py compiles a prose plan end-to-end (ADR 0027)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_emit_from_prose import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
