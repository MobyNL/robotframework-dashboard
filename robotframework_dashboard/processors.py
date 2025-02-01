from robot.api import ExecutionResult, ResultVisitor
from robot.result.model import TestCase, TestSuite, Keyword
from datetime import datetime
from pathlib import Path


class OutputProcessor:
    def get_output_data(self, output_path: Path):
        output = ExecutionResult(output_path)
        if hasattr(output, "generation_time"):
            generation_time = output.generation_time
        else:
            with open(output_path, "r") as f:
                for line in f:
                    if "<robot" in line:
                        generation_time = line.split('generated="', 1)[1].split('"', 1)[
                            0
                        ]
                        if "T" in generation_time:
                            generation_time = datetime.strptime(
                                generation_time, "%Y-%m-%dT%H:%M:%S.%f"
                            )
                        else:
                            generation_time = datetime.strptime(
                                generation_time, "%Y%m%d %H:%M:%S.%f"
                            )
                        break
        run_list, suite_list, test_list, keyword_list = [], [], [], []
        output.visit(RunProcessor(generation_time, run_list))
        output.visit(SuiteProcessor(generation_time, suite_list))
        output.visit(TestProcessor(generation_time, test_list))
        output.visit(KeywordProcessor(generation_time, keyword_list))
        average_keyword_list = self.calculate_keyword_averages(keyword_list)
        return {
            "runs": run_list,
            "suites": suite_list,
            "tests": test_list,
            "keywords": average_keyword_list,
        }

    def calculate_keyword_averages(self, keyword_list: list):
        average_keyword_dict = {}
        average_keyword_list = []
        for keyword in keyword_list:
            run_start = keyword[0]
            name = keyword[1]
            passed = int(keyword[2])
            failed = int(keyword[3])
            skipped = int(keyword[4])
            elapsed_s = keyword[5]
            if not name in average_keyword_dict.keys():
                average_keyword_dict[name] = {
                    "passed": passed,
                    "failed": failed,
                    "skipped": skipped,
                    "elapsed_s": [elapsed_s],
                }
            else:
                average_keyword_dict[name]["passed"] += passed
                average_keyword_dict[name]["failed"] += failed
                average_keyword_dict[name]["skipped"] += skipped
                average_keyword_dict[name]["elapsed_s"].append(elapsed_s)
        for name in average_keyword_dict.keys():
            elapsed_list = average_keyword_dict[name]["elapsed_s"]
            sum_elapsed_list = sum(elapsed_list)
            len_elapsed_list = len(elapsed_list)
            min_elapsed_list = min(elapsed_list)
            max_elapsed_list = max(elapsed_list)
            average_keyword_list.append(
                (
                    run_start,  # run_start
                    name,  # keyword name
                    average_keyword_dict[name]["passed"],  # amount of passes
                    average_keyword_dict[name]["failed"],  # amount of fails
                    average_keyword_dict[name]["skipped"],  # amount of skips
                    len_elapsed_list,  # times used
                    round(sum_elapsed_list, 3),  # total usage time
                    round(sum_elapsed_list / len_elapsed_list, 3),  # average usage time
                    round(min_elapsed_list, 3),  # fastest usage time
                    round(max_elapsed_list, 3),  # slowest usage time
                )
            )
        return average_keyword_list


class RunProcessor(ResultVisitor):
    def __init__(self, run_time: datetime, run_list: list):
        self.run_list = run_list
        self.run_time = run_time

    def visit_suite(self, suite: TestSuite):
        stats = suite.statistics

        # handling for older robot versions
        if hasattr(suite, "full_name"):
            full_name = suite.full_name
        else:
            full_name = suite.longname
        if hasattr(suite, "elapsed_time"):
            elapsed_time = round(suite.elapsed_time.total_seconds(), 3)
        else:
            elapsed_time = round(suite.elapsedtime / 1000, 3)
        if hasattr(suite, "start_time"):
            start_time = suite.start_time
        else:
            start_time = suite.starttime

        self.run_list.append(
            (
                self.run_time,
                full_name,
                suite.name,
                stats.total,
                stats.passed,
                stats.failed,
                stats.skipped,
                elapsed_time,
                start_time,
            )
        )


class SuiteProcessor(ResultVisitor):

    def __init__(self, run_time: datetime, suite_list: list):
        self.suite_list = suite_list
        self.run_time = run_time

    def start_suite(self, suite: TestSuite):
        if suite.tests:
            try:
                stats = suite.statistics.all
            except:
                stats = suite.statistics

            # handling for older robot versions
            if hasattr(suite, "full_name"):
                full_name = suite.full_name
            else:
                full_name = suite.longname
            if hasattr(suite, "elapsed_time"):
                elapsed_time = round(suite.elapsed_time.total_seconds(), 3)
            else:
                elapsed_time = round(suite.elapsedtime / 1000, 3)
            if hasattr(suite, "start_time"):
                start_time = suite.start_time
            else:
                start_time = suite.starttime

            self.suite_list.append(
                (
                    self.run_time,
                    full_name,
                    suite.name,
                    stats.total,
                    stats.passed,
                    stats.failed,
                    stats.skipped,
                    elapsed_time,
                    start_time,
                )
            )


class TestProcessor(ResultVisitor):
    def __init__(self, run_time: datetime, test_list: list):
        self.test_list = test_list
        self.run_time = run_time

    def visit_test(self, test: TestCase):
        # handling for older robot versions
        if hasattr(test, "full_name"):
            full_name = test.full_name
        else:
            full_name = test.longname
        if hasattr(test, "elapsed_time"):
            elapsed_time = round(test.elapsed_time.total_seconds(), 3)
        else:
            elapsed_time = round(test.elapsedtime / 1000, 3)
        if hasattr(test, "start_time"):
            start_time = test.start_time
        else:
            start_time = test.starttime

        self.test_list.append(
            (
                self.run_time,
                full_name,
                test.name,
                test.passed,
                test.failed,
                test.skipped,
                elapsed_time,
                start_time,
                test.message[:150],
                str(test.tags).replace(' ', ''),
            )
        )


class KeywordProcessor(ResultVisitor):
    def __init__(self, run_time: datetime, keyword_list: list):
        self.keyword_list = keyword_list
        self.run_time = run_time

    def end_keyword(self, keyword: Keyword):
        # handling for older robot versions
        if hasattr(keyword, "elapsed_time"):
            elapsed_time = round(keyword.elapsed_time.total_seconds(), 3)
        else:
            elapsed_time = round(keyword.elapsedtime / 1000, 3)

        self.keyword_list.append(
            (
                self.run_time,
                keyword.name,
                keyword.passed,
                keyword.failed,
                keyword.skipped,
                elapsed_time,
            )
        )
