"""Module contains classes and methods representing DG testsuites."""

from io import TextIOBase
from dgtools.testcase import DGTestCase

class DGTestsuite(object):
    """Represents DG testsuite"""

    # pylint: disable=too-few-public-methods

    def __init__(self, name: str) -> None:
        self.name = name
        self.testcases = [] # type: List[DGTestCase]

    def add_testcase(self, case: DGTestCase) -> None:
        """Adds a testcase to this testuite"""

        self.testcases.append(case)

    def write_sum_file(self, output_stream: TextIOBase) -> None:
        """Write this testsuite into a stream, resembling the .sum format"""
        for case in self.testcases:
            output_stream.write("Running {0} ...\n".format(case.name))
            for check in case.checks:
                output_stream.write("{0}: {1}\n".format(check.result, check.name))
