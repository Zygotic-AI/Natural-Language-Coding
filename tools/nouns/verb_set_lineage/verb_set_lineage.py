"""Closed atomic verb set and active-tip lineage (ADR 0028)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

BASELINE = (
    "create",
    "read",
    "write",
    "update",
    "delete",
    "validate",
    "emit",
    "bind",
)


def extension_errors(document: dict[str, object], baseline: tuple[str, ...] = BASELINE) -> list[str]:
    verbs = document.get("verbs")
    if not isinstance(verbs, list):
        return ["verbs must be a list"]
    allowed = set(baseline)
    errors: list[str] = []
    for row in verbs:
        if isinstance(row, str):
            name = row
            adr = "baseline" if name in allowed else ""
        elif isinstance(row, dict):
            raw_name = row.get("name")
            raw_adr = row.get("adr")
            name = raw_name if isinstance(raw_name, str) else ""
            adr = raw_adr if isinstance(raw_adr, str) else ""
        else:
            errors.append("verb row must be a name or an object")
            continue
        if not name:
            errors.append("verb name is empty")
            continue
        if name not in allowed and not adr.strip():
            errors.append(f"{name}: extension requires an ADR")
    return errors


def baseline_errors(document: dict[str, object]) -> list[str]:
    verbs = document.get("verbs")
    if not isinstance(verbs, list):
        return ["baseline verbs must be a list"]
    if tuple(verbs) != BASELINE:
        return ["baseline atomic verb set changed"]
    return []


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors: list[str] = []
    baseline_path = root / "integrity" / "atomic-verbs.json"
    repo_path = root / ".nlc" / "verbs.json"
    if not baseline_path.is_file():
        errors.append("missing integrity/atomic-verbs.json")
    else:
        errors.extend(baseline_errors(json.loads(baseline_path.read_text(encoding="utf-8"))))
    if not repo_path.is_file():
        errors.append("missing .nlc/verbs.json")
    else:
        errors.extend(extension_errors(json.loads(repo_path.read_text(encoding="utf-8"))))
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
