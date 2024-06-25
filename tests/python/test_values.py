"""
:file: test_values.py

:date: 2024/06/25
:author: Bryan Gillis

Mock unit tests of functions which fail on certain values.
"""

import math
import pytest

def my_floor(x):
  """Mock implementation of a "floor" function, which fails on negative non-integer values.
  """
  return int(x)

@pytest.fixture
def test_values_pass():
  return [0.5, 1.0, 0.0, 1.1, 2.3, 100000, 1e99]

@pytest.fixture
def test_values_fail():
  return [0, 0.0, 1.0, 1.2, 1.9, -1.0, -1.5, -1.9, -2]

@pytest.fixture
def test_values_err():
  return [0, 0.0, math.nan]

def _test_my_floor(_test_values):
  """Common implementation of tests.
  """
  for x in _test_values:
    assert my_floor(x)==math.floor(x), f"my_floor failed for input {x}"

def test_my_floor_pass(test_values_pass):
  """Mock unit test for `my_floor` which is expected to pass.
  """
  _test_my_floor(test_values_pass)

def test_my_floor_fail(test_values_fail):
  """Mock unit test for `my_floor` which is expected to fail.
  """
  _test_my_floor(test_values_fail)

def test_my_floor_err(test_values_err):
  """Mock unit test for `my_floor` which is expected to raise an exception other than an AssertionError.
  """
  _test_my_floor(test_values_err)

def test_my_floor(test_values):
  """Mock unit test which runs on a set of test values from a flexible fixture.
  """
  _test_my_floor(test_values)

@pytest.mark.skip
def test_my_floor_skip():
  """Mock unit test which is skipped
  """
  pass