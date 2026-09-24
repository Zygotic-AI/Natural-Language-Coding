"""UC20 v1: verb → interior primitive inventory (Python domain/)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import re
import sys
from pathlib import Path

from nlc_requirements import hub_tool

from nlc_uc_blockers import PRIMITIVE_NAMES

INVENTORY_FILE = "verb-primitives.json"
CALL_RE = re.compile(
    r"\b(" + "|".join(sorted(PRIMITIVE_NAMES)) + r")\s*\(",
)


def _scan_source_file(path: Path, verb: str, found: dict[str, set[str]]) -> None:
    if "/tests/" in str(path) or path.name.startswith("test_"):
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    prims = set(m.group(1) for m in CALL_RE.finditer(text))
    if prims:
        found.setdefault(verb, set()).update(prims)


def _scan_py_file(path: Path, verb: str, found: dict[str, set[str]]) -> None:
    _scan_source_file(path, verb, found)


def scan_domain_verbs(root: Path) -> dict[str, list[str]]:
    found: dict[str, set[str]] = {}
    domain = root / "domain"
    if domain.is_dir():
        for path in domain.rglob("*.py"):
            _scan_py_file(path, path.stem, found)
        for ext in ("*.ts", "*.js", "*.tsx", "*.jsx"):
            for path in domain.rglob(ext):
                _scan_source_file(path, path.stem, found)
    goals = root / "goals"
    if goals.is_dir():
        for impl in goals.glob("*/implementation.py"):
            if impl.parent.is_dir():
                _scan_py_file(impl, impl.parent.name, found)
    return {k: sorted(v) for k, v in sorted(found.items())}


def write_inventory(root: Path, verbs: dict[str, list[str]]) -> Path:
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    path = nlc / INVENTORY_FILE
    path.write_text(
        json.dumps({"schema": 1, "verbs": verbs}, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def check_inventory(root: Path) -> list[str]:
    live = scan_domain_verbs(root)
    if not live:
        return []
    inv_path = root / ".nlc" / INVENTORY_FILE
    if not inv_path.is_file():
        return [
            "UC20 call-tree: missing .nlc/verb-primitives.json "
            "(./nlc maintainer call-tree --sync after verb edits)"
        ]
    try:
        data = json.loads(inv_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["UC20 call-tree: invalid verb-primitives.json"]
    declared = data.get("verbs") or {}
    if not isinstance(declared, dict):
        return ["UC20 call-tree: verbs must be object"]
    bad: list[str] = []
    for verb, prims in live.items():
        dec = declared.get(verb)
        if dec is None:
            bad.append(f"{verb}: undeclared primitives {prims}")
            continue
        dec_set = set(dec) if isinstance(dec, list) else set()
        live_set = set(prims)
        if dec_set != live_set:
            bad.append(f"{verb}: declared {sorted(dec_set)} vs scanned {sorted(live_set)}")
    for verb in declared:
        if verb not in live:
            bad.append(f"{verb}: declared but no domain scan")
    if not bad:
        return []
    return ["UC20 call-tree: " + "; ".join(bad[:4])]


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="UC20 verb primitive inventory (v1 Python)")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--sync", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.sync:
        verbs = scan_domain_verbs(root)
        path = write_inventory(root, verbs)
        print(f"call-tree: MET {path.relative_to(root)} ({len(verbs)} verbs)")
        return 0
    if args.check:
        errs = check_inventory(root)
        if errs:
            print(errs[0], file=sys.stderr)
            print("CALL_TREE:NOT_MET")
            return 1
        print("CALL_TREE:MET")
        return 0
    parser.print_help()
    return 2


