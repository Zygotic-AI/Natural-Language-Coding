#!/usr/bin/env python3
"""Every uc-product expansion_only key appears in product-completion-scope.json (ADR 0041)."""

from __future__ import annotations



import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCOPE = ROOT / "integrity" / "product-completion-scope.json"
STATUS = ROOT / "integrity" / "uc-product-status.json"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not SCOPE.is_file():
        violations.append("missing product-completion-scope.json")
        print("RESULT:NOT_MET")
        return 1

    scope = json.loads(SCOPE.read_text(encoding="utf-8"))
    exp_scope = scope.get("expansion_only") or {}
    findings = scope.get("findings") or []
    if not findings:
        violations.append("findings array empty")
    for row in findings:
        if not row.get("disposition") or not row.get("acceptance"):
            violations.append(f"findings row {row.get('id')} incomplete")

    if not STATUS.is_file():
        violations.append("missing uc-product-status.json")
    else:
        status = json.loads(STATUS.read_text(encoding="utf-8"))
        for uc, block in (status.get("ucs") or {}).items():
            for key in block.get("expansion_only") or []:
                sid = f"{uc}.{key}"
                if sid not in exp_scope:
                    violations.append(f"expansion_only key not in scope: {sid}")
        packs = status.get("packs_v02") or {}
        for key in packs.get("expansion_only") or []:
            sid = f"packs_v02.{key}"
            if sid not in exp_scope:
                violations.append(f"packs_v02 expansion not in scope: {sid}")
        hub = status.get("hub_v02") or {}
        if hub.get("pack_registry") == "open":
            if "pack_registry" not in (scope.get("hub_v02") or {}):
                violations.append("hub_v02.pack_registry open but not in scope")

    adr = ROOT / "adrs" / "0041-product-completion-scope.md"
    if not adr.is_file():
        violations.append("missing ADR 0041")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

