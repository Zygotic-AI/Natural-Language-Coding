# ADR 0016 — Hub carries no product requirements (UC19 retired)

- Status: Accepted
- Date: 2026-09-20
- Deciders: Human manager
- Class: F (product boundary)

## Context

USE-CASES listed **UC19** as a “full PCI” path in the hub. That implied this repository ships or certifies payment compliance. NLC is a **tool** for adopters to enforce **their** requirements in **their** app repos—not a carrier of PCI, HIPAA, or other product regulation.

The PAN worked example remains useful as **shape** (ADR → rules → tags → obligations), not as a hub use-case to complete.

## Decision

1. **UC19 is retired** as a hub deliverable. Do not track “full PCI walkthrough” in FINDINGS/TODO for this repo.

2. **Worked examples** under `docs/worked-examples/` are illustrative only; they are not requirements NLC imposes on adopters.

3. **Requirement packs** (ingest → ratify → export → consume) are the product line for sharing compliance and policy bundles—target **hub v0.2.0** (see [`TODO`](../TODO)).

4. **Language packs** (per-stack scanners / call-tree gates) and **rule IR** (engine for requirement packs) remain separate from UC19; see [`docs/nlc/README.md`](../docs/nlc/README.md).

## Consequences

- FINDINGS and USE-CASES no longer list UC19 as “needed.”
- Marketing and README state clearly: hub = compiler + gates; packs = adopter or marketplace content.

## Rejected

- Building PCI certification or walkthrough SSOT in the Natural-Language-Coding hub repo.
