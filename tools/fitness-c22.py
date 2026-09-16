#!/usr/bin/env python3
"""C22 v2: N/A is a lie if this tree holds a charter *and* code.

If PROPOSAL.md / CONFIRM.md exists:
  missing-c22            — no `C22 — PASS|N/A`
  c22-na-with-both       — C22 is N/A but the tree has CHARTER.md/adrs/ *and*
                           goals/ or domain/ source
  c22-pass-missing-cite  — C22 is PASS but the note cites neither a charter/adr
                           path nor a code path that exists

No note → skip (MET). Does not inspect git.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> <kind>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ("PROPOSAL.md", "CONFIRM.md")
C22 = re.compile(r"\bC22\s*—\s*(PASS|N/A)\b")
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
CODE_EXTS = {".py", ".ts", ".js", ".json"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def has_charter(root: Path) -> bool:
    if (root / "CHARTER.md").is_file():
        return True
    adrs = root / "adrs"
    if adrs.is_dir():
        return any(p.suffix == ".md" and p.name.lower() != "readme.md" for p in adrs.glob("*.md"))
    return False


def code_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in ("goals", "domain"):
        tree = root / name
        if not tree.is_dir():
            continue
        for p in tree.rglob("*"):
            if not p.is_file() or is_skipped(p):
                continue
            if "tests" in p.parts:
                continue
            if p.suffix in CODE_EXTS or p.name.endswith(".schema.json"):
                files.append(p)
    return files


def cited_existing(text: str, root: Path) -> tuple[bool, bool]:
    """Return (cited_charter, cited_code) for paths that exist under root or ROOT."""
    cited_charter = False
    cited_code = False
    for raw in re.findall(r"[A-Za-z0-9_./-]+\.(?:md|py|ts|js|json)", text):
        cand = Path(raw)
        hits = []
        if cand.is_file():
            hits.append(cand)
        elif (root / raw).is_file():
            hits.append(root / raw)
        elif (ROOT / raw).is_file():
            hits.append(ROOT / raw)
        for hit in hits:
            s = str(hit).replace("\\", "/")
            if hit.name == "CHARTER.md" or "/adrs/" in s or hit.parent.name == "adrs":
                cited_charter = True
            if "/goals/" in s or "/domain/" in s:
                cited_code = True
    if "CHARTER.md" in text and ((root / "CHARTER.md").is_file() or (ROOT / "CHARTER.md").is_file()):
        cited_charter = True
    return cited_charter, cited_code


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    notes = [scan_root / n for n in NOTES if (scan_root / n).is_file()]
    if not notes:
        return []
    charter = has_charter(scan_root)
    code = bool(code_files(scan_root))
    violations: list[tuple[str, str]] = []
    for path in notes:
        text = path.read_text(errors="replace")
        m = C22.search(text)
        if m is None:
            violations.append((rel(path), "missing-c22"))
            continue
        verdict = m.group(1).upper()
        if verdict == "N/A":
            if charter and code:
                violations.append((rel(path), "c22-na-with-both"))
            continue
        cited_charter, cited_code = cited_existing(text, scan_root)
        if charter and not cited_charter:
            violations.append((rel(path), "c22-pass-missing-cite"))
        elif code and not cited_code:
            violations.append((rel(path), "c22-pass-missing-cite"))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, str]] = set()
    printed: list[tuple[str, str]] = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, kind = item
            print(f"VIOLATION {path} {kind}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
