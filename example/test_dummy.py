import time

import pytest


@pytest.fixture(scope='function')
def fx():
    time.sleep(2)
    yield


@pytest.fixture(scope='function')
def fx2():
    yield
    time.sleep(2)


def test_dummy(fx):
    pass

@pytest.mark.teardown_timeout(0.2)
def test_dummy_2(fx2):
    pass
