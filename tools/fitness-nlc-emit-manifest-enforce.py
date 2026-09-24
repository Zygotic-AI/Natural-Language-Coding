#!/usr/bin/env python3
"""Fitness: X3 full emit-manifest enforcement — ok MET, bad stays red."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_nlc_emit_manifest_enforce import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
