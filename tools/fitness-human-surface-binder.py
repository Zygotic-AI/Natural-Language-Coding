#!/usr/bin/env python3
"""ADR 0017–0020: human menu, interview gap, dashboard, MENU/HARNESS wired in CI."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FITNESS = (
    "fitness-menu-harness-sync.py",
    "fitness-interview-gap-shape.py",
    "fitness-dashboard-interview-sync.py",
    "fitness-interview-prompt-shape.py",
)

LANDMINES = (
    "assert-interview-gap-passes.py",
    "assert-dashboard-interview-passes.py",
)

DOCS = (
    "docs/nlc/MENU.md",
    "docs/nlc/HARNESS.md",
    "tools/nlc_menu_data.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = (ROOT / "tools" / "ci_fitness.py").read_text(encoding="utf-8", errors="replace")
    for name in FITNESS:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
        elif name.replace(".py", "") not in ci:
            violations.append(f"ci_fitness must run {name}")
    for name in LANDMINES:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
            continue
        stem = name.removesuffix("-passes.py").removesuffix(".py")
        if stem not in ci and name not in ci:
            violations.append(f"ci_fitness must run {name}")
    for rel in DOCS:
        if not (ROOT / rel).is_file():
            violations.append(f"missing {rel}")
    menu = (ROOT / "docs/nlc/MENU.md").read_text(encoding="utf-8", errors="replace") if (ROOT / "docs/nlc/MENU.md").is_file() else ""
    if menu and "/planit" not in menu:
        violations.append("MENU.md must list /planit for agents")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
