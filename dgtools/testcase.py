"""Module contains classes and methods representing DG testcases and results."""

from enum import Enum, unique

@unique
class DGResult(Enum):
    """Constants representing results of the individual checks"""
    PASS = "PASS"
    FAIL = "FAIL"

    def __str__(self):
        return str(self.value)

class DGTestCaseCheck(object):
    """Represents a single DG check: a key and a result"""

    # pylint: disable=too-few-public-methods

    def __init__(self, name: str, result: DGResult) -> None:
        self.name = name
        self.result = result


class DGTestCase(object):
    """Represents a DG testcase, contains zero or more checks"""

    # pylint: disable=too-few-public-methods

    def __init__(self, name: str) -> None:
        self.name = name
        self.checks = [] # type: List[DGTestCaseCheck]

    def add_check(self, name: str, result: DGResult) -> None:
        """Add one check to the testcase."""
        self.checks.append(DGTestCaseCheck(name, result))
