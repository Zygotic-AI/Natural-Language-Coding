# Tools

Enforcement. Specimens in `examples/` are not a product.

**Vocabulary links:** after editing [`docs/TERMS.md`](../docs/TERMS.md), run `python3 tools/link-terms-dictionary.py` to refresh term links in markdown across the repo.

**Requirements preflight (ADR 0013):** Python tools call `nlc_requirements.hub_tool()` or `hub_prove()` at entry. Install scripts check `python3` / `git` before work.

**Human CLI (`nlc`):** adopters use `./nlc`, `verify`, `new`, etc. **Maintainer / agent:**

```bash
./nlc maintainer requirements   # after ratification
./nlc maintainer check-rules
./nlc maintainer regen-plan --change kind:id --orchestrate --write-queue
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
