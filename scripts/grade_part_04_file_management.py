#!/usr/bin/env python3
"""Progress checker for Part 4: Creating, Copying, Moving, and Deleting."""

from __future__ import annotations

import argparse
import json
import os
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
        is_command_positions,
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
        is_command_positions,
        load_commands,
        parse_history_lines,
        print_text_report,
    )


LAB_ID = "part-04-file-management"
TITLE = "Part 4: Creating, Copying, Moving, and Deleting"

HISTORY_CHECKS: tuple[Check, ...] = (
    Check("Before You Start", "Go to `/home/student/lab`", is_cd("/home/student/lab")),
    Check("Activity 1", "Run `mkdir practice`", is_command("mkdir", exact_flags=set(), target="practice")),
    Check("Activity 2", "Run `touch practice/file1.txt`", is_command("touch", exact_flags=set(), target="practice/file1.txt")),
    Check(
        "Activity 3",
        "Run `cp notes.txt practice/notes-copy.txt`",
        is_command_positions("cp", ["notes.txt", "practice/notes-copy.txt"], exact_flags=set()),
    ),
    Check(
        "Activity 4",
        "Run `mv practice/file1.txt practice/renamed.txt`",
        is_command_positions("mv", ["practice/file1.txt", "practice/renamed.txt"], exact_flags=set()),
    ),
    Check(
        "Activity 5",
        "Run `rm -i practice/renamed.txt`",
        is_command("rm", exact_flags={"i"}, target="practice/renamed.txt"),
    ),
    Check("Activity 6", "Run `mkdir practice/empty-folder`", is_command("mkdir", exact_flags=set(), target="practice/empty-folder")),
    Check("Activity 6", "Run `rmdir practice/empty-folder`", is_command("rmdir", exact_flags=set(), target="practice/empty-folder")),
    Check("Activity 7", "Run `mkdir practice/remove-me`", is_command("mkdir", exact_flags=set(), target="practice/remove-me")),
    Check("Activity 7", "Run `touch practice/remove-me/temp.txt`", is_command("touch", exact_flags=set(), target="practice/remove-me/temp.txt")),
    Check(
        "Activity 7",
        "Run `rm -r practice/remove-me`",
        is_command("rm", exact_flags={"r"}, target="practice/remove-me"),
    ),
)


def state_result(activity: str, label: str, passed: bool, path: Path) -> dict[str, object]:
    return {
        "activity": activity,
        "label": label,
        "passed": passed,
        "match": {"path": str(path)} if passed else None,
    }


def state_checks(lab_home: Path) -> list[dict[str, object]]:
    practice = lab_home / "practice"
    notes = lab_home / "notes.txt"
    notes_copy = practice / "notes-copy.txt"
    renamed = practice / "renamed.txt"
    original = practice / "file1.txt"
    empty_folder = practice / "empty-folder"
    remove_me = practice / "remove-me"

    results = [
        state_result("Final State", "`practice/` exists", practice.is_dir(), practice),
        state_result("Final State", "`practice/notes-copy.txt` exists", notes_copy.is_file(), notes_copy),
        state_result("Final State", "`practice/file1.txt` was renamed", not original.exists(), original),
        state_result("Final State", "`practice/renamed.txt` was removed", not renamed.exists(), renamed),
        state_result("Final State", "`practice/empty-folder` was removed with `rmdir`", not empty_folder.exists(), empty_folder),
        state_result("Final State", "`practice/remove-me` was removed with `rm -r`", not remove_me.exists(), remove_me),
    ]

    content_matches = notes.is_file() and notes_copy.is_file() and notes.read_bytes() == notes_copy.read_bytes()
    results.append(
        state_result(
            "Final State",
            "`practice/notes-copy.txt` matches `notes.txt`",
            content_matches,
            notes_copy,
        )
    )

    return results


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
