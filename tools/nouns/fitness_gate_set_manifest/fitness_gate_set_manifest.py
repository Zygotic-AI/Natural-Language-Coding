"""ADR 0051 SG2 / ADR 0052: gate-set baseline manifest + owner sidecar."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

from nouns.gate_set_manifest.gate_set_manifest import gate_set_manifest_errors


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = gate_set_manifest_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
