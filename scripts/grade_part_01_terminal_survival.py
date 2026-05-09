#!/usr/bin/env python3
"""Progress checker for Part 1: Terminal Survival.

This intentionally grades command attempts from shell history, not written
answers. It is best used as a formative checker inside a controlled lab
container where history is appended after each command.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
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


def is_ls(
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
        if command.name != "ls":
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


def is_man_page(page: str) -> Callable[[Command], bool]:
    return lambda command: command.name == "man" and page in command.args


CHECKS: tuple[Check, ...] = (
    Check("Activity 1", "Run `pwd`", is_simple("pwd")),
    Check("Activity 2", "Run bare `ls`", is_ls(exact_flags=set(), no_targets=True)),
    Check("Activity 2", "List `lab-files`", is_ls(exact_flags=set(), target="lab-files")),
    Check("Activity 2", "List `lab-files/campus`", is_ls(exact_flags=set(), target="lab-files/campus")),
    Check("Activity 2", "List `lab-files/campus/clubs`", is_ls(exact_flags=set(), target="lab-files/campus/clubs")),
    Check("Activity 2", "List `lab-files/campus/classes`", is_ls(exact_flags=set(), target="lab-files/campus/classes")),
    Check("Activity 3", "Run `ls -l`", is_ls(exact_flags={"l"}, no_targets=True)),
    Check("Activity 3", "Run `ls -a`", is_ls(exact_flags={"a"}, no_targets=True)),
    Check("Activity 3", "Run `ls -la` or `ls -al`", is_ls(exact_flags={"l", "a"}, no_targets=True)),
    Check(
        "Activity 3",
        "Run `ls -lh lab-files/campus/classes`",
        is_ls(exact_flags={"l", "h"}, target="lab-files/campus/classes"),
    ),
    Check("Activity 4", "Run `clear`", is_simple("clear")),
    Check("Activity 5", "Run `whoami`", is_simple("whoami")),
    Check("Activity 5", "Run `hostname`", is_simple("hostname")),
    Check("Activity 5", "Run `date`", is_simple("date")),
    Check("Activity 6", "Run `history`", is_simple("history")),
    Check("Activity 7", "Run `ls --help`", has_help("ls")),
    Check("Activity 7", "Run `date --help`", has_help("date")),
    Check("Activity 7", "Run `whoami --help`", has_help("whoami")),
    Check("Activity 7", "Run `man ls`", is_man_page("ls")),
)


def grade(commands: Iterable[Command]) -> list[dict[str, object]]:
    command_list = list(commands)
    results: list[dict[str, object]] = []

    for check in CHECKS:
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


def print_text_report(results: list[dict[str, object]], history_files: list[Path], pass_percent: float) -> None:
    passed_count = sum(1 for result in results if result["passed"])
    total_count = len(results)
    percent = (passed_count / total_count) * 100 if total_count else 0.0

    print("Part 1: Terminal Survival progress")
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
    print("If recent commands are missing, run `history -a` or configure the lab shell to append history after each command.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--history-file",
        action="append",
        type=Path,
        help="History file to grade. Can be passed more than once. Defaults to HISTFILE, ~/.bash_history, ~/.zsh_history, and ~/.linux-basics-history when present.",
    )
    parser.add_argument(
        "--pass-percent",
        type=float,
        default=100.0,
        help="Percent required for the text report status to show complete. Default: 100.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args(argv)

    history_files = args.history_file if args.history_file else discover_history_files()
    if not history_files:
        print(
            "No shell history file found. Pass --history-file PATH or configure HISTFILE in the lab container.",
            file=sys.stderr,
        )
        return 2

    commands = load_commands(history_files)
    results = grade(commands)
    passed_count = sum(1 for result in results if result["passed"])
    percent = (passed_count / len(results)) * 100 if results else 0.0

    if args.json:
        print(
            json.dumps(
                {
                    "lab": "part-01-terminal-survival",
                    "history_files": [str(path.expanduser()) for path in history_files],
                    "passed": percent >= args.pass_percent,
                    "score": {
                        "passed": passed_count,
                        "total": len(results),
                        "percent": round(percent, 1),
                    },
                    "checks": results,
                },
                indent=2,
            )
        )
    else:
        print_text_report(results, history_files, args.pass_percent)

    return 0 if percent >= args.pass_percent else 1


if __name__ == "__main__":
    raise SystemExit(main())
