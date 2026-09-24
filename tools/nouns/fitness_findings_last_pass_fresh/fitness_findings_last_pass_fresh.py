#!/usr/bin/env python3
"""FINDINGS last_pass_sha must match current HEAD short SHA (F2)."""

from __future__ import annotations



import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = ROOT / "FINDINGS.md"

SHA_RE = re.compile(r"last_pass_sha:\s*([0-9a-f]{7,40})", re.I)


def git_short_head() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return (proc.stdout or "").strip()


def main() -> int:
    _ = sys.argv[1:]
    if not FINDINGS.is_file():
        print("VIOLATION missing FINDINGS.md")
        print("RESULT:NOT_MET")
        return 1

    text = FINDINGS.read_text(encoding="utf-8", errors="replace")
    m = SHA_RE.search(text)
    if not m:
        print("VIOLATION FINDINGS.md missing last_pass_sha: <git short sha>")
        print("RESULT:NOT_MET")
        return 1

    recorded = m.group(1)
    head = git_short_head()
    if not head:
        print("VIOLATION cannot resolve git HEAD")
        print("RESULT:NOT_MET")
        return 1

    if not head.startswith(recorded) and not recorded.startswith(head):
        if head[: len(recorded)] != recorded and recorded[: len(head)] != head:
            print(f"VIOLATION last_pass_sha {recorded} != HEAD {head}")
            print("RESULT:NOT_MET")
            return 1

    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

