"""Dashboard: scan app repo state and refresh .nlc/work-queue.json."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import re
from pathlib import Path

from nlc_pipeline import (
    STAGE_TITLES,
    is_hub_repo,
    load_persisted_items,
    merge_queue_items,
    normalize_stage,
)

from markdown_plain import strip_links
from nlc_adr_scan import list_pending_adrs
RELEASED = re.compile(r"^Released-by:\s*(.*)$", re.I | re.M)
AGENT = re.compile(
    r"\b(agent|ai|bot|assistant|grok|confirmer|claude|gpt|copilot)\b",
    re.I,
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def requirements_incomplete(root: Path) -> bool:
    if list_pending_adrs(root / "adrs"):
        return True
    if (root / ".nlc" / "requirements-sync-pending.json").is_file():
        return True
    if not is_hub_repo(root) and (root / ".nlc" / "lock.json").is_file():
        goals = root / "goals"
        domain = root / "domain"
        has_goal = goals.is_dir() and any(goals.iterdir()) if goals.is_dir() else False
        has_domain = domain.is_dir() and any(domain.iterdir()) if domain.is_dir() else False
        if not has_goal and not has_domain:
            return True
    return False


def scan_rule_conflicts(root: Path) -> list[dict]:
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return []
    from nlc_pipeline import is_hub_repo

    if is_hub_repo(root):
        return []
    import subprocess
    import sys

    hub_script = Path(__file__).resolve().parents[2] / "check-rule-adoption.py"
    proc = subprocess.run(
        [sys.executable, str(hub_script), str(adopted)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return []
    return [
        {
            "id": "rules-conflict",
            "stage": "requirements",
            "label": "Adopted rules conflict",
            "next": "/interview in your agent",
            "priority": 8,
        }
    ]


def scan_planit_in_progress(root: Path) -> list[dict]:
    path = root / ".nlc" / "planit-in-progress.json"
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not data.get("active"):
        return []
    return [
        {
            "id": "planit-active",
            "stage": "build",
            "label": data.get("label", "Build & compile in progress"),
            "next": "/planit in your agent — pick up where you left off",
            "priority": 12,
        }
    ]


def scan_requirements_work(root: Path) -> list[dict]:
    items: list[dict] = []
    items.extend(
        i
        for i in load_persisted_items(root)
        if normalize_stage(str(i.get("stage", ""))) == "requirements"
    )

    pending = list_pending_adrs(root / "adrs")
    if pending:
        n = len(pending)
        items.append(
            {
                "id": "adrs-pending",
                "stage": "requirements",
                "label": f"{n} requirement{'s' if n != 1 else ''} unfinished — ratify",
                "next": "/interview in your agent",
                "detail": ", ".join(pending[:5]) + ("…" if len(pending) > 5 else ""),
                "priority": 10,
            }
        )

    if not is_hub_repo(root) and (root / ".nlc" / "lock.json").is_file():
        goals = root / "goals"
        domain = root / "domain"
        has_goal = goals.is_dir() and any(goals.iterdir()) if goals.is_dir() else False
        has_domain = domain.is_dir() and any(domain.iterdir()) if domain.is_dir() else False
        if not has_goal and not has_domain and not pending:
            items.append(
                {
                    "id": "requirements-new-app",
                    "stage": "requirements",
                    "label": "New requirements — what you're building",
                    "next": "/interview in your agent",
                    "priority": 5,
                }
            )

    flag = root / ".nlc" / "requirements-sync-pending.json"
    if flag.is_file() and not pending:
        items.append(
            {
                "id": "requirements-sync",
                "stage": "requirements",
                "label": "Requirements update — finish sync",
                "next": "/interview in your agent",
                "priority": 25,
            }
        )

    return items


def scan_build_pending(root: Path) -> list[dict]:
    if requirements_incomplete(root):
        return []
    if not (root / ".nlc" / "lock.json").is_file() and not is_hub_repo(root):
        return []

    persisted = [
        i
        for i in load_persisted_items(root)
        if normalize_stage(str(i.get("stage", ""))) == "build"
    ]
    if persisted:
        return persisted

    if is_hub_repo(root):
        return []

    goals = root / "goals"
    has_impl = goals.is_dir() and any(goals.rglob("implementation.py"))
    adrs = list((root / "adrs").glob("*.md"))
    if adrs and not has_impl:
        return [
            {
                "id": "build-after-bind",
                "stage": "build",
                "label": "Build & compile waiting",
                "next": "/planit in your agent",
                "priority": 20,
            }
        ]
    return []


def scan_verify_pending(root: Path) -> list[dict]:
    if requirements_incomplete(root):
        return []
    items = [
        i
        for i in load_persisted_items(root)
        if normalize_stage(str(i.get("stage", ""))) == "verify"
    ]
    if items:
        return items
    from nlc_verify import verify_fast

    goals = root / "goals"
    has_impl = goals.is_dir() and any(goals.rglob("implementation.py"))
    if not has_impl and not is_hub_repo(root):
        return []
    ok, _reasons = verify_fast(root)
    if ok:
        return []
    return [
        {
            "id": "verify-waiting",
            "stage": "verify",
            "label": "Verify before prod",
            "next": "./nlc verify  (if fail: /verify in your agent)",
            "priority": 30,
        }
    ]


def scan_confirm(root: Path) -> list[dict]:
    for name in ("CONFIRM.md", "CONFIRM"):
        path = root / name
        if not path.is_file():
            continue
        text = strip_links(_read_text(path))
        m = RELEASED.search(text)
        if m is None or not m.group(1).strip():
            return [
                {
                    "id": "ship-unsigned",
                    "stage": "maintain",
                    "label": "Release sign-off not recorded",
                    "next": "./nlc ship-check when CONFIRM.md is signed",
                    "priority": 50,
                }
            ]
        if AGENT.search(m.group(1)):
            return [
                {
                    "id": "ship-agent-name",
                    "stage": "maintain",
                    "label": "Released-by must be a person, not an agent",
                    "next": "Edit CONFIRM.md, then ./nlc ship-check",
                    "priority": 50,
                }
            ]
    return []


def scan_regen_queue(root: Path) -> list[dict]:
    if requirements_incomplete(root):
        return []
    path = root / ".nlc" / "delta-regen-queue.json"
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    steps = data.get("steps") or []
    if not steps:
        return []
    n = len(steps)
    return [
        {
            "id": "delta-regen",
            "stage": "build",
            "label": f"{n} rebuild{'s' if n != 1 else ''} after requirements updated",
            "next": "./nlc maintainer regen-continue  (then /planit; regen-advance after each goal)",
            "priority": 15,
        }
    ]


def scan_lock_upgrade(root: Path, installed_hub: str | None) -> list[dict]:
    lock_path = root / ".nlc" / "lock.json"
    if not lock_path.is_file() or not installed_hub:
        return []
    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    pinned = str(lock.get("hub", ""))
    if pinned and pinned != installed_hub:
        return [
            {
                "id": "hub-upgrade",
                "stage": "maintain",
                "label": f"Compiler update available ({pinned} → {installed_hub})",
                "next": "./nlc upgrade",
                "priority": 40,
            }
        ]
    return []


def refresh_work_queue(root: Path, installed_hub: str | None) -> dict:
    scanned: list[dict] = []
    scanned.extend(scan_rule_conflicts(root))
    scanned.extend(scan_requirements_work(root))
    scanned.extend(scan_planit_in_progress(root))
    scanned.extend(scan_build_pending(root))
    scanned.extend(scan_regen_queue(root))
    scanned.extend(scan_verify_pending(root))
    scanned.extend(scan_lock_upgrade(root, installed_hub))
    scanned.extend(scan_confirm(root))

    persisted = load_persisted_items(root)
    items = merge_queue_items(scanned, persisted)

    payload = {"schema": 1, "items": items}
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    (nlc / "work-queue.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    return payload


def format_dashboard(
    root: Path,
    queue: dict,
    hub_version: str,
) -> str:
    lines = [
        "Natural Language Coding",
        "=======================",
        f"Project: {root}",
        f"Compiler: {hub_version}",
        "",
        "Guide (anytime): /interview in your agent — walks you through anything; queue below is unfinished work.",
        "",
        "YOUR QUEUE (Requirements → Build & compile → Verify)",
        "====================================================",
    ]
    items = queue.get("items") or []
    if items:
        n = 0
        last_stage: str | None = None
        for item in items:
            stage = normalize_stage(str(item.get("stage") or "requirements"))
            if stage != last_stage:
                title = STAGE_TITLES.get(stage, stage)
                lines.append("")
                lines.append(f"  [{title}]")
                last_stage = stage
            n += 1
            lines.append(f"  {n}. {item.get('label', '')}")
            detail = item.get("detail")
            if detail:
                lines.append(f"     ({detail})")
            nxt = item.get("next", "")
            if nxt:
                lines.append(f"     → {nxt}")
            from nlc_menu_data import command_map_step

            step = command_map_step(normalize_stage(str(item.get("stage") or "")))
            if step:
                lines.append(f"     (command map step {step})")
    else:
        lines.append("")
        lines.append("  (nothing open)")
        lines.append("     → /interview in your agent")

    from nlc_menu_data import render_short_map_lines

    lines.append("")
    lines.extend(render_short_map_lines())
    return "\n".join(lines)
