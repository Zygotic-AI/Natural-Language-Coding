"""Landmine: hub before-generate writer refuses partial scope lists."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAMP = ROOT / ".nlc" / "before-generate-stamp.json"


def _digest(path: Path) -> str:
    if not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    before = _digest(STAMP)
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc.py"),
            "maintainer",
            "guide",
            "before-generate",
            "--scope",
            "default",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    after = _digest(STAMP)
    if proc.returncode == 0:
        print("ASSERT:FAIL writer should refuse partial hub scopes")
        return 1
    if before != after:
        print("ASSERT:FAIL writer must not change stamp bytes on refusal")
        return 1
    print("ASSERT:PASS hub writer refuses partial scopes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
