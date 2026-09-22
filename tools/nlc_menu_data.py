"""Single source for human menu labels (ADR 0017, 0020)."""

from __future__ import annotations

INSTALL_CMD = (
    "curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/"
    "main/scripts/install.sh | bash"
)

# Humans: machine commands + agent slash skills. Requirements/build are agent-only (ADR 0020).
SHORT_MAP: list[tuple[str, str]] = [
    ("Start (new app)", "./nlc new <folder> --name MyApp"),
    ("Start (existing code, beta)", "./nlc adopt-existing ."),
    ("Guide (anytime)", "/interview in your agent"),
    ("Requirements", "/interview in your agent"),
    ("Build & compile", "/planit in your agent"),
    ("Verify", "./nlc verify"),
    ("Share packs", "./nlc pack export | ./nlc pack install"),
    ("Upgrade compiler", "./nlc upgrade"),
    ("Release check", "./nlc ship-check"),
]


COMMAND_MAP_STEP: dict[str, int] = {
    "requirements": 4,
    "build": 5,
    "verify": 6,
    "maintain": 9,
}


def command_map_step(stage: str) -> int | None:
    return COMMAND_MAP_STEP.get(stage)


def render_short_map_lines() -> list[str]:
    lines = ["Command map", "-----------"]
    for i, (label, cmd) in enumerate(SHORT_MAP, start=1):
        lines.append(f"  {i}. {label}: {cmd}")
    return lines


def render_workflow_lines() -> list[str]:
    return render_short_map_lines()
