from typing import List
def below_zero(operations) -> bool:
    balance = 0

    for op in operations:
        balance += op
        if balance < 0:
            return True

    return False

def test_below_zero():
    assert below_zero([10, -20, 10]) == True
    assert below_zero([10, 20, -30]) == False
    assert below_zero([10, -10, 20, -30]) == True
    assert below_zero([10, 20, 30]) == False
    assert below_zero([-10, 20, -30]) == True
    assert below_zero([]) == False