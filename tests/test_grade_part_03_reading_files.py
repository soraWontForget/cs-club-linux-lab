import unittest

from scripts import grade_part_03_reading_files as grader


COMPLETE_HISTORY = """
cd /home/student/lab
cat notes.txt
less logs/app.log
head logs/app.log
tail logs/errors.log
wc notes.txt
tail -f logs/app.log
"""


class GradePartThreeTest(unittest.TestCase):
    def test_complete_history_passes_all_checks(self):
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands)

        self.assertEqual(len(results), 7)
        self.assertTrue(all(result["passed"] for result in results))

    def test_plain_tail_and_tail_follow_are_separate_checks(self):
        commands = grader.parse_history_lines(["tail -f logs/app.log"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `tail logs/errors.log`"])
        self.assertTrue(labels["Run `tail -f logs/app.log`"])

    def test_head_with_extra_flag_does_not_count_for_default_head(self):
        commands = grader.parse_history_lines(["head -n 5 logs/app.log"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `head logs/app.log`"])

    def test_trailing_slashes_do_not_affect_lab_cd(self):
        commands = grader.parse_history_lines(["cd /home/student/lab/"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Go to `/home/student/lab`"])


if __name__ == "__main__":
    unittest.main()
