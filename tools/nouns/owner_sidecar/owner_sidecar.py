"""OpenPGP owner approval sidecar verification (ADR 0052)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

REPO_SLUG = "Zygotic-AI/Natural-Language-Coding"
OWNER_KEY_REL = "integrity/owner-keys/richard-pickett.asc"
TRUSTED_REL = "integrity/owner-keys/TRUSTED_FINGERPRINTS"
_FIELD = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def content_hash(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def normalize_fingerprint(fp: str) -> str:
    return re.sub(r"\s+", "", fp).upper()


def load_trusted_fingerprints(root: Path) -> tuple[set[str], list[str]]:
    path = root / TRUSTED_REL
    if not path.is_file():
        return set(), [f"missing {TRUSTED_REL}"]
    fps: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fps.add(normalize_fingerprint(line))
    if not fps:
        return set(), [f"empty trusted fingerprints in {TRUSTED_REL}"]
    return fps, []


def parse_signed_statement(asc_text: str) -> tuple[dict[str, str], list[str]]:
    if "-----BEGIN PGP SIGNED MESSAGE-----" not in asc_text:
        return {}, ["sidecar is not a PGP clearsigned message"]
    body = asc_text.split("-----BEGIN PGP SIGNATURE-----", 1)[0]
    body = body.split("-----BEGIN PGP SIGNED MESSAGE-----", 1)[-1]
    body = body.replace("\r\n", "\n")
    if body.startswith("\nHash:"):
        body = body.split("\n", 2)[-1] if body.count("\n") >= 2 else body
    elif body.startswith("Hash:"):
        body = body.split("\n", 1)[-1]
    body = body.lstrip("\n")
    if body.startswith("Hash:"):
        body = body.split("\n", 1)[-1].lstrip("\n")
    fields: dict[str, str] = {}
    for line in body.splitlines():
        match = _FIELD.match(line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    required = ["Repo", "Document", "Content-SHA256", "Decision", "Date", "Summary"]
    errors = [f"sidecar statement missing field {name}" for name in required if name not in fields]
    return fields, errors


def gpg_verify_clearsigned(root: Path, asc_path: Path) -> tuple[str | None, list[str]]:
    key_path = root / OWNER_KEY_REL
    if not key_path.is_file():
        return None, [f"missing {OWNER_KEY_REL}"]
    trusted, terr = load_trusted_fingerprints(root)
    if terr:
        return None, terr
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "gnupg"
        home.mkdir()
        env = {"GNUPGHOME": str(home), "LANG": "C"}
        imp = subprocess.run(
            ["gpg", "--batch", "--import", str(key_path)],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        if imp.returncode != 0:
            return None, [f"gpg import failed: {(imp.stderr or imp.stdout).strip()}"]
        ver = subprocess.run(
            ["gpg", "--verify", str(asc_path)],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        out = (ver.stderr or "") + (ver.stdout or "")
        if "Good signature" not in out:
            return None, [f"gpg verify failed: {out.strip() or 'no output'}"]
        fp_match = re.search(
            r"Primary key fingerprint:\s*([0-9A-Fa-f\s]+)", out
        ) or re.search(r"using EDDSA key ([0-9A-Fa-f]+)", out)
        if not fp_match:
            return None, ["gpg verify did not report signing key fingerprint"]
        fp = normalize_fingerprint(fp_match.group(1))
        if fp not in trusted:
            return None, [f"signing fingerprint {fp} not in {TRUSTED_REL}"]
        return fp, []


def verify_sidecar_p1(root: Path, document_rel: str) -> list[str]:
    """Return violations; empty list means MET for P1 on document_rel."""
    doc_rel = document_rel.replace("\\", "/").lstrip("./")
    doc_path = root / doc_rel
    asc_path = root / f"{doc_rel}.approval.asc"
    errors: list[str] = []
    if not doc_path.is_file():
        return [f"{doc_rel}: document missing"]
    if not asc_path.is_file():
        return [f"{doc_rel}: missing sidecar {doc_rel}.approval.asc"]
    asc_text = asc_path.read_text(encoding="utf-8")
    fields, parse_errors = parse_signed_statement(asc_text)
    errors.extend(parse_errors)
    fp, gpg_errors = gpg_verify_clearsigned(root, asc_path)
    errors.extend(gpg_errors)
    if errors:
        return errors
    doc_bytes = doc_path.read_bytes()
    actual_hash = content_hash(doc_bytes)
    if fields.get("Content-SHA256") != actual_hash:
        errors.append(
            f"{doc_rel}: Content-SHA256 mismatch (statement {fields.get('Content-SHA256')} vs file {actual_hash})"
        )
    status = _read_status_line(doc_path)
    if status and fields.get("Decision") != status:
        errors.append(
            f"{doc_rel}: Decision {fields.get('Decision')!r} != document Status {status!r}"
        )
    if fields.get("Repo") != REPO_SLUG:
        errors.append(f"{doc_rel}: Repo must be {REPO_SLUG!r}")
    if fields.get("Document") != doc_rel:
        errors.append(f"{doc_rel}: Document field must be {doc_rel!r}")
    return errors


def _read_status_line(doc_path: Path) -> str | None:
    for line in doc_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- Status:"):
            return line.split(":", 1)[1].strip()
    return None



def statement_field_errors(
    fields: dict[str, str],
    *,
    document_rel: str,
    document_bytes: bytes,
    status: str,
) -> list[str]:
    """P1 field checks (b)-(e) without gpg; for known-bad fixtures."""
    errors: list[str] = []
    doc_rel = document_rel.replace("\\", "/").lstrip("./")
    actual_hash = content_hash(document_bytes)
    if fields.get("Content-SHA256") != actual_hash:
        errors.append("Content-SHA256 mismatch")
    if fields.get("Decision") != status:
        errors.append("Decision mismatch")
    if fields.get("Repo") != REPO_SLUG:
        errors.append("Repo mismatch")
    if fields.get("Document") != doc_rel:
        errors.append("Document mismatch")
    return errors

def verify_sidecar_p1_on_bytes(
    root: Path,
    *,
    document_rel: str,
    document_bytes: bytes,
    asc_path: Path,
    status: str,
) -> list[str]:
    """P1 verify with explicit document bytes (known-bad fixtures)."""
    errors: list[str] = []
    if not asc_path.is_file():
        return ["missing sidecar"]
    asc_text = asc_path.read_text(encoding="utf-8")
    fields, parse_errors = parse_signed_statement(asc_text)
    errors.extend(parse_errors)
    _, gpg_errors = gpg_verify_clearsigned(root, asc_path)
    errors.extend(gpg_errors)
    if parse_errors or gpg_errors:
        return errors
    actual_hash = content_hash(document_bytes)
    if fields.get("Content-SHA256") != actual_hash:
        errors.append("Content-SHA256 mismatch")
    if fields.get("Decision") != status:
        errors.append("Decision mismatch")
    if fields.get("Repo") != REPO_SLUG:
        errors.append("Repo mismatch")
    if fields.get("Document") != document_rel.replace("\\", "/").lstrip("./"):
        errors.append("Document mismatch")
    return errors
