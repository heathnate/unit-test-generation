import pytest
from typing import List

def mean_absolute_deviation(numbers: List[float]) -> float:
    mean = sum(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)

def test_mean_absolute_deviation_normal():
    assert mean_absolute_deviation([1, 2, 3, 4, 5]) == 1.2
    assert mean_absolute_deviation([5, 5, 5, 5, 5]) == 0.0
    assert mean_absolute_deviation([-1, -2, -3, -4, -5]) == 1.2

def test_mean_absolute_deviation_edge():
    assert mean_absolute_deviation([1]) == 0.0
    assert mean_absolute_deviation([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 0.0
    assert mean_absolute_deviation([0, 0, 0, 0, 0]) == 0.0

def test_mean_absolute_deviation_error():
    with pytest.raises(ZeroDivisionError):
        mean_absolute_deviation([])
    with pytest.raises(TypeError):
        mean_absolute_deviation(None)
    with pytest.raises(TypeError):
        mean_absolute_deviation("12345")