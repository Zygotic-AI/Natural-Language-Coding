#!/usr/bin/env python3
"""Landmine ADR 0006: teaching adopter invoice-correct has no contract_change blockers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_invoice_correct_contract_blockers_passes import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
