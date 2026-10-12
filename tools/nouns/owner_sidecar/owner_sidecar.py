"""OpenPGP owner approval sidecar verification (ADR 0052)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import re
import subprocess
import tempfile
from pathlib import Path

REPO_SLUG = "Zygotic-AI/Natural-Language-Coding"
OWNER_KEY_REL = "integrity/owner-keys/richard-pickett.asc"
TRUSTED_REL = "integrity/owner-keys/TRUSTED_FINGERPRINTS"
_FIELD = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
_REQUIRED_FIELDS = ("Repo", "Document", "Content-SHA256", "Decision", "Date", "Summary")
_KNOWN_DOCUMENT_STATUS = frozenset({"Accepted", "Proposed", "Superseded", "Rejected", "Deprecated"})


def content_hash(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def normalize_fingerprint(fp: str) -> str:
    return re.sub(r"\s+", "", fp).upper()


def load_trusted_fingerprints_from_text(text: str) -> tuple[set[str], list[str]]:
    fps: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fps.add(normalize_fingerprint(line))
    if not fps:
        return set(), ["empty trusted fingerprint allowlist"]
    return fps, []


def load_trusted_fingerprints(root: Path) -> tuple[set[str], list[str]]:
    path = root / TRUSTED_REL
    if not path.is_file():
        return set(), [f"missing {TRUSTED_REL}"]
    return load_trusted_fingerprints_from_text(path.read_text(encoding="utf-8"))


def parse_statement_plaintext(plaintext: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    fields: dict[str, str] = {}
    for line in plaintext.replace("\r\n", "\n").splitlines():
        match = _FIELD.match(line)
        if not match:
            continue
        name, value = match.group(1), match.group(2).strip()
        if name in fields:
            errors.append(f"duplicate statement field {name!r}")
            continue
        fields[name] = value
    for name in _REQUIRED_FIELDS:
        if name not in fields:
            errors.append(f"sidecar statement missing field {name}")
    return fields, errors


def _parse_gpg_status(status_lines: str) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    goodsigs = 0
    validsigs: set[str] = set()
    for raw in status_lines.splitlines():
        if not raw.startswith("[GNUPG:] "):
            continue
        parts = raw[9:].split(" ")
        tag = parts[0]
        if tag == "GOODSIG" and len(parts) >= 3:
            goodsigs += 1
        if tag == "VALIDSIG" and len(parts) >= 10:
            validsigs.add(normalize_fingerprint(parts[-1]))
    if goodsigs < 1:
        errors.append("gpg status missing GOODSIG")
    if not validsigs:
        errors.append("gpg status missing VALIDSIG")
    return validsigs, errors


def gpg_verify_clearsigned(
    asc_path: Path,
    *,
    trusted_fingerprints: set[str],
    key_import_paths: list[Path],
) -> tuple[str | None, dict[str, str], list[str]]:
    errors: list[str] = []
    if not trusted_fingerprints:
        return None, {}, ["empty trusted fingerprint set"]
    if not key_import_paths:
        return None, {}, ["no key material provided for gpg import"]
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "gnupg"
        home.mkdir()
        env = {"GNUPGHOME": str(home), "LANG": "C"}
        for key_path in key_import_paths:
            if not key_path.is_file():
                errors.append(f"missing key import path {key_path}")
                continue
            imp = subprocess.run(
                ["gpg", "--batch", "--import", str(key_path)],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )
            if imp.returncode != 0:
                errors.append(f"gpg import failed for {key_path}: {(imp.stderr or imp.stdout).strip()}")
        if errors:
            return None, {}, errors
        decrypt = subprocess.run(
            ["gpg", "--batch", "--decrypt", "--status-fd", "2", str(asc_path)],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        status_text = decrypt.stderr or ""
        if decrypt.returncode != 0:
            return None, {}, [f"gpg decrypt failed: {(decrypt.stderr or decrypt.stdout).strip()}"]
        validsigs, status_errors = _parse_gpg_status(status_text)
        errors.extend(status_errors)
        if errors:
            return None, {}, errors
        trusted_valid = {fp for fp in validsigs if fp in trusted_fingerprints}
        if not trusted_valid:
            return (
                None,
                {},
                [
                    "no VALIDSIG primary fingerprint in trusted allowlist "
                    f"(saw {sorted(validsigs)}, trusted {sorted(trusted_fingerprints)})"
                ],
            )
        if len(trusted_valid) > 1:
            errors.append("multiple trusted VALIDSIG primary fingerprints")
        signer_fp = sorted(trusted_valid)[0]
        fields, parse_errors = parse_statement_plaintext(decrypt.stdout or "")
        errors.extend(parse_errors)
        if errors:
            return signer_fp, fields, errors
        return signer_fp, fields, []


def gpg_verify_clearsigned_in_repo(root: Path, asc_path: Path) -> tuple[str | None, dict[str, str], list[str]]:
    trusted, terr = load_trusted_fingerprints(root)
    if terr:
        return None, {}, terr
    key_path = root / OWNER_KEY_REL
    return gpg_verify_clearsigned(
        asc_path, trusted_fingerprints=trusted, key_import_paths=[key_path]
    )


def _read_status_line(doc_path: Path) -> str | None:
    for line in doc_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- Status:"):
            return line.split(":", 1)[1].strip()
    return None


def _document_requires_status_line(document_rel: str) -> bool:
    rel = document_rel.replace("\\", "/").lstrip("./")
    return rel.startswith("adrs/") and rel.endswith(".md")


def _status_line_errors(doc_path: Path, document_rel: str) -> list[str]:
    if not _document_requires_status_line(document_rel):
        return []
    status = _read_status_line(doc_path)
    if status is None:
        return [f"{document_rel}: missing Status line"]
    if status not in _KNOWN_DOCUMENT_STATUS:
        return [f"{document_rel}: unknown Status {status!r}"]
    return []


def verify_sidecar_p1_fields(
    *,
    document_rel: str,
    document_bytes: bytes,
    fields: dict[str, str],
    require_status_line: bool,
    doc_path: Path | None,
) -> list[str]:
    errors: list[str] = []
    doc_rel = document_rel.replace("\\", "/").lstrip("./")
    actual_hash = content_hash(document_bytes)
    if fields.get("Content-SHA256") != actual_hash:
        errors.append(
            f"{doc_rel}: Content-SHA256 mismatch (statement {fields.get('Content-SHA256')} vs file {actual_hash})"
        )
    if fields.get("Repo") != REPO_SLUG:
        errors.append(f"{doc_rel}: Repo must be {REPO_SLUG!r}")
    if fields.get("Document") != doc_rel:
        errors.append(f"{doc_rel}: Document field must be {doc_rel!r}")
    if require_status_line and doc_path is not None:
        errors.extend(_status_line_errors(doc_path, doc_rel))
        status = _read_status_line(doc_path)
        if status is not None and fields.get("Decision") != status:
            errors.append(
                f"{doc_rel}: Decision {fields.get('Decision')!r} != document Status {status!r}"
            )
    return errors



def sidecar_path_for_document(document_rel: str) -> str:
    """Repo convention: adrs/foo.md -> adrs/foo.approval.asc (see ADR 0052 example)."""
    rel = document_rel.replace("\\", "/").lstrip("./")
    if rel.endswith(".md"):
        return rel[:-3] + ".approval.asc"
    return rel + ".approval.asc"


def verify_sidecar_p1(root: Path, document_rel: str) -> list[str]:
    doc_rel = document_rel.replace("\\", "/").lstrip("./")
    doc_path = root / doc_rel
    asc_path = root / sidecar_path_for_document(doc_rel)
    if not doc_path.is_file():
        return [f"{doc_rel}: document missing"]
    if not asc_path.is_file():
        return [f"{doc_rel}: missing sidecar {doc_rel}.approval.asc"]
    require_status = _document_requires_status_line(doc_rel)
    if require_status:
        status_errors = _status_line_errors(doc_path, doc_rel)
        if status_errors:
            return status_errors
    _, fields, errors = gpg_verify_clearsigned_in_repo(root, asc_path)
    if errors:
        return [f"{doc_rel}: {item}" for item in errors]
    errors.extend(
        verify_sidecar_p1_fields(
            document_rel=doc_rel,
            document_bytes=doc_path.read_bytes(),
            fields=fields,
            require_status_line=require_status,
            doc_path=doc_path,
        )
    )
    return errors


def verify_sidecar_with_trusted_set(
    root: Path,
    document_rel: str,
    asc_path: Path,
    *,
    trusted_fingerprints: set[str],
    key_import_paths: list[Path],
    document_bytes: bytes | None = None,
) -> list[str]:
    doc_rel = document_rel.replace("\\", "/").lstrip("./")
    doc_path = root / doc_rel
    if document_bytes is None:
        if not doc_path.is_file():
            return [f"{doc_rel}: document missing"]
        document_bytes = doc_path.read_bytes()
    if not asc_path.is_file():
        return [f"{doc_rel}: missing sidecar"]
    require_status = _document_requires_status_line(doc_rel)
    if require_status and doc_path.is_file():
        status_errors = _status_line_errors(doc_path, doc_rel)
        if status_errors:
            return status_errors
    _, fields, errors = gpg_verify_clearsigned(
        asc_path,
        trusted_fingerprints=trusted_fingerprints,
        key_import_paths=key_import_paths,
    )
    if errors:
        return [f"{doc_rel}: {item}" for item in errors]
    errors.extend(
        verify_sidecar_p1_fields(
            document_rel=doc_rel,
            document_bytes=document_bytes,
            fields=fields,
            require_status_line=require_status,
            doc_path=doc_path if doc_path.is_file() else None,
        )
    )
    return errors


def statement_field_errors(
    fields: dict[str, str],
    *,
    document_rel: str,
    document_bytes: bytes,
    status: str,
) -> list[str]:
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
    _, fields, errors = gpg_verify_clearsigned_in_repo(root, asc_path)
    if errors:
        return errors
    errors.extend(
        verify_sidecar_p1_fields(
            document_rel=document_rel,
            document_bytes=document_bytes,
            fields=fields,
            require_status_line=True,
            doc_path=None,
        )
    )
    if fields.get("Decision") != status:
        errors.append("Decision mismatch")
    return errors
