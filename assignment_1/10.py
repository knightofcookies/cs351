from typing import List


def generate_squares_upto_n(n: int) -> List:
    return [i**2 for i in range(0, n + 1)]


print(generate_squares_upto_n(5))
