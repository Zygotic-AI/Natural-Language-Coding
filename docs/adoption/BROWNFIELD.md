# [Brownfield](../TERMS.md#brownfield) adoption (beta)

[NLC](../TERMS.md#nlc) confidence is **higher for [greenfield](../TERMS.md#greenfield)** than for existing codebases. [Brownfield](../TERMS.md#brownfield) is supported as a **manual** path until inventory, [binding](../TERMS.md#binding), and [delta-regen](../TERMS.md#delta-regen-queue) mature.

## [Greenfield](../TERMS.md#greenfield) (supported)

```bash
python3 /path/to/nlc-hub/tools/nlc-init.py ~/projects/my-new-app --name MyApp
```

See [BOOTSTRAP.md](BOOTSTRAP.md).

## [Brownfield](../TERMS.md#brownfield) (beta)

1. Do **not** use `nlc-init` on repos with existing `domain/` or `goals/` content.
2. Follow [BOOTSTRAP.md](BOOTSTRAP.md): [charter](../TERMS.md#charter), CI hooks, interview-first.
3. Introduce **one [noun](../TERMS.md#noun) + one [goal](../TERMS.md#goal)** behind gates before migrating legacy modules.
4. Use [`tools/nlc-delta-regen.py`](../../tools/nlc-delta-regen.py) after [contract](../TERMS.md#contract) changes (UC9 v1 plan).
5. Expect judgment gaps (R1/C3/C4) — no static [gate](../TERMS.md#gate) replaces “is this the right [noun](../TERMS.md#noun)?”

Record adoption [ADR](../TERMS.md#adr) in the [app repo](../TERMS.md#adopter) when you commit to the shape.
