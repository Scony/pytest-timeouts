import signal
import functools

import pytest


@pytest.hookimpl
def pytest_addoption(parser):
    group = parser.getgroup('timeouts')
    group.addoption(
        '--setup-timeout',
        type=float,
        help='test case setup timeout in seconds',
    )
    group.addoption(
        '--execution-timeout',
        type=float,
        help='test case call (execution) timeout in seconds',
    )
    group.addoption(
        '--teardown-timeout',
        type=float,
        help='test case teardown timeout in seconds',
    )


@pytest.hookimpl
def pytest_configure(config):
    assert hasattr(signal, 'SIGALRM')
    config.pluginmanager.register(TimeoutsPlugin(config))


class TimeoutsPlugin(object):
    def __init__(self, config):
        self.setup_timeout = self.fetch_timeout_value('setup_timeout', config)
        self.call_timeout = self.fetch_timeout_value('execution_timeout', config)
        self.teardown_timeout = self.fetch_timeout_value('teardown_timeout', config)

    @staticmethod
    def fetch_timeout_value(timeout_name, config):
        timeout = config.getvalue(timeout_name)
        timeout = 0.0 if timeout is None else timeout
        timeout = 0.0 if timeout < 0.0 else timeout
        return timeout

    @pytest.hookimpl(tryfirst=True)
    def pytest_report_header(self, config):
        return ['setup timeout: %ss, execution timeout: %ss, teardown timeout: %ss' % (
            self.setup_timeout,
            self.call_timeout,
            self.teardown_timeout,
        )]

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_setup(self, item):
        self.setup_timer(self.setup_timeout)
        yield
        self.cancel_timer()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item):
        self.setup_timer(self.call_timeout)
        yield
        self.cancel_timer()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_teardown(self, item):
        self.setup_timer(self.teardown_timeout)
        yield
        self.cancel_timer()

    @staticmethod
    def setup_timer(timeout):
        handler = functools.partial(TimeoutsPlugin.timeout_handler, timeout)
        signal.signal(signal.SIGALRM, handler)
        signal.setitimer(signal.ITIMER_REAL, timeout)

    @staticmethod
    def cancel_timer():
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    @staticmethod
    def timeout_handler(timeout, signum, frame):
        __tracebackhide__ = True
        pytest.fail('Timeout >%ss' % timeout)
