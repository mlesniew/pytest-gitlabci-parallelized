# -*- coding: utf-8 -*-
import os

import pytest


def check_positive(value):
    value = int(value)
    if value < 1:
        raise ValueError("value must be an int greater than 0")
    return value


def pytest_addoption(parser):
    group = parser.getgroup("gitlabci-parallelized")
    group.addoption(
        "--ci-node-total",
        dest="ci_node_total",
        type=check_positive,
        default=check_positive(os.getenv("CI_NODE_TOTAL") or 1),
        help="Total number of GitLab CI worker nodes.",
    )
    group.addoption(
        "--ci-node-index",
        dest="ci_node_index",
        type=int,
        default=check_positive(os.getenv("CI_NODE_INDEX") or 1),
        help="Index of this GitLab CI worker node.",
    )


def pytest_report_collectionfinish(config, startdir, items):
    ci_node_total = config.getoption("ci_node_total")
    ci_node_index = config.getoption("ci_node_index")

    if ci_node_index > ci_node_total:
        return "Invalid node index, skipping all tests."

    if ci_node_total <= 1:
        return

    return "GitLab CI node {} / {} -- running {} tests...".format(
        ci_node_index, ci_node_total, len(items)
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_cmdline_main(config):
    outcome = yield config
    exit_code = outcome.get_result()

    # Exit Code 5 indicates no tests were collected
    # https://docs.pytest.org/en/7.1.x/reference/exit-codes.html
    # If there are more workers than tests, this can cause "No Tests" error
    # This is fine, and we cast it to an OK exit code
    if config.getoption("ci_node_total") > 1 and exit_code == 5:
        outcome.force_result(0)


def pytest_collection_modifyitems(session, config, items):
    ci_node_total = config.getoption("ci_node_total")
    ci_node_index = config.getoption("ci_node_index")

    if ci_node_index > ci_node_total:
        # no tests to run
        items.clear()
        return

    if ci_node_total <= 1:
        # no filtering needed
        return

    total_items = len(items)

    a = (total_items * (ci_node_index - 1)) // ci_node_total
    b = (total_items * (ci_node_index)) // ci_node_total

    items[:] = items[a:b]
