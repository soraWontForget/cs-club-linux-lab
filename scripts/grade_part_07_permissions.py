#!/usr/bin/env python3
"""Progress checker for Part 7: File Permissions."""

from __future__ import annotations

import argparse
import json
import os
import stat
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
        is_ls,
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
        is_ls,
        load_commands,
        parse_history_lines,
        print_text_report,
    )


LAB_ID = "part-07-file-permissions"
TITLE = "Part 7: File Permissions"
HELLO_SCRIPT = "scripts/hello.sh"
HELLO_EXECUTION = "./scripts/hello.sh"


def is_hello_execution(command: Command) -> bool:
    return command.tokens == (HELLO_EXECUTION,)


def is_chmod_plus_x_hello(command: Command) -> bool:
    return command.name == "chmod" and command.args == ("+x", HELLO_SCRIPT)


HISTORY_CHECKS: tuple[Check, ...] = (
    Check("Before You Start", "Go to `/home/student/lab`", is_cd("/home/student/lab")),
    Check("Activity 1", "Run `id`", is_command("id", exact_flags=set(), no_targets=True)),
    Check("Activity 1", "Run `groups`", is_command("groups", exact_flags=set(), no_targets=True)),
    Check(
        "Activity 2",
        "Run `ls -l scripts/hello.sh`",
        is_ls(exact_flags={"l"}, target=HELLO_SCRIPT),
    ),
    Check("Activity 3", "Run `./scripts/hello.sh`", is_hello_execution),
    Check("Activity 4", "Run `chmod +x scripts/hello.sh`", is_chmod_plus_x_hello),
)


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


def state_result(activity: str, label: str, passed: bool, path: Path) -> dict[str, object]:
    return {
        "activity": activity,
        "label": label,
        "passed": passed,
        "match": {"path": str(path)} if passed else None,
    }


def state_checks(lab_home: Path) -> list[dict[str, object]]:
    hello = lab_home / HELLO_SCRIPT
    exists = hello.is_file()
    executable = exists and bool(hello.stat().st_mode & stat.S_IXUSR)

    return [
        state_result("Final State", "`scripts/hello.sh` exists", exists, hello),
        state_result("Final State", "`scripts/hello.sh` is executable", executable, hello),
    ]


def grade(commands: list[Command], lab_home: Path | None = None):
    command_list = list(commands)
    results = grade_commands(command_list, HISTORY_CHECKS)
    results.extend(
        [
            count_result(
                activity="Activity 5",
                label="Run `ls -l scripts/hello.sh` again after `chmod`",
                commands=command_list,
                matcher=is_ls(exact_flags={"l"}, target=HELLO_SCRIPT),
                required_count=2,
            ),
            count_result(
                activity="Activity 6",
                label="Run `./scripts/hello.sh` again after `chmod`",
                commands=command_list,
                matcher=is_hello_execution,
                required_count=2,
            ),
        ]
    )
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
