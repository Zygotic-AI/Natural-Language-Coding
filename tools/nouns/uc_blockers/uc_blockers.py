"""USE-CASE blockers for ./nlc verify (UC1, UC3–UC5, UC12–UC13, UC20)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import re
import subprocess
import sys
from pathlib import Path

PRIMITIVE_NAMES = {
    "read",
    "write",
    "return",
    "log",
    "display",
    "transmit",
    "copy",
    "retain",
    "retry",
    "wait",
    "ship",
}


def _hub_skip(root: Path) -> bool:
    from nlc_pipeline import is_hub_repo

    return is_hub_repo(root)


def _compiled_surface(root: Path) -> bool:
    if (root / "goals").is_dir() and any((root / "goals").iterdir()):
        return True
    domain = root / "domain"
    if domain.is_dir():
        for path in domain.rglob("*.py"):
            if path.is_file():
                return True
    return False


def interview_packet_blockers(root: Path) -> list[str]:
    """UC1: bind-ready interview packet before compiled product exists."""
    if _hub_skip(root):
        return []
    if not _compiled_surface(root):
        return []
    path = root / ".nlc" / "interview-packet.json"
    if not path.is_file():
        return [
            "missing .nlc/interview-packet.json (UC1 — complete /interview bind-ready handoff)"
        ]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["invalid .nlc/interview-packet.json"]
    if not data.get("bind_ready"):
        return ["interview packet bind_ready is false (finish /interview before generate)"]
    if not str(data.get("outcome", "")).strip():
        return ["interview packet missing outcome one-line"]
    goals = data.get("goals")
    if not isinstance(goals, list) or not goals:
        return ["interview packet must name at least one goal id or document explicit none"]
    reqs = data.get("requirements")
    if not isinstance(reqs, list) or not reqs:
        return [
            "interview packet missing requirements[] "
            "(ADR ids, standards, or Waived: reason per /interview gate)"
        ]
    domains = data.get("knowledge_domains")
    if not isinstance(domains, list) or not domains:
        return [
            "interview packet missing knowledge_domains[] "
            "(knowledge-steward load-knowledge-domain before bind-ready)"
        ]
    return []


def proposed_adr_blockers(root: Path) -> list[str]:
    """UC3: prose requirements cannot ship as only policy — ratify ADRs first."""
    if _hub_skip(root):
        return []
    if not _compiled_surface(root):
        return []
    from nlc_adr_scan import list_pending_adrs

    pending = list_pending_adrs(root / "adrs")
    if not pending:
        return []
    show = ", ".join(pending[:4]) + ("…" if len(pending) > 4 else "")
    return [f"UC3 requirements gate: Proposed ADR(s) still open: {show}"]


def goal_bindings_narrow_blockers(root: Path) -> list[str]:
    """UC9 v2: multi-goal repos must declare goal-bindings for rule blast radius."""
    if _hub_skip(root):
        return []
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    goals_dir = root / "goals"
    if not goals_dir.is_dir():
        return []
    goal_ids = [d.name for d in goals_dir.iterdir() if d.is_dir()]
    if len(goal_ids) < 2:
        return []
    bindings = root / "rules" / "goal-bindings.json"
    if bindings.is_file():
        return []
    return [
        "UC9 blast radius: multiple goals but missing rules/goal-bindings.json "
        "(narrow rule-tagged regen per IMPACT-GRAPH.md)"
    ]


def _engine_runtime_tags_from_adopted(root: Path) -> set[str]:
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return set()
    try:
        rows = json.loads(adopted.read_text(encoding="utf-8")).get("adoptions") or []
    except json.JSONDecodeError:
        return set()
    tags: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        match = row.get("match") or {}
        for key in ("tags_all", "tags_any"):
            for t in match.get(key) or []:
                ts = str(t)
                if ts == "engine.runtime" or ts.startswith("engine.runtime."):
                    tags.add(ts)
    return tags


def engine_runtime_tag_strict_blockers(root: Path) -> list[str]:
    """UC13 v2: goal engine_runtime must match adopted engine.runtime.<name> tag."""
    if _hub_skip(root):
        return []
    goals = root / "goals"
    if not goals.is_dir():
        return []
    required: list[tuple[str, str]] = []
    for gdir in goals.iterdir():
        if not gdir.is_dir():
            continue
        meta = gdir / "goal.json"
        if not meta.is_file():
            continue
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not data.get("durable"):
            continue
        rt = data.get("engine_runtime")
        if not rt:
            continue
        required.append((gdir.name, str(rt).strip().lower()))
    if not required:
        return []
    rule_tags = _engine_runtime_tags_from_adopted(root)
    if not rule_tags:
        return []
    violations: list[str] = []
    for gid, rt in required:
        specific = f"engine.runtime.{rt}"
        if specific in rule_tags:
            continue
        if "engine.runtime" in rule_tags and specific not in rule_tags:
            violations.append(
                f"goal {gid} engine_runtime={rt!r} rejects bare engine.runtime; need {specific}"
            )
        else:
            violations.append(f"goal {gid} engine_runtime={rt!r} needs adopted tag {specific}")
    if not violations:
        return []
    return ["UC13 engine.runtime strict: " + "; ".join(violations[:4])]


def durable_rule_blockers(root: Path) -> list[str]:
    """UC13: durable goals require engine.runtime rule row in adopted.json."""
    if _hub_skip(root):
        return []
    goals = root / "goals"
    if not goals.is_dir():
        return []
    needs_engine = False
    for gdir in goals.iterdir():
        if not gdir.is_dir():
            continue
        meta = gdir / "goal.json"
        if not meta.is_file():
            continue
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("durable") or data.get("engine_runtime"):
            needs_engine = True
            break
    if not needs_engine:
        return []
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return ["UC13 durable engine: durable goal requires rules/adopted.json engine.runtime rule"]
    try:
        rows = json.loads(adopted.read_text(encoding="utf-8")).get("adoptions") or []
    except json.JSONDecodeError:
        return ["UC13 durable engine: invalid rules/adopted.json"]
    for row in rows:
        if not isinstance(row, dict):
            continue
        match = row.get("match") or {}
        tags_all = match.get("tags_all") or []
        tags_any = match.get("tags_any") or []
        for t in list(tags_all) + list(tags_any):
            ts = str(t)
            if ts == "engine.runtime" or ts.startswith("engine.runtime."):
                return []
    return [
        "UC13 durable engine: add adopted rule matching engine.runtime "
        "(goal.durable ∧ wrong runtime → forbid)"
    ]


def rule_runner_blockers(root: Path) -> list[str]:
    """UC4: rule IR snapshot matches adopted.json."""
    if _hub_skip(root):
        return []
    from nouns.rule_receipt.rule_receipt import check_semantic_ir

    return check_semantic_ir(root)


def call_tree_blockers(root: Path) -> list[str]:
    """UC20: declared verb primitive inventory matches domain scan."""
    if _hub_skip(root):
        return []
    from nlc_call_tree import check_inventory

    return check_inventory(root)


def upstream_hand_patch_blockers(root: Path) -> list[str]:
    """UC10: generated implementations must record prescribed generate provenance."""
    if _hub_skip(root):
        return []
    goals = root / "goals"
    if not goals.is_dir():
        return []
    from nlc_generate_provenance import provenance_for

    bad: list[str] = []
    for impl in sorted(goals.rglob("implementation.py")):
        rel = str(impl.relative_to(root)).replace("\\", "/")
        prov = provenance_for(root, rel)
        if prov is None or not prov.get("prescribed_path"):
            bad.append(rel)
    if not bad:
        return []
    show = ", ".join(bad[:3]) + ("…" if len(bad) > 3 else "")
    return [
        f"UC10 upstream defect: missing generate provenance for {show} "
        "(use ./nlc maintainer goal-scaffold or rule-emit, not hand-patch)"
    ]


def adr_traceability_blockers(root: Path) -> list[str]:
    """UC3: adopted rules cite Accepted ADRs on disk."""
    if _hub_skip(root):
        return []
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    adrs_dir = root / "adrs"
    if not adrs_dir.is_dir():
        return []
    try:
        rows = json.loads(adopted.read_text(encoding="utf-8")).get("adoptions") or []
    except json.JSONDecodeError:
        return ["invalid rules/adopted.json"]
    bad: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        adr_id = str(row.get("adr_id", "")).strip()
        rid = str(row.get("rule_id", "?"))
        if not adr_id:
            bad.append(f"rule {rid} missing adr_id")
            continue
        num = adr_id.lstrip("0") or "0"
        pattern = f"{int(num):04d}-" if num.isdigit() else adr_id
        matches = list(adrs_dir.glob(f"*{pattern}*.md")) if adrs_dir.is_dir() else []
        if not matches:
            bad.append(f"rule {rid} cites missing ADR file for {adr_id}")
            continue
        text = matches[0].read_text(encoding="utf-8", errors="replace")
        if re.search(r"^\s*-\s*Status:\s*Accepted\s*$", text, re.I | re.M) is None:
            bad.append(f"rule {rid} cites non-Accepted ADR {matches[0].name}")
    if not bad:
        return []
    return ["UC3 ADR traceability: " + "; ".join(bad[:4])]


def rule_ir_blockers(root: Path) -> list[str]:
    """UC4: adopted rules are valid rule IR rows."""
    if _hub_skip(root):
        return []
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    try:
        rows = json.loads(adopted.read_text(encoding="utf-8")).get("adoptions") or []
    except json.JSONDecodeError:
        return ["invalid rules/adopted.json"]
    bad: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            bad.append("adoptions row must be object")
            continue
        rid = row.get("rule_id")
        if not rid:
            bad.append("rule missing rule_id")
        if row.get("effect") not in ("forbid", "must"):
            bad.append(f"rule {rid} missing effect forbid|must")
        match = row.get("match")
        if not isinstance(match, dict):
            bad.append(f"rule {rid} missing match object")
        elif not match.get("primitive") and not match.get("tags_all") and not match.get("tags_any"):
            bad.append(f"rule {rid} match needs primitive or tags")
    if not bad:
        return []
    return ["UC4 rule IR: " + "; ".join(bad[:4])]


def rule_apply_blockers(root: Path) -> list[str]:
    """UC5: compiler-owned markers + must-rule obligation receipts (semantic apply)."""
    if _hub_skip(root):
        return []
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    if not _compiled_surface(root):
        return []
    from nouns.rule_receipt.rule_receipt import check_semantic_apply

    return check_semantic_apply(root)


def closed_set_blockers(root: Path) -> list[str]:
    """UC12: rule primitives/tags stay inside closed SSOT sets."""
    if _hub_skip(root):
        return []
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    try:
        rows = json.loads(adopted.read_text(encoding="utf-8")).get("adoptions") or []
    except json.JSONDecodeError:
        return []
    bad: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        match = row.get("match") or {}
        prim = str(match.get("primitive") or "").strip()
        if prim and prim not in PRIMITIVE_NAMES:
            bad.append(f"unknown primitive {prim!r} in rule {row.get('rule_id')}")
    if not bad:
        return []
    return ["UC12 closed set: " + "; ".join(bad[:4])]


def durable_engine_blockers(root: Path) -> list[str]:
    """UC13: durable goals declare engine runtime expectation in knowledge or goal meta."""
    if _hub_skip(root):
        return []
    goals = root / "goals"
    if not goals.is_dir():
        return []
    durable_goals: list[str] = []
    for gdir in goals.iterdir():
        if not gdir.is_dir():
            continue
        meta = gdir / "goal.json"
        if meta.is_file():
            try:
                data = json.loads(meta.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("durable") or data.get("engine_runtime"):
                durable_goals.append(gdir.name)
    if not durable_goals:
        return []
    facts = root / "knowledge" / "facts.json"
    blob = facts.read_text(encoding="utf-8", errors="replace") if facts.is_file() else ""
    missing = [g for g in durable_goals if g not in blob and "engine.runtime" not in blob]
    if not missing:
        return []
    return [
        "UC13 durable engine: goal(s) "
        + ", ".join(missing[:3])
        + " need engine.runtime fact in knowledge/facts.json or goal.json engine_runtime"
    ]


def primitive_inventory_blockers(root: Path) -> list[str]:
    """UC20: verb bodies must not use interior primitive names as public methods (v1 scan)."""
    if _hub_skip(root):
        return []
    domain = root / "domain"
    if not domain.is_dir():
        return []
    bad: list[str] = []
    reserved = PRIMITIVE_NAMES
    for path in domain.rglob("*.py"):
        if "/tests/" in str(path) or path.name.startswith("test_"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for name in reserved:
            if re.search(rf"\.{name}\s*\(", text):
                bad.append(f"{path.relative_to(root)} uses .{name}()")
    if not bad:
        return []
    show = ", ".join(bad[:3]) + ("…" if len(bad) > 3 else "")
    return [f"UC20 primitive inventory: interior primitive call {show}"]


def interview_requirements_sync_blockers(root: Path) -> list[str]:
    """UC3: bind-ready interview cannot coexist with requirements-sync-pending."""
    if _hub_skip(root):
        return []
    pending = root / ".nlc" / "requirements-sync-pending.json"
    if not pending.is_file():
        return []
    packet = root / ".nlc" / "interview-packet.json"
    if not packet.is_file():
        return []
    try:
        data = json.loads(packet.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not data.get("bind_ready"):
        return []
    return [
        "UC3 requirements sync: bind_ready interview packet but requirements-sync-pending "
        "(ratify pack/ADR changes or clear pending after regen)"
    ]


def non_python_adapter_blockers(root: Path) -> list[str]:
    """UC16: non-Python sources require declared language adapters."""
    if _hub_skip(root):
        return []
    from nlc_language_scan import scan

    found = scan(root)
    extra = [lang for lang in found if lang != "python"]
    if not extra:
        return []
    adapters = root / ".nlc" / "language-adapters.json"
    approved: set[str] = set()
    if adapters.is_file():
        try:
            data = json.loads(adapters.read_text(encoding="utf-8"))
            approved = set(data.get("approved") or [])
        except json.JSONDecodeError:
            return ["UC16: invalid .nlc/language-adapters.json"]
    missing = sorted(set(extra) - approved)
    if not missing:
        return []
    return [
        "UC16 code packs: non-Python sources "
        + ", ".join(missing)
        + " without LANGUAGE-SCANNER adapter (declare .nlc/language-adapters.json approved[])"
    ]


def ensure_before_generate_stamp(root: Path) -> list[str]:
    """UC18: maintainer generate tools require fresh before-generate stamp."""
    from nlc_guide_state import before_generate_stamp_valid

    if _hub_skip(root):
        return []
    if not _compiled_surface(root):
        return []
    if not before_generate_stamp_valid(root, max_age_seconds=86400):
        return [
            "before-generate stamp missing or stale "
            "(./nlc maintainer guide before-generate --scope <topic>)"
        ]
    return []
