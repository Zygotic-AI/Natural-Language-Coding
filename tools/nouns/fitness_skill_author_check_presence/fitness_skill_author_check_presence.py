"""Install and the hub use-case must still invoke the skill-author checker."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ADR = ROOT / "adrs" / "0054-published-skill-author-contract.md"
GOAL_SH = ROOT / "goals" / "hub_skill_author_check" / "execute.sh"
GOAL_PS1 = ROOT / "goals" / "hub_skill_author_check" / "execute.ps1"
INSTALL_SH = ROOT / "goals" / "hub_install" / "execute.sh"
INSTALL_PS1 = ROOT / "goals" / "hub_install" / "execute.ps1"
CLI = ROOT / "tools" / "nlc-skill-author-check.py"
CHECKLIST = ROOT / "integrity" / "skill-author-checklist.json"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path, label in (
        (ADR, "adrs/0054-published-skill-author-contract.md"),
        (GOAL_SH, "goals/hub_skill_author_check/execute.sh"),
        (GOAL_PS1, "goals/hub_skill_author_check/execute.ps1"),
        (INSTALL_SH, "goals/hub_install/execute.sh"),
        (INSTALL_PS1, "goals/hub_install/execute.ps1"),
        (CLI, "tools/nlc-skill-author-check.py"),
        (CHECKLIST, "integrity/skill-author-checklist.json"),
    ):
        if not path.is_file():
            violations.append(f"missing {label}")
    goal_sh = GOAL_SH.read_text(encoding="utf-8") if GOAL_SH.is_file() else ""
    goal_ps1 = GOAL_PS1.read_text(encoding="utf-8") if GOAL_PS1.is_file() else ""
    install_sh = INSTALL_SH.read_text(encoding="utf-8") if INSTALL_SH.is_file() else ""
    install_ps1 = INSTALL_PS1.read_text(encoding="utf-8") if INSTALL_PS1.is_file() else ""
    if "nlc-skill-author-check.py" not in goal_sh:
        violations.append("hub_skill_author_check/execute.sh must invoke nlc-skill-author-check.py")
    if "implementation.py" in goal_sh or "implementation.py" in goal_ps1:
        violations.append("hub_skill_author_check must not add implementation.py")
    if "nlc-skill-author-check.py" not in goal_ps1:
        violations.append("hub_skill_author_check/execute.ps1 must invoke nlc-skill-author-check.py")
    if "hub_skill_author_check" not in install_sh:
        violations.append("hub_install/execute.sh must invoke goals/hub_skill_author_check")
    if "hub_skill_author_check" not in install_ps1:
        violations.append("hub_install/execute.ps1 must invoke goals/hub_skill_author_check")
    if install_sh.find("hub_skill_author_check") > install_sh.find("NLC_SKIP_VERIFY") >= 0:
        violations.append("hub_install/execute.sh must not hide the skill-author check behind NLC_SKIP_VERIFY")
    if install_ps1.find("hub_skill_author_check") > install_ps1.find("NLC_SKIP_VERIFY") >= 0:
        violations.append("hub_install/execute.ps1 must not hide the skill-author check behind NLC_SKIP_VERIFY")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
