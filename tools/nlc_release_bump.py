#!/usr/bin/env python3
"""Hub release semver: suggest bump from diff heuristics, apply version + migration unit."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402
VERSION_PATH = ROOT / "integrity" / "nlc-version.json"

# Major hints apply only on charter/policy paths — not docs mentioning "breaking change".
POLICY_PATH_PREFIXES = ("adrs/", "rules/", "knowledge/", "integrity/")
MAJOR_HINTS = (
    "breaking change",
    "breaking:",
    "removed obligation",
    "incompatible",
)
MINOR_PATH_PREFIXES = ("adrs/", "rules/", "knowledge/", "integrity/examples/")
MINOR_TEXT_HINTS = (
    "pci",
    "hipaa",
    "requirement pack",
    "new policy",
    "new standard",
    "soc2",
    "gdpr",
)


def read_version() -> str:
    data = json.loads(VERSION_PATH.read_text(encoding="utf-8"))
    return str(data["version"]).strip()


def write_version(version: str) -> None:
    VERSION_PATH.write_text(
        json.dumps({"version": version}, indent=2) + "\n",
        encoding="utf-8",
    )


def bump_semver(current: str, level: str) -> str:
    major, minor, patch = (int(x) for x in current.split("."))
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    if level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"unknown level: {level}")


def _git_lines(*args: str) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]


def changed_paths() -> list[str]:
    lines = _git_lines("status", "--porcelain")
    paths: list[str] = []
    for ln in lines:
        if len(ln) < 4:
            continue
        paths.append(ln[3:].strip())
    paths.extend(_git_lines("diff", "--name-only", "HEAD"))
    paths.extend(_git_lines("diff", "--cached", "--name-only"))
    seen: set[str] = set()
    out: list[str] = []
    for p in paths:
        norm = p.replace("\\", "/")
        if norm not in seen:
            seen.add(norm)
            out.append(norm)
    return out


def diff_blob() -> str:
    proc = subprocess.run(
        ["git", "diff", "HEAD"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    text = (proc.stdout or "") + (proc.stderr or "")
    proc2 = subprocess.run(
        ["git", "diff", "--cached"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return (text + (proc2.stdout or "")).lower()


def _is_policy_path(path: str) -> bool:
    if path.rstrip("/") == "CHARTER.md":
        return True
    return any(path.startswith(prefix) for prefix in POLICY_PATH_PREFIXES)


def policy_diff_blob(paths: list[str]) -> str:
    policy = [p for p in paths if _is_policy_path(p)]
    if not policy:
        return ""
    proc = subprocess.run(
        ["git", "diff", "HEAD", "--", *policy],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    text = (proc.stdout or "") + (proc.stderr or "")
    proc2 = subprocess.run(
        ["git", "diff", "--cached", "--", *policy],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return (text + (proc2.stdout or "")).lower()


def suggest_bump() -> tuple[str, list[str]]:
    paths = changed_paths()
    blob = diff_blob()
    policy_blob = policy_diff_blob(paths)
    reasons: list[str] = []
    level = "patch"

    if any(p.rstrip("/") == "CHARTER.md" for p in paths):
        return "major", ["CHARTER.md changed — treat as major unless you know otherwise"]

    for p in paths:
        if p.startswith("examples/"):
            continue
        if "/remove-" in p or p.startswith("remove-"):
            return "major", [f"breaking-looking path: {p}"]

    for hint in MAJOR_HINTS:
        if hint in policy_blob and "non-breaking" not in policy_blob:
            reasons.append(f"policy diff mentions “{hint}”")
            level = "major"
            break

    if level != "major":
        for prefix in MINOR_PATH_PREFIXES:
            if any(p.startswith(prefix) for p in paths):
                reasons.append(f"requirements/policy tree touched ({prefix})")
                level = "minor"
                break
        if level == "patch":
            for hint in MINOR_TEXT_HINTS:
                if hint in blob:
                    reasons.append(f"diff suggests new scope (e.g. {hint})")
                    level = "minor"
                    break
        if any(p.startswith("adrs/") and p.endswith(".md") for p in paths):
            if level == "patch":
                reasons.append("ADR files changed")
            level = "minor"

    if not reasons:
        reasons.append("default: patch (fixes, docs-only, or internal tooling)")
    return level, reasons


def apply_bump(level: str | None, keep: bool) -> tuple[str, str]:
    from nlc_migration_catalog import ensure_migration_chain

    current = read_version()
    if keep:
        return current, current
    if not level:
        raise ValueError("level required when not keeping current version")
    new = bump_semver(current, level)
    if new == current:
        raise ValueError("bump produced same version")
    ensure_migration_chain(ROOT, current, new)
    write_version(new)
    return current, new


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Hub release version helper")
    parser.add_argument("--suggest", action="store_true", help="Print suggested bump level")
    parser.add_argument("--current", action="store_true", help="Print current version")
    parser.add_argument(
        "--apply",
        choices=("patch", "minor", "major", "keep"),
        help="Bump (or keep) and write integrity/nlc-version.json + migration",
    )
    parser.add_argument(
        "--peek",
        choices=("patch", "minor", "major", "keep"),
        help="Print target version without writing files",
    )
    args = parser.parse_args()

    if args.peek:
        current = read_version()
        if args.peek == "keep":
            print(current)
        else:
            print(bump_semver(current, args.peek))
        return 0

    if args.current:
        print(read_version())
        return 0
    if args.suggest:
        level, reasons = suggest_bump()
        print(level)
        for r in reasons:
            print(f"  hint: {r}", file=sys.stderr)
        return 0
    if args.apply:
        keep = args.apply == "keep"
        level = None if keep else args.apply
        old, new = apply_bump(level, keep)
        print(f"version: {old} -> {new}")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
