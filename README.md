# pytest-timeouts
[![Build Status](https://travis-ci.org/Scony/pytest-timeouts.svg?branch=master)](https://travis-ci.org/Scony/pytest-timeouts)
[![codecov](https://codecov.io/gh/Scony/pytest-timeouts/branch/master/graph/badge.svg)](https://codecov.io/gh/Scony/pytest-timeouts)
[![Documentation Status](https://readthedocs.org/projects/pytest-timeouts/badge/?version=latest)](https://pytest-timeouts.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/pytest-timeouts.svg)](https://pypi.org/project/pytest-timeouts/)
![pyversion](https://img.shields.io/pypi/pyversions/pytest-timeouts.svg)
![Supported pytest 3|4](https://img.shields.io/badge/pytest-3|4-blue.svg)
[![Downloads](https://pepy.tech/badge/pytest-timeouts)](https://pepy.tech/project/pytest-timeouts)
[![PyPI - License](https://img.shields.io/pypi/l/pytest-timeouts.svg)](https://github.com/Scony/pytest-timeouts/blob/master/LICENSE)
![GitHub Release Date](https://img.shields.io/github/release-date/Scony/pytest-timeouts.svg)

Linux-only Pytest plugin to control durations of various test case execution phases.

## Documentation

For documentation visit [pytest-timeouts.readthedocs.io](https://pytest-timeouts.readthedocs.io).

## About

This plugin has been designed for specific use cases which are out of the scope of famous `pytest-timeout` plugin.
It uses a `SIGALRM` signal to schedule a timer which breaks the test case.

## Features

* `setup`, `execution` and `teardown` phase timeouts controllable by:
   * opts: `--setup-timeout`, `--execution-timeout` and `--teardown-timeout`
   * ini: `setup_timeout`, `execution_timeout` and `teardown_timeout`
   * mark: `setup_timeout`, `execution_timeout` and `teardown_timeout`
* fixed order of timeout settings: **opts** > **markers** > **ini**, controlled by `--timeouts-order`
* `--timeouts-order` allow change order of override timeout settings, and disable some settings, i.e. `--timeout-order i` disable markers and opts, any combination is allow
* timeout disabled when debugging with PDB

## Installation

### Stable

```bash
pip install pytest-timeouts
```

### Master

```bash
pip install git+https://github.com/Scony/pytest-timeouts.git
```

## Usage

### Command line

```bash
pytest --setup-timeout 2.5 --execution-timeout 2.01  --teardown-timeout 0
```

### `pytest.ini` setting

```ini
[pytest]
setup_timeout = 2.5
execution_timeout = 2.01
teardown_timeout = 0
```

### Mark

```python
import time

import pytest


@pytest.mark.setup_timeout(0.3)
@pytest.mark.execution_timeout(0.5)
@pytest.mark.teardown_timeout(0.4)
def test_timeout():
    time.sleep(1)
```

## Contributors

* Pawel Lampe
* Kamil Luczak
