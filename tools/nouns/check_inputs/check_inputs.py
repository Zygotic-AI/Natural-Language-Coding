"""Self-derived declared inputs for every labeled ci_fitness check."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import ast
import json
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[3]
CI_FITNESS = ROOT / "tools" / "nouns" / "ci_fitness" / "ci_fitness.py"
SNAPSHOT_REL = "integrity/check-inputs.json"
RELEASABLE = ROOT / "integrity" / "releasable-gates.json"


class CheckDecl(NamedTuple):
    """One labeled suite check and the script it runs."""

    label: str
    script: str
    kind: str


def _tracked(root: Path) -> set[str]:
    import subprocess

    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return set()
    out: set[str] = set()
    for line in (proc.stdout or "").splitlines():
        line = line.strip().replace("\\", "/")
        if line and "__pycache__" not in line and not line.endswith(".pyc"):
            out.add(line)
    return out


def _kind_for_script(script: str) -> str:
    name = Path(script).name
    if name.startswith("assert-"):
        return "landmine"
    if name.startswith("fitness-"):
        return "fitness"
    return "other"


def _script_from_list(node: ast.AST) -> str | None:
    if not isinstance(node, ast.List):
        return None
    for elt in node.elts:
        if isinstance(elt, ast.BinOp) and isinstance(elt.op, ast.Div):
            right = elt.right
            if isinstance(right, ast.Constant) and isinstance(right.value, str):
                name = right.value
                if name.endswith(".py"):
                    return "tools/" + name
    return None


def _explicit_run_checks(tree: ast.AST) -> list[CheckDecl]:
    found: list[CheckDecl] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Name) or func.id != "run":
            continue
        if len(node.args) < 2:
            continue
        label_node = node.args[0]
        if not isinstance(label_node, ast.Constant) or not isinstance(label_node.value, str):
            continue
        script = _script_from_list(node.args[1])
        if not script:
            continue
        found.append(CheckDecl(label_node.value, script, _kind_for_script(script)))
    return found


def _hub_only_names(root: Path) -> set[str]:
    path = root / "integrity" / "releasable-gates.json"
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return set(data.get("hub_only_fitness") or [])


def discover_checks(root: Path) -> list[CheckDecl]:
    """Every labeled check ci_fitness can run, derived from the runner plus globs."""
    text = (root / "tools" / "nouns" / "ci_fitness" / "ci_fitness.py").read_text(encoding="utf-8")
    tree = ast.parse(text)
    by_label: dict[str, CheckDecl] = {}
    for item in _explicit_run_checks(tree):
        by_label[item.label] = item
    tools_dir = root / "tools"
    for path in sorted(tools_dir.glob("assert-*-fails.py")):
        rel = "tools/" + path.name
        label = str(path.relative_to(root)).replace("\\", "/")
        by_label.setdefault(label, CheckDecl(label, rel, "landmine"))
        by_label.setdefault(path.stem, CheckDecl(path.stem, rel, "landmine"))
    for path in sorted(tools_dir.glob("assert-release-probe-*-passes.py")):
        rel = "tools/" + path.name
        by_label.setdefault(path.stem, CheckDecl(path.stem, rel, "landmine"))
    hub_only = _hub_only_names(root)
    for path in sorted(tools_dir.glob("fitness-*.py")):
        if path.name in hub_only:
            continue
        rel = "tools/" + path.name
        label = f"{path.name} invoice-correct"
        by_label.setdefault(label, CheckDecl(label, rel, "fitness"))
    examples = root / "examples"
    if examples.is_dir():
        sys.path.insert(0, str(root / "tools"))
        from nouns.field_write_bypass_fixtures.field_write_bypass_fixtures import (  # noqa: E402
            O9A_BYPASS_FIXTURE_DIRS,
        )

        skip = {"invoice-violation", "internal-link-landmine"} | set(O9A_BYPASS_FIXTURE_DIRS)
        for path in sorted(examples.iterdir()):
            if not path.is_dir() or path.name in skip or path.name.startswith("invoice-bypass-"):
                continue
            label = f"no-noun-field-writes {path.name}"
            by_label.setdefault(
                label,
                CheckDecl(label, "tools/fitness-no-noun-field-writes.py", "fitness"),
            )
    return [by_label[k] for k in sorted(by_label)]


def _noun_dir_for_script(script: str) -> str:
    stem = Path(script).stem.replace("-", "_")
    return "tools/nouns/" + stem


def own_files(root: Path, script: str, tracked: set[str]) -> list[str]:
    """Adapter plus its noun package; landmines stay inside this set."""
    files: set[str] = set()
    if script in tracked:
        files.add(script)
    noun_prefix = _noun_dir_for_script(script) + "/"
    for rel in tracked:
        if rel == _noun_dir_for_script(script) or rel.startswith(noun_prefix):
            files.add(rel)
    return sorted(files)


def _string_constants(source: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    out: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            out.append(node.value)
    return out


def extra_inputs(root: Path, files: list[str], tracked: set[str]) -> list[str]:
    """Tracked paths named as string constants in the check's own files."""
    extra: set[str] = set()
    for rel in files:
        path = root / rel
        if not path.is_file() or not rel.endswith(".py"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for raw in _string_constants(text):
            norm = raw.replace("\\", "/").removeprefix("./")
            if norm in tracked:
                extra.add(norm)
    return sorted(extra)


def declared_inputs(root: Path, check: CheckDecl, tracked: set[str] | None = None) -> list[str]:
    """Declared inputs derived from the check's own files (and named paths)."""
    fileset = tracked if tracked is not None else _tracked(root)
    own = own_files(root, check.script, fileset)
    if check.kind == "landmine":
        return own
    extra = extra_inputs(root, own, fileset)
    return sorted(set(own) | set(extra))


def derive_payload(root: Path) -> dict[str, object]:
    tracked = _tracked(root)
    checks = []
    for check in discover_checks(root):
        checks.append(
            {
                "label": check.label,
                "script": check.script,
                "kind": check.kind,
                "inputs": declared_inputs(root, check, tracked),
            }
        )
    return {
        "schema": 1,
        "source": "tools/nouns/check_inputs/check_inputs.py",
        "checks": checks,
    }


def load_committed(root: Path) -> dict[str, object] | None:
    path = root / SNAPSHOT_REL
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def check_inputs_map(root: Path, payload: dict[str, object] | None = None) -> dict[str, list[str]]:
    data = payload if payload is not None else load_committed(root)
    if data is None:
        raise ValueError("unreadable check-inputs map")
    rows = data.get("checks")
    if not isinstance(rows, list) or not rows:
        raise ValueError("unreadable check-inputs map")
    out: dict[str, list[str]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("unreadable check-inputs map")
        label = row.get("label")
        inputs = row.get("inputs")
        if not isinstance(label, str) or not label:
            raise ValueError("unreadable check-inputs map")
        if not isinstance(inputs, list) or not all(isinstance(x, str) and x for x in inputs):
            raise ValueError("unreadable check-inputs map")
        out[label] = list(inputs)
    return out


def declaration_errors(root: Path) -> list[str]:
    """Fail when any suite check lacks a declaration or the committed map drifts."""
    errors: list[str] = []
    derived = derive_payload(root)
    committed = load_committed(root)
    if committed is None:
        errors.append(f"missing or unreadable {SNAPSHOT_REL}")
    elif committed != derived:
        errors.append(f"{SNAPSHOT_REL} differs from derived check inputs")
    derived_map = check_inputs_map(root, derived)
    for check in discover_checks(root):
        inputs = derived_map.get(check.label) or []
        if not inputs:
            errors.append(f"{check.label} lacks a declaration")
    return errors


def write_snapshot(root: Path) -> Path:
    dest = root / SNAPSHOT_REL
    dest.write_text(json.dumps(derive_payload(root), indent=2) + "\n", encoding="utf-8")
    return dest


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = ROOT
    if "--write" in args:
        dest = write_snapshot(root)
        payload = json.loads(dest.read_text(encoding="utf-8"))
        print(f"wrote {SNAPSHOT_REL} ({len(payload.get('checks') or [])} checks)")
        return 0
    errors = declaration_errors(root)
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
