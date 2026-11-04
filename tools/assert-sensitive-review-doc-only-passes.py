#!/usr/bin/env python3
"""Hub landmine adapter for KB-0058-doc."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_sensitive_review_doc_only_passes.assert_sensitive_review_doc_only_passes import (  # noqa: E402
    main,
)

if __name__ == "__main__":
    raise SystemExit(main())
