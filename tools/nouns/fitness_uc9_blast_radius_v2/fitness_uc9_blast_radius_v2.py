#!/usr/bin/env python3
"""UC9 v2 rule-tagged blast radius product boundary (P6.1)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRODUCT_BOUNDARY = ROOT / "integrity" / "uc9-product-boundary.json"
IMPACT = ROOT / "docs" / "spine" / "IMPACT-GRAPH.md"
STATUS = ROOT / "integrity" / "uc-product-status.json"


def run_assert(rel: str) -> bool:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / rel)],
        cwd=str(ROOT),
        check=False,
    )
    return proc.returncode == 0


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not PRODUCT_BOUNDARY.is_file():
        violations.append("missing integrity/uc9-product-boundary.json")
    else:
        data = json.loads(PRODUCT_BOUNDARY.read_text(encoding="utf-8"))
        if data.get("remain_expansion"):
            violations.append("uc9-product-boundary remain_expansion must be empty")
        for cmd in data.get("product_closed", {}).get("proof_commands") or []:
            if not cmd.startswith("python3 tools/"):
                violations.append(f"bad proof command: {cmd}")
    if not IMPACT.is_file():
        violations.append("missing IMPACT-GRAPH.md")
    else:
        text = IMPACT.read_text(encoding="utf-8", errors="replace")
        if "--orchestrate" not in text or "--write-queue" not in text:
            violations.append("IMPACT-GRAPH.md must document orchestrate + write-queue")
    if STATUS.is_file():
        exp = (json.loads(STATUS.read_text(encoding="utf-8")).get("ucs") or {}).get(
            "UC9", {}
        ).get("expansion_only") or []
        if exp:
            violations.append(f"UC9 expansion_only must be empty after P6.1: {exp}")
    for script in (
        "assert-goal-bindings-narrow-fails.py",
        "assert-delta-regen-narrow-passes.py",
        "assert-delta-regen-orchestrate-passes.py",
        "assert-verify-regen-queue-fails.py",
    ):
        if not run_assert(script):
            violations.append(f"{script} must ASSERT:PASS")
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

