"""
:file: test_values.py

:date: 2024/06/25
:author: Bryan Gillis

Mock unit tests of functions which fail on certain values.
"""

import math

def my_floor(x):
  """Mock implementation of a "floor" function, which fails on negative non-integer values.
  """
  return int(x)

def test_my_floor_pass():
  """Mock unit test for `my_floor` which is expected to pass.
  """

  for x in [0.5, 1.0, 0.0, 1.1, 2.3, 100000, 1e99]:
    assert my_floor(x)==math.floor(x), f"my_floor failed for input {x}"

def test_my_floor_fail():
  """Mock unit test for `my_floor` which is expected to fail.
  """

  for x in [0, 0.0, 1.0, 1.2, 1.9, -1.0, -1.5, -1.9, -2]:
    assert my_floor(x)==math.floor(x), f"my_floor failed for input {x}"

def test_my_floor_err():
  """Mock unit test for `my_floor` which is expected to raise an exception.
  """

  for x in [0, 0.0, "0", "0.5"]:
    assert my_floor(x)==math.floor(x), f"my_floor failed for input {x}"
