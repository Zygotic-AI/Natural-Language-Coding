#!/usr/bin/env python3
"""Known-fail: version 1 dropped a required field, no ADR."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_c10_breaking_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
