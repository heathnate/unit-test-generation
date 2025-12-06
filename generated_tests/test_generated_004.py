import pytest
from typing import List

def below_zero(operations: List[int]) -> bool:
    balance = 0

    for op in operations:
        balance += op
        if balance < 0:
            return True

    return False

def test_below_zero():
    assert below_zero([1, -1, 2, -3]) == True
    assert below_zero([1, 2, 3, 4]) == False
    assert below_zero([-1, -2, -3, -4]) == True
    assert below_zero([0, 0, 0, 0]) == False
    assert below_zero([]) == False

def test_below_zero_edge_cases():
    assert below_zero([1, -2, 3, -4]) == True
    assert below_zero([-1, 2, -3, 4]) == True
    assert below_zero([1, -1, 1, -1]) == False
    assert below_zero([-1, 1, -1, 1]) == True

def test_below_zero_error_cases():
    with pytest.raises(TypeError):
        below_zero(None)
    with pytest.raises(TypeError):
        below_zero("string")
    with pytest.raises(TypeError):
        below_zero(123)