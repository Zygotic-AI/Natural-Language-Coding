"""RuleReceipt noun: private marker/IR policy; verbs are the only mutation path."""

from __future__ import annotations

import json
import re
from pathlib import Path

BOUNDARY = "bba-emit"

RULE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MARKER_RE = re.compile(r"(?:#|//)\s*nlc:rule=([A-Za-z0-9][A-Za-z0-9._-]*)")
SKIP_DIRS = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
SCAN_DIRS = ("goals", "domain", "adapters", "workflows")
SNAPSHOT = "rule-ir.snapshot.json"

_PREFIX = {
    "python": "# nlc:rule={id}",
    "py": "# nlc:rule={id}",
    "javascript": "// nlc:rule={id}",
    "js": "// nlc:rule={id}",
    "typescript": "// nlc:rule={id}",
    "ts": "// nlc:rule={id}",
}


class RuleReceipt:
    """Owns receipt-line shaping, marker scan/apply, and rule-IR snapshot verbs."""

    def format_marker(self, rule_id: str, lang: str = "python") -> str:
        rid = rule_id.strip()
        if not RULE_ID_RE.match(rid):
            raise ValueError(f"invalid rule_id: {rule_id}")
        key = lang.strip().lower()
        template = _PREFIX.get(key)
        if template is None:
            raise ValueError(
                f"unsupported lang: {lang} (use: {', '.join(sorted(set(_PREFIX)))})"
            )
        return template.format(id=rid)

    def load_adopted(self, path: Path) -> list[dict]:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data.get("adoptions") or []
        return [r for r in rows if isinstance(r, dict) and r.get("rule_id")]

    def parse_adr_arg(self, value: str) -> tuple[int, int] | int | None:
        value = value.strip().lstrip("adr:").lstrip("ADR")
        if ".." in value:
            a, b = value.split("..", 1)
            return (int(a), int(b))
        if value.isdigit():
            return int(value)
        return None

    def adr_in_range(self, adr_id: str, spec: tuple[int, int] | int | None) -> bool:
        if spec is None:
            return True
        try:
            n = int(str(adr_id).strip())
        except ValueError:
            return False
        if isinstance(spec, tuple):
            return spec[0] <= n <= spec[1]
        return n == spec

    def rule_tags(self, rule: dict) -> set[str]:
        match = rule.get("match") or {}
        out: set[str] = set()
        for key in ("tags_all", "tags_any"):
            for t in match.get(key) or []:
                out.add(str(t))
        return out

    def filter_rules(
        self,
        rules: list[dict],
        adr_spec: tuple[int, int] | int | None,
        tag: str | None,
    ) -> list[dict]:
        out: list[dict] = []
        for r in rules:
            if not self.adr_in_range(str(r.get("adr_id", "")), adr_spec):
                continue
            if tag and tag not in self.rule_tags(r):
                continue
            out.append(r)
        return out

    def scan_markers(self, root: Path) -> list[dict]:
        hits: list[dict] = []
        for dirname in SCAN_DIRS:
            base = root / dirname
            if not base.is_dir():
                continue
            for path in base.rglob("*"):
                if not path.is_file():
                    continue
                if any(p in SKIP_DIRS for p in path.parts):
                    continue
                if path.suffix not in {".py", ".ts", ".js", ".tsx", ".jsx", ".mjs", ".cjs"}:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                rel = str(path.relative_to(root)).replace("\\", "/")
                goal_id = ""
                if "/goals/" in rel:
                    goal_id = rel.split("/goals/", 1)[1].split("/", 1)[0]
                for line_no, line in enumerate(text.splitlines(), start=1):
                    for m in MARKER_RE.finditer(line):
                        hits.append(
                            {
                                "rule_id": m.group(1),
                                "file": rel,
                                "line": line_no,
                                "goal_id": goal_id or None,
                            }
                        )
        return hits

    def existing_rule_ids(self, text: str) -> set[str]:
        return {m.group(1) for m in MARKER_RE.finditer(text)}

    def _first_def_body_insert(self, lines: list[str]) -> tuple[int, str]:
        def_idx = -1
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith("def ") and stripped.endswith(":"):
                def_idx = i
                break
        if def_idx < 0:
            return len(lines), "    "
        j = def_idx + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        indent = "    "
        if j < len(lines):
            m = re.match(r"^(\s*)", lines[j])
            if m and m.group(1):
                indent = m.group(1)
            s = lines[j].lstrip()
            dq = chr(34) * 3
            sq = chr(39) * 3
            if s.startswith(dq) or s.startswith(sq):
                quote = s[:3]
                if s.count(quote) >= 2 and len(s) > 3:
                    j += 1
                else:
                    j += 1
                    while j < len(lines) and quote not in lines[j]:
                        j += 1
                    j += 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    m2 = re.match(r"^(\s*)", lines[j])
                    if m2 and m2.group(1):
                        indent = m2.group(1)
        return j, indent

    def apply_markers_to_source(self, text: str, rule_ids: list[str]) -> tuple[str, list[str]]:
        have = self.existing_rule_ids(text)
        missing = [rid for rid in rule_ids if rid not in have]
        if not missing:
            return text, []
        lines = text.splitlines()
        insert_at, indent = self._first_def_body_insert(lines)
        if insert_at == len(lines) or not any(l.strip() for l in lines):
            if lines and lines[-1].strip():
                lines.append("")
        block = [f"{indent}{self.format_marker(rid, 'python')}" for rid in missing]
        out = lines[:insert_at] + block + lines[insert_at:]
        return "\n".join(out) + ("\n" if text.endswith("\n") else ""), missing

    def materialize_ir(self, root: Path) -> list[dict]:
        adopted = root / "rules" / "adopted.json"
        if not adopted.is_file():
            return []
        rows = self.load_adopted(adopted)
        out: list[dict] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            out.append(
                {
                    "rule_id": row.get("rule_id"),
                    "adr_id": row.get("adr_id"),
                    "effect": row.get("effect"),
                    "obligation": row.get("obligation"),
                    "match": row.get("match") or {},
                    "precedence_tier": row.get("precedence_tier"),
                    "precedence_rank": row.get("precedence_rank"),
                }
            )
        return sorted(out, key=lambda r: str(r.get("rule_id") or ""))

    def write_snapshot(self, root: Path, rows: list[dict]) -> Path:
        nlc = root / ".nlc"
        nlc.mkdir(parents=True, exist_ok=True)
        path = nlc / SNAPSHOT
        path.write_text(
            json.dumps({"schema": 1, "rules": rows}, indent=2) + "\n",
            encoding="utf-8",
        )
        return path

    def check_ir(self, root: Path) -> list[str]:
        adopted = root / "rules" / "adopted.json"
        if not adopted.is_file():
            return []
        live = self.materialize_ir(root)
        snap_path = root / ".nlc" / SNAPSHOT
        if not snap_path.is_file():
            return [
                "UC4 rule runner: missing .nlc/rule-ir.snapshot.json "
                "(./nlc maintainer rule-runner --materialize after adopt)"
            ]
        try:
            snap = json.loads(snap_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return ["UC4 rule runner: invalid rule-ir.snapshot.json"]
        stored = snap.get("rules") or []
        if stored != live:
            return [
                "UC4 rule runner: adopted.json drifted from rule-ir.snapshot (re-run --materialize)"
            ]
        bad: list[str] = []
        for row in live:
            rid = row.get("rule_id")
            eff = row.get("effect")
            if eff == "must" and not str(row.get("obligation") or "").strip():
                bad.append(f"rule {rid} effect must requires obligation")
            match = row.get("match") or {}
            if (
                not match.get("primitive")
                and not match.get("tags_all")
                and not match.get("tags_any")
            ):
                bad.append(f"rule {rid} has empty match")
        if bad:
            return ["UC4 rule runner: " + "; ".join(bad[:4])]
        return []


_DEFAULT = RuleReceipt()


def marker_line(rule_id: str, lang: str = "python") -> str:
    return _DEFAULT.format_marker(rule_id, lang)


def load_adopted(path: Path) -> list[dict]:
    return _DEFAULT.load_adopted(path)


def parse_adr_arg(value: str) -> tuple[int, int] | int | None:
    return _DEFAULT.parse_adr_arg(value)


def filter_rules(
    rules: list[dict],
    adr_spec: tuple[int, int] | int | None,
    tag: str | None,
) -> list[dict]:
    return _DEFAULT.filter_rules(rules, adr_spec, tag)


def scan_markers(root: Path) -> list[dict]:
    return _DEFAULT.scan_markers(root)


def apply_markers_to_source(text: str, rule_ids: list[str]) -> tuple[str, list[str]]:
    return _DEFAULT.apply_markers_to_source(text, rule_ids)


def materialize_ir(root: Path) -> list[dict]:
    return _DEFAULT.materialize_ir(root)


def write_snapshot(root: Path, rows: list[dict]) -> Path:
    return _DEFAULT.write_snapshot(root, rows)


def check_ir(root: Path) -> list[str]:
    return _DEFAULT.check_ir(root)

