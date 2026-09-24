#!/usr/bin/env python3
"""FINDINGS ship/tag prose must match reachable git tags on HEAD (F1)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_findings_shipped_tag_sync import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
