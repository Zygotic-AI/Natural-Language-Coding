"""Known-bad: unsigned checker digest is refused; this branch does not require it."""

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
    on_main = subprocess.run(
        ["git", "cat-file", "-e", "origin/main:tools/check-checker-digest-signature.py"],
        cwd=str(ROOT),
        capture_output=True,
        check=False,
    )
    if on_main.returncode == 0:
        print("ASSERT:FAIL origin/main already has the tag verifier; bootstrap skip is wrong")
        return 1
    print("ASSERT:PASS unsigned checker digest is refused by the tag verifier and not by this branch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
