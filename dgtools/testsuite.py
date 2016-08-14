"""Module contains classes and methods representing DG testsuites."""

from io import TextIOBase
from typing import Iterable
from dgtools.testcase import DGTestCase


class DGTestsuite(object):
    """Represents DG testsuite"""

    # pylint: disable=too-few-public-methods

    def __init__(self, name: str) -> None:
        self.name = name
        self._tcmap = {} # type: Dict[str, DGTestCase]

    def add_testcase(self, case: DGTestCase) -> None:
        """Adds a testcase to this testuite"""

        self._tcmap[case.name] = case

    def write_sum_file(self, output_stream: TextIOBase) -> None:
        """Write this testsuite into a stream, resembling the .sum format"""
        for case in self.testcases:
            output_stream.write("Running {0} ...\n".format(case.name))
            for check in case.checks:
                output_stream.write("{0}: {1}\n".format(check.result, check.name))

    def __getitem__(self, index: str) -> DGTestCase:
        return self._tcmap[index]

    @property
    def testcases(self) -> Iterable[DGTestCase]:
        """Returns a view on a set of testcases in this testsuite"""
        return self._tcmap.values()
