"""Install script for setuptools."""

import os

from setuptools import find_packages, setup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def get_version() -> str:
    locals_dict = {}
    with open(os.path.join(THIS_DIR, "spotlight", "version.py"), "r") as fp:
        exec(fp.read(), globals(), locals_dict)
    return locals_dict["__version__"]  # pytype: disable=invalid-directive


setup(
    name="spotlight",
    version=get_version(),
    description="A spotlight-equivalent for Linux.",
    author="Kevin",
    author_email="kevinarmandzakka@gmail.com",
    license="MIT",
    url="https://github.com/kevinzakka/spotlight",
    packages=find_packages(),
    install_requires=[
        "pycairo",
        "PyGObject",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
