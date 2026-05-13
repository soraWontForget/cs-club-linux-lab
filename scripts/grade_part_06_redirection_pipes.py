#!/usr/bin/env python3
"""Progress checker for Part 6: Redirection and Pipelines."""

from __future__ import annotations

import argparse
import json
import os
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
        load_commands,
        option_profile,
        parse_history_lines,
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
        load_commands,
        option_profile,
        parse_history_lines,
        print_text_report,
        split_shell_segments,
        tokenize,
    )


LAB_ID = "part-06-redirection-pipes"
TITLE = "Part 6: Redirection and Pipelines"

PRACTICE_DIR = "practice/part6"
REPORT_FILE = "practice/part6/report.txt"
ERRORS_ONLY_FILE = "practice/part6/errors-only.txt"
WARNINGS_FILE = "practice/part6/warnings.txt"
ERROR_MESSAGE_FILE = "practice/part6/error-message.txt"
ERRORS_LOG = "logs/errors.log"


def command_name(tokens: Iterable[str]) -> str:
    tokens = tuple(tokens)
    if not tokens:
        return ""
    return Path(tokens[0]).name


def token_args(tokens: Iterable[str]) -> tuple[str, ...]:
    tokens = tuple(tokens)
    return tokens[1:]


def args_before_redirection(args: Iterable[str]) -> tuple[str, ...]:
    result: list[str] = []
    for arg in args:
        if arg in {">", ">>", "<", "2>", "2>>"}:
            break
        if arg.startswith(">") or arg.startswith(">>") or arg.startswith("<") or arg.startswith("2>"):
            break
        result.append(arg)
    return tuple(result)


def tokens_have_flag(tokens: Iterable[str], flag: str) -> bool:
    command = Command(
        raw=" ".join(tokens),
        tokens=tuple(tokens),
        source="<pipeline>",
        line_number=0,
    )
    letters, unknown_option = option_profile(command)
    return not unknown_option and flag in letters


def read_redirection_target(command_line: str, start: int) -> tuple[str, int]:
    while start < len(command_line) and command_line[start].isspace():
        start += 1

    chars: list[str] = []
    quote: str | None = None
    escaped = False
    index = start

    while index < len(command_line):
        char = command_line[index]

        if escaped:
            chars.append(char)
            escaped = False
            index += 1
            continue

        if char == "\\":
            chars.append(char)
            escaped = True
            index += 1
            continue

        if quote:
            chars.append(char)
            if char == quote:
                quote = None
            index += 1
            continue

        if char in {"'", '"'}:
            quote = char
            chars.append(char)
            index += 1
            continue

        if char.isspace() or char in {"|", ";", "&"}:
            break

        chars.append(char)
        index += 1

    raw_target = "".join(chars)
    target_tokens = tokenize(raw_target)
    target = target_tokens[0] if target_tokens else raw_target
    return target, index


def redirections(command_line: str) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    quote: str | None = None
    escaped = False
    index = 0

    while index < len(command_line):
        char = command_line[index]

        if escaped:
            escaped = False
            index += 1
            continue

        if char == "\\":
            escaped = True
            index += 1
            continue

        if quote:
            if char == quote:
                quote = None
            index += 1
            continue

        if char in {"'", '"'}:
            quote = char
            index += 1
            continue

        operator = ""
        if command_line.startswith("2>>", index):
            operator = "2>>"
        elif command_line.startswith("2>", index):
            operator = "2>"
        elif command_line.startswith(">>", index):
            operator = ">>"
        elif char == ">":
            operator = ">"
        elif char == "<":
            operator = "<"

        if operator:
            target, next_index = read_redirection_target(command_line, index + len(operator))
            results.append((operator, target))
            index = max(next_index, index + len(operator))
            continue

        index += 1

    return results


def has_redirection(command: Command, operator: str, target: str) -> bool:
    return (operator, target) in redirections(command.history_line)


