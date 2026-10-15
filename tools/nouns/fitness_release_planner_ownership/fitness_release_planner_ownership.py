"""ADR 0049: the release planner owns every intentional stop."""

from __future__ import annotations

import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path

BOUNDARY = "bba-emit"

EXECUTOR_REL = "goals/hub_release/execute.sh"
PLANNER_REL = "tools/nouns/release_state/release_state.py"
OBSERVER_REL = "tools/nouns/nlc_release_state/nlc_release_state.py"

CLOSED_KINDS = frozenset({"REPAIR", "AWAIT", "HUMAN_DECISION", "TERMINAL"})
REQUIRED_ACTIONS: dict[str, str] = {
    "ENSURE_MIGRATIONS": "REPAIR",
    "VERIFY_SHIPPED_BASELINE": "REPAIR",
    "WRITE_NOTES": "REPAIR",
    "ALIGN_VERSION": "REPAIR",
    "VERIFY_TARGET": "REPAIR",
    "PREP": "REPAIR",
    "WRITE_RECORD": "REPAIR",
    "COMMIT": "REPAIR",
    "CREATE_RELEASE_LINE": "REPAIR",
    "CREATE_REPAIR_COMMIT": "REPAIR",
    "FETCH_REMOTE": "REPAIR",
    "FAST_FORWARD_LOCAL": "REPAIR",
    "PUSH_NEW": "REPAIR",
    "PUSH_FAST_FORWARD": "REPAIR",
    "CREATE_PR": "REPAIR",
    "CREATE_LOCAL_TAG": "REPAIR",
    "PUSH_TAG": "REPAIR",
    "RETRY_PUBLISH": "REPAIR",
    "EXIT_AWAIT": "AWAIT",
    "OBSERVE_PUBLISH": "AWAIT",
    "BLOCKED": "HUMAN_DECISION",
    "NONE": "TERMINAL",
}
_GENERIC_FACT = re.compile(
    r"(?i)^(?:runtime[_-]?error|generic[_-]?runtime(?:[_-]?error)?|generic[_-]?error)$"
)
_SET_E = re.compile(r"(?<![A-Za-z0-9_])set\s+(?:-[A-Za-z]*e[A-Za-z]*|-o\s+errexit)\b")
_EXIT = re.compile(r"(?<![A-Za-z0-9_])exit(?:\s+(\S+))?")
_RETURN = re.compile(r"(?<![A-Za-z0-9_])return(?:\s+(\S+))?")
_RELEASE_FAIL = re.compile(r"(?<![A-Za-z0-9_])release_fail(?!\s*\()(?![A-Za-z0-9_])")
_PYTHON = re.compile(r"(?<![A-Za-z0-9_])python3?(?![A-Za-z0-9_])")
_LOOP_WORD = re.compile(r"(?<![A-Za-z0-9_])(?:while|until|for)(?![A-Za-z0-9_])")
_DO = re.compile(r"(?<![A-Za-z0-9_])do(?![A-Za-z0-9_])")
_DONE = re.compile(r"(?<![A-Za-z0-9_])done(?![A-Za-z0-9_])")
_PLANNER_REF = re.compile(
    r"(?<![A-Za-z0-9_])(?:nlc_release_state|plan_release|release_plan_field)(?![A-Za-z0-9_])"
)
_FUNC = re.compile(r"(?:function\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)")
_BOUNDARY = "action_result_boundary:"
_DISPATCH = "dispatch_release_plan"


@dataclass(frozen=True)
class _ShellLine:
    number: int
    text: str
    commands: str
    function: str


