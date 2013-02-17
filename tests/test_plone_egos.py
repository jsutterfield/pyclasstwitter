import snack_underflow

def test_basic_batch():
    x = [i for i in range(6)]
    result = snack_underflow.divide_ten(x, 3)
    assert(len(result) == 2)