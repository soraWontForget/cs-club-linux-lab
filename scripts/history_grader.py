"""Shared helpers for history-based Linux Basics Lab progress checkers."""

from __future__ import annotations

import os
import re
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


@dataclass(frozen=True)
class Command:
    raw: str
    tokens: tuple[str, ...]
    source: str
    line_number: int

    @property
    def name(self) -> str:
        if not self.tokens:
            return ""
        return Path(self.tokens[0]).name

    @property
    def args(self) -> tuple[str, ...]:
        return self.tokens[1:]


@dataclass(frozen=True)
class Check:
    activity: str
    label: str
    matcher: Callable[[Command], bool]


def strip_history_metadata(line: str) -> str:
    """Normalize bash/zsh history-file lines and pasted `history` output."""
    line = line.rstrip("\n")

    # zsh EXTENDED_HISTORY format: ": 1715288458:0;ls -la"
    zsh_match = re.match(r"^: \d+:\d+;(.*)$", line)
    if zsh_match:
        return zsh_match.group(1).strip()

    # Pasted `history` command output commonly starts with a command number.
    numbered_match = re.match(r"^\s*\d+\s{1,2}(.*)$", line)
    if numbered_match:
        return numbered_match.group(1).strip()

    return line.strip()


def split_shell_segments(command_line: str) -> list[str]:
    """Split common one-line shell command chains without full shell parsing."""
    segments: list[str] = []
    current: list[str] = []
    quote: str | None = None
    escaped = False
    index = 0

    while index < len(command_line):
        char = command_line[index]

        if escaped:
            current.append(char)
            escaped = False
            index += 1
            continue

        if char == "\\":
            current.append(char)
            escaped = True
            index += 1
            continue

        if quote:
            current.append(char)
            if char == quote:
                quote = None
            index += 1
            continue

        if char in {"'", '"'}:
            quote = char
            current.append(char)
            index += 1
            continue

        if command_line.startswith("&&", index) or command_line.startswith("||", index):
            segment = "".join(current).strip()
            if segment:
                segments.append(segment)
            current = []
            index += 2
            continue

        if char in {";", "|"}:
            segment = "".join(current).strip()
            if segment:
                segments.append(segment)
            current = []
            index += 1
            continue

        current.append(char)
        index += 1

    segment = "".join(current).strip()
    if segment:
        segments.append(segment)

    return segments


def tokenize(segment: str) -> tuple[str, ...]:
    try:
        return tuple(shlex.split(segment, comments=False, posix=True))
    except ValueError:
        return tuple(segment.split())


def parse_history_lines(lines: Iterable[str], source: str = "<memory>") -> list[Command]:
    commands: list[Command] = []

    for line_number, line in enumerate(lines, start=1):
        stripped = strip_history_metadata(line)
        if not stripped or stripped.startswith("#"):
            continue

        for segment in split_shell_segments(stripped):
            tokens = tokenize(segment)
            if tokens:
                commands.append(
                    Command(
                        raw=segment,
                        tokens=tokens,
                        source=source,
                        line_number=line_number,
                    )
                )

    return commands


def parse_history_file(path: Path) -> list[Command]:
    with path.expanduser().open("r", encoding="utf-8", errors="replace") as history:
        return parse_history_lines(history, source=str(path.expanduser()))


def discover_history_files() -> list[Path]:
    candidates: list[Path] = []

    histfile = os.environ.get("HISTFILE")
    if histfile:
        candidates.append(Path(histfile).expanduser())

    candidates.extend(
        [
            Path("~/.bash_history").expanduser(),
            Path("~/.zsh_history").expanduser(),
            Path("~/.linux-basics-history").expanduser(),
        ]
    )

    found: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        resolved = path.resolve(strict=False)
        if resolved in seen:
            continue
        seen.add(resolved)
        if path.exists() and path.is_file():
            found.append(path)

    return found


def is_simple(command_name: str) -> Callable[[Command], bool]:
    return lambda command: command.name == command_name and not command.args


def has_help(command_name: str) -> Callable[[Command], bool]:
    return lambda command: command.name == command_name and "--help" in command.args


def option_profile(command: Command) -> tuple[set[str], bool]:
    letters: set[str] = set()
    unknown_option = False

    for arg in command.args:
        if arg == "--":
            break
        if arg.startswith("--"):
            if arg == "--all":
                letters.add("a")
            else:
                unknown_option = True
            continue
        if arg.startswith("-") and len(arg) > 1:
            letters.update(arg[1:])

    return letters, unknown_option


