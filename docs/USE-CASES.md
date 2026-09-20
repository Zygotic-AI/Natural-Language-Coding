# Product use-cases

SSOT for what this practice *does*. Code is derived. Actors: **human manager**
(non-coder) and **[compiler](TERMS.md#compiler)** (AI). One compile, staged outputs — do not fuse
[goal](TERMS.md#goal), [ADR](TERMS.md#adr), and if/then into one blob.

Status: **in force** = charter/tool exists. **Parked** = decided, not executable (still needed when that expansion happens). **Missing** = **needed** — the product is incomplete without it; not optional polish.


---

## Spine (one compile)

| ID | Story | Status |
|----|--------|--------|
| UC1 | **[Interview](TERMS.md#interview).** Human states an outcome. [Compiler](TERMS.md#compiler) interviews until goals, ADRs/standards, knowledge facts, and dependencies are bound. Unbound statement → keep interviewing, do not emit. | In force as [PLANIT](TERMS.md#planit) start / [binding](TERMS.md#binding) idea. [Interview](TERMS.md#interview) skill still thin. |
| UC2 | **Execute a [goal](TERMS.md#goal) (PLANIT).** From a bound [goal](TERMS.md#goal): classify → plan → atomic statements → bind → emit → adversarial [audit](TERMS.md#audit). | In force: [charter](TERMS.md#charter) §6; orchestrator [`planit`](../.agents/skills/planit/SKILL.md) + leaf `bbp-*` skills; see [`PLANIT-ORCHESTRATION.md`](ai-compiled-systems/PLANIT-ORCHESTRATION.md). |
| UC3 | **Standard / req / business [rule](TERMS.md#rule) → [ADR](TERMS.md#adr).** PCI, Temporal, “do not store PAN,” etc. become a decision: why, rejected, consequences. | Process. No conversion [gate](TERMS.md#gate). |
| UC4 | **[ADR](TERMS.md#adr) → if/then.** Reduce to tags, primitives, facts, rules. If the closed set cannot speak, add a tag/fact/primitive first (itself an ADR). | [ADR](TERMS.md#adr) 0007. Runner parked. |
| UC5 | **Rules → emit.** Verb declares [primitive](TERMS.md#primitive) + tagged target. [Compiler](TERMS.md#compiler) applies the [rule](TERMS.md#rule) (encrypt, forbid return, Temporal engine) or the [gate](TERMS.md#gate) fails. Prompt memory is not the bind. | Promised. v1 stand-in: `taint.txt` + Python fitness. |

Same conversation may produce UC1–UC4. Three artifacts, three gates: **[goal](TERMS.md#goal)**, **[ADR](TERMS.md#adr)**, **[rule](TERMS.md#rule)**.

---

## Beside the spine

| ID | Story | Status |
|----|--------|--------|
| UC6 | **Classify A–F.** [Adjective](TERMS.md#adjective) / verb / [goal](TERMS.md#goal) / durable / [contract](TERMS.md#contract) / [charter](TERMS.md#charter). Wrong class fails (C on a charter change is illegal). | In force: C1. |
| UC7 | **Adversarial review.** Second role attacks the plan before emit. Open FAIL blocks [ship](TERMS.md#ship) unless rebutted. | In force: C23. |
| UC8 | **[Prove](TERMS.md#prove) / [ship](TERMS.md#ship).** AI gates green = compile. `Ratified-by` (class A/B/D/E/F) and `Released-by` (always) = [ship](TERMS.md#ship). Unmet [gate](TERMS.md#gate) prints Step 1…N. | In force: `ci-fitness.sh`, `release-audit.py`, C24. |
| [UC9](TERMS.md#uc9) | **Change a [requirement](TERMS.md#requirement).** Human changes one ADR/rule. [Compiler](TERMS.md#compiler) diffs tagged nouns/verbs/goals and regenerates that [blast radius](TERMS.md#blast-radius) only. | Impact graph + `nlc-delta-regen.py`; `--orchestrate` queue (see [`IMPACT-GRAPH.md`](spine/IMPACT-GRAPH.md)). |
| UC10 | **[Defect](TERMS.md#defect) is upstream.** Emit wrong → [RCA](TERMS.md#rca) to [interview](TERMS.md#interview) / [ADR](TERMS.md#adr) / [rule](TERMS.md#rule). Human does not patch generated code. | [Charter](TERMS.md#charter) + [ADR](TERMS.md#adr) 0006. |
| UC11 | **Breaking [contract](TERMS.md#contract).** Additive = quiet. Break stays red until the human accepts the *[requirement](TERMS.md#requirement)*, not the schema. | [ADR](TERMS.md#adr) 0006. |
| UC12 | **Expand the closed set.** New [primitive](TERMS.md#primitive) or [tag](TERMS.md#tag) is an [ADR](TERMS.md#adr), then a row in [`integrity/primitives.md`](../integrity/primitives.md). Prefer tag/fact before a new [primitive](TERMS.md#primitive). | In force as SSOT file. Runner parked. |
| UC13 | **Durable [goal](TERMS.md#goal) → engine [tag](TERMS.md#tag).** `goal.durable ∧ engine.runtime ≠ (named runtime) → forbid`. Temporal is a tagged [noun](TERMS.md#noun), not a fourth citizen. | [ADR](TERMS.md#adr) 0007. |
| [UC14](TERMS.md#uc14) | **[Rule](TERMS.md#rule) conflict at adopt-time.** Same [tag](TERMS.md#tag)+[primitive](TERMS.md#primitive) match with incompatible effects (e.g. `pan ∧ return → forbid` vs `pan ∧ return → must export`). Higher **[ADR](TERMS.md#adr) precedence tier** wins; tie → human records override (ADR 0012). Not “encrypt vs cannot store” (those compose). | v1: `check-rule-adoption.py`. |
| [UC15](TERMS.md#uc15) | **Adopt in a repo.** [Greenfield](TERMS.md#greenfield): `nlc-init`. [Brownfield](TERMS.md#brownfield): beta manual path. | [Greenfield](TERMS.md#greenfield) CLI v1; [brownfield](TERMS.md#brownfield) doc only. |
| [UC16](TERMS.md#uc16) | **[Code packs](TERMS.md#code-pack) / interior swap.** Same contracts; replace one [noun](TERMS.md#noun)’s interior (Python → Rust, file log → Logstash). | Parked: `docs/LANGUAGE-SCANNER.md`. Engine [tag](TERMS.md#tag): 0007. |
| UC17 | **Record / supersede.** New decision = [ADR](TERMS.md#adr). Old [ADR](TERMS.md#adr) marked superseded, not deleted. | In force: R22. |
| [UC18](TERMS.md#uc18) | **Knowledge facts.** [Interview](TERMS.md#interview) writes facts the rules can bind (invoice receives payments, PAN is in scope). Unbound fact → UC1 continues. | `knowledge/facts.json` + `validate-knowledge-facts.py`. |
| ~~[UC19](TERMS.md#uc19)~~ | *Retired (ADR 0016).* [Hub](TERMS.md#hub) does not [ship](TERMS.md#ship) product requirements. Shape example only: `docs/worked-examples/pan-handling/`. | **[Requirement packs](TERMS.md#requirement-pack)** — v0.2 (`TODO`). |
| [UC20](TERMS.md#uc20) | **Call-tree inventory.** Verb → interior [primitive](TERMS.md#primitive) functions. Extra/missing [primitive](TERMS.md#primitive) vs bind list fails. | [ADR](TERMS.md#adr) 0009. [Gate](TERMS.md#gate) parked. |
| [UC21](TERMS.md#uc21) | **[Gate](TERMS.md#gate) after every generate.** Metrics first; default-fail [gate](TERMS.md#gate) on that artifact before the next statement. | [ADR](TERMS.md#adr) 0010 / [PLANIT](TERMS.md#planit) 6.5. Binder parked. |


---

## Needed (Missing rows are required)

These are not a someday list. The spine does not close without them.

| ID | Why it is needed |
|----|------------------|
| [UC9](TERMS.md#uc9) (rule-tagged blast radius) | v2: narrow `rule:` changes via [tag](TERMS.md#tag) bindings, not all goals. |
| [UC14](TERMS.md#uc14) edge cases | Composable obligations and cross-primitive policy need richer IR over time. |
| [UC15](TERMS.md#uc15) [brownfield](TERMS.md#brownfield) | Automated inventory/migration not shipped. |
| [UC18](TERMS.md#uc18) harness wire-up | Mandatory `load-knowledge-domain` / `nlc-before-generate` on every generate path. |
| [Requirement packs](TERMS.md#requirement-pack) (v0.2) | Ingest → ratify → export → consume ADR/rule bundles (ADR 0016). Not [UC19](TERMS.md#uc19). |

Parked (needed at expansion): [UC16](TERMS.md#uc16) [code packs](TERMS.md#code-pack), [UC20](TERMS.md#uc20) call-tree packs, [Rule IR](TERMS.md#rule-ir) for UC4/UC5.

---

## Not human stories


- Design the Invoice class
- Write or patch generated source to “make it green”
- Inherit one [noun](TERMS.md#noun) from another
- Open-ended [primitive](TERMS.md#primitive) names invented at emit time

---

## Next process (not more Python regex)

When a row is **Missing**, the work is an [ADR](TERMS.md#adr) or a content-type, then a bindable [gate](TERMS.md#gate).
Do not mint an **R** id until the [gate](TERMS.md#gate) exists (R27).
