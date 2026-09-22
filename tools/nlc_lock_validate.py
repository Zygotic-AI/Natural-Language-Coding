"""ADR 0015: compiled-system .nlc/lock.json shape."""

from __future__ import annotations

from typing import Any

from nlc_distribution import LOCK_SCHEMA, normalize_version


def validate_lock(data: dict[str, Any]) -> tuple[bool, str]:
    if int(data.get("schema", 0)) != LOCK_SCHEMA:
        return False, f"lock schema must be {LOCK_SCHEMA}"
    hub = str(data.get("hub", "")).strip()
    if not hub:
        return False, "lock field hub missing"
    try:
        normalize_version(hub)
    except ValueError:
        return False, f"lock hub not semver: {hub}"
    store = str(data.get("store", "user"))
    if store not in {"user", "path"}:
        return False, f"lock store invalid: {store}"
    if store == "path" and not str(data.get("store_path", "")).strip():
        return False, "lock store=path requires store_path"
    return True, "lock valid"
