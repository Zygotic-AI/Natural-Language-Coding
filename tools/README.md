# Tools

Enforcement. Specimens in `examples/` are not a product.

Hub suite (landmines + invoice-correct + matrix):

```bash
bash tools/ci-fitness.sh
```

Charter §14 check 1 only:

```bash
bash tools/ci-fitness-check1.sh
```

Designed fail: matching `tools/assert-*-fails.py` exits 0 (`ASSERT:PASS`).
Designed pass: `examples/invoice-correct` is MET on the bound v1 tools.
True miss: an assert exits 1, or invoice-correct is NOT_MET.
