"""ADR 0051 gate-set path enumeration (SSOT for S-GATE-SET-REGISTRY).

Membership equals the transitive load closure of everything CI runs (computed,
never hand-kept). Documented exclusions are not gate-set members.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import ast
import fnmatch
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath

# Intentional exclusions (not grading gates); reason per entry.
GATE_SET_EXCLUSIONS: dict[str, str] = {
    "docs/history/": "provenance only; never a pass/fail grading input (ADR 0051 table)",
    "docs/rca/": "provenance only; never a pass/fail grading input (ADR 0051 table)",
    "reviews/": "provenance only; never a pass/fail grading input (ADR 0051 table)",
    "staging/": "candidate bytes; live signed machinery verifies then atomic-activates (ADR 0055)",
    "examples/": "adopter specimens are test inputs, not the referee; editing one must not require an owner signature",
}

_EXCL_PREFIXES = tuple(GATE_SET_EXCLUSIONS.keys())
_BASES = ("", "tools/", "tools/nouns/")
_TOKEN = re.compile(r"[A-Za-z0-9_.\-/*]+")
_NAMESPACE_ROOTS = frozenset({"tools", "tools/nouns"})

# Exact-path derivation exclusions (not a pattern). Armor/statement name the
# manifest digest; including them would cycle. The whole-tree freshness stamp
# is a CI-loaded path, so without this exclude it becomes a signed member and
# every content edit requires a new owner signature (PR #30 option A).
MANIFEST_APPROVAL_ASC_REL = "integrity/gate-set-baseline.manifest.sha256.approval.asc"
BOOTSTRAP_STATEMENT_REL = "adrs/owner-approvals/staged-signing.statement.txt"
BOOTSTRAP_ARMOR_REL = "adrs/owner-approvals/staged-signing.approval.asc"
CONTENT_TREE_HASH_REL = "integrity/hub-content-tree-hash.txt"
# Generated ledgers and the findings narrative. The content-tree stamp already
# covers their bytes. Keeping them in the signed set made every refresh a new signature.
_LEDGER_EXCLUDE: frozenset[str] = frozenset(
    {
        ".nlc/verified.json",
        ".nlc/work-queue.json",
        ".nlc/before-generate-stamp.json",
        ".nlc/adr-bind-snapshot.json",
        ".nlc/planit-change-evidence.json",
        "FINDINGS.md",
    }
)
_DERIVATION_EXCLUDE: frozenset[str] = frozenset(
    {
        MANIFEST_APPROVAL_ASC_REL,
        BOOTSTRAP_STATEMENT_REL,
        BOOTSTRAP_ARMOR_REL,
        CONTENT_TREE_HASH_REL,
    }
) | _LEDGER_EXCLUDE
_PLACEHOLDER_ARMOR = b"-----BEGIN PGP SIGNED MESSAGE-----\nnot-valid\n"

# Once-per-run membership cache. Checks reuse this; they do not re-derive.
_PROCESS_CACHE: dict[str, list[str]] = {}
_COMPUTE_COUNT = 0
_ENV_CACHE = "NLC_GATE_SET_CACHE"


def armor_occupancy_paths() -> tuple[str, ...]:
    """Every path real owner armor occupies for this bootstrap (ADR 0055)."""
    return (MANIFEST_APPROVAL_ASC_REL, BOOTSTRAP_ARMOR_REL)


def place_placeholder_armor(root: Path) -> list[str]:
    """Write non-signature placeholder bytes at every occupancy path. Returns rels."""
    placed: list[str] = []
    for rel in armor_occupancy_paths():
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(_PLACEHOLDER_ARMOR)
        placed.append(rel)
    return placed


def _is_derivation_excluded(rel: str) -> bool:
    return rel in _DERIVATION_EXCLUDE


def _git_tracked_files(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    out: list[str] = []
    for line in (proc.stdout or "").splitlines():
        line = line.strip().replace("\\", "/")
        if not line or "__pycache__" in line or line.endswith(".pyc"):
            continue
        if _is_derivation_excluded(line):
            continue
        out.append(line)
    return sorted(out)


def _is_excluded(rel: str) -> bool:
    for prefix in _EXCL_PREFIXES:
        if rel == prefix.rstrip("/") or rel.startswith(prefix):
            return True
    if "/__pycache__/" in rel or rel.endswith(".pyc"):
        return True
    return False


def _norm_path(p: str) -> str:
    out: list[str] = []
    for part in p.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if out:
                out.pop()
            continue
        out.append(part)
    return "/".join(out)


def _closure_dirs(tracked: list[str]) -> dict[str, list[str]]:
    dirs: dict[str, list[str]] = {}
    for f in tracked:
        parts = f.split("/")
        for i in range(1, len(parts)):
            dirs.setdefault("/".join(parts[:i]), []).append(f)
    return dirs


def _glob_hits(c: str, raw: str, tracked: set[str]) -> set[str]:
    base = raw.rsplit("/", 1)[-1]
    if "**" in raw or re.fullmatch(r"\*(\.[A-Za-z0-9]+)?", base):
        return set()
    depth = c.count("/")
    return {f for f in tracked if f.count("/") == depth and fnmatch.fnmatchcase(f, c)}


def _resolve_ref(
    s: str, here: str, tracked: set[str], dirs: dict[str, list[str]]
) -> set[str]:
    s = s.strip().strip("'\"").lstrip("$").replace("\\", "/")
    if not s or len(s) > 300 or not s.strip("./"):
        return set()
    hits: set[str] = set()
    for base in (here + "/", *_BASES):
        c = _norm_path(base + s)
        if not c:
            continue
        if "*" in c:
            hits |= _glob_hits(c, s, tracked)
        elif c in tracked:
            hits.add(c)
        elif c in dirs and "/" in c and c not in _NAMESPACE_ROOTS:
            hits |= set(dirs[c])
    return hits


def _mod_files(
    dotted: str, here: str, level: int, tracked: set[str]
) -> set[str]:
    out: set[str] = set()
    if level:
        base = here.split("/")
        base = base[: len(base) - (level - 1)] if level > 1 else base
        bases = ["/".join(base) + "/"]
    else:
        bases = [here + "/", *_BASES]
    path = dotted.replace(".", "/")
    for b in bases:
        c = _norm_path(b + path)
        for cand in (c + ".py", c + "/__init__.py"):
            if cand in tracked:
                out.add(cand)
    return out


def _path_chain(node: ast.AST, vars_map: dict[str, str]) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return vars_map.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left, right = _path_chain(node.left, vars_map), _path_chain(node.right, vars_map)
        if right is None:
            return None
        return right if left is None else left + "/" + right
    return None


def _py_edges(
    root: Path, rel: str, tracked: set[str], dirs: dict[str, list[str]]
) -> set[str]:
    here = str(PurePosixPath(rel).parent)
    try:
        tree = ast.parse((root / rel).read_text(encoding="utf-8"))
    except Exception:
        return set()
    out: set[str] = set()
    vars_map: dict[str, str] = {}
    for n in ast.walk(tree):
        if (
            isinstance(n, ast.Assign)
            and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name)
            and isinstance(n.value, ast.BinOp)
        ):
            v = _path_chain(n.value, vars_map)
            if v is not None:
                vars_map[n.targets[0].id] = v
    for n in ast.walk(tree):
        if (
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr in ("glob", "rglob", "iterdir")
        ):
            base = _path_chain(n.func.value, vars_map)
            pat = (
                n.args[0].value
                if n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)
                else "*"
            )
            if base:
                for b in (here + "/", *_BASES):
                    d = _norm_path(b + base)
                    if d in dirs:
                        for member in dirs[d]:
                            rest = member[len(d) + 1 :]
                            if n.func.attr == "rglob":
                                if fnmatch.fnmatchcase(rest.rsplit("/", 1)[-1], pat):
                                    out.add(member)
                            elif n.func.attr == "iterdir" or fnmatch.fnmatchcase(
                                rest.split("/")[0], pat
                            ):
                                out.add(member)
        if isinstance(n, ast.Import):
            for a in n.names:
                parts = a.name.split(".")
                for i in range(1, len(parts) + 1):
                    out |= _mod_files(".".join(parts[:i]), here, 0, tracked)
        elif isinstance(n, ast.ImportFrom):
            m = n.module or ""
            parts = m.split(".") if m else []
            for i in range(1, len(parts) + 1):
                out |= _mod_files(".".join(parts[:i]), here, n.level, tracked)
            for a in n.names:
                out |= _mod_files((m + "." if m else "") + a.name, here, n.level, tracked)
        elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div):
            s = _path_chain(n, vars_map)
            if s:
                out |= _resolve_ref(s, here, tracked, dirs)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and "\n" not in n.value:
            if "/" in n.value or "." in n.value:
                out |= _resolve_ref(n.value, here, tracked, dirs)
    return out


def _text_edges(
    root: Path, rel: str, tracked: set[str], dirs: dict[str, list[str]]
) -> set[str]:
    here = str(PurePosixPath(rel).parent)
    try:
        txt = (root / rel).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return set()
    out: set[str] = set()
    for tok in _TOKEN.findall(txt):
        if "/" in tok or tok.endswith((".py", ".sh", ".json")):
            out |= _resolve_ref(tok, here, tracked, dirs)
    return out


def _pkg_edges(rel: str, tracked: set[str], dirs: dict[str, list[str]]) -> set[str]:
    out: set[str] = set()
    parts = rel.split("/")
    for i in range(1, len(parts)):
        d = "/".join(parts[:i])
        if d + "/__init__.py" in tracked:
            out.add(d + "/__init__.py")
    d = "/".join(parts[:-1])
    if d + "/__init__.py" in tracked and d not in _NAMESPACE_ROOTS:
        out |= {
            x
            for x in dirs.get(d, [])
            if not x.endswith(".py") or x.count("/") > d.count("/") + 1
        }
    return out


def _root_key(root: Path) -> str:
    return str(root.resolve())


def compute_count() -> int:
    """How many times membership was derived this process (tests)."""
    return _COMPUTE_COUNT


def reset_cache_for_tests(*, process_only: bool = False) -> None:
    """Drop the in-process cache. process_only keeps the run-cache file."""
    global _COMPUTE_COUNT
    _PROCESS_CACHE.clear()
    if not process_only:
        _COMPUTE_COUNT = 0


def _load_run_cache() -> list[str] | None:
    raw = os.environ.get(_ENV_CACHE, "").strip()
    if not raw:
        return None
    path = Path(raw)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, list) or not data:
        return None
    if not all(isinstance(item, str) and item for item in data):
        return None
    return list(data)


def _store_run_cache(paths: list[str]) -> None:
    raw = os.environ.get(_ENV_CACHE, "").strip()
    if not raw:
        return
    path = Path(raw)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(paths) + "\n", encoding="utf-8")


def _compute_gate_set_paths(root: Path) -> list[str]:
    """Transitive load closure of CI workflow seeds (v2 rules, sorted repo-relative paths)."""
    global _COMPUTE_COUNT
    _COMPUTE_COUNT += 1
    tracked_list = _git_tracked_files(root)
    tracked = set(tracked_list)
    dirs = _closure_dirs(tracked_list)
    seeds = {f for f in tracked if f.startswith(".github/workflows/")}
    todo, seen = list(seeds), set()
    while todo:
        f = todo.pop()
        if f in seen or _is_excluded(f) or _is_derivation_excluded(f):
            continue
        seen.add(f)
        if f.endswith(".py"):
            e = _py_edges(root, f, tracked, dirs) | _pkg_edges(f, tracked, dirs)
        elif f.endswith((".yml", ".yaml", ".sh")):
            e = _text_edges(root, f, tracked, dirs)
        else:
            e = set()
        todo.extend(
            x for x in e if x not in seen and not _is_derivation_excluded(x)
        )
    return sorted(seen)


def derive_gate_set_paths(root: Path) -> list[str]:
    """Return cached membership for this run, computing it at most once per root."""
    key = _root_key(root)
    hit = _PROCESS_CACHE.get(key)
    if hit is not None:
        return list(hit)
    cached = _load_run_cache()
    if cached is not None:
        _PROCESS_CACHE[key] = cached
        return list(cached)
    paths = _compute_gate_set_paths(root)
    _PROCESS_CACHE[key] = paths
    _store_run_cache(paths)
    return list(paths)


def prime_run_cache(root: Path, dest: Path | None = None) -> Path:
    """Compute membership once and publish the run-cache path for child checks."""
    path = dest
    if path is None:
        raw = os.environ.get(_ENV_CACHE, "").strip()
        path = Path(raw) if raw else Path(os.environ.get("TMPDIR", "/tmp")) / "nlc-gate-set-cache.json"
    os.environ[_ENV_CACHE] = str(path)
    reset_cache_for_tests(process_only=True)
    paths = _compute_gate_set_paths(root)
    _PROCESS_CACHE[_root_key(root)] = paths
    _store_run_cache(paths)
    return path


def iter_gate_set_relative_paths(root: Path) -> list[str]:
    """Return sorted repo-relative tracked gate-set members."""
    return derive_gate_set_paths(root)


def is_gate_set_path(root: Path, rel_posix: str) -> bool:
    normalized = rel_posix.replace("\\", "/").lstrip("./")
    return normalized in set(derive_gate_set_paths(root))


def gate_set_category_counts(root: Path) -> dict[str, int]:
    counts = {
        "fitness_nouns": 0,
        "assert_nouns": 0,
        "fitness_adapters": 0,
        "assert_adapters": 0,
        "verifier_orchestration": 0,
        "owner_keys": 0,
        "gate_specimens_fixtures": 0,
        "gate_specimens_examples": 0,
        "exclusions_registry": 0,
        "releasable_ssot": 0,
        "workflows": 0,
    }
    for rel in derive_gate_set_paths(root):
        if rel.startswith("tools/nouns/fitness_"):
            counts["fitness_nouns"] += 1
        elif rel.startswith("tools/nouns/assert_"):
            counts["assert_nouns"] += 1
        elif rel.startswith("tools/fitness-"):
            counts["fitness_adapters"] += 1
        elif rel.startswith("tools/assert-"):
            counts["assert_adapters"] += 1
        elif rel.startswith("tools/fixtures/"):
            counts["gate_specimens_fixtures"] += 1
        elif rel.startswith("examples/") or rel.startswith("tools/examples/"):
            counts["gate_specimens_examples"] += 1
        elif rel.startswith("integrity/owner-keys/"):
            counts["owner_keys"] += 1
        elif rel.startswith(".github/workflows/"):
            counts["workflows"] += 1
        elif "EXCLUSIONS" in rel or rel.endswith("-exclusions.json"):
            counts["exclusions_registry"] += 1
        elif rel == "integrity/releasable-gates.json":
            counts["releasable_ssot"] += 1
        elif (
            rel.startswith("tools/nouns/owner_sidecar/")
            or rel.startswith("tools/nouns/gate_set")
            or rel.startswith("tools/nouns/fitness_adr_owner")
            or rel.startswith("tools/nouns/fitness_gate_set")
            or rel.startswith("tools/nouns/fitness_owner")
            or rel == "tools/nouns/ci_fitness/ci_fitness.py"
            or rel.startswith("tools/ci")
        ):
            counts["verifier_orchestration"] += 1
    return counts
