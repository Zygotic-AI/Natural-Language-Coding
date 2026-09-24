# Hub pack registry (v1)

Curated list of requirement packs the hub documents for ingest/install honesty. Policy: [ADR 0041](../../adrs/0041-product-completion-scope.md).

| Artifact | Role |
| -------- | ---- |
| [`integrity/hub-pack-registry.json`](../../integrity/hub-pack-registry.json) | Registry data (may be empty) |
| [`integrity/schemas/hub-pack-registry.schema.json`](../../integrity/schemas/hub-pack-registry.schema.json) | JSON shape |
| `python3 tools/validate-hub-pack-registry.py` | Machine gate → `HUB_PACK_REGISTRY:MET` |

**v1 is hub-local**, not a public internet registry. An empty `packs` array means install is not restricted by the registry. When entries exist, `nlc-pack-install` refuses manifests not listed (name + version).

Scope dispositions for other product gaps: [`integrity/product-completion-scope.json`](../../integrity/product-completion-scope.json).
