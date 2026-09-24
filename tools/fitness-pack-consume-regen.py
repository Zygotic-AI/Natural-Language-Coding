#!/usr/bin/env python3
"""hub_v02.pack_consume_regen: install must write pack-consume-status.json when closed."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_pack_consume_regen import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
