# Requirement packs (hub v0.2)

NLC hub ships **tools**, not PCI/HIPAA/etc. **Requirement packs** are versioned bundles adopters or enterprises author, ratify, and share.

## Lifecycle

1. **Ingest** — source standard/docs → candidate ADRs + rules (human review; not automated ratification).
2. **Ratify** — ADR status + `rules/adopted.json` in the authoring repo.
3. **Export** — `python3 tools/nlc-pack-export.py --name my-pack --version 1.0.0`
4. **Consume** — `python3 tools/nlc-pack-install.py pack-my-pack-1.0.0.tar.gz` in an app repo; scope tags/data; UC9 regen as needed.

## Manifest

[`integrity/schemas/nlc-pack-manifest.schema.json`](../../integrity/schemas/nlc-pack-manifest.schema.json)

## v0.2 checklist

See [`TODO`](../../TODO) — Hub v0.2.0 section. Ingest skill and public registry are out of band.
