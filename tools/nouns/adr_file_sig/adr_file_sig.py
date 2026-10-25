"""Per-file detached owner signatures for numbered ADRs (ADR 0056).

Sibling convention: adrs/NNNN-slug.md -> adrs/NNNN-slug.md.asc
The signature is gpg --detach-sign --armor over the exact current file bytes.
Batch owner-approvals statements do not cover an ADR.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import subprocess
import tempfile
from pathlib import Path

from nouns.owner_sidecar import owner_sidecar as osc

# Pinned owner Ed25519 key. Tests may rebind this name on a scratch tree.
PINNED_OWNER_FINGERPRINT = "9D1BD57770FC3A1DE84702750AFD22B063AE01BC"
_ADR_FILE = re.compile(r"^(\d{4})-.+\.md$")


def detached_sig_rel(document_rel: str) -> str:
    """Repo convention: adrs/foo.md -> adrs/foo.md.asc."""
    rel = document_rel.replace("\\", "/").lstrip("./")
    return rel + ".asc"


def numbered_adr_rel(document_rel: str) -> bool:
    rel = document_rel.replace("\\", "/").lstrip("./")
    return rel.startswith("adrs/") and bool(_ADR_FILE.match(Path(rel).name))


def _parse_validsigs(status_lines: str) -> tuple[set[str], list[str]]:
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
            validsigs.add(osc.normalize_fingerprint(parts[-1]))
    if goodsigs < 1:
        errors.append("gpg status missing GOODSIG")
    if not validsigs:
        errors.append("gpg status missing VALIDSIG")
    return validsigs, errors


def gpg_verify_detached(
    sig_path: Path,
    document_path: Path,
    *,
    required_fingerprint: str,
    key_import_paths: list[Path],
) -> tuple[str | None, list[str]]:
    """Verify a detached signature over document_path bytes. Returns (signer, errors)."""
    pin = osc.normalize_fingerprint(required_fingerprint)
    if not pin:
        return None, ["empty required fingerprint"]
    if not key_import_paths:
        return None, ["no key material provided for gpg import"]
    if not sig_path.is_file():
        return None, [f"missing detached signature {sig_path.name}"]
    if not document_path.is_file():
        return None, ["document missing"]
    errors: list[str] = []
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
                errors.append(
                    f"gpg import failed for {key_path}: {(imp.stderr or imp.stdout).strip()}"
                )
        if errors:
            return None, errors
        verify = subprocess.run(
            [
                "gpg",
                "--batch",
                "--verify",
                "--status-fd",
                "2",
                str(sig_path),
                str(document_path),
            ],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        status_text = verify.stderr or ""
        if verify.returncode != 0:
            return None, [f"gpg verify failed: {(verify.stderr or verify.stdout).strip()}"]
        validsigs, status_errors = _parse_validsigs(status_text)
        errors.extend(status_errors)
        if errors:
            return None, errors
        if pin not in validsigs:
            return (
                None,
                [
                    "detached signature not by pinned key "
                    f"(saw {sorted(validsigs)}, pinned {pin})"
                ],
            )
        return pin, []


def verify_adr_detached_signature(root: Path, document_rel: str) -> list[str]:
    """NOT_MET unless a valid per-file detached signature by the pinned key covers current bytes."""
    doc_rel = document_rel.replace("\\", "/").lstrip("./")
    doc_path = root / doc_rel
    sig_rel = detached_sig_rel(doc_rel)
    sig_path = root / sig_rel
    if not doc_path.is_file():
        return [f"{doc_rel}: document missing"]
    status_errors = osc.document_status_errors(doc_rel, doc_path)
    if status_errors:
        return status_errors
    if not sig_path.is_file():
        return [f"{doc_rel}: missing detached signature {sig_rel}"]
    key_path = root / osc.OWNER_KEY_REL
    signer, errors = gpg_verify_detached(
        sig_path,
        doc_path,
        required_fingerprint=PINNED_OWNER_FINGERPRINT,
        key_import_paths=[key_path],
    )
    if errors:
        return [f"{doc_rel}: {item}" for item in errors]
    if signer != osc.normalize_fingerprint(PINNED_OWNER_FINGERPRINT):
        return [f"{doc_rel}: detached signature not by pinned key"]
    return []
