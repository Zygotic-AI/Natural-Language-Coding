#!/usr/bin/env python3
"""UC20 v1: verb → interior primitive inventory (Python domain/)."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.call_tree import *  # noqa: F403
__all__ = ['CALL_RE', 'INVENTORY_FILE', '_scan_py_file', 'check_inventory', 'main', 'scan_domain_verbs', 'write_inventory']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

