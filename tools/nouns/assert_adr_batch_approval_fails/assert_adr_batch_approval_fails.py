"""Known-bad: batch owner approval must fail closed on hash, wrong key, missing entry, tamper."""

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

from nouns.fitness_adr_owner_sidecar.fitness_adr_owner_sidecar import (  # noqa: E402
    sidecar_errors,
)
from nouns.owner_sidecar.owner_sidecar import (  # noqa: E402
    content_hash,
    verify_sidecar_p1,
)

_A = "adrs/0001-zero-variance-integrity.md"
_B = "adrs/0002-p2-scope.md"
_C = "adrs/0003-systems-extension-agent-nouns.md"


def _run(argv: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, env=env, capture_output=True, text=True, check=False)


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
    key_text = exported.stdout if isinstance(exported.stdout, str) else exported.stdout.decode("utf-8")
    (tree / "integrity/owner-keys/richard-pickett.asc").write_text(key_text, encoding="utf-8")
    (tree / "integrity/owner-keys/TRUSTED_FINGERPRINTS").write_text(
        f"# scratch pin\n{fp}\n", encoding="utf-8"
    )


def _statement(tree: Path, rels: list[str], *, corrupt: str | None = None) -> str:
    lines: list[str] = []
    for rel in rels:
        digest = content_hash((tree / rel).read_bytes())
        if rel == corrupt:
            digest = ("0" * 64) if digest[0] != "0" else ("1" * 64)
        lines.append(f"{rel} sha256:{digest}")
    return "\n".join(lines) + "\n"


def _clearsign(home: Path, body: str, dest: Path) -> None:
    env = {**os.environ, "GNUPGHOME": str(home)}
    dest.parent.mkdir(parents=True, exist_ok=True)
    src = dest.parent / (dest.name + ".txt")
    src.write_text(body, encoding="utf-8")
    proc = _run(["gpg", "--batch", "--yes", "--clearsign", "--output", str(dest), str(src)], env=env)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    src.unlink(missing_ok=True)


def _commit_batch(tree: Path, home: Path, fp: str, body: str, name: str) -> Path:
    dest = tree / "adrs" / "owner-approvals" / (name + ".approval.asc")
    _clearsign(home, body, dest)
    _run(["git", "add", "-A"], cwd=tree)
    _run(
        ["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", name, "--allow-empty"],
        cwd=tree,
    )
    return dest


def _clone() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="nlc-batch-kb-"))
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
                "isolate-batches",
                "--allow-empty",
            ],
            cwd=tree,
        )
    return tree


def _needles(errs: list[str], rel: str) -> list[str]:
    return [item for item in errs if rel in item]


