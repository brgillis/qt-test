"""
:file: conftest.py

:date: 2024/06/25
:author: Bryan Gillis

pytest test configuration.
"""

import pytest

def pytest_addoption(parser):
    parser.addoption("--test_values", nargs="+", default=[0, 1, 1.0, 1.5], type=str)


@pytest.fixture
def test_values(request):
    return request.config.getoption("--test_values")