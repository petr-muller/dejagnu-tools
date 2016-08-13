# We don't care about some stuff in tests
# pylint: disable=missing-docstring, no-self-use

import unittest

from io import StringIO

from dgtools.testsuite import DGTestsuite
from dgtools.testcase import DGTestCase, DGResult


class DGTestsuiteTest(unittest.TestCase):
    NAME = "NAME"
    RESULT = DGResult.FAIL

    def sanity_test(self):
        suite = DGTestsuite(DGTestsuiteTest.NAME)
        assert suite.name == DGTestsuiteTest.NAME
        assert len(suite.testcases) == 0

    def testcases_test(self):
        suite = DGTestsuite(DGTestsuiteTest.NAME)
        case = DGTestCase(DGTestsuiteTest.NAME)

        suite.add_testcase(case)
        assert len(suite.testcases) == 1
        assert suite.testcases[0] is case

    def write_sum_file_test(self):
        suite = DGTestsuite(DGTestsuiteTest.NAME)
        case = DGTestCase(DGTestsuiteTest.NAME)
        case.add_check(DGTestsuiteTest.NAME, DGTestsuiteTest.RESULT)
        suite.add_testcase(case)

        with StringIO() as stream:
            suite.write_sum_file(stream)
            summary = stream.getvalue()
            assert summary == "Running {0} ...\n{1}: {2}\n".format(DGTestsuiteTest.NAME,
                                                                   DGTestsuiteTest.RESULT,
                                                                   DGTestsuiteTest.NAME)
