# [Jobs to be done](TERMS.md#jobs-to-be-done)

Why adopters want **[Natural Language Coding](TERMS.md#nlc)**—outcomes people seek, not every compiler use-case id.

**Companion docs:** numbered [compiler](TERMS.md#compiler) stories live in [`USE-CASES.md`](USE-CASES.md). **ADR → binders:** [`ADR-ENFORCEMENT.md`](ADR-ENFORCEMENT.md), [`TODO`](../TODO).

**Precondition:** Work runs through interview → planit → generate → gate → `./nlc verify` on an [adopter](TERMS.md#adopter) compiled-system layout.

---

## Jobs (narrative)

### Policy, change, and traceability

**J1 — Policy → ADRs → code enforcement**  
Your standards become ratified [ADRs](TERMS.md#adr), bindable [rules](TERMS.md#rule), markers in code, and [gates](TERMS.md#gate)—so you can show where each policy is enforced.

**J2 — Technology or approach change with sized [blast radius](TERMS.md#blast-radius)**  
See who is affected (goals, callers, regen plan) before a runtime, interior, or integration change.

**J3 — [Goal](TERMS.md#goal) → code for simple [audit](TERMS.md#audit)**  
Reviewers trace behavior to a **named goal** and plan.

**J9 — Scope audit (tag or ADR range)**  
One pass: “where is this tag / ADR range enforced in the tree?”

### [Interview](TERMS.md#interview) and decisions

**J4 — Outcome in, spec out**  
State a result; emit waits until goals, ADRs, facts, and dependencies are bound.

**J5 — No invented requirements**  
Unbound claims stay in interview; generate does not expand scope silently.

**J6 — Durable decision log**  
ADRs with supersession; decisions stay findable.

### Change and contracts

**J7 — Breaking API change with a caller list**  
Contract breaks stay visible until requirements are accepted and callers are in the plan.

**J8 — [Requirement](TERMS.md#requirement) change without full rewrite**  
Change one ADR/[rule](TERMS.md#rule); regen only the affected [blast radius](TERMS.md#blast-radius).

**J10 — Detect conflicting obligations before code**  
Incompatible adopted rules fail at adopt-time.

### [Quality](TERMS.md#quality) and [ship](TERMS.md#ship)

**J11 — [Prove](TERMS.md#prove) before [ship](TERMS.md#ship)**  
`verify` / fitness green; human release steps where the [charter](TERMS.md#charter) requires them.

**J12 — [Defect](TERMS.md#defect) fixes upstream**  
Red [gate](TERMS.md#gate) → interview / ADR / rule / regen—not patch-to-green on generated output.

**J13 — [Gate](TERMS.md#gate) after every generate**  
No next step until that artifact’s metrics pass.

### Adoption and distribution

**J14 — [Greenfield](TERMS.md#greenfield) [app repo](TERMS.md#adopter) quickly**  
Install, lock, scaffold, menu.

**J15 — Upgrade [hub](TERMS.md#hub) semver safely**  
Lock + migration chain.

**J16 — Import [requirement packs](TERMS.md#requirement-pack)**  
Install and ratify **your** requirement bundles in **your** repo (export/consume).

### Review and roles

**J17 — Adversarial review before emit**  
Second role on the plan; open FAIL blocks [ship](TERMS.md#ship) unless rebutted.

**J18 — [Produce ≠ audit ≠ ship](TERMS.md#produce-audit-ship)**  
Separate writer, reviewer, releaser.

**J19 — Right [change class](TERMS.md#change-class)**  
Ceremony matches adjective / verb / goal / [charter](TERMS.md#charter) risk.

### Durable workflows

**J20 — Durable goals without a platform religion**  
Durable work binds to **tagged** engine nouns; bad pairings fail [gate](TERMS.md#gate).

**J21 — Idempotency under retry**  
Retries and verbs honor idempotency keys—checked in fitness.

---

## Mechanism map

| # | Job | Status | Mechanisms (when available) | Blocking gap (implementation) |
| --- | --- | --- | --- | --- |
| J1 | Policy → ADRs → enforcement | **Available** (v1) | [`rule-coverage`](../tools/nlc_rule_coverage.py), [`rule-emit`](../tools/nlc_rule_emit.py), [`rule-runner`](../tools/nlc_rule_runner.py), verify blockers | Full ADR 0007 **semantic** apply on every emit still expansion ([`ADR-ENFORCEMENT.md`](ADR-ENFORCEMENT.md) gap). |
| J2 | Tech change — sized blast radius | **Blocked** | [`nlc-delta-regen.py`](../tools/nlc-delta-regen.py), goal-bindings | UC16 adapters + full tag blast radius still expansion ([`IMPACT-GRAPH.md`](spine/IMPACT-GRAPH.md)). |
| J3 | Goal → code audit | **Available** | `goals/<id>/`; [planit](../.agents/skills/planit/SKILL.md); [`nlc_gate_record.py`](../tools/nlc_gate_record.py); `./nlc verify`. | — |
| J4 | Outcome in, spec out | **Available** | `/interview`, `.nlc/interview-packet.json`, [`validate-interview-packet.py`](../tools/validate-interview-packet.py) | — |
| J5 | No invented requirements | **Available** (v1) | `before-generate` stamp + maintainer generate tools | Every ad-hoc agent write path still expansion (UC18). |
| J6 | Decision log | **Available** | `adrs/`; [UC17](TERMS.md#uc17). | — |
| J7 | Breaking API + callers | **Available** | C10/C21 + [`contract-break-accept`](../tools/nlc_contract_break_accept.py); diff-scoped [`fitness-c10-changed.py`](../tools/fitness-c10-changed.py) / [`fitness-c21-changed.py`](../tools/fitness-c21-changed.py) when CHANGED listed | Full product verify (non-specimen) still evolving. |
| J8 | Requirement change — delta regen | **Available** (v1) | `nlc-delta-regen.py`, goal-bindings on multi-goal verify | Rule-tagged narrowing v2 still expansion. |
| J9 | Tag / ADR scope audit | **Available** | `./nlc maintainer rule-coverage`; `./nlc maintainer rule-emit`; `./nlc maintainer call-tree` (Python v1). | Per-stack call-tree packs still expansion (ADR 0009). |
| J10 | Rule conflicts at adopt | **Available** | [`check-rule-adoption.py`](../tools/check-rule-adoption.py); [ADR 0012](../adrs/0012-adr-precedence-and-rule-conflicts.md). | — |
| J11 | Prove before ship | **Available** | `./nlc verify`; [`VERIFY-AND-SHIP.md`](nlc/VERIFY-AND-SHIP.md); [`release-audit.py`](../tools/release-audit.py). | — |
| J12 | Defect upstream | **Available** | [UC10](TERMS.md#uc10); planit + regen path; charter defect policy. | — |
| J13 | Gate after generate | **Available** | [ADR 0010](../adrs/0010-gate-after-every-generate.md); `gate-record`; `nlc verify`. | — |
| J14 | Greenfield adopt | **Available** | [`nlc-init.py`](../tools/nlc-init.py); [`BOOTSTRAP.md`](adoption/BOOTSTRAP.md). | — |
| J15 | Hub upgrade | **Available** | [`nlc-update.py`](../tools/nlc-update.py); [`migrations/`](../migrations/README.md). | — |
| J16 | Requirement packs | **Available** (v1) | export/install, [`pack-ingest`](../tools/nlc-pack-ingest.py), `/requirement-pack-ingest` | Consume/regen hook + optional registry ([`TODO`](../TODO) Hub v0.2). |
| J17 | Adversarial before emit | **Available** | C23; [planit](../.agents/skills/planit/SKILL.md); [`bbp-reviewer`](../agents/). | — |
| J18 | Produce ≠ audit ≠ ship | **Available** | [ADR 0003](../adrs/0003-systems-extension-agent-nouns.md); agent roles. | — |
| J19 | Change class | **Available** | [`fitness-c1.py`](../tools/fitness-c1.py). | — |
| J20 | Durable + tagged engine | **Available** (v2) | `durable_engine_blockers` + `durable_rule_blockers` + `engine_runtime_tag_strict_blockers` | Bare `engine.runtime` tag insufficient when goal declares `engine_runtime`. |
| J21 | Idempotency under retry | **Available** | [`fitness-c15-idempotent.py`](../tools/fitness-c15-idempotent.py). | — |

**Blocked** = job is real; Accepted ADRs call for tooling we have not finished. Track in [`TODO`](../TODO) (ADR enforcement).
**`gate missing` badge:** see [`USE-CASES.md`](USE-CASES.md) Needed (expansion) and [`FINDINGS.md`](../FINDINGS.md) Parked — Accepted ADR ≠ wired deep gate.

---

## Related

| Topic | Doc |
| ----- | --- |
| [Compiler](TERMS.md#compiler) use-case ids | [`USE-CASES.md`](USE-CASES.md) |
| Impact / regen | [`spine/IMPACT-GRAPH.md`](spine/IMPACT-GRAPH.md) |
| ADR binders | [`ADR-ENFORCEMENT.md`](ADR-ENFORCEMENT.md) |
