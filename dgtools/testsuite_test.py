# We don't care about some stuff in tests
# pylint: disable=missing-docstring, no-self-use

import unittest

from dgtools.testsuite import DGTestsuite
from dgtools.testcase import DGTestCase

class DGTestsuiteTest(unittest.TestCase):
    NAME = "NAME"

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
