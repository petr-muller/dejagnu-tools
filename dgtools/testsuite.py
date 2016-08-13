"""Module contains classes and methods representing DG testsuites."""

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
