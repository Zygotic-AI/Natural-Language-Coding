"""C8: no tracked tool writes *.approval.asc or sets ratified/pending registry state."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KNOWN_BAD = ROOT / "tools/fixtures/no-tool-writes-ratification/write-approval-asc.py"
_WRITE = {"write_text", "write_bytes"}
_RATIFIED_KEYS = frozenset({"ratified", "pending", "ratification_state"})


def _string_constants(node: ast.AST) -> list[str]:
    out: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            out.append(child.value)
    return out


def ratification_write_errors_for_source(rel: str, source: str) -> list[str]:
    """NOT_MET when source writes a sidecar or sets ratified/pending registry state."""
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"{rel}: syntax error {exc}"]
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = ""
        if isinstance(func, ast.Attribute):
            name = func.attr
        elif isinstance(func, ast.Name):
            name = func.id
        strings = _string_constants(node)
        if name in _WRITE or (
            name == "open" and any(flag in strings for flag in ("w", "wt", "wb", "a", "at"))
        ):
            for item in strings:
                if item.endswith(".approval.asc") or item.endswith("approval.asc"):
                    errors.append(f"{rel}: writes ratification sidecar {item}")
        if name in {"__setitem__", "update"} or name in _WRITE:
            for item in strings:
                if item in _RATIFIED_KEYS:
                    errors.append(f"{rel}: sets {item} registry state")
    return errors


def tracked_tool_rels(root: Path) -> list[str]:
    rels: list[str] = []
    tools = root / "tools"
    if not tools.is_dir():
        return rels
    for path in tools.rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        if "/fixtures/" in rel or rel.startswith("tools/fixtures/"):
            continue
        rels.append(rel)
    return sorted(rels)


def ratification_write_errors(root: Path, tool_rels: list[str] | None = None) -> list[str]:
    errors: list[str] = []
    rels = tool_rels if tool_rels is not None else tracked_tool_rels(root)
    for rel in rels:
        path = root / rel
        if not path.is_file():
            continue
        errors.extend(ratification_write_errors_for_source(rel, path.read_text(encoding="utf-8")))
    return errors


def main() -> int:
    errors = ratification_write_errors(ROOT)
    if not KNOWN_BAD.is_file():
        errors.append(f"missing known-bad {KNOWN_BAD.relative_to(ROOT)}")
    else:
        kb = ratification_write_errors_for_source(
            "tools/fixtures/no-tool-writes-ratification/write-approval-asc.py",
            KNOWN_BAD.read_text(encoding="utf-8"),
        )
        if not kb:
            errors.append("known-bad write-approval-asc.py: expected NOT_MET got MET")
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
