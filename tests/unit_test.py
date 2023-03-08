# -*- coding: utf-8 -*-


def test_help_message(testdir):
    result = testdir.runpytest("--help")
    result.stdout.fnmatch_lines(
        [
            "*gitlabci-parallelized:",
            "*--ci-node-total=*",
            "*Total number of GitLab CI worker nodes.",
            "*--ci-node-index=*",
            "*Index of this GitLab CI worker node.",
        ]
    )


TEST_SCRIPT = """
import unittest

class TestCase(unittest.TestCase):
    def test_1(self):
        assert True

    def test_2(self):
        assert True
"""


def test_with_gitlabci_parallelize(testdir):
    testdir.makepyfile(TEST_SCRIPT)
    result = testdir.runpytest("--ci-node-index=1", "--ci-node-total=2")
    result.stdout.fnmatch_lines(["GitLab CI node 1 / 2 -- running 1 tests..."])
    assert result.ret == 0


def test_with_gitlabci_parallelize_and_no_included_tests(testdir):
    testdir.makepyfile(TEST_SCRIPT)
    result = testdir.runpytest("--ci-node-index=1", "--ci-node-total=3", "-q")
    result.stdout.fnmatch_lines(["GitLab CI node 1 / 3 -- running 0 tests..."])
    assert result.ret == 0


def test_without_gitlabci_parallelize(testdir):
    testdir.makepyfile(TEST_SCRIPT)
    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(
        [
            "*test_1 PASSED*",
            "*test_2 PASSED*",
        ]
    )
    assert result.ret == 0
