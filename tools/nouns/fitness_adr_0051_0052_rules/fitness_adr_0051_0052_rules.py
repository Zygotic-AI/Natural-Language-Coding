"""C11: integrity/adr-0051-0052-rules.json ids equal derive_rules.py; non-CONTEXT rows are bound."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RULES_REL = "integrity/adr-0051-0052-rules.json"
DERIVE = ROOT / "tools" / "derive-adr-0051-0052-rules.py"
OWNER_EXEMPT = frozenset({"0051:L25", "0052:DEC-6"})
KNOWN_BAD = ROOT / "tools/fixtures/adr-0051-0052-rules/missing-rule-id.json"


def derive_rule_ids(root: Path) -> list[str]:
    proc = subprocess.run(
        [sys.executable, str(DERIVE), str(root)],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    ids: list[str] = []
    for line in (proc.stdout or "").splitlines():
        if not line.strip():
            continue
        ids.append(line.split("\t", 1)[0])
    return ids


def load_rules(payload: dict[str, object]) -> list[dict[str, object]]:
    raw = payload.get("rules")
    if not isinstance(raw, list):
        return []
    return [row for row in raw if isinstance(row, dict)]


def rules_ssot_errors(root: Path, payload: dict[str, object] | None = None) -> list[str]:
    errors: list[str] = []
    if payload is None:
        path = root / RULES_REL
        if not path.is_file():
            return [f"missing {RULES_REL}"]
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            return [f"{RULES_REL} must be object"]
        payload = loaded
    derived = derive_rule_ids(root)
    if not derived:
        return ["derive-adr-0051-0052-rules.py produced no ids"]
    rows = load_rules(payload)
    have = [str(row.get("id") or "") for row in rows]
    missing = [i for i in derived if i not in have]
    extra = [i for i in have if i not in derived]
    if missing:
        errors.append("rules SSOT missing derived ids: " + ",".join(missing))
    if extra:
        errors.append("rules SSOT extra ids: " + ",".join(extra))
    if have != derived:
        errors.append("rules SSOT id order or set differs from derive_rules.py")
    for row in rows:
        rid = str(row.get("id") or "")
        status = str(row.get("status") or "")
        if status == "CONTEXT" or rid in OWNER_EXEMPT:
            continue
        check_id = str(row.get("check_id") or "").strip()
        known_bad = str(row.get("known_bad_id") or "").strip()
        if not check_id:
            errors.append(f"{rid}: missing check_id")
        if not known_bad:
            errors.append(f"{rid}: missing known_bad_id")
    return errors


def main() -> int:
    errors = rules_ssot_errors(ROOT)
    if not KNOWN_BAD.is_file():
        errors.append(f"missing known-bad {KNOWN_BAD.relative_to(ROOT)}")
    else:
        payload = json.loads(KNOWN_BAD.read_text(encoding="utf-8"))
        kb = rules_ssot_errors(ROOT, payload if isinstance(payload, dict) else {})
        if not kb:
            errors.append("known-bad missing-rule-id.json: expected NOT_MET got MET")
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
