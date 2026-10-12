#!/usr/bin/env python3
"""PM offline owner ratification verify (ADR 0052 decision 6).

Verification code loads only from the checkout containing this script.
The --tree argument is read-only data; it is never added to sys.path.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ADAPTER = Path(__file__).resolve()
sys.path.insert(0, str(_ADAPTER.parent))
from nouns.verify_owner_ratification_offline import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(adapter_path=_ADAPTER))
