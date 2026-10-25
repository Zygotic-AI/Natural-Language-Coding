"""CI-less script test: throwaway key via --test-fingerprint (tests only)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts" / "sign-adrs.sh"
GOAL = ROOT / "goals" / "sign_adrs" / "execute.sh"


def _run(
    argv: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=str(cwd) if cwd else None, env=env, capture_output=True, text=True, check=False
    )


def _make_key(home: Path, name: str) -> str:
    home.mkdir(parents=True, exist_ok=True)
    os.chmod(home, 0o700)
    conf = home / "key.conf"
    conf.write_text(
        "%no-protection\nKey-Type: EDDSA\nKey-Curve: ed25519\nKey-Usage: sign\n"
        f"Name-Real: {name}\nName-Email: {name}@example.invalid\nExpire-Date: 1d\n",
        encoding="utf-8",
    )
    env = {**os.environ, "GNUPGHOME": str(home)}
    gen = _run(["gpg", "--batch", "--generate-key", str(conf)], env=env)
    if gen.returncode != 0:
        raise RuntimeError(gen.stderr or gen.stdout)
    listed = _run(["gpg", "--list-secret-keys", "--with-colons"], env=env)
    for line in (listed.stdout or "").splitlines():
        parts = line.split(":")
        if parts and parts[0] == "fpr":
            return parts[9]
    raise RuntimeError("no fingerprint")


def _write_adr(adr_dir: Path, name: str, body: str) -> Path:
    path = adr_dir / name
    path.write_text(body, encoding="utf-8")
    return path


def _check(ok_flag: bool, name: str, detail: object, acc: list[bool]) -> None:
    print(f"{'PASS' if ok_flag else 'FAIL'} {name}: {detail}")
    print(f"ASSERT:{'PASS' if ok_flag else 'FAIL'} {name}")
    acc.append(ok_flag)


def main() -> int:
    if not SCRIPT.is_file():
        print("ASSERT:FAIL missing scripts/sign-adrs.sh")
        return 1
    if not GOAL.is_file():
        print("ASSERT:FAIL missing goals/sign_adrs/execute.sh")
        return 1
    tmp = Path(tempfile.mkdtemp(prefix="nlc-sign-adrs-"))
    tree = tmp / "r"
    adr_dir = tree / "adrs"
    adr_dir.mkdir(parents=True)
    home = Path(tempfile.mkdtemp(prefix="nlc-sign-adrs-gpg-"))
    env = {**os.environ, "GNUPGHOME": str(home), "CI": "true", "GITHUB_ACTIONS": "1"}
    fp = _make_key(home, "script-test")
    a = _write_adr(
        adr_dir,
        "0001-one.md",
        "# ADR 0001\n\n- Status: Accepted\n\n## Decision\n\none\n",
    )
    b = _write_adr(
        adr_dir,
        "0002-two.md",
        "# ADR 0002\n\n- Status: Proposed\n\n## Decision\n\ntwo\n",
    )
    acc: list[bool] = []

    refused = _run([str(SCRIPT), "--root", str(tree), "--adr-dir", str(adr_dir)], env=env)
    _check(
        refused.returncode != 0 and "CI" in (refused.stderr or ""),
        "refuses CI without --ci-less",
        refused.stderr.strip()[:120],
        acc,
    )

    no_allow = _run(
        [
            str(SCRIPT),
            "--ci-less",
            "--test-fingerprint",
            fp,
            "--root",
            str(tree),
            "--adr-dir",
            str(adr_dir),
        ],
        env=env,
    )
    _check(
        no_allow.returncode != 0 and "allow-test-key" in (no_allow.stderr or ""),
        "test-fingerprint without --allow-test-key refuses",
        no_allow.stderr.strip()[:120],
        acc,
    )

    first = _run(
        [
            str(SCRIPT),
            "--ci-less",
            "--test-fingerprint",
            fp,
            "--allow-test-key",
            "--root",
            str(tree),
            "--adr-dir",
            str(adr_dir),
        ],
        env=env,
    )
    out = (first.stdout or "") + (first.stderr or "")
    _check(
        first.returncode == 0
        and (adr_dir / "0001-one.md.asc").is_file()
        and (adr_dir / "0002-two.md.asc").is_file()
        and "signed 2" in out
        and "UNLOCK" in out
        and "default-cache-ttl" in out
        and "pinentry-mode error" in out,
        "first run unlocks once then signs missing ADRs",
        out[-280:],
        acc,
    )
    wrapper = SCRIPT.read_text(encoding="utf-8")
    _check(
        "exec " in wrapper and "goals/sign_adrs/execute.sh" in wrapper,
        "scripts/sign-adrs.sh is a thin entrypoint to the goal",
        "exec wrapper",
        acc,
    )
    text = GOAL.read_text(encoding="utf-8")
    _check(
        "--pinentry-mode error" in text
        and "default-cache-ttl" in text
        and "nlc-sign-adrs-unlock" in text
        and "--output /dev/null" in text,
        "script does one throwaway unlock then refuses a recurring prompt",
        "needles present",
        acc,
    )
    first_a = (adr_dir / "0001-one.md.asc").read_bytes()
    first_b = (adr_dir / "0002-two.md.asc").read_bytes()

    second = _run(
        [
            str(SCRIPT),
            "--ci-less",
            "--test-fingerprint",
            fp,
            "--allow-test-key",
            "--root",
            str(tree),
            "--adr-dir",
            str(adr_dir),
        ],
        env=env,
    )
    out2 = (second.stdout or "") + (second.stderr or "")
    _check(
        second.returncode == 0
        and "nothing to sign" in out2
        and (adr_dir / "0001-one.md.asc").read_bytes() == first_a
        and (adr_dir / "0002-two.md.asc").read_bytes() == first_b,
        "second run is idempotent",
        out2[-200:],
        acc,
    )

    a.write_text(a.read_text(encoding="utf-8") + "\nedit\n", encoding="utf-8")
    third = _run(
        [
            str(SCRIPT),
            "--ci-less",
            "--test-fingerprint",
            fp,
            "--allow-test-key",
            "--root",
            str(tree),
            "--adr-dir",
            str(adr_dir),
        ],
        env=env,
    )
    out3 = (third.stdout or "") + (third.stderr or "")
    _check(
        third.returncode == 0
        and "signed 1" in out3
        and "0001-one.md" in out3
        and (adr_dir / "0002-two.md.asc").read_bytes() == first_b
        and (adr_dir / "0001-one.md.asc").read_bytes() != first_a,
        "third run signs only the stale ADR",
        out3[-240:],
        acc,
    )

    dry = _run(
        [
            str(SCRIPT),
            "--ci-less",
            "--dry-run",
            "--test-fingerprint",
            fp,
            "--allow-test-key",
            "--root",
            str(tree),
            "--adr-dir",
            str(adr_dir),
        ],
        env=env,
    )
    _check(
        dry.returncode == 0 and "DRY-RUN" in (dry.stdout or "") and "0 file" in (dry.stdout or ""),
        "dry-run after catch-up signs nothing",
        (dry.stdout or "")[-160:],
        acc,
    )

    missing_key = _run(
        [
            str(SCRIPT),
            "--ci-less",
            "--test-fingerprint",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
            "--allow-test-key",
            "--root",
            str(tree),
            "--adr-dir",
            str(adr_dir),
        ],
        env=env,
    )
    _check(
        missing_key.returncode != 0 and "not in the local keyring" in (missing_key.stderr or ""),
        "refuses when key is not in the keyring",
        (missing_key.stderr or "")[:160],
        acc,
    )

    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(home, ignore_errors=True)
    # b is written so the first run has two ADRs; keep the name live for linters.
    _ = b
    return 0 if all(acc) else 1


if __name__ == "__main__":
    raise SystemExit(main())
