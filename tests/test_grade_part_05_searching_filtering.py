import unittest

from scripts import grade_part_05_searching_filtering as grader


COMPLETE_HISTORY = """
cd /home/student/lab
find . -name "*.txt"
find . -type f
grep "ERROR" logs/errors.log
grep -i "warn" logs/errors.log
cat logs/errors.log | grep ERROR
find . -name "*.txt" | sort
cut -d',' -f1 lab-files/search-practice/incidents.csv
cut -d',' -f1 lab-files/search-practice/incidents.csv | sort | uniq
"""


class GradePartFiveTest(unittest.TestCase):
    def test_complete_history_passes_all_checks(self):
        commands = grader.parse_history_lines(COMPLETE_HISTORY.splitlines())
        results = grader.grade(commands)

        self.assertEqual(len(results), 9)
        self.assertTrue(all(result["passed"] for result in results))

    def test_find_name_requires_txt_pattern(self):
        commands = grader.parse_history_lines(["find . -name '*.log'"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels['Run `find . -name "*.txt"`'])

    def test_find_type_requires_regular_file_type(self):
        commands = grader.parse_history_lines(["find . -type d"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `find . -type f`"])

    def test_grep_error_requires_pattern_and_file(self):
        commands = grader.parse_history_lines(["grep ERROR logs/app.log"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels['Run `grep "ERROR" logs/errors.log`'])

    def test_grep_warn_requires_case_insensitive_flag(self):
        commands = grader.parse_history_lines(['grep "warn" logs/errors.log'])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels['Run `grep -i "warn" logs/errors.log`'])

    def test_cat_grep_requires_pipe(self):
        commands = grader.parse_history_lines(["cat logs/errors.log; grep ERROR"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels["Run `cat logs/errors.log | grep ERROR`"])

    def test_find_sort_requires_pipeline(self):
        commands = grader.parse_history_lines(['find . -name "*.txt"', "sort"])
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(labels['Run `find . -name "*.txt" | sort`'])

    def test_cut_accepts_split_delimiter_and_field_options(self):
        commands = grader.parse_history_lines(
            ["cut -d ',' -f 1 lab-files/search-practice/incidents.csv"]
        )
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertTrue(labels["Run `cut -d',' -f1 lab-files/search-practice/incidents.csv`"])

    def test_sort_must_come_before_uniq_in_final_pipeline(self):
        commands = grader.parse_history_lines(
            ["cut -d',' -f1 lab-files/search-practice/incidents.csv | uniq | sort"]
        )
        results = grader.grade(commands)
        labels = {result["label"]: result["passed"] for result in results}

        self.assertFalse(
            labels["Run `cut -d',' -f1 lab-files/search-practice/incidents.csv | sort | uniq`"]
        )


if __name__ == "__main__":
    unittest.main()
