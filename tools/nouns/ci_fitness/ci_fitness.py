"""Hub compile fitness suite (cross-platform).

Same sequence as legacy ci-fitness.sh. Use on Windows without bash:

  python tools/ci_fitness.py

From repo root. Exit 0 = CI:MET, 1 = CI:FAIL.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_prove  # noqa: E402
from nouns.field_write_bypass_fixtures.field_write_bypass_fixtures import (  # noqa: E402
    O9A_BYPASS_FIXTURE_DIRS,
)
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
            if d.name in {"invoice-violation", "internal-link-landmine"}:
                continue
            if d.name in O9A_BYPASS_FIXTURE_DIRS:
                continue
            if d.name.startswith("invoice-bypass-"):
                fail(f"unexpected invoice-bypass fixture {d.name} (not in O9A_BYPASS_FIXTURE_DIRS)")
            print(f"scanning {d}/")
            run(
                f"no-noun-field-writes {d.name}",
                [sys.executable, str(TOOLS / "fitness-no-noun-field-writes.py"), str(d)],
            )


def run_ci_fitness_suite(*, include_releasable_verify: bool = False) -> int:
    """Hub compile fitness. Releasable verify profile runs only when requested (not from hub-ci-fitness gate)."""
    if include_releasable_verify:
        from nouns.releasable_gates.releasable_gates import run_profile

        print("=== releasable verify profile (SSOT) ===")
        if run_profile("verify", ROOT) != 0:
            fail("releasable verify profile")

    session_preflight()

    charter_check1()

    print("=== ADR 0050 evidence identity ===")
    run(
        "fitness-no-history-ids-in-evidence",
        [sys.executable, str(TOOLS / "fitness-no-history-ids-in-evidence.py")],
    )
    run(
        "fitness-landmine-self-contained",
        [sys.executable, str(TOOLS / "fitness-landmine-self-contained.py")],
    )
    run(
        "fitness-root-session-artifacts",
        [sys.executable, str(TOOLS / "fitness-root-session-artifacts.py")],
    )
    run(
        "fitness-hub-public-self-contained",
        [sys.executable, str(TOOLS / "fitness-hub-public-self-contained.py")],
    )
    run(
        "fitness-internal-links",
        [sys.executable, str(TOOLS / "fitness-internal-links.py")],
    )
    run(
        "fitness-sync-up-review-appendix",
        [sys.executable, str(TOOLS / "fitness-sync-up-review-appendix.py")],
    )
    run(
        "assert-internal-link-gate-fails",
        [sys.executable, str(TOOLS / "assert-internal-link-gate-fails.py")],
    )
    run(
        "assert-hub-in-force-exclusions-passes",
        [sys.executable, str(TOOLS / "assert-hub-in-force-exclusions-passes.py")],
    )
    run(
        "fitness-goal-write-hook",
        [sys.executable, str(TOOLS / "fitness-goal-write-hook.py")],
    )
    run(
        "assert-field-write-bypass-fails",
        [sys.executable, str(TOOLS / "assert-field-write-bypass-fails.py")],
    )
    run(
        "assert-unresolvable-refuses-passes",
        [sys.executable, str(TOOLS / "assert-unresolvable-refuses-passes.py")],
    )
    run(
        "assert-evidence-unresolved-ref-refuses",
        [sys.executable, str(TOOLS / "assert-evidence-unresolved-ref-refuses.py")],
    )

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
    run(
        "full-nlc-audit quick",
        [sys.executable, str(TOOLS / "assert-full-nlc-audit-quick-passes.py")],
    )
    run(
        "full-nlc-audit emit-inference-checklist",
        [sys.executable, str(TOOLS / "assert-full-nlc-audit-emit-checklist-passes.py")],
    )

    print("=== invoice-correct must MET on bound tools ===")
    correct = ROOT / "examples" / "invoice-correct"
    hub_only: set[str] = set()
    manifest = ROOT / "integrity" / "releasable-gates.json"
    if manifest.is_file():
        import json

        hub_only = set(json.loads(manifest.read_text(encoding="utf-8")).get("hub_only_fitness") or [])
    for path in sorted(TOOLS.glob("fitness-*.py")):
        if path.name in hub_only:
            print(f"--- skip {path.name} invoice-correct (hub-only) ---")
            continue
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
        "fitness-use-cases-expansion-sync",
        [sys.executable, str(TOOLS / "fitness-use-cases-expansion-sync.py")],
    )
    run(
        "fitness-product-completion-p8-closeout",
        [sys.executable, str(TOOLS / "fitness-product-completion-p8-closeout.py")],
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
        "assert-piped-install-smoke",
        [sys.executable, str(TOOLS / "assert-piped-install-smoke-passes.py")],
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
        "assert-durable-engine-tag-strict-fails",
        [sys.executable, str(TOOLS / "assert-durable-engine-tag-strict-fails.py")],
    )
    run(
        "assert-durable-engine-tag-strict-passes",
        [sys.executable, str(TOOLS / "assert-durable-engine-tag-strict-passes.py")],
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
        "assert-non-python-adapter-passes",
        [sys.executable, str(TOOLS / "assert-non-python-adapter-passes.py")],
    )
    run(
        "assert-rule-runner-passes",
        [sys.executable, str(TOOLS / "assert-rule-runner-passes.py")],
    )
    run(
        "assert-call-tree-pack-reference",
        [sys.executable, str(TOOLS / "assert-call-tree-pack-reference-passes.py")],
    )
    run(
        "assert-delta-regen-narrow-passes",
        [sys.executable, str(TOOLS / "assert-delta-regen-narrow-passes.py")],
    )
    run(
        "assert-delta-regen-orchestrate-passes",
        [sys.executable, str(TOOLS / "assert-delta-regen-orchestrate-passes.py")],
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
        "assert-release-main-purity",
        [sys.executable, str(TOOLS / "assert-release-main-purity-passes.py")],
    )
    run(
        "assert-release-infer",
        [sys.executable, str(TOOLS / "assert-release-infer-passes.py")],
    )
    run(
        "assert-release-state",
        [sys.executable, str(TOOLS / "assert-release-state-passes.py")],
    )
    run(
        "assert-release-context",
        [sys.executable, str(TOOLS / "assert-release-context-passes.py")],
    )
    run(
        "fitness-release-planner-ownership",
        [sys.executable, str(TOOLS / "fitness-release-planner-ownership.py")],
    )
    run(
        "assert-release-planner-ownership",
        [sys.executable, str(TOOLS / "assert-release-planner-ownership-fails.py")],
    )
    run(
        "assert-jidoka-ssot-agents-link",
        [sys.executable, str(TOOLS / "assert-jidoka-ssot-agents-link-passes.py")],
    )
    run(
        "assert-goal-write-hook-landmine",
        [sys.executable, str(TOOLS / "assert-goal-write-hook-landmine-passes.py")],
    )
    run(
        "assert-release-main-purity-remediation",
        [sys.executable, str(TOOLS / "assert-release-main-purity-remediation-passes.py")],
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

    run(
        "fitness-releasable-gate-ssot",
        [sys.executable, str(TOOLS / "fitness-releasable-gate-ssot.py")],
    )
    run(
        "fitness-adr-approval",
        [sys.executable, str(TOOLS / "fitness-adr-approval.py")],
    )
    run(
        "fitness-adr-record-gate",
        [sys.executable, str(TOOLS / "fitness-adr-record-gate.py")],
    )
    run(
        "fitness-verb-set-lineage",
        [sys.executable, str(TOOLS / "fitness-verb-set-lineage.py")],
    )
    run(
        "fitness-executable-shape",
        [sys.executable, str(TOOLS / "fitness-executable-shape.py")],
    )
    run(
        "assert-planit-other-skill",
        [sys.executable, str(TOOLS / "assert-planit-other-skill-fails.py")],
    )
    run(
        "assert-adr-approval-mismatch",
        [sys.executable, str(TOOLS / "assert-adr-approval-mismatch-fails.py")],
    )
    run(
        "assert-verb-primitive-inventory",
        [sys.executable, str(TOOLS / "assert-verb-primitive-inventory-fails.py")],
    )
    run(
        "assert-verb-set-extension",
        [sys.executable, str(TOOLS / "assert-verb-set-extension-fails.py")],
    )
    run(
        "assert-executable-kernel-exempt",
        [sys.executable, str(TOOLS / "assert-executable-kernel-exempt-fails.py")],
    )
    print("=== RCA-1 releasable gate landmines ===")
    run(
        "assert-releasable-gate-list-duplicate",
        [sys.executable, str(TOOLS / "assert-releasable-gate-list-duplicate-fails.py")],
    )
    run(
        "assert-releasable-failure-without-reproduce",
        [sys.executable, str(TOOLS / "assert-releasable-failure-without-reproduce-fails.py")],
    )
    run(
        "assert-releasable-home-invariant",
        [sys.executable, str(TOOLS / "assert-releasable-home-invariant-passes.py")],
    )
    run(
        "assert-stale-committed-evidence",
        [sys.executable, str(TOOLS / "assert-stale-committed-evidence-fails.py")],
    )
    run(
        "assert-hub-only-fitness-scope",
        [sys.executable, str(TOOLS / "assert-hub-only-fitness-scope-passes.py")],
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


def main() -> int:
    hub_prove()
    return run_ci_fitness_suite(include_releasable_verify=True)


if __name__ == "__main__":
    sys.exit(main())
