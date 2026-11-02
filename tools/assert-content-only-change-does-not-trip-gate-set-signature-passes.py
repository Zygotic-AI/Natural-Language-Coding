#!/usr/bin/env python3
"""Hub landmine adapter for assert_content_only_change_does_not_trip_gate_set_signature_passes."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_content_only_change_does_not_trip_gate_set_signature_passes import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
