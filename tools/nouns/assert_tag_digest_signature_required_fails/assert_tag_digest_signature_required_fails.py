"""Known-bad: an unsigned checker digest is refused once the tag verifier exists."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check-checker-digest-signature.py"), "--root", str(ROOT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    blob = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0 or "CHECKER_DIGEST_SIGNATURE:NOT_MET" not in blob:
        print(f"ASSERT:FAIL tag verifier accepted unsigned digest: {blob}")
        return 1
    print("ASSERT:PASS unsigned checker digest is refused by the tag verifier")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
