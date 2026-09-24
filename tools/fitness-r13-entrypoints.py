#!/usr/bin/env python3
"""R13/C11 v2: one public entrypoint file per *changed* goal directory."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_r13_entrypoints import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
