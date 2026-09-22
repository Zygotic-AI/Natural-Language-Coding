# [Requirement packs](../TERMS.md#requirement-pack) (hub v0.2)

[NLC](../TERMS.md#nlc) [hub](../TERMS.md#hub) ships **tools**, not PCI/HIPAA/etc. **[Requirement packs](../TERMS.md#requirement-pack)** are versioned bundles adopters or enterprises author, ratify, and share.

## Lifecycle

1. **Ingest** — source standard/docs → candidate ADRs + rules (human review; not automated ratification).
2. **Ratify** — [ADR](../TERMS.md#adr) status + `rules/adopted.json` in the authoring repo.
3. **Export** — `python3 tools/nlc-pack-export.py --name my-pack --version 1.0.0`
4. **Consume** — `python3 tools/nlc-pack-install.py pack-my-pack-1.0.0.tar.gz` in an [app repo](../TERMS.md#adopter); scope tags/data; [UC9](../TERMS.md#uc9) regen as needed.

## Manifest

[`integrity/schemas/nlc-pack-manifest.schema.json`](../../integrity/schemas/nlc-pack-manifest.schema.json)

## v0.2 checklist

See [`TODO`](../../TODO) — [Hub](../TERMS.md#hub) v0.2.0 section. Ingest skill and public registry are out of band.
