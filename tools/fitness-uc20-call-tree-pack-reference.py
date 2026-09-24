#!/usr/bin/env python3
"""UC20 reference TypeScript call-tree pack (P4)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_uc20_call_tree_pack_reference import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
