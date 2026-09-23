"""Fast fingerprint verify (.nlc/verified.json) and verify-deep (full gates + refresh)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIR_NAMES = {".git", ".nlc", "__pycache__", "node_modules", ".venv"}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_verify_paths(root: Path) -> list[Path]:
    """Paths that define compiled-system identity for fingerprint verify."""
    rels: list[Path] = []
    for pattern in (
        "adrs",
        "rules",
        "knowledge",
        "goals",
        "domain",
    ):
        base = root / pattern
        if not base.exists():
            continue
        if base.is_file():
            rels.append(base.relative_to(root))
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            if path.suffix in {".pyc", ".pyo"}:
                continue
            rels.append(path.relative_to(root))
    return rels


def build_fingerprint_manifest(root: Path, hub_version: str) -> dict:
    files: dict[str, str] = {}
    for rel in iter_verify_paths(root):
        files[str(rel).replace("\\", "/")] = _sha256_file(root / rel)
    return {
        "schema": 1,
        "algorithm": "sha256",
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hub": hub_version,
        "files": files,
    }


def verified_path(root: Path) -> Path:
    return root / ".nlc" / "verified.json"


def write_verified(root: Path, hub_version: str) -> Path:
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    payload = build_fingerprint_manifest(root, hub_version)
    path = verified_path(root)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _load_manifest(root: Path) -> dict | None:
    path = verified_path(root)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def fingerprint_mismatches(root: Path) -> list[str]:
    data = _load_manifest(root)
    if data is None:
        return ["no fingerprint record — run ./nlc verify-deep once"]
    expected: dict[str, str] = dict(data.get("files") or {})
    if not expected:
        return ["fingerprint record is empty — run ./nlc verify-deep"]
    bad: list[str] = []
    for rel, want in expected.items():
        path = root / rel
        if not path.is_file():
            bad.append(f"missing {rel}")
            continue
        got = _sha256_file(path)
        if got != want:
            bad.append(f"changed {rel}")
    for rel in iter_verify_paths(root):
        key = str(rel).replace("\\", "/")
        if key not in expected:
            bad.append(f"new {key}")
    return bad


def pipeline_blockers(root: Path) -> list[str]:
    from nlc_compliance import verify_fast_blockers
    from nlc_dashboard import requirements_incomplete, scan_requirements_work

    blockers: list[str] = []
    if requirements_incomplete(root):
        for item in scan_requirements_work(root):
            blockers.append(item.get("label", "requirements unfinished"))
    blockers.extend(verify_fast_blockers(root))
    regen = root / ".nlc" / "delta-regen-queue.json"
    if regen.is_file():
        try:
            data = json.loads(regen.read_text(encoding="utf-8"))
            steps = data.get("steps") or []
            if steps:
                blockers.append(f"{len(steps)} rebuild(s) still queued")
        except json.JSONDecodeError:
            blockers.append("invalid delta-regen queue")
    return blockers


def verify_fast(root: Path) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    reasons.extend(pipeline_blockers(root))
    reasons.extend(fingerprint_mismatches(root))
    return (len(reasons) == 0, reasons)


def emit_verify_fail(reasons: list[str]) -> None:
    print("Verify failed.", file=sys.stderr)
    for r in reasons[:12]:
        print(f"  {r}", file=sys.stderr)
    if len(reasons) > 12:
        print(f"  … and {len(reasons) - 12} more", file=sys.stderr)
    print("  Fix: /verify in your agent", file=sys.stderr)
    print("  Or: ./nlc verify-deep  (full check and refresh fingerprints)", file=sys.stderr)


def _run_verify_suite(root: Path) -> int | None:
    """Run adopter .nlc/verify-suite.json when present; None if skipped."""
    path = root / ".nlc" / "verify-suite.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("verify-deep: invalid .nlc/verify-suite.json", file=sys.stderr)
        return 1
    cmd = data.get("command")
    if not isinstance(cmd, list) or not cmd:
        print("verify-deep: verify-suite.json needs a command array", file=sys.stderr)
        return 1
    cwd = data.get("cwd", ".")
    work = (root / str(cwd)).resolve() if cwd != "." else root
    return subprocess.run([str(x) for x in cmd], cwd=str(work)).returncode


def verify_deep(root: Path, hub: Path, hub_version: str) -> int:
    fitness = hub / "tools" / "ci_fitness.py"
    from nlc_pipeline import is_hub_repo

    suite_code = _run_verify_suite(root)
    if suite_code is not None and suite_code != 0:
        print("Verify-deep failed (app verify-suite).", file=sys.stderr)
        print("  See docs/nlc/APP-VERIFY.md", file=sys.stderr)
        return suite_code

    if is_hub_repo(root) and fitness.is_file():
        code = subprocess.run(
            [sys.executable, str(fitness)],
            cwd=str(root),
        ).returncode
    elif (root / ".nlc" / "lock.json").is_file():
        audit = hub / "tools" / "release-audit.py"
        if audit.is_file():
            code = subprocess.run(
                [sys.executable, str(audit), str(root)],
                cwd=str(root),
            ).returncode
        else:
            code = 0
    else:
        print(
            "verify-deep: recording fingerprints only (add .nlc/lock.json for full gates).",
            file=sys.stderr,
        )
        code = 0

    if code != 0:
        print("Verify-deep failed (compile gates).", file=sys.stderr)
        print("  Fix: /verify in your agent", file=sys.stderr)
        return code

    from nlc_compliance import verify_deep_extra_blockers

    extra = verify_deep_extra_blockers(root)
    if extra:
        emit_verify_fail(extra)
        return 1

    path = write_verified(root, hub_version)
    from nlc_pipeline import clear_persisted_stage
    from nlc_dashboard import refresh_work_queue

    clear_persisted_stage(root, "verify")
    refresh_work_queue(root, hub_version)
    print(f"Verify-deep passed. Fingerprints updated: {path}")
    return 0
