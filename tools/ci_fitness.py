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
    run(
        "fitness-quality-metric",
        [sys.executable, str(TOOLS / "fitness-quality-metric.py")],
    )

    print("=== agent noun packages ===")
    run(
        "validate-agent-noun-packages",
        [sys.executable, str(TOOLS / "validate-agent-noun-packages.py")],
    )
    run(
        "fitness-agent-noun-structure",
        [sys.executable, str(TOOLS / "fitness-agent-noun-structure.py")],
    )
    run("fitness-nlc-naming", [sys.executable, str(TOOLS / "fitness-nlc-naming.py")])
    run(
        "fitness-hub-no-product-requirements",
        [sys.executable, str(TOOLS / "fitness-hub-no-product-requirements.py")],
    )
    run(
        "fitness-p2-hub-scope",
        [sys.executable, str(TOOLS / "fitness-p2-hub-scope.py")],
    )
    run(
        "fitness-menu-harness-sync",
        [sys.executable, str(TOOLS / "fitness-menu-harness-sync.py")],
    )
    run(
        "fitness-interview-gap-shape",
        [sys.executable, str(TOOLS / "fitness-interview-gap-shape.py")],
    )
    run(
        "fitness-dashboard-interview-sync",
        [sys.executable, str(TOOLS / "fitness-dashboard-interview-sync.py")],
    )
    run(
        "fitness-interview-prompt-shape",
        [sys.executable, str(TOOLS / "fitness-interview-prompt-shape.py")],
    )
    run(
        "fitness-requirements-hub-entrypoints",
        [sys.executable, str(TOOLS / "fitness-requirements-hub-entrypoints.py")],
    )
    run(
        "fitness-planit-generate-markers",
        [sys.executable, str(TOOLS / "fitness-planit-generate-markers.py")],
    )
    run(
        "fitness-nlc-rule-emit-wired",
        [sys.executable, str(TOOLS / "fitness-nlc-rule-emit-wired.py")],
    )
    run(
        "fitness-planit-noun-shape",
        [sys.executable, str(TOOLS / "fitness-planit-noun-shape.py")],
    )
    run(
        "fitness-harness-gate-binder-sync",
        [sys.executable, str(TOOLS / "fitness-harness-gate-binder-sync.py")],
    )
    run(
        "fitness-produce-ssot-binder",
        [sys.executable, str(TOOLS / "fitness-produce-ssot-binder.py")],
    )
    run(
        "fitness-verify-skill-binders",
        [sys.executable, str(TOOLS / "fitness-verify-skill-binders.py")],
    )
    run(
        "fitness-adr-0001-binder",
        [sys.executable, str(TOOLS / "fitness-adr-0001-binder.py")],
    )
    run(
        "fitness-distribution-binder",
        [sys.executable, str(TOOLS / "fitness-distribution-binder.py")],
    )
    run(
        "fitness-adr-0004-0005-binder",
        [sys.executable, str(TOOLS / "fitness-adr-0004-0005-binder.py")],
    )
    run(
        "fitness-adr-0006-binder",
        [sys.executable, str(TOOLS / "fitness-adr-0006-binder.py")],
    )
    run(
        "fitness-adr-0008-binder",
        [sys.executable, str(TOOLS / "fitness-adr-0008-binder.py")],
    )
    run(
        "fitness-adr-0010-binder",
        [sys.executable, str(TOOLS / "fitness-adr-0010-binder.py")],
    )
    run(
        "fitness-adr-0023-binder",
        [sys.executable, str(TOOLS / "fitness-adr-0023-binder.py")],
    )
    run(
        "fitness-verify-rule-coverage-wired",
        [sys.executable, str(TOOLS / "fitness-verify-rule-coverage-wired.py")],
    )
    run(
        "fitness-adopter-verify-binder",
        [sys.executable, str(TOOLS / "fitness-adopter-verify-binder.py")],
    )
    run(
        "fitness-compiled-system-uc-binder",
        [sys.executable, str(TOOLS / "fitness-compiled-system-uc-binder.py")],
    )
    run(
        "fitness-compiled-system-uc-product",
        [sys.executable, str(TOOLS / "fitness-compiled-system-uc-product.py")],
    )
    run(
        "fitness-todo-use-cases-ssot",
        [sys.executable, str(TOOLS / "fitness-todo-use-cases-ssot.py")],
    )
    run(
        "fitness-todo-use-cases-ssot-matrix",
        [sys.executable, str(TOOLS / "fitness-todo-use-cases-ssot-matrix.py")],
    )
    run(
        "fitness-jobs-todo-sync",
        [sys.executable, str(TOOLS / "fitness-jobs-todo-sync.py")],
    )
    run(
        "fitness-adr-gap-parked",
        [sys.executable, str(TOOLS / "fitness-adr-gap-parked.py")],
    )
    run(
        "fitness-brownfield-rule-trace",
        [sys.executable, str(TOOLS / "fitness-brownfield-rule-trace.py")],
    )
    run(
        "fitness-specimen-contract-policy",
        [sys.executable, str(TOOLS / "fitness-specimen-contract-policy.py")],
    )
    run(
        "fitness-verify-pipeline-wired",
        [sys.executable, str(TOOLS / "fitness-verify-pipeline-wired.py")],
    )
    run(
        "fitness-nlc-adopt-existing-hints",
        [sys.executable, str(TOOLS / "fitness-nlc-adopt-existing-hints.py")],
    )
    run(
        "fitness-human-surface-binder",
        [sys.executable, str(TOOLS / "fitness-human-surface-binder.py")],
    )
    run(
        "fitness-guide-orchestration",
        [sys.executable, str(TOOLS / "fitness-guide-orchestration.py")],
    )

    print("=== ADR 0001 / 0014 hub landmines ===")
    run(
        "assert-binding-matrix-met",
        [sys.executable, str(TOOLS / "assert-binding-matrix-met.py")],
    )
    run(
        "assert-migration-catalog",
        [sys.executable, str(TOOLS / "assert-migration-catalog-passes.py")],
    )
    run(
        "assert-migration-step-noop",
        [sys.executable, str(TOOLS / "assert-migration-step-noop-passes.py")],
    )
    run(
        "assert-install-verify",
        [sys.executable, str(TOOLS / "assert-install-verify-passes.py")],
    )
    run(
        "assert-project-lock-schema",
        [sys.executable, str(TOOLS / "assert-project-lock-schema-passes.py")],
    )
    run(
        "assert-nlc-update-hermetic",
        [sys.executable, str(TOOLS / "assert-nlc-update-hermetic-passes.py")],
    )
    run(
        "assert-release-smoke",
        [sys.executable, str(TOOLS / "assert-release-smoke-passes.py")],
    )

    print("=== ADR 0010 policy landmines ===")
    run(
        "assert-batch-generate-policy",
        [sys.executable, str(TOOLS / "assert-batch-generate-policy-fails.py")],
    )
    run(
        "assert-verify-gate-record",
        [sys.executable, str(TOOLS / "assert-verify-gate-record-fails.py")],
    )
    run(
        "assert-verify-regen-queue",
        [sys.executable, str(TOOLS / "assert-verify-regen-queue-fails.py")],
    )
    run(
        "assert-rule-coverage-fails",
        [sys.executable, str(TOOLS / "assert-rule-coverage-fails.py")],
    )
    run(
        "assert-rule-coverage-passes",
        [sys.executable, str(TOOLS / "assert-rule-coverage-passes.py")],
    )
    run(
        "assert-hub-rule-coverage",
        [sys.executable, str(TOOLS / "assert-hub-rule-coverage-passes.py")],
    )
    run(
        "assert-verify-rule-coverage-blockers-fails",
        [sys.executable, str(TOOLS / "assert-verify-rule-coverage-blockers-fails.py")],
    )
    run(
        "assert-verify-rule-coverage-blockers-passes",
        [sys.executable, str(TOOLS / "assert-verify-rule-coverage-blockers-passes.py")],
    )
    run(
        "assert-adopter-verify-fast-green",
        [sys.executable, str(TOOLS / "assert-adopter-verify-fast-green-passes.py")],
    )
    run(
        "assert-interview-packet-fails",
        [sys.executable, str(TOOLS / "assert-interview-packet-fails.py")],
    )
    run(
        "assert-todo-use-cases-ssot-fails",
        [sys.executable, str(TOOLS / "assert-todo-use-cases-ssot-fails.py")],
    )
    run(
        "assert-rule-runner-fails",
        [sys.executable, str(TOOLS / "assert-rule-runner-fails.py")],
    )
    run(
        "assert-goal-bindings-narrow-fails",
        [sys.executable, str(TOOLS / "assert-goal-bindings-narrow-fails.py")],
    )
    run(
        "assert-upstream-hand-patch-fails",
        [sys.executable, str(TOOLS / "assert-upstream-hand-patch-fails.py")],
    )
    run(
        "assert-pack-ingest-candidates-passes",
        [sys.executable, str(TOOLS / "assert-pack-ingest-candidates-passes.py")],
    )
    run(
        "assert-durable-engine-rule-fails",
        [sys.executable, str(TOOLS / "assert-durable-engine-rule-fails.py")],
    )
    run(
        "assert-requirements-sync-pending-fails",
        [sys.executable, str(TOOLS / "assert-requirements-sync-pending-fails.py")],
    )
    run(
        "assert-non-python-adapter-fails",
        [sys.executable, str(TOOLS / "assert-non-python-adapter-fails.py")],
    )
    run(
        "assert-delta-regen-narrow-passes",
        [sys.executable, str(TOOLS / "assert-delta-regen-narrow-passes.py")],
    )
    run(
        "assert-invoice-correct-contract",
        [sys.executable, str(TOOLS / "assert-invoice-correct-contract-blockers-passes.py")],
    )
    run(
        "assert-contract-change-c21",
        [sys.executable, str(TOOLS / "assert-contract-change-detects-c21-fails.py")],
    )
    run(
        "assert-brownfield-inventory",
        [sys.executable, str(TOOLS / "assert-brownfield-inventory-passes.py")],
    )
    run(
        "assert-interview-gap",
        [sys.executable, str(TOOLS / "assert-interview-gap-passes.py")],
    )
    run(
        "assert-dashboard-interview",
        [sys.executable, str(TOOLS / "assert-dashboard-interview-passes.py")],
    )
    run(
        "assert-rule-adoption-conflicts",
        [sys.executable, str(TOOLS / "assert-rule-adoption-conflicts-fails.py")],
    )
    run(
        "assert-rule-adoption-passes",
        [sys.executable, str(TOOLS / "assert-rule-adoption-passes.py")],
    )
    run(
        "assert-c10-changed-scoped",
        [sys.executable, str(TOOLS / "assert-c10-changed-scoped-passes.py")],
    )
    run(
        "assert-c21-changed-scoped",
        [sys.executable, str(TOOLS / "assert-c21-changed-scoped-passes.py")],
    )
    run(
        "assert-requirements-hub-entrypoints",
        [sys.executable, str(TOOLS / "assert-requirements-hub-entrypoints-passes.py")],
    )
    run(
        "assert-nlc-naming",
        [sys.executable, str(TOOLS / "assert-nlc-naming-passes.py")],
    )
    run(
        "assert-hub-no-product-requirements",
        [sys.executable, str(TOOLS / "assert-hub-no-product-requirements-passes.py")],
    )
    run(
        "assert-gate-record-describe",
        [sys.executable, str(TOOLS / "assert-gate-record-describe-passes.py")],
    )
    run(
        "assert-agent-noun-structure",
        [sys.executable, str(TOOLS / "assert-agent-noun-structure-passes.py")],
    )
    run(
        "assert-p2-hub-scope",
        [sys.executable, str(TOOLS / "assert-p2-hub-scope-passes.py")],
    )
    run(
        "assert-quality-metric",
        [sys.executable, str(TOOLS / "assert-quality-metric-passes.py")],
    )
    run(
        "assert-validate-agent-nouns",
        [sys.executable, str(TOOLS / "assert-validate-agent-nouns-passes.py")],
    )
    run(
        "assert-release-preflight",
        [sys.executable, str(TOOLS / "assert-release-preflight-passes.py")],
    )
    run(
        "assert-human-surface",
        [sys.executable, str(TOOLS / "assert-human-surface-passes.py")],
    )
    run(
        "assert-guide-orchestration",
        [sys.executable, str(TOOLS / "assert-guide-orchestration-passes.py")],
    )
    run(
        "assert-invoice-noun-inheritance",
        [sys.executable, str(TOOLS / "assert-invoice-correct-noun-inheritance-passes.py")],
    )
    run(
        "assert-verify-rule-marker-gate",
        [sys.executable, str(TOOLS / "assert-verify-rule-marker-gate-fails.py")],
    )
    run(
        "assert-verify-contract-change",
        [sys.executable, str(TOOLS / "assert-verify-contract-change-fails.py")],
    )
    run(
        "assert-verify-breaking-accept",
        [sys.executable, str(TOOLS / "assert-verify-breaking-accept-fails.py")],
    )
    run(
        "assert-verify-before-generate-stamp",
        [sys.executable, str(TOOLS / "assert-verify-before-generate-stamp-fails.py")],
    )
    run(
        "assert-verify-stale-stamp",
        [sys.executable, str(TOOLS / "assert-verify-stale-stamp-fails.py")],
    )
    run("assert-rule-marker-emit", [sys.executable, str(TOOLS / "assert-rule-marker-emit.py")])
    run(
        "assert-verify-skill-gate",
        [sys.executable, str(TOOLS / "assert-verify-skill-gate-fails.py")],
    )
    run(
        "assert-produce-handoff-refused",
        [sys.executable, str(TOOLS / "assert-produce-handoff-refused.py")],
    )
    run(
        "assert-verify-deep-produce-refused",
        [sys.executable, str(TOOLS / "assert-verify-deep-produce-refused.py")],
    )
    run(
        "assert-goal-scaffold-emits-markers",
        [sys.executable, str(TOOLS / "assert-goal-scaffold-emits-markers.py")],
    )
    run(
        "assert-rule-emit-sync",
        [sys.executable, str(TOOLS / "assert-rule-emit-sync-passes.py")],
    )
    run(
        "assert-produce-role-separation",
        [sys.executable, str(TOOLS / "assert-produce-role-separation-refused.py")],
    )
    run(
        "assert-verify-deep-role-separation",
        [sys.executable, str(TOOLS / "assert-verify-deep-role-separation-refused.py")],
    )
    run(
        "assert-noun-inheritance",
        [sys.executable, str(TOOLS / "assert-noun-inheritance-fails.py")],
    )

    print("=== produce handoff preflight ===")
    from nlc_produce_package import preflight_handoff

    handoff = preflight_handoff(ROOT)
    if handoff == 2:
        fail("handoff_refused produce package")
    if handoff != 0:
        fail("produce preflight")

    print("CI:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
