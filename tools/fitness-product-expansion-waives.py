#!/usr/bin/env python3
"""Waived expansion keys must be empty in uc-product-status."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_product_expansion_waives import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
