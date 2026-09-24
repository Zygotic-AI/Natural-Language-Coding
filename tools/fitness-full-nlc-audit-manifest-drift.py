#!/usr/bin/env python3
"""Operator docs must not duplicate full-nlc-audit manifest stage inventories (ADR 0038)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_full_nlc_audit_manifest_drift import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
