import pytest

from src.util.calculator import calculate_ingredient_readiness

# This is a demo test case to assert whether the Pytest execution works correctly. The test should pass.
@pytest.mark.demo
def test_division_by_zero():
    result = calculate_ingredient_readiness(1, 0)

    assert result == 0