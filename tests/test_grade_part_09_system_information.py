import unittest

from scripts import grade_part_09_system_information as grader


COMPLETE_HISTORY = """
cd /home/student/lab
uname
df
du
free
uptime
env
echo $PATH
"""


class GradePartNineTest(unittest.TestCase):
    def test_complete_history_passes_all_checks(self):
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands)

        self.assertEqual(len(results), 8)
        self.assertTrue(all(result["passed"] for result in results))

    def test_commands_require_bare_versions(self):
        commands = grader.parse_history_lines(
            [
                "uname -a",
                "df -h",
                "du -sh .",
                "free -h",
                "uptime -p",
                "env PATH=/tmp",
            ]
        )
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `uname`"])
        self.assertFalse(labels["Run `df`"])
        self.assertFalse(labels["Run `du`"])
        self.assertFalse(labels["Run `free`"])
        self.assertFalse(labels["Run `uptime`"])
        self.assertFalse(labels["Run `env`"])

    def test_echo_path_accepts_braced_variable(self):
        commands = grader.parse_history_lines(["echo ${PATH}"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `echo $PATH`"])

    def test_echo_path_rejects_other_variables(self):
        commands = grader.parse_history_lines(["echo $HOME"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `echo $PATH`"])


if __name__ == "__main__":
    unittest.main()
