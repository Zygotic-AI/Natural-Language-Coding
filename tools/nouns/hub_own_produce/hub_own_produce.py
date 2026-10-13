"""ADR 0051 SG1/SG3 hub material produce package validation."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import fnmatch
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from nouns.gate_set_manifest.gate_set_manifest import gate_paths_manifest_errors
from nouns.gate_set.gate_set import is_gate_set_path

PROFILE_REL = "integrity/hub-gate-diff-profile.json"
DEFAULT_BASE_REFS = (
    "origin/release/v0.3.0",
    "release/v0.3.0",
)
FORBID_CLAUSE_NEEDLES = (
    "weakening a check",
    "broadening an exemption",
    "rewriting a receipt",
)
_DEFAULT_HUB_MATERIAL_GLOBS = (
    "adrs/**",
    "docs/**",
    "tools/**",
    "integrity/**",
    "agents/**",
    "theory/**",
    "content-types/**",
    ".agents/**",
    ".cursor/**",
    ".nlc/**",
    ".github/**",
    "CHARTER.md",
    "AGENTS.md",
    "MANIFESTO.md",
    "DESCRIBE.md",
    "TODO",
    "examples/**",
)

_CI_ONLY_EXIT = re.compile(
    r"^(?:ci\s*(?:fitness)?\s*green|fitness\s*green|github\s*actions?\s*(?:success|green)|ci\s*met)$",
    re.I,
)
_CI_ONLY_TOKEN = re.compile(
    r"\b(?:ci(?:_|\s)?fitness|fitness\s*green|github\s*actions?|ci\s*met|actions?\s*success)\b",
    re.I,
)


def _load_profile(root: Path) -> tuple[dict[str, Any] | None, str]:
    path = root / PROFILE_REL
    if not path.is_file():
        return None, f"missing {PROFILE_REL}"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, f"invalid JSON in {PROFILE_REL}"
    if not isinstance(data, dict):
        return None, f"{PROFILE_REL} must be object"
    return data, ""


def _glob_match(rel: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return rel == prefix or rel.startswith(prefix + "/")
    return fnmatch.fnmatch(rel, pattern)


def is_graded_subject_path(root: Path, rel_posix: str) -> bool:
    """True when rel is a graded subject path per hub-gate-diff-profile SSOT."""
    normalized = _norm_rel(rel_posix)
    profile, err = _load_profile(root)
    if profile is None:
        return False
    excludes = profile.get("graded_subject_exclude_globs")
    if isinstance(excludes, list):
        for pat in excludes:
            if isinstance(pat, str) and _glob_match(normalized, pat):
                return False
    globs = profile.get("graded_subject_globs")
    if not isinstance(globs, list):
        return False
    for pat in globs:
        if isinstance(pat, str) and _glob_match(normalized, pat):
            return True
    return False


def _norm_rel(rel: str) -> str:
    """Normalize a repo-relative path without stripping leading-dot directories such as .nlc/."""
    normalized = rel.replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _normalize_path_list(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, str) and item.strip():
            out.append(_norm_rel(item))
    return out


def _normalize_changed_paths(data: dict[str, Any]) -> list[str]:
    """Normalize a Candidate path list. CI must pass git-derived paths, never package fields."""
    return _normalize_path_list(data.get("changed_paths"))


def is_hub_compile_root(root: Path) -> bool:
    """True when root is the NLC hub compile tree (CHARTER + hub-gate-diff profile)."""
    return (root / "CHARTER.md").is_file() and (root / PROFILE_REL).is_file()


def _resolve_merge_base(root: Path) -> str | None:
    for ref in DEFAULT_BASE_REFS:
        proc = subprocess.run(
            ["git", "merge-base", "HEAD", ref],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            sha = (proc.stdout or "").strip()
            if sha:
                return sha
    return None


def derived_changed_paths(root: Path) -> list[str]:
    """Return repo-relative paths from git diff <merge-base origin/release/v0.3.0>..HEAD."""
    base = _resolve_merge_base(root)
    if not base:
        return []
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base}..HEAD"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return _normalize_path_list((proc.stdout or "").splitlines())


def is_hub_material_path(root: Path, rel_posix: str) -> bool:
    """True when a changed path makes the hub produce profile mandatory."""
    normalized = _norm_rel(rel_posix)
    if is_gate_set_path(root, normalized) or is_graded_subject_path(root, normalized):
        return True
    profile, _err = _load_profile(root)
    globs: list[str] = list(_DEFAULT_HUB_MATERIAL_GLOBS)
    if profile is not None:
        extra = profile.get("hub_material_globs")
        if isinstance(extra, list) and extra:
            globs = [p for p in extra if isinstance(p, str)]
    for pat in globs:
        if _glob_match(normalized, pat):
            return True
    return False


def derive_hub_scope(root: Path) -> tuple[bool, list[str]]:
    """Derive hub_material and changed_paths from git. Never read those fields from a package."""
    changed = derived_changed_paths(root)
    hub = is_hub_compile_root(root) or any(is_hub_material_path(root, p) for p in changed)
    return hub, changed


def validate_property_leaf_goals(data: dict[str, Any]) -> tuple[bool, str]:
    """S-HUB-GOAL-TREE: hub_goal_tree with non-empty property_leaf_goals."""
    tree = data.get("hub_goal_tree")
    if not isinstance(tree, dict):
        return False, "HUB_GOAL_TREE: hub_goal_tree missing or not object"
    root_goal = str(tree.get("root_goal_id") or "").strip()
    if not root_goal:
        return False, "HUB_GOAL_TREE: root_goal_id missing"
    leaves = tree.get("property_leaf_goals")
    if not isinstance(leaves, list) or len(leaves) == 0:
        return False, "HUB_GOAL_TREE: property_leaf_goals must be non-empty array"
    for index, leaf in enumerate(leaves):
        if not isinstance(leaf, dict):
            return False, f"HUB_GOAL_TREE: property_leaf_goals[{index}] must be object"
        leaf_id = str(leaf.get("leaf_id") or "").strip()
        statement = str(leaf.get("statement") or "").strip()
        exit_status = str(leaf.get("exit_status") or "").strip()
        evidence = str(leaf.get("evidence_path") or leaf.get("evidence_ref") or "").strip()
        if not leaf_id:
            return False, f"HUB_GOAL_TREE: property_leaf_goals[{index}].leaf_id missing"
        if not statement:
            return False, f"HUB_GOAL_TREE: property_leaf_goals[{index}].statement missing"
        if not exit_status:
            return False, f"HUB_GOAL_TREE: property_leaf_goals[{index}].exit_status missing"
        if not evidence:
            return False, f"HUB_GOAL_TREE: property_leaf_goals[{index}] evidence missing"
    return True, f"{len(leaves)} property leaf goal(s)"


def validate_hub_exit_not_ci_only(data: dict[str, Any]) -> tuple[bool, str]:
    """R-HUB-EXIT: terminal exit may not name only CI / fitness / Actions success."""
    status = str(data.get("ssot_exit_status") or "").strip()
    if not status:
        return False, "R-HUB-EXIT: ssot_exit_status missing"
    if _CI_ONLY_EXIT.match(status):
        return False, "R-HUB-EXIT: ssot_exit_status names only CI/fitness green"
    terminal = data.get("terminal_exit")
    if isinstance(terminal, str) and terminal.strip():
        if _CI_ONLY_EXIT.match(terminal.strip()):
            return False, "R-HUB-EXIT: terminal_exit names only CI/fitness green"
    leaves_ok, _ = validate_property_leaf_goals(data)
    if not leaves_ok:
        return False, "R-HUB-EXIT: property leaf goals required for hub material exit"
    if _CI_ONLY_TOKEN.fullmatch(status.replace("_", " ")):
        return False, "R-HUB-EXIT: ssot_exit_status is CI-only wording"
    return True, "hub material exit names property goals"


def validate_hub_gate_diff_role_separation(
    root: Path, data: dict[str, Any]
) -> tuple[bool, str]:
    """R-HUB-SAME-PACKAGE-REFUSE when changed_paths touch gate-set and graded subject."""
    changed = _normalize_changed_paths(data)
    if not changed:
        return True, "no changed_paths declared"
    gate_hits = [p for p in changed if is_gate_set_path(root, p)]
    subject_hits = [p for p in changed if is_graded_subject_path(root, p)]
    if not gate_hits or not subject_hits:
        return True, "gate-set and graded subject not both in changed_paths"
    producer = str(data.get("producer_role") or "").strip().casefold()
    auditor = str(data.get("adversarial_auditor_role") or "").strip().casefold()
    reviewer_receipt = data.get("adversarial_reviewer_receipt")
    has_reviewer_receipt = isinstance(reviewer_receipt, dict) and bool(
        str(reviewer_receipt.get("reviewer_role") or "").strip()
    )
    if producer and auditor and producer != auditor and has_reviewer_receipt:
        return True, "gate+subject diff with separate adversarial reviewer receipt"
    return (
        False,
        "HUB_GATE_DIFF_ROLE_SEPARATION: same package changes gate-set and graded "
        "subject without separate adversarial reviewer receipt",
    )


def validate_gate_set_change_receipts(root: Path, data: dict[str, Any]) -> tuple[bool, str]:
    """R-GATE-SET-NO-SILENT-WEAKEN for paths declared in changed_paths."""
    changed = _normalize_changed_paths(data)
    gate_paths = [p for p in changed if is_gate_set_path(root, p)]
    if not gate_paths:
        return True, "no gate-set paths in changed_paths"
    errors = gate_paths_manifest_errors(root, gate_paths)
    if errors:
        return False, f"R-GATE-SET-NO-SILENT-WEAKEN: {errors[0]}"
    return True, f"{len(gate_paths)} gate-set path(s) match receipts"


def validate_hub_brief(root: Path, data: dict[str, Any]) -> tuple[bool, str]:
    """R-HUB-BRIEF-FORBID-WEAKEN: committed brief names every leaf id and the forbid clause."""
    ref = str(data.get("brief_ref") or "").strip()
    if not ref:
        return False, "R-HUB-BRIEF-FORBID-WEAKEN: brief_ref missing"
    rel = _norm_rel(ref)
    path = root / rel
    if not path.is_file():
        return False, f"R-HUB-BRIEF-FORBID-WEAKEN: brief {rel} not committed"
    text = path.read_text(encoding="utf-8")
    for needle in FORBID_CLAUSE_NEEDLES:
        if needle not in text:
            return False, f"R-HUB-BRIEF-FORBID-WEAKEN: brief missing forbid clause {needle!r}"
    tree = data.get("hub_goal_tree")
    leaves = tree.get("property_leaf_goals") if isinstance(tree, dict) else None
    if not isinstance(leaves, list):
        return False, "R-HUB-BRIEF-FORBID-WEAKEN: property leaf ids required"
    for index, leaf in enumerate(leaves):
        if not isinstance(leaf, dict):
            continue
        leaf_id = str(leaf.get("leaf_id") or "").strip()
        if leaf_id and leaf_id not in text:
            return False, f"R-HUB-BRIEF-FORBID-WEAKEN: brief missing leaf id {leaf_id}"
        if not leaf_id:
            return False, f"R-HUB-BRIEF-FORBID-WEAKEN: property_leaf_goals[{index}].leaf_id missing"
    return True, "brief names property leaves and forbid clause"


def validate_hub_material_package(
    root: Path, data: dict[str, Any]
) -> tuple[bool, str, str]:
    """Validate a hub-material produce package; hub_material and changed_paths are git-derived."""
    hub, changed = derive_hub_scope(root)
    if not hub:
        return True, "ok", "not hub_material"
    effective = dict(data)
    effective["changed_paths"] = changed
    ok, reason = validate_property_leaf_goals(effective)
    if not ok:
        return False, "handoff_refused", reason
    ok, reason = validate_hub_exit_not_ci_only(effective)
    if not ok:
        return False, "handoff_refused", reason
    ok, reason = validate_hub_brief(root, effective)
    if not ok:
        return False, "handoff_refused", reason
    ok, reason = validate_hub_gate_diff_role_separation(root, effective)
    if not ok:
        return False, "handoff_refused", reason
    ok, reason = validate_gate_set_change_receipts(root, effective)
    if not ok:
        return False, "handoff_refused", reason
    return True, "ok", "hub material produce package valid"


def validate_hub_material_fixture(data: dict[str, Any], check: str) -> tuple[bool, str]:
    """Validate one hub_material requirement for fitness fixture scans (check id)."""
    if check == "principle_subgoals":
        return validate_property_leaf_goals(data)
    if check == "property_exit":
        return validate_hub_exit_not_ci_only(data)
    return False, f"unknown check {check}"
