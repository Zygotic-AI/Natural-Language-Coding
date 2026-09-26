#!/usr/bin/env python3
"""CLI: main production-trunk purity (ADR 0044)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_main_purity import main  # noqa: E402

HUB_ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main(hub_root=HUB_ROOT))
