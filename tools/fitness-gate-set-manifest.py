#!/usr/bin/env python3
"""Hub fitness adapter for fitness_gate_set_manifest."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_gate_set_manifest import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
