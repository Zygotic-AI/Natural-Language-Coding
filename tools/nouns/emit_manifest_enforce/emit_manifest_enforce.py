"""X3: full emit-manifest enforcement (NLC-0024-06)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOUNDARY = "bba-emit"

HUB_ROOT = Path(__file__).resolve().parents[3]

REQUIRED = (
    "schema",
    "emit_id",
    "action_id",
    "artifact_path",
    "bound_adr_ids",
    "audit",
    "gate",
    "decision_trace",
    "thought_anchors",
    "unused",
)


def schema_path(hub_root: Path | None = None) -> Path:
    hub = (hub_root or HUB_ROOT).resolve()
    return hub / "docs" / "nlc" / "emit-manifest.schema.json"


def load_schema(hub_root: Path | None = None) -> dict | None:
    path = schema_path(hub_root)
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data: object, schema: dict | None) -> list[str]:
    v: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    for key in REQUIRED:
        if key not in data:
            v.append(f"missing {key}")
    if data.get("schema") != "nlc-emit-manifest/v0":
        v.append("schema must be nlc-emit-manifest/v0")
    if data.get("unused") != "na":
        v.append('unused must be "na"')
    audit = data.get("audit") if isinstance(data.get("audit"), dict) else {}
    status = audit.get("status")
    if status not in {"pass", "fail", "na"}:
        v.append(f"audit.status must be pass|fail|na, got {status!r}")
    if not audit.get("path"):
        v.append("audit.path required")
    gate = data.get("gate") if isinstance(data.get("gate"), dict) else {}
    if gate.get("default") != "closed":
        v.append("gate.default must be closed")
    if not isinstance(data.get("bound_adr_ids"), list):
        v.append("bound_adr_ids must be a list")
    if not isinstance(data.get("decision_trace"), list):
        v.append("decision_trace must be a list")
    if not isinstance(data.get("thought_anchors"), list):
        v.append("thought_anchors must be a list")
    return v


def iter_manifests(root: Path) -> list[Path]:
    if root.is_file() and root.name == "emit-manifest.json":
        return [root.resolve()]
    return sorted({p.resolve() for p in root.rglob("emit-manifest.json") if p.is_file()})


def main(argv: list[str] | None = None, hub_root: Path | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[0]).resolve() if args else Path.cwd()
    schema = load_schema(hub_root)
    paths = iter_manifests(root)
    violations: list[str] = []
    if schema is None:
        violations.append("missing docs/nlc/emit-manifest.schema.json")
    if not paths:
        print("RESULT:MET")
        print("note: no emit-manifest.json found")
        return 0
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            violations.append(f"{path}: invalid json ({exc})")
            continue
        for item in validate(data, schema):
            violations.append(f"{path}: {item}")
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0
