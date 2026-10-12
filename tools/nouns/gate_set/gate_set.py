"""ADR 0051 gate-set path enumeration (SSOT for S-GATE-SET-REGISTRY).

Membership: tracked paths that grade hub/adopter work in CI (primary: invoked by
hub compile fitness + releasable gate argv), plus verifier/orchestration paths.
Documented exclusions are not gate-set members.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import re
import subprocess
from pathlib import Path

# Intentional exclusions (not grading gates); reason per entry.
GATE_SET_EXCLUSIONS: dict[str, str] = {
    "docs/history/": "provenance only; never a pass/fail grading input (ADR 0051 table)",
    "docs/rca/": "provenance only; never a pass/fail grading input (ADR 0051 table)",
    "reviews/": "provenance only; never a pass/fail grading input (ADR 0051 table)",
}

GATE_SET_INFRASTRUCTURE: tuple[str, ...] = (
    "tools/ci_fitness.py",
    "tools/ci-fitness.sh",
    "tools/nouns/ci_fitness/ci_fitness.py",
    "tools/generate-gate-set-baseline-manifest.py",
    "integrity/releasable-gates.json",
    ".github/workflows/fitness.yml",
    ".github/workflows/release.yml",
    ".github/workflows/history-rewrite-invariant.yml",
)

GATE_SET_VERIFIER_PREFIXES: tuple[str, ...] = (
    "tools/nouns/owner_sidecar/",
    "tools/nouns/gate_set/",
    "tools/nouns/gate_set_manifest/",
    "tools/nouns/fitness_adr_owner_sidecar/",
    "tools/nouns/fitness_gate_set_manifest/",
    "tools/nouns/fitness_owner_key_trust/",
    "tools/nouns/fitness_owner_ratification_known_bad/",
)


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
    return [line.strip().replace("\\", "/") for line in (proc.stdout or "").splitlines() if line.strip()]


def _is_excluded(rel: str) -> bool:
    for prefix, _reason in GATE_SET_EXCLUSIONS.items():
        if rel == prefix.rstrip("/") or rel.startswith(prefix):
            return True
    if "/__pycache__/" in rel or rel.endswith(".pyc"):
        return True
    return False


def _prefix_gate_set(rel: str) -> bool:
    if _is_excluded(rel):
        return False
    if rel.startswith("tools/nouns/fitness_") or rel.startswith("tools/nouns/assert_"):
        return True
    if rel.startswith("tools/fitness-") and rel.endswith(".py"):
        return True
    if rel.startswith("tools/assert-") and rel.endswith(".py"):
        return True
    name = rel.rsplit("/", 1)[-1]
    if rel.startswith("integrity/owner-keys/"):
        return True
    if rel.startswith("integrity/") and "EXCLUSIONS" in name:
        return True
    if rel.startswith("integrity/") and name.endswith("-exclusions.json"):
        return True
    if rel == "integrity/releasable-gates.json":
        return True
    for prefix in GATE_SET_VERIFIER_PREFIXES:
        if rel.startswith(prefix):
            return True
    if rel in GATE_SET_INFRASTRUCTURE:
        return True
    return False


def _paths_from_ci_fitness_source(root: Path) -> set[str]:
    rels: set[str] = set()
    src = (root / "tools/nouns/ci_fitness/ci_fitness.py").read_text(encoding="utf-8")
    for match in re.finditer(r'TOOLS / "([^"]+\.py)"', src):
        rels.add(f"tools/{match.group(1)}")
    for match in re.finditer(r'TOOLS / "([^"]+)"', src):
        name = match.group(1)
        if name.endswith(".py"):
            rels.add(f"tools/{name}")
    # Dynamic landmine glob: assert-*-fails.py
    tools = root / "tools"
    if tools.is_dir():
        for path in tools.glob("assert-*-fails.py"):
            rels.add(str(path.relative_to(root)).replace("\\", "/"))
        for path in tools.glob("fitness-*.py"):
            rels.add(str(path.relative_to(root)).replace("\\", "/"))
    for rel in GATE_SET_INFRASTRUCTURE:
        rels.add(rel)
    # Noun packages backing each fitness/assert adapter
    for rel in list(rels):
        if rel.startswith("tools/fitness-") and rel.endswith(".py"):
            stem = rel[len("tools/fitness-") : -3].replace("-", "_")
            prefix = f"tools/nouns/fitness_{stem}/"
            for tracked in _git_tracked_files(root):
                if tracked.startswith(prefix):
                    rels.add(tracked)
        if rel.startswith("tools/assert-") and rel.endswith(".py"):
            stem = rel[len("tools/assert-") : -3].replace("-", "_")
            prefix = f"tools/nouns/assert_{stem}/"
            for tracked in _git_tracked_files(root):
                if tracked.startswith(prefix):
                    rels.add(tracked)
    return rels


def _paths_from_releasable_gates(root: Path) -> set[str]:
    rels: set[str] = set()
    manifest = root / "integrity/releasable-gates.json"
    if not manifest.is_file():
        return rels
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for gate in (data.get("gates") or {}).values():
        argv = gate.get("argv") or []
        for part in argv:
            if isinstance(part, str) and part.endswith(".py"):
                name = Path(part).name
                rels.add(f"tools/{name}")
    for name in data.get("hub_only_fitness") or []:
        if isinstance(name, str) and name.endswith(".py"):
            rels.add(f"tools/{name}")
    return rels



def _paths_from_gate_specimens(root: Path, tracked: set[str]) -> set[str]:
    """Known-bad, landmine, and expected pass/fail specimen bytes gates read."""
    members: set[str] = set()
    for rel in tracked:
        if rel.startswith("tools/fixtures/"):
            members.add(rel)
        if rel.startswith("tools/examples/"):
            members.add(rel)
        if rel.startswith("examples/"):
            members.add(rel)
    return members

def iter_gate_set_relative_paths(root: Path) -> list[str]:
    """Return sorted repo-relative tracked gate-set members."""
    tracked = set(_git_tracked_files(root))
    members: set[str] = set()
    for rel in tracked:
        if _prefix_gate_set(rel):
            members.add(rel)
    members.update(_paths_from_ci_fitness_source(root) & tracked)
    members.update(_paths_from_releasable_gates(root) & tracked)
    for prefix in GATE_SET_VERIFIER_PREFIXES:
        for rel in tracked:
            if rel.startswith(prefix):
                members.add(rel)
    for rel in GATE_SET_INFRASTRUCTURE:
        if rel in tracked:
            members.add(rel)
    for rel in tracked:
        if rel.startswith("integrity/owner-keys/"):
            members.add(rel)
    members.update(_paths_from_gate_specimens(root, tracked))
    members = {rel for rel in members if not _is_excluded(rel)}
    return sorted(members)


def is_gate_set_path(root: Path, rel_posix: str) -> bool:
    normalized = rel_posix.replace("\\", "/").lstrip("./")
    return normalized in set(iter_gate_set_relative_paths(root))


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
    for rel in iter_gate_set_relative_paths(root):
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
            or rel in GATE_SET_INFRASTRUCTURE
            or rel == "tools/nouns/ci_fitness/ci_fitness.py"
        ):
            counts["verifier_orchestration"] += 1
    return counts
