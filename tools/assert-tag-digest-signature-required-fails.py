#!/usr/bin/env python3
"""Hub landmine adapter for assert_tag_digest_signature_required_fails."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_tag_digest_signature_required_fails.assert_tag_digest_signature_required_fails import main


if __name__ == "__main__":
    raise SystemExit(main())
