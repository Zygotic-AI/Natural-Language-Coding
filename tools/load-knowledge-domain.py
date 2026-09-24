#!/usr/bin/env python3
"""Knowledge steward `load-knowledge-domain` — read confirmed facts for a scope.

Usage:
  python3 tools/load-knowledge-domain.py <scope> [repo-root]

Output: JSON {status, facts} on stdout. Exit 0 unless DOMAIN_UNAVAILABLE.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.load_knowledge_domain import main  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