def planner_ownership_errors(root: Path) -> list[str]:
    """Return release-planner ownership failures for one specimen root."""
    errors: list[str] = []
    executor = root / EXECUTOR_REL
    planner = root / PLANNER_REL
    observer = root / OBSERVER_REL
    executor_text = _read(executor, EXECUTOR_REL, errors)
    planner_text = _read(planner, PLANNER_REL, errors)
    observer_text = _read(observer, OBSERVER_REL, errors)
    if executor_text is not None:
        errors.extend(_executor_errors(executor_text))
    if planner_text is not None:
        errors.extend(_planner_errors(planner_text, PLANNER_REL))
    if observer_text is not None:
        errors.extend(_observer_errors(observer_text, OBSERVER_REL))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = planner_ownership_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


def _read(path: Path, rel: str, errors: list[str]) -> str | None:
    if not path.is_file():
        errors.append(f"missing {rel}")
        return None
    return path.read_text(encoding="utf-8")


def _executor_errors(source: str) -> list[str]:
    lines = _shell_lines(source)
    errors: list[str] = []
    for line in lines:
        if _SET_E.search(line.commands):
            errors.append(f"executor enables set -e ({line.number})")
    helpers = _stop_helpers(lines)
    for line in lines:
        if line.function == _DISPATCH:
            continue
        exit_kind = _status_kind(_EXIT, line.commands, bare_is_dynamic=True)
        if exit_kind:
            errors.append(
                f"executor {exit_kind} exit outside {_DISPATCH} ({line.number})"
            )
        return_kind = _status_kind(_RETURN, line.commands, bare_is_dynamic=False)
        if return_kind:
            errors.append(
                f"executor {return_kind} return outside {_DISPATCH} ({line.number})"
            )
        if _RELEASE_FAIL.search(line.commands):
            errors.append(f"executor release_fail call outside {_DISPATCH} ({line.number})")
        for name in sorted(helpers):
            if _calls(line.commands, name):
                errors.append(
                    f"executor failure helper {name} outside {_DISPATCH} ({line.number})"
                )
    if not any(_is_action_loop(body) for body in _loop_bodies(lines)):
        errors.append("executor missing planner action loop")
    command_text = "\n".join(line.commands for line in lines)
    for action, kind in REQUIRED_ACTIONS.items():
        if kind != "REPAIR":
            continue
        token = f"{_BOUNDARY}{action}"
        if re.search(rf"{re.escape(token)}(?![A-Za-z0-9_])", command_text) is None:
            errors.append(f"executor missing action result boundary for {action}")
    errors.extend(_python_bypass_errors(lines, helpers))
    errors.extend(_shell_git_errors(lines))
    return errors


def _planner_errors(source: str, rel: str) -> list[str]:
    tree = _parsed(source, rel)
    if isinstance(tree, str):
        return [tree]
    errors = _registry_errors(tree)
    errors.extend(_prefix(rel, _python_git_errors(tree)))
    return errors


def _observer_errors(source: str, rel: str) -> list[str]:
    tree = _parsed(source, rel)
    if isinstance(tree, str):
        return [tree]
    errors: list[str] = []
    if not _has_main_context(tree):
        errors.append("observer omits main_context")
    if re.search(r'else\s*\(\s*["\']contained["\']', source):
        errors.append("observer treats an unproved context as contained")
    for name in _generic_facts(tree):
        errors.append(f"observer has generic runtime-error fact {name}")
    errors.extend(_prefix(rel, _python_git_errors(tree)))
    return errors


def _registry_errors(tree: ast.AST) -> list[str]:
    registry = _action_kinds(tree)
    if registry is None:
        return ["planner ACTION_KINDS is not a closed literal registry"]
    errors: list[str] = []
    for action, kind in REQUIRED_ACTIONS.items():
        actual = registry.get(action)
        if actual is None:
            errors.append(f"planner action {action} is missing from ACTION_KINDS")
        elif actual not in CLOSED_KINDS or actual != kind:
            errors.append(f"planner action {action} is untyped ({actual})")
    for action, kind in registry.items():
        if action in REQUIRED_ACTIONS:
            continue
        shown = kind if kind else "missing"
        errors.append(f"planner action {action} is untyped ({shown})")
    progress = _tuple_registry(tree, "ACTION_PROGRESS_FACTS")
    repairs = {action for action, kind in REQUIRED_ACTIONS.items() if kind == "REPAIR"}
    if progress is None:
        errors.append("planner ACTION_PROGRESS_FACTS is not a closed literal registry")
    else:
        missing = sorted(repairs - set(progress))
        extra = sorted(set(progress) - repairs)
        for action in missing:
            errors.append(f"planner repair {action} has no progress fact tuple")
        for action in extra:
            errors.append(f"planner non-repair {action} has a progress fact tuple")
        for action, names in progress.items():
            if not names:
                errors.append(f"planner repair {action} has an empty progress fact tuple")
    return errors


