import unittest

from scripts import grade_part_08_processes as grader


COMPLETE_HISTORY = """
cd /home/student/lab
ps
top
sleep 100
jobs
bg
jobs
fg
sleep 100 &
jobs
fg
sleep 100 &
ps
kill 12345
jobs
"""


class GradePartEightTest(unittest.TestCase):
    def test_complete_history_passes_all_checks(self):
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands)

        self.assertEqual(len(results), 14)
        self.assertTrue(all(result["passed"] for result in results))

    def test_kill_requires_numeric_pid(self):
        commands = grader.parse_history_lines(["kill <PID>", "kill %1"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `kill PID` with the numeric sleep PID"])

    def test_kill_accepts_numeric_pid(self):
        commands = grader.parse_history_lines(["kill 12345"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `kill PID` with the numeric sleep PID"])

    def test_foreground_and_background_sleep_are_distinct(self):
        commands = grader.parse_history_lines(["sleep 100"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `sleep 100`"])
        self.assertFalse(labels["Run `sleep 100 &`"])

    def test_background_sleep_accepts_no_space_before_ampersand(self):
        commands = grader.parse_history_lines(["sleep 100&"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `sleep 100`"])
        self.assertTrue(labels["Run `sleep 100 &`"])

    def test_jobs_count_checks_require_repeated_jobs_commands(self):
        commands = grader.parse_history_lines(["jobs", "bg", "jobs"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `jobs` after pressing `Ctrl-Z`"])
        self.assertTrue(labels["Run `jobs` again after `bg`"])
        self.assertFalse(labels["Run `sleep 100 &`, `jobs`, then `fg` in order"])
        self.assertFalse(labels["Run `jobs` after `kill PID`"])

    def test_ps_count_requires_second_bare_ps(self):
        commands = grader.parse_history_lines(["ps", "ps aux"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `ps`"])
        self.assertFalse(labels["Run `ps` again to find the sleep PID"])

    def test_bg_and_fg_accept_job_specs(self):
        commands = grader.parse_history_lines(["bg %1", "fg %1"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `bg`"])
        self.assertTrue(labels["Run `fg`"])

    def test_background_jobs_fg_sequence_must_be_in_order(self):
        commands = grader.parse_history_lines(["jobs", "fg", "sleep 100 &"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `sleep 100 &`, `jobs`, then `fg` in order"])

    def test_activity_seven_requires_second_background_sleep(self):
        commands = grader.parse_history_lines(["sleep 100 &", "jobs", "fg", "ps", "kill 12345", "jobs"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `sleep 100 &` again before finding the PID"])


if __name__ == "__main__":
    unittest.main()
