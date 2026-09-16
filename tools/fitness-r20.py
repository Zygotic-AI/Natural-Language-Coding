#!/usr/bin/env python3
"""R20: verbs.schema.json required fields are named and typed in the verb.

Every input.required name must appear in that method's signature or body
and be annotated. If the schema gives a JSON type, it must match
(integer→int, string→str, boolean→bool, number→int|float).
"""


from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
DEF = re.compile(rf"^(\s*)def\s+({IDENT})\s*\((.*)\)\s*(?:->[^:]*)?:\s*$")
JSON_TO_PY = {
    "integer": {"int"},
    "string": {"str"},
    "boolean": {"bool"},
    "number": {"int", "float"},
}


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


def methods(text: str) -> dict[str, tuple[str, str]]:
    """name -> (signature_inside_parens, body)."""
    lines = text.splitlines()
    found: dict[str, tuple[str, str]] = {}
    i = 0
    while i < len(lines):
        m = DEF.match(lines[i])
        if not m:
            i += 1
            continue
        indent, name, sig = m.group(1), m.group(2), m.group(3)
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
        found[name] = (sig, "\n".join(body))
    return found


def annotation(sig: str, field: str) -> str | None:
    m = re.search(rf"\b{re.escape(field)}\s*:\s*({IDENT})", sig)
    return m.group(1) if m else None


def json_type(spec: dict, field: str) -> str | None:
    inp = spec.get("input")
    if not isinstance(inp, dict):
        return None
    props = inp.get("properties")
    if not isinstance(props, dict):
        return None
    node = props.get(field)
    if not isinstance(node, dict):
        return None
    t = node.get("type")
    return t if isinstance(t, str) else None


def scan_one(scan_root: Path) -> list[tuple[str, str, str, str]]:
    violations: list[tuple[str, str, str, str]] = []
    for noun in noun_dirs(scan_root):
        schema = noun / "schemas" / "verbs.schema.json"
        if not schema.is_file():
            continue
        try:
            data = json.loads(schema.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        verbs = data.get("verbs") if isinstance(data, dict) else None
        if not isinstance(verbs, dict):
            continue
        blob = ""
        for py in noun.glob("*.py"):
            if py.name.startswith("test_") or py.name.endswith("_test.py"):
                continue
            blob += py.read_text(errors="replace") + "\n"
        defs = methods(blob)
        for vname, spec in verbs.items():
            if not isinstance(spec, dict):
                continue
            inp = spec.get("input")
            required = inp.get("required") if isinstance(inp, dict) else None
            if not isinstance(required, list):
                continue
            sig, body = defs.get(vname, ("", ""))
            hay = sig + "\n" + body
            for field in required:
                if not isinstance(field, str):
                    continue
                if re.search(rf"\b{re.escape(field)}\b", hay) is None:
                    violations.append((rel(noun), vname, "missing-field", field))
                    continue
                ann = annotation(sig, field)
                if not ann:
                    violations.append((rel(noun), vname, "missing-annotation", field))
                    continue
                jt = json_type(spec, field)
                if jt in JSON_TO_PY and ann not in JSON_TO_PY[jt]:
                    violations.append((rel(noun), vname, "type-mismatch", field))

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
            noun, verb, kind, field = item
            print(f"VIOLATION {noun} {verb} {kind} {field}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