def main() -> int:
    tree = _clone()
    home_a = Path(tempfile.mkdtemp(prefix="nlc-gpg-a-"))
    home_b = Path(tempfile.mkdtemp(prefix="nlc-gpg-b-"))
    fp_a = _make_key(home_a, "batch-a")
    fp_b = _make_key(home_b, "batch-b")
    _pin_key(tree, home_a, fp_a)
    ok = True

    # KB1: valid signature, one sha changed → that ADR NOT_MET
    dest1 = _commit_batch(tree, home_a, fp_a, _statement(tree, [_A, _B], corrupt=_A), "kb-hash")
    errs1 = sidecar_errors(tree)
    a1 = _needles(errs1, _A)
    b1 = _needles(errs1, _B)
    good1 = any("sha256 mismatch" in item or "batch sha256" in item for item in a1)
    print(f"{'PASS' if good1 else 'FAIL'} kb-hash-changed: A={a1[:1]} B_listed={bool(b1)}")
    print(f"ASSERT:{'PASS' if good1 else 'FAIL'} batch correct signature one sha changed")
    ok = ok and good1
    dest1.unlink()
    _run(["git", "add", "-A"], cwd=tree)
    _run(["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", "drop1"], cwd=tree)

    # KB2: other key → all listed ADRs NOT_MET
    dest2 = _commit_batch(tree, home_b, fp_b, _statement(tree, [_A, _B]), "kb-wrong-key")
    errs2 = sidecar_errors(tree)
    a2 = _needles(errs2, _A)
    b2 = _needles(errs2, _B)
    blob2 = " ".join(errs2)
    good2 = bool(a2) and bool(b2) and (
        "No public key" in blob2
        or "pinned key" in blob2
        or "trusted allowlist" in blob2
        or "gpg decrypt failed" in blob2
    )
    print(f"{'PASS' if good2 else 'FAIL'} kb-wrong-key: A={bool(a2)} B={bool(b2)}")
    print(f"ASSERT:{'PASS' if good2 else 'FAIL'} batch signed by another key")
    ok = ok and good2
    dest2.unlink()
    _run(["git", "add", "-A"], cwd=tree)
    _run(["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", "drop2"], cwd=tree)

    # KB3: missing from batch and no sidecar → NOT_MET
    _commit_batch(tree, home_a, fp_a, _statement(tree, [_A]), "kb-missing")
    errs3 = sidecar_errors(tree)
    c3 = _needles(errs3, _C)
    good3 = any("missing sidecar" in item for item in c3)
    print(f"{'PASS' if good3 else 'FAIL'} kb-missing-entry: C={c3[:1]}")
    print(f"ASSERT:{'PASS' if good3 else 'FAIL'} ADR missing from batch and no sidecar")
    ok = ok and good3

    # KB4: tamper batch body → signature invalid
    dest4 = tree / "adrs" / "owner-approvals" / "kb-missing.approval.asc"
    raw = dest4.read_text(encoding="utf-8")
    tampered = raw.replace("sha256:", "sha256:", 1)
    if "sha256:" in raw:
        idx = raw.index("sha256:") + 7
        hexpart = raw[idx : idx + 64]
        flip = ("0" * 64) if hexpart[0] != "0" else ("f" * 64)
        tampered = raw[:idx] + flip + raw[idx + 64 :]
    dest4.write_text(tampered, encoding="utf-8")
    _run(["git", "add", "-A"], cwd=tree)
    _run(["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", "tamper"], cwd=tree)
    errs4 = sidecar_errors(tree)
    blob4 = " ".join(errs4)
    good4 = (
        "gpg decrypt failed" in blob4
        or "BADSIG" in blob4
        or "signature" in blob4.lower()
        or "GOODSIG" in blob4
        or "no VALIDSIG" in blob4
        or "gpg status missing" in blob4
    )
    print(f"{'PASS' if good4 else 'FAIL'} kb-tamper: {errs4[:1]}")
    print(f"ASSERT:{'PASS' if good4 else 'FAIL'} tampered batch body signature invalid")
    ok = ok and good4

    # Existing sidecar rejections still reject
    fixture = ROOT / "tools/fixtures/owner-ratification-sidecar/accepted-doc-no-sidecar.md"
    miss = verify_sidecar_p1(ROOT, fixture.relative_to(ROOT).as_posix())
    good5 = any("missing sidecar" in item for item in miss)
    wrong = ROOT / "tools/fixtures/owner-ratification-sidecar/wrong-key.approval.asc"
    stub = "tools/fixtures/owner-ratification-sidecar/stub-doc.md"
    from nouns.owner_sidecar.owner_sidecar import verify_sidecar_p1_on_bytes

    wrong_errs = verify_sidecar_p1_on_bytes(
        ROOT, document_rel=stub, document_bytes=(ROOT / stub).read_bytes(), asc_path=wrong, status="Accepted"
    )
    good6 = any("No public key" in item or "gpg" in item.lower() for item in wrong_errs)
    print(f"{'PASS' if good5 else 'FAIL'} existing missing-sidecar still rejects")
    print(f"{'PASS' if good6 else 'FAIL'} existing wrong-key sidecar still rejects")
    print(f"ASSERT:{'PASS' if good5 and good6 else 'FAIL'} existing sidecar rejections")
    ok = ok and good5 and good6

    shutil.rmtree(tree.parent, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
