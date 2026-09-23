"""GateLedger noun: gate-scope list + gate-record receipts (ADR 0010)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

BOUNDARY = "bba-emit"

SCOPE_FILE = "gate-scope.json"
VALID_OUTCOMES = {"PASS", "FAIL", "WAIVED"}


class GateLedger:
    """Owns .nlc/gate-scope.json and .nlc/gate-records.json mutations."""

    def normalize_rel(self, artifact: str) -> str:
        rel = artifact.replace("\\", "/").strip()
        if rel.startswith("./"):
            rel = rel[2:]
        return rel

    def load_scope_paths(self, root: Path) -> list[str]:
        path = root / ".nlc" / SCOPE_FILE
        if not path.is_file():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        raw = data.get("artifacts") or []
        out: list[str] = []
        for item in raw:
            rel = self.normalize_rel(str(item))
            if rel:
                out.append(rel)
        return sorted(set(out))

    def add_scope_path(self, root: Path, artifact: str) -> None:
        rel = self.normalize_rel(artifact)
        if not rel:
            raise ValueError("artifact path is required")
        nlc = root / ".nlc"
        nlc.mkdir(parents=True, exist_ok=True)
        path = nlc / SCOPE_FILE
        paths = self.load_scope_paths(root)
        if rel not in paths:
            paths.append(rel)
            paths.sort()
        path.write_text(
            json.dumps({"schema": 1, "artifacts": paths}, indent=2) + "\n",
            encoding="utf-8",
        )

    def scoped_artifact_paths(self, root: Path) -> list[Path]:
        from nlc_pipeline import is_hub_repo

        if is_hub_repo(root):
            return []
        out: list[Path] = []
        for rel in self.load_scope_paths(root):
            candidate = root / rel
            if candidate.is_file():
                out.append(candidate)
        return out

    def append_record(
        self,
        root: Path,
        *,
        artifact: str,
        gate_id: str,
        outcome: str,
        command: str | None = None,
    ) -> None:
        if outcome not in VALID_OUTCOMES:
            raise ValueError(f"outcome must be one of {VALID_OUTCOMES}")
        rel = self.normalize_rel(artifact)
        nlc = root / ".nlc"
        nlc.mkdir(parents=True, exist_ok=True)
        path = nlc / "gate-records.json"
        records: list[dict] = []
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                records = list(data.get("records") or [])
            except json.JSONDecodeError:
                records = []
        records.append(
            {
                "artifact": rel,
                "gate_id": gate_id,
                "outcome": outcome,
                "command": command or "",
                "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )
        path.write_text(
            json.dumps({"schema": 1, "records": records}, indent=2) + "\n",
            encoding="utf-8",
        )
        self.add_scope_path(root, rel)


_DEFAULT = GateLedger()


def add_scope_path(root: Path, artifact: str) -> None:
    _DEFAULT.add_scope_path(root, artifact)


def load_scope_paths(root: Path) -> list[str]:
    return _DEFAULT.load_scope_paths(root)


def scoped_artifact_paths(root: Path) -> list[Path]:
    return _DEFAULT.scoped_artifact_paths(root)


def append_record(
    root: Path,
    *,
    artifact: str,
    gate_id: str,
    outcome: str,
    command: str | None = None,
) -> None:
    _DEFAULT.append_record(
        root, artifact=artifact, gate_id=gate_id, outcome=outcome, command=command
    )

