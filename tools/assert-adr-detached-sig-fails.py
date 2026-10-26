#!/usr/bin/env python3
"""Hub landmine adapter for assert_adr_detached_sig_fails."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_adr_detached_sig_fails.assert_adr_detached_sig_fails import main


if __name__ == "__main__":
    raise SystemExit(main())
