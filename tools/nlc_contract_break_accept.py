"""ADR 0006: manager accepts requirement/ADR for breaking contract changes."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from nlc_requirements import hub_tool

ACCEPT_PATH = ".nlc/contract-break-accept.json"


def load_acceptances(root: Path) -> list[dict]:
    path = root / ACCEPT_PATH
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    rows = data.get("acceptances") or []
    return [r for r in rows if isinstance(r, dict)]


def append_acceptance(
    root: Path,
    *,
    schema_path: str,
    adr_id: str,
    accepted_by: str,
    requirement_id: str | None = None,
) -> None:
    rel = schema_path.replace("\\", "/").lstrip("./")
    if not adr_id.strip():
        raise ValueError("adr_id is required")
    if not accepted_by.strip():
        raise ValueError("accepted_by is required (role language, not a person name)")
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    path = nlc / "contract-break-accept.json"
    records = load_acceptances(root)
    records.append(
        {
            "schema_path": rel,
            "adr_id": adr_id.strip(),
            "requirement_id": (requirement_id or "").strip() or None,
            "accepted_by": accepted_by.strip(),
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    )
    path.write_text(
        json.dumps({"schema": 1, "acceptances": records}, indent=2) + "\n",
        encoding="utf-8",
    )


def _load_c10():
    import importlib.util

    tools = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("fitness_c10", tools / "fitness-c10.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("fitness-c10.py unavailable")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def acceptance_blockers(root: Path) -> list[str]:
    import product_tree

    c10 = _load_c10()
    breaking_contract_events = c10.breaking_contract_events
    has_adr = c10.has_adr

    if product_tree.is_specimen(root):
        return []
    events = breaking_contract_events(root)
    if not events:
        return []
    if not has_adr(root):
        return []

    by_path: dict[str, list[dict]] = {}
    for row in load_acceptances(root):
        sp = str(row.get("schema_path", "")).replace("\\", "/")
        if sp:
            by_path.setdefault(sp, []).append(row)

    blockers: list[str] = []
    for schema_rel, detail in events:
        key = schema_rel.replace("\\", "/")
        rows = by_path.get(key) or []
        ok = False
        for row in rows:
            if not str(row.get("adr_id", "")).strip():
                continue
            if not str(row.get("accepted_by", "")).strip():
                continue
            ok = True
            break
        if not ok:
            blockers.append(
                f"breaking contract {key} ({detail}) needs manager acceptance "
                f"(./nlc maintainer contract-break-accept --schema {key} --adr <id> "
                f"--accepted-by 'role:…')"
            )
    return blockers


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(
        description="Record ADR 0006 acceptance for a breaking published contract",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--schema", required=True, help="Repo-relative schema path")
    parser.add_argument("--adr", required=True, help="ADR id that justifies the break")
    parser.add_argument("--requirement", default=None, help="Optional requirement id")
    parser.add_argument("--accepted-by", required=True, help="Role label (not a person name)")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        append_acceptance(
            root,
            schema_path=args.schema,
            adr_id=args.adr,
            accepted_by=args.accepted_by,
            requirement_id=args.requirement,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"contract-break-accept: MET schema={args.schema}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
