"""Classify every executable file into one Boundary-Based Programming shape."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

KERNEL_MARK = "tools/nouns/executable_shape/"
EXECUTABLE_KINDS = (
    "python",
    "shell",
    "workflow",
    "test",
    "fixture",
    "generated",
    "template",
    "migration",
    "vendored",
    "configuration",
)
CLASSES = (
    "noun implementation",
    "goal",
    "primitive adapter",
    "thin entrypoint",
    "contained fixture",
)
CONFORMING_EXAMPLES = frozenset(
    {
        "action-plan-ok",
        "adopter-verify-fast-green",
        "agent-ratified",
        "call-tree-pack-reference",
        "changed-only-ok",
        "durable-engine-strict-ok",
        "emit-from-prose",
        "emit-manifest-ok",
        "invoice-correct",
        "non-python-with-adapter",
        "pipeline-wire-ok",
        "rca-packet-ok",
        "retrying-goal",
        "retrying-nested-ok",
        "reverse-audit-ok",
        "rule-coverage-minimal",
        "rule-marker-domain",
        "rule-semantic-apply-must-ok",
        "rule-semantic-pan-forbid-return-ok",
    }
)
_FUNC = re.compile(r"^(?:function\s+\w+|\w+\s*\(\))\s*\{?\s*$")
_SKIP = {".git", "__pycache__", ".venv", "venv", "node_modules", "dist"}


def exemption_violations(exempt: list[str]) -> list[str]:
    """The kernel cannot exempt its own files."""
    bad: list[str] = []
    for item in exempt:
        norm = item.replace("\\", "/")
        if KERNEL_MARK in norm or norm.endswith("executable_shape.py"):
            bad.append(norm)
    return bad


def _kind(rel: str) -> str:
    if rel.startswith("templates/"):
        return "template"
    if rel.startswith("migrations/"):
        return "migration"
    if rel.startswith(".github/workflows/"):
        return "workflow"
    if rel.startswith(".cursor/"):
        return "configuration"
    if "/tests/" in rel or rel.rsplit("/", 1)[-1].startswith("test_"):
        return "test"
    if rel.startswith("examples/") or rel.startswith("reviews/"):
        return "fixture"
    if rel.endswith(".py"):
        return "python"
    if rel.endswith((".sh", ".bash", ".ps1", ".cmd")) or rel in {"nlc", "release"}:
        return "shell"
    return "configuration"


def _shell_defines_function(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if _FUNC.match(stripped):
            return True
    return False


def _thin_shell(text: str) -> bool:
    if _shell_defines_function(text):
        return False
    lowered = text.lower()
    return (
        "exec " in text
        or "execute.sh" in text
        or "execute.ps1" in text
        or "python" in lowered
        or lowered.lstrip().startswith("@echo")
    )


def classify(rel: str, text: str) -> str | None:
    """Return one shape class, or None when the file is unclassified."""
    if rel.startswith("staging/"):
        return "contained fixture"
    if rel.startswith("reviews/"):
        return "contained fixture"
    if rel.startswith("examples/"):
        parts = rel.split("/")
        specimen = parts[1] if len(parts) > 1 else ""
        if specimen not in CONFORMING_EXAMPLES:
            return "contained fixture"
        if "/goals/" in rel:
            return "goal"
        return "noun implementation"
    if rel.startswith("goals/"):
        return "goal"
    if rel.startswith("tools/nouns/"):
        return "noun implementation"
    if rel.startswith("migrations/"):
        return "noun implementation"
    if rel.startswith(".github/workflows/"):
        return "goal"
    if rel.startswith("templates/"):
        return "thin entrypoint"
    if rel == ".cursor/hooks.json":
        return "thin entrypoint"
    if rel.startswith(".cursor/hooks/"):
        if "case " in text:
            return "goal"
        return "thin entrypoint"
    if rel.startswith("tools/fixtures/"):
        return "contained fixture"
    if rel.startswith("tools/") and rel.endswith(".py"):
        if "from nouns." in text and len(text) < 2500:
            return "primitive adapter"
        return None
    if rel.endswith((".sh", ".bash", ".ps1", ".cmd")) or rel in {"nlc", "release", "templates/adopter/nlc"}:
        if _thin_shell(text):
            return "thin entrypoint"
        return None
    return None


def iter_executable_files(root: Path) -> list[Path]:
    found: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in _SKIP for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix in {".py", ".sh", ".bash", ".ps1", ".cmd"}:
            found.append(path)
            continue
        if rel in {"nlc", "release", "templates/adopter/nlc", ".cursor/hooks.json"}:
            found.append(path)
            continue
        if rel.startswith(".github/workflows/") and path.suffix in {".yml", ".yaml"}:
            found.append(path)
            continue
        if rel.startswith("migrations/") and path.suffix in {".yaml", ".yml"}:
            found.append(path)
            continue
        if rel.startswith("templates/") and path.suffix in {".yml", ".yaml"}:
            found.append(path)
    return sorted(found)


def inventory(root: Path) -> tuple[dict[str, str], list[str]]:
    if exemption_violations([]):
        raise RuntimeError("kernel exemption list is not empty")
    classified: dict[str, str] = {}
    unclassified: list[str] = []
    for path in iter_executable_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        kind = _kind(rel)
        if kind not in EXECUTABLE_KINDS:
            unclassified.append(rel)
            continue
        label = classify(rel, text)
        if label not in CLASSES:
            unclassified.append(rel)
            continue
        classified[rel] = label
    return classified, unclassified


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    _classified, unclassified = inventory(root)
    print(f"UNCLASSIFIED:{len(unclassified)}")
    for rel in unclassified:
        print(f"UNCLASSIFIED {rel}")
    if unclassified:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
