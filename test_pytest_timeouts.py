pytest_plugins = 'pytester'


def test_arg_parse(testdir):
    testdir.makepyfile("""
        def test_dummy(): pass
    """)
    result = testdir.runpytest(
        '--setup-timeout=1.5',
        '--execution-timeout=2.5',
        '--teardown-timeout=3.5',
    )
    result.stdout.fnmatch_lines([
        "setup timeout: 1.5s, execution timeout: 2.5s, teardown timeout: 3.5s"
    ])


def test_ini_parse(testdir):
    testdir.makepyfile("""
        def test_dummy(): pass
    """)
    testdir.makeini("""
        [pytest]
        setup_timeout = 1.5
        execution_timeout = 2.5
        teardown_timeout = 3.5
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        "setup timeout: 1.5s, execution timeout: 2.5s, teardown timeout: 3.5s"
    ])


def test_setup_timeout(testdir):
    testdir.makepyfile("""
        import pytest
        import time


        @pytest.fixture(scope='function')
        def fx():
            time.sleep(1)
            yield


        def test_dummy(fx):
            pass
    """)
    result = testdir.runpytest('--setup-timeout=0.5')
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.5s*'
    ])


def test_execution_timeout(testdir):
    testdir.makepyfile("""
        import pytest
        import time


        def test_dummy():
            time.sleep(1)
    """)
    result = testdir.runpytest('--execution-timeout=0.4')
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.4s*'
    ])


def test_teardown_timeout(testdir):
    testdir.makepyfile("""
        import pytest
        import time

        @pytest.fixture(scope='function')
        def fx():
            yield
            time.sleep(1)


        def test_dummy(fx):
            pass
    """)
    result = testdir.runpytest('--teardown-timeout=0.3')
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.3s*'
    ])


def test_execucution_marker_timeout(testdir):
    testdir.makepyfile("""
        import pytest
        import time

        @pytest.mark.execution_timeout(0.2)
        def test_dummy():
            time.sleep(1)
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.2s*'
    ])
