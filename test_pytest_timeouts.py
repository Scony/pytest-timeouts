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


        @pytest.fixture(scope='function')
        def fx2():
            time.sleep(1)
            yield


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


def test_setup_marker_timeout(testdir):
    testdir.makepyfile("""
        import pytest
        import time


        @pytest.fixture(scope='function')
        def fx():
            time.sleep(1)
            yield


        @pytest.mark.setup_timeout(0.2)
        def test_dummy(fx):
            time.sleep(1)
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.2s*'
    ])


def test_teardown_marker_timeout(testdir):
    testdir.makepyfile("""
        import pytest
        import time


        @pytest.fixture(scope='function')
        def fx():
            yield
            time.sleep(1)


        @pytest.mark.teardown_timeout(0.2)
        def test_dummy(fx):
            pass
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.2s*'
    ])


def test_timeout_setting_order(testdir):
    testdir.makepyfile("""
        import pytest
        import time


        @pytest.fixture(scope='function')
        def fx():
            yield
            time.sleep(1)


        @pytest.fixture(scope='function')
        def fx2():
            time.sleep(1)
            yield


        @pytest.mark.teardown_timeout(0.2)
        def test_dummy(fx):
            pass


        @pytest.mark.setup_timeout(0.4)
        def test_dummy2(fx2):
            pass
    """)
    testdir.makeini("""
        [pytest]
        setup_timeout = 0.3
        teardown_timeout = 0.3
    """)
    result = testdir.runpytest('--setup-timeout=0.1')
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.2s*',
        '*Failed: Timeout >0.1s*',
    ])


def test_timeout_override_order(testdir):
    testdir.makepyfile("""
        import pytest
        import time


        @pytest.fixture(scope='function')
        def fx():
            yield
            time.sleep(1)


        @pytest.fixture(scope='function')
        def fx2():
            time.sleep(1)
            yield


        @pytest.mark.teardown_timeout(0.2)
        def test_dummy(fx):
            pass


        @pytest.mark.setup_timeout(0.4)
        def test_dummy_2(fx2):
            pass
    """)
    testdir.makeini("""
        [pytest]
        setup_timeout = 0.1
    """)
    result = testdir.runpytest(
        '--setup-timeout=0.3',
        '--teardown-timeout=0.3',
        '--timeouts-order="imo"',
    )
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.2s*',
        '*Failed: Timeout >0.1s*',
    ])


def test_disable_args_and_markers(testdir):
    testdir.makepyfile("""
        import pytest
        import time


        @pytest.fixture(scope='function')
        def fx():
            yield
            time.sleep(1)


        @pytest.fixture(scope='function')
        def fx2():
            time.sleep(1)
            yield


        @pytest.mark.teardown_timeout(0.2)
        def test_dummy(fx):
            pass


        @pytest.mark.setup_timeout(0.4)
        def test_dummy_2(fx2):
            pass
    """)
    testdir.makeini("""
        [pytest]
        setup_timeout = 0.1
        teardown_timeout = 0.1
    """)
    result = testdir.runpytest(
        '--setup-timeout=0.3',
        '--teardown-timeout=0.3',
        '--timeouts-order="i"',
    )
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.1s*',
        '*Failed: Timeout >0.1s*',
    ])


def test_marker_value_missing(testdir):
    testdir.makepyfile("""
        import pytest
        import time
        @pytest.mark.execution_timeout()
        def test_dummy():
            time.sleep(1)
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*TypeError:*'
    ])


def test_marker_value_invalid(testdir):
    testdir.makepyfile("""
        import pytest
        import time
        @pytest.mark.execution_timeout('asdf')
        def test_dummy():
            time.sleep(1)
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*ValueError:*'
    ])


def test_timeout_scope_fixture(testdir):
    testdir.makepyfile("""
        import pytest
        import time


        pytestmark = [
            pytest.mark.teardown_timeout(0.12, 'function'),
            pytest.mark.teardown_timeout(0.14, 'module'),
            pytest.mark.teardown_timeout(0.13),
        ]


        @pytest.fixture(scope='function')
        def fx():
            yield
            time.sleep(1)


        @pytest.fixture(scope='class')
        def fx2():
            yield
            time.sleep(1)


        @pytest.fixture(scope='module')
        def fx3():
            yield
            time.sleep(1)


        def test_dummy(fx):
            pass


        def test_dummy_2(fx2):
            pass


        @pytest.mark.teardown_timeout(0.11)
        def test_dummy_4(fx):
            pass


        def test_dummy_3(fx3):
            pass
   """)
    testdir.makeini("""
        [pytest]
        teardown_timeout = 0.15
    """)
    result = testdir.runpytest()
    result.stdout.fnmatch_lines([
        '*Failed: Timeout >0.12s*',
        '*Failed: Timeout >0.13s*',
        '*Failed: Timeout >0.11s*',
        '*Failed: Timeout >0.14s*',
    ])
