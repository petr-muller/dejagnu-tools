# We don't care about some stuff in tests
# pylint: disable=missing-docstring, no-self-use

import unittest

from dgtools.testcases import DGTestCase, DGResult, DGTestCaseCheck

class DGTestCaseTest(unittest.TestCase):
    TESTCASE = "/a/path/to/a/expect/file.exp"
    CHECK1 = "check1"
    CHECK2 = "check2"

    def sanity_test(self):
        case = DGTestCase(DGTestCaseTest.TESTCASE)
        assert case.name == DGTestCaseTest.TESTCASE
        assert len(case.checks) == 0

    def check_test(self):
        case = DGTestCase(DGTestCaseTest.TESTCASE)
        case.add_check(DGTestCaseTest.CHECK1, DGResult.PASS)

        assert len(case.checks) == 1
        assert case.checks[0].name == DGTestCaseTest.CHECK1
        assert case.checks[0].result == DGResult.PASS

        case.add_check(DGTestCaseTest.CHECK2, DGResult.FAIL)
        assert len(case.checks) == 2

class DGTestCaseCheckTest(unittest.TestCase):
    CHECK1 = "check1"
    RESULT1 = DGResult.PASS

    def sanity_test(self):
        check = DGTestCaseCheck(DGTestCaseCheckTest.CHECK1, DGTestCaseCheckTest.RESULT1)
        assert check.name == DGTestCaseCheckTest.CHECK1
        assert check.result == DGTestCaseCheckTest.RESULT1


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
