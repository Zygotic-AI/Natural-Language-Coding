# Getting started (about five minutes)

1. **Install**

   macOS / Linux / WSL:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.sh | bash
   ```

   Windows (PowerShell):

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass -Force
   irm https://raw.githubusercontent.com/Zygotic-AI/Natural-Language-Coding/main/scripts/install.ps1 | iex
   ```

2. **Open your app repo** in Cursor (or work in this hub for charter/tool changes).

3. **`/interview`** — state the outcome; bind goals, requirements, and knowledge domains. Use [INTERVIEW-PATTERNS.md](INTERVIEW-PATTERNS.md) when stuck. Stop when gaps are closed or explicitly waived. Do not emit product code in this pass.

4. **`/planit`** — load → plan → bind → generate (one artifact) → gate → prove. See [PROCESS.md](PROCESS.md).

5. **Red vs green** — from hub install path (`$env:USERPROFILE\.local\share\nlc\hub` on Windows):

   ```bash
   python3 tools/ci_fitness.py
   python3 tools/release-audit.py /path/to/your-app
   ```

   Windows: `python tools\ci_fitness.py` or `powershell -File tools\ci-fitness.ps1`. Prove PASS is compile. Ship needs human `Released-by:`.

Adopt a new repo: [BOOTSTRAP.md](../adoption/BOOTSTRAP.md). Words: [GLOSSARY.md](GLOSSARY.md).
