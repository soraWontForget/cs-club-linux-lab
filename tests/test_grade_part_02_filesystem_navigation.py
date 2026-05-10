import unittest

from scripts import grade_part_02_filesystem_navigation as grader


COMPLETE_HISTORY = """
cd /home/student/lab
pwd
ls
ls -l
ls -a
ls -la
cd logs
pwd
ls
ls -la
cd ..
pwd
ls
cd ~
pwd
ls
cd ~/lab
pwd
ls .
ls ..
cd ./logs
pwd
cd ..
pwd
tree
tree logs
"""


class GradePartTwoTest(unittest.TestCase):
    def test_complete_history_passes_all_checks(self):
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands)

        self.assertEqual(len(results), 15)
        self.assertTrue(all(result["passed"] for result in results))

    def test_trailing_slashes_are_accepted_for_cd_targets(self):
        commands = grader.parse_history_lines(["cd /home/student/lab/", "cd logs/", "cd ./logs/"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Go to `/home/student/lab`"])
        self.assertTrue(labels["Move into `logs`"])
        self.assertTrue(labels["Move with `cd ./logs`"])

    def test_ls_flag_checks_are_exact(self):
        commands = grader.parse_history_lines(["ls -al"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `ls -la` or `ls -al`"])
        self.assertFalse(labels["Run `ls -l`"])
        self.assertFalse(labels["Run `ls -a`"])

    def test_tree_logs_does_not_count_as_bare_tree(self):
        commands = grader.parse_history_lines(["tree logs"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run bare `tree`"])
        self.assertTrue(labels["Run `tree logs`"])


if __name__ == "__main__":
    unittest.main()
