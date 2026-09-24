#!/usr/bin/env python3
"""ADR 0016: hub must not ship product requirement packs as repo SSOT."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_hub_no_product_requirements import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
