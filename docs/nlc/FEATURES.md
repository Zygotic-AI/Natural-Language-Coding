# Product features

Living SSOT for **what NLC already does**, **what we are thinking about**, **which of those sit on a milestone**, and **why**.

This file is not an architecture decision record. Records that must be enforced as law live under [`adrs/`](../../adrs/). This file keeps the story and the use cases so a teammate can ask an agent “why is this before that?” and get the same reasons we used here, without rehashing them with the original operator first.

**How to read**

| Section | Meaning |
| ------- | ------- |
| [Released](#released) | In the current ship (today **v0.5.0**) |
| [Upcoming](#upcoming) | Features we are thinking about. Longer than what we will put on milestones. Order here is the intended sequence, not a frozen calendar. |
| [Milestones](#milestones) | Slices we are actually scheduling. High confidence in the next one. Each further slice is more likely to move. We do not invent a long chain of milestones we already know will be wrong by the time we get there. |

When a reason or use case is spoken in planning, it is written here in the same change.

Companion maps (what the practice *does*, live gaps, task log): [`docs/JOBS-TO-BE-DONE.md`](../JOBS-TO-BE-DONE.md), [`docs/USE-CASES.md`](../USE-CASES.md), [`FINDINGS.md`](../../FINDINGS.md), [`TODO`](../../TODO).

---

## Released

Current ship: **v0.5.0**. First public cut was described as v0.1.0 in README history (install, lock, greenfield, interview, compile one step at a time, verify, impact graph, regen of the blast radius). GitHub Releases start at v0.3.0. If a released capability has no tighter tag story, it is listed as current ship.

The public site (naturallanguagecoding.ai / naturallanguagecompiler.ai) uses the full-job names (trace graph, rewrite MySQL to Oracle, HIPAA as code). Several of those names have a **first slice** in Released and a **full job** in Upcoming. NLC does not ship HIPAA, GDPR, PCI-DSS, or FedRAMP texts. Adopters bring packs.

### v0.1.0 first slice

| Feature | What the customer gets | Why it is here |
| ------- | ---------------------- | -------------- |
| One-line install | curl on Linux/macOS/WSL; PowerShell on Windows | Front door. No product if they cannot install. |
| Checksum-verified install | Tagged tarball into a local version store; bad download refuses | They should not run bytes we did not publish. |
| Compiler lock | App repo pinned to one hub version | Upgrades are a choice, not a surprise. |
| Greenfield app scaffold | `./nlc new` writes `./nlc`, lock, CI verify template | Empty-app path we trust more than existing-code path. |
| Plain-English interview | `/interview` splits what they said into named goals; no emit until goals, requirements, and facts are bound | Site “describe functionality.” Emit from unbound chat is how slop ships. |
| Incremental compile | `/planit` compiles one bound goal; small-context code; stop when a gate fails | Site “compile.” Whole-app dumps hide defects. |
| Tightly scoped emit and refuse | Atomic units; defects at compile time; do not hand-patch generated files | First slice of “no code slop.” Full precise rewrite is still upcoming. |
| Verify path | `./nlc verify` and `./nlc verify-deep`; red comes with next steps | Compile green is not hope. |
| Impact graph | Which goals call which noun verbs | Size a change before regenerating. Not yet the three-query trace graph. |
| Delta regeneration | Change one requirement; regen queue for the blast radius | First slice of “update.” Not architecture swap. |
| Human CLI dashboard | `./nlc` shows the queue and a short command map | Humans should not memorize maintainer flags. |

### v0.2.0 compiled-system close and packs

| Feature | What the customer gets | Why it is here |
| ------- | ---------------------- | -------------- |
| Requirement packs | Ingest a policy doc into candidates; human approves; export/install a versioned pack; regen hint after install | Site “add constraints” first slice. Hub still does not ratify policy from chat memory. |
| Hub-local pack list | Curated list when it has entries; empty list means install is not restricted | Honesty: not a public internet registry. |
| Policy to decisions to rules | A standard becomes an accepted decision, then if/then rules the compiler can run | First slice of policy-as-code. Types-and-actions in the app is upcoming. |
| Rule receipts in code | Markers on generated code; ask where a tag is enforced | First slice of auditability. |
| Rules that fight when you accept them | Two accepted rules that are a straight contradiction on the same thing fail before code | Already shipped. Combining rules that are not a fistfight is upcoming. |
| Knowledge facts before generate | Facts bound in interview; stamp before generate; refuse stale stamp | Do not invent requirements at emit. |
| Gate after every generate | Each artifact gated before the next statement; receipt so verify fails if skipped | No batch-generate then pray. |
| Adversarial review | Second role attacks the plan before emit | Writer is not the only eyes. |
| Produce, audit, and ship as separate roles | Human `Released-by:` on `CONFIRM.md` to ship | Compile green is not release. |
| Change class A–F | Ceremony matches risk | Illegal class fails. |
| Breaking-contract acceptance | Break stays red until the requirement is accepted; caller list | Schema diff is not the acceptance. |
| Durable workflows with tagged engines | Durable goals bind to a named engine; bad pairings fail | Engine is a tagged noun, not a fourth citizen. |
| Python call-tree inventory | Verb → interior functions in Python `domain/` | First language only. |
| Language inventory scan | List languages present | Inventory is not parity. |
| Brownfield inventory (beta) | `./nlc adopt-existing`; plan; v1 apply; still add one noun and one goal by hand | Not the full “install into this repo and migrate without starting over.” |
| Closed-set expansion | New primitive or tag is a decision first | Emit does not invent primitive names. |
| Decision log | Accepted decisions recorded; old ones superseded, not deleted | First slice of “all decisions are viewable.” |
| Defects go upstream | Bad emit is an interview/decision/rule miss; hand-patched generated files fail verify | Patching generated code hides the process defect. |
| Emit pipeline gates | No emit if the action is not on the plan or decisions are unbound | Default-closed around emit. |
| Semantic rule apply | Must/forbid on tagged Python goals | First slice. Combining across different actions is upcoming. |
| Human ship check | `./nlc ship-check` | Promotion is human. |
| Compiler upgrade | `./nlc upgrade` walks the version chain | Global upgrade exists; **per-repo install pin** is still upcoming. |
| Install doctor | `./nlc doctor` / `doctor fix` | Repair without re-reading the README. |
| Retry idempotency checks | Fail when a retry would double-apply | Fitness, not a dashboard feature. |
| Quality as ops vs defects | Each gate is pass or fail | No partial scores. |
| RCA packet | Record the process miss, not a person | Climb upstream. |
| TypeScript adapter specimen | Teaching example only | Not “we convert languages.” |
| Adopter CI template | `nlc-init` writes a verify workflow | PRs run `./nlc verify`. |

### v0.3.0–v0.5.0 (current ship)

| Feature | Version | What the customer gets | Why it is here |
| ------- | ------- | ---------------------- | -------------- |
| Zero-parameter hub `./release` | v0.3.0 | Hub maintainers cut a ship with no bump flags | Operator surface, not app compile. |
| Cursor Write/Delete hooks (to be removed) | v0.3.0 | Cursor-only early deny on `goals/` Write/Delete | **Wrong shape.** See Upcoming “No editor hooks” and [ADR 0058](../../adrs/0058-harness-and-model-agnostic.md). Does not see shell, other tool connections, or helper agents. Other editors have no such hook. |
| Loadable published skills | v0.4.0 | `/interview`, `/planit`, `/verify` load after install | Skills must parse. |
| Tag-time checker signature | v0.4.1 | Owner signs the checker digest at tag | Thinner than “customer proves the whole release is unedited.” |
| GitHub product name | v0.5.0 | Install from `Zygotic-AI/Natural-Language-Compiler` | Rename. Old name redirects. |
| Python-first compiled systems | v0.5.0 | Python apps compile and gate; other languages are listed, not equal | Honesty until “other languages” upcoming. |

---

## Upcoming

Intended sequence. More items than we will put on milestones. Convert-language is **not** its own product command; it is explained under Precise rewrite and Brownfield so we do not pretend there is `./nlc convert-language`.

### 1. No editor hooks (harness- and model-agnostic)

**What.** NLC does not ship or rely on editor/harness hooks. After the agent writes files, `./nlc verify` still fails if compiled files appeared without stamps and gates. No required model or agent host.

**Use cases.**

- Same compile rules in Cursor, Claude Code, Codex, Copilot, and anything else common.
- An agent writes generated files with a shell redirect, a helper agent, or a tool connection. Verify still catches it.
- A common model does poorly. We RCA NLC first. We only name a model or harness “not recommended” after we can show the expectation is reasonable and that setup still will not meet it.

**Why this order.** It is a single rule: no hooks. The alternative is “hooks if you remember, verify if you do not,” which is hope. We should not marry one editor before we brownfield ourselves. Law: [ADR 0058](../../adrs/0058-harness-and-model-agnostic.md) (Proposed). Removing the in-tree Cursor hooks is follow-on after that record is accepted.

**Later, not now.** A milestone may **enable a named harness**. That work adds accepted decisions for that harness, including “confirm this is the harness in use, error if it is not.” Until then, no hooks.

### 2. Install NLC into a specific repo

**What.** A repo can pin its own NLC copy. The machine-wide install can move without dragging every repo along.

**Use cases.**

- Several greenfield apps. Upgrade the global install. Leave one app on the older pin because it is not ready.
- The self-rewrite goes sideways. A repo stays on the last good pin.
- A test repo pins the self-rewrite build without affecting everything else.

**Why this order.** This is not only a brownfield surface. Greenfield needs it too. It has to exist **before** we brownfield ourselves, so a bad self-rewrite is survivable. Today install is per user (`~/.local/share/nlc`, `~/.local/bin`, `~/.agents/skills`).

### 3. Full requirement import

**What.** Any document becomes accepted goals and if/then constraints, each citing document, page, and line. The human edits and approves. The agent writes one chunk per pass (a section or a set of goals) and stops. Interview stays the path when there is no document.

**Use cases.** Drop a policy PDF/markdown in; do not play twenty questions inside the chunk. Approve or fix the slice. Repeat.

**Why this order.** Dogfood of this repo is “import our own docs.” That import has to exist first. Pack ingest today produces candidates; this is the full job.

### 4. Trace graph

**What.** One link from intention to constraint to code. Three queries: from code back to the goal and the decisions; from a policy such as PCI to every place it is enforced; find every use of a library, component, or action.

**Use cases.** Site “security / auditability / reproducibility.” Fix a vulnerability in one accepted decision and see every location. Walk a suspicious file back to why it exists.

**Why this order.** Precise rewrite and “constraints become types and actions” need to know what a change touches. The v0.1.0 impact graph is goal→verb calls only.

### 5. Precise rewrite

**What.** One accepted decision regenerates only the code it touches. Architecture swap (MySQL to Oracle) is an accepted decision plus recompile. Later edits replace those units. That is the no-code-slop rule.

**Convert language is not a separate feature.** Two paths, both already implied by other work:

- App already compiling with NLC: accept “output is language X” and recompile. QA as usual.
- App written elsewhere: brownfield it, then emit in the new language, compare original vs new, add goals and constraints as the comparison demands.

A how-to can list those steps. We do not need `./nlc convert-language` unless we later want a wrapper. Language conversion of a foreign app is brownfield, so it waits on brownfield. Architecture (and language) as an accepted decision plus recompile can exist for apps already in NLC without being its own command.

**Why this order.** Before we rewrite ourselves. After the graph, so the blast radius is real.

### 6. Constraints become types and actions in the app

**What.** An accepted constraint becomes data types and actions the app enforces. A later policy change uses precise rewrite on those units. Adopters bring HIPAA / GDPR / PCI-DSS / FedRAMP packs. The hub does not ship those texts.

**Use cases.** Site “policy-as-code” full job. Policy changes, only the units that policy owns are rewritten.

**Why this order.** Needs precise rewrite. Needed before we trust a self-rewrite of this repo.

### 7. Brownfield ourselves (first cut) — this is dogfood

**What.** Treat **this** repository like we did not write it. Inventory, plan, apply. Do not cheat by reading our own goals as if that were the import. This is how we learn brownfield: a first cut that works on us, then we refine on later repos until it is actually right.

**As-is source reading (what we used to isolate as “scanners”) lives here**, not as a greenfield extra. If emit is correct, compiled source is already documented. Reading as-is files is for code NLC did not produce. On a first-cut self-brownfield we pretend we did not produce it.

**Use cases.** Prove we can take a real tree without starting over. Install-into-repo is already done (item 2), so we can pin the experiment.

**Why this order.** After import, graph, precise rewrite, constraints-as-types, install-into-repo, and no editor hooks. Before we tell customers brownfield is done. Before we write the “rules that have to work together” combining logic, so we see real cases first.

**Why not cheat.** If the tool special-cases “this is the NLC hub, skip inventory,” we did not test brownfield. We tested a shortcut.

### 8. Rules that have to work together, not just fight

**What is already shipped.** Two accepted rules that are a straight contradiction on the **same** thing fail when you accept them. Example: “never return the card number” vs “must export the card number.”

**What this upcoming work is.** Rules that are not a fistfight but both have to be true, including across packs.

**Use case (encryption).** Company policy says encryption must be XYZ. A PCI-DSS pack says it must be ABC. NLC says: these two conflict; they can be resolved by the more stringent encryption. The **human accepts that resolution**, or modifies it and accepts the modification. Same shape if they uploaded corporate policy first and then install PCI-DSS (or a pack that builds the codified constraints): there is an **audit and a resolution process**. They accept the resolutions or edit them and accept their edits. Nothing silent.

**Why this order.** After we have brownfielded ourselves. If we invent the combining rules first, we will be stuck dogfooding inside a guess. Head-on fights-at-accept-time stay as they are.

### 9. Brownfield on other people’s repos

**What.** The same inventory / plan / apply path on trees we did not write, until it is correct. As-is source reading for those languages as they show up.

**Why this order.** First cut on us, then other repos. We do not claim brownfield done from one tree.

### 10. Other languages besides Python

**What.** Emit and check languages other than Python. Companies can adopt NLC in the language they already use.

**Why this order.** This repo is Python; self-brownfield does not need a second language. Convert-language of a foreign app is brownfield plus emit, not a third command. Public pack sharing waits until other languages exist, because companies show up when their language works, and then some of them will want to publish a PCI pack.

**Not bundled with the public pack list.** Packs are not tied to a language. We still sequence pack sharing **after** other languages for the adoption reason above, as two different upcoming items.

### 11. Public packs, signing, and registering with the NLC effort

**What.** A group registers a public key with the NLC effort. We check the email. They upload a signed bundle we can check file-by-file (a signed inventory of every file in that exact bundle) before we list it. We may run security checks. Users should still check what they use.

**Why this order.** After other languages, for the adoption reason in item 10. Not bundled *as the same work* as language emit.

**Problem that must be solved before this ships (not today).** Stolen signing keys and how a legitimate group rotates a key without letting a thief vote in a replacement.

Working sketch (not accepted law):

- A publisher registers an odd number of keys (3, 5, or 7). Any one key may publish.
- Revoking a key, or undoing a published pack, needs a request signed by a **majority of the other keys**. A thief needs a majority, not one laptop.
- The original people can email the NLC effort when something is badly wrong. Humans can freeze listings until it is sorted. Digital first; human-to-human when needed.
- Reputation: a publisher with one key is flagged less secure than one with five. We may later want a way to believe those keys are not all on one laptop. Not designed today.

Different knobs (do not mash them):

- **Stop listing an uploader** (spam / junk). We just do not distribute new bundles. Old signatures still verify as “this key signed that then.”
- **This pack version is withdrawn.** Not the same as banning the person.
- **This key may no longer sign new things** (leak). Old reviewed bundles can remain; new signatures from that key do not.
- **This is still the same group, new keys** (laptop died). Recovery cannot be “the stolen key said so.”

### 12. Finished low-code UI

**What.** A product UI on the same compile path. Until then: commands plus the agent.

**Why last.** We will not know the real surface until the compile path we are actually shipping exists. Building a UI on the current first slices would freeze the wrong shape.

---

## Milestones

Only slices we are scheduling. Confidence is highest in the next one.

### Next (high confidence)

**No editor hooks.** Accept [ADR 0058](../../adrs/0058-harness-and-model-agnostic.md). Remove in-tree Cursor hooks and the fitness that requires them. Verify on the files is the only notice path.

Open work: [`TODO`](../../TODO) rows under “No editor hooks.”

### After that (medium confidence)

**Install NLC into a specific repo** (Upcoming item 2). Needed before we brownfield ourselves.

### Not a milestone yet

Everything else in Upcoming stays on the thinking list. We will promote the next slice when we are close enough that the reasons will still be true. Enabling a named harness is a future milestone of its own, after “no hooks” is the default.

---

## Questions this file should answer without a new interview

- Why is install-into-a-repo before we brownfield ourselves? Because greenfield apps need a pin too, and a bad self-rewrite must be survivable.
- Why is dogfood brownfield on us, not a separate “rewrite from docs while skipping inventory”? Because that is how we learn brownfield without cheating.
- Why are as-is source readers part of brownfield? Because greenfield emit should already document the source.
- Why is convert-language not a feature? Because it is either “accept output language and recompile” or “brownfield then emit in the new language.”
- Why are public packs after other languages but not the same work? Packs are language-agnostic; companies arrive when their language works.
- Why no editor hooks? One rule. Verify on files. Do not marry a harness. Commodity models; RCA NLC before blaming the model.
- Why wait to combine rules that are not head-on fights? So we write that logic from cases we saw on our own tree, including company policy vs PCI encryption, with a human-accepted resolution.
- Why not solve stolen keys today? Signed public packs are not the next milestone. The majority-key sketch and the freeze-by-email path are recorded so we do not start pack signing without them.
