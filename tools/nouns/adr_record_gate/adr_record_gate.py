"""Fail the hub compile when an active ADR is unapproved, unbound, or a gap."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from nouns.adr_approval.adr_approval import active_numbers, approval_errors  # noqa: E402

_RANGE = re.compile(r"^\|\s*(\d{4})(?:[–-](\d{4}))?\s*\|")
_SELF = {
    "tools/fitness-adr-record-gate.py",
    "tools/nouns/adr_record_gate/adr_record_gate.py",
}


def enforcement_rows(text: str) -> dict[str, str]:
    """Map each ADR number to its status cell."""
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = _RANGE.match(line.strip())
        if not match:
            continue
        start = int(match.group(1))
        end = int(match.group(2) or match.group(1))
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        status = parts[-1] if parts else ""
        for number in range(start, end + 1):
            rows[f"{number:04d}"] = status
    return rows


def status_errors(status: str) -> list[str]:
    lowered = status.lower()
    errors: list[str] = []
    if re.search(r"\bgap\b", lowered):
        errors.append("marked as a gap")
    if "bound" not in lowered:
        errors.append("unbound")
    return errors


def record_gate_errors(root: Path) -> list[str]:
    errors = [f"approval: {item}" for item in approval_errors(root)]
    numbers = active_numbers((root / "adrs" / "ACTIVE.md").read_text(encoding="utf-8"))
    rows = enforcement_rows((root / "docs" / "ADR-ENFORCEMENT.md").read_text(encoding="utf-8"))
    gates_path = root / "integrity" / "adr-gates.json"
    if not gates_path.is_file():
        errors.append("missing integrity/adr-gates.json")
        gates: dict[str, object] = {}
    else:
        payload = json.loads(gates_path.read_text(encoding="utf-8"))
        raw = payload.get("records") if isinstance(payload, dict) else None
        gates = raw if isinstance(raw, dict) else {}
    backlog = root / "integrity" / "charter-ratify-backlog.json"
    if not backlog.is_file():
        errors.append("0031: missing charter ratification backlog")
    for number in numbers:
        status = rows.get(number)
        if status is None:
            errors.append(f"{number}: missing enforcement row")
            continue
        for problem in status_errors(status):
            errors.append(f"{number}: {problem}")
        row = gates.get(number)
        if not isinstance(row, dict):
            errors.append(f"{number}: missing gate registry row")
            continue
        for key in ("gate", "fixture"):
            rel = row.get(key)
            if not isinstance(rel, str) or not (root / rel).is_file():
                errors.append(f"{number}: missing {key}")
    if backlog.is_file():
        payload = json.loads(backlog.read_text(encoding="utf-8"))
        residuals = payload.get("non_r_residuals") if isinstance(payload, dict) else None
        if not isinstance(residuals, list):
            errors.append("0037: missing non_r_residuals")
    seen: set[str] = set()
    for number in numbers:
        row = gates.get(number)
        if not isinstance(row, dict):
            continue
        rel = row.get("fixture")
        if not isinstance(rel, str) or rel in seen or rel in _SELF:
            continue
        seen.add(rel)
        path = root / rel
        if not path.is_file():
            continue
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            tail = (proc.stdout + "\n" + proc.stderr).strip().splitlines()
            detail = tail[-1] if tail else "no output"
            errors.append(f"{number}: fixture {rel} failed ({proc.returncode}) {detail}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = record_gate_errors(root)
    if errors:
        for item in errors[:20]:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
