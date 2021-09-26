#!/bin/bash

# Bash settings: fail on any error and display all commands being run.
set -e
set -x

N_CPU=$(grep -c ^processor /proc/cpuinfo)
SRC_FILES=(spotlight/ setup.py)

# Set up a virtual environment.
python -m venv spotlight_testing
source spotlight_testing/bin/activate

# Install dependencies.
apt-get update
apt-get install -y libgirepository1.0-dev python3-gi python3-gi-cairo gir1.2-gtk-3.0
pip install --upgrade pip setuptools wheel
pip install -e .[dev]

# Format checking.
flake8 ${SRC_FILES[@]}
black --check ${SRC_FILES}

# Type checking.
pytype -n "${N_CPU}" ${SRC_FILES[@]}

# TODO(kevin): Add pytest checking.

# Clean-up.
deactivate
rm -rf spotlight_testing/