def _action_kinds(tree: ast.AST) -> dict[str, str] | None:
    if not isinstance(tree, ast.Module):
        return None
    found: dict[str, str] | None = None
    seen = False
    for node in tree.body:
        value: ast.AST | None = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "ACTION_KINDS":
                value = node.value
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "ACTION_KINDS":
                    value = node.value
        if value is None:
            continue
        seen = True
        found = _literal_dict(value)
    if not seen:
        return None
    return found


def _literal_dict(node: ast.AST) -> dict[str, str] | None:
    if not isinstance(node, ast.Dict):
        return None
    found: dict[str, str] = {}
    for key, value in zip(node.keys, node.values, strict=True):
        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
            return None
        if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
            return None
        found[key.value] = value.value
    return found


def _tuple_registry(tree: ast.AST, name: str) -> dict[str, tuple[str, ...]] | None:
    if not isinstance(tree, ast.Module):
        return None
    for node in tree.body:
        value: ast.AST | None = None
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == name
        ):
            value = node.value
        elif isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        ):
            value = node.value
        if not isinstance(value, ast.Dict):
            continue
        found: dict[str, tuple[str, ...]] = {}
        for key, item in zip(value.keys, value.values, strict=True):
            if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                return None
            if not isinstance(item, ast.Tuple):
                return None
            names: list[str] = []
            for element in item.elts:
                if not isinstance(element, ast.Constant) or not isinstance(
                    element.value, str
                ):
                    return None
                names.append(element.value)
            found[key.value] = tuple(names)
        return found
    return None


