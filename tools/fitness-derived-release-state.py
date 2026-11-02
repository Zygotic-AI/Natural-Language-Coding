#!/usr/bin/env python3
"""Hub fitness adapter for the one derived-release-state check."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_derived_release_state.fitness_derived_release_state import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
