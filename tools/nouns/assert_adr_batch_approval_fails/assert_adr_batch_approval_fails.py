"""Known-bad: batch owner approval must fail closed on hash, key, path, header, sidecar."""

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
from nouns.owner_sidecar import owner_sidecar as osc  # noqa: E402
from nouns.owner_sidecar.owner_sidecar import (  # noqa: E402
    REPO_SLUG,
    content_hash,
    verify_sidecar_p1,
)

_A = "adrs/0001-zero-variance-integrity.md"
_B = "adrs/0002-p2-scope.md"
_C = "adrs/0003-systems-extension-agent-nouns.md"
_P46 = "adrs/0046-repository-planit-identity.md"
_S47 = "adrs/0047-adr-approval-receipts.md"
_PIN = osc.OWNER_BATCH_FINGERPRINT


def _run(argv: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, env=env, capture_output=True, text=True, check=False)


def _make_key(home: Path, name: str, *, rsa: bool = False) -> str:
    home.mkdir(parents=True, exist_ok=True)
    os.chmod(home, 0o700)
    conf = home / "key.conf"
    if rsa:
        body = (
            "%no-protection\nKey-Type: RSA\nKey-Length: 2048\nKey-Usage: sign\n"
            f"Name-Real: {name}\nName-Email: {name}@example.invalid\nExpire-Date: 1d\n"
        )
    else:
        body = (
            "%no-protection\nKey-Type: EDDSA\nKey-Curve: ed25519\nKey-Usage: sign\n"
            f"Name-Real: {name}\nName-Email: {name}@example.invalid\nExpire-Date: 1d\n"
        )
    conf.write_text(body, encoding="utf-8")
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


def _set_pin(fp: str) -> None:
    osc.OWNER_BATCH_FINGERPRINT = fp


def _statement(
    tree: Path,
    rels: list[str],
    *,
    corrupt: str | None = None,
    written: list[str] | None = None,
    repo: str = REPO_SLUG,
    decision: str = "Accepted",
    count: str | None = None,
    include_count: bool = True,
) -> str:
    paths = written if written is not None else list(rels)
    sha_lines: list[str] = []
    for rel, shown in zip(rels, paths):
        src = tree / rel
        digest = content_hash(src.read_bytes()) if src.is_file() else ("a" * 64)
        if rel == corrupt or shown == corrupt:
            digest = ("0" * 64) if digest[0] != "0" else ("1" * 64)
        sha_lines.append(f"{shown} sha256:{digest}")
    headers = [
        f"Repo: {repo}",
        "Statement: ADR batch owner approval",
        f"Decision: {decision}",
        "Date: 2026-10-13",
        "Signer: known-bad",
        "Meaning: known-bad",
    ]
    if include_count:
        headers.append(f"Count: {count if count is not None else str(len(sha_lines))}")
    return "\n".join(headers + sha_lines) + "\n"


def _clearsign(home: Path, body: str, dest: Path) -> None:
    env = {**os.environ, "GNUPGHOME": str(home)}
    dest.parent.mkdir(parents=True, exist_ok=True)
    src = dest.parent / (dest.name + ".txt")
    src.write_text(body, encoding="utf-8")
    proc = _run(["gpg", "--batch", "--yes", "--clearsign", "--output", str(dest), str(src)], env=env)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    src.unlink(missing_ok=True)


def _commit_batch(tree: Path, home: Path, body: str, name: str) -> Path:
    dest = tree / "adrs" / "owner-approvals" / (name + ".approval.asc")
    _clearsign(home, body, dest)
    _run(["git", "add", "-A"], cwd=tree)
    _run(
        ["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", name, "--allow-empty"],
        cwd=tree,
    )
    return dest


def _drop(tree: Path, dest: Path) -> None:
    if dest.is_file():
        dest.unlink()
    _run(["git", "add", "-A"], cwd=tree)
    _run(["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", "drop"], cwd=tree)


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


