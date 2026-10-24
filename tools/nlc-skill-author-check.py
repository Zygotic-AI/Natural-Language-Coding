#!/usr/bin/env python3
"""Same skill-author checklist for pre-release and post-install."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.skill_author_check import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
