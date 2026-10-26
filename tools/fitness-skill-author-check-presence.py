#!/usr/bin/env python3
"""Hub install still invokes the skill-author checklist use-case."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_skill_author_check_presence import *  # noqa: F403

if __name__ == "__main__":
    sys.exit(main())
