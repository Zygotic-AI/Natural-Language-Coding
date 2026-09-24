"""Shared ACTIVE.md parsing + hash for ADR 0029 tools."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone

BOUNDARY = "bba-emit"

ACTIVE_ROW = re.compile(
    r"^\|\s*(\d{4})\s*\|\s*(L-\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|"
)
INDEX_ROW = re.compile(
    r"^\|\s*(\d{4})\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*(L-\d+)\s*\|"
)


def parse_active_rows(text: str) -> list[dict]:
    adrs: list[dict] = []
    for line in text.splitlines():
        m = ACTIVE_ROW.match(line.strip())
        if not m:
            continue
        adrs.append(
            {
                "adr": m.group(1),
                "lineage": m.group(2).strip(),
                "origin": m.group(3).strip(),
                "effective": m.group(4).strip(),
            }
        )
    return adrs


def parse_index_rows(text: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in text.splitlines():
        m = INDEX_ROW.match(line.strip())
        if not m:
            continue
        adr = m.group(1)
        successor = m.group(5).strip()
        rows[adr] = {
            "status": m.group(4).strip(),
            "successor": successor if successor not in ("—", "-", "") else "",
            "lineage": m.group(6).strip(),
        }
    return rows


def active_sha256(adrs: list[dict]) -> str:
    body = "\n".join(f"{a['adr']}:{a['lineage']}" for a in adrs)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def bind_snapshot_payload(active_text: str) -> dict:
    adrs = parse_active_rows(active_text)
    return {
        "schema": 1,
        "source": "adrs/ACTIVE.md",
        "active_sha256": active_sha256(adrs),
        "adrs": adrs,
        "written_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
