"""Prove a harness loaded this repository's Planit skill."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import sys
from pathlib import Path

CANONICAL_PATH = ".agents/skills/planit/SKILL.md"
REGISTRY_REL = "integrity/planit-skill-registry.json"
EVIDENCE_REL = ".nlc/planit-change-evidence.json"
_SKIP = {".git", "__pycache__", ".venv", "venv", "node_modules", "dist"}


def content_hash(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def load_registry(root: Path) -> dict[str, object]:
    payload = json.loads((root / REGISTRY_REL).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {}
    return payload


def identity_errors(registry: dict[str, object], loaded_path: str, loaded: bytes) -> list[str]:
    errors: list[str] = []
    if loaded_path != registry.get("canonical_path"):
        errors.append("loaded path is not the canonical Planit skill")
    if content_hash(loaded) != registry.get("content_sha256"):
        errors.append("loaded Planit skill hash does not match the registry")
    return errors


def handoff_errors(record: dict[str, object], registry: dict[str, object]) -> list[str]:
    errors: list[str] = []
    if record.get("planit_skill_path") != registry.get("canonical_path"):
        errors.append("handoff Planit path does not match the registry")
    if record.get("planit_skill_sha256") != registry.get("content_sha256"):
        errors.append("handoff Planit hash does not match the registry")
    return errors


def source_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    paths: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in _SKIP for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        if rel == EVIDENCE_REL:
            continue
        paths.append(rel)
    for rel in sorted(paths):
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update((root / rel).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def evidence_errors(root: Path, registry: dict[str, object]) -> list[str]:
    path = root / EVIDENCE_REL
    if not path.is_file():
        return ["missing Planit change evidence"]
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        return ["Planit change evidence must be an object"]
    errors = handoff_errors(record, registry)
    if record.get("source_tree_sha256") != source_tree_hash(root):
        errors.append("Planit change evidence does not match the current tree")
    return errors


def prove(root: Path, loaded_path: str) -> list[str]:
    registry = load_registry(root)
    loaded = (root / loaded_path).read_bytes()
    return identity_errors(registry, loaded_path, loaded)


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    args = sys.argv[1:]
    loaded = CANONICAL_PATH
    if "--loaded" in args:
        loaded = args[args.index("--loaded") + 1]
    errors = prove(root, loaded)
    if "--record" in args and not errors:
        registry = load_registry(root)
        record = {
            "planit_skill_path": registry.get("canonical_path"),
            "planit_skill_sha256": registry.get("content_sha256"),
            "source_tree_sha256": source_tree_hash(root),
        }
        dest = root / EVIDENCE_REL
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print("PLANIT_IDENTITY:RECORDED")
        return 0
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("PLANIT_IDENTITY:NOT_MET")
        return 1
    if "--check-evidence" in args or ("--record" not in args and "--skill-only" not in args):
        evidence = evidence_errors(root, load_registry(root))
        if evidence:
            for item in evidence:
                print(f"VIOLATION {item}")
            print("PLANIT_IDENTITY:NOT_MET")
            return 1
    print("PLANIT_IDENTITY:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
