"""KB-0058-unsigned-tag: the tag gate does not require a digest sidecar."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.nlc_release_tag_gate import nlc_release_tag_gate as tag_gate  # noqa: E402


def main() -> int:
    if hasattr(tag_gate, "checker_digest_signature_problems"):
        print("ASSERT:FAIL tag gate still has checker_digest_signature_problems")
        return 1
    print("ASSERT:PASS tag gate allows an unsigned merge commit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
