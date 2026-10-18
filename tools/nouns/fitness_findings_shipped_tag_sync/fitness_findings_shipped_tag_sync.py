#!/usr/bin/env python3
"""FINDINGS / DESCRIBE current-ship prose must not contradict shipped identity (F1)."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = ROOT / "FINDINGS.md"
DESCRIBE = ROOT / "DESCRIBE.md"
VERSION_REL = "integrity/nlc-version.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
LEFTOVER_FINDINGS = FIXTURES / "origin-main-needed-leftover.md"
LEFTOVER_DESCRIBE = FIXTURES / "origin-main-current-ship.md"

TAGGED_ON_ORIGIN = re.compile(
    r"v(\d+\.\d+\.\d+)\s+is\s+tagged\s+on\s+origin|tagged\s+on\s+origin.*v(\d+\.\d+\.\d+)",
    re.I,
)
NO_SHIPPED_TAG = re.compile(r"no shipped tag", re.I)
NLC_VERSION_CLAIM = re.compile(
    r"nlc-version\.json`?\s+(?:is\s+)?\*{0,2}(\d+\.\d+\.\d+)",
    re.I,
)
SHIPPED_GIT_TAG = re.compile(
    r"Shipped git tag\s+\*{0,2}`?v(\d+\.\d+\.\d+)`?",
    re.I,
)
LAST_TAGGED_SHIP = re.compile(
    r"Last tagged ship is\s+\*{0,2}v(\d+\.\d+\.\d+)",
    re.I,
)


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def read_file_version(root: Path = ROOT) -> str | None:
    path = root / VERSION_REL
    if not path.is_file():
        return None
    try:
        return str(json.loads(path.read_text(encoding="utf-8"))["version"]).strip()
    except (OSError, json.JSONDecodeError, KeyError):
        return None


def current_branch() -> str:
    proc = _git("rev-parse", "--abbrev-ref", "HEAD")
    return (proc.stdout or "").strip()


def is_main_or_tag_time(*, tag_time: bool = False) -> bool:
    if tag_time:
        return True
    branch = current_branch()
    if branch == "main":
        return True
    if branch.startswith("release/"):
        return False
    head = (_git("rev-parse", "HEAD").stdout or "").strip()
    main = (_git("rev-parse", "origin/main").stdout or "").strip()
    return bool(head and main and head == main)


def resolve_shipped_version() -> str | None:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_release_tags import last_shipped_tag, tag_version  # noqa: E402

    for ref in ("origin/main", "main"):
        tag = last_shipped_tag(ref)
        if tag:
            return tag_version(tag)
    return None


def describe_current_ship_section(text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+Current ship\s*$", line, re.I):
            start = i
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def _allowed_phrase_versions(
    *,
    shipped_ver: str | None,
    file_ver: str | None,
    on_main_or_tag: bool,
) -> set[str]:
    if on_main_or_tag:
        return {file_ver} if file_ver else set()
    allowed = set()
    if shipped_ver:
        allowed.add(shipped_ver)
    if file_ver:
        allowed.add(file_ver)
    return allowed


def check_claims(
    text: str,
    *,
    source: str,
    shipped_ver: str | None,
    file_ver: str | None,
    on_main_or_tag: bool,
) -> list[str]:
    violations: list[str] = []
    if shipped_ver and NO_SHIPPED_TAG.search(text):
        violations.append(f"{source} asserts no shipped tag but origin/main has v{shipped_ver}")

    for m in NLC_VERSION_CLAIM.finditer(text):
        claimed = m.group(1)
        if file_ver and claimed != file_ver:
            violations.append(
                f"{source} asserts nlc-version.json is {claimed} but file is {file_ver}"
            )

    allowed = _allowed_phrase_versions(
        shipped_ver=shipped_ver, file_ver=file_ver, on_main_or_tag=on_main_or_tag
    )
    for m in SHIPPED_GIT_TAG.finditer(text):
        claimed = m.group(1)
        if claimed not in allowed:
            violations.append(
                f"{source} Shipped git tag v{claimed} does not match allowed {sorted(allowed)}"
            )
    for m in LAST_TAGGED_SHIP.finditer(text):
        claimed = m.group(1)
        if claimed not in allowed:
            violations.append(
                f"{source} Last tagged ship v{claimed} does not match allowed {sorted(allowed)}"
            )
    for m in TAGGED_ON_ORIGIN.finditer(text):
        claimed = m.group(1) or m.group(2)
        if shipped_ver is None:
            violations.append(
                f"{source} claims v{claimed} tagged on origin but no reachable tag on origin/main"
            )
        elif claimed != shipped_ver:
            violations.append(
                f"{source} claims v{claimed} on origin but newest origin/main tag is v{shipped_ver}"
            )
    return violations


def check_surfaces(
    findings_text: str,
    describe_text: str,
    *,
    shipped_ver: str | None,
    file_ver: str | None,
    on_main_or_tag: bool,
) -> list[str]:
    violations = check_claims(
        findings_text,
        source="FINDINGS.md",
        shipped_ver=shipped_ver,
        file_ver=file_ver,
        on_main_or_tag=on_main_or_tag,
    )
    current_ship = describe_current_ship_section(describe_text)
    if current_ship:
        violations.extend(
            check_claims(
                current_ship,
                source="DESCRIBE.md Current ship",
                shipped_ver=shipped_ver,
                file_ver=file_ver,
                on_main_or_tag=on_main_or_tag,
            )
        )
    return violations


def leftover_fixture_violations(*, shipped_ver: str | None, file_ver: str | None) -> list[str]:
    if not LEFTOVER_FINDINGS.is_file() or not LEFTOVER_DESCRIBE.is_file():
        return ["missing F1 leftover fixtures next to fitness_findings_shipped_tag_sync"]
    return check_surfaces(
        LEFTOVER_FINDINGS.read_text(encoding="utf-8", errors="replace"),
        LEFTOVER_DESCRIBE.read_text(encoding="utf-8", errors="replace"),
        shipped_ver=shipped_ver,
        file_ver=file_ver,
        on_main_or_tag=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="F1 FINDINGS/DESCRIBE current-ship sync")
    parser.add_argument("paths", nargs="*", help="Ignored (ci_fitness may pass a tree path)")
    parser.add_argument("--tag-time", action="store_true", help="Treat as main/tag-time phrase rule")
    args = parser.parse_args()
    _ = args.paths

    shipped_ver = resolve_shipped_version()
    file_ver = read_file_version()
    on_main_or_tag = is_main_or_tag_time(tag_time=args.tag_time)

    leftover = leftover_fixture_violations(shipped_ver=shipped_ver, file_ver=file_ver)
    if not leftover:
        print("VIOLATION leftover fixture must NOT_MET (no shipped tag / 0.2.0 / stale Last-pass)")
        print("RESULT:NOT_MET")
        return 1

    if not FINDINGS.is_file():
        print("VIOLATION missing FINDINGS.md")
        print("RESULT:NOT_MET")
        return 1
    if not DESCRIBE.is_file():
        print("VIOLATION missing DESCRIBE.md")
        print("RESULT:NOT_MET")
        return 1

    violations = check_surfaces(
        FINDINGS.read_text(encoding="utf-8", errors="replace"),
        DESCRIBE.read_text(encoding="utf-8", errors="replace"),
        shipped_ver=shipped_ver,
        file_ver=file_ver,
        on_main_or_tag=on_main_or_tag,
    )
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())


BOUNDARY = "bba-emit"
