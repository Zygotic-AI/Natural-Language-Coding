#!/usr/bin/env python3
"""R17 v1: workflows/ may host a goal; it may not *be* a goal."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_r17_workflow_citizen import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
