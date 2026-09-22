# Tools

Enforcement. Specimens in `examples/` are not a product.

**Vocabulary links:** after editing [`docs/TERMS.md`](../docs/TERMS.md), run `python3 tools/link-terms-dictionary.py` to refresh term links in markdown across the repo.

**Requirements preflight (ADR 0013):** Python tools call `nlc_requirements.hub_tool()` or `hub_prove()` at entry. Install scripts check `python3` / `git` before work.

**Human CLI (`nlc`):** adopters use `./nlc`, `verify`, `new`, etc. **Maintainer / agent:**

```bash
./nlc maintainer requirements   # after ratification
./nlc maintainer check-rules
./nlc maintainer rule-coverage --adr 0007 --check
./nlc maintainer rule-marker --id <rule_id>
./nlc maintainer rule-emit --goal <id>   # ADR 0023 compiler-owned markers after generate
./nlc maintainer gate-scope --add <path>
./nlc maintainer goal-scaffold --goal <id>
./nlc maintainer regen-plan --change kind:id --orchestrate --write-queue
```

`./nlc verify` runs ADR 0006 contract gates (C10/C21 + breaking acceptance) via `nlc_contract_change.py` / `nlc_contract_break_accept.py`.

Hub compile also runs `fitness-agent-noun-structure.py` (ADR 0003) and `fitness-nlc-naming.py` (ADR 0011).

Migration catalog (ADR 0014): `python3 tools/assert-migration-catalog-passes.py`; release `./release` preflight uses `nlc_migration_catalog.py`.

Hub boundary (ADR 0016): `fitness-hub-no-product-requirements.py`; landmine `assert-hub-no-product-requirements-passes.py`. P2 hub scope (ADR 0002): `fitness-p2-hub-scope.py`.

Adopter verify (0021/0023): `examples/adopter-verify-fast-green/`; `fitness-adopter-verify-binder.py`; `assert-adopter-verify-fast-green-passes.py`. Parked ADRs: `fitness-adr-gap-parked.py` (0007/0009).

Meta binders (hub ADR coverage): `fitness-adr-0004-0005-binder.py`, `fitness-adr-0006-binder.py`, `fitness-adr-0008-binder.py`, `fitness-adr-0010-binder.py`, `fitness-adr-0023-binder.py`, `fitness-human-surface-binder.py` (0017–0020). See [`docs/ADR-ENFORCEMENT.md`](../docs/ADR-ENFORCEMENT.md).

Consumer naming (ADR 0011): landmine `assert-nlc-naming-passes.py`. Gate binder (ADR 0010): `fitness-harness-gate-binder-sync.py`, `assert-gate-record-describe-passes.py`. SSOT produce (ADR 0005): `fitness-produce-ssot-binder.py`. Verify skill (ADR 0021/0023): `fitness-verify-skill-binders.py`.

Distribution (ADR 0015): `fitness-distribution-binder.py`; landmines install/lock/hermetic/smoke (see file). Release preflight (ADR 0014): `assert-release-preflight-passes.py`.

Binding matrix (ADR 0001): `fitness-adr-0001-binder.py`, `assert-binding-matrix-met.py`. P2 scope (ADR 0002): `assert-p2-hub-scope-passes.py`. Agent nouns (ADR 0003): `assert-agent-noun-structure-passes.py`, `assert-validate-agent-nouns-passes.py`. Quality handoff (ADR 0004/0005): `assert-quality-metric-passes.py`.

Noun shape (ADR 0008): `fitness-no-noun-inheritance.py`; specimen `examples/noun-inheritance-violation/`; landmine `assert-noun-inheritance-fails.py`.

Human menu (ADR 0017/0020): `fitness-menu-harness-sync.py` vs `docs/nlc/MENU.md` and `nlc_menu_data.py`.

Interview on gap (ADR 0018): `fitness-interview-gap-shape.py` (includes `scripts/install.sh`); landmine `assert-interview-gap-passes.py` (`./nlc new`). Prompt shape: `fitness-interview-prompt-shape.py`. Dashboard: `fitness-dashboard-interview-sync.py` + `assert-dashboard-interview-passes.py`.

Rule trace (ADR 0023): [`docs/nlc/RULE-TRACE.md`](../docs/nlc/RULE-TRACE.md); `fitness-verify-rule-coverage-wired.py`; verify landmines `assert-verify-rule-coverage-blockers-*.py`; hub `assert-hub-rule-coverage-passes.py`.

Rule conflicts (ADR 0012): `check-rule-adoption.py`; specimens `rule-adoption-conflict/` / `rule-coverage-minimal`; landmines `assert-rule-adoption-conflicts-fails.py`, `assert-rule-adoption-passes.py`.

Contract change (ADR 0006): `nlc_contract_change.py` (hub cwd fix); non-specimen landmines `assert-invoice-correct-contract-blockers-passes.py`, `assert-contract-change-detects-c21-fails.py`; diff-scoped `fitness-c10-changed.py` / `fitness-c21-changed.py`.

Brownfield + rule trace: `fitness-brownfield-rule-trace.py`; `nlc-brownfield-inventory.py` stderr hints goal-scaffold.

Guided orchestration (ADR 0019): `fitness-guide-orchestration.py`.

Requirements preflight (ADR 0013): `fitness-requirements-hub-entrypoints.py`; landmine `assert-requirements-hub-entrypoints-passes.py`.

```bash
./nlc maintainer contract-break-accept --schema domain/foo/schemas/verbs.schema.json --adr 0099 --accepted-by 'role:manager'
```

## Compile vs release

`ci_fitness.py` is the **compile** suite (landmines + invoice-correct + matrix). `ci-fitness.sh` / `ci-fitness.ps1` invoke it.
Class C can print `CI:MET` with **no human**. That is intentional.

`release-audit.py` is the **ship** hook. It re-runs every `fitness-*.py` on a
product tree **and** requires a human `Released-by:` on CONFIRM.md. Class A/B/D/E/F
also need `Ratified-by:` (C24). Pipeline: run this **before** merge or deploy.

```bash
python3 tools/ci_fitness.py
python3 tools/release-audit.py examples/invoice-correct
# expected: RELEASE:NOT_MET  UNMET 1 H-RELEASE
```

A tree that is compile-green but unsigned must not ship. Remediation steps are
printed as `Step 1`, `Step 2`, … — open this file, run this command.

Hub suite (landmines + invoice-correct + matrix):

```bash
python3 tools/ci_fitness.py
```

Windows:

```powershell
python tools\ci_fitness.py
# or
powershell -File tools\ci-fitness.ps1
```

Charter §14 check 1 only (legacy bash):

```bash
bash tools/ci-fitness-check1.sh
```

Session start (not a P2 binder):

```bash
bash tools/session-preflight.sh
```
