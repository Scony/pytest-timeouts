import signal
import functools

import pytest


@pytest.hookimpl
def pytest_addoption(parser):
    group = parser.getgroup('timeouts')
    group.addoption(
        '--execution-timeout',
        type=float,
        help='test case call (execution) timeout in seconds',
    )


@pytest.hookimpl
def pytest_configure(config):
    assert hasattr(signal, 'SIGALRM')
    config.pluginmanager.register(TimeoutsPlugin(config))


class TimeoutsPlugin(object):
    def __init__(self, config):
        self.call_timeout = config.getvalue('execution_timeout')
        self.call_timeout = 0.0 if self.call_timeout is None else self.call_timeout
        self.call_timeout = 0.0 if self.call_timeout < 0.0 else self.call_timeout

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item):
        self.setup_timer(self.call_timeout)
        yield
        self.cancel_timer()

    @staticmethod
    def setup_timer(timeout):
        signal.signal(signal.SIGALRM, functools.partial(TimeoutsPlugin.timeout_handler, timeout))
        signal.setitimer(signal.ITIMER_REAL, timeout)

    @staticmethod
    def cancel_timer():
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    @staticmethod
    def timeout_handler(timeout, signum, frame):
        __tracebackhide__ = True
        pytest.fail('Timeout >%ss' % timeout)
