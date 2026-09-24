#!/usr/bin/env python3
"""Fitness: nlc-pipeline-wire.py sequences X1→X6 on the ok specimen (ADR 0030)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_pipeline_wire import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
