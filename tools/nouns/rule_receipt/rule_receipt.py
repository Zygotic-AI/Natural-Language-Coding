"""RuleReceipt noun: private marker/IR policy; verbs are the only mutation path."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

BOUNDARY = "bba-emit"

RULE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
MARKER_RE = re.compile(r"(?:#|//)\s*nlc:rule=([A-Za-z0-9][A-Za-z0-9._-]*)")
OBLIGATION_RE = re.compile(r"nlc:obligation=(.+)")
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

    def _marker_line_for_rule(self, rule_id: str, row: dict | None) -> str:
        line = self.format_marker(rule_id, "python")
        if row and row.get("effect") == "must":
            ob = str(row.get("obligation") or "").strip()
            if ob:
                line = f"{line}  # nlc:obligation={ob}"
        return line

    def apply_markers_to_source(
        self,
        text: str,
        rule_ids: list[str],
        adopted_rows: list[dict] | None = None,
    ) -> tuple[str, list[str]]:
        have = self.existing_rule_ids(text)
        missing = [rid for rid in rule_ids if rid not in have]
        if not missing:
            return text, []
        by_id = {
            str(r["rule_id"]): r
            for r in (adopted_rows or [])
            if isinstance(r, dict) and r.get("rule_id")
        }
        lines = text.splitlines()
        insert_at, indent = self._first_def_body_insert(lines)
        if insert_at == len(lines) or not any(l.strip() for l in lines):
            if lines and lines[-1].strip():
                lines.append("")
        block = [
            f"{indent}{self._marker_line_for_rule(rid, by_id.get(rid))}" for rid in missing
        ]
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

    def tagged_fields(self, root: Path) -> dict[str, set[str]]:
        """Map field identifiers to tags (tags.txt + taint.txt → implicit pan)."""
        out: dict[str, set[str]] = {}
        domain = root / "domain"
        if not domain.is_dir():
            return out
        for path in domain.rglob("tags.txt"):
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                raw = line.split("#", 1)[0].strip()
                if not raw:
                    continue
                parts = raw.split()
                if len(parts) >= 2:
                    out.setdefault(parts[0], set()).add(parts[1])
                elif len(parts) == 1:
                    out.setdefault(parts[0], set()).add(parts[0])
        for path in domain.rglob("taint.txt"):
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                field = line.split("#", 1)[0].strip()
                if field:
                    out.setdefault(field, set()).add("pan")
        return out

    def _expr_uses_tagged_name(self, node: ast.AST | None, tagged: dict[str, set[str]]) -> bool:
        if node is None:
            return False
        names: set[str] = set()

        class V(ast.NodeVisitor):
            def visit_Name(self, n: ast.Name) -> None:
                names.add(n.id)

        V().visit(node)
        return any(n in tagged for n in names)

    def _semantic_forbid_primitive(
        self,
        root: Path,
        rule: dict,
        tagged: dict[str, set[str]],
    ) -> list[str]:
        match = rule.get("match") or {}
        primitive = (match.get("primitive") or "").strip()
        if rule.get("effect") != "forbid" or not primitive:
            return []
        need_tags: set[str] = set(match.get("tags_all") or []) | set(match.get("tags_any") or [])
        if not need_tags:
            return []
        fields = {f for f, tags in tagged.items() if tags & need_tags}
        if not fields:
            return []
        rid = rule.get("rule_id") or "?"
        goals = root / "goals"
        if not goals.is_dir():
            return []
        violations: list[str] = []
        for impl in sorted(goals.rglob("implementation.py")):
            try:
                tree = ast.parse(
                    impl.read_text(encoding="utf-8", errors="replace"),
                    filename=str(impl),
                )
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if primitive == "return" and isinstance(node, ast.Return):
                    if self._expr_uses_tagged_name(node.value, {f: tagged[f] for f in fields}):
                        rel = impl.relative_to(root)
                        violations.append(
                            f"rule {rid}: forbid {primitive} on tagged field at {rel}:{node.lineno}"
                        )
                if primitive == "write" and isinstance(node, ast.Assign):
                    for t in node.targets:
                        if isinstance(t, ast.Name) and t.id in fields:
                            rel = impl.relative_to(root)
                            violations.append(
                                f"rule {rid}: forbid {primitive} on tagged field at {rel}:{node.lineno}"
                            )
        return violations

    def check_semantic_ir(self, root: Path) -> list[str]:
        """UC4 v2: evaluate adopted forbid rules against goal implementations."""
        structural = self.check_ir(root)
        if structural:
            return structural
        adopted = root / "rules" / "adopted.json"
        if not adopted.is_file():
            return []
        rows = self.load_adopted(adopted)
        tagged = self.tagged_fields(root)
        bad: list[str] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            bad.extend(self._semantic_forbid_primitive(root, row, tagged))
        if not bad:
            return []
        return ["UC4 semantic rule runner: " + "; ".join(bad[:4])]

    def check_semantic_apply(self, root: Path) -> list[str]:
        """UC5 v2: compiler-owned markers include must-rule obligation receipts."""
        adopted_path = root / "rules" / "adopted.json"
        if not adopted_path.is_file():
            return []
        rows = self.load_adopted(adopted_path)
        if not rows:
            return []
        want = {str(r["rule_id"]) for r in rows}
        markers = self.scan_markers(root)
        by_rule: dict[str, list[dict]] = {}
        for m in markers:
            by_rule.setdefault(str(m["rule_id"]), []).append(m)
        missing = sorted(want - set(by_rule))
        if missing:
            return [f"UC5 semantic apply: missing markers for {', '.join(missing[:4])}"]
        bad: list[str] = []
        for row in rows:
            if row.get("effect") != "must":
                continue
            ob = str(row.get("obligation") or "").strip()
            if not ob:
                continue
            rid = str(row["rule_id"])
            for site in by_rule.get(rid) or []:
                path = root / site["file"]
                if not path.is_file():
                    bad.append(f"rule {rid}: missing file {site['file']}")
                    continue
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
                line_no = int(site["line"])
                window = lines[max(0, line_no - 1) : min(len(lines), line_no + 2)]
                blob = "\n".join(window)
                if ob not in blob and not any(OBLIGATION_RE.search(ln) and ob in ln for ln in window):
                    bad.append(
                        f"rule {rid}: missing obligation receipt at {site['file']}:{line_no}"
                    )
        if not bad:
            return []
        return ["UC5 semantic apply: " + "; ".join(bad[:4])]


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


def apply_markers_to_source(
    text: str,
    rule_ids: list[str],
    adopted_rows: list[dict] | None = None,
) -> tuple[str, list[str]]:
    return _DEFAULT.apply_markers_to_source(text, rule_ids, adopted_rows)


def materialize_ir(root: Path) -> list[dict]:
    return _DEFAULT.materialize_ir(root)


def write_snapshot(root: Path, rows: list[dict]) -> Path:
    return _DEFAULT.write_snapshot(root, rows)


def check_ir(root: Path) -> list[str]:
    return _DEFAULT.check_ir(root)


def check_semantic_ir(root: Path) -> list[str]:
    return _DEFAULT.check_semantic_ir(root)


def check_semantic_apply(root: Path) -> list[str]:
    return _DEFAULT.check_semantic_apply(root)

