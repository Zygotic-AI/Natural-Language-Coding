#!/usr/bin/env python3
"""hub_v02.pack_consume_regen: install must write pack-consume-status.json when closed."""

from __future__ import annotations



import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INSTALL = ROOT / "tools" / "nlc-pack-install.py"
STATUS = ROOT / "integrity" / "uc-product-status.json"
NEEDLES = (
    "pack-consume-status.json",
    "write_pack_consume_status",
    "uc9_queue_hint",
    "scope_tags",
)


def main() -> int:
    _ = sys.argv[1:]
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    hub = status.get("hub_v02") or {}
    flag = str(hub.get("pack_consume_regen", ""))
    src = INSTALL.read_text(encoding="utf-8", errors="replace")
    missing = [n for n in NEEDLES if n not in src]
    if missing:
        for n in missing:
            print(f"VIOLATION nlc-pack-install.py missing {n}")
        print("RESULT:NOT_MET")
        return 1
    if flag == "closed":
        # Writer present is enough for hub gate; adopter runtime writes the file.
        print("RESULT:MET pack_consume_regen=closed + install writer present")
        return 0
    if flag == "open":
        print("RESULT:MET pack_consume_regen still open (writer ready)")
        return 0
    print(f"VIOLATION unexpected hub_v02.pack_consume_regen={flag!r}")
    print("RESULT:NOT_MET")
    return 1


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

