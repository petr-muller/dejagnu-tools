# We don't care about some stuff in tests
# pylint: disable=missing-docstring, no-self-use

import unittest
from io import StringIO
from dgtools.conversions import GitTestsuite
from dgtools.testcase import DGResult

class GitTestsuiteTest(unittest.TestCase):
    # pylint: disable=fixme

    EXAMPLE = """    SUBDIR git-gui
    SUBDIR gitk-git
    SUBDIR perl
Manifying 8 pod documents
    SUBDIR templates
make -C t/ all
make[1]: Entering directory '/home/afri/Temporary/git/t'
rm -f -r 'test-results'
make aggregate-results-and-cleanup
make[2]: Entering directory '/home/afri/Temporary/git/t'
*** t0000-basic.sh ***
ok 1 - .git/objects should be empty after git init in an empty repo
ok 2 - .git/objects should have 3 subdirectories
ok 3 - success is reported like this
# passed all 3 test(s)
1..5
*** t1013-read-tree-submodule.sh ***
ok 1 - git read-tree -u -m: added submodule creates empty directory
ok 2 - git read-tree -u -m: added submodule leaves existing empty directory alone
ok 3 - git read-tree -u -m: added submodule doesn't remove untracked unignored file with same name
ok 4 - git read-tree -u -m: replace tracked file with submodule creates empty directory
ok 5 - git read-tree -u -m: replace directory with submodule
ok 6 - git read-tree -u -m: removed submodule leaves submodule directory and its contents in place
ok 7 - git read-tree -u -m: removed submodule leaves submodule containing a .git directory alone
ok 8 - git read-tree -u -m: replace submodule with a directory must fail
ok 9 - git read-tree -u -m: replace submodule containing a .git directory with a directory must fail
not ok 10 - git read-tree -u -m: replace submodule with a file must fail # TODO known breakage
not ok 11 - git read-tree -u -m: replace submodule containing a .git directory with a file must fail
ok 12 # skip .git hidden (missing MINGW)
"""
    CASES = ["t0000-basic.sh", "t1013-read-tree-submodule.sh"]

    def tc_pattern_test(self):
        line = "*** t1013-read-tree-submodule.sh ***"
        match = GitTestsuite.TC_PATTERN.match(line)
        assert match is not None
        assert match.group("testcase") == "t1013-read-tree-submodule.sh"

    def check_pattern_ok_test(self):
        ok_line = "ok 1 - git read-tree -u -m"
        match = GitTestsuite.CHECK_PATTERN.match(ok_line)
        assert match is not None
        assert match.group("separator") == "-"
        assert match.group("check") == "git read-tree -u -m"

    def check_pattern_nok_test(self):
        nok_line = "not ok 11 - git read-tree -u -m: replace submodule"
        match = GitTestsuite.CHECK_PATTERN.match(nok_line)
        assert match is not None
        assert match.group("separator") == "-"
        assert match.group("check") == "git read-tree -u -m: replace submodule"

    def check_pattern_skip_test(self):
        skip_line = "ok 12 # skip .git hidden (missing MINGW)"
        match = GitTestsuite.CHECK_PATTERN.match(skip_line)
        assert match is not None
        assert match.group("separator") == "#"
        assert match.group("check") == "skip .git hidden (missing MINGW)"

    def check_pattern_kfail_test(self):
        kfail_line = "not ok 10 - git read-tree -u -m: replace # TODO known breakage"
        match = GitTestsuite.CHECK_PATTERN.match(kfail_line)
        assert match is not None
        assert match.group("separator") == "-"
        assert match.group("check") == "git read-tree -u -m: replace # TODO known breakage"

    def parse_test(self):
        input_file = StringIO(GitTestsuiteTest.EXAMPLE)
        testsuite = GitTestsuite.parse("git", input_file)

        assert testsuite.name == "git"
        assert len(testsuite.testcases) == 2
        assert set([case.name for case in testsuite.testcases]) == set(GitTestsuiteTest.CASES)

        t0000 = testsuite["t0000-basic.sh"]
        assert len(t0000.checks) == 3
        for check in t0000.checks:
            assert check.result == DGResult.PASS

        t1013 = testsuite["t1013-read-tree-submodule.sh"]
        assert len(t1013.checks) == 12
        assert len([check for check in t1013.checks if check.result == DGResult.PASS]) == 9
        assert len([check for check in t1013.checks if check.result == DGResult.FAIL]) == 1
        assert len([check for check in t1013.checks if check.result == DGResult.KFAIL]) == 1
        assert len([check for check in t1013.checks if check.result == DGResult.UNSUPPORTED]) == 1
