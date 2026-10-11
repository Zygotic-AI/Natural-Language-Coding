#!/usr/bin/env python3
"""Fail on broken relative markdown links in in-force documentation (O6)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

SKIP_DIR_PARTS = {
    "reviews",
    "node_modules",
    ".git",
    ".venv",
    "theory",
    "docs/rca",
    "docs/history",
    "examples",
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```", re.MULTILINE)

IN_FORCE_MARKDOWN = [
    ROOT / "AGENTS.md",
    ROOT / "DESCRIBE.md",
    ROOT / "README.md",
    ROOT / "CHARTER.md",
    ROOT / "docs" / "OPERATING_BINDINGS.md",
    ROOT / "docs" / "TERMS.md",
    ROOT / "docs" / "bba" / "BBA-EMIT-PROCESS.md",
    ROOT / "docs" / "nlc" / "compiler" / "PLANIT-ORCHESTRATION.md",
    ROOT / "integrity" / "ACTIONS.md",
    ROOT / "integrity" / "BOUNDARY.md",
    ROOT / "integrity" / "GATE.md",
]


def strip_fences(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(part in rel.split("/") for part in SKIP_DIR_PARTS)


def iter_markdown_files() -> list[Path]:
    found: list[Path] = []
    adrs = ROOT / "adrs"
    if adrs.is_dir():
        found.extend(sorted(adrs.glob("*.md")))
    for path in IN_FORCE_MARKDOWN:
        if path.is_file():
            found.append(path)
    return sorted(set(found))


def resolve_link(source: Path, target: str) -> Path | None:
    raw = target.strip()
    if not raw or raw.startswith("#"):
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
        return None
    file_part = raw.split("#", 1)[0].strip()
    if not file_part:
        return None
    if file_part.startswith("/"):
        return ROOT / file_part.lstrip("/")
    return (source.parent / file_part).resolve()


def scan_file(path: Path) -> list[str]:
    text = strip_fences(path.read_text(encoding="utf-8", errors="replace"))
    violations: list[str] = []
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        rel = path
    for match in LINK_RE.finditer(text):
        resolved = resolve_link(path, match.group(1))
        if resolved is None:
            continue
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            if path.is_relative_to(ROOT):
                violations.append(f"{rel}: link escapes repo {match.group(1)!r}")
            continue
        if not resolved.is_file() and not resolved.is_dir():
            violations.append(f"{rel}: broken link {match.group(1)!r}")
    return violations


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in iter_markdown_files():
        violations.extend(scan_file(path))
    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
