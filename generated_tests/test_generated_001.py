from typing import List
def has_close_elements(numbers, threshold) -> bool:
    for idx, elem in enumerate(numbers):
        for idx2, elem2 in enumerate(numbers):
            if idx != idx2:
                distance = abs(elem - elem2)
                if distance < threshold:
                    return True

    return False

def test_has_close_elements():
    assert has_close_elements([1, 2, 3, 4, 5], 1) == True
    assert has_close_elements([1, 2, 3, 4, 5], 0.5) == False
    assert has_close_elements([10, 20, 30, 40, 50], 10) == True
    assert has_close_elements([10, 20, 30, 40, 50], 11) == False
    assert has_close_elements([-1, -2, -3, -4, -5], 1) == True
    assert has_close_elements([-1, -2, -3, -4, -5], 0.5) == False
    assert has_close_elements([], 1) == False