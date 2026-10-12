"""ADR 0051 SG1/SG3 hub material produce package validation."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import fnmatch
import json
import re
from pathlib import Path
from typing import Any

from nouns.gate_set_manifest.gate_set_manifest import gate_paths_manifest_errors
from nouns.gate_set.gate_set import is_gate_set_path

PROFILE_REL = "integrity/hub-gate-diff-profile.json"

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
    normalized = rel_posix.replace("\\", "/").lstrip("./")
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


def _normalize_changed_paths(data: dict[str, Any]) -> list[str]:
    raw = data.get("changed_paths")
    if not isinstance(raw, list):
        return []
    out: list[str] = []
    for item in raw:
        if isinstance(item, str) and item.strip():
            out.append(item.replace("\\", "/").lstrip("./"))
    return out


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


def validate_hub_material_package(
    root: Path, data: dict[str, Any]
) -> tuple[bool, str, str]:
    """Validate hub_material produce package; returns (ok, kind, reason)."""
    if not data.get("hub_material"):
        return True, "ok", "not hub_material"
    ok, reason = validate_property_leaf_goals(data)
    if not ok:
        return False, "handoff_refused", reason
    ok, reason = validate_hub_exit_not_ci_only(data)
    if not ok:
        return False, "handoff_refused", reason
    ok, reason = validate_hub_gate_diff_role_separation(root, data)
    if not ok:
        return False, "handoff_refused", reason
    ok, reason = validate_gate_set_change_receipts(root, data)
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
