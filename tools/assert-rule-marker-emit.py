#!/usr/bin/env python3
"""Landmine: nlc_rule_marker.py emits stable ADR 0023 lines."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "nlc_rule_marker.py"


def load() -> object:
    spec = importlib.util.spec_from_file_location("nlc_rule_marker", TOOL)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load nlc_rule_marker.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    mod = load()
    py = mod.marker_line("demo-verb-only", "python")
    if py != "# nlc:rule=demo-verb-only":
        print(f"ASSERT:FAIL python marker got {py!r}")
        return 1
    js = mod.marker_line("pan-no-return", "js")
    if js != "// nlc:rule=pan-no-return":
        print(f"ASSERT:FAIL js marker got {js!r}")
        return 1
    try:
        mod.marker_line("bad id", "python")
        print("ASSERT:FAIL should reject bad rule_id")
        return 1
    except ValueError:
        pass
    print("ASSERT:PASS nlc_rule_marker emit shape")
    return 0


if __name__ == "__main__":
    sys.exit(main())
