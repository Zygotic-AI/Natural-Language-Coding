"""Control/gate designs must carry a lifecycle walkthrough and verifier-change known-bad."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

PLANIT = ROOT / ".agents" / "skills" / "planit" / "SKILL.md"
AWL = ROOT / ".agents" / "skills" / "planit" / "references" / "audited-work-loop-standard.md"
RELEASE = ROOT / ".agents" / "skills" / "release" / "SKILL.md"
BRIEF_MOD = ROOT / "tools" / "nouns" / "hub_own_produce" / "hub_own_produce.py"
KNOWN_BAD = ROOT / "tools" / "assert-verifier-change-via-staging-passes.py"

LIFECYCLE_NEEDLES = (
    "create, change, sign, ingest, rotate",
    "first bootstrap",
    "legitimate change to the verifier",
)
CONTROL_GATE_NEEDLES = (
    "CONTROL-LIFECYCLE",
    "control or gate design",
)


def _hub_repo(root: Path) -> bool:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from nlc_pipeline import is_hub_repo

    return is_hub_repo(root)


def control_lifecycle_errors(root: Path) -> list[str]:
    errors: list[str] = []
    planit = root / ".agents" / "skills" / "planit" / "SKILL.md"
    awl = root / ".agents" / "skills" / "planit" / "references" / "audited-work-loop-standard.md"
    release = root / ".agents" / "skills" / "release" / "SKILL.md"
    brief_mod = root / "tools" / "nouns" / "hub_own_produce" / "hub_own_produce.py"
    known_bad = root / "tools" / "assert-verifier-change-via-staging-passes.py"
    for path, label in (
        (planit, "Planit skill"),
        (awl, "AWL standard"),
        (release, "/release skill"),
        (brief_mod, "briefing validator"),
        (known_bad, "verifier-change known-bad"),
    ):
        if not path.is_file():
            errors.append(f"missing {label} ({path.as_posix()})")
    texts = {
        "planit": planit.read_text(encoding="utf-8") if planit.is_file() else "",
        "awl": awl.read_text(encoding="utf-8") if awl.is_file() else "",
        "release": release.read_text(encoding="utf-8") if release.is_file() else "",
        "brief": brief_mod.read_text(encoding="utf-8") if brief_mod.is_file() else "",
    }
    for needle in LIFECYCLE_NEEDLES:
        if needle not in texts["planit"]:
            errors.append(f"Planit skill missing checked rule {needle!r}")
        if needle not in texts["awl"]:
            errors.append(f"AWL standard missing checked rule {needle!r}")
    if "CONTROL-LIFECYCLE" not in texts["planit"]:
        errors.append("Planit skill missing CONTROL-LIFECYCLE gate row")
    if "control or gate design" not in texts["brief"]:
        errors.append("briefing validator missing control or gate design branch")
    for needle in LIFECYCLE_NEEDLES:
        if needle not in texts["brief"]:
            errors.append(f"briefing validator missing {needle!r}")
    if "mandated-paths" not in texts["release"] and "derive-mandated-paths" not in texts["release"]:
        errors.append("/release skill must import the derived mandated-path list")
    return errors


def main() -> int:
    args = sys.argv[1:]
    root = Path(args[0]).resolve() if args and not args[0].startswith("-") else ROOT
    if not _hub_repo(root):
        print("CONTROL_LIFECYCLE:MET skip (hub-only gate, not hub tree)")
        return 0
    errors = control_lifecycle_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("CONTROL_LIFECYCLE:NOT_MET")
        return 1
    print("CONTROL_LIFECYCLE:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
