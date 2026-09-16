#!/usr/bin/env python3
"""R32: tainted values do not leave the consuming unit.

Same-file and other files under goals/adapters/workflows: a helper that
returns taint taints its callers. Nested imports that call that helper
name are followed when the helper is in the scan root.

Out of reach: helpers outside the scan root / third-party packages.
"""


from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EXTS = {".ts", ".js", ".py", ".mjs", ".cjs", ".tsx", ".jsx"}
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
OUTSIDE_DIR_NAMES = ("goals", "workflows", "adapters")
IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
DEF = re.compile(rf"^(\s*)def\s+({IDENT})\s*\([^)]*\)\s*(?:->[^:]*)?:\s*$")
ASSIGN = re.compile(rf"^(\s*)({IDENT})\s*=(?!=)\s*(.+)$")
GET_CALL = re.compile(r"\.(?:get_|read_|export_)[A-Za-z0-9_]*\s*\(")

RETURN = re.compile(r"\breturn\b(.*)$")
STORE = re.compile(rf"(?:this|{IDENT})\s*\.\s*{IDENT}\s*=(?!=)\s*(.+)$")
CALL = re.compile(rf"\b({IDENT})\s*\((.*)\)")
SKIP_CALLEES = {"print", "len", "str", "int", "list", "dict", "set", "range"}


def is_skipped_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def is_test(path: Path) -> bool:
    return (
        "tests" in path.parts
        or path.name.startswith("test_")
        or path.name.endswith("_test.py")
    )


def source_files(tree: Path) -> list[Path]:
    if not tree.is_dir():
        return []
    return sorted(
        p for p in tree.rglob("*")
        if p.is_file()
        and p.suffix in SOURCE_EXTS
        and not is_skipped_dir(p)
        and not is_test(p)
    )


def noun_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    domain = root / "domain"
    if domain.is_dir():
        found.extend(sorted(p for p in domain.iterdir() if p.is_dir()))
    examples = root / "examples"
    if examples.is_dir():
        for domain_dir in sorted(examples.rglob("domain")):
            if domain_dir.is_dir() and domain_dir.name == "domain" and not is_skipped_dir(domain_dir):
                found.extend(sorted(p for p in domain_dir.iterdir() if p.is_dir()))
    return found


def outside_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in OUTSIDE_DIR_NAMES:
        files.extend(source_files(root / name))
    examples = root / "examples"
    if examples.is_dir():
        for path in examples.rglob("*"):
            if path.is_dir() and path.name in OUTSIDE_DIR_NAMES and not is_skipped_dir(path):
                files.extend(source_files(path))
    return sorted(set(files))


