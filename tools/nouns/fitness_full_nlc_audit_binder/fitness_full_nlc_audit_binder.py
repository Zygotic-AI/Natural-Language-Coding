#!/usr/bin/env python3
"""Binder: full-nlc-audit manifest, script, and skill stay wired."""

from __future__ import annotations



import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    manifest = ROOT / "integrity" / "full-nlc-audit-manifest.json"
    script = ROOT / "tools" / "full-nlc-audit.py"
    skill = ROOT / ".agents" / "skills" / "full-nlc-audit" / "SKILL.md"
    doc = ROOT / "docs" / "nlc" / "FULL-NLC-AUDIT.md"
    leaves = ROOT / "integrity" / "integration-leaves.json"
    handoff = ROOT / ".agents" / "instructions" / "planit-phase7-handoff-adr-0038.md"
    manifest_fitness = ROOT / "tools" / "fitness-full-nlc-audit-manifest.py"
    drift_fitness = ROOT / "tools" / "fitness-full-nlc-audit-manifest-drift.py"

    for path, label in (
        (manifest, "manifest"),
        (script, "full-nlc-audit.py"),
        (skill, "skill"),
        (doc, "FULL-NLC-AUDIT.md"),
        (leaves, "integration-leaves.json"),
        (handoff, "planit-phase7-handoff-adr-0038.md"),
        (manifest_fitness, "fitness-full-nlc-audit-manifest.py"),
        (drift_fitness, "fitness-full-nlc-audit-manifest-drift.py"),
    ):
        if not path.is_file():
            violations.append(f"missing {label}")

    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for profile in ("quick", "release-prep", "full"):
            if profile not in (data.get("profiles") or {}):
                violations.append(f"manifest missing profile {profile}")
        quick = (data.get("profiles") or {}).get("quick") or []
        if "binding-matrix" not in quick:
            violations.append("quick profile must include binding-matrix")

    text = script.read_text(encoding="utf-8") if script.is_file() else ""
    if "FULL_NLC_AUDIT:MET" not in text:
        violations.append("full-nlc-audit.py must emit FULL_NLC_AUDIT:MET")
    if "--emit-inference-checklist" not in text:
        violations.append("full-nlc-audit.py must support --emit-inference-checklist")
    if "git_worktree_clean" not in text:
        violations.append("full-nlc-audit.py must implement git_worktree_clean builtin")

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

