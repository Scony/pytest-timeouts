from setuptools import setup

with open("README.md") as fd:
    long_description = fd.read()

setup(
    name='pytest-timeouts',
    version='1.1.1',
    description='Linux-only Pytest plugin to control durations of various test case execution phases',
    long_description=long_description,
    author='Pawel Lampe',
    author_email='pawel.lampe@gmail.com',
    url='https://github.com/Scony/pytest-timeouts',
    project_urls={
        "Documentation": "https://pytest-timeouts.readthedocs.io/",
        "Source Code": "https://github.com/Scony/pytest-timeouts/",
    },
    license='MIT',
    install_requires=[
        'pytest>=3.1',
    ],
    py_modules=[
        'pytest_timeouts',
    ],
    entry_points={
        'pytest11': ['timeouts = pytest_timeouts'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        "Topic :: Utilities",
    ],
)
