#!/usr/bin/env python3
"""Hub adapter for check_inputs snapshot write/check."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.check_inputs.check_inputs import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
