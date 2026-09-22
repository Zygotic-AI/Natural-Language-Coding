#!/usr/bin/env python3
"""ADR 0023: canonical compiler-style nlc:rule= receipt lines."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402

RULE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

PREFIX = {
    "python": "# nlc:rule={id}",
    "py": "# nlc:rule={id}",
    "javascript": "// nlc:rule={id}",
    "js": "// nlc:rule={id}",
    "typescript": "// nlc:rule={id}",
    "ts": "// nlc:rule={id}",
}


def marker_line(rule_id: str, lang: str = "python") -> str:
    rid = rule_id.strip()
    if not RULE_ID_RE.match(rid):
        raise ValueError(f"invalid rule_id: {rule_id}")
    key = lang.strip().lower()
    template = PREFIX.get(key)
    if template is None:
        raise ValueError(f"unsupported lang: {lang} (use: {', '.join(sorted(set(PREFIX)))})")
    return template.format(id=rid)


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