def pipeline_tokens(command: Command) -> list[tuple[str, ...]]:
    if "|" not in command.history_line:
        return []
    return [tokenize(segment) for segment in split_shell_segments(command.history_line)]


def is_mkdir_practice_part6(command: Command) -> bool:
    return command.name == "mkdir" and command.args == ("-p", PRACTICE_DIR)


def is_date_to_report(command: Command) -> bool:
    return command.name == "date" and has_redirection(command, ">", REPORT_FILE)


def is_whoami_append_report(command: Command) -> bool:
    return command.name == "whoami" and has_redirection(command, ">>", REPORT_FILE)


def is_hostname_append_report(command: Command) -> bool:
    return command.name == "hostname" and has_redirection(command, ">>", REPORT_FILE)


def is_echo_new_report(command: Command) -> bool:
    if command.name != "echo" or not has_redirection(command, ">", REPORT_FILE):
        return False
    echo_args = args_before_redirection(command.args)
    return echo_args in {("New report",), ("New", "report")}


def is_wc_input_redirect(command: Command) -> bool:
    if command.name != "wc" or not has_redirection(command, "<", ERRORS_LOG):
        return False

    letters, unknown_option = option_profile(command)
    return not unknown_option and letters == {"l"}


def is_wc_lines_file(command: Command) -> bool:
    if command.name != "wc" or command.args != ("-l", ERRORS_LOG):
        return False

    letters, unknown_option = option_profile(command)
    return not unknown_option and letters == {"l"}


def is_grep_error_wc_pipeline(command: Command) -> bool:
    segments = pipeline_tokens(command)
    for index in range(len(segments) - 1):
        left = segments[index]
        right = segments[index + 1]
        if command_name(left) == "grep" and token_args(left) == ("ERROR", ERRORS_LOG):
            if command_name(right) == "wc" and tokens_have_flag(right, "l"):
                return True
    return False


def is_grep_error_sort_to_file(command: Command) -> bool:
    if not has_redirection(command, ">", ERRORS_ONLY_FILE):
        return False

    segments = pipeline_tokens(command)
    for index in range(len(segments) - 1):
        left = segments[index]
        right = segments[index + 1]
        if command_name(left) == "grep" and token_args(left) == ("ERROR", ERRORS_LOG):
            if command_name(right) == "sort":
                return True
    return False


def is_grep_warn_tee_pipeline(command: Command) -> bool:
    segments = pipeline_tokens(command)
    for index in range(len(segments) - 1):
        left = segments[index]
        right = segments[index + 1]
        if command_name(left) == "grep" and token_args(left) == ("WARN", ERRORS_LOG):
            if command_name(right) == "tee" and WARNINGS_FILE in token_args(right):
                return True
    return False


def is_ls_error_redirect(command: Command) -> bool:
    return (
        command.name == "ls"
        and "missing-file" in command.args
        and has_redirection(command, "2>", ERROR_MESSAGE_FILE)
    )


HISTORY_CHECKS: tuple[Check, ...] = (
    Check("Before You Start", "Go to `/home/student/lab`", is_cd("/home/student/lab")),
    Check("Activity 1", "Run `mkdir -p practice/part6`", is_mkdir_practice_part6),
    Check("Activity 2", "Run `date > practice/part6/report.txt`", is_date_to_report),
    Check("Activity 3", "Run `whoami >> practice/part6/report.txt`", is_whoami_append_report),
    Check("Activity 3", "Run `hostname >> practice/part6/report.txt`", is_hostname_append_report),
    Check("Activity 4", "Run `echo \"New report\" > practice/part6/report.txt`", is_echo_new_report),
    Check("Activity 5", "Run `wc -l < logs/errors.log`", is_wc_input_redirect),
    Check("Activity 5", "Run `wc -l logs/errors.log`", is_wc_lines_file),
    Check("Activity 6", "Run `grep \"ERROR\" logs/errors.log | wc -l`", is_grep_error_wc_pipeline),
    Check(
        "Activity 7",
        "Run `grep \"ERROR\" logs/errors.log | sort > practice/part6/errors-only.txt`",
        is_grep_error_sort_to_file,
    ),
    Check(
        "Activity 8",
        "Run `grep \"WARN\" logs/errors.log | tee practice/part6/warnings.txt`",
        is_grep_warn_tee_pipeline,
    ),
    Check(
        "Activity 9",
        "Run `ls missing-file 2> practice/part6/error-message.txt`",
        is_ls_error_redirect,
    ),
)


