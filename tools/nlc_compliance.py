"""ADR enforcement helpers for verify / verify-deep."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

EMPTY_WAIVED = re.compile(r"^\s*Waived:\s*$", re.M)

def _validate_q2_adversarial(data: dict) -> tuple[bool, str]:
    import importlib.util

    path = Path(__file__).resolve().parent / "fitness-quality-metric.py"
    spec = importlib.util.spec_from_file_location("fitness_quality_metric", path)
    if spec is None or spec.loader is None:
        return False, "fitness-quality-metric unavailable"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validate_q2_adversarial(data)


def _parse_utc(ts: str) -> datetime | None:
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def rule_conflict_blockers(root: Path) -> list[str]:
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    from nlc_pipeline import is_hub_repo

    if is_hub_repo(root):
        return []
    import subprocess
    import sys

    script = Path(__file__).resolve().parent / "check-rule-adoption.py"
    proc = subprocess.run(
        [sys.executable, str(script), str(adopted)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return []
    return ["adopted rules conflict (run ./nlc maintainer check-rules)"]


def _product_paths(root: Path) -> list[Path]:
    out: list[Path] = []
    for name in ("goals", "domain"):
        base = root / name
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix not in {".pyc", ".pyo"}:
                out.append(path)
    return out


def before_generate_stamp_blockers(root: Path) -> list[str]:
    product = _product_paths(root)
    if not product:
        return []
    stamp_path = root / ".nlc" / "before-generate-stamp.json"
    if not stamp_path.is_file():
        return [
            "product files exist without before-generate stamp "
            "(./nlc maintainer guide before-generate)"
        ]
    try:
        stamp = json.loads(stamp_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["invalid .nlc/before-generate-stamp.json"]
    if not stamp.get("ok"):
        return ["before-generate stamp not OK"]
    at = _parse_utc(str(stamp.get("at", "")))
    if at is None:
        return ["before-generate stamp has no valid timestamp"]
    stale: list[str] = []
    for path in product:
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        if mtime > at:
            rel = path.relative_to(root)
            stale.append(str(rel).replace("\\", "/"))
    if not stale:
        return []
    show = ", ".join(stale[:5]) + ("…" if len(stale) > 5 else "")
    return [
        f"product changed after before-generate stamp: {show} "
        "(re-run ./nlc maintainer guide before-generate)"
    ]


def _goal_implementations(root: Path) -> list[Path]:
    goals = root / "goals"
    if not goals.is_dir():
        return []
    return sorted(goals.rglob("implementation.py"))


def gate_record_blockers(root: Path) -> list[str]:
    impls = _goal_implementations(root)
    if not impls:
        return []
    records_path = root / ".nlc" / "gate-records.json"
    if not records_path.is_file():
        return [
            "goal implementation(s) exist without gate records "
            "(./nlc maintainer gate-record after each PLANIT 6.5 PASS)"
        ]
    try:
        data = json.loads(records_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["invalid .nlc/gate-records.json"]
    records: list[dict] = list(data.get("records") or [])
    by_artifact: dict[str, dict] = {}
    for rec in records:
        if rec.get("outcome") != "PASS":
            continue
        art = str(rec.get("artifact", "")).replace("\\", "/")
        if not art:
            continue
        at = _parse_utc(str(rec.get("at", "")))
        if at is None:
            continue
        prev = by_artifact.get(art)
        if prev is None or at > _parse_utc(str(prev.get("at", ""))):
            by_artifact[art] = rec
    bad: list[str] = []
    for path in impls:
        rel = str(path.relative_to(root)).replace("\\", "/")
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        rec = by_artifact.get(rel)
        if rec is None:
            bad.append(rel)
            continue
        at = _parse_utc(str(rec.get("at", "")))
        if at is None or mtime > at:
            bad.append(rel)
    if not bad:
        return []
    show = ", ".join(bad[:5]) + ("…" if len(bad) > 5 else "")
    return [f"gate PASS not recorded after last edit: {show}"]


def change_adversarial_blockers(root: Path) -> list[str]:
    from nlc_pipeline import is_hub_repo

    if is_hub_repo(root):
        return []
    if not _goal_implementations(root):
        return []
    path = root / ".nlc" / "change-adversarial.json"
    if not path.is_file():
        return [
            "compiled goals present but missing .nlc/change-adversarial.json "
            "(bbp-reviewer artifact for this change)"
        ]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["invalid .nlc/change-adversarial.json"]
    ok, reason = _validate_q2_adversarial(data)
    if not ok:
        return [f"change-adversarial invalid: {reason}"]
    return []


def waiver_blockers(root: Path) -> list[str]:
    bad: list[str] = []
    for path in sorted((root / "adrs").glob("*.md")) if (root / "adrs").is_dir() else []:
        text = path.read_text(encoding="utf-8", errors="replace")
        if EMPTY_WAIVED.search(text):
            bad.append(path.name)
    if not bad:
        return []
    return [f"empty Waived: line in {', '.join(bad)} — add reason or ratify"]


def plan_audit_blockers(root: Path) -> list[str]:
    pip = root / ".nlc" / "planit-in-progress.json"
    if not pip.is_file():
        return []
    try:
        data = json.loads(pip.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not data.get("active"):
        return []
    path = root / ".nlc" / "plan-audit.json"
    if not path.is_file():
        return [
            "planit active but missing .nlc/plan-audit.json "
            "(./nlc maintainer plan-audit --from <bbp-reviewer-export.json>)"
        ]
    try:
        audit = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ["invalid .nlc/plan-audit.json"]
    ok, reason = _validate_q2_adversarial(audit)
    if not ok:
        return [f"plan-audit invalid: {reason}"]
    return []


def produce_package_blockers(root: Path) -> list[str]:
    from nlc_pipeline import is_hub_repo
    from nlc_produce_package import load_and_validate

    need = is_hub_repo(root) or bool(_goal_implementations(root))
    if not need:
        return []
    path = root / ".nlc" / "produce-package.json"
    ok, kind, reason = load_and_validate(path)
    if ok:
        return []
    if kind == "handoff_refused":
        return [f"produce handoff_refused: {reason}"]
    return [f"produce package invalid: {reason}"]


def verify_fast_blockers(root: Path) -> list[str]:
    reasons: list[str] = []
    reasons.extend(waiver_blockers(root))
    reasons.extend(rule_conflict_blockers(root))
    reasons.extend(before_generate_stamp_blockers(root))
    reasons.extend(gate_record_blockers(root))
    reasons.extend(plan_audit_blockers(root))
    return reasons


def verify_deep_extra_blockers(root: Path) -> list[str]:
    reasons: list[str] = []
    reasons.extend(produce_package_blockers(root))
    reasons.extend(change_adversarial_blockers(root))
    return reasons
