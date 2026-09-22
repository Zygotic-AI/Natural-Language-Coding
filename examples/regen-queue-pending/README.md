# [Specimen](../../docs/TERMS.md#specimen): open [delta-regen queue](../../docs/TERMS.md#delta-regen-queue)

`./nlc verify` must **not** [MET](../../docs/TERMS.md#met) while `.nlc/delta-regen-queue.json` has pending `steps` (ADR 0006 / UC9 — prove stays red until regen completes).

Used by `tools/assert-verify-regen-queue-fails.py`.
