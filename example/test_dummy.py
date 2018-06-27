import time

import pytest


@pytest.fixture(scope='function')
def fx():
    time.sleep(2)
    yield


def test_dummy(fx):
    pass
