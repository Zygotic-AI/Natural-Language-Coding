## 8. Repository shape

> **TODO (carried forward):** vocabulary rename — "laws"/"invariants" → **adjective** is a whole-document pass, not applied locally here.
> **TODO (carried forward):** "binder" → **gate** (binding = planning act; gate = verification act). Not applied locally.
> **TODO (open):** workflow listed as a peer of noun/verb/goal. ACS says workflow is a goal-of-goals. Confirm before this lands.

Suggested layout. Adapt names; keep the separations.

```text
repo/
├─ CHARTER.md                          # this document, or a pointer to it
├─ adrs/
│   ├─ 0001-boundary-based-programming.md
│   └─ 0002-invoice-verbs.md
├─ domain/
│   └─ invoice/
│       ├─ invoice.ts                  # noun, private state
│       ├─ verbs/
│       │   ├─ issue.ts
│       │   ├─ apply-payment.ts
│       │   └─ void.ts
│       ├─ contracts/                  # canonical verb schemas
│       └─ tests/
├─ goals/
│   └─ record-bank-payment/
│       ├─ goal.yaml                   # purpose, owner, entrypoint, deps
│       ├─ contract-input.json
│       ├─ contract-output.json
│       ├─ implementation/
│       └─ tests/
├─ workflows/                          # if Temporal or equivalent
│   └─ collect-invoice-payment/
├─ contracts-shared/                   # canonical types referenced by both layers
└─ integrity/
    ├─ fitness/                        # lint/arch rules
    └─ checklist.md                    # or generate from this document
```

`capabilities/` as a second tree is optional. Do not add `governance/`, `compliance/`, `risk/` folders unless a real artifact has nowhere else to live. Empty architecture folders are how charters rot.

**ACS addition.** The layout above is the *compile target*, not the source. The source is intent — goals, requirements, ADRs — held by humans. The AI compiler emits this tree. Every path here must be BBA-shaped or the compile fails: nouns own adjectives, verbs are the only mutation, goals call verbs and never write fields. A goal folder that reimplements an adjective is not a valid output; the gate fails it before it ships.

**How §8 works in the merge:** the repo shape is unchanged — it was already correct BBA. ACS adds one sentence: this tree is generated from intent, and the compiler is not allowed to emit anything that violates the shape. The "do not add governance/compliance/risk folders" rule stands; those concerns are annotations on nouns, verbs, and goals, not sibling trees.
