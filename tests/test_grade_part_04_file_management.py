import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import grade_part_04_file_management as grader


COMPLETE_HISTORY = """
cd /home/student/lab
mkdir practice
touch practice/file1.txt
cp notes.txt practice/notes-copy.txt
mv practice/file1.txt practice/renamed.txt
rm -i practice/renamed.txt
mkdir practice/empty-folder
rmdir practice/empty-folder
mkdir practice/remove-me
touch practice/remove-me/temp.txt
rm -r practice/remove-me
"""


class GradePartFourTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp())
        (self.tempdir / "notes.txt").write_text("practice notes\n", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def create_completed_state(self):
        practice = self.tempdir / "practice"
        practice.mkdir()
        shutil.copyfile(self.tempdir / "notes.txt", practice / "notes-copy.txt")

    def test_complete_history_and_state_pass_all_checks(self):
        self.create_completed_state()
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands, lab_home=self.tempdir)

        self.assertEqual(len(results), 18)
        self.assertTrue(all(result["passed"] for result in results))

    def test_cp_requires_exact_source_and_destination(self):
        commands = grader.parse_history_lines(["cp notes.txt practice/wrong-name.txt"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `cp notes.txt practice/notes-copy.txt`"])

    def test_mv_requires_exact_old_and_new_names(self):
        commands = grader.parse_history_lines(["mv practice/file1.txt practice/other.txt"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `mv practice/file1.txt practice/renamed.txt`"])

    def test_rm_interactive_and_recursive_are_separate_checks(self):
        commands = grader.parse_history_lines(["rm -r practice/remove-me"])
        results = grader.grade(commands, lab_home=None)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `rm -i practice/renamed.txt`"])
        self.assertTrue(labels["Run `rm -r practice/remove-me`"])

    def test_state_checks_fail_when_copy_is_missing(self):
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands, lab_home=self.tempdir)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["`practice/` exists"])
        self.assertFalse(labels["`practice/notes-copy.txt` exists"])
        self.assertFalse(labels["`practice/notes-copy.txt` matches `notes.txt`"])


if __name__ == "__main__":
    unittest.main()
