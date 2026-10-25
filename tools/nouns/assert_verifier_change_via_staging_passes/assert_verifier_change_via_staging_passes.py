"""Known-bad that must succeed: legitimate verifier change through staging + test-only sign."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ".agents/skills/planit/SKILL.md"
FIXTURE = ROOT / "tools" / "fixtures" / "staged-activation"
TEST_PUB = FIXTURE / "test-only.pub.asc"
TEST_SEC = FIXTURE / "test-only.sec.asc"
TEST_FPR = (FIXTURE / "TEST-ONLY-FINGERPRINT").read_text(encoding="utf-8").strip()


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(argv: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, env=merged)


def _scratch_hub() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="verifier-stage-"))
    dest = tmp / "hub"
    shutil.copytree(
        ROOT,
        dest,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "node_modules"),
    )
    _run(["git", "init"], dest)
    _run(["git", "config", "user.email", "scratch@test.invalid"], dest)
    _run(["git", "config", "user.name", "scratch"], dest)
    _run(["git", "add", "-A"], dest)
    commit = _run(["git", "commit", "-m", "scratch base"], dest)
    if commit.returncode != 0:
        raise RuntimeError(commit.stderr or commit.stdout)
    return dest


def _identity(hub: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        [
            sys.executable,
            str(hub / "tools" / "fitness-planit-identity.py"),
            "--skill-only",
            "--loaded",
            CANONICAL,
        ],
        hub,
    )


def _hook(hub: Path) -> subprocess.CompletedProcess[str]:
    return _run(
        ["bash", str(hub / ".cursor" / "hooks" / "nlc-planit-identity.sh")],
        hub,
        env={"PATH": os.environ.get("PATH", "")},
    )


def _must_identity_met(hub: Path, label: str) -> list[str]:
    errors: list[str] = []
    ident = _identity(hub)
    out = (ident.stdout or "") + (ident.stderr or "")
    if ident.returncode != 0 or "PLANIT_IDENTITY:MET" not in out:
        errors.append(f"{label}: identity not MET\n{out[-800:]}")
    hook = _hook(hub)
    hook_out = (hook.stdout or "") + (hook.stderr or "")
    if hook.returncode != 0 or '"permission":"allow"' not in hook_out:
        errors.append(f"{label}: hook did not allow\n{hook_out[-800:]}")
    return errors


def main() -> int:
    if not TEST_PUB.is_file() or not TEST_SEC.is_file():
        print("ASSERT:FAIL missing TEST-ONLY key fixture")
        return 1
    if TEST_FPR.upper() == "9D1BD57770FC3A1DE84702750AFD22B063AE01BC":
        print("ASSERT:FAIL TEST-ONLY fingerprint must not be the owner key")
        return 1
    hub = _scratch_hub()
    errors = _must_identity_met(hub, "commit-base")
    stage = _run(
        [
            sys.executable,
            str(hub / "tools" / "stage-gate-machinery.py"),
            "--change-id",
            "verifier-change",
            "--path",
            CANONICAL,
        ],
        hub,
    )
    if stage.returncode != 0:
        print("ASSERT:FAIL stage failed")
        print((stage.stdout or "") + (stage.stderr or ""))
        return 1
    staged = hub / "staging" / "verifier-change" / CANONICAL
    staged.write_text(
        staged.read_text(encoding="utf-8") + "\n<!-- legitimate staged verifier change -->\n",
        encoding="utf-8",
    )
    _run(["git", "add", "-A"], hub)
    _run(["git", "commit", "-m", "stage only; live unchanged"], hub)
    errors.extend(_must_identity_met(hub, "commit-staged"))
    sys.path.insert(0, str(hub / "tools"))
    from nouns.gate_activate.gate_activate import proposed_manifest_bytes
    from nouns.owner_sidecar.owner_sidecar import content_hash

    proposed = proposed_manifest_bytes(hub, "verifier-change")
    digest = content_hash(proposed)
    statement = hub / "tools" / "fixtures" / "staged-activation" / "proposed.statement.txt"
    statement.write_text(
        "\n".join(
            [
                "Repo: Zygotic-AI/Natural-Language-Coding",
                "Document: integrity/gate-set-baseline.manifest.sha256",
                f"Content-SHA256: {digest}",
                "Decision: Accepted",
                "Date: 2026-10-25",
                "Summary: TEST-ONLY legitimate verifier change through staging",
                "",
            ]
        ),
        encoding="utf-8",
    )
    gnupg = Path(tempfile.mkdtemp(prefix="test-only-gpg-"))
    gnupg.chmod(0o700)
    env = {"GNUPGHOME": str(gnupg)}
    imported = _run(["gpg", "--batch", "--import", str(TEST_SEC)], hub, env=env)
    if imported.returncode != 0:
        print("ASSERT:FAIL could not import TEST-ONLY key")
        print(imported.stderr)
        return 1
    signed = _run(
        [
            "gpg",
            "--batch",
            "--yes",
            "--pinentry-mode",
            "loopback",
            "--passphrase",
            "",
            "--clearsign",
            "-u",
            TEST_FPR,
            "-o",
            str(statement) + ".asc",
            str(statement),
        ],
        hub,
        env=env,
    )
    if signed.returncode != 0:
        print("ASSERT:FAIL TEST-ONLY clearsign failed")
        print((signed.stdout or "") + (signed.stderr or ""))
        return 1
    activate = _run(
        [
            sys.executable,
            str(hub / "tools" / "activate-gate-machinery.py"),
            "--change-id",
            "verifier-change",
            "--armor",
            str(statement) + ".asc",
            "--trusted-fingerprint",
            TEST_FPR,
            "--key-import",
            str(hub / "tools" / "fixtures" / "staged-activation" / "test-only.pub.asc"),
        ],
        hub,
    )
    act_out = (activate.stdout or "") + (activate.stderr or "")
    if activate.returncode != 0 or "ACTIVATE:MET" not in act_out:
        print("ASSERT:FAIL activate after TEST-ONLY sign must MET")
        print(act_out[-2000:])
        return 1
    if "legitimate staged verifier change" not in (hub / CANONICAL).read_text(encoding="utf-8"):
        print("ASSERT:FAIL live skill did not receive staged bytes")
        return 1
    _run(["git", "add", "-A"], hub)
    _run(["git", "commit", "-m", "atomic activate"], hub)
    errors.extend(_must_identity_met(hub, "commit-activated"))
    live_hash = _sha(hub / CANONICAL)
    registry = (hub / "integrity" / "planit-skill-registry.json").read_text(encoding="utf-8")
    if live_hash not in registry:
        errors.append("activated registry does not name live skill bytes")
    if errors:
        print("ASSERT:FAIL legitimate verifier change via staging")
        for item in errors:
            print(item)
        return 1
    print("ASSERT:PASS legitimate verifier change via staging; identity MET at every commit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
