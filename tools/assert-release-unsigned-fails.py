#!/usr/bin/env python3
"""invoice-correct is AI-green and must not RELEASE without Released-by."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_release_unsigned_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
