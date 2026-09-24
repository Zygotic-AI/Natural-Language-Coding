#!/usr/bin/env python3
"""ADR 0041: hub pack registry v1 wired + uc-product pack_registry closed."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_pack_registry import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
