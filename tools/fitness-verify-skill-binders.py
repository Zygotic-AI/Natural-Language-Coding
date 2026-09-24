#!/usr/bin/env python3
"""ADR 0021/0010/0023: /verify skill cites gate + rule trace remediation."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_verify_skill_binders import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
