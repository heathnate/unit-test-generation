def truncate_number(number) -> float:
    return number % 1.0

import pytest

def test_truncate_number():
    assert truncate_number(5.6) == 0.6
    assert truncate_number(0.0) == 0.0
    assert truncate_number(1.0) == 0.0
    assert truncate_number(123.456) == 0.456
    assert truncate_number(-1.2) == 0.8
    assert truncate_number(-0.8) == 0.2