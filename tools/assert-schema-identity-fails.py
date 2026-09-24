#!/usr/bin/env python3
"""Known-fail fixture gate for R11/C9 v1."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_schema_identity_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
