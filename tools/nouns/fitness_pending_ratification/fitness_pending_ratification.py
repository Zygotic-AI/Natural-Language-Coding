"""C7: Pending/Proposed decision or Proposed document presented as ratified → NOT_MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

from nouns.owner_sidecar.owner_sidecar import pending_presented_as_ratified_errors

ROOT = Path(__file__).resolve().parents[3]
KNOWN_BAD = ROOT / "tools/fixtures/owner-ratification-sidecar/pending-as-ratified.json"


def pending_errors_for_case(case: dict[str, object]) -> list[str]:
    fields = case.get("fields")
    if not isinstance(fields, dict):
        return ["pending case missing fields"]
    status = str(case.get("status") or "")
    str_fields = {str(k): str(v) for k, v in fields.items()}
    return pending_presented_as_ratified_errors(status, str_fields, document_rel=str(case.get("document_rel") or ""))


def main() -> int:
    errors: list[str] = []
    if not KNOWN_BAD.is_file():
        errors.append(f"missing known-bad {KNOWN_BAD.relative_to(ROOT)}")
    else:
        payload = json.loads(KNOWN_BAD.read_text(encoding="utf-8"))
        cases = payload if isinstance(payload, list) else payload.get("cases")
        if not isinstance(cases, list) or not cases:
            errors.append("pending-as-ratified.json must list cases")
        else:
            for case in cases:
                if not isinstance(case, dict):
                    errors.append("pending case must be object")
                    continue
                found = pending_errors_for_case(case)
                if not found:
                    errors.append(f"{case.get('name')}: expected NOT_MET got MET")
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
