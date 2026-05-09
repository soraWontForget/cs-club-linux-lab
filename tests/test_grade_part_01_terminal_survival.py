import unittest

from scripts import grade_part_01_terminal_survival as grader


COMPLETE_HISTORY = """
cd linux-basics-lab
pwd
ls
ls lab-files
ls lab-files/campus
ls lab-files/campus/clubs
ls lab-files/campus/classes
ls -l
ls -a
ls -la
ls -lh lab-files/campus/classes
pwd
ls
date
clear
whoami
hostname
date
history
ls --help
date --help
whoami --help
man ls
"""


class GradePartOneTest(unittest.TestCase):
    def test_complete_history_passes_all_checks(self):
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands)

        self.assertEqual(len(results), 19)
        self.assertTrue(all(result["passed"] for result in results))

    def test_zsh_extended_history_is_supported(self):
        commands = grader.parse_history_lines([": 1715288458:0;ls -al"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `ls -la` or `ls -al`"])
        self.assertFalse(labels["Run `ls -l`"])
        self.assertFalse(labels["Run `ls -a`"])

    def test_combined_command_lines_are_split(self):
        commands = grader.parse_history_lines(["pwd && whoami; hostname"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `pwd`"])
        self.assertTrue(labels["Run `whoami`"])
        self.assertTrue(labels["Run `hostname`"])

    def test_plain_date_and_date_help_are_separate_checks(self):
        commands = grader.parse_history_lines(["date --help"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `date`"])
        self.assertTrue(labels["Run `date --help`"])

    def test_ls_help_does_not_count_as_bare_ls(self):
        commands = grader.parse_history_lines(["ls --help"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run bare `ls`"])
        self.assertTrue(labels["Run `ls --help`"])


if __name__ == "__main__":
    unittest.main()