def positional_args(command: Command) -> list[str]:
    args: list[str] = []
    parsing_options = True

    for arg in command.args:
        if parsing_options and arg == "--":
            parsing_options = False
            continue
        if parsing_options and arg.startswith("-"):
            continue
        args.append(arg.rstrip("/"))

    return args


def is_command(
    command_name: str,
    *,
    required_flags: Iterable[str] = (),
    exact_flags: Iterable[str] | None = None,
    target: str | None = None,
    no_targets: bool = False,
) -> Callable[[Command], bool]:
    required = set(required_flags)
    exact = set(exact_flags) if exact_flags is not None else None
    normalized_target = target.rstrip("/") if target else None

    def matcher(command: Command) -> bool:
        if command.name != command_name:
            return False

        positions = positional_args(command)
        if no_targets and positions:
            return False
        if normalized_target and normalized_target not in positions:
            return False

        letters, unknown_option = option_profile(command)
        if exact is not None:
            return not unknown_option and letters == exact

        return required.issubset(letters)

    return matcher


def is_command_positions(
    command_name: str,
    expected_positions: Iterable[str],
    *,
    required_flags: Iterable[str] = (),
    exact_flags: Iterable[str] | None = None,
) -> Callable[[Command], bool]:
    required = set(required_flags)
    exact = set(exact_flags) if exact_flags is not None else None
    expected = [position.rstrip("/") for position in expected_positions]

    def matcher(command: Command) -> bool:
        if command.name != command_name:
            return False

        if positional_args(command) != expected:
            return False

        letters, unknown_option = option_profile(command)
        if exact is not None:
            return not unknown_option and letters == exact

        return required.issubset(letters)

    return matcher


def is_ls(
    *,
    required_flags: Iterable[str] = (),
    exact_flags: Iterable[str] | None = None,
    target: str | None = None,
    no_targets: bool = False,
) -> Callable[[Command], bool]:
    return is_command(
        "ls",
        required_flags=required_flags,
        exact_flags=exact_flags,
        target=target,
        no_targets=no_targets,
    )


def is_cd(target: str) -> Callable[[Command], bool]:
    normalized_target = target.rstrip("/") if target != "/" else target

    def matcher(command: Command) -> bool:
        if command.name != "cd" or len(command.args) != 1:
            return False
        arg = command.args[0]
        normalized_arg = arg.rstrip("/") if arg != "/" else arg
        return normalized_arg == normalized_target

    return matcher


def is_tree(target: str | None = None) -> Callable[[Command], bool]:
    normalized_target = target.rstrip("/") if target else None

    def matcher(command: Command) -> bool:
        if command.name != "tree":
            return False
        positions = positional_args(command)
        if normalized_target is None:
            return not positions
        return normalized_target in positions

    return matcher


def is_man_page(page: str) -> Callable[[Command], bool]:
    return lambda command: command.name == "man" and page in command.args


def grade(commands: Iterable[Command], checks: Iterable[Check]) -> list[dict[str, object]]:
    command_list = list(commands)
    results: list[dict[str, object]] = []

    for check in checks:
        match = next((command for command in command_list if check.matcher(command)), None)
        results.append(
            {
                "activity": check.activity,
                "label": check.label,
                "passed": match is not None,
                "match": {
                    "command": match.raw,
                    "source": match.source,
                    "line": match.line_number,
                }
                if match
                else None,
            }
        )

    return results


def load_commands(history_files: list[Path]) -> list[Command]:
    commands: list[Command] = []
    for path in history_files:
        commands.extend(parse_history_file(path))
    return commands


def print_text_report(
    *,
    title: str,
    results: list[dict[str, object]],
    history_files: list[Path],
    pass_percent: float,
) -> None:
    passed_count = sum(1 for result in results if result["passed"])
    total_count = len(results)
    percent = (passed_count / total_count) * 100 if total_count else 0.0

    print(f"{title} progress")
    print()
    print("History files checked:")
    for path in history_files:
        print(f"  - {path.expanduser()}")
    print()
    print(f"Score: {passed_count}/{total_count} checks ({percent:.1f}%)")
    print(f"Status: {'complete' if percent >= pass_percent else 'in progress'}")
    print()

    current_activity = None
    for result in results:
        if result["activity"] != current_activity:
            current_activity = str(result["activity"])
            print(current_activity)
        marker = "x" if result["passed"] else " "
        print(f"  [{marker}] {result['label']}")

    missing = [result for result in results if not result["passed"]]
    if missing:
        print()
        print("Missing checks:")
        for result in missing:
            print(f"  - {result['activity']}: {result['label']}")

    print()
    print("Note: this checks command attempts only. It does not grade written checkpoint answers.")
    print("If recent commands are missing, run `history -a` or use the lab shell aliases.")
