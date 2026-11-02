#!/usr/bin/env python3
"""Grade a tree's checker-digest armor. This file on main is the tag verifier.

The commit being tagged must not be the process that decides its own signature.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.checker_digest.checker_digest import DIGEST_REL, digest_errors  # noqa: E402
from nouns.owner_sidecar.owner_sidecar import verify_sidecar_p1  # noqa: E402


def signature_errors(root: Path) -> list[str]:
    errors = digest_errors(root)
    errors.extend(verify_sidecar_p1(root, DIGEST_REL))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Require checker-digest owner armor")
    parser.add_argument("--root", default=None, help="Tree to grade (default: this repo)")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else ROOT
    errors = signature_errors(root)
    if errors:
        print("CHECKER_DIGEST_SIGNATURE:NOT_MET")
        for item in errors:
            print(f"VIOLATION {item}")
        return 1
    print("CHECKER_DIGEST_SIGNATURE:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
