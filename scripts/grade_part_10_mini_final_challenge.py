#!/usr/bin/env python3
"""Progress checker for Part 10: Mini Final Challenge."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from .grade_part_06_redirection_pipes import args_before_redirection, has_redirection
    from .history_grader import (
        Check,
        Command,
        discover_history_files,
        grade as grade_commands,
        is_cd,
        is_command,
        is_command_positions,
        load_commands,
        option_profile,
        parse_history_lines,
        positional_args,
        print_text_report,
    )
except ImportError:
    from grade_part_06_redirection_pipes import args_before_redirection, has_redirection
    from history_grader import (
        Check,
        Command,
        discover_history_files,
        grade as grade_commands,
        is_cd,
        is_command,
        is_command_positions,
        load_commands,
        option_profile,
        parse_history_lines,
        positional_args,
        print_text_report,
    )


LAB_ID = "part-10-mini-final-challenge"
TITLE = "Part 10: Mini Final Challenge"

APP_LOG = "logs/app.log"
SUBMISSION_DIR = "submission"
ERRORS_FOUND_FILE = "errors-found.txt"
ERRORS_BACKUP_FILE = "errors-backup.txt"
SUBMITTED_ERRORS_FILE = "submission/errors-found.txt"


def is_grep_error_to_file(command: Command) -> bool:
    if command.name != "grep" or not has_redirection(command, ">", ERRORS_FOUND_FILE):
        return False

    grep_args = args_before_redirection(command.args)
    grep_command = Command(
        raw=" ".join((command.tokens[0], *grep_args)),
        tokens=(command.tokens[0], *grep_args),
        source=command.source,
        line_number=command.line_number,
    )
    letters, unknown_option = option_profile(grep_command)
    if unknown_option or letters != {"i"}:
        return False

    positions = positional_args(grep_command)
    return len(positions) == 2 and positions[0].lower() == "error" and positions[1] == APP_LOG


HISTORY_CHECKS: tuple[Check, ...] = (
    Check("Before You Start", "Go to `/home/student/lab`", is_cd("/home/student/lab")),
    Check(
        "Challenge",
        "Run `mkdir submission`",
        is_command("mkdir", exact_flags=set(), target=SUBMISSION_DIR),
    ),
    Check(
        "Challenge",
        'Run `grep -i "error" logs/app.log > errors-found.txt`',
        is_grep_error_to_file,
    ),
    Check(
        "Challenge",
        "Run `cp errors-found.txt errors-backup.txt`",
        is_command_positions("cp", [ERRORS_FOUND_FILE, ERRORS_BACKUP_FILE], exact_flags=set()),
    ),
    Check(
        "Challenge",
        "Run `mv errors-found.txt submission/`",
        is_command_positions("mv", [ERRORS_FOUND_FILE, SUBMISSION_DIR], exact_flags=set()),
    ),
    Check(
        "Challenge",
        "Run `ls -l submission/`",
        is_command("ls", exact_flags={"l"}, target=SUBMISSION_DIR),
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


def expected_error_text(app_log: Path) -> str:
    log_lines = read_text(app_log).splitlines()
    matching_lines = [line for line in log_lines if "error" in line.lower()]
    if not matching_lines:
        return ""
    return "\n".join(matching_lines) + "\n"


def state_checks(lab_home: Path) -> list[dict[str, object]]:
    submission_dir = lab_home / SUBMISSION_DIR
    root_errors_found = lab_home / ERRORS_FOUND_FILE
    backup_file = lab_home / ERRORS_BACKUP_FILE
    submitted_file = lab_home / SUBMITTED_ERRORS_FILE
    expected_text = expected_error_text(lab_home / APP_LOG)
    backup_text = read_text(backup_file)
    submitted_text = read_text(submitted_file)

    return [
        state_result("Final State", "`submission/` exists", submission_dir.is_dir(), submission_dir),
        state_result(
            "Final State",
            "`submission/errors-found.txt` exists",
            submitted_file.is_file(),
            submitted_file,
        ),
        state_result(
            "Final State",
            "`errors-found.txt` was moved out of the top level",
            not root_errors_found.exists(),
            root_errors_found,
        ),
        state_result(
            "Final State",
            "`errors-backup.txt` exists",
            backup_file.is_file(),
            backup_file,
        ),
        state_result(
            "Final State",
            "`submission/errors-found.txt` contains matching `logs/app.log` error lines",
            bool(expected_text) and submitted_file.is_file() and submitted_text == expected_text,
            submitted_file,
        ),
        state_result(
            "Final State",
            "`errors-backup.txt` contains matching `logs/app.log` error lines",
            bool(expected_text) and backup_file.is_file() and backup_text == expected_text,
            backup_file,
        ),
        state_result(
            "Final State",
            "The submitted file and backup match",
            submitted_file.is_file() and backup_file.is_file() and submitted_text == backup_text,
            submitted_file,
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
