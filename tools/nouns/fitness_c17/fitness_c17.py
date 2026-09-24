#!/usr/bin/env python3
"""C17: each verb has success, precondition failure, and adjective preservation.


For each verb in verbs.schema.json:
  untested-verb            — name never appears in noun tests
  verb-no-failure-test     — no test that names the verb and assertRaises/raises
  verb-no-preservation-test — no non-raises test that names the verb, an
                              adjective token, and an assert

No adjectives.txt → preservation skipped (nothing to preserve).
Does not execute the tests; CI does.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <noun> <kind> <verb>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
SOURCE_EXTS = {".py", ".ts", ".js"}
RAISES = re.compile(r"assertRaises|pytest\.raises|\braises\s*\(")
ASSERT = re.compile(r"\bassert(Equal|NotEqual|True|False)?\b|\b==\b")
TEST_FN = re.compile(
    r"^(\s*)def\s+(test_[A-Za-z0-9_]+)\s*\([^)]*\)\s*(?:->[^:]*)?:\s*$"
)


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def noun_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    domain = root / "domain"
    if domain.is_dir():
        found.extend(p for p in domain.iterdir() if p.is_dir())
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob("domain"):
            if named.is_dir() and named.name == "domain" and not is_skipped(named):
                found.extend(p for p in named.iterdir() if p.is_dir())
    return sorted(set(found))


def verb_names(noun: Path) -> list[str]:
    schema = noun / "schemas" / "verbs.schema.json"
    if not schema.is_file():
        return []
    try:
        data = json.loads(schema.read_text())
    except json.JSONDecodeError:
        return []
    verbs = data.get("verbs")
    if not isinstance(verbs, dict):
        return []
    return [str(k) for k in verbs.keys()]


def adjectives(noun: Path) -> set[str]:
    path = noun / "adjectives.txt"
    if not path.is_file():
        return set()
    names = set()
    for raw in path.read_text(errors="replace").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            names.add(line)
    return names


def test_files(noun: Path) -> list[Path]:
    files: list[Path] = []
    tests = noun / "tests"
    if tests.is_dir():
        files.extend(
            p for p in tests.rglob("*")
            if p.is_file() and p.suffix in SOURCE_EXTS
        )
    files.extend(
        p for p in noun.iterdir()
        if p.is_file()
        and p.suffix in SOURCE_EXTS
        and (p.name.startswith("test_") or p.name.endswith("_test.py"))
    )
    return files


def test_functions(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    found: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        m = TEST_FN.match(lines[i])
        if not m:
            i += 1
            continue
        indent, name = m.group(1), m.group(2)
        body: list[str] = []
        i += 1
        while i < len(lines):
            raw = lines[i]
            if raw.strip() == "":
                i += 1
                continue
            if raw.startswith(indent + "    ") or raw.startswith(indent + "\t"):
                body.append(raw)
                i += 1
                continue
            break
        found.append((name, "\n".join(body)))
    return found


def names_adj(body: str, tokens: set[str]) -> bool:
    for tok in tokens:
        if re.search(rf"['\"]{re.escape(tok)}['\"]", body) or re.search(
            rf"\b{re.escape(tok)}\b", body
        ):
            return True
    return False


def scan_one(scan_root: Path) -> list[tuple[str, str, str]]:
    violations: list[tuple[str, str, str]] = []
    for noun in noun_dirs(scan_root):
        names = verb_names(noun)
        if not names:
            continue
        adjs = adjectives(noun)
        fns: list[tuple[str, str]] = []
        blob_parts: list[str] = []
        for path in test_files(noun):
            text = path.read_text(errors="replace")
            blob_parts.append(text)
            fns.extend(test_functions(text))
        blob = "\n".join(blob_parts)
        for name in names:
            if re.search(rf"\b{re.escape(name)}\b", blob) is None:
                violations.append((rel(noun), "untested-verb", name))
                continue
            has_failure = False
            has_preserve = False
            for _tname, body in fns:
                if re.search(rf"\b{re.escape(name)}\b", body) is None:
                    continue
                if RAISES.search(body):
                    has_failure = True
                    continue
                if adjs and names_adj(body, adjs) and ASSERT.search(body):
                    has_preserve = True
            if not has_failure:
                violations.append((rel(noun), "verb-no-failure-test", name))
            if adjs and not has_preserve:
                violations.append((rel(noun), "verb-no-preservation-test", name))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen = set()
    printed = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            noun, kind, name = item
            print(f"VIOLATION {noun} {kind} {name}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
