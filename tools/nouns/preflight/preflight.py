"""Install / hub preflight for human ./nlc (ADR 0017–0018)."""

from __future__ import annotations

from pathlib import Path

from nouns.menu_data import INSTALL_CMD

BOUNDARY = "bba-emit"


def preflight_issues(hub: Path, project: Path) -> list[dict[str, str]]:
    """Each issue: problem, fix (human interview shape, one line each)."""
    issues: list[dict[str, str]] = []

    hub_nlc = hub / "tools" / "nlc.py"
    if not hub_nlc.is_file():
        issues.append(
            {
                "id": "hub-missing",
                "problem": "Natural Language Coding is not installed on this machine.",
                "fix": f"Run: {INSTALL_CMD}",
            }
        )
        return issues

    ver_path = hub / "integrity" / "nlc-version.json"
    if not ver_path.is_file():
        issues.append(
            {
                "id": "hub-incomplete",
                "problem": "The compiler install looks broken (missing version file).",
                "fix": "Run: ./nlc doctor fix",
            }
        )

    planit = Path.home() / ".agents" / "skills" / "planit" / "SKILL.md"
    interview = Path.home() / ".agents" / "skills" / "interview" / "SKILL.md"
    if not planit.is_file() or not interview.is_file():
        missing = []
        if not planit.is_file():
            missing.append("build skill")
        if not interview.is_file():
            missing.append("guide skill")
        issues.append(
            {
                "id": "skills-missing",
                "problem": f"Agent skills are missing ({', '.join(missing)}).",
                "fix": "Run: ./nlc doctor fix",
            }
        )

    lock = project / ".nlc" / "lock.json"
    if project != hub.resolve() and not lock.is_file():
        if not (project / ".nlc").is_dir():
            issues.append(
                {
                    "id": "not-a-project",
                    "problem": "This folder is not an NLC app yet.",
                    "fix": "./nlc new <folder> --name MyApp   OR   ./nlc adopt-existing .",
                }
            )

    return issues
