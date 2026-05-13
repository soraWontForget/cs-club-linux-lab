import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import grade_part_07_permissions as grader


COMPLETE_HISTORY = """
cd /home/student/lab
id
groups
ls -l scripts/hello.sh
./scripts/hello.sh
chmod +x scripts/hello.sh
ls -l scripts/hello.sh
./scripts/hello.sh
"""


class GradePartSevenTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp())
        scripts = self.tempdir / "scripts"
        scripts.mkdir()
        self.hello = scripts / "hello.sh"
        self.hello.write_text("#!/usr/bin/env bash\necho hello\n", encoding="utf-8")
        self.hello.chmod(0o644)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def make_hello_executable(self):
        self.hello.chmod(0o755)

    def test_complete_history_and_state_pass_all_checks(self):
        self.make_hello_executable()
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands, lab_home=self.tempdir)

        self.assertEqual(len(results), 10)
        self.assertTrue(all(result["passed"] for result in results))

    def test_chmod_requires_plus_x_and_target_script(self):
        commands = grader.parse_history_lines(["chmod 755 scripts/hello.sh"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `chmod +x scripts/hello.sh`"])

    def test_single_ls_does_not_pass_after_chmod_check(self):
        commands = grader.parse_history_lines(["ls -l scripts/hello.sh"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `ls -l scripts/hello.sh`"])
        self.assertFalse(labels["Run `ls -l scripts/hello.sh` again after `chmod`"])

    def test_single_script_run_does_not_pass_after_chmod_check(self):
        commands = grader.parse_history_lines(["./scripts/hello.sh"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `./scripts/hello.sh`"])
        self.assertFalse(labels["Run `./scripts/hello.sh` again after `chmod`"])

    def test_script_execution_requires_relative_path(self):
        commands = grader.parse_history_lines(["hello.sh"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `./scripts/hello.sh`"])

    def test_state_check_fails_when_script_is_not_executable(self):
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands, lab_home=self.tempdir)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["`scripts/hello.sh` exists"])
        self.assertFalse(labels["`scripts/hello.sh` is executable"])


if __name__ == "__main__":
    unittest.main()
