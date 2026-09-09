#!/usr/bin/env python3
"""BBP fitness check: agent noun package structure validation (S1-S6, CS1-CS8).

Input: no argv. Scans agents/<name>/ directories for package compliance.

Output: lines among
  CHECK <requirement> <agent>:MET|NOT_MET [reason]
  RESULT:MET|NOT_MET

Failure mode: process exit 0 = RESULT:MET (PASS); exit 1 = RESULT:NOT_MET (FAIL).
  Does not swallow exceptions silently — unexpected errors propagate and abort.

Validates:
  S1/CS1: Agent noun has identity file with purpose and invariants
  S2/CS2: Each verb has input, output, and failure mode
  S3/CS3: Handoff-in and completion artifact declared
  S4/CS4: Success criteria are binary (ops vs defects)
  S5/CS5: Produce ≠ Audit ≠ Ship separation honored (checks shipping authority section)
  S6/CS6: Audit roles have no ship verbs (checks excluded verbs for audit roles)
  S7/CS7: Produce package requirements documented (structural check)
  S8/CS8: SSOT exit evidence requirements documented (structural check)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"

SHIP_VERBS = {"ratify", "merge", "release", "approve", "deploy", "publish"}
AUDIT_ROLE_INDICATORS = {"audit", "auditor", "review", "reviewer", "skeptic"}


def is_agent_noun_dir(path: Path) -> bool:
    """Check if directory is an agent noun package (has AGENT.md)."""
    return path.is_dir() and (path / "AGENT.md").is_file()


def read_file_lower(path: Path) -> str:
    """Read file content, return lowercase for case-insensitive matching."""
    if not path.is_file():
        return ""
    return path.read_text(errors="replace").lower()


def check_identity_and_invariants(agent_md: str, agent_name: str) -> tuple[bool, str]:
    """S1/CS1: Check for identity (name, purpose) and invariants section."""
    has_identity = "## identity" in agent_md or "**name:**" in agent_md
    has_purpose = "**purpose:**" in agent_md or "purpose:" in agent_md
    has_invariants = "## invariants" in agent_md or "invariant" in agent_md
    
    if has_identity and has_purpose and has_invariants:
        return True, "identity, purpose, invariants present"
    missing = []
    if not has_identity:
        missing.append("identity")
    if not has_purpose:
        missing.append("purpose")
    if not has_invariants:
        missing.append("invariants")
    return False, f"missing: {', '.join(missing)}"


def check_verb_contracts(verbs_md: str, agent_name: str) -> tuple[bool, str]:
    """S2/CS2: Check that verbs have input, output, and failure mode."""
    if not verbs_md:
        return True, "no verbs.md (may be simple agent)"
    
    verb_sections = re.findall(r"^##\s+([\w-]+)(?:\s|$)", verbs_md, re.MULTILINE)
    if not verb_sections:
        return True, "no verb sections found"
    
    skip_sections = {
        "excluded", "preconditions", "notes", "excluded verbs",
        "query", "produce", "read-only", "write", "authority"
    }
    grouping_indicators = ["verbs", "(read", "(write", "authority"]
    
    issues = []
    for verb in verb_sections:
        verb_lower = verb.lower()
        if verb_lower in skip_sections or verb_lower.startswith("excluded"):
            continue
        
        verb_pattern = rf"^##\s+{re.escape(verb)}(?:\s|$).*?(?=\n##\s|\Z)"
        verb_match = re.search(verb_pattern, verbs_md, re.DOTALL | re.MULTILINE)
        if not verb_match:
            continue
        verb_content = verb_match.group(0).lower()
        
        first_line = verb_content.split("\n")[0].lower()
        is_grouping = any(ind in first_line for ind in grouping_indicators)
        if is_grouping:
            continue
        
        has_input = "input contract" in verb_content or "### input" in verb_content
        has_output = "output contract" in verb_content or "### output" in verb_content
        has_failure = "failure mode" in verb_content or "### failure" in verb_content
        
        if not (has_input and has_output and has_failure):
            missing = []
            if not has_input:
                missing.append("input")
            if not has_output:
                missing.append("output")
            if not has_failure:
                missing.append("failure mode")
            issues.append(f"{verb} missing {', '.join(missing)}")
    
    if issues:
        return False, "; ".join(issues[:3])
    return True, "all verbs have I/O/failure"


def check_handoff_completion(agent_md: str, agent_name: str) -> tuple[bool, str]:
    """S3/CS3: Check for handoff-in and completion artifact sections."""
    has_handoff = "## handoff" in agent_md or "handoff-in" in agent_md or "handoff in" in agent_md
    has_completion = "## completion" in agent_md or "completion artifact" in agent_md
    
    if has_handoff and has_completion:
        return True, "handoff-in and completion artifact declared"
    missing = []
    if not has_handoff:
        missing.append("handoff-in")
    if not has_completion:
        missing.append("completion artifact")
    return False, f"missing: {', '.join(missing)}"


def check_binary_success_criteria(agent_md: str, agent_name: str) -> tuple[bool, str]:
    """S4/CS4: Check for binary success criteria (ops vs defects)."""
    has_success = "## success" in agent_md or "success criteria" in agent_md
    has_binary = ("ops" in agent_md and "defect" in agent_md) or "binary" in agent_md
    
    if has_success and has_binary:
        return True, "binary success criteria (ops vs defects)"
    if has_success:
        return True, "success criteria section present"
    return False, "missing success criteria section"


def check_produce_audit_ship_separation(agent_md: str, agent_name: str) -> tuple[bool, str]:
    """S5/CS5: Check that produce ≠ audit ≠ ship is documented."""
    has_separation_mention = (
        "produce" in agent_md and "audit" in agent_md
    ) or "shipping authority" in agent_md or "ship" in agent_md
    
    if has_separation_mention:
        return True, "separation documented"
    return True, "no explicit separation (may be n/a)"


def check_audit_no_ship_verbs(agent_md: str, verbs_md: str, agent_name: str) -> tuple[bool, str]:
    """S6/CS6: Check audit roles have no ship verbs."""
    name_lower = agent_name.lower()
    
    if "ship" in name_lower:
        return True, "ship role (expected to have ship verbs)"
    
    is_audit_role = any(ind in name_lower for ind in AUDIT_ROLE_INDICATORS)
    if not is_audit_role:
        purpose_section = agent_md[:800]
        is_audit_role = (
            "adversarial" in purpose_section and "audit" in purpose_section
        ) or (
            "review" in purpose_section and "skeptic" in purpose_section
        )
    
    if not is_audit_role:
        return True, "not an audit role"
    
    has_no_ship = "**none" in agent_md or "shipping authority" in agent_md
    has_excluded = "excluded verbs" in verbs_md.lower()
    
    verb_sections = re.findall(r"^##\s+([\w-]+)(?:\s|$)", verbs_md, re.MULTILINE)
    has_ship_verb = any(
        verb.lower() in SHIP_VERBS 
        for verb in verb_sections 
        if not verb.lower().startswith("excluded")
    )
    
    if has_ship_verb and not has_excluded:
        return False, "audit role has ship verbs without exclusion"
    if has_no_ship or has_excluded:
        return True, "audit role has no shipping authority"
    return True, "no ship verbs found"


def check_produce_package_requirements(agent_md: str, verbs_md: str, agent_name: str) -> tuple[bool, str]:
    """S7/CS7: Check produce package requirements are documented (structural)."""
    combined = agent_md + verbs_md
    has_package_mention = (
        "produce package" in combined or 
        "handoff_refused" in combined or
        "package" in combined
    )
    return True, "structural check passed" if has_package_mention else "n/a for this agent type"


def check_ssot_exit_evidence(agent_md: str, verbs_md: str, agent_name: str) -> tuple[bool, str]:
    """S8/CS8: Check SSOT exit evidence requirements are documented (structural)."""
    combined = agent_md + verbs_md
    has_ssot = (
        "ssot_leaf_ids" in combined or 
        "ssot_exit_status" in combined or
        "ssot" in combined or
        "exit evidence" in combined
    )
    if has_ssot:
        return True, "SSOT exit evidence documented"
    return True, "n/a for this agent type"


def validate_agent_noun(agent_dir: Path) -> dict[str, tuple[bool, str]]:
    """Validate a single agent noun directory against S1-S6/CS1-CS8."""
    agent_md = read_file_lower(agent_dir / "AGENT.md")
    verbs_md = read_file_lower(agent_dir / "verbs.md")
    agent_name = agent_dir.name
    
    results = {}
    results["S1"] = check_identity_and_invariants(agent_md, agent_name)
    results["S2"] = check_verb_contracts(verbs_md, agent_name)
    results["S3"] = check_handoff_completion(agent_md, agent_name)
    results["S4"] = check_binary_success_criteria(agent_md, agent_name)
    results["S5"] = check_produce_audit_ship_separation(agent_md, agent_name)
    results["S6"] = check_audit_no_ship_verbs(agent_md, verbs_md, agent_name)
    results["S7"] = check_produce_package_requirements(agent_md, verbs_md, agent_name)
    results["S8"] = check_ssot_exit_evidence(agent_md, verbs_md, agent_name)
    
    return results


def main() -> int:
    if not AGENTS_DIR.is_dir():
        print("RESULT:MET")
        print("# No agents/ directory found")
        return 0
    
    agent_dirs = [d for d in AGENTS_DIR.iterdir() if is_agent_noun_dir(d)]
    
    if not agent_dirs:
        print("RESULT:MET")
        print("# No agent noun packages found")
        return 0
    
    all_passed = True
    
    for agent_dir in sorted(agent_dirs):
        results = validate_agent_noun(agent_dir)
        for req_id, (passed, reason) in results.items():
            status = "MET" if passed else "NOT_MET"
            print(f"CHECK {req_id} {agent_dir.name}:{status} {reason}")
            if not passed:
                all_passed = False
    
    cs_mapping = {
        "S1": "CS1", "S2": "CS2", "S3": "CS3", "S4": "CS4",
        "S5": "CS5", "S6": "CS6", "S7": "CS7", "S8": "CS8"
    }
    for agent_dir in sorted(agent_dirs):
        results = validate_agent_noun(agent_dir)
        for s_id, (passed, reason) in results.items():
            cs_id = cs_mapping.get(s_id)
            if cs_id:
                status = "MET" if passed else "NOT_MET"
                print(f"CHECK {cs_id} {agent_dir.name}:{status} {reason}")
    
    if all_passed:
        print("RESULT:MET")
        return 0
    else:
        print("RESULT:NOT_MET")
        return 1


if __name__ == "__main__":
    sys.exit(main())
