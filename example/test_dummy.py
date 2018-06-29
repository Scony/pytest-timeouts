import time

import pytest

pytest_plugins = 'pytester'

def test_fixture_timeout_arg(testdir):
    testdir.makepyfile("""
    import pytest
    import time


    @pytest.fixture(scope='function')
    def fx():
        time.sleep(2)
        yield


    def test_dummy(fx):
        pass
    """)
    result = testdir.runpytest('--setup-timeout=1.5')
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >1.5s*'
    ])