def _check(ok_flag: bool, name: str, detail: object, acc: list[bool]) -> None:
    print(f"{'PASS' if ok_flag else 'FAIL'} {name}: {detail}")
    print(f"ASSERT:{'PASS' if ok_flag else 'FAIL'} {name}")
    acc.append(ok_flag)


def main() -> int:
    tree = _clone()
    home_a = Path(tempfile.mkdtemp(prefix="nlc-gpg-a-"))
    home_b = Path(tempfile.mkdtemp(prefix="nlc-gpg-b-"))
    home_rsa = Path(tempfile.mkdtemp(prefix="nlc-gpg-rsa-"))
    fp_a = _make_key(home_a, "batch-a")
    fp_b = _make_key(home_b, "batch-b")
    fp_rsa = _make_key(home_rsa, "batch-rsa", rsa=True)
    _pin_key(tree, home_a, fp_a)
    _set_pin(fp_a)
    acc: list[bool] = []

    dest = _commit_batch(tree, home_a, _statement(tree, [_A, _B], corrupt=_A), "kb-hash")
    errs = sidecar_errors(tree)
    a1 = _needles(errs, _A)
    _check(any("sha256 mismatch" in item or "batch sha256" in item for item in a1), "batch correct signature one sha changed", a1[:1], acc)
    _drop(tree, dest)

    dest = _commit_batch(tree, home_b, _statement(tree, [_A, _B]), "kb-wrong-key")
    errs = sidecar_errors(tree)
    blob = " ".join(errs)
    good = bool(_needles(errs, _A)) and bool(_needles(errs, _B)) and (
        "No public key" in blob or "pinned key" in blob or "trusted allowlist" in blob or "gpg decrypt failed" in blob
    )
    _check(good, "batch signed by another key", f"A={bool(_needles(errs, _A))} B={bool(_needles(errs, _B))}", acc)
    _drop(tree, dest)

    dest = _commit_batch(tree, home_a, _statement(tree, [_A]), "kb-missing")
    errs = sidecar_errors(tree)
    _check(any("missing sidecar" in item for item in _needles(errs, _C)), "ADR missing from batch and no sidecar", _needles(errs, _C)[:1], acc)
    dest4 = dest
    raw = dest4.read_text(encoding="utf-8")
    tampered = raw
    if "sha256:" in raw:
        idx = raw.index("sha256:") + 7
        hexpart = raw[idx : idx + 64]
        flip = ("0" * 64) if hexpart[0] != "0" else ("f" * 64)
        tampered = raw[:idx] + flip + raw[idx + 64 :]
    dest4.write_text(tampered, encoding="utf-8")
    _run(["git", "add", "-A"], cwd=tree)
    _run(["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", "tamper"], cwd=tree)
    errs = sidecar_errors(tree)
    blob = " ".join(errs)
    good = (
        "gpg decrypt failed" in blob
        or "BADSIG" in blob
        or "signature" in blob.lower()
        or "GOODSIG" in blob
        or "no VALIDSIG" in blob
        or "gpg status missing" in blob
    )
    _check(good, "tampered batch body signature invalid", errs[:1], acc)
    _drop(tree, dest4)

    dest = _commit_batch(tree, home_a, _statement(tree, [_P46]), "kb-proposed")
    errs = sidecar_errors(tree)
    blob = " ".join(errs)
    _check("0046" in blob and ("Accepted" in blob or "Proposed" in blob or "invalid" in blob.lower()), "batch listing Proposed 0046", errs[:2], acc)
    _drop(tree, dest)

    dest = _commit_batch(tree, home_a, _statement(tree, [_S47]), "kb-superseded")
    errs = sidecar_errors(tree)
    blob = " ".join(errs)
    _check("0047" in blob and ("Accepted" in blob or "Superseded" in blob or "invalid" in blob.lower()), "batch listing Superseded 0047", errs[:2], acc)
    _drop(tree, dest)

    for shown, label in (
        (f"../{_A}", "../adrs/"),
        (f"./{_A}", "./adrs/"),
        (f"/{_A}", "/adrs/"),
        ("docs/TERMS.md", "docs/TERMS.md"),
    ):
        dest = _commit_batch(tree, home_a, _statement(tree, [_A], written=[shown]), label.replace("/", "-"))
        errs = sidecar_errors(tree)
        blob = " ".join(errs)
        _check("invalid batch path" in blob and shown in blob, f"batch path {label}", errs[:1], acc)
        _drop(tree, dest)

    dest = _commit_batch(tree, home_a, _statement(tree, [_A], repo="wrong/repo"), "kb-repo")
    errs = sidecar_errors(tree)
    _check("Repo" in " ".join(errs), "wrong Repo", errs[:1], acc)
    _drop(tree, dest)

    dest = _commit_batch(tree, home_a, _statement(tree, [_A], include_count=False), "kb-no-count")
    errs = sidecar_errors(tree)
    _check("missing Count" in " ".join(errs), "missing Count", errs[:1], acc)
    _drop(tree, dest)

    dest = _commit_batch(tree, home_a, _statement(tree, [_A], count="99"), "kb-wrong-count")
    errs = sidecar_errors(tree)
    _check("Count" in " ".join(errs) and "99" in " ".join(errs), "wrong Count", errs[:1], acc)
    _drop(tree, dest)

    dest = _commit_batch(tree, home_a, _statement(tree, [_A]), "kb-sidecar")
    sidecar_dest = tree / "adrs" / "0001-zero-variance-integrity.approval.asc"
    shutil.copy(ROOT / "tools/fixtures/owner-ratification-sidecar/wrong-key.approval.asc", sidecar_dest)
    _run(["git", "add", "-A"], cwd=tree)
    _run(["git", "-c", "user.email=kb@example.invalid", "-c", "user.name=kb", "commit", "-m", "bad-sidecar"], cwd=tree)
    errs = sidecar_errors(tree)
    a_errs = _needles(errs, _A)
    good = bool(a_errs) and not any("missing sidecar" in item for item in a_errs)
    _check(good, "invalid own sidecar next to a valid batch", a_errs[:1], acc)
    sidecar_dest.unlink()
    _drop(tree, dest)

    _set_pin(_PIN)
    _pin_key(tree, home_rsa, fp_rsa)
    dest = _commit_batch(tree, home_rsa, _statement(tree, [_A]), "kb-rsa")
    errs = sidecar_errors(tree)
    blob = " ".join(errs)
    good = (
        "Ed25519" in blob
        or "pinned key" in blob
        or "trusted allowlist" in blob
        or "No public key" in blob
        or "gpg decrypt failed" in blob
    )
    _check(good, "RSA-only trusted key with the pin absent", errs[:2], acc)
    _drop(tree, dest)
    _set_pin(fp_a)

    fixture = ROOT / "tools/fixtures/owner-ratification-sidecar/accepted-doc-no-sidecar.md"
    miss = verify_sidecar_p1(ROOT, fixture.relative_to(ROOT).as_posix())
    good5 = any("missing sidecar" in item for item in miss)
    wrong = ROOT / "tools/fixtures/owner-ratification-sidecar/wrong-key.approval.asc"
    stub = "tools/fixtures/owner-ratification-sidecar/stub-doc.md"
    wrong_errs = osc.verify_sidecar_p1_on_bytes(
        ROOT, document_rel=stub, document_bytes=(ROOT / stub).read_bytes(), asc_path=wrong, status="Accepted"
    )
    good6 = any("No public key" in item or "gpg" in item.lower() for item in wrong_errs)
    _check(good5 and good6, "existing sidecar rejections", f"missing={good5} wrong-key={good6}", acc)

    shutil.rmtree(tree.parent, ignore_errors=True)
    _set_pin(_PIN)
    return 0 if all(acc) else 1


if __name__ == "__main__":
    raise SystemExit(main())
