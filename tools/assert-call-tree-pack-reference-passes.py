#!/usr/bin/env python3
"""Landmine UC20: reference TypeScript call-tree pack inventory MET."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_call_tree_pack_reference_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
