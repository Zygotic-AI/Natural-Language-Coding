#!/usr/bin/env python3
"""CLI: infer hub ./release plan (zero-parameter surface)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_infer import main  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
