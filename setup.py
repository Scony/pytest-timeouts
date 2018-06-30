from setuptools import setup

setup(
    name='pytest-timeouts',
    version='1.0.0',
    description='Linux-only Pytest plugin to control durations of various test case execution phases',
    author='Pawel Lampe',
    author_email='pawel.lampe@gmail.com',
    url='https://github.com/Scony/pytest-timeouts',
    license='MIT',
    install_requires=[
        'pytest',
    ],
    py_modules=[
        'pytest_timeouts',
    ],
    entry_points={
        'pytest11': ['timeouts = pytest_timeouts'],
    },
)
