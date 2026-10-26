#!/usr/bin/env python3
"""Hub landmine adapter for assert_sign_adrs_script_passes."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_sign_adrs_script_passes.assert_sign_adrs_script_passes import main


if __name__ == "__main__":
    raise SystemExit(main())
