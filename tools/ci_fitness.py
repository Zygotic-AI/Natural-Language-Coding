#!/usr/bin/env python3
"""Hub compile fitness suite (cross-platform).

Same sequence as legacy ci-fitness.sh. Use on Windows without bash:

  python tools/ci_fitness.py

From repo root. Exit 0 = CI:MET, 1 = CI:FAIL.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.ci_fitness import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
