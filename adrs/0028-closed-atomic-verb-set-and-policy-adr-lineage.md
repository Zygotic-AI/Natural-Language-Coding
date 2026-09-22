# ADR 0028 — Closed atomic verb set and policy-as-ADR lineage

- Status: Accepted
- Date: 2026-09-22
- Deciders: Human manager
- Class: B (emit shape / vocabulary) + F (process / enforcement)

## Context

The BBA emit process resolves nouns, assigns verbs, tags data, then evaluates a policy overlay before generation. Two open questions remained:

1. **Verb set size and ownership.** A small closed set of atomic verbs keeps composition honest; compound verbs become sequences. But adopters need the ability to extend the set at their own repo level without forking the hub.
2. **Policy versioning.** Policies (e.g. PCI) change over time. The existing ADR practice marks superseded records and keeps them forever, which grows the log and contradicts the desire for "only the applicable decision." We need a lineage model that preserves auditability without accumulating stale decisions.

## Decision

### 1. Closed atomic verb set, repo-owned with hub baseline

The hub ships a **baseline atomic verb set** — the minimum every compiled system must understand:

`create`, `read`, `write`, `update`, `delete`, `validate`, `emit`, `bind`.

- Every verb an adopter needs beyond this set is a **compound verb**: a named sequence of atomic verbs, each individually gated, plus an outer gate. No compound verb is a primitive.
- The set is **defined at the adopter repo level** (`.nlc/verbs.json` or equivalent), not inside the hub. The hub provides the baseline; the adopter extends it.
- Extending the set is an explicit, gated act: a new verb requires an ADR (or an accepted rule) citing why no compound of existing verbs suffices. The gate warns: *adding verbs is a footgun — every added verb widens the surface the policy overlay and audit must cover.*
- The baseline itself is versioned with the hub; adopters pin via the lock file (ADR 0015).

**Rationale:** a tiny set forces composition, which is where contracts and gates live. A large set hides composition inside names and defeats the overlay's ability to match on atomic operations.

### 2. Policies become ADRs; ADRs form immutable lineages

A policy document (regulation, standard, internal rule) is **not** stored as a living document the system reads at runtime. It is compiled into ADRs:

1. The policy text is passed through a prompt that extracts candidate decisions.
2. Each decision becomes an ADR that **cites the exact page and line numbers** of the source policy it implements.
3. Each ADR produces the if/then **rule set** the overlay evaluates (datum tag × atomic verb → obligation).
4. When the policy changes, the affected ADRs are revised by writing a **new ADR** that references the old one — the old ADR is never edited in place.

**Lineage, not accumulation.** An ADR that revises a prior decision does not merely mark the old one "superseded" and leave it in the active set. It forms a **lineage**: a chain of immutable records where only the tip is active. Readers and gates resolve to the tip; the chain is retained for audit.

- **Active set** = the tip of each lineage. This is what the overlay, audit, and RCA climb against.
- **Full history** = every link in every lineage, retained immutably (git provides this; the ADR index surfaces only tips).
- A lineage may be **retired** when the underlying policy is withdrawn — the tip is marked retired, the chain stays for audit, and no gate consults it.

**What this rejects:**

- Editing an accepted ADR in place to change its decision.
- Keeping superseded ADRs in the active set "for reference" — they belong in the lineage, not the active index.
- Treating the policy document itself as runtime input; the document is the *source*, the ADR lineage is the *law*.

**Open (deferred):** exact lineage data structure (file-per-link vs. index with parent pointers), retirement semantics, and how multi-policy conflicts resolve across lineages. Those are implementation details; the principle — immutable lineage, tip-is-active, policy-compiles-to-ADR — is settled here.

## Consequences

- `docs/bba/VERB-SET.md` and `docs/bba/POLICY-ADR-LINEAGE.md` document the two decisions for adopters.
- TERMS gains `atomic verb`, `compound verb`, `lineage`, `active set`.
- ADR-ENFORCEMENT and the ADR index gain row 0028.
- No new R ids in this ADR; binders land with the verb-set and lineage tools.
- The footgun warning is normative: an adopter extending the verb set without an ADR fails the contribution gate.

## Rejected

- **Unlimited verb vocabulary** — defeats composition and overlay matching.
- **Hub-owned verb set with no adopter extension** — blocks legitimate domain verbs.
- **In-place ADR edits** — destroys the immutable decision record the no-blame RCA depends on.
- **Superseded-but-active ADRs** — contradicts "only the applicable decision"; lineages solve this without deletion.
