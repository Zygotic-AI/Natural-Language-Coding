"""OpenPGP owner approval sidecar verification (ADR 0052)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import re
import subprocess
import tempfile
from pathlib import Path
from typing import NamedTuple

REPO_SLUG = "Zygotic-AI/Natural-Language-Coding"
OWNER_KEY_REL = "integrity/owner-keys/richard-pickett.asc"
TRUSTED_REL = "integrity/owner-keys/TRUSTED_FINGERPRINTS"
_FIELD = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
_REQUIRED_FIELDS = ("Repo", "Document", "Content-SHA256", "Decision", "Date", "Summary")
OWNER_BATCH_FINGERPRINT = "9D1BD57770FC3A1DE84702750AFD22B063AE01BC"
BATCH_DIR_REL = "adrs/owner-approvals"
_BATCH_LINE = re.compile(r"^(\S+)\s+sha256:([0-9a-fA-F]{64})\s*$")
_EXACT_BATCH_ADR = re.compile(r"^adrs/[0-9]{4}-[^/]+\.md$")
_EDDSA_PUBKEY_ALGO = "22"
_CLEARSIGN_BODY = re.compile(
    r"-----BEGIN PGP SIGNED MESSAGE-----\r?\n(?:Hash:[^\n]*\n)?\r?\n(.*)\r?\n-----BEGIN PGP SIGNATURE-----",
    re.DOTALL,
)
_KNOWN_DOCUMENT_STATUS = frozenset({"Accepted", "Proposed", "Superseded", "Rejected", "Deprecated"})
_KNOWN_STATUS_FOLD = {item.lower(): item for item in _KNOWN_DOCUMENT_STATUS}
_PENDING_DECISIONS = frozenset({"Pending", "Proposed"})
_ADR_FILE = re.compile(r"^(\d{4})-.+\.md$")
_INLINE_STATUS = re.compile(
    r"^-?\s*(?:\*\*)?Status(?:\*\*)?:\s*(?:\*\*)?\s*(.+)$",
    re.IGNORECASE,
)
_HEADING_STATUS = re.compile(r"^#{2,3}\s+Status\s*$", re.IGNORECASE)
_STOP_HEADING = re.compile(r"^#{2,3}\s+(Decision|Context)\b", re.IGNORECASE)
_EMPHASIS = re.compile(r"(\*\*|__|\*|_)")


class StatusParse(NamedTuple):
    """First header Status marker, or empty when the header has none."""

    normalized: str | None
    raw_line: str | None
    raw_value: str | None
    marker_present: bool


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


def gpg_verify_clearsigned_plaintext(
    asc_path: Path,
    *,
    trusted_fingerprints: set[str],
    key_import_paths: list[Path],
) -> tuple[str | None, str, list[str]]:
    """Verify a clearsignature. Returns (signer, plaintext, errors). No sidecar-field parse."""
    errors: list[str] = []
    if not trusted_fingerprints:
        return None, "", ["empty trusted fingerprint set"]
    if not key_import_paths:
        return None, "", ["no key material provided for gpg import"]
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
            return None, "", errors
        decrypt = subprocess.run(
            ["gpg", "--batch", "--decrypt", "--status-fd", "2", str(asc_path)],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        status_text = decrypt.stderr or ""
        plaintext = decrypt.stdout or ""
        if decrypt.returncode != 0:
            return None, plaintext, [f"gpg decrypt failed: {(decrypt.stderr or decrypt.stdout).strip()}"]
        validsigs, status_errors = _parse_gpg_status(status_text)
        errors.extend(status_errors)
        if errors:
            return None, plaintext, errors
        trusted_valid = {fp for fp in validsigs if fp in trusted_fingerprints}
        if not trusted_valid:
            return (
                None,
                plaintext,
                [
                    "no VALIDSIG primary fingerprint in trusted allowlist "
                    f"(saw {sorted(validsigs)}, trusted {sorted(trusted_fingerprints)})"
                ],
            )
        if len(trusted_valid) > 1:
            errors.append("multiple trusted VALIDSIG primary fingerprints")
        signer_fp = sorted(trusted_valid)[0]
        if errors:
            return signer_fp, plaintext, errors
        return signer_fp, plaintext, []


def gpg_verify_clearsigned(
    asc_path: Path,
    *,
    trusted_fingerprints: set[str],
    key_import_paths: list[Path],
) -> tuple[str | None, dict[str, str], list[str]]:
    signer_fp, plaintext, errors = gpg_verify_clearsigned_plaintext(
        asc_path, trusted_fingerprints=trusted_fingerprints, key_import_paths=key_import_paths
    )
    if errors:
        return signer_fp, {}, errors
    fields, parse_errors = parse_statement_plaintext(plaintext)
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


def _normalize_status_token(raw: str) -> str | None:
    """Strip emphasis and trailing punctuation; first word → known Status spelling."""
    text = _EMPHASIS.sub("", raw).strip()
    text = text.rstrip(".,;:!?…").strip()
    if not text:
        return None
    first = text.split()[0].rstrip(".,;:!?…")
    if not first:
        return None
    return _KNOWN_STATUS_FOLD.get(first.lower())


def parse_document_status(text: str) -> StatusParse:
    """First Status marker in the document header (before Decision/Context)."""
    lines = text.replace("\r\n", "\n").splitlines()
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if _STOP_HEADING.match(stripped):
            break
        if _HEADING_STATUS.match(stripped):
            value_line = None
            scan = index + 1
            while scan < len(lines):
                nxt = lines[scan].strip()
                if nxt:
                    value_line = lines[scan]
                    break
                scan += 1
            raw_value = value_line.strip() if value_line is not None else ""
            return StatusParse(
                normalized=_normalize_status_token(raw_value) if raw_value else None,
                raw_line=value_line if value_line is not None else lines[index],
                raw_value=raw_value or None,
                marker_present=True,
            )
        inline = _INLINE_STATUS.match(stripped)
        if inline:
            raw_value = inline.group(1).strip()
            return StatusParse(
                normalized=_normalize_status_token(raw_value),
                raw_line=lines[index],
                raw_value=raw_value,
                marker_present=True,
            )
        index += 1
    return StatusParse(normalized=None, raw_line=None, raw_value=None, marker_present=False)


def parse_document_status_path(doc_path: Path) -> StatusParse:
    return parse_document_status(doc_path.read_text(encoding="utf-8"))


def read_status_line(doc_path: Path) -> str | None:
    """Return the first header Status token (Accepted/Proposed/…), or None."""
    return parse_document_status_path(doc_path).normalized


def _document_requires_status_line(document_rel: str) -> bool:
    rel = document_rel.replace("\\", "/").lstrip("./")
    return rel.startswith("adrs/") and bool(_ADR_FILE.match(Path(rel).name))


def numbered_adr_rel(document_rel: str) -> bool:
    return _document_requires_status_line(document_rel)


def status_value_for_error(parsed: StatusParse) -> str:
    if parsed.raw_value is not None:
        return parsed.raw_value
    if parsed.raw_line is not None:
        return parsed.raw_line
    return ""


def document_status_errors(document_rel: str, doc_path: Path) -> list[str]:
    """Numbered ADRs must have a known Status. Missing/unknown → C6 NOT_MET."""
    rel = document_rel.replace("\\", "/").lstrip("./")
    if not numbered_adr_rel(rel):
        return []
    parsed = parse_document_status_path(doc_path)
    if parsed.normalized in _KNOWN_DOCUMENT_STATUS:
        return []
    value = status_value_for_error(parsed)
    return [f"{rel}: unparseable or unknown Status {value}"]


def non_adr_status_errors(document_rel: str, doc_path: Path) -> list[str]:
    """Unparseable non-ADR Status is a violation only when the raw marker mentions accept."""
    rel = document_rel.replace("\\", "/").lstrip("./")
    parsed = parse_document_status_path(doc_path)
    if not parsed.marker_present or parsed.normalized is not None:
        return []
    raw = parsed.raw_line or ""
    if "accept" not in raw.lower():
        return []
    value = status_value_for_error(parsed)
    return [f"{rel}: unparseable or unknown Status {value}"]


def _status_line_errors(doc_path: Path, document_rel: str) -> list[str]:
    return document_status_errors(document_rel, doc_path)


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
        status = read_status_line(doc_path)
        if status is not None and fields.get("Decision") != status:
            errors.append(
                f"{doc_rel}: Decision {fields.get('Decision')!r} != document Status {status!r}"
            )
        errors.extend(pending_presented_as_ratified_errors(status, fields, document_rel=doc_rel))
    else:
        errors.extend(
            pending_presented_as_ratified_errors(None, fields, document_rel=doc_rel)
        )
    return errors


def pending_presented_as_ratified_errors(
    status: str | None, fields: dict[str, str], *, document_rel: str = ""
) -> list[str]:
    """NOT_MET when a Pending/Proposed decision or Proposed document is presented as ratified."""
    errors: list[str] = []
    prefix = f"{document_rel}: " if document_rel else ""
    decision = fields.get("Decision")
    if decision in _PENDING_DECISIONS:
        errors.append(f"{prefix}pending Decision {decision!r} is not ratification")
    if status == "Proposed" and decision == "Accepted":
        errors.append(f"{prefix}Proposed document presented as ratified")
    return errors



def sidecar_path_for_document(document_rel: str) -> str:
    """Repo convention: adrs/foo.md -> adrs/foo.approval.asc (see ADR 0052 example)."""
    rel = document_rel.replace("\\", "/").lstrip("./")
    if rel.endswith(".md"):
        return rel[:-3] + ".approval.asc"
    return rel + ".approval.asc"


def _git_tracked_rels(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [line.strip().replace("\\", "/") for line in (proc.stdout or "").splitlines() if line.strip()]


def committed_batch_approval_rels(root: Path) -> list[str]:
    found: list[str] = []
    prefix = BATCH_DIR_REL.rstrip("/") + "/"
    for rel in _git_tracked_rels(root):
        if not rel.startswith(prefix):
            continue
        if rel.count("/") != 2:
            continue
        if rel.endswith(".approval.asc"):
            found.append(rel)
    return sorted(found)


def extract_clearsigned_body(text: str) -> str:
    match = _CLEARSIGN_BODY.search(text.replace("\r\n", "\n"))
    if not match:
        return ""
    return match.group(1)


def parse_batch_entries(plaintext: str) -> tuple[dict[str, str], list[str]]:
    """Parse `path sha256:hex` lines. Paths are kept exactly as written (no lstrip)."""
    entries: dict[str, str] = {}
    errors: list[str] = []
    for raw in plaintext.replace("\r\n", "\n").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = _BATCH_LINE.match(stripped)
        if not match:
            if _FIELD.match(stripped):
                continue
            errors.append(f"unparseable batch line {stripped!r}")
            continue
        path = match.group(1)
        digest = match.group(2).lower()
        if path in entries:
            errors.append(f"duplicate batch path {path}")
            continue
        entries[path] = digest
    return entries, errors


def parse_batch_headers(plaintext: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw in plaintext.replace("\r\n", "\n").splitlines():
        match = _FIELD.match(raw.strip())
        if not match:
            continue
        name, value = match.group(1), match.group(2).strip()
        if name not in fields:
            fields[name] = value
    return fields


def batch_header_errors(fields: dict[str, str], entry_count: int) -> list[str]:
    errors: list[str] = []
    if fields.get("Repo") != REPO_SLUG:
        errors.append(f"batch Repo must be {REPO_SLUG!r}")
    if fields.get("Decision") != "Accepted":
        errors.append("batch Decision must be 'Accepted'")
    if "Count" not in fields:
        errors.append("batch missing Count")
    elif fields["Count"] != str(entry_count):
        errors.append(f"batch Count {fields['Count']!r} != {entry_count}")
    return errors


def batch_allowed_fingerprints(_trusted: set[str] | None = None) -> set[str]:
    """Batch signatures accept only OWNER_BATCH_FINGERPRINT. No trusted-set fallback."""
    return {OWNER_BATCH_FINGERPRINT}


def openpgp_key_is_ed25519(key_path: Path) -> bool:
    """True when the public key packet is EdDSA (OpenPGP algo 22 / Ed25519)."""
    if not key_path.is_file():
        return False
    proc = subprocess.run(
        ["gpg", "--batch", "--show-keys", "--with-colons", str(key_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    for line in (proc.stdout or "").splitlines():
        parts = line.split(":")
        if parts and parts[0] == "pub" and len(parts) > 3 and parts[3] == _EDDSA_PUBKEY_ALGO:
            return True
    return False


def batch_entry_errors(root: Path, path: str) -> list[str]:
    """An entry is invalid when the path is not exactly adrs/NNNN-*.md, missing, or not Accepted."""
    if not _EXACT_BATCH_ADR.match(path):
        return [f"invalid batch path {path!r}"]
    doc = root / path
    if not doc.is_file():
        return [f"batch path does not exist {path}"]
    if read_status_line(doc) != "Accepted":
        return [f"batch entry {path} requires Status Accepted"]
    return []


def verify_batch_approval(root: Path, batch_rel: str) -> tuple[dict[str, str], list[str]]:
    """Verify one committed batch. Returns (entries, errors). Entries parsed even on sig fail."""
    rel = batch_rel.replace("\\", "/").lstrip("./")
    path = root / rel
    errors: list[str] = []
    entries: dict[str, str] = {}
    if not path.is_file():
        return {}, [f"{rel}: batch missing"]
    body = extract_clearsigned_body(path.read_text(encoding="utf-8", errors="replace"))
    parsed, perr = parse_batch_entries(body)
    entries.update(parsed)
    errors.extend(f"{rel}: {item}" for item in perr)
    errors.extend(f"{rel}: {item}" for item in batch_header_errors(parse_batch_headers(body), len(entries)))
    for entry_path in entries:
        errors.extend(f"{rel}: {item}" for item in batch_entry_errors(root, entry_path))
    key_path = root / OWNER_KEY_REL
    if not openpgp_key_is_ed25519(key_path):
        errors.append(f"{rel}: batch key is not Ed25519")
    pin = batch_allowed_fingerprints()
    signer, _plaintext, verr = gpg_verify_clearsigned_plaintext(
        path, trusted_fingerprints=pin, key_import_paths=[key_path]
    )
    if verr:
        return entries, [f"{rel}: {item}" for item in verr] + errors
    if signer is None or signer not in pin:
        return entries, [
            f"{rel}: batch not signed by pinned key {OWNER_BATCH_FINGERPRINT}"
        ] + errors
    return entries, errors


def committed_batch_file_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in committed_batch_approval_rels(root):
        _entries, berr = verify_batch_approval(root, rel)
        errors.extend(berr)
    return errors


def document_batch_result(root: Path, document_rel: str) -> tuple[bool, list[str]]:
    """Return (covered, errors). covered True only when a valid batch lists a matching Accepted hash."""
    doc_rel = document_rel.replace("\\", "/").lstrip("./")
    doc_path = root / doc_rel
    if not doc_path.is_file():
        return False, [f"{doc_rel}: document missing"]
    actual = content_hash(doc_path.read_bytes())
    status = read_status_line(doc_path)
    listed_errors: list[str] = []
    for batch_rel in committed_batch_approval_rels(root):
        entries, berr = verify_batch_approval(root, batch_rel)
        if doc_rel not in entries:
            continue
        if berr:
            listed_errors.append(f"{doc_rel}: listed in invalid batch {batch_rel}")
            listed_errors.extend(berr)
            continue
        if entries[doc_rel] != actual:
            listed_errors.append(
                f"{doc_rel}: batch sha256 mismatch (statement {entries[doc_rel]} vs file {actual})"
            )
            continue
        if status != "Accepted":
            listed_errors.append(f"{doc_rel}: batch entry requires Status Accepted")
            continue
        return True, []
    return False, listed_errors


def verify_owner_signed(root: Path, document_rel: str) -> list[str]:
    """Own sidecar, if present, is decisive: invalid sidecar is NOT_MET even when a batch covers."""
    doc_rel = document_rel.replace("\\", "/").lstrip("./")
    sidecar = root / sidecar_path_for_document(doc_rel)
    if sidecar.is_file():
        return verify_sidecar_p1(root, doc_rel)
    covered, batch_errs = document_batch_result(root, doc_rel)
    if covered:
        return []
    if batch_errs:
        return batch_errs
    return [f"{doc_rel}: missing sidecar {doc_rel}.approval.asc"]


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
