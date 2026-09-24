#!/usr/bin/env python3
"""full-nlc-audit skill must document when to write integration-leaves (F4 guidance)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_full_nlc_audit_skill_leaves_section import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
