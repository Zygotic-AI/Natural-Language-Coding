## 12. Minimal fitness checks to install

> **TODO (carried forward):** vocabulary rename — "laws"/"invariants" → **adjective** is a whole-document pass, not applied locally here.
> **TODO (carried forward):** "binder" → **gate** (binding = planning act; gate = verification act). Not applied locally.
> **TODO (open):** workflow listed as a peer of noun/verb/goal. ACS says workflow is a goal-of-goals. Confirm before this lands.

These are the smallest enforcement set. Language-specific tools vary (module visibility, ESLint boundaries, ArchUnit, import-linter, custom grep in CI). The check must fail the build, not warn.

1. **No field writes across the noun boundary.** Goal, workflow, and adapter packages cannot assign noun fields.
2. **No imports of noun internals.** Only the noun's public verb module is importable.
3. **No imports of goal internals from another goal.**
4. **Law locality.** A denylist of invariant identifiers or modules (status transition tables, rounding functions) that may only appear under `domain/<noun>/`.
5. **Contract presence.** A public entrypoint without a schema file (or generated schema) fails CI.
6. **Schema identity.** Same property name + different type across contracts in one change fails CI or a review bot.

Until check 1 exists, the charter is not in force. Start there.

---

**ACS addition — gates, not wishes.** Each check above is a gate: default-closed, binary outcome, evidence required. An item with no registered gate is marked **unbound**, never passed. The PLANIT bind step attaches the relevant rule to each atomic plan step before generation; the gate verifies after. A step that finds no applicable rule must explicitly declare "no bindings applicable" — that declaration is itself a binding.

**ACS addition — taint lifetime.** Check 1 is necessary but not sufficient. A goal that re-decides an adjective in its own logic — computing "is this invoice voidable?" instead of asking the Invoice boundary — never touches a field, so check 1 stays green while the rule forks. The gate family must also track adjective lifetimes: a sensitive adjective fetched inside a verb must be consumed in place or dropped; it must not be assigned to a field, passed to another boundary, or returned from the consuming verb. See A5 in the adversarial audit.

**ACS addition — non-OO escape hatches.** Private fields stop OO access, not raw SQL, ORM bypasses, deserialization, or reflection. A7 scans for those paths touching adjectives outside a published verb.

**How §12 works in the merge:** the six checks were already the right minimal set. ACS adds the gate semantics (default-closed, unbound-never-passed, binding declaration at plan time) and extends the family beyond field writes to cover adjective re-decision and non-OO escape hatches. Check 1 remains the first gate to build; the taint and escape-hatch gates follow.
