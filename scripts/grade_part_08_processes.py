#!/usr/bin/env python3
"""Progress checker for Part 8: Processes and Jobs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable

try:
    from .history_grader import (
        Check,
        Command,
        discover_history_files,
        grade as grade_commands,
        is_cd,
        is_command,
        is_simple,
        load_commands,
        parse_history_lines,
        print_text_report,
    )
except ImportError:
    from history_grader import (
        Check,
        Command,
        discover_history_files,
        grade as grade_commands,
        is_cd,
        is_command,
        is_simple,
        load_commands,
        parse_history_lines,
        print_text_report,
    )


LAB_ID = "part-08-processes"
TITLE = "Part 8: Processes and Jobs"


def is_foreground_sleep_100(command: Command) -> bool:
    return command.name == "sleep" and command.args == ("100",)


def is_background_sleep_100(command: Command) -> bool:
    if command.name != "sleep":
        return False

    if command.args == ("100", "&"):
        return True

    if command.args == ("100&",):
        return True

    return False


def is_job_spec(arg: str) -> bool:
    if arg in {"%+", "%-"}:
        return True

    if arg.startswith("%"):
        return arg[1:].isdigit()

    return arg.isdigit()


def is_job_control(command_name: str) -> Callable[[Command], bool]:
    def matcher(command: Command) -> bool:
        if command.name != command_name:
            return False

        if not command.args:
            return True

        return len(command.args) == 1 and is_job_spec(command.args[0])

    return matcher


def is_numeric_pid(arg: str) -> bool:
    return arg.isdigit() and int(arg) > 0


def is_kill_numeric_pid(command: Command) -> bool:
    return command.name == "kill" and len(command.args) == 1 and is_numeric_pid(command.args[0])


def count_result(
    *,
    activity: str,
    label: str,
    commands: list[Command],
    matcher: Callable[[Command], bool],
    required_count: int,
) -> dict[str, object]:
    matches = [command for command in commands if matcher(command)]
    first_match = matches[0] if matches else None
    passed = len(matches) >= required_count

    return {
        "activity": activity,
        "label": label,
        "passed": passed,
        "match": {
            "command": first_match.raw,
            "source": first_match.source,
            "line": first_match.line_number,
            "count": len(matches),
        }
        if passed and first_match
        else None,
    }


CHECKS: tuple[Check, ...] = (
    Check("Before You Start", "Go to `/home/student/lab`", is_cd("/home/student/lab")),
    Check("Activity 1", "Run `ps`", is_command("ps", exact_flags=set(), no_targets=True)),
    Check("Activity 2", "Run `top`", is_simple("top")),
    Check("Activity 3", "Run `sleep 100`", is_foreground_sleep_100),
    Check("Activity 3", "Run `jobs` after pressing `Ctrl-Z`", is_simple("jobs")),
    Check("Activity 4", "Run `bg`", is_job_control("bg")),
    Check("Activity 5", "Run `fg`", is_job_control("fg")),
    Check("Activity 6", "Run `sleep 100 &`", is_background_sleep_100),
    Check("Activity 7", "Run `kill PID` with the numeric sleep PID", is_kill_numeric_pid),
)


def grade(commands):
    command_list = list(commands)
    results = grade_commands(command_list, CHECKS)
    results.extend(
        [
            count_result(
                activity="Activity 4",
                label="Run `jobs` again after `bg`",
                commands=command_list,
                matcher=is_simple("jobs"),
                required_count=2,
            ),
            count_result(
                activity="Activity 6",
                label="Run `jobs` after starting `sleep 100 &`",
                commands=command_list,
                matcher=is_simple("jobs"),
                required_count=3,
            ),
            count_result(
                activity="Activity 7",
                label="Run `ps` again to find the sleep PID",
                commands=command_list,
                matcher=is_command("ps", exact_flags=set(), no_targets=True),
                required_count=2,
            ),
            count_result(
                activity="Activity 7",
                label="Run `jobs` after `kill PID`",
                commands=command_list,
                matcher=is_simple("jobs"),
                required_count=4,
            ),
        ]
    )
    return results


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
