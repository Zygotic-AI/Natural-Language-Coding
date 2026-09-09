#!/usr/bin/env python3
"""Validate agent noun packages for BBP completeness.

Checks that each agent noun package under agents/<name>/ has:
  - AGENT.md with identity, invariants, handoff-in, completion artifact, success criteria
  - verbs.md where every verb declares input contract, output contract, and failure mode

Input: optional argv[1:] = specific agent names; if none, scans all agents/*/ directories.

Output: lines among
  PACKAGE:<name>:VALID|INVALID
  AGENT_MISSING <name>
  VERBS_MISSING <name>
  AGENT_MISSING_SECTION <name> <section>
  VERB_MISSING_INPUT <name> <verb>
  VERB_MISSING_OUTPUT <name> <verb>
  VERB_MISSING_FAILURE <name> <verb>
  RESULT:MET|NOT_MET

Failure mode: process exit 0 = RESULT:MET (PASS); exit 1 = RESULT:NOT_MET (FAIL).
  Does not swallow exceptions silently — unexpected errors propagate and abort.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"

AGENT_REQUIRED_SECTIONS = [
    "Identity",
    "Invariants",
    "Handoff-in",
    "Completion artifact",
    "Success criteria",
]

VERB_REQUIRED_SECTIONS = [
    "Input contract",
    "Output contract",
    "Failure mode",
]


class ValidationResult(NamedTuple):
    name: str
    valid: bool
    errors: list[str]


def find_agent_packages(names: list[str] | None = None) -> list[Path]:
    """Find agent noun package directories.
    
    If names provided, returns paths for those specific agents.
    Otherwise scans agents/ for all directories containing AGENT.md or verbs.md.
    """
    if names:
        return [AGENTS_DIR / n for n in names]
    
    packages = []
    if not AGENTS_DIR.exists():
        return packages
    
    for d in sorted(AGENTS_DIR.iterdir()):
        if not d.is_dir():
            continue
        if (d / "AGENT.md").exists() or (d / "verbs.md").exists():
            packages.append(d)
    return packages


def extract_headings(text: str) -> list[str]:
    """Extract markdown heading titles from text."""
    headings = []
    for line in text.split("\n"):
        match = re.match(r"^#+\s+(.+)", line)
        if match:
            headings.append(match.group(1).strip())
    return headings


def check_section_present(headings: list[str], section: str) -> bool:
    """Check if a section (case-insensitive partial match) is present in headings."""
    section_lower = section.lower()
    return any(section_lower in h.lower() for h in headings)


def extract_verbs(text: str) -> list[str]:
    """Extract verb names from verbs.md (## verb-name headings)."""
    verbs = []
    for line in text.split("\n"):
        match = re.match(r"^##\s+([a-z][a-z0-9-]*)", line, re.I)
        if match:
            verb_name = match.group(1).lower()
            if verb_name not in ("query", "produce", "excluded", "preconditions"):
                verbs.append(verb_name)
    return verbs


def extract_verb_sections(text: str, verb_name: str) -> list[str]:
    """Extract sections (### headings) under a specific verb."""
    lines = text.split("\n")
    in_verb = False
    sections = []
    
    for line in lines:
        if re.match(r"^##\s+", line) and not re.match(r"^###", line):
            verb_match = re.match(r"^##\s+([a-z][a-z0-9-]*)", line, re.I)
            if verb_match and verb_match.group(1).lower() == verb_name.lower():
                in_verb = True
            else:
                in_verb = False
        elif in_verb:
            section_match = re.match(r"^###\s+(.+)", line)
            if section_match:
                sections.append(section_match.group(1).strip())
    
    return sections


def validate_agent_md(pkg_path: Path, name: str) -> list[str]:
    """Validate AGENT.md structure, return list of errors."""
    errors = []
    agent_path = pkg_path / "AGENT.md"
    
    if not agent_path.exists():
        errors.append(f"AGENT_MISSING {name}")
        return errors
    
    text = agent_path.read_text()
    headings = extract_headings(text)
    
    for section in AGENT_REQUIRED_SECTIONS:
        if not check_section_present(headings, section):
            errors.append(f"AGENT_MISSING_SECTION {name} {section}")
    
    return errors


def validate_verbs_md(pkg_path: Path, name: str) -> list[str]:
    """Validate verbs.md structure, return list of errors."""
    errors = []
    verbs_path = pkg_path / "verbs.md"
    
    if not verbs_path.exists():
        errors.append(f"VERBS_MISSING {name}")
        return errors
    
    text = verbs_path.read_text()
    verbs = extract_verbs(text)
    
    if not verbs:
        errors.append(f"VERBS_EMPTY {name}")
        return errors
    
    for verb in verbs:
        sections = extract_verb_sections(text, verb)
        sections_lower = [s.lower() for s in sections]
        
        if not any("input" in s for s in sections_lower):
            errors.append(f"VERB_MISSING_INPUT {name} {verb}")
        if not any("output" in s for s in sections_lower):
            errors.append(f"VERB_MISSING_OUTPUT {name} {verb}")
        if not any("failure" in s for s in sections_lower):
            errors.append(f"VERB_MISSING_FAILURE {name} {verb}")
    
    return errors


def validate_package(pkg_path: Path) -> ValidationResult:
    """Validate a single agent noun package."""
    name = pkg_path.name
    errors = []
    
    if not pkg_path.exists():
        errors.append(f"PACKAGE_NOT_FOUND {name}")
        return ValidationResult(name, False, errors)
    
    errors.extend(validate_agent_md(pkg_path, name))
    errors.extend(validate_verbs_md(pkg_path, name))
    
    return ValidationResult(name, len(errors) == 0, errors)


def main() -> int:
    """Run validation on all or specified agent noun packages."""
    names = sys.argv[1:] if len(sys.argv) > 1 else None
    packages = find_agent_packages(names)
    
    if not packages:
        print("NO_PACKAGES_FOUND")
        print("RESULT:NOT_MET")
        return 1
    
    all_valid = True
    
    for pkg_path in packages:
        result = validate_package(pkg_path)
        
        status = "VALID" if result.valid else "INVALID"
        print(f"PACKAGE:{result.name}:{status}")
        
        for error in result.errors:
            print(error)
        
        if not result.valid:
            all_valid = False
    
    if all_valid:
        print("RESULT:MET")
        return 0
    else:
        print("RESULT:NOT_MET")
        return 1


if __name__ == "__main__":
    sys.exit(main())
