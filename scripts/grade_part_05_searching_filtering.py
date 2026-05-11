#!/usr/bin/env python3
"""Progress checker for Part 5: Searching, Filtering, and Pipes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

try:
    from .history_grader import (
        Check,
        Command,
        discover_history_files,
        grade as grade_commands,
        is_cd,
        is_from_pipeline,
        load_commands,
        option_profile,
        parse_history_lines,
        positional_args,
        print_text_report,
        split_shell_segments,
        tokenize,
    )
except ImportError:
    from history_grader import (
        Check,
        Command,
        discover_history_files,
        grade as grade_commands,
        is_cd,
        is_from_pipeline,
        load_commands,
        option_profile,
        parse_history_lines,
        positional_args,
        print_text_report,
        split_shell_segments,
        tokenize,
    )


LAB_ID = "part-05-searching-filtering-pipes"
TITLE = "Part 5: Searching, Filtering, and Pipes"
INCIDENTS_FILE = "lab-files/search-practice/incidents.csv"


def command_name(tokens: Iterable[str]) -> str:
    tokens = tuple(tokens)
    if not tokens:
        return ""
    return Path(tokens[0]).name


def token_args(tokens: Iterable[str]) -> tuple[str, ...]:
    tokens = tuple(tokens)
    return tokens[1:]


def is_find_name_txt(command: Command) -> bool:
    return command.name == "find" and command.args == (".", "-name", "*.txt")


def is_find_type_file(command: Command) -> bool:
    return command.name == "find" and command.args == (".", "-type", "f")


def is_grep_pattern(
    pattern: str,
    target: str,
    *,
    exact_flags: Iterable[str],
):
    expected_flags = set(exact_flags)

    def matcher(command: Command) -> bool:
        if command.name != "grep":
            return False

        letters, unknown_option = option_profile(command)
        if unknown_option or letters != expected_flags:
            return False

        return positional_args(command) == [pattern, target]

    return matcher


def cut_has_delimiter(args: tuple[str, ...], delimiter: str) -> bool:
    for index, arg in enumerate(args):
        if arg == "-d" and index + 1 < len(args) and args[index + 1] == delimiter:
            return True
        if arg.startswith("-d") and arg[2:] == delimiter:
            return True
        if arg == f"--delimiter={delimiter}":
            return True
    return False


def cut_has_field(args: tuple[str, ...], field: str) -> bool:
    for index, arg in enumerate(args):
        if arg == "-f" and index + 1 < len(args) and args[index + 1] == field:
            return True
        if arg.startswith("-f") and arg[2:] == field:
            return True
        if arg == f"--fields={field}":
            return True
    return False


def is_cut_incident_type(command: Command) -> bool:
    if command.name != "cut" or INCIDENTS_FILE not in command.args:
        return False

    return cut_has_delimiter(command.args, ",") and cut_has_field(command.args, "1")


def pipeline_tokens(command: Command) -> list[tuple[str, ...]]:
    if not is_from_pipeline(command):
        return []
    return [tokenize(segment) for segment in split_shell_segments(command.history_line)]


def is_cat_errors_grep_error_pipeline(command: Command) -> bool:
    segments = pipeline_tokens(command)
    for index in range(len(segments) - 1):
        left = segments[index]
        right = segments[index + 1]
        if command_name(left) == "cat" and token_args(left) == ("logs/errors.log",):
            if command_name(right) == "grep" and token_args(right) == ("ERROR",):
                return True
    return False


def is_find_txt_sort_pipeline(command: Command) -> bool:
    segments = pipeline_tokens(command)
    for index in range(len(segments) - 1):
        left = segments[index]
        right = segments[index + 1]
        if command_name(left) == "find" and token_args(left) == (".", "-name", "*.txt"):
            if command_name(right) == "sort" and not token_args(right):
                return True
    return False


def is_cut_sort_uniq_pipeline(command: Command) -> bool:
    segments = pipeline_tokens(command)
    for index in range(len(segments) - 2):
        cut_command = Command(
            raw=" ".join(segments[index]),
            tokens=segments[index],
            source=command.source,
            line_number=command.line_number,
            source_line=command.history_line,
            segment_index=index,
        )
        sort_tokens = segments[index + 1]
        uniq_tokens = segments[index + 2]

        if not is_cut_incident_type(cut_command):
            continue
        if command_name(sort_tokens) != "sort" or token_args(sort_tokens):
            continue
        if command_name(uniq_tokens) != "uniq" or token_args(uniq_tokens):
            continue

        return True

    return False


CHECKS: tuple[Check, ...] = (
    Check("Before You Start", "Go to `/home/student/lab`", is_cd("/home/student/lab")),
    Check("Activity 1", "Run `find . -name \"*.txt\"`", is_find_name_txt),
    Check("Activity 2", "Run `find . -type f`", is_find_type_file),
    Check(
        "Activity 3",
        "Run `grep \"ERROR\" logs/errors.log`",
        is_grep_pattern("ERROR", "logs/errors.log", exact_flags=set()),
    ),
    Check(
        "Activity 4",
        "Run `grep -i \"warn\" logs/errors.log`",
        is_grep_pattern("warn", "logs/errors.log", exact_flags={"i"}),
    ),
    Check("Activity 5", "Run `cat logs/errors.log | grep ERROR`", is_cat_errors_grep_error_pipeline),
    Check("Activity 6", "Run `find . -name \"*.txt\" | sort`", is_find_txt_sort_pipeline),
    Check(
        "Activity 7",
        "Run `cut -d',' -f1 lab-files/search-practice/incidents.csv`",
        is_cut_incident_type,
    ),
    Check(
        "Activity 8",
        "Run `cut -d',' -f1 lab-files/search-practice/incidents.csv | sort | uniq`",
        is_cut_sort_uniq_pipeline,
    ),
)


def grade(commands: list[Command]):
    return grade_commands(commands, CHECKS)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--history-file",
        action="append",
        type=Path,
        help="History file to grade. Can be passed more than once.",
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
            "No shell history file found. Pass --history-file PATH or use the lab shell aliases.",
            file=sys.stderr,
        )
        return 2

    results = grade(load_commands(history_files))
    passed_count = sum(1 for result in results if result["passed"])
    percent = (passed_count / len(results)) * 100 if results else 0.0

    if args.json:
        print(
            json.dumps(
                {
                    "lab": LAB_ID,
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
        print_text_report(
            title=TITLE,
            results=results,
            history_files=history_files,
            pass_percent=args.pass_percent,
        )

    return 0 if percent >= args.pass_percent else 1


if __name__ == "__main__":
    raise SystemExit(main())
