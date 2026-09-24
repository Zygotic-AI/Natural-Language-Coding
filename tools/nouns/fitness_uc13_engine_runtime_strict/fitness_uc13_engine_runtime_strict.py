#!/usr/bin/env python3
"""UC13 v2 engine.runtime tag strict product boundary (P6.2)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from fitness_hub_source import read_tool  # noqa: E402

PRODUCT_BOUNDARY = ROOT / "integrity" / "uc13-product-boundary.json"
STATUS = ROOT / "integrity" / "uc-product-status.json"


def run_assert(rel: str) -> bool:
    return (
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / rel)],
            cwd=str(ROOT),
            check=False,
        ).returncode
        == 0
    )


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not PRODUCT_BOUNDARY.is_file():
        violations.append("missing integrity/uc13-product-boundary.json")
    else:
        data = json.loads(PRODUCT_BOUNDARY.read_text(encoding="utf-8"))
        if data.get("remain_expansion"):
            violations.append("uc13-product-boundary remain_expansion must be empty")
    if STATUS.is_file():
        exp = (json.loads(STATUS.read_text(encoding="utf-8")).get("ucs") or {}).get(
            "UC13", {}
        ).get("expansion_only") or []
        if exp:
            violations.append(f"UC13 expansion_only must be empty after P6.2: {exp}")
    comp = read_tool("tools/nlc_compliance.py")
    if "engine_runtime_tag_strict_blockers" not in comp:
        violations.append("verify_fast_blockers must wire engine_runtime_tag_strict_blockers")
    for script in (
        "assert-durable-engine-rule-fails.py",
        "assert-durable-engine-tag-strict-fails.py",
        "assert-durable-engine-tag-strict-passes.py",
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

