#!/usr/bin/env python3
"""Landmine: validate-agent-noun-packages MET on hub agents/."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_validate_agent_nouns_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
