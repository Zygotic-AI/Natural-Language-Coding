#!/usr/bin/env python3
"""Hub landmine adapter for KB-0058-unsigned-tag."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_unsigned_tag_passes.assert_unsigned_tag_passes import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
