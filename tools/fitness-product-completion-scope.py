#!/usr/bin/env python3
"""Every uc-product expansion_only key appears in product-completion-scope.json (ADR 0041)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_product_completion_scope import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
