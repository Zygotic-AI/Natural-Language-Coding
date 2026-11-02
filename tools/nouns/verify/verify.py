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
            rel = path.relative_to(root)
            key = str(rel).replace("\\", "/")
            if key in {
                "adrs/owner-approvals/staged-signing.statement.txt",
                "adrs/owner-approvals/staged-signing.approval.asc",
            }:
                continue
            rels.append(rel)
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
    """Write ``.nlc/verified.json`` only when a recorded file hash changed.

    ``recorded_at`` is left untouched when every path hash is the same, so a
    second verify-deep does not dirty the ledger.
    """
    path = verified_path(root)
    payload = build_fingerprint_manifest(root, hub_version)
    existing = _load_manifest(root)
    if isinstance(existing, dict) and existing.get("files") == payload["files"]:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
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
            bad.append(
                f"fingerprint .nlc/verified.json lists {rel} but the file is missing; "
                "refresh with ./nlc verify-deep"
            )
            continue
        got = _sha256_file(path)
        if got != want:
            bad.append(
                f"fingerprint .nlc/verified.json hash for {rel} does not match the file; "
                "refresh with ./nlc verify-deep"
            )
    for rel in iter_verify_paths(root):
        key = str(rel).replace("\\", "/")
        if key not in expected:
            bad.append(
                f"fingerprint .nlc/verified.json has no entry for {key}; "
                "refresh with ./nlc verify-deep"
            )
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
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from nlc_pipeline import is_hub_repo

    # The hub merge command is ./nlc verify, which runs the fitness suite.
    # App repos still use this fingerprint file. The hub uses the content-tree stamp.
    if not is_hub_repo(root):
        reasons.extend(fingerprint_mismatches(root))
    if reasons:
        return False, reasons

    if is_hub_repo(root):
        from nouns.releasable_gates.releasable_gates import run_profile

        if run_profile("verify", root.resolve()) != 0:
            reasons.append("releasable verify profile failed (see FAILED lines above)")
    return (len(reasons) == 0, reasons)


def emit_verify_fail(reasons: list[str], *, root: Path | None = None) -> None:
    print("Verify failed.", file=sys.stderr)
    for r in reasons[:12]:
        print(f"  {r}", file=sys.stderr)
    if len(reasons) > 12:
        print(f"  … and {len(reasons) - 12} more", file=sys.stderr)
    tree = root or Path.cwd()
    try:
        rel = tree.resolve().relative_to(Path(__file__).resolve().parents[3])
        tree_arg = str(rel) if str(rel) != "." else "."
    except ValueError:
        tree_arg = str(tree.resolve())
    print(f"Reproduce: ./nlc verify --project {tree_arg}", file=sys.stderr)
    print("  Or: ./nlc verify-deep  (full release gates + refresh fingerprints)", file=sys.stderr)


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
    from nlc_pipeline import is_hub_repo

    suite_code = _run_verify_suite(root)
    if suite_code is not None and suite_code != 0:
        print("Verify-deep failed (app verify-suite).", file=sys.stderr)
        print("  See docs/nlc/APP-VERIFY.md", file=sys.stderr)
        return suite_code

    if is_hub_repo(root):
        sys.path.insert(0, str(hub / "tools"))
        from nouns.releasable_gates.releasable_gates import run_profile

        code = run_profile("release", root.resolve())
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
        emit_verify_fail(["release profile failed"], root=root)
        return code

    from nlc_compliance import verify_deep_extra_blockers

    extra = verify_deep_extra_blockers(root)
    if extra:
        emit_verify_fail(extra)
        return 1

    path = verified_path(root)
    before = path.read_bytes() if path.is_file() else None
    path = write_verified(root, hub_version)
    from nlc_pipeline import clear_persisted_stage
    from nlc_dashboard import refresh_work_queue

    clear_persisted_stage(root, "verify")
    refresh_work_queue(root, hub_version)
    changed = before != path.read_bytes()
    state = "updated" if changed else "unchanged"
    print(f"Verify-deep passed. Fingerprints {state}: {path}")
    return 0


