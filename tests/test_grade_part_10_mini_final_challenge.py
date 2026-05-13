import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import grade_part_10_mini_final_challenge as grader


COMPLETE_HISTORY = """
cd /home/student/lab
mkdir submission
grep -i "error" logs/app.log > errors-found.txt
cp errors-found.txt errors-backup.txt
mv errors-found.txt submission/
ls -l submission/
"""


APP_LOG_TEXT = """\
2026-05-09 09:00:00 INFO  app boot requested
2026-05-09 09:02:12 ERROR failed to write temporary cache
2026-05-09 09:04:28 info  retry complete
2026-05-09 09:06:33 Error notification service timed out
2026-05-09 09:08:47 error retry queue is full
"""


EXPECTED_ERRORS = """\
2026-05-09 09:02:12 ERROR failed to write temporary cache
2026-05-09 09:06:33 Error notification service timed out
2026-05-09 09:08:47 error retry queue is full
"""


class GradePartTenTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp())
        (self.tempdir / "logs").mkdir()
        (self.tempdir / "logs" / "app.log").write_text(APP_LOG_TEXT, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def create_completed_state(self):
        submission = self.tempdir / "submission"
        submission.mkdir()
        (submission / "errors-found.txt").write_text(EXPECTED_ERRORS, encoding="utf-8")
        (self.tempdir / "errors-backup.txt").write_text(EXPECTED_ERRORS, encoding="utf-8")

    def test_complete_history_and_state_pass_all_checks(self):
        self.create_completed_state()
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands, lab_home=self.tempdir)

        self.assertEqual(len(results), 13)
        self.assertTrue(all(result["passed"] for result in results))

    def test_grep_requires_case_insensitive_flag(self):
        commands = grader.parse_history_lines(["grep error logs/app.log > errors-found.txt"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels['Run `grep -i "error" logs/app.log > errors-found.txt`'])

    def test_grep_requires_errors_found_redirection_target(self):
        commands = grader.parse_history_lines(['grep -i "error" logs/app.log > wrong-file.txt'])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels['Run `grep -i "error" logs/app.log > errors-found.txt`'])

    def test_grep_accepts_redirection_without_space(self):
        commands = grader.parse_history_lines(['grep -i "error" logs/app.log >errors-found.txt'])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels['Run `grep -i "error" logs/app.log > errors-found.txt`'])

    def test_mv_requires_submission_destination(self):
        commands = grader.parse_history_lines(["mv errors-found.txt other-folder/"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `mv errors-found.txt submission/`"])

    def test_state_checks_fail_when_errors_found_was_not_moved(self):
        self.create_completed_state()
        (self.tempdir / "errors-found.txt").write_text(EXPECTED_ERRORS, encoding="utf-8")
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands, lab_home=self.tempdir)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["`errors-found.txt` was moved out of the top level"])

    def test_state_checks_are_case_insensitive_for_expected_log_matches(self):
        submission = self.tempdir / "submission"
        submission.mkdir()
        (submission / "errors-found.txt").write_text(EXPECTED_ERRORS, encoding="utf-8")
        (self.tempdir / "errors-backup.txt").write_text(EXPECTED_ERRORS, encoding="utf-8")

        results = grader.grade([], lab_home=self.tempdir)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(
            labels["`submission/errors-found.txt` contains matching `logs/app.log` error lines"]
        )
        self.assertTrue(labels["`errors-backup.txt` contains matching `logs/app.log` error lines"])


if __name__ == "__main__":
    unittest.main()
