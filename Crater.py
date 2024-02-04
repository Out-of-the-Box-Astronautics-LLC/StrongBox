#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
"""
#  Data structure to define the name, size, and location of Moon craters

# Disable PyLint (VSCode) linting messages that seem unuseful
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name
# pylint: disable=global-statement
#
# Disable Pyright (Zed IDE) linting messages that seem unuseful
# https://pypi.org/project/pyright/
# TODO https://github.com/microsoft/pyright/blob/main/docs/getting-started.md
# PYRIGHT_PYTHON_IGNORE_WARNINGS = True
# Using Command Line Interface (CLI): pyright --verifytypes TODO --ignoreexternal MainApp.py

class Crater:

    def __init__(self, name: str, size: float, location: tuple):
        self.name = name
        self.size = size
        self.xCoordinate = location[0]
        self.yCoordinate = location[1]
