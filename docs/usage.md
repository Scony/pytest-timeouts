# Usage

Pytest test scenario can be split to three stage:

- setup - control by **setup-timeout**: before test, when fixtures are setup
- execution - control by **execution-timeout**: test execution
- teardown - control by **teardown-timeout**: after test

Timeout is provided in seconds.

## Command line

*pytest-timeout* can be control from command line.

List on available option:

- **setup-timeout**
- **execution-timeout**
- **teardown-timeout**
- **timeout-order**, control order of override timeout, more in [Timeout order](#timeout-order)

### Examples

- Set setup timeout to 5s, execution timeout to 10s and teardown timeout to 7s
```bash
pytest --setup-timeout 5 --execution-timeout 10 --teardown-timeout 7
```

- Set timeout order override **opt** > **ini**, **mark** disable
```
pytest --timeout-order oi
```

## `pytest.ini` file

In ini file you can set timeout for any stage.

### Example

```ini
[pytest]
setup_timeout = 2.5
execution-timeout = 2.01
teardown-timeout = 0
```

## Timeout order

Timeout order is a combination of three option:

- **i** - ini
- **o** - options set up from command line
- **m** - markers

Default order of override timeout is: **opts** > **markers** > **ini**.

You can change order of override or disable it, i.e. **_i_** will disable **opts** and **markers**, **_mo_** change override order to **markers** > **opts** and **ini** will be disable

## Marks

Marks can be use to change timeout for specific test, module, etc.
Mark can be added in two way:

- mark function

    Mark allow modify timeout specific element
```python
import pytest

@pytest.mark.setup_timeout(0.5)
class TestClass(object):
    pass

@pytest.mark.execution_timeout(0.5)
@pytest.mark.teardown_timeout(0.4)
def text_fixture():
    pass
```

- mark file

    Mark define for file modify timeout for every element in module.
```python
import python

pytestmark = [
    pytest.mark.execution_timeout(0.12),
    pytest.mark.setup_timeout(0.14),
    pytest.mark.teardown_timeout(0.13),
]
```

### Marks with scope

For file mark, we also can provide scope: `function`, `module`, `session`, `class`

```python
import python

pytestmark = [
    pytest.mark.execution_timeout(0.12, 'session'),
    pytest.mark.setup_timeout(0.14, 'module'),
    pytest.mark.teardown_timeout(0.13, 'class'),
]
```
That solution allow us for example disable `teardown_timeout` for session fixture.
