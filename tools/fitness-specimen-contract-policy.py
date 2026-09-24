#!/usr/bin/env python3
"""ADR 0006: specimen contract-change skip policy is documented and testable."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_specimen_contract_policy import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
