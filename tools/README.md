# Tools

Enforcement. Specimens in `examples/` are not a product.

## Compile vs release

`ci-fitness.sh` is the **compile** suite (landmines + invoice-correct + matrix).
Class C can print `CI:MET` with **no human**. That is intentional.

`release-audit.py` is the **ship** hook. It re-runs every `fitness-*.py` on a
product tree **and** requires a human `Released-by:` on CONFIRM.md. Class A/B/D/E/F
also need `Ratified-by:` (C24). Pipeline: run this **before** merge or deploy.

```bash
bash tools/ci-fitness.sh
python3 tools/release-audit.py examples/invoice-correct
# expected: RELEASE:NOT_MET  UNMET 1 H-RELEASE
```

A tree that is compile-green but unsigned must not ship. Remediation steps are
printed as `Step 1`, `Step 2`, … — open this file, run this command.

Hub suite (landmines + invoice-correct + matrix):

```bash
bash tools/ci-fitness.sh
```

Charter §14 check 1 only:

```bash
bash tools/ci-fitness-check1.sh
```

Session start (not a P2 binder):

```bash
bash tools/session-preflight.sh
```
