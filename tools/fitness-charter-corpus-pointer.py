#!/usr/bin/env python3
"""E1: CHARTER.md or CHARTER-CORPUS.md must point at integrity/rule-corpus.json."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.fitness_charter_corpus_pointer import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
