"""Skill is a content type whose recipe gate is the published-skill author checklist."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOW_TO = ROOT / "content-types" / "HOW-TO-ADD.md"
LEXICON = ROOT / "integrity" / "LEXICON.md"
CONTRIB = ROOT / "integrity" / "CONTRIBUTION.md"
TERMS = ROOT / "docs" / "TERMS.md"
TOOLS_README = ROOT / "tools" / "README.md"
LINKER = ROOT / "tools" / "nouns" / "link_terms_dictionary" / "link_terms_dictionary.py"
CHECKLIST = ROOT / "integrity" / "skill-author-checklist.json"
CLI = ROOT / "tools" / "nlc-skill-author-check.py"
LANDMINE = ROOT / "examples" / "skill-author-check-landmine" / ".agents" / "skills" / "demo" / "SKILL.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path, label in (
        (HOW_TO, "content-types/HOW-TO-ADD.md"),
        (LEXICON, "integrity/LEXICON.md"),
        (CONTRIB, "integrity/CONTRIBUTION.md"),
        (TERMS, "docs/TERMS.md"),
        (TOOLS_README, "tools/README.md"),
        (LINKER, "link_terms_dictionary.py"),
        (CHECKLIST, "integrity/skill-author-checklist.json"),
        (CLI, "tools/nlc-skill-author-check.py"),
        (LANDMINE, "skill-author-check-landmine SKILL.md"),
    ):
        if not path.is_file():
            violations.append(f"missing {label}")
    how = HOW_TO.read_text(encoding="utf-8") if HOW_TO.is_file() else ""
    if "| [Skill](#skill)" not in how and "| Skill |" not in how:
        violations.append("HOW-TO-ADD index must name Skill")
    if "## [Skill]" not in how and "## Skill" not in how:
        violations.append("HOW-TO-ADD must have a Skill type recipe")
    if "nlc-skill-author-check.py" not in how:
        violations.append("Skill recipe must point at nlc-skill-author-check.py")
    if "skill-author-checklist.json" not in how:
        violations.append("Skill recipe must point at skill-author-checklist.json")
    if "name:" not in how or "Incomplete-Packet" not in how:
        violations.append("Skill recipe must include incomplete-packet fixture for name:")
    lex = LEXICON.read_text(encoding="utf-8") if LEXICON.is_file() else ""
    if "Skill" not in lex.split("### [Content type]", 1)[-1].split("### ", 1)[0]:
        violations.append("LEXICON content-type list must include Skill")
    contrib = CONTRIB.read_text(encoding="utf-8") if CONTRIB.is_file() else ""
    if ".agents/skills/<name>/SKILL.md" not in contrib:
        violations.append("CONTRIBUTION naming table must include Skill path")
    terms = TERMS.read_text(encoding="utf-8") if TERMS.is_file() else ""
    if "Skill" not in terms:
        violations.append("TERMS.md must name Skill as a content type")
    if "every `*.md`" not in terms and "not every `*.md`" not in terms:
        if "recipe-marked prose" not in terms:
            violations.append("TERMS.md must narrow the TERMS-link walk off unbounded *.md")
    tools_readme = TOOLS_README.read_text(encoding="utf-8") if TOOLS_README.is_file() else ""
    if "recipe-marked prose" not in tools_readme and "not every `*.md`" not in tools_readme:
        violations.append("tools/README.md must not describe an unbounded markdown TERMS-link walk")
    linker = LINKER.read_text(encoding="utf-8") if LINKER.is_file() else ""
    if '.agents/skills/' not in linker or '.cursor/skills/' not in linker:
        violations.append("linker must skip published skill trees")
    landmine = LANDMINE.read_text(encoding="utf-8") if LANDMINE.is_file() else ""
    if "name: [" not in landmine:
        violations.append("landmine must keep name: as a markdown link")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
