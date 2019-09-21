from setuptools import setup

setup(
    version='1.2.1',
    install_requires=[
        'pytest>=3.1',
    ],
    entry_points={
        'pytest11': ['timeouts = pytest_timeouts'],
    },
)
