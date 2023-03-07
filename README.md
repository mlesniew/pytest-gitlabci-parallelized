# pytest-gitlabci-parallelized

[![PyPI version](https://img.shields.io/pypi/v/pytest-gitlabci-parallelized.svg)](https://pypi.org/project/pytest-gitlabci-parallelized) [![Python versions](https://img.shields.io/pypi/pyversions/pytest-gitlabci-parallelized.svg)](https://pypi.org/project/pytest-gitlabci-parallelized)

Parallelize pytest across GitLab CI workers.

This pytest plugin is inspired and based on [pytest-circleci-parallelized](https://github.com/ryanwilsonperkin/pytest-circleci-parallelized).

---

## Features

Leverage the builtin parallelism of GitLab CI to run your test suites.  Call `pytest` with the `CI_NODE_INDEX` and `CI_NODE_TOTAL` environment variables set or use the `--ci-node-index` and `--ci-node-total` switches to split tests amongst nodes.

Read more about the GitLab CI parallel test splitting [here](https://docs.gitlab.com/ee/ci/yaml/#parallel).

```yaml
# .gitlab-ci.yml

tests:
  stage: test
  script: pytest
  parallel: 5

```


## Installation

You can install "pytest-gitlabci-parallelized" via pip from [PyPI](https://pypi.org/project/pytest-gitlabci-parallelized/).

```sh
pip install pytest-gitlabci-parallelized
```

## Contributing

Contributors welcome! Tests can be run with [`pytest`](https://docs.pytest.org/en/7.1.x/).

## License

Distributed under the terms of the [MIT](/LICENSE) license, `pytest-gitlabci-parallelized` is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/mlesniew/pytest-gitlabci-parallelized/issues/new) along with a detailed description.
