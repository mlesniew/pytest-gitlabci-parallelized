# -*- coding: utf-8 -*-
import pytest
import os


def pytest_addoption(parser):
    group = parser.getgroup("gitlab-ci-parallel")
    group.addoption(
        "--gitlab-ci-parallel",
        dest="gitlab_ci_parallel",
        action="store_true",
        default=False,
        help="Enable parallelization across GitLab CI runners.",
    )


def get_gitlab_node_info():
    try:
        idx = int(os.getenv("CI_NODE_INDEX", "0"))
        tot = int(os.getenv("CI_NODE_TOTAL", "0"))
        if 0 <= idx < tot and tot > 0:
            return idx, tot
    except ValueError:
        pass
    return None


def gitlab_ci_parallel_enabled(config):
    return config.getoption("gitlab_ci_parallel") and get_gitlab_node_info()


def pytest_report_collectionfinish(config, startdir, items):
    if gitlab_ci_parallel_enabled(config):
        return "GitLab CI parallelizm is enabled, running only {} tests.".format(len(items))


@pytest.hookimpl(hookwrapper=True)
def pytest_cmdline_main(config):
    outcome = yield config
    exit_code = outcome.get_result()

    # Exit Code 5 indicates no tests were collected
    # https://docs.pytest.org/en/7.1.x/reference/exit-codes.html
    # If there are more workers than tests, this can cause "No Tests" error
    # This is fine, and we cast it to an OK exit code
    if gitlab_ci_parallel_enabled(config) and exit_code == 5:
        outcome.force_result(0)


def pytest_collection_modifyitems(session, config, items):
    if not gitlab_ci_parallel_enabled(config):
        return

    node_idx, node_tot = get_gitlab_node_info()

    a = (len(items) * node_idx) // node_tot
    b = (len(items) * (node_idx + 1)) // node_tot

    items[:] = items[a: b]