def assert_hash_ledger_stable() -> int:
    """Re-writing a hash ledger must not touch it when every recorded hash matches."""
    import subprocess
    import tempfile

    from nouns.adr_bind_snapshot.adr_bind_snapshot import write_bind_snapshot
    from nouns.evidence_ref.sync_content_tree_hash import sync_content_tree_hash
    from nouns.guide_state.guide_state import (
        before_generate_ok,
        before_generate_stamp_valid,
    )
    from nouns.install_hash_update.install_hash_update import (
        GLOBS,
        write_install_hashes,
    )

    def fail(msg: str) -> int:
        print(f"ASSERT:FAIL {msg}")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        goal = root / "goals" / "a.txt"
        adr = root / "adrs" / "0001.md"
        goal.parent.mkdir()
        adr.parent.mkdir()
        goal.write_text("one\n", encoding="utf-8")
        adr.write_text("adr\n", encoding="utf-8")
        write_verified(root, "0")
        ledger = json.loads(verified_path(root).read_text(encoding="utf-8"))
        ledger["recorded_at"] = "2020-01-01T00:00:00Z"
        verified_path(root).write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        before = verified_path(root).read_bytes()
        write_verified(root, "0")
        if verified_path(root).read_bytes() != before:
            return fail("verified.json changed when every file hash matched")
        goal.write_text("two\n", encoding="utf-8")
        write_verified(root, "0")
        after = json.loads(verified_path(root).read_text(encoding="utf-8"))
        if after["recorded_at"] == "2020-01-01T00:00:00Z":
            return fail("recorded_at stayed after a file hash changed")
        if after["files"]["adrs/0001.md"] != ledger["files"]["adrs/0001.md"]:
            return fail("unchanged path hash was rewritten")
        if after["files"]["goals/a.txt"] == ledger["files"]["goals/a.txt"]:
            return fail("changed path hash was not updated")

        if before_generate_ok(root, ["demo"]) != 0:
            return fail("before-generate stamp write failed")
        stamp_path = root / ".nlc" / "before-generate-stamp.json"
        stamp = json.loads(stamp_path.read_text(encoding="utf-8"))
        stamp["at"] = "2020-01-01T00:00:00Z"
        stamp_path.write_text(json.dumps(stamp, indent=2) + "\n", encoding="utf-8")
        if before_generate_ok(root, ["demo"]) != 0:
            return fail("before-generate re-run failed")
        if json.loads(stamp_path.read_text(encoding="utf-8"))["at"] != "2020-01-01T00:00:00Z":
            return fail("stamp at changed when product hash matched")
        if not before_generate_stamp_valid(root, max_age_seconds=1):
            return fail("matching product hash was treated as stale")
        goal.write_text("three\n", encoding="utf-8")
        if before_generate_stamp_valid(root, max_age_seconds=86400):
            return fail("stamp stayed valid after product bytes changed")
        if before_generate_ok(root, ["demo"]) != 0:
            return fail("stamp refresh after product change failed")
        refreshed = json.loads(stamp_path.read_text(encoding="utf-8"))
        if refreshed["at"] == "2020-01-01T00:00:00Z":
            return fail("stamp at was not updated after the product hash changed")
        if refreshed["product_content_sha256"] == stamp["product_content_sha256"]:
            return fail("stamp kept the old product hash")

        inst = root / "inst"
        for rel in GLOBS:
            path = inst / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("v1\n", encoding="utf-8")
        if write_install_hashes(inst) is not True:
            return fail("install ledger did not write an initial record")
        install_path = inst / "integrity" / "nlc-install-hashes.json"
        install_before = install_path.read_bytes()
        if write_install_hashes(inst) is not False or install_path.read_bytes() != install_before:
            return fail("install ledger changed when every hash matched")
        charter = inst / "CHARTER.md"
        charter.write_text("v2\n", encoding="utf-8")
        old_map = json.loads(install_before.decode("utf-8"))["files"]
        if write_install_hashes(inst) is not True:
            return fail("install ledger did not update after CHARTER.md changed")
        new_map = json.loads(install_path.read_text(encoding="utf-8"))["files"]
        if new_map["CHARTER.md"] == old_map["CHARTER.md"]:
            return fail("CHARTER.md hash was not updated")
        if new_map["scripts/install.sh"] != old_map["scripts/install.sh"]:
            return fail("unchanged install hash was rewritten")

        active = "| 0001 | L-1 | origin | effective |\n"
        snap = root / ".nlc" / "adr-bind-snapshot.json"
        if not write_bind_snapshot(snap, active):
            return fail("bind snapshot did not write an initial record")
        snap_data = json.loads(snap.read_text(encoding="utf-8"))
        snap_data["written_at"] = "2020-01-01T00:00:00Z"
        snap.write_text(json.dumps(snap_data, indent=2) + "\n", encoding="utf-8")
        if write_bind_snapshot(snap, active):
            return fail("bind snapshot rewrote an unchanged ACTIVE hash")
        if json.loads(snap.read_text(encoding="utf-8"))["written_at"] != "2020-01-01T00:00:00Z":
            return fail("written_at changed when the ACTIVE hash matched")
        if not write_bind_snapshot(snap, "| 0001 | L-1 | origin | later |\n"):
            return fail("bind snapshot did not update after ACTIVE changed")
        if json.loads(snap.read_text(encoding="utf-8"))["written_at"] == "2020-01-01T00:00:00Z":
            return fail("written_at stayed after the ACTIVE hash changed")

        tree = root / "tree"
        tree.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=tree, check=True)
        readme = tree / "README"
        readme.write_text("a\n", encoding="utf-8")
        subprocess.run(["git", "add", "README"], cwd=tree, check=True)
        sync_content_tree_hash(tree)
        digest_path = tree / "integrity" / "hub-content-tree-hash.txt"
        first = digest_path.read_bytes()
        mtime = digest_path.stat().st_mtime_ns
        sync_content_tree_hash(tree)
        if digest_path.read_bytes() != first or digest_path.stat().st_mtime_ns != mtime:
            return fail("content-tree hash file changed when the tree did not")
        readme.write_text("b\n", encoding="utf-8")
        sync_content_tree_hash(tree)
        if digest_path.read_bytes() == first:
            return fail("content-tree hash stayed after a tracked file changed")

    from nouns.gate_set.gate_set import is_gate_set_path

    hub = Path(__file__).resolve().parents[3]
    if is_gate_set_path(hub, "examples/invoice-correct/README.md"):
        return fail("example tree is still a signed gate-set member")
    if is_gate_set_path(hub, ".nlc/verified.json"):
        return fail("verified.json is still a signed gate-set member")
    if is_gate_set_path(hub, "FINDINGS.md"):
        return fail("FINDINGS.md is still a signed gate-set member")
    if not is_gate_set_path(hub, "tools/ci_fitness.py"):
        return fail("tools/ci_fitness.py fell out of the signed set")

    print("ASSERT:PASS hash ledgers stay put when recorded hashes match")
    return 0