def _has_main_context(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "observe":
            return _function_has_key(node, "main_context")
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "observe":
            return _function_has_key(node, "main_context")
    return False


def _function_has_key(node: ast.AST, key: str) -> bool:
    for inner in ast.walk(node):
        if isinstance(inner, ast.Dict):
            for item in inner.keys:
                if isinstance(item, ast.Constant) and item.value == key:
                    return True
        targets: list[ast.AST] = []
        if isinstance(inner, ast.Assign):
            targets.extend(inner.targets)
        elif isinstance(inner, ast.AnnAssign):
            targets.append(inner.target)
        for target in targets:
            if (
                isinstance(target, ast.Subscript)
                and isinstance(target.slice, ast.Constant)
                and target.slice.value == key
            ):
                return True
    return False


def _generic_facts(tree: ast.AST) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key in node.keys:
            if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                continue
            if _GENERIC_FACT.match(key.value) and key.value not in found:
                found.append(key.value)
    return found


def _python_git_errors(tree: ast.AST) -> list[str]:
    errors: list[str] = []
    for node in ast.walk(tree):
        argv = _string_sequence(node)
        if argv is not None:
            errors.extend(_git_ops(argv))
            continue
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and "git " in node.value:
            errors.extend(_git_ops(node.value.split()))
    return errors


def _string_sequence(node: ast.AST) -> list[str] | None:
    if not isinstance(node, ast.List | ast.Tuple):
        return None
    values: list[str] = []
    for item in node.elts:
        if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
            return None
        values.append(item.value)
    return values


def _shell_git_errors(lines: list[_ShellLine]) -> list[str]:
    errors: list[str] = []
    for line in lines:
        for name in _git_ops(line.commands.split()):
            errors.append(f"forbidden automatic {name} ({line.number})")
    return errors


def _git_ops(tokens: list[str]) -> list[str]:
    found: list[str] = []
    for index, token in enumerate(tokens):
        if token.strip("();") != "git" or index + 1 >= len(tokens):
            continue
        sub = tokens[index + 1].strip("();")
        args = [argument.strip("();") for argument in tokens[index + 2 :]]
        if sub == "merge":
            found.append("git merge")
        elif sub == "stash":
            found.append("git stash")
        elif sub == "push" and any(arg in {"--force", "-f"} for arg in args):
            found.append("git push --force")
        elif sub == "tag" and any(arg in {"-f", "--force"} for arg in args):
            found.append("git tag -f")
        elif sub == "reset" and "--hard" in args:
            found.append("git reset --hard")
    return found


def _python_bypass_errors(lines: list[_ShellLine], helpers: set[str]) -> list[str]:
    errors: list[str] = []
    for line in lines:
        if _direct_python_failure(line.text, helpers):
            where = line.function or "top-level"
            errors.append(
                "executor python failure bypasses action result boundary "
                f"({where}:{line.number})"
            )
    return errors


def _direct_python_failure(text: str, helpers: set[str]) -> bool:
    if _PYTHON.search(text) is None or _BOUNDARY in text:
        return False
    if re.search(r"(?:\|\||&&)\s*(?:exit|return)(?![A-Za-z0-9_])", text):
        return True
    if _RELEASE_FAIL.search(text):
        return True
    return any(_calls(text, name) for name in helpers)


def _stop_helpers(lines: list[_ShellLine]) -> set[str]:
    helpers: set[str] = set()
    changed = True
    while changed:
        changed = False
        for line in lines:
            name = line.function
            if not name or name == _DISPATCH or name in helpers:
                continue
            stops = _status_kind(_EXIT, line.commands, bare_is_dynamic=True) or _status_kind(
                _RETURN, line.commands, bare_is_dynamic=False
            )
            calls_helper = any(_calls(line.commands, helper) for helper in helpers)
            if stops or _RELEASE_FAIL.search(line.commands) or calls_helper:
                helpers.add(name)
                changed = True
    return helpers


def _loop_bodies(lines: list[_ShellLine]) -> list[str]:
    awaiting_do = 0
    stack: list[list[str]] = []
    finished: list[str] = []
    for line in lines:
        if _LOOP_WORD.search(line.text):
            awaiting_do += len(_LOOP_WORD.findall(line.text))
        if awaiting_do and _DO.search(line.text):
            awaiting_do -= 1
            stack.append([])
            continue
        if stack and _DONE.search(line.text):
            finished.append("\n".join(stack.pop()))
            continue
        if stack:
            stack[-1].append(line.text)
    return finished


def _is_action_loop(body: str) -> bool:
    performs = _DISPATCH in body or _BOUNDARY in body
    return _PLANNER_REF.search(body) is not None and performs


def _shell_lines(source: str) -> list[_ShellLine]:
    brace = 0
    stack: list[tuple[str, int]] = []
    pending = ""
    heredoc = ""
    rows: list[_ShellLine] = []
    for number, raw in enumerate(source.splitlines(), 1):
        if heredoc:
            if raw.strip() == heredoc:
                heredoc = ""
            continue
        terminator = _heredoc_terminator(raw)
        text = _strip_comment(raw)
        commands = _strip_quotes(text)
        current = stack[-1][0] if stack else ""
        rows.append(_ShellLine(number, text, commands, current))
        pending, brace, stack = _apply_structure(commands, pending, brace, stack)
        if terminator:
            heredoc = terminator
    return rows


def _apply_structure(
    commands: str,
    pending: str,
    brace: int,
    stack: list[tuple[str, int]],
) -> tuple[str, int, list[tuple[str, int]]]:
    structure = re.sub(r"\$\{[^{}]*\}", "", commands)
    index = 0
    while index < len(structure):
        matched = _FUNC.match(structure, index)
        previous = structure[index - 1] if index else ""
        if matched and (index == 0 or not (previous.isalnum() or previous == "_")):
            pending = matched.group(1)
            index = matched.end()
            continue
        character = structure[index]
        if character == "{":
            brace += 1
            if pending:
                stack.append((pending, brace))
                pending = ""
        elif character == "}":
            if stack and stack[-1][1] == brace:
                stack.pop()
            brace = max(0, brace - 1)
        index += 1
    return pending, brace, stack


def _heredoc_terminator(line: str) -> str:
    quote: str | None = None
    index = 0
    while index < len(line):
        character = line[index]
        if quote is not None:
            if character == quote:
                quote = None
            index += 1
            continue
        if character in {"'", '"'}:
            quote = character
            index += 1
            continue
        if character == "#":
            return ""
        if character == "<" and index + 1 < len(line) and line[index + 1] == "<":
            if index + 2 < len(line) and line[index + 2] == "<":
                index += 3
                continue
            return _heredoc_word(line, index + 2)
        index += 1
    return ""


def _heredoc_word(line: str, index: int) -> str:
    if index < len(line) and line[index] == "-":
        index += 1
    while index < len(line) and line[index].isspace():
        index += 1
    quote = ""
    if index < len(line) and line[index] in {"'", '"'}:
        quote = line[index]
        index += 1
    start = index
    while index < len(line) and (line[index].isalnum() or line[index] == "_"):
        index += 1
    word = line[start:index]
    if quote and (index >= len(line) or line[index] != quote):
        return ""
    return word


def _strip_comment(line: str) -> str:
    out: list[str] = []
    quote: str | None = None
    index = 0
    while index < len(line):
        character = line[index]
        if quote is None:
            if character == "\\" and index + 1 < len(line):
                out.append(line[index : index + 2])
                index += 2
                continue
            if character in {"'", '"'}:
                quote = character
                out.append(character)
                index += 1
                continue
            if character == "#":
                break
            out.append(character)
            index += 1
            continue
        out.append(character)
        if character == "\\" and quote == '"' and index + 1 < len(line):
            out.append(line[index + 1])
            index += 2
            continue
        if character == quote:
            quote = None
        index += 1
    return "".join(out)


def _strip_quotes(line: str) -> str:
    out: list[str] = []
    quote: str | None = None
    index = 0
    while index < len(line):
        character = line[index]
        if quote is None:
            if character == "\\" and index + 1 < len(line):
                out.append(line[index + 1])
                index += 2
                continue
            if character in {"'", '"'}:
                quote = character
                index += 1
                continue
            out.append(character)
            index += 1
            continue
        if character == "\\" and quote == '"' and index + 1 < len(line):
            index += 2
            continue
        if character == quote:
            quote = None
        index += 1
    return "".join(out)


def _status_kind(pattern: re.Pattern[str], commands: str, *, bare_is_dynamic: bool) -> str:
    found = ""
    for match in pattern.finditer(commands):
        arg = match.group(1)
        if arg is None:
            if bare_is_dynamic:
                found = "dynamic"
            continue
        if arg == "0":
            continue
        found = "nonzero" if arg.isdigit() else "dynamic"
    return found


def _calls(commands: str, name: str) -> bool:
    return (
        re.search(
            rf"(?<![A-Za-z0-9_]){re.escape(name)}(?!\s*\()(?![A-Za-z0-9_])",
            commands,
        )
        is not None
    )


def _parsed(source: str, rel: str) -> ast.AST | str:
    try:
        return ast.parse(source)
    except SyntaxError as exc:
        return f"{rel} syntax: {exc.msg}"


def _prefix(rel: str, names: list[str]) -> list[str]:
    return [f"{rel} forbidden automatic {name}" for name in names]


if __name__ == "__main__":
    sys.exit(main())
