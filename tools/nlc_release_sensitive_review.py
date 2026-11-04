#!/usr/bin/env python3
"""Grade sensitive-file changes. Default grader is origin/main's copy (ADR 0058)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.sensitive_review.sensitive_review import main  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
