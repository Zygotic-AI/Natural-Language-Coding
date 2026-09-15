# A7 — escape hatches (v1)

Not a binding-matrix id. Adversarial-audit concern. Also how R6 grows.

## Statement

ORM dirty writes, raw SQL, reflection, `exec` / `eval`, and `obj.__dict__`
must fail CI when they happen outside the noun.

## V1 gate

`tools/fitness-escape-hatch.py` covers `__dict__`, `vars(`, `exec(`, `eval(`
in goals/adapters.

Raw SQL and `.save(` / `setattr(` stay on `fitness-verb-path.py` (R6 v1).
Named field assignment stays on R5.

Known-fail: `examples/invoice-escape-hatch-violation/`.

## Not bound

No matrix row. V1 is the reflection slice, not every ORM dialect.
