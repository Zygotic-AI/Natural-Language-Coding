"""SSOT checks: TODO compiled-system section vs integrity/uc-product-status.json."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "integrity" / "uc-product-status.json"
SECTION_START = "## Build a compiled system — use-case dependencies"
V1_MARKERS = ("v1 binder", "v1 only", "binder only", "partial", "stub", "v1:")

SPINE_STATUS_PREFIXES = (
    "In force",
    "In force v1",
    "Retired",
    "Expansion only",
)


def load_status(path: Path | None = None) -> dict[str, Any]:
    p = path or STATUS_PATH
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("schema") != 1:
        raise ValueError("uc-product-status.json schema must be 1")
    return data


def gate_configured(status: dict[str, Any]) -> bool:
    ucs = status.get("ucs")
    return isinstance(ucs, dict) and len(ucs) > 0


def _section_lines(text: str) -> list[str]:
    if SECTION_START not in text:
        return []
    chunk = text.split(SECTION_START, 1)[1]
    if "## " in chunk:
        chunk = chunk.split("\n## ", 1)[0]
    return chunk.splitlines()


def _compiled_section_lines(todo_text: str) -> list[str]:
    return _section_lines(todo_text)


def _parse_todo_uc_rows(lines: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in lines:
        if "**UC" not in line:
            if "Requirement packs" in line:
                rows.append({"kind": "PACKS", "line": line, "state": "done" if "✔" in line else "open"})
            continue
        m = re.search(r"\*\*(UC\d+)(?:\s*\(([^)]*))\)\*\*", line)
        if not m:
            continue
        uc_id = m.group(1)
        role = (m.group(2) or "").strip().lower()
        state = "done" if "✔" in line else "open"
        rows.append({"kind": "UC", "id": uc_id, "role": role, "line": line, "state": state})
    return rows


def _is_product_done_row(row: dict[str, str]) -> bool:
    if row.get("kind") != "UC":
        return False
    if row.get("state") != "done":
        return False
    line = row.get("line", "").lower()
    if any(m in line for m in V1_MARKERS):
        return False
    role = row.get("role", "")
    if "product" in role or role == "":
        return True
    return False


def _uc_product_state(status: dict[str, Any], uc_id: str) -> str:
    ucs = status.get("ucs") or {}
    row = ucs.get(uc_id) or {}
    return str(row.get("product") or "open")


def check_todo_vs_status(
    todo_text: str,
    status: dict[str, Any],
    *,
    todo_path: Path | None = None,
) -> list[str]:
    violations: list[str] = []
    if not gate_configured(status):
        violations.append("uc-product-status.json has no ucs map (hollow SSOT gate)")
    lines = _compiled_section_lines(todo_text)
    rows = _parse_todo_uc_rows(lines)

    for row in rows:
        if row.get("kind") != "UC":
            continue
        uc_id = row["id"]
        prod = _uc_product_state(status, uc_id)
        if _is_product_done_row(row) and prod != "closed":
            violations.append(
                f"{uc_id} product @done in TODO but integrity/uc-product-status.json product={prod!r}"
            )
        if prod == "open" and row.get("role", "").find("product") >= 0 and row.get("state") == "done":
            if not any(m in row.get("line", "").lower() for m in V1_MARKERS):
                violations.append(f"{uc_id} product marked done while status SSOT product=open")

    for row in rows:
        if row.get("kind") != "UC":
            continue
        uc_id = row["id"]
        if _uc_product_state(status, uc_id) == "closed":
            product_open = any(
                r.get("id") == uc_id and "product" in r.get("role", "") and r.get("state") == "open"
                for r in rows
            )
            if product_open:
                violations.append(
                    f"{uc_id} product=closed in SSOT but TODO still has open product row"
                )

    packs = status.get("packs_v02") or {}
    hub = status.get("hub_v02") or {}
    for row in rows:
        if row.get("kind") != "PACKS":
            continue
        if row.get("state") != "done":
            continue
        if str(packs.get("product")) != "closed":
            violations.append("Requirement packs product @done but packs_v02.product not closed in SSOT")

    if str(hub.get("pack_ingest")) == "closed":
        for needle in ("☐ Ingest prompt/skill", "☐ **Ingest prompt"):
            if needle in todo_text:
                violations.append(f"hub_v02.pack_ingest closed but TODO still has {needle!r}")

    return violations


def check_todo_evidence_suffix(todo_text: str) -> list[str]:
    """Compiled-system @done rows must cite evidence= landmine or fitness id."""
    violations: list[str] = []
    for line in _compiled_section_lines(todo_text):
        if "✔" not in line or "**UC" not in line:
            if "✔" in line and "Requirement packs" in line:
                if "evidence=" not in line:
                    violations.append("Requirement packs @done missing evidence= suffix")
            continue
        if "evidence=" not in line:
            m = re.search(r"\*\*(UC\d+)", line)
            if m:
                violations.append(f"{m.group(1)} @done missing evidence= suffix")
    return violations


def check_spine_status_vocabulary(use_cases_text: str) -> list[str]:
    violations: list[str] = []
    in_spine = False
    for line in use_cases_text.splitlines():
        if line.startswith("## Spine"):
            in_spine = True
            continue
        if in_spine and line.startswith("## "):
            break
        if not in_spine or "|" not in line or line.strip().startswith("|---"):
            continue
        if line.strip().startswith("| ID"):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 3:
            continue
        status_cell = parts[-1]
        if not status_cell or status_cell.startswith("~~"):
            continue
        if not any(status_cell.startswith(p) for p in SPINE_STATUS_PREFIXES):
            if "UC" in parts[0]:
                violations.append(f"spine status not in vocabulary: {status_cell[:80]!r}")
    beside = False
    for line in use_cases_text.splitlines():
        if "## Beside the spine" in line:
            beside = True
            continue
        if beside and line.startswith("## ") and "Beside" not in line:
            if line.startswith("## Needed") or line.startswith("## Expansion"):
                break
            if not line.startswith("## Beside"):
                break
        if not beside or "|" not in line or line.strip().startswith("|---"):
            continue
        if line.strip().startswith("| ID") or line.strip().startswith("| ["):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 3:
            continue
        status_cell = parts[-1]
        if status_cell.startswith("~~") or "*Retired*" in line or "~~[" in line:
            continue
        if "Requirement packs" in line or "UC19" in line:
            continue
        if status_cell and not any(status_cell.startswith(p) for p in SPINE_STATUS_PREFIXES):
            if re.search(r"UC\d+", line):
                violations.append(f"beside-spine status not in vocabulary: {status_cell[:80]!r}")
    return violations


def check_jobs_vs_status(jobs_text: str, status: dict[str, Any], todo_text: str) -> list[str]:
    """JOBS Blocked rows must not contradict closed UC product in SSOT."""
    violations: list[str] = []
    ucs = status.get("ucs") or {}

    def product_closed(uc: str) -> bool:
        return str((ucs.get(uc) or {}).get("product")) == "closed"

    rules: list[tuple[str, str, str]] = [
        ("J4", "UC1", r"\|\s*J4\s*\|[^|]*\|\s*\*\*Blocked\*\*"),
        ("J5", "UC18", r"\|\s*J5\s*\|[^|]*\|\s*\*\*Blocked\*\*"),
        ("J8", "UC9", r"\|\s*J8\s*\|[^|]*\|\s*\*\*Blocked\*\*"),
        ("J20", "UC13", r"\|\s*J20\s*\|[^|]*\|\s*\*\*Blocked\*\*"),
    ]
    for job_id, uc_id, pattern in rules:
        if product_closed(uc_id) and re.search(pattern, jobs_text):
            violations.append(
                f"{job_id} still Blocked in JOBS-TO-BE-DONE but {uc_id} product=closed in uc-product-status.json"
            )

    if str((status.get("packs_v02") or {}).get("product")) == "closed":
        if re.search(r"\|\s*J16\s*\|[^|]*\|\s*\*\*Blocked\*\*", jobs_text):
            if "export/install not shipped" in jobs_text.lower():
                violations.append("J16 Blocked text contradicts packs_v02.product=closed")

    if "☐ Consume:" in todo_text and str(status.get("hub_v02", {}).get("pack_consume_regen")) == "open":
        if re.search(r"\|\s*J16\s*\|[^|]*\|\s*\*\*Available\*\*", jobs_text):
            pass
    return violations
