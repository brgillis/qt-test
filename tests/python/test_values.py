"""
:file: test_values.py

:date: 2024/06/25
:author: Bryan Gillis

Mock implementation and unit tests of a function `my_floor` which is known to fail on certain values (any non-integer
negative value), to aid in demonstrating the Qt interface for running unit tests.
"""

import math

import pytest

def my_floor(x):
  """Mock implementation of a "floor" function, which fails on any non-integer negative values.
  """
  return int(x)

@pytest.fixture
def test_values_pass():
  """Fixture providing a set of values which it is known that the mock function works correctly on.
  """
  return [0.5, 1.0, 0.0, 1.1, 2.3, 100000, 1e99]

@pytest.fixture
def test_values_fail():
  """Fixture providing a set of values, including some which it is known the mock function works incorrectly on.
  """
  return [0, 0.0, 1.0, 1.2, 1.9, -1.0, -1.5, -1.9, -2]

@pytest.fixture
def test_values_err():
  """Fixture providing a set of values, including one which it is known the function will raise an exception for.
  """
  return [0, 0.0, math.nan]

def _test_my_floor(_test_values):
  """Common implementation of all different unit tests. The mock function is run on each value, and the result is
  compared with the results of the built-in `math.floor` function.
  """
  for x in map(float,_test_values):
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
  """Mock unit test which runs on a set of test values from a flexible fixture (defined in conftest.py). The values
  provided to this fixture can be set by passing a list of values in the invocation of pytest through e.g.
  `... --test values 0 1 2 3`. If no custom values are provided, a default list of values will be used where the
  function will pass the test.
  """
  _test_my_floor(test_values)

@pytest.mark.skip
def test_my_floor_skip():
  """Mock unit test which is skipped.
  """
  pass