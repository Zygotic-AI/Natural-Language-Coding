#!/usr/bin/env python3
"""Binder: full-nlc-audit manifest, script, and skill stay wired."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_full_nlc_audit_binder import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
