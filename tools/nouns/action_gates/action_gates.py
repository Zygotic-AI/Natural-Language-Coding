"""X6: run the default-closed gates of ADRs bound to an action (ADR 0024 / 0030).

Input: JSON list of {"adr_id", "gate_cmd", "args": [...]}.
Each gate_cmd is executed; non-zero exit or RESULT:NOT_MET fails the stage.
Default-closed: an empty list fails (no bound gates means nothing was bound).
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from nlc_requirements import hub_tool  # noqa: E402


def main() -> int:
    hub_tool()
    path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    if path is None or not path.is_file():
        print("RESULT:NOT_MET")
        print("VIOLATION no action-gates file given (default-closed)")
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"VIOLATION invalid json: {exc}")
        print("RESULT:NOT_MET")
        return 1
    if not isinstance(data, list) or not data:
        print("VIOLATION action-gates must be a non-empty list")
        print("RESULT:NOT_MET")
        return 1
    for row in data:
        if not isinstance(row, dict):
            print("VIOLATION gate entry is not an object")
            print("RESULT:NOT_MET")
            return 1
        cmd = row.get("gate_cmd")
        if not cmd:
            print(f"VIOLATION gate for {row.get('adr_id')!r} has no gate_cmd")
            print("RESULT:NOT_MET")
            return 1
        args = [str(a) for a in row.get("args", [])]
        proc = subprocess.run([cmd, *args], capture_output=True, text=True)
        out = (proc.stdout or "") + (proc.stderr or "")
        sys.stdout.write(out)
        if proc.returncode != 0 or "RESULT:NOT_MET" in out:
            print(f"RESULT:NOT_MET adr={row.get('adr_id')}")
            return 1
        print(f"PIPELINE:MET adr={row.get('adr_id')} gate={cmd}")
    print("RESULT:MET")
    return 0


