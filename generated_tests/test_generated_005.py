from typing import List

def mean_absolute_deviation(numbers: List[float]) -> float:
    mean = sum(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)

def test_mean_absolute_deviation():
    assert mean_absolute_deviation([1, 2, 3, 4, 5]) == 1.2
    assert mean_absolute_deviation([0, 0, 0, 0, 0]) == 0.0
    assert mean_absolute_deviation([-1, -2, -3, -4, -5]) == 1.2
    assert mean_absolute_deviation([1, -2, 3, -4, 5]) == 2.8
    assert mean_absolute_deviation([1.5, 2.5, 3.5, 4.5, 5.5]) == 1.2