"""C4: no ci_fitness-wired tool grades another fitness/assert tool's source or logic."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CI_FITNESS = ROOT / "tools" / "nouns" / "ci_fitness" / "ci_fitness.py"
KNOWN_BAD = ROOT / "tools/fixtures/no-check-on-check/mutate-fitness-landmine.py"
_WRITE = {"write_text", "write_bytes"}
_TOOL_SUBJECT = re.compile(
    r"(tools/fitness-[^\"']+\.py|tools/assert-[^\"']+\.py|"
    r"tools/nouns/fitness_[^\"']+|tools/nouns/assert_[^\"']+|"
    r"tools/nouns/ci_fitness/[^\"']+)"
)
_ALLOWED_VERIFY_ON_CANDIDATE = (
    "assert-gate-set-closure-member-tamper-fails.py",
    "assert-gate-set-manifest-tamper-fails.py",
    "assert-gate-set-manifest-missing-sidecar-fails.py",
    "assert-gate-set-manifest-placeholder-sidecar-fails.py",
    "fitness-owner-ratification-known-bad.py",
    "fitness-known-bad-ssot.py",
    "fitness-no-check-on-check.py",
)


def _string_constants(node: ast.AST) -> list[str]:
    out: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            out.append(child.value)
    return out


def check_on_check_errors_for_source(rel: str, source: str) -> list[str]:
    """Return NOT_MET reasons when source mutates or re-grades another fitness/assert tool."""
    errors: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"{rel}: syntax error {exc}"]
    assigned: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for const in _string_constants(node.value):
                match = _TOOL_SUBJECT.search(const)
                if match:
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            assigned[target.id] = match.group(1)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = ""
        receiver: ast.AST | None = None
        if isinstance(func, ast.Attribute):
            name = func.attr
            receiver = func.value
        elif isinstance(func, ast.Name):
            name = func.id
        strings = _string_constants(node)
        if receiver is not None:
            strings.extend(_string_constants(receiver))
            if isinstance(receiver, ast.Name) and receiver.id in assigned:
                strings.append(assigned[receiver.id])
        joined = " ".join(strings)
        if name in _WRITE or (
            name == "open" and any(flag in strings for flag in ("w", "wt", "wb", "a", "at"))
        ):
            match = _TOOL_SUBJECT.search(joined)
            if match:
                errors.append(
                    f"{rel}: mutates fitness/assert tool source {match.group(1)} "
                    "(check-on-check / mutation landmine)"
                )
    return errors


def wired_tool_relpaths(root: Path) -> list[str]:
    """Every tool ci_fitness invokes (explicit run + designed-fail glob + invoice-correct glob)."""
    rels: set[str] = set()
    text = (root / "tools/nouns/ci_fitness/ci_fitness.py").read_text(encoding="utf-8")
    for match in re.finditer(r"TOOLS\s*/\s*[\"']([^\"']+\.py)[\"']", text):
        rels.add("tools/" + match.group(1))
    tools_dir = root / "tools"
    for path in tools_dir.glob("assert-*-fails.py"):
        rels.add("tools/" + path.name)
    for path in tools_dir.glob("fitness-*.py"):
        rels.add("tools/" + path.name)
    return sorted(rels)


def check_on_check_errors(root: Path, tool_rels: list[str] | None = None) -> list[str]:
    errors: list[str] = []
    rels = tool_rels if tool_rels is not None else wired_tool_relpaths(root)
    for rel in rels:
        path = root / rel
        if not path.is_file():
            continue
        if path.name in _ALLOWED_VERIFY_ON_CANDIDATE:
            # Allowed: constraint verify on a known-bad Candidate, including gate-set member bytes.
            continue
        errors.extend(check_on_check_errors_for_source(rel, path.read_text(encoding="utf-8")))
    return errors


def main() -> int:
    errors = check_on_check_errors(ROOT)
    if not KNOWN_BAD.is_file():
        errors.append(f"missing known-bad {KNOWN_BAD.relative_to(ROOT)}")
    else:
        kb = check_on_check_errors_for_source(
            "tools/fixtures/no-check-on-check/mutate-fitness-landmine.py",
            KNOWN_BAD.read_text(encoding="utf-8"),
        )
        if not kb:
            errors.append("known-bad mutate-fitness-landmine.py: expected NOT_MET got MET")
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
