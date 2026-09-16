"""Change set: CONFIRM CHANGED: list, else dirty git, else origin/main...HEAD.

None means tree-wide (no list, no diff). A non-empty set means only those
paths (and their parent units) are in scope.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

NOTES = ("CONFIRM.md", "PROPOSAL.md")
CHANGED_HEAD = re.compile(r"^CHANGED:\s*$", re.I | re.M)
BULLET = re.compile(r"^\s*[-*]\s+(\S+)\s*$")


def parse_changed_list(text: str) -> list[str]:
    m = CHANGED_HEAD.search(text)
    if m is None:
        return []
    rest = text[m.end() :]
    paths: list[str] = []
    for line in rest.splitlines():
        if not line.strip():
            if paths:
                break
            continue
        b = BULLET.match(line)
        if b is None:
            break
        paths.append(b.group(1).replace("\\", "/").lstrip("./"))
    return paths


def _git_names(repo: Path, args: list[str]) -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(repo), *args],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    names: list[str] = []
    for line in out.splitlines():
        line = line.strip().replace("\\", "/")
        if line:
            names.append(line)
    return names


def git_changed(repo: Path) -> list[str]:
    return _git_names(repo, ["diff", "--name-only"]) + _git_names(
        repo, ["diff", "--cached", "--name-only"]
    )


def git_pr_changed(repo: Path) -> list[str]:
    for base in ("origin/main", "origin/master", "main"):
        names = _git_names(repo, ["diff", "--name-only", f"{base}...HEAD"])
        if names:
            return names
    return []


def _scope(names: list[str], scan_root: Path, repo_root: Path) -> list[str]:
    scoped: list[str] = []
    scan_rel = ""
    try:
        scan_rel = scan_root.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        scan_rel = ""
    for d in names:
        if not scan_rel or d == scan_rel or d.startswith(scan_rel + "/"):
            scoped.append(d)
            if scan_rel and d.startswith(scan_rel + "/"):
                scoped.append(d[len(scan_rel) + 1 :])
    return scoped


def changed_paths(scan_root: Path, repo_root: Path) -> set[str] | None:
    listed: list[str] = []
    for name in NOTES:
        path = scan_root / name
        if path.is_file():
            listed.extend(parse_changed_list(path.read_text(errors="replace")))
    if listed:
        return set(listed)
    scoped = _scope(git_changed(repo_root), scan_root, repo_root)
    if scoped:
        return set(scoped)
    scoped = _scope(git_pr_changed(repo_root), scan_root, repo_root)
    if scoped:
        return set(scoped)
    return None


def is_charter_path(path: str) -> bool:
    n = path.replace("\\", "/")
    return n.endswith("CHARTER.md") or "/adrs/" in f"/{n}" or n.startswith("adrs/")


def is_code_path(path: str) -> bool:
    n = path.replace("\\", "/")
    return (
        "/goals/" in f"/{n}"
        or "/domain/" in f"/{n}"
        or n.endswith(".schema.json")
        or n.startswith("goals/")
        or n.startswith("domain/")
    )


def unit_touched(unit: Path, changed: set[str], scan_root: Path, repo_root: Path) -> bool:
    rels: set[str] = set()
    try:
        rels.add(unit.resolve().relative_to(scan_root.resolve()).as_posix())
    except ValueError:
        pass
    try:
        rels.add(unit.resolve().relative_to(repo_root.resolve()).as_posix())
    except ValueError:
        pass
    rels.add(unit.as_posix())
    for c in changed:
        cn = c.replace("\\", "/").lstrip("./")
        for r in rels:
            if not r:
                continue
            if cn == r or cn.startswith(r + "/") or r.startswith(cn.rstrip("/") + "/"):
                return True
            parent = str(Path(cn).parent).replace("\\", "/")
            if parent == r or parent.startswith(r + "/"):
                return True
    return False
