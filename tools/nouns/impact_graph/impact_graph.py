"""Emit or persist the R21 impact graph for an adopter repo."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.generate_impact_graph import build  # noqa: E402


def _build(root: Path) -> dict:
    return build(root)


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Impact graph for blast radius (UC9)")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write generated/impact-graph.json under repo root",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    graph = _build(root)
    if args.write:
        out_dir = root / "generated"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "impact-graph.json"
        out_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
        print(f"IMPACT_GRAPH:MET path={out_path}")
    json.dump(graph, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


