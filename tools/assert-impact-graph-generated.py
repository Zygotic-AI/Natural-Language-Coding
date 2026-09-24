#!/usr/bin/env python3
"""Designed pass: invoice-correct produces a generated apply_payment edge."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_impact_graph_generated import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
