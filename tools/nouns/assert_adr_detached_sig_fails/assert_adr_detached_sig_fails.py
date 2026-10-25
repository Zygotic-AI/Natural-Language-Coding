"""Known-good / known-bad: Accepted ADR per-file detached signatures (ADR 0056)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.adr_file_sig import adr_file_sig as afs  # noqa: E402
from nouns.fitness_adr_owner_sidecar.fitness_adr_owner_sidecar import (  # noqa: E402
    sidecar_errors,
)

_A = "adrs/0001-zero-variance-integrity.md"


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


def _pin_key(tree: Path, home: Path, fp: str) -> None:
    env = {**os.environ, "GNUPGHOME": str(home)}
    exported = _run(["gpg", "--armor", "--export", fp], env=env)
    (tree / "integrity/owner-keys/richard-pickett.asc").write_text(exported.stdout, encoding="utf-8")
    (tree / "integrity/owner-keys/TRUSTED_FINGERPRINTS").write_text(
        f"# scratch pin\n{fp}\n", encoding="utf-8"
    )


def _detach_sign(home: Path, doc: Path, dest: Path) -> None:
    env = {**os.environ, "GNUPGHOME": str(home)}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.unlink(missing_ok=True)
    proc = _run(
        ["gpg", "--batch", "--yes", "--detach-sign", "--armor", "--output", str(dest), str(doc)],
        env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)


def _clearsign(home: Path, body: str, dest: Path) -> None:
    env = {**os.environ, "GNUPGHOME": str(home)}
    dest.parent.mkdir(parents=True, exist_ok=True)
    src = dest.parent / (dest.name + ".txt")
    src.write_text(body, encoding="utf-8")
    proc = _run(
        ["gpg", "--batch", "--yes", "--clearsign", "--output", str(dest), str(src)], env=env
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    src.unlink(missing_ok=True)


def _clone() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="nlc-adr-sig-"))
    tree = tmp / "r"
    subprocess.run(["git", "clone", "--local", "-q", str(ROOT), str(tree)], check=True)
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    subprocess.run(["git", "-C", str(tree), "checkout", "-q", head], check=True)
    batch_dir = tree / "adrs" / "owner-approvals"
    if batch_dir.is_dir():
        for path in batch_dir.iterdir():
            if path.is_file() and path.name.endswith(".approval.asc"):
                path.unlink()
    for leftover in (tree / "adrs").glob("[0-9][0-9][0-9][0-9]-*.md.asc"):
        leftover.unlink()
    _run(["git", "add", "-A"], cwd=tree)
    _run(
        [
            "git",
            "-c",
            "user.email=kb@example.invalid",
            "-c",
            "user.name=kb",
            "commit",
            "-m",
            "isolate-adr-sigs",
            "--allow-empty",
        ],
        cwd=tree,
    )
    return tree


def _needles(errs: list[str], rel: str) -> list[str]:
    return [item for item in errs if rel in item]


def _check(ok_flag: bool, name: str, detail: object, acc: list[bool]) -> None:
    print(f"{'PASS' if ok_flag else 'FAIL'} {name}: {detail}")
    print(f"ASSERT:{'PASS' if ok_flag else 'FAIL'} {name}")
    acc.append(ok_flag)


def main() -> int:
    tree = _clone()
    home_a = Path(tempfile.mkdtemp(prefix="nlc-gpg-a-"))
    home_b = Path(tempfile.mkdtemp(prefix="nlc-gpg-b-"))
    fp_a = _make_key(home_a, "adr-a")
    fp_b = _make_key(home_b, "adr-b")
    _pin_key(tree, home_a, fp_a)
    saved_pin = afs.PINNED_OWNER_FINGERPRINT
    afs.PINNED_OWNER_FINGERPRINT = fp_a
    acc: list[bool] = []

    doc = tree / _A
    sig = tree / f"{_A}.asc"

    _detach_sign(home_a, doc, sig)
    errs = sidecar_errors(tree)
    a_errs = _needles(errs, _A)
    _check(not a_errs, "valid per-file sig by pinned key passes", a_errs[:1], acc)

    original = doc.read_bytes()
    doc.write_bytes(original + b"\n# edited after signing\n")
    errs = sidecar_errors(tree)
    a_errs = _needles(errs, _A)
    _check(
        bool(a_errs)
        and any(
            "gpg verify failed" in item or "GOODSIG" in item or "VALIDSIG" in item for item in a_errs
        ),
        "a: ADR edited after signing fails",
        a_errs[:1],
        acc,
    )
    doc.write_bytes(original)

    _detach_sign(home_b, doc, sig)
    errs = sidecar_errors(tree)
    a_errs = _needles(errs, _A)
    blob = " ".join(a_errs)
    _check(
        bool(a_errs)
        and (
            "pinned key" in blob
            or "No public key" in blob
            or "gpg verify failed" in blob
            or "trusted" in blob
        ),
        "b: sig by a different key fails",
        a_errs[:1],
        acc,
    )

    sig.unlink(missing_ok=True)
    errs = sidecar_errors(tree)
    a_errs = _needles(errs, _A)
    _check(
        any("missing detached signature" in item for item in a_errs),
        "c: missing sig fails",
        a_errs[:1],
        acc,
    )

    from nouns.owner_sidecar.owner_sidecar import REPO_SLUG, content_hash

    digest = content_hash(doc.read_bytes())
    batch_body = (
        f"Repo: {REPO_SLUG}\n"
        "Statement: ADR batch owner approval\n"
        "Decision: Accepted\n"
        "Date: 2026-10-13\n"
        "Count: 1\n"
        f"{_A} sha256:{digest}\n"
    )
    batch_dest = tree / "adrs" / "owner-approvals" / "batch-only.approval.asc"
    _clearsign(home_a, batch_body, batch_dest)
    _run(["git", "add", "-A"], cwd=tree)
    _run(
        ["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", "batch"],
        cwd=tree,
    )
    errs = sidecar_errors(tree)
    a_errs = _needles(errs, _A)
    _check(
        any("missing detached signature" in item for item in a_errs),
        "d: batch statement present but no per-file sig fails",
        a_errs[:1],
        acc,
    )

    afs.PINNED_OWNER_FINGERPRINT = saved_pin
    shutil.rmtree(tree.parent, ignore_errors=True)
    return 0 if all(acc) else 1


if __name__ == "__main__":
    raise SystemExit(main())
