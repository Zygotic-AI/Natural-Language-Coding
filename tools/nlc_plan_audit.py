"""Record plan-level adversarial audit artifact (ADR 0003 / planit phase 4)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nlc_requirements import hub_tool


def _validate_q2(data: dict) -> tuple[bool, str]:
    import importlib.util

    path = Path(__file__).resolve().parent / "fitness-quality-metric.py"
    spec = importlib.util.spec_from_file_location("fitness_quality_metric", path)
    if spec is None or spec.loader is None:
        return False, "fitness-quality-metric unavailable"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.validate_q2_adversarial(data)


def install_audit(root: Path, data: dict) -> tuple[bool, str]:
    ok, reason = _validate_q2(data)
    if not ok:
        return False, reason
    dest = root / ".nlc" / "plan-audit.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True, "plan-audit.json written"


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Install bbp-reviewer plan audit JSON")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--from", dest="src", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    src = args.src.resolve()
    if not src.is_file():
        print("Plan audit source file not found.", file=sys.stderr)
        return 2
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Plan audit source is not valid JSON.", file=sys.stderr)
        return 2
    ok, msg = install_audit(root, data)
    if not ok:
        print(f"Plan audit invalid: {msg}", file=sys.stderr)
        return 1
    print(f"plan-audit:MET {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
