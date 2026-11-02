#!/usr/bin/env python3
"""Thin adapter: release-probe changelog-tag-exists fails."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_release_probe_fail_closed import run  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(run("changelog-tag-exists", "fails"))
