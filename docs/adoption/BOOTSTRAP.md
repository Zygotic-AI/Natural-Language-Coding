# Bootstrap an [adopter repo](../TERMS.md#adopter) (UC15)

Use this when the **[compiled system](../TERMS.md#compiled-system)** lives in **your** repository—not in this [hub](../TERMS.md#hub)’s `examples/` specimens.

## Minimum layout

Per [charter](../TERMS.md#charter) §8 ([`CHARTER.md`](../../CHARTER.md)):

```text
your-app/
├─ CHARTER.md              # copy or submodule pointer to hub charter
├─ adrs/
├─ goals/                  # one folder per goal
├─ domain/                 # one folder per noun
├─ integrity/              # fitness config for this tree (optional at day one)
└─ .github/workflows/      # optional: run fitness + release-audit before merge
```

Reference shape (Python specimen): [`examples/invoice-correct/`](../../examples/invoice-correct/) — **fixture only**, not a product template.

## [Greenfield](../TERMS.md#greenfield) (preferred)

```bash
python3 /path/to/nlc-hub/tools/nlc-init.py ~/projects/my-app --name MyApp
```

Refuses non-empty `domain/` or `goals/` (brownfield: [BROWNFIELD.md](BROWNFIELD.md)).

## Steps

1. **Create the repo** — [greenfield](../TERMS.md#greenfield): `nlc-init` above; [brownfield](../TERMS.md#brownfield): existing codebase (beta).

2. **Install [NLC](../TERMS.md#nlc)** on the machine that runs agents:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.sh | bash
   ```

   Remote install fetches the latest **semver release tarball** (or `NLC_VERSION` / `NLC_REF` override). [Hub](../TERMS.md#hub) lands in `~/.local/share/nlc/versions/<semver>/` with an active `hub` pointer. [Verify](../TERMS.md#verify): [`integrity/nlc-install-hashes.json`](../../integrity/nlc-install-hashes.json) unless `NLC_SKIP_VERIFY=1`.

   [Greenfield](../TERMS.md#greenfield) scaffold writes [`.nlc/lock.json`](../../integrity/schemas/nlc-lock.schema.json). Upgrade later: `python3 ~/.local/share/nlc/hub/tools/nlc-update.py` from the [app repo](../TERMS.md#adopter) (ADR 0014).

3. **Add [charter](../TERMS.md#charter)** — copy [`CHARTER.md`](../../CHARTER.md) or link in root `README.md` to the [hub](../TERMS.md#hub) revision you adopt.

4. **Copy CI hooks** from [hub](../TERMS.md#hub) (adjust paths):

   ```bash
   # From hub root (${NLC_INSTALL_ROOT}/hub or this clone)
   ./nlc verify-deep && ./nlc verify   # compile gates (hub: ci_fitness via verify-deep)
   python3 tools/release-audit.py .  # ship — after human Released-by:
   ```

5. **[Interview](../TERMS.md#interview)** in Cursor on the [app repo](../TERMS.md#adopter): goals, requirements, [knowledge domains](../TERMS.md#knowledge-domain) bound before emit.

6. **[Planit](../TERMS.md#planit)** first [boundary](../TERMS.md#boundary): one [noun](../TERMS.md#noun) + verbs, or one [goal](../TERMS.md#goal) calling existing verbs—[prove](../TERMS.md#prove) before the next statement ([`PROCESS.md`](../ai-compiled-systems/PROCESS.md), [ADR](../TERMS.md#adr) 0010).

7. **Adoption done** when [charter](../TERMS.md#charter) §14 is true (real noun, real goal, deliberate gate red in CI, written agent loop).

## [Hub](../TERMS.md#hub) vs [adopter](../TERMS.md#adopter)

| Lives in [hub](../TERMS.md#hub) | Lives in [adopter](../TERMS.md#adopter) |
| ------------ | ---------------- |
| [Charter](../TERMS.md#charter) SSOT, [integrity](../TERMS.md#integrity) theory, `tools/` sources | Your `domain/`, `goals/`, app ADRs |
| `examples/*` [gate](../TERMS.md#gate) specimens | Your [compiled system](../TERMS.md#compiled-system) |
| Portable skills (install copies to `~/.agents/skills`) | Repo-specific fitness [binding](../TERMS.md#binding) (which tools scan which tree) |

## Still missing (honest)

Full automated “create repo from template” CLI is not shipped. Fact SSOT (UC18), rule-conflict at adopt (UC14), and [delta-regen](../TERMS.md#delta-regen-queue) (UC9) are open — see [`FINDINGS.md`](../../FINDINGS.md).

## Template stub

Optional copy-paste: [`templates/adopter/README.md`](../../templates/adopter/README.md).
