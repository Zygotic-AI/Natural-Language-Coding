#!/usr/bin/env python3
"""Hub adapter: release surfaces must not tell a human to sign (ADR 0058)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_sign_stop.fitness_sign_stop import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
