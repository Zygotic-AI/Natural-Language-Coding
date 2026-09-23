# ADR 0029 — ADR lineage, ACTIVE set, and bind snapshot

Status: Accepted  
Date: 2026-09-22  
Corpus: nlc  
Origin: session decision — policy lineage and binding performance

## Context

Policies change. An ADR that says "encryption must be AES-256" this year becomes "AES-512" next year. We do not want ADRs to grow forever by accumulating cancelled predecessors, and we do not want the binding process to read every historical ADR on every plan.

## Decision

Three documents, not two. The binding process reads only the active set.

### 1. `adrs/INDEX.md` — full history

Every ADR ever written. Each entry carries:

- ADR number
- Created date
- Origin: source document, page, line number (for policy-derived ADRs)
- Status: active | superseded | retired
- Successor pointer: the ADR that replaced it, if any
- Lineage id: groups an ADR with its replacements

Nothing is ever deleted from INDEX. It is the audit trail.

### 2. `adrs/CATALOG.md` — one-line summaries

A flat, human-readable list of every ADR — active or not — with a one-line description. Used for navigation and search. Never used for binding. Cheap to scan, never authoritative for enforcement.

### 3. `adrs/ACTIVE.md` — tips of lineages

Only the current ADR per lineage. This is the **only** file the binding process reads. The rule is absolute: if an ADR is not in ACTIVE, it does not apply. No superseded-check logic lives in the binder. Lineage resolution happens once, at retirement time, when ACTIVE is updated.

## Lineage rule

When a policy changes:

1. A new ADR is written that references the old ADR (page, line, lineage id).
2. The old ADR's status becomes `superseded` in INDEX.
3. ACTIVE is updated: the old ADR is removed, the new one is added.
4. The old ADR is never edited. Its text stays as the record of what was true then.

Example: ADR-0142 says AES-256. Policy updates. ADR-0198 says AES-512, cites ADR-0142. ADR-0142 → superseded in INDEX, removed from ACTIVE, ADR-0198 → active in ACTIVE. One active rule, full history preserved.

## Bind snapshot

A plan snapshots the ACTIVE set at bind time. This gives reproducibility: you can prove exactly which rules a given emit was checked against.

A freshness check runs between bind and emit. If ACTIVE changed in that window, the plan fails and must re-bind. This gives freshness: a policy change mid-flight is caught, not silently applied to a stale plan.

Both, not either/or.

## Why three documents, not two

INDEX and CATALOG could be merged, but they serve different jobs with different shapes. INDEX carries lineage edges and origin citations — structured, audit-grade. CATALOG is a flat readable list for humans. Merging them makes both worse. The split is load-bearing, not cosmetic.

## Consequences

- Binder reads only `adrs/ACTIVE.md`. No history traversal at bind time.
- Retiring an ADR is a single, explicit operation: update INDEX status, update ACTIVE, write the successor.
- Policy-to-ADR compilation (page/line extraction) remains a separate process; this ADR defines the storage and binding contract, not the extraction mechanism.
- Tools (lineage resolver, ACTIVE freshness gate, bind snapshot) are gaps — law first, as usual.

## Open questions (implementation, not principle)

- Exact data structure of lineage edges in INDEX
- Soft vs hard retirement semantics
- Cross-lineage conflict detection when two active ADRs from different lineages conflict
