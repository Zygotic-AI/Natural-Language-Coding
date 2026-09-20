#!/usr/bin/env python3
"""Hub compile fitness suite (cross-platform).

Same sequence as legacy ci-fitness.sh. Use on Windows without bash:

  python tools/ci_fitness.py

From repo root. Exit 0 = CI:MET, 1 = CI:FAIL.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_prove  # noqa: E402
TOOLS = ROOT / "tools"


def fail(msg: str) -> None:
    print(f"CI:FAIL {msg}")
    sys.exit(1)


def run(label: str, argv: list[str]) -> None:
    print(f"--- {label} ---")
    proc = subprocess.run(
        argv,
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        fail(label)


def session_preflight() -> None:
    print("=== session preflight v1 ===")
    short = ROOT / ".agents" / "bbp-short-form.md"
    if not short.is_file():
        print("SESSION:NOT_MET missing short-form")
        sys.exit(1)
    print("SESSION:LOAD short-form .agents/bbp-short-form.md")
    if not (ROOT / "CHARTER.md").is_file():
        print("SESSION:NOT_MET missing charter")
        sys.exit(1)
    print("SESSION:LOAD charter CHARTER.md")
    print("SESSION:REMIND knowledge-steward load-knowledge-domain before generate")
    print("SESSION:REMIND confirmer python tools/ci_fitness.py")
    print("SESSION:REMIND ADR 0006 breaking contracts stay red until callers are in the plan")
    print("SESSION:MATRIX")
    run("session binding matrix", [sys.executable, str(TOOLS / "audit-binding-matrix.py")])
    print("SESSION:MET")


def charter_check1() -> None:
    print("=== charter §14 check 1 ===")
    run(
        "assert-invoice-violation-fails",
        [sys.executable, str(TOOLS / "assert-invoice-violation-fails.py")],
    )
    print("=== check 1: non-fixture example trees must MET ===")
    examples = ROOT / "examples"
    if examples.is_dir():
        for d in sorted(examples.iterdir()):
            if not d.is_dir():
                continue
            if d.name == "invoice-violation":
                continue
            print(f"scanning {d}/")
            run(
                f"no-noun-field-writes {d.name}",
                [sys.executable, str(TOOLS / "fitness-no-noun-field-writes.py"), str(d)],
            )


def main() -> int:
    hub_prove()
    session_preflight()

    charter_check1()

    print("=== designed-fail landmines (assert exit 0 = landmine live) ===")
    for path in sorted(TOOLS.glob("assert-*-fails.py")):
        run(str(path.relative_to(ROOT)), [sys.executable, str(path)])

    print("=== designed-pass impact graph ===")
    run(
        "impact graph",
        [sys.executable, str(TOOLS / "assert-impact-graph-generated.py")],
    )
    run(
        "release signed",
        [sys.executable, str(TOOLS / "assert-release-signed-passes.py")],
    )

    print("=== invoice-correct must MET on bound tools ===")
    correct = ROOT / "examples" / "invoice-correct"
    for path in sorted(TOOLS.glob("fitness-*.py")):
        run(
            f"{path.name} invoice-correct",
            [sys.executable, str(path), str(correct)],
        )

    print("=== changed-only-ok must MET on C7/C11 ===")
    changed = ROOT / "examples" / "changed-only-ok"
    run(
        "C7 changed-only-ok",
        [sys.executable, str(TOOLS / "fitness-contract-presence.py"), str(changed)],
    )
    run(
        "C11 changed-only-ok",
        [sys.executable, str(TOOLS / "fitness-r13-entrypoints.py"), str(changed)],
    )

    print("=== retrying-nested-ok must MET on C15 ===")
    retry_ok = ROOT / "examples" / "retrying-nested-ok"
    run(
        "C15 retrying-nested-ok",
        [sys.executable, str(TOOLS / "fitness-c15-idempotent.py"), str(retry_ok)],
    )

    print("=== binding matrix ===")
    run("binding matrix", [sys.executable, str(TOOLS / "audit-binding-matrix.py")])

    print("CI:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
