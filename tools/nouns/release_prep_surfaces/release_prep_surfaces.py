"""Deterministic release-prep writer for FINDINGS, DESCRIBE, and the hub record."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS_REL = "FINDINGS.md"
DESCRIBE_REL = "DESCRIBE.md"
RECORD_REL = "integrity/hub-release-record.json"
VERSION_REL = "integrity/nlc-version.json"
CONTENT_TREE_REF = "integrity/hub-content-tree-hash.txt"

_SHIPPED_GIT_TAG = re.compile(
    r"(Shipped git tag\s+\*{0,2}`?)v\d+\.\d+\.\d+(`?\*{0,2})",
    re.I,
)
_LAST_TAGGED_SHIP = re.compile(
    r"(Last tagged ship is\s+\*{0,2})v\d+\.\d+\.\d+(\*{0,2})",
    re.I,
)
_CURRENT_SHIP = re.compile(r"^##\s+Current ship\s*$", re.I)
_HASH_LINE = (
    "`last_pass_tree_hash:` see [`integrity/hub-content-tree-hash.txt`]"
    "(integrity/hub-content-tree-hash.txt) "
    "(ADR 0050 content fingerprint; not a commit id)."
)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )


def read_version(root: Path) -> str:
    data = json.loads((root / VERSION_REL).read_text(encoding="utf-8"))
    return str(data["version"]).strip()


def current_branch(root: Path) -> str:
    return (_git(root, "rev-parse", "--abbrev-ref", "HEAD").stdout or "").strip()


def infer_release_branch(root: Path, version: str) -> str:
    record_path = root / RECORD_REL
    if record_path.is_file():
        try:
            existing = json.loads(record_path.read_text(encoding="utf-8"))
            branch = str(existing.get("release_branch") or "").strip()
            if branch:
                return branch
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    branch = current_branch(root)
    if branch.startswith("release/"):
        return branch
    return f"release/v{version}"


def record_bytes(version: str, release_branch: str) -> bytes:
    payload = {
        "schema": 2,
        "version": version,
        "release_branch": release_branch,
        "content_tree_hash_ref": CONTENT_TREE_REF,
    }
    return (json.dumps(payload, indent=2) + "\n").encode("utf-8")


def render_findings(text: str, version: str) -> str:
    out = _SHIPPED_GIT_TAG.sub(rf"\1v{version}\2", text)
    out = _LAST_TAGGED_SHIP.sub(rf"\1v{version}\2", out)
    if "hub-content-tree-hash.txt" not in out:
        lines = out.splitlines()
        insert_at = 1 if lines else 0
        lines.insert(insert_at, "")
        lines.insert(insert_at + 1, _HASH_LINE)
        out = "\n".join(lines)
        if text.endswith("\n"):
            out += "\n"
    return out


def render_describe(text: str, version: str) -> str:
    out = _LAST_TAGGED_SHIP.sub(rf"\1v{version}\2", text)
    lines = out.splitlines()
    start = None
    for i, line in enumerate(lines):
        if _CURRENT_SHIP.match(line):
            start = i
            break
    if start is None:
        if out and not out.endswith("\n"):
            out += "\n"
        out += f"\n## Current ship\n\nLast tagged ship is **v{version}**.\n"
        return out
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    body = ["", f"Last tagged ship is **v{version}**.", ""]
    new_lines = lines[: start + 1] + body + lines[end:]
    rendered = "\n".join(new_lines)
    if text.endswith("\n"):
        rendered += "\n"
    return rendered


def expected_surfaces(
    root: Path, *, version: str | None = None, release_branch: str | None = None
) -> dict[str, bytes]:
    ver = version or read_version(root)
    branch = release_branch or infer_release_branch(root, ver)
    findings = (root / FINDINGS_REL).read_text(encoding="utf-8")
    describe = (root / DESCRIBE_REL).read_text(encoding="utf-8")
    return {
        FINDINGS_REL: render_findings(findings, ver).encode("utf-8"),
        DESCRIBE_REL: render_describe(describe, ver).encode("utf-8"),
        RECORD_REL: record_bytes(ver, branch),
    }


def write_all(
    root: Path, *, version: str | None = None, release_branch: str | None = None
) -> list[str]:
    expected = expected_surfaces(root, version=version, release_branch=release_branch)
    written: list[str] = []
    for rel, body in expected.items():
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        written.append(rel)
    return written


def match_errors(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        expected = expected_surfaces(root)
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        return [f"release-prep script failed: {exc}"]
    for rel, body in expected.items():
        path = root / rel
        if not path.is_file():
            errors.append(f"missing {rel}")
            continue
        if path.read_bytes() != body:
            errors.append(f"{rel} differs from release-prep script output")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Script-only FINDINGS/DESCRIBE/record at prep")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--version")
    parser.add_argument("--branch")
    args = parser.parse_args(argv)
    if args.write:
        written = write_all(ROOT, version=args.version, release_branch=args.branch)
        print("RELEASE_PREP_SURFACES:WROTE " + " ".join(written))
        return 0
    errors = match_errors(ROOT)
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
