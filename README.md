# pytest-testit-parametrize
[![Release Status](https://img.shields.io/pypi/v/pytest-testit-parametrize.svg?style=plastic)](https://pypi.python.org/pypi/pytest-testit-parametrize)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-testit-parametrize.svg?style=plastic)](https://pypi.org/project/pytest-testit-parametrize)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pytest-testit-parametrize?style=plastic)

### A pytest plugin for uploading parameterized tests parameters into TMS TestIT

## Getting Started

### Installation

```
pip install pytest-testit-parametrize
```

## Usage

Read parameters from collected pytest autotests and write them into Test IT test cases
```
pytest --testit-params-init
```

Remove parameterization parameters from Test IT test cases related to collected autotests by pytest
```
pytest --testit-params-flush
```

You can use both flags at the same time.

NOTE:
When the plugin finishes its work the testrun will be interrupted, so no autotests will actually be run. 
The plugin only affects autotests with the `@pytest.mark.parameterize` decorator. All others are ignored

## Configuration 

To have the plugin working you should have a completely identical configuration to what is required for [testit-adapter-pytest](https://github.com/testit-tms/adapters-python/tree/main/testit-adapter-pytest#file). 

# Contributing

You can help to develop the project. Any contributions are **greatly appreciated**.
Tests can be run with [tox](https://tox.readthedocs.io/en/latest/), please ensure
the coverage at least stays the same before you submit a pull request.

# License

Distributed under the terms of the [Apache Software License 2.0](https://www.apache.org/licenses/LICENSE-2.0), "pytest-testit-parametrize" is free and open source software

# Issues

If you encounter any problems, please [file an issue](https://github.com/iromanchenko-cyrm/pytest-testit-parametrize/issues) along with a detailed description.