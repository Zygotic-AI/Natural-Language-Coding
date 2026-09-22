"""ADR 0010: declare Planit-generated artifacts that require gate receipts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nlc_requirements import hub_tool

SCOPE_FILE = "gate-scope.json"


def _norm_rel(artifact: str) -> str:
    rel = artifact.replace("\\", "/").strip()
    if rel.startswith("./"):
        rel = rel[2:]
    return rel


def load_scope_paths(root: Path) -> list[str]:
    path = root / ".nlc" / SCOPE_FILE
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    raw = data.get("artifacts") or []
    out: list[str] = []
    for item in raw:
        rel = _norm_rel(str(item))
        if rel:
            out.append(rel)
    return sorted(set(out))


def add_scope_path(root: Path, artifact: str) -> None:
    rel = _norm_rel(artifact)
    if not rel:
        raise ValueError("artifact path is required")
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    path = nlc / SCOPE_FILE
    paths = load_scope_paths(root)
    if rel not in paths:
        paths.append(rel)
        paths.sort()
    path.write_text(
        json.dumps({"schema": 1, "artifacts": paths}, indent=2) + "\n",
        encoding="utf-8",
    )


def scoped_artifact_paths(root: Path) -> list[Path]:
    """Paths listed in gate-scope that exist on disk (adopter / verify landmines only)."""
    from nlc_pipeline import is_hub_repo

    if is_hub_repo(root):
        return []
    out: list[Path] = []
    for rel in load_scope_paths(root):
        candidate = root / rel
        if candidate.is_file():
            out.append(candidate)
    return out


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Declare ADR 0010 gate-scoped artifacts")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--add", dest="artifact", help="Repo-relative artifact path")
    parser.add_argument("--list", action="store_true", help="Print scoped paths")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.list:
        for rel in load_scope_paths(root):
            print(rel)
        return 0
    if not args.artifact:
        print("gate-scope needs --add <path> or --list", file=sys.stderr)
        return 2
    try:
        add_scope_path(root, args.artifact)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"gate-scope: MET artifact={args.artifact}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
