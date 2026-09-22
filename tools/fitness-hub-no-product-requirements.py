#!/usr/bin/env python3
"""ADR 0016: hub must not ship product requirement packs as repo SSOT."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_DIRS = (
    "compliance",
    "requirements/pci",
    "requirements/hipaa",
    "product-requirements",
)


def main() -> int:
    violations: list[str] = []
    adopted = ROOT / "rules" / "adopted.json"
    if adopted.is_file():
        try:
            data = json.loads(adopted.read_text(encoding="utf-8"))
            rows = data.get("adoptions") or []
            if rows:
                violations.append(
                    "rules/adopted.json must not list product adoptions on hub (ADR 0016)"
                )
        except json.JSONDecodeError:
            violations.append("rules/adopted.json is invalid JSON")
    readme = ROOT / "README.md"
    if readme.is_file():
        head = readme.read_text(encoding="utf-8", errors="replace")
        if "0016" not in head and "product requirements" not in head.casefold():
            violations.append("README must mention ADR 0016 / no product requirements")
    for rel in FORBIDDEN_DIRS:
        if (ROOT / rel).exists():
            violations.append(f"forbidden product-requirements path: {rel}")
    goals = ROOT / "goals"
    if goals.is_dir() and any(goals.rglob("implementation.py")):
        violations.append("hub root goals/**/implementation.py is product code (ADR 0016)")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
