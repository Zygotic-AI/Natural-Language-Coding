"""Change set for C7/C8/C11 v2: CONFIRM CHANGED: list, else git, else all.

None means tree-wide (no list, no dirty git). A non-empty set means only
those paths (and their parent units) are in scope.
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


def git_changed(repo: Path) -> list[str]:
    cmds = (
        ["git", "-C", str(repo), "diff", "--name-only"],
        ["git", "-C", str(repo), "diff", "--cached", "--name-only"],
    )
    names: list[str] = []
    for cmd in cmds:
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        except (OSError, subprocess.CalledProcessError):
            continue
        for line in out.splitlines():
            line = line.strip().replace("\\", "/")
            if line:
                names.append(line)
    return names


def changed_paths(scan_root: Path, repo_root: Path) -> set[str] | None:
    listed: list[str] = []
    for name in NOTES:
        path = scan_root / name
        if path.is_file():
            listed.extend(parse_changed_list(path.read_text(errors="replace")))
    dirty = git_changed(repo_root)
    scoped: list[str] = []
    scan_rel = ""
    try:
        scan_rel = scan_root.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        scan_rel = ""
    for d in dirty:
        if not scan_rel or d == scan_rel or d.startswith(scan_rel + "/"):
            scoped.append(d)
            if scan_rel and d.startswith(scan_rel + "/"):
                scoped.append(d[len(scan_rel) + 1 :])
    if listed:
        return set(listed)
    if scoped:
        return set(scoped)
    return None



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
            if parent in {r, "."}:
                if parent == r:
                    return True
            if parent.startswith(r + "/"):
                return True
    return False
