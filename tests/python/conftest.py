"""
:file: conftest.py

:date: 2024/06/25
:author: Bryan Gillis

Common code to be run by pytest for all unit tests.
"""

import pytest

def pytest_addoption(parser):
  """Function called automatically by pytest to add an option to its command-line invocation. This option allows the
  user to specify a list of values which will be used for one of the unit tests.
  """
  parser.addoption("--test_values", nargs="+", default=[0, 1, 1.0, 1.5], type=str)
  