def load_list(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    names = set()
    for line in path.read_text().splitlines():
        raw = line.strip()
        if raw and not raw.startswith("#"):
            names.add(raw)
    return names


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def is_comment(line: str) -> bool:
    s = line.strip()
    return s.startswith("#") or s.startswith("//")


def functions(text: str) -> list[tuple[str, int, list[str]]]:
    lines = text.splitlines()
    found: list[tuple[str, int, list[str]]] = []
    i = 0
    while i < len(lines):
        m = DEF.match(lines[i])
        if not m:
            i += 1
            continue
        indent, name = m.group(1), m.group(2)
        start = i + 1
        body: list[str] = []
        i += 1
        while i < len(lines):
            raw = lines[i]
            if raw.strip() == "":
                body.append(raw)
                i += 1
                continue
            if raw.startswith(indent + "    ") or raw.startswith(indent + "\t"):
                body.append(raw)
                i += 1
                continue
            break
        found.append((name, start, body))
    return found


def names_in(expr: str) -> set[str]:
    return set(re.findall(rf"\b({IDENT})\b", expr))


def tainted_from(expr: str, tainted: set[str]) -> bool:
    if GET_CALL.search(expr):
        return True
    return bool(names_in(expr) & tainted)


def scan_function(path: str, start: int, body: list[str], tokens: set[str], taint_fns: set[str]) -> list[tuple[str, int, str]]:
    tainted: set[str] = set(tokens)

    def from_expr(expr: str) -> bool:
        if GET_CALL.search(expr):
            return True
        if any(re.search(rf"\b{re.escape(fn)}\s*\(", expr) for fn in taint_fns):
            return True
        return bool(names_in(expr) & tainted)

    changed = True
    while changed:
        changed = False
        for line in body:
            stripped = line.strip()
            if is_comment(stripped):
                continue
            m = ASSIGN.match(line.rstrip())
            if not m:
                continue
            lhs, rhs = m.group(2), m.group(3)
            if lhs not in tainted and from_expr(rhs):
                tainted.add(lhs)
                changed = True

    violations: list[tuple[str, int, str]] = []
    for offset, line in enumerate(body):
        lineno = start + offset
        stripped = line.strip()
        if is_comment(stripped) or not stripped:
            continue
        ret = RETURN.search(stripped)
        if ret and from_expr(ret.group(1)):
            leaked = (names_in(ret.group(1)) & tainted) or {"get"}
            violations.append((path, lineno, f"return-taint:{next(iter(leaked))}"))
            continue
        store = STORE.search(stripped)
        if store and from_expr(store.group(1)):
            leaked = (names_in(store.group(1)) & tainted) or {"get"}
            violations.append((path, lineno, f"store-taint:{next(iter(leaked))}"))
            continue
        call = CALL.search(stripped)
        if call:
            callee, args = call.group(1), call.group(2)
            if callee in SKIP_CALLEES:
                continue
            if GET_CALL.search(stripped) and "=" not in stripped.split("(")[0]:
                continue
            leaked = names_in(args) & tainted
            if leaked:
                violations.append((path, lineno, f"pass-taint:{next(iter(leaked))}"))
    return violations


def function_returns_taint(body: list[str], tokens: set[str], taint_fns: set[str]) -> bool:
    tainted: set[str] = set(tokens)
    changed = True
    while changed:
        changed = False
        for line in body:
            if is_comment(line.strip()):
                continue
            m = ASSIGN.match(line.rstrip())
            if not m:
                continue
            lhs, rhs = m.group(2), m.group(3)
            hit = bool(GET_CALL.search(rhs) or (names_in(rhs) & tainted))
            if not hit:
                hit = any(re.search(rf"\b{re.escape(fn)}\s*\(", rhs) for fn in taint_fns)
            if lhs not in tainted and hit:
                tainted.add(lhs)
                changed = True
    for line in body:
        ret = RETURN.search(line.strip())
        if not ret:
            continue
        expr = ret.group(1)
        if GET_CALL.search(expr) or (names_in(expr) & tainted):
            return True
        if any(re.search(rf"\b{re.escape(fn)}\s*\(", expr) for fn in taint_fns):
            return True
    return False


def scan_one(scan_root: Path) -> list[tuple[str, int, str]]:
    tokens: set[str] = set()
    for noun_dir in noun_dirs(scan_root):
        tokens |= load_list(noun_dir / "taint.txt")
    if not tokens:
        return []
    files = []
    for path in outside_files(scan_root):
        text = path.read_text(errors="replace")
        files.append((path, text, functions(text)))
    taint_fns: set[str] = set()
    changed = True
    while changed:
        changed = False
        for _path, _text, fns in files:
            for name, _start, body in fns:
                if name in taint_fns:
                    continue
                if function_returns_taint(body, tokens, taint_fns):
                    taint_fns.add(name)
                    changed = True
    violations: list[tuple[str, int, str]] = []
    for path, _text, fns in files:
        for name, start, body in fns:
            violations.extend(scan_function(rel(path), start, body, tokens, taint_fns))
    return violations



def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, int, str]] = set()
    printed = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, lineno, kind = item
            print(f"VIOLATION {path}:{lineno} {kind}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
