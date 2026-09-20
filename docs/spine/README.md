# Compile spine (UC9, UC14, UC18)

Hub does not ship product requirements (ADR 0016). Rule-shape example: [`pan-handling`](../worked-examples/pan-handling/README.md).

| UC | Tool / doc | Role |
| ---- | ----------- | ---- |
| UC9 | [`IMPACT-GRAPH.md`](IMPACT-GRAPH.md), [`tools/nlc-delta-regen.py`](../../tools/nlc-delta-regen.py) | Generated graph + blast-radius plan (`--orchestrate`) |
| UC14 | [`tools/check-rule-adoption.py`](../../tools/check-rule-adoption.py), ADR 0012 | Precedence + human override on real conflicts |
| UC18 | [`knowledge/facts.json`](../../knowledge/facts.json), [`tools/nlc-before-generate.py`](../../tools/nlc-before-generate.py) | Fact SSOT — [`docs/nlc/HARNESS.md`](../nlc/HARNESS.md) |
| UC15 greenfield | [`tools/nlc-init.py`](../../tools/nlc-init.py) | Empty repo scaffold + lock + CI template |
