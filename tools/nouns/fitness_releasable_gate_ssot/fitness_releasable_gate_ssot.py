"""Refuse a second home for releasable gate profiles (RCA-1 containment)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SSOT = ROOT / "integrity" / "releasable-gates.json"
_FORBIDDEN_REDIRECT = re.compile(r"/verify in your agent", re.I)
_PROFILE_MARK = '"profiles"'


def scan_duplicate_profiles() -> list[str]:
    violations: list[str] = []
    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts or "node_modules" in path.parts:
            continue
        if path.resolve() == SSOT.resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if _PROFILE_MARK not in text:
            continue
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            continue
        profiles = data.get("profiles") if isinstance(data, dict) else None
        if not isinstance(profiles, dict):
            continue
        if "verify" in profiles and "release" in profiles:
            rel = path.relative_to(ROOT)
            violations.append(f"second releasable profile home: {rel}")
    return violations


def scan_forbidden_redirect() -> list[str]:
    violations: list[str] = []
    for rel in (
        "tools/nouns/verify/verify.py",
        "tools/nouns/dashboard/dashboard.py",
        ".agents/skills/verify/SKILL.md",
    ):
        path = ROOT / rel
        if not path.is_file():
            continue
        if _FORBIDDEN_REDIRECT.search(path.read_text(encoding="utf-8", errors="replace")):
            violations.append(f"forbidden agent redirect in {rel}")
    return violations


def wired_to_runner() -> list[str]:
    violations: list[str] = []
    ci = ROOT / "tools" / "nouns" / "ci_fitness" / "ci_fitness.py"
    verify = ROOT / "tools" / "nouns" / "verify" / "verify.py"
    for label, path, needle in (
        ("ci_fitness", ci, "run_profile"),
        ("verify", verify, "run_profile"),
    ):
        if not path.is_file():
            violations.append(f"missing {label} module")
            continue
        if needle not in path.read_text(encoding="utf-8", errors="replace"):
            violations.append(f"{label} must call releasable run_profile")
    return violations


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.releasable_gates.releasable_gates import (
        _release_prep_sync_violations,
        verify_subset_of_release,
    )

    violations: list[str] = []
    if not SSOT.is_file():
        violations.append("missing integrity/releasable-gates.json")
    violations.extend(verify_subset_of_release())
    violations.extend(_release_prep_sync_violations())
    violations.extend(scan_duplicate_profiles())
    violations.extend(scan_forbidden_redirect())
    violations.extend(wired_to_runner())
    for item in violations:
        print(f"VIOLATION {item}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
