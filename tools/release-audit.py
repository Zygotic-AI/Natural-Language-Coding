#!/usr/bin/env python3
"""Release audit: AI gates + human gates, with numbered remediations.

Pipeline hook. Run before merge/deploy. Not the same as ci-fitness.sh
(that suite proves landmines + the teaching tree). This tool proves a
*product tree* may ship.

Exit 0 = RELEASE:MET. Exit 1 = RELEASE:NOT_MET.
Class C can pass ci-fitness without a human. It cannot pass this tool
without `Released-by: <human name>` on CONFIRM.md.

Input: optional argv tree (default: cwd).
Output: GATE lines, then UNMET blocks with Step 1…N, then RELEASE:MET|NOT_MET.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_audit import main  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
