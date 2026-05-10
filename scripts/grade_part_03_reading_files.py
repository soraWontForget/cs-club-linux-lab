#!/usr/bin/env python3
"""Progress checker for Part 3: Reading Files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from .history_grader import (
        Check,
        Command,
        discover_history_files,
        grade as grade_commands,
        is_cd,
        is_command,
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
        load_commands,
        parse_history_lines,
        print_text_report,
    )


LAB_ID = "part-03-reading-files"
TITLE = "Part 3: Reading Files"

CHECKS: tuple[Check, ...] = (
    Check("Before You Start", "Go to `/home/student/lab`", is_cd("/home/student/lab")),
    Check("Activity 1", "Run `cat notes.txt`", is_command("cat", exact_flags=set(), target="notes.txt")),
    Check("Activity 2", "Run `less logs/app.log`", is_command("less", exact_flags=set(), target="logs/app.log")),
    Check("Activity 3", "Run `head logs/app.log`", is_command("head", exact_flags=set(), target="logs/app.log")),
    Check("Activity 4", "Run `tail logs/errors.log`", is_command("tail", exact_flags=set(), target="logs/errors.log")),
    Check("Activity 5", "Run `wc notes.txt`", is_command("wc", exact_flags=set(), target="notes.txt")),
    Check("Activity 6", "Run `tail -f logs/app.log`", is_command("tail", exact_flags={"f"}, target="logs/app.log")),
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
