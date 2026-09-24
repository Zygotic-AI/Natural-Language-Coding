#!/usr/bin/env python3
"""ADR 0013: hub nlc*.py CLIs call hub_tool() before work."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_requirements_hub_entrypoints import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
