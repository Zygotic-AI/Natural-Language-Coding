#!/usr/bin/env python3
"""R21 v1: print callers from code. Do not commit the output.

Scans goals/**/*.py for <name>.<verb>( call sites. Writes JSON to stdout
with a generated marker. Hand-checked-in graphs stay forbidden by
fitness-no-hand-authored-graphs.py.

Input: optional argv root. No args → hub ROOT.
Output: JSON on stdout. Exit 0 always unless the tree cannot be read.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.generate_impact_graph import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
