#!/usr/bin/env python3
"""C15: retrying goals call an idempotent verb that *honors* a key.


If a goal .py contains retry/temporalio/durable/`for attempt in`:
  missing-idempotent      — verb lacks `"idempotent": true`
  missing-key-in-schema   — schema does not declare idempotency_key
  missing-idempotency-key — call site does not pass that key by name
                            (nested parens are parsed)
  key-unused              — verb method never uses the key in its body

No retry marker → skip (MET).

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <goal> <kind> <verb>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}
RETRY = re.compile(r"\b(retry|temporalio|durable)\b|for\s+attempt\s+in", re.I)
CALL_START = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\.([A-Za-z_][A-Za-z0-9_]*)\s*\(")
DEF = re.compile(r"^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)\s*(?:->[^:]*)?:\s*$")
SKIP_VERBS = {"print", "append", "get", "set", "update"}
KEY_NAMES = ("idempotency_key", "idempotent_key")
KEY_ARG = re.compile(r"\b(idempotency_key|idempotent_key)\s*=")
KEY_WORD = re.compile(r"\b(idempotency_key|idempotent_key)\b")


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def collect(root: Path, name: str) -> list[Path]:
    found: list[Path] = []
    direct = root / name
    if direct.is_dir():
        found.append(direct)
    examples = root / "examples"
    if examples.is_dir():
        for p in examples.rglob(name):
            if p.is_dir() and p.name == name and not is_skipped(p):
                found.append(p)
    return found


def verb_specs(root: Path) -> dict[str, dict]:
    specs: dict[str, dict] = {}
    for domain in collect(root, "domain"):
        for schema in domain.rglob("verbs.schema.json"):
            try:
                data = json.loads(schema.read_text())
            except (OSError, json.JSONDecodeError):
                continue
            verbs = data.get("verbs") if isinstance(data, dict) else None
            if not isinstance(verbs, dict):
                continue
            for key, spec in verbs.items():
                if isinstance(spec, dict):
                    specs[str(key)] = spec
    return specs


def schema_has_key(spec: dict) -> bool:
    inp = spec.get("input")
    if not isinstance(inp, dict):
        return False
    required = inp.get("required") or []
    props = inp.get("properties") or {}
    for name in KEY_NAMES:
        if name in required or name in props:
            return True
    return spec.get("idempotency_key") is True


def methods_in(text: str) -> dict[str, str]:
    lines = text.splitlines()
    found: dict[str, str] = {}
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
        found[name] = sig + "\n" + "\n".join(body)
    return found


def verb_bodies(root: Path) -> dict[str, str]:
    bodies: dict[str, str] = {}
    for domain in collect(root, "domain"):
        for py in domain.rglob("*.py"):
            if is_skipped(py) or "tests" in py.parts or py.name.startswith("test_"):
                continue
            bodies.update(methods_in(py.read_text(errors="replace")))
    return bodies


def verb_honors_key(body: str) -> bool:
    """True if the key appears in the body, not only as a parameter name."""
    lines = body.splitlines()
    if not lines:
        return False
    sig = lines[0]
    rest = "\n".join(lines[1:])
    return KEY_WORD.search(rest) is not None or (
        KEY_WORD.search(sig) is not None and KEY_WORD.search(rest) is not None
    )


def extract_calls(text: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for m in CALL_START.finditer(text):
        start = m.end()
        depth = 1
        i = start
        while i < len(text) and depth:
            ch = text[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            i += 1
        args = text[start : i - 1] if depth == 0 else text[start:]
        found.append((m.group(1), args))
    return found


def goal_py(root: Path) -> list[Path]:
    files: list[Path] = []
    for goals in collect(root, "goals"):
        files.extend(
            p for p in goals.rglob("*.py")
            if p.is_file() and not is_skipped(p) and "tests" not in p.parts
        )
    return files


def scan_one(scan_root: Path) -> list[tuple[str, str, str]]:
    specs = verb_specs(scan_root)
    bodies = verb_bodies(scan_root)
    violations: list[tuple[str, str, str]] = []
    for path in goal_py(scan_root):
        text = path.read_text(errors="replace")
        body = "\n".join(
            ln for ln in text.splitlines() if not ln.strip().startswith("#")
        )
        if RETRY.search(body) is None:
            continue
        for verb, args in extract_calls(body):
            if verb in SKIP_VERBS:
                continue
            spec = specs.get(verb)
            if not isinstance(spec, dict) or spec.get("idempotent") is not True:
                violations.append((rel(path), "missing-idempotent", verb))
                continue
            if not schema_has_key(spec):
                violations.append((rel(path), "missing-key-in-schema", verb))
            if KEY_ARG.search(args) is None:
                violations.append((rel(path), "missing-idempotency-key", verb))
                continue
            impl = bodies.get(verb, "")
            if not verb_honors_key(impl):
                violations.append((rel(path), "key-unused", verb))
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
            path, kind, verb = item
            print(f"VIOLATION {path} {kind} {verb}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
