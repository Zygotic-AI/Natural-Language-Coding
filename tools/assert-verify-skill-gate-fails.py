#!/usr/bin/env python3
"""Landmine: gate-scoped SKILL.md must fail verify without gate-record (ADR 0010)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_verify_skill_gate_fails import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
