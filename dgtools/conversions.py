"""This module contains classes for converting various input formats to DGTestsuite"""

import argparse
import sys
import re
from io import TextIOBase

from dgtools.testsuite import DGTestsuite
from dgtools.testcase import DGTestCase, DGResult


class GitTestsuite(object):
    """Converts a test result file format used by Git project to DGTestsuite"""

    # pylint: disable=too-few-public-methods

    TC_PATTERN = re.compile(r"^\*\*\* (?P<testcase>.*) \*\*\*$")
    CHECK_PATTERN = re.compile(r"^(ok|not ok) [0-9]+ (?P<separator>[-#]) (?P<check>.*)$")

    def __init__(self):
        raise Exception("GitTestuite should not be instantiated")

    @staticmethod
    def parse(name: str, stream: TextIOBase) -> DGTestsuite:
        """Converts a test result file format used by Git project to DGTestsuite"""
        testsuite = None

        for line in iter(stream.readline, ""):
            tc_candidate = GitTestsuite.TC_PATTERN.match(line)
            check_candidate = GitTestsuite.CHECK_PATTERN.match(line)
            if tc_candidate is not None:
                if testsuite is None:
                    testsuite = DGTestsuite(name)
                testcase = DGTestCase(tc_candidate.group("testcase"))
                testsuite.add_testcase(testcase)
            elif check_candidate is not None:
                name = check_candidate.group("check")

                if line.startswith("ok"):
                    if name.startswith("skip"):
                        result = DGResult.UNSUPPORTED
                        name = name[5:]
                    else:
                        result = DGResult.PASS  # pylint: disable=redefined-variable-type
                elif name.endswith(" # TODO known breakage"):  # pylint: disable=fixme
                    name = name[:-22]
                    result = DGResult.KFAIL
                else:
                    result = DGResult.FAIL
                testcase.add_check(name, result)

        return testsuite

FORMATS = {"git" : GitTestsuite}

def main():
    """Converts an input stream of a given format to DG testsuite and writes it to the stdout"""
    parser = argparse.ArgumentParser()
    parser.add_argument("format", choices=("git", ))
    parser.add_argument("result_file", type=argparse.FileType("r"))
    parser.add_argument("--name", default="test-result")

    args = parser.parse_args()

    result_parser = FORMATS[args.format]
    testsuite = result_parser.parse(args.name, args.result_file)
    testsuite.write_sum_file(sys.stdout)
