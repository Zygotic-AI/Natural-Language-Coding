#!/usr/bin/env python3
"""Thin entry for the pull-request offer gate."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.pr_offer_gate import main

if __name__ == "__main__":
    sys.exit(main())
