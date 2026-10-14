#!/usr/bin/env python3
"""Fail when tracked evidence/fixtures pin resolvable git commit ids (ADR 0050)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.evidence_ref.evidence_ref import commit_pins_in_text  # noqa: E402

SCAN_ROOTS = (
    ROOT / "FINDINGS.md",
    ROOT / "integrity",
    ROOT / "tools" / "nouns",
    ROOT / "examples",
)

SKIP_DIR_PARTS = {
    "docs/rca",
    "docs/history",
    "__pycache__",
}

SKIP_FILES = {
    "integrity/nlc-install-hashes.json",
    "integrity/planit-skill-registry.json",
}


def tracked_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    out: list[Path] = []
    for line in (proc.stdout or "").splitlines():
        rel = line.strip()
        if not rel:
            continue
        if rel.replace("\\", "/") in SKIP_FILES:
            continue
        if rel.startswith("docs/rca/") or rel.startswith("docs/history/"):
            continue
        path = ROOT / rel
        if path.is_file():
            out.append(path)
    return out


def should_scan(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("docs/rca/") or rel.startswith("docs/history/"):
        return False
    if rel in SKIP_FILES:
        return False
    for part in SKIP_DIR_PARTS:
        if part in rel:
            return False
    if rel == "FINDINGS.md":
        return True
    if rel.startswith("integrity/") and rel.endswith(".json"):
        return True
    if "/nouns/assert_" in rel and rel.endswith(".py"):
        return True
    if rel.startswith("examples/") and (rel.endswith(".json") or rel.endswith(".md")):
        return True
    return False


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in tracked_files():
        if not should_scan(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        pins = commit_pins_in_text(ROOT, text)
        if pins:
            violations.append(f"{path.relative_to(ROOT)} pins commits: {', '.join(pins[:5])}")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())


BOUNDARY = "bba-emit"
