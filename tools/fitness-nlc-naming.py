#!/usr/bin/env python3
"""ADR 0011: consumer-facing naming (NLC product, not ACS-as-whole-product)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_naming import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
