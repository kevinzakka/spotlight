"""Install script for setuptools."""

import os

from setuptools import find_packages, setup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DESCRIPTION = "An open-source Spotlight for Linux, for researchers."
CORE_REQUIREMENTS = [
    "pycairo",
    "PyGObject",
    "py-dict-client",
    "lark",
]
DEV_REQUIREMENTS = [
    "pytest-xdist",
    "pytype",
    "ipdb",
    "black",
    "isort",
    "flake8",
]


def get_version() -> str:
    locals_dict = {}
    with open(os.path.join(THIS_DIR, "spotlight", "version.py"), "r") as fp:
        exec(fp.read(), globals(), locals_dict)
    return locals_dict["__version__"]  # pytype: disable=invalid-directive


def readme():
    """Load README for use as package's long description."""
    with open(os.path.join(THIS_DIR, "README.md"), "r") as fp:
        return fp.read()


setup(
    name="spotlight",
    version=get_version(),
    author="Kevin",
    author_email="kevinarmandzakka@gmail.com",
    license="MIT",
    description=DESCRIPTION,
    long_description=readme(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    url="https://github.com/kevinzakka/spotlight",
    packages=find_packages(),
    install_requires=[
        "pycairo",
        "PyGObject",
        "py-dict-client",
        "lark",
    ],
    extras_require={
        "dev": DEV_REQUIREMENTS,
    },
    entry_points={"console_scripts": ["spotlight=main:main"]},
)
