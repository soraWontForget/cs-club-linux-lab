import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import grade_part_06_redirection_pipes as grader


COMPLETE_HISTORY = """
cd /home/student/lab
mkdir -p practice/part6
date > practice/part6/report.txt
whoami >> practice/part6/report.txt
hostname >> practice/part6/report.txt
echo "New report" > practice/part6/report.txt
wc -l < logs/errors.log
wc -l logs/errors.log
grep "ERROR" logs/errors.log | wc -l
grep "ERROR" logs/errors.log | sort > practice/part6/errors-only.txt
grep "WARN" logs/errors.log | tee practice/part6/warnings.txt
ls missing-file 2> practice/part6/error-message.txt
"""


ERRORS_LOG_TEXT = """\
2026-05-09 09:02:44 WARN  command typo detected: sl
2026-05-09 09:03:01 ERROR missing file requested: missing.txt
2026-05-09 09:04:17 WARN  hidden file not visible without -a
2026-05-09 09:05:33 ERROR manual page exited without q key note
"""


class GradePartSixTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp())
        (self.tempdir / "logs").mkdir()
        (self.tempdir / "logs" / "errors.log").write_text(ERRORS_LOG_TEXT, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def create_completed_state(self):
        practice = self.tempdir / "practice" / "part6"
        practice.mkdir(parents=True)
        (practice / "report.txt").write_text("New report\n", encoding="utf-8")
        (practice / "errors-only.txt").write_text(
            "\n".join(sorted(line for line in ERRORS_LOG_TEXT.splitlines() if "ERROR" in line)) + "\n",
            encoding="utf-8",
        )
        (practice / "warnings.txt").write_text(
            "\n".join(line for line in ERRORS_LOG_TEXT.splitlines() if "WARN" in line) + "\n",
            encoding="utf-8",
        )
        (practice / "error-message.txt").write_text(
            "ls: cannot access 'missing-file': No such file or directory\n",
            encoding="utf-8",
        )

    def test_complete_history_and_state_pass_all_checks(self):
        self.create_completed_state()
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands, lab_home=self.tempdir)

        self.assertEqual(len(results), 18)
        self.assertTrue(all(result["passed"] for result in results))

    def test_overwrite_and_append_are_separate_checks(self):
        commands = grader.parse_history_lines(
            [
                "date >> practice/part6/report.txt",
                "whoami > practice/part6/report.txt",
            ]
        )
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `date > practice/part6/report.txt`"])
        self.assertFalse(labels["Run `whoami >> practice/part6/report.txt`"])

    def test_echo_overwrite_accepts_unquoted_words(self):
        commands = grader.parse_history_lines(["echo New report > practice/part6/report.txt"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `echo \"New report\" > practice/part6/report.txt`"])

    def test_input_redirection_requires_less_than_operator(self):
        commands = grader.parse_history_lines(["wc -l logs/errors.log"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `wc -l < logs/errors.log`"])
        self.assertTrue(labels["Run `wc -l logs/errors.log`"])

    def test_input_redirection_does_not_count_as_file_argument_version(self):
        commands = grader.parse_history_lines(["wc -l < logs/errors.log"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `wc -l < logs/errors.log`"])
        self.assertFalse(labels["Run `wc -l logs/errors.log`"])

    def test_count_error_lines_requires_pipeline(self):
        commands = grader.parse_history_lines(['grep "ERROR" logs/errors.log; wc -l'])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels['Run `grep "ERROR" logs/errors.log | wc -l`'])

    def test_saved_error_pipeline_requires_redirection_target(self):
        commands = grader.parse_history_lines(['grep "ERROR" logs/errors.log | sort'])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(
            labels['Run `grep "ERROR" logs/errors.log | sort > practice/part6/errors-only.txt`']
        )

    def test_tee_pipeline_requires_tee(self):
        commands = grader.parse_history_lines(['grep "WARN" logs/errors.log > practice/part6/warnings.txt'])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels['Run `grep "WARN" logs/errors.log | tee practice/part6/warnings.txt`'])

    def test_error_redirect_requires_stderr_operator(self):
        commands = grader.parse_history_lines(["ls missing-file > practice/part6/error-message.txt"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `ls missing-file 2> practice/part6/error-message.txt`"])

    def test_redirection_parser_accepts_no_space_before_target(self):
        commands = grader.parse_history_lines(
            [
                "date >practice/part6/report.txt",
                "whoami >>practice/part6/report.txt",
                "wc -l <logs/errors.log",
                "ls missing-file 2>practice/part6/error-message.txt",
            ]
        )
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `date > practice/part6/report.txt`"])
        self.assertTrue(labels["Run `whoami >> practice/part6/report.txt`"])
        self.assertTrue(labels["Run `wc -l < logs/errors.log`"])
        self.assertTrue(labels["Run `ls missing-file 2> practice/part6/error-message.txt`"])


if __name__ == "__main__":
    unittest.main()
