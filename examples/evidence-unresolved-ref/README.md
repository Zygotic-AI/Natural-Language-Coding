# evidence-unresolved-ref

[Specimen](../../docs/TERMS.md#specimen) for **ADR 0050**: a gate must **REFUSE** when evidence names a commit that does not exist.

Designed fail: `tools/assert-evidence-unresolved-ref-refuses.py` expects `RELEASE_TAG_GATE:REFUSE` for the dangling id in [`integrity/evidence-dangling-ref.json`](integrity/evidence-dangling-ref.json).

This tree is not a product; it exists only to prove REFUSE semantics.
