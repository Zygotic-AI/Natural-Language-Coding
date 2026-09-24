#!/usr/bin/env python3
"""Landmine ADR 0016: hub must MET fitness-hub-no-product-requirements."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_hub_no_product_requirements_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
