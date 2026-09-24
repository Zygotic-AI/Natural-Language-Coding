"""ADR 0004/0005 produce package validation and handoff_refused preflight."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from nlc_requirements import hub_tool



def _qm():
    path = Path(__file__).resolve().parents[2] / "fitness-quality-metric.py"
    spec = importlib.util.spec_from_file_location("fitness_quality_metric", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("fitness-quality-metric unavailable")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def validate_role_separation(data: dict[str, Any]) -> tuple[bool, str]:
    """ADR 0003 / CS5: producer and final adversarial auditor must differ when both set."""
    producer = str(data.get("producer_role") or "").strip().casefold()
    auditor = str(data.get("adversarial_auditor_role") or "").strip().casefold()
    if producer and auditor and producer == auditor:
        return (
            False,
            "ROLE_SEPARATION: producer_role must differ from adversarial_auditor_role",
        )
    return True, ""


def validate_produce_package(data: dict[str, Any]) -> tuple[bool, str, str]:
    """Returns (ok, kind, reason) where kind is handoff_refused|fail|ok."""
    ok_sep, sep_reason = validate_role_separation(data)
    if not ok_sep:
        return False, "handoff_refused", sep_reason
    qm = _qm()
    ok, reason = qm.validate_q1_cs9_produce_package(data)
    if not ok:
        return False, "handoff_refused", reason
    leaf = data.get("ssot_leaf_ids")
    status = data.get("ssot_exit_status")
    if not leaf or not isinstance(leaf, list) or len(leaf) == 0:
        return False, "handoff_refused", "SSOT_EXIT_EVIDENCE: ssot_leaf_ids missing"
    if not status or not str(status).strip():
        return False, "handoff_refused", "SSOT_EXIT_EVIDENCE: ssot_exit_status missing"
    if data.get("quality_snapshot"):
        ok2, reason2 = qm.validate_q2_adversarial(data)
        if not ok2:
            return False, "fail", reason2
    return True, "ok", "produce package valid"


def load_and_validate(path: Path) -> tuple[bool, str, str]:
    if not path.is_file():
        return False, "handoff_refused", "missing produce package"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False, "handoff_refused", "invalid produce package JSON"
    return validate_produce_package(data)


def preflight_handoff(root: Path) -> int:
    """Exit 0 MET, 2 handoff_refused, 1 FAIL."""
    path = root / ".nlc" / "produce-package.json"
    ok, kind, reason = load_and_validate(path)
    if ok:
        print(f"handoff_preflight:MET {reason}")
        return 0
    if kind == "handoff_refused":
        print(f"handoff_refused: {reason}", file=sys.stderr)
        if "SSOT_EXIT_EVIDENCE" in reason:
            print("handoff_refused: SSOT_EXIT_EVIDENCE", file=sys.stderr)
        return 2
    print(f"handoff_refused: produce incomplete — {reason}", file=sys.stderr)
    return 2


def main() -> int:
    import argparse

    hub_tool()
    parser = argparse.ArgumentParser(description="Produce package preflight (ADR 0004)")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    return preflight_handoff(args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
