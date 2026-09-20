# Product use-cases

SSOT for what this practice *does*. Code is derived. Actors: **human manager**
(non-coder) and **compiler** (AI). One compile, staged outputs — do not fuse
goal, ADR, and if/then into one blob.

Status: **in force** = charter/tool exists. **Parked** = decided, not executable (still needed when that expansion happens). **Missing** = **needed** — the product is incomplete without it; not optional polish.


---

## Spine (one compile)

| ID | Story | Status |
|----|--------|--------|
| UC1 | **Interview.** Human states an outcome. Compiler interviews until goals, ADRs/standards, knowledge facts, and dependencies are bound. Unbound statement → keep interviewing, do not emit. | In force as PLANIT start / binding idea. Interview skill still thin. |
| UC2 | **Execute a goal (PLANIT).** From a bound goal: classify → plan → atomic statements → bind → emit → adversarial audit. | In force: charter §6; orchestrator [`planit`](../.agents/skills/planit/SKILL.md) + leaf `bbp-*` skills; see [`PLANIT-ORCHESTRATION.md`](ai-compiled-systems/PLANIT-ORCHESTRATION.md). |
| UC3 | **Standard / req / business rule → ADR.** PCI, Temporal, “do not store PAN,” etc. become a decision: why, rejected, consequences. | Process. No conversion gate. |
| UC4 | **ADR → if/then.** Reduce to tags, primitives, facts, rules. If the closed set cannot speak, add a tag/fact/primitive first (itself an ADR). | ADR 0007. Runner parked. |
| UC5 | **Rules → emit.** Verb declares primitive + tagged target. Compiler applies the rule (encrypt, forbid return, Temporal engine) or the gate fails. Prompt memory is not the bind. | Promised. v1 stand-in: `taint.txt` + Python fitness. |

Same conversation may produce UC1–UC4. Three artifacts, three gates: **goal**, **ADR**, **rule**.

---

## Beside the spine

| ID | Story | Status |
|----|--------|--------|
| UC6 | **Classify A–F.** Adjective / verb / goal / durable / contract / charter. Wrong class fails (C on a charter change is illegal). | In force: C1. |
| UC7 | **Adversarial review.** Second role attacks the plan before emit. Open FAIL blocks ship unless rebutted. | In force: C23. |
| UC8 | **Prove / ship.** AI gates green = compile. `Ratified-by` (class A/B/D/E/F) and `Released-by` (always) = ship. Unmet gate prints Step 1…N. | In force: `ci-fitness.sh`, `release-audit.py`, C24. |
| UC9 | **Change a requirement.** Human changes one ADR/rule. Compiler diffs tagged nouns/verbs/goals and regenerates that blast radius only. | Impact graph + `nlc-delta-regen.py`; `--orchestrate` queue (see [`IMPACT-GRAPH.md`](spine/IMPACT-GRAPH.md)). |
| UC10 | **Defect is upstream.** Emit wrong → RCA to interview / ADR / rule. Human does not patch generated code. | Charter + ADR 0006. |
| UC11 | **Breaking contract.** Additive = quiet. Break stays red until the human accepts the *requirement*, not the schema. | ADR 0006. |
| UC12 | **Expand the closed set.** New primitive or tag is an ADR, then a row in [`integrity/primitives.md`](../integrity/primitives.md). Prefer tag/fact before a new primitive. | In force as SSOT file. Runner parked. |
| UC13 | **Durable goal → engine tag.** `goal.durable ∧ engine.runtime ≠ (named runtime) → forbid`. Temporal is a tagged noun, not a fourth citizen. | ADR 0007. |
| UC14 | **Rule conflict at adopt-time.** Same tag+primitive match with incompatible effects (e.g. `pan ∧ return → forbid` vs `pan ∧ return → must export`). Higher **ADR precedence tier** wins; tie → human records override (ADR 0012). Not “encrypt vs cannot store” (those compose). | v1: `check-rule-adoption.py`. |
| UC15 | **Adopt in a repo.** Greenfield: `nlc-init`. Brownfield: beta manual path. | Greenfield CLI v1; brownfield doc only. |
| UC16 | **Language / interior swap.** Same contracts; replace one noun’s interior (Python → Rust, file log → Logstash). | Parked: `docs/LANGUAGE-SCANNER.md`. Engine tag: 0007. |
| UC17 | **Record / supersede.** New decision = ADR. Old ADR marked superseded, not deleted. | In force: R22. |
| UC18 | **Knowledge facts.** Interview writes facts the rules can bind (invoice receives payments, PAN is in scope). Unbound fact → UC1 continues. | `knowledge/facts.json` + `validate-knowledge-facts.py`. |
| ~~UC19~~ | *Retired (ADR 0016).* Hub does not ship product requirements. Shape example only: `docs/worked-examples/pan-handling/`. | **Requirement packs** — v0.2 (`TODO`). |
| UC20 | **Call-tree inventory.** Verb → interior primitive functions. Extra/missing primitive vs bind list fails. | ADR 0009. Gate parked. |
| UC21 | **Gate after every generate.** Metrics first; default-fail gate on that artifact before the next statement. | ADR 0010 / PLANIT 6.5. Binder parked. |


---

## Needed (Missing rows are required)

These are not a someday list. The spine does not close without them.

| ID | Why it is needed |
|----|------------------|
| UC9 (rule-tagged blast radius) | v2: narrow `rule:` changes via tag bindings, not all goals. |
| UC14 edge cases | Composable obligations and cross-primitive policy need richer IR over time. |
| UC15 brownfield | Automated inventory/migration not shipped. |
| UC18 harness wire-up | Mandatory `load-knowledge-domain` / `nlc-before-generate` on every generate path. |
| Requirement packs (v0.2) | Ingest → ratify → export → consume ADR/rule bundles (ADR 0016). Not UC19. |

Parked (needed at expansion): UC16 language packs, UC20 call-tree packs, Rule IR for UC4/UC5.

---

## Not human stories


- Design the Invoice class
- Write or patch generated source to “make it green”
- Inherit one noun from another
- Open-ended primitive names invented at emit time

---

## Next process (not more Python regex)

When a row is **Missing**, the work is an ADR or a content-type, then a bindable gate.
Do not mint an **R** id until the gate exists (R27).
