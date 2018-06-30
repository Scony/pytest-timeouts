from __future__ import absolute_import

import functools
import signal

import pytest

SETUP_TIMEOUT_HELP = 'test case setup timeout in seconds'
EXECUTION_TIMEOUT_HELP = 'test case execution timeout in seconds'
TEARDOWN_TIMEOUT_HELP = 'test case teardown timeout in seconds'


@pytest.hookimpl
def pytest_addoption(parser):
    group = parser.getgroup('timeouts')
    group.addoption(
        '--setup-timeout',
        type=float,
        help=SETUP_TIMEOUT_HELP,
    )
    group.addoption(
        '--execution-timeout',
        type=float,
        help=EXECUTION_TIMEOUT_HELP,
    )
    group.addoption(
        '--teardown-timeout',
        type=float,
        help=TEARDOWN_TIMEOUT_HELP,
    )
    parser.addini('setup_timeout', SETUP_TIMEOUT_HELP)
    parser.addini('execution_timeout', SETUP_TIMEOUT_HELP)
    parser.addini('teardown_timeout', SETUP_TIMEOUT_HELP)


@pytest.hookimpl
def pytest_configure(config):
    assert hasattr(signal, 'SIGALRM')
    config.pluginmanager.register(TimeoutsPlugin(config))


class TimeoutsPlugin(object):
    def __init__(self, config):
        self.setup_timeout = self.fetch_timeout_value('setup_timeout', config)
        self.call_timeout = self.fetch_timeout_value(
            'execution_timeout', config)
        self.teardown_timeout = self.fetch_timeout_value(
            'teardown_timeout', config)

    @staticmethod
    def parse_timeout(timeout):
        timeout = (
            0.0 if (timeout is None) or (timeout == '')
            else float(timeout)
        )
        timeout = 0.0 if timeout < 0.0 else timeout
        return timeout

    @staticmethod
    def fetch_timeout_value(timeout_name, config):
        timeout_option = config.getvalue(timeout_name)
        timeout_ini = config.getini(timeout_name)
        return (
            TimeoutsPlugin.parse_timeout(timeout_ini) if timeout_option is None
            else TimeoutsPlugin.parse_timeout(timeout_option)
        )

    @staticmethod
    def fetch_mark_timeout(item, timeout_name):
        markers = [
            mark.args[0] for mark in item.iter_markers(name=timeout_name)
        ]
        if len(markers) == 1:
            return markers[0]
        return None

    @pytest.hookimpl(tryfirst=True)
    def pytest_report_header(self, config):
        timeout_prints = [
            'setup timeout: %ss' % self.setup_timeout,
            'execution timeout: %ss' % self.call_timeout,
            'teardown timeout: %ss' % self.teardown_timeout,
        ]
        return [', '.join(timeout_prints)]

    @pytest.hookimpl
    def pytest_enter_pdb(self):
        self.cancel_timer()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_setup(self, item):
        self.setup_timer(self.setup_timeout)
        yield
        self.cancel_timer()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item):
        marker_timeout = TimeoutsPlugin.fetch_mark_timeout(
            item,
            'execution_timeout'
        )
        if marker_timeout is not None:
            self.setup_timer(TimeoutsPlugin.parse_timeout(marker_timeout))
        else:
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
