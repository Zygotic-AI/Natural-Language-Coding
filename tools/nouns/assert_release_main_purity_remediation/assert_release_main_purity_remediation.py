"""Landmine: main purity NOT_MET fix is not fetch-only (RCA 26-09-25)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

BOUNDARY = "bba-emit"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.release_remediate import main_purity_remediation  # noqa: E402

    lines = main_purity_remediation(hub=ROOT, next_release_branch="release/v0.3.0")
    text = "\n".join(lines)
    if "reset --hard" not in text:
        print("ASSERT:FAIL main_purity_remediation must reset main to tag")
        return 1
    if len(lines) < 4:
        print("ASSERT:FAIL main_purity_remediation too short (fetch-only risk)")
        return 1
    if lines[0].strip().startswith("git fetch") and "reset" not in text:
        print("ASSERT:FAIL fetch-only remediation")
        return 1
    print("ASSERT:PASS main purity remediation (not fetch-only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