def state_result(activity: str, label: str, passed: bool, path: Path) -> dict[str, object]:
    return {
        "activity": activity,
        "label": label,
        "passed": passed,
        "match": {"path": str(path)} if passed else None,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def state_checks(lab_home: Path) -> list[dict[str, object]]:
    practice_dir = lab_home / PRACTICE_DIR
    report_file = lab_home / REPORT_FILE
    errors_only_file = lab_home / ERRORS_ONLY_FILE
    warnings_file = lab_home / WARNINGS_FILE
    error_message_file = lab_home / ERROR_MESSAGE_FILE
    errors_log = lab_home / ERRORS_LOG

    log_lines = read_text(errors_log).splitlines()
    expected_errors = "\n".join(sorted(line for line in log_lines if "ERROR" in line))
    if expected_errors:
        expected_errors += "\n"
    expected_warnings = "\n".join(line for line in log_lines if "WARN" in line)
    if expected_warnings:
        expected_warnings += "\n"

    report_text = read_text(report_file)
    errors_only_text = read_text(errors_only_file)
    warnings_text = read_text(warnings_file)
    error_message_text = read_text(error_message_file)

    return [
        state_result("Final State", "`practice/part6/` exists", practice_dir.is_dir(), practice_dir),
        state_result("Final State", "`practice/part6/report.txt` exists", report_file.is_file(), report_file),
        state_result(
            "Final State",
            "`practice/part6/report.txt` was overwritten with `New report`",
            report_text == "New report\n",
            report_file,
        ),
        state_result(
            "Final State",
            "`practice/part6/errors-only.txt` contains sorted `ERROR` lines",
            errors_only_file.is_file() and errors_only_text == expected_errors,
            errors_only_file,
        ),
        state_result(
            "Final State",
            "`practice/part6/warnings.txt` contains `WARN` lines",
            warnings_file.is_file() and warnings_text == expected_warnings,
            warnings_file,
        ),
        state_result(
            "Final State",
            "`practice/part6/error-message.txt` captured the missing-file error",
            "missing-file" in error_message_text,
            error_message_file,
        ),
    ]


def grade(commands: list[Command], lab_home: Path | None = None):
    results = grade_commands(commands, HISTORY_CHECKS)
    if lab_home is not None:
        results.extend(state_checks(lab_home))
    return results


def default_lab_home() -> Path:
    return Path(os.environ.get("LAB_HOME", os.getcwd())).expanduser()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--history-file",
        action="append",
        type=Path,
        help="History file to grade. Can be passed more than once.",
    )
    parser.add_argument(
        "--lab-home",
        type=Path,
        default=default_lab_home(),
        help="Lab directory to inspect for final file state. Default: LAB_HOME or current directory.",
    )
    parser.add_argument(
        "--history-only",
        action="store_true",
        help="Skip final filesystem state checks.",
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

    lab_home = None if args.history_only else args.lab_home.expanduser()
    results = grade(load_commands(history_files), lab_home=lab_home)
    passed_count = sum(1 for result in results if result["passed"])
    percent = (passed_count / len(results)) * 100 if results else 0.0

    if args.json:
        print(
            json.dumps(
                {
                    "lab": LAB_ID,
                    "history_files": [str(path.expanduser()) for path in history_files],
                    "lab_home": str(lab_home) if lab_home else None,
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
