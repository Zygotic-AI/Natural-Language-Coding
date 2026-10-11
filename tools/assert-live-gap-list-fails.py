#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_live_gap_list_fails.assert_live_gap_list_fails import main


if __name__ == "__main__":
    sys.exit(main())
