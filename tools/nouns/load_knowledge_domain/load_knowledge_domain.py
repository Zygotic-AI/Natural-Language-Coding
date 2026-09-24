"""Knowledge steward load-knowledge-domain — read confirmed facts for a scope."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOUNDARY = "bba-emit"


def load_domain(repo: Path, scope: str, include_proposals: bool) -> dict:
    facts_path = repo / "knowledge" / "facts.json"
    if not facts_path.is_file():
        return {
            "status": "error",
            "facts": [],
            "error": {"code": "DOMAIN_UNAVAILABLE", "message": "missing knowledge/facts.json"},
        }

    data = json.loads(facts_path.read_text(errors="replace"))
    rows = data.get("facts") or []
    allowed = {"confirmed"}
    if include_proposals:
        allowed.add("proposed")

    scope_l = scope.lower()
    matched = []
    for fact in rows:
        if not isinstance(fact, dict):
            continue
        st = fact.get("status")
        if st not in allowed:
            continue
        fscope = str(fact.get("scope") or "").lower()
        if fscope == scope_l or scope_l in fscope or fscope in scope_l:
            matched.append(
                {
                    "id": fact.get("id"),
                    "statement": fact.get("statement"),
                    "status": st,
                    "scope": fact.get("scope"),
                }
            )

    status = "loaded" if matched else "empty"
    return {"status": status, "facts": matched}


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 1:
        print(
            "usage: load-knowledge-domain.py <scope> [repo-root]",
            file=sys.stderr,
        )
        return 2
    scope = args[0]
    repo = Path(args[1]).resolve() if len(args) > 1 else Path.cwd()
    include = "--include-proposals" in args
    result = load_domain(repo, scope, include)
    if result.get("status") == "error":
        print(json.dumps(result, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0
