import pytest

def test_truncate_number():
    assert truncate_number(1.2345) == 0.2345
    assert truncate_number(0.9999) == 0.9999
    assert truncate_number(3.0) == 0.0
    assert truncate_number(4.5678) == 0.5678

def test_truncate_number_negative():
    assert truncate_number(-1.2345) == 0.7655
    assert truncate_number(-0.9999) == 0.0001
    assert truncate_number(-3.0) == 0.0
    assert truncate_number(-4.5678) == 0.4322

def test_truncate_number_edge_cases():
    assert truncate_number(0.0) == 0.0
    assert truncate_number(1.0) == 0.0
    assert truncate_number(-1.0) == 0.0

def test_truncate_number_error_cases():
    with pytest.raises(TypeError):
        truncate_number("1.2345")
    with pytest.raises(TypeError):
        truncate_number(None)
    with pytest.raises(TypeError):
        truncate_number([])
    with pytest.raises(TypeError):
        truncate_number({})