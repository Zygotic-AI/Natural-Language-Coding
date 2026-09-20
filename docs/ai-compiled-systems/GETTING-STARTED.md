# Getting started (about five minutes)

1. **Install** (macOS / Linux / WSL):

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.sh | bash
   ```

2. **Open your app repo** in Cursor (or work in this hub for charter/tool changes).

3. **`/interview`** — state the outcome; bind goals, requirements, and knowledge domains. Stop when gaps are closed or explicitly waived. Do not emit product code in this pass.

4. **`/planit`** — load → plan → bind → generate (one artifact) → gate → prove. See [PROCESS.md](PROCESS.md).

5. **Red vs green** — from hub install path:

   ```bash
   bash ~/.local/share/nlc/hub/tools/ci-fitness.sh
   python3 ~/.local/share/nlc/hub/tools/release-audit.py /path/to/your-app
   ```

   Prove PASS is compile. Ship needs human `Released-by:`.

Adopt a new repo: [BOOTSTRAP.md](../adoption/BOOTSTRAP.md). Words: [GLOSSARY.md](GLOSSARY.md).
