# Bootstrap an adopter repo (UC15)

Use this when the **compiled system** lives in **your** repository—not in this hub’s `examples/` specimens.

## Minimum layout

Per charter §8 ([`CHARTER.md`](../../CHARTER.md)):

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

## Greenfield (preferred)

```bash
python3 /path/to/nlc-hub/tools/nlc-init.py ~/projects/my-app --name MyApp
```

Refuses non-empty `domain/` or `goals/` (brownfield: [BROWNFIELD.md](BROWNFIELD.md)).

## Steps

1. **Create the repo** — greenfield: `nlc-init` above; brownfield: existing codebase (beta).

2. **Install NLC** on the machine that runs agents:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.sh | bash
   ```

   Remote install fetches the latest **semver release tarball** (or `NLC_VERSION` / `NLC_REF` override). Hub lands in `~/.local/share/nlc/versions/<semver>/` with an active `hub` pointer. Verify: [`integrity/nlc-install-hashes.json`](../../integrity/nlc-install-hashes.json) unless `NLC_SKIP_VERIFY=1`.

   Greenfield scaffold writes [`.nlc/lock.json`](../../integrity/schemas/nlc-lock.schema.json). Upgrade later: `python3 ~/.local/share/nlc/hub/tools/nlc-update.py` from the app repo (ADR 0014).

3. **Add charter** — copy [`CHARTER.md`](../../CHARTER.md) or link in root `README.md` to the hub revision you adopt.

4. **Copy CI hooks** from hub (adjust paths):

   ```bash
   # From hub root (${NLC_INSTALL_ROOT}/hub or this clone)
   python3 tools/ci_fitness.py       # prove — compile (Windows: ci-fitness.ps1)
   python3 tools/release-audit.py .  # ship — after human Released-by:
   ```

5. **Interview** in Cursor on the app repo: goals, requirements, knowledge domains bound before emit.

6. **Planit** first boundary: one noun + verbs, or one goal calling existing verbs—prove before the next statement ([`PROCESS.md`](../ai-compiled-systems/PROCESS.md), ADR 0010).

7. **Adoption done** when charter §14 is true (real noun, real goal, deliberate gate red in CI, written agent loop).

## Hub vs adopter

| Lives in hub | Lives in adopter |
| ------------ | ---------------- |
| Charter SSOT, integrity theory, `tools/` sources | Your `domain/`, `goals/`, app ADRs |
| `examples/*` gate specimens | Your compiled system |
| Portable skills (install copies to `~/.agents/skills`) | Repo-specific fitness binding (which tools scan which tree) |

## Still missing (honest)

Full automated “create repo from template” CLI is not shipped. Fact SSOT (UC18), rule-conflict at adopt (UC14), and delta-regen (UC9) are open — see [`FINDINGS.md`](../../FINDINGS.md).

## Template stub

Optional copy-paste: [`templates/adopter/README.md`](../../templates/adopter/README.md).
