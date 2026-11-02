#!/usr/bin/env python3
"""Hub adapter for deterministic release-prep FINDINGS/DESCRIBE/record writes."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.release_prep_surfaces.release_prep_surfaces import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
