#!/usr/bin/env python3
"""ADR 0023: canonical compiler-style nlc:rule= receipt lines (CLI adapter)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.rule_receipt.rule_receipt import marker_line  # noqa: E402


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Emit ADR 0023 rule receipt comment line")
    parser.add_argument("--id", required=True, help="adopted rule_id")
    parser.add_argument("--lang", default="python", help="python|js|ts|…")
    args = parser.parse_args()
    try:
        line = marker_line(args.id, args.lang)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    sys.stdout.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